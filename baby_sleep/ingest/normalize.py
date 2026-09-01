"""Normalize adapter output into a clean canonical SleepLog:
resolve midnight crossings, reconcile durations, classify nap vs night,
and drop impossible rows (D15 sanity pre-filter)."""
from __future__ import annotations

from datetime import datetime, time, timedelta

from baby_sleep.contract.enums import DataQuality, SleepType, StartMarker
from baby_sleep.contract.models import SleepLog, SleepSession

MAX_SANE_MINUTES = 20 * 60
OVERLAP_REPAIR_NOTE_FRACTION = 0.20   # >20% of sessions needing overlap repair => data-quality note

# Forgot-to-stop repair (D15). These are product heuristics, not clinical thresholds.
FORGOT_STOP_NIGHT_HOURS = 13            # a "night" longer than this reads as a left-running timer
FORGOT_STOP_LATE_END = (9, 30)          # ...or one that ends after 09:30 local ...
FORGOT_STOP_LATE_END_MIN_HOURS = 11     # ... while still running past 11h
MIN_CLEAN_NIGHTS_FOR_REPAIR = 3         # need this many clean nights to infer a morning wake


def resolve_end(
    start: datetime, end: datetime | None, duration_minutes: int | None
) -> tuple[datetime | None, int | None]:
    """Return a consistent (end, duration_minutes). If end is time-only and lands
    before start, roll it to the next day. If only duration is known, compute end;
    if only end is known, compute duration."""
    if end is not None and end < start:
        end = end + timedelta(days=1)
    if end is None and duration_minutes is not None:
        end = start + timedelta(minutes=duration_minutes)
    if duration_minutes is None and end is not None:
        duration_minutes = int((end - start).total_seconds() // 60)
    return end, duration_minutes


def is_sane(start: datetime, end: datetime | None, duration_minutes: int | None) -> bool:
    """Reject un-analyzable or impossible sessions: no end AND no duration (nothing to
    measure), non-positive or >20h duration, or end before start."""
    if end is None and duration_minutes is None:
        return False
    if end is not None and end < start:
        return False
    return duration_minutes is None or (0 < duration_minutes <= MAX_SANE_MINUTES)


NIGHT_START_HOUR = 19          # 7pm or later ...
NIGHT_END_HOUR = 5             # ... or before 5am
LONG_SLEEP_MINUTES = 4 * 60    # a long consolidated stretch reads as night


def classify_sleep_type(
    start: datetime, duration_minutes: int | None, crosses_midnight: bool
) -> SleepType:
    """Deterministic nap/night rule. Night if it crosses midnight, or begins in the
    night window (>=19:00 or <05:00) and is a long consolidated stretch."""
    if crosses_midnight:
        return SleepType.NIGHT
    in_night_window = start.hour >= NIGHT_START_HOUR or start.hour < NIGHT_END_HOUR
    if in_night_window and (duration_minutes or 0) >= LONG_SLEEP_MINUTES:
        return SleepType.NIGHT
    return SleepType.NAP


def _effective_marks(marks: StartMarker, convention: StartMarker | None) -> StartMarker:
    """A session's own marker wins; fall back to the family convention for UNKNOWN."""
    if marks is not StartMarker.UNKNOWN:
        return marks
    return convention or StartMarker.UNKNOWN


def _is_forgot_to_stop(s: SleepSession) -> bool:
    """A night whose duration betrays a timer left running past the real morning wake."""
    if s.sleep_type is not SleepType.NIGHT or s.duration_minutes is None:
        return False
    if s.duration_minutes > FORGOT_STOP_NIGHT_HOURS * 60:
        return True
    end = s.end.value if s.end is not None else None
    if end is not None and (end.hour, end.minute) > FORGOT_STOP_LATE_END:
        return s.duration_minutes > FORGOT_STOP_LATE_END_MIN_HOURS * 60
    return False


def _repair_forgot_to_stop(
    sessions: list[SleepSession],
) -> tuple[list[SleepSession], list[str]]:
    """Repair forgot-to-stop nights (D15). Truncate a left-running night's end to the
    child's typical morning wake — the median end-of-day across the *clean* nights in the
    same log — when at least ``MIN_CLEAN_NIGHTS_FOR_REPAIR`` clean nights exist; mark the
    repaired end ``INFERRED`` and warn. With too little clean history to infer a wake time,
    reset: drop the bad night with a warning rather than keep or guess at it."""
    flagged = {i for i, s in enumerate(sessions) if _is_forgot_to_stop(s)}
    if not flagged:
        return sessions, []
    clean_wakes = sorted(
        s.end.value.hour * 60 + s.end.value.minute
        for i, s in enumerate(sessions)
        if i not in flagged and s.sleep_type is SleepType.NIGHT and s.end is not None)
    median_wake = clean_wakes[len(clean_wakes) // 2] if (
        len(clean_wakes) >= MIN_CLEAN_NIGHTS_FOR_REPAIR) else None

    out: list[SleepSession] = []
    warnings: list[str] = []
    for i, s in enumerate(sessions):
        if i not in flagged:
            out.append(s)
            continue
        if median_wake is None:
            warnings.append(
                f"dropped forgot-to-stop night starting {s.start.value.isoformat()} "
                "(insufficient clean-night history to repair)")
            continue
        start = s.start.value
        repaired_end = datetime.combine(start.date(), time(median_wake // 60, median_wake % 60))
        if repaired_end <= start:
            repaired_end = repaired_end + timedelta(days=1)
        new_duration = int((repaired_end - start).total_seconds() // 60)
        warnings.append(
            f"repaired forgot-to-stop night: truncated end from {s.end.value.isoformat()} to "
            f"{repaired_end.isoformat()} (inferred from typical morning wake)")
        out.append(s.model_copy(update={
            "end": s.end.model_copy(update={"value": repaired_end}),
            "duration_minutes": new_duration,
            "data_quality": DataQuality.INFERRED,
        }))
    return out, warnings


def _resolve_overlaps(
    sessions: list[SleepSession],
) -> tuple[list[SleepSession], list[str]]:
    """Detect and repair overlapping sessions (D15), preserving original order.

    A session fully contained in an earlier one is a double-log and is dropped; a
    partial overlap has its start trimmed forward to the earlier session's end (its
    duration recomputed, marked ``INFERRED``). Every action emits a warning naming both
    timestamps, and a data-quality note fires if more than 20% of sessions needed a fix.
    """
    if not sessions:
        return sessions, []
    order = sorted(range(len(sessions)), key=lambda i: sessions[i].start.value)
    actions: dict[int, tuple[str, datetime | None]] = {}
    warnings: list[str] = []
    fixed = 0
    frontier_end: datetime | None = None
    for i in order:
        s = sessions[i]
        s_start = s.start.value
        s_end = s.end.value if s.end is not None else None
        if frontier_end is not None and s_start < frontier_end:
            if s_end is not None and s_end <= frontier_end:
                actions[i] = ("drop", None)
                warnings.append(
                    f"dropped overlapping session {s_start.isoformat()}–{s_end.isoformat()} "
                    "contained within an earlier session")
                fixed += 1
                continue
            actions[i] = ("trim", frontier_end)
            warnings.append(
                f"trimmed overlapping session start from {s_start.isoformat()} to "
                f"{frontier_end.isoformat()} (overlaps an earlier session)")
            fixed += 1
            if s_end is not None:
                frontier_end = max(frontier_end, s_end)
        elif s_end is not None:
            frontier_end = s_end if frontier_end is None else max(frontier_end, s_end)

    kept: list[SleepSession] = []
    for i, s in enumerate(sessions):
        act = actions.get(i)
        if act is None:
            kept.append(s)
        elif act[0] == "drop":
            continue
        else:  # trim
            new_start = act[1]
            s_end = s.end.value if s.end is not None else None
            new_duration = (
                int((s_end - new_start).total_seconds() // 60) if s_end is not None else None)
            kept.append(s.model_copy(update={
                "start": s.start.model_copy(update={"value": new_start}),
                "duration_minutes": new_duration,
                "data_quality": DataQuality.INFERRED,
            }))
    if fixed / len(sessions) > OVERLAP_REPAIR_NOTE_FRACTION:
        warnings.append(
            f"data quality: {fixed} of {len(sessions)} sessions needed overlap repair "
            "(>20%) — baseline reliability reduced")
    return kept, warnings


def normalize(
    log: SleepLog, start_convention: StartMarker | None = None
) -> tuple[SleepLog, list[str]]:
    """Return a cleaned copy of the log plus human-readable warnings.

    Canonical ``start`` means ASLEEP. When a session's effective start marker is
    PUT_DOWN and sleep-onset latency is known, shift ``start`` forward to the
    asleep time (recording ``put_down_at`` and trimming duration); the SOL is kept
    in ``onset_latency_minutes`` and never discarded. PUT_DOWN without a known SOL
    is preserved and flagged uncertain. Impossible rows are dropped with a warning.
    """
    kept: list[SleepSession] = []
    warnings: list[str] = []
    for s in log.sessions:
        start = s.start.value
        end = s.end.value if s.end is not None else None
        end, duration = resolve_end(start, end, s.duration_minutes)

        put_down_at = s.put_down_at
        marks = _effective_marks(s.start_marks, start_convention)
        onset = s.onset_latency_minutes
        if marks is StartMarker.PUT_DOWN and onset is not None:
            put_down_at = s.start.model_copy()             # preserve original anchor's precision/raw
            start = start + timedelta(minutes=onset)       # canonical start = asleep
            if end is not None:
                duration = int((end - start).total_seconds() // 60)
            elif duration is not None:
                duration = duration - onset
            marks = StartMarker.ASLEEP
        elif marks is StartMarker.PUT_DOWN and onset is None:
            warnings.append(
                "start semantics uncertain (put-down anchor, unknown onset latency) "
                f"for session starting {s.start.value.isoformat()}")

        if end is None and duration is None:
            warnings.append(
                f"dropped session with no end time or duration starting {s.start.value.isoformat()}")
            continue
        if not is_sane(start, end, duration):
            warnings.append(f"dropped impossible sleep session starting {s.start.value.isoformat()}")
            continue
        crosses = end is not None and end.date() > start.date()
        sleep_type = s.sleep_type
        if sleep_type is SleepType.UNKNOWN:
            sleep_type = classify_sleep_type(start, duration, crosses)
        updated = s.model_copy(update={
            "start": s.start.model_copy(update={"value": start}),
            "end": (
                s.end.model_copy(update={"value": end}) if s.end is not None and end is not None
                else s.start.model_copy(update={"value": end}) if end is not None
                else None),
            "duration_minutes": duration,
            "sleep_type": sleep_type,
            "start_marks": marks,
            "put_down_at": put_down_at,
        })
        kept.append(updated)

    kept, forgot_warnings = _repair_forgot_to_stop(kept)
    warnings.extend(forgot_warnings)
    kept, overlap_warnings = _resolve_overlaps(kept)
    warnings.extend(overlap_warnings)
    return log.model_copy(update={"sessions": kept}), warnings
