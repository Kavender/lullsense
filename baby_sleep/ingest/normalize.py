"""Normalize adapter output into a clean canonical SleepLog:
resolve midnight crossings, reconcile durations, classify nap vs night,
and drop impossible rows (D15 sanity pre-filter)."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import UTC, datetime, time, timedelta, timezone
from typing import Annotated, Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, PlainSerializer

from baby_sleep.contract.enums import DataQuality, SleepType, StartMarker
from baby_sleep.contract.models import SleepLog, SleepSession

MAX_SANE_MINUTES = 20 * 60
OVERLAP_REPAIR_NOTE_FRACTION = 0.20   # >20% of sessions needing overlap repair => data-quality note

# Forgot-to-stop repair (D15). These are product heuristics, not clinical thresholds.
FORGOT_STOP_NIGHT_HOURS = 13            # a "night" longer than this reads as a left-running timer
FORGOT_STOP_LATE_END = (9, 30)          # ...or one that ends after 09:30 local ...
FORGOT_STOP_LATE_END_MIN_HOURS = 11     # ... while still running past 11h
MIN_CLEAN_NIGHTS_FOR_REPAIR = 3         # need this many clean nights to infer a morning wake

IsoDatetime = Annotated[datetime, PlainSerializer(lambda d: d.isoformat())]   # offset as-is


class Span(BaseModel):
    model_config = ConfigDict(frozen=True)
    start: IsoDatetime
    end: IsoDatetime | None


class Fix(BaseModel):
    """One repair applied to a session, keyed by its ``record_id`` (CAM-12 §3.4; field
    names are the wire's). ``original`` is the bounds as given to ``normalize`` (without a
    ``record_id``: the bounds before this step); ``derived`` the bounds after this step,
    ``None`` for a drop."""
    model_config = ConfigDict(frozen=True)
    recordId: str | None
    action: Literal["truncate_end", "drop", "trim_start"]
    reason: Literal["forgot_to_stop", "forgot_to_stop_no_history", "implausible_duration",
                    "overlap_contained", "overlap_partial"]
    original: Span
    derived: Span | None
    overlapsRecordId: str | None = None


# (session, action, reason, derived (start, end) | None, overlapped session | None)
FixNote = Callable[..., None]


def _elapsed_minutes(start: datetime, end: datetime) -> int:
    """Real elapsed minutes. Aware datetimes sharing a tzinfo subtract by wall clock in
    Python, which is off by an hour across a DST transition, so compare in UTC."""
    if start.tzinfo is not None and end.tzinfo is not None:
        start, end = start.astimezone(UTC), end.astimezone(UTC)
    return int((end - start).total_seconds() // 60)


def _add_minutes(start: datetime, minutes: int) -> datetime:
    """``start`` plus real elapsed minutes, expressed in ``start``'s own timezone."""
    if start.tzinfo is None:
        return start + timedelta(minutes=minutes)
    return (start.astimezone(UTC) + timedelta(minutes=minutes)).astimezone(start.tzinfo)


def _instant(dt: datetime) -> datetime:
    """Sort/max key that orders aware datetimes by real time (see ``_before``)."""
    return dt.astimezone(UTC) if dt.tzinfo is not None else dt


def _before(a: datetime, b: datetime) -> bool:
    """``a`` strictly before ``b`` in real time. Aware datetimes sharing a tzinfo compare by
    wall clock in Python (fold is ignored), which misorders the repeated DST fall-back hour."""
    if a.tzinfo is not None and b.tzinfo is not None:
        return a.astimezone(UTC) < b.astimezone(UTC)
    return a < b


def _in_own_zone(dt: datetime, s: SleepSession) -> datetime:
    """A derived instant expressed in session ``s``'s own local time (CAM-12 §5.5): the
    offset its IANA ``tz`` has at that instant, as a fixed offset (a wall time inside a
    spring-forward gap resolves to a real instant). Without ``tz`` (adapters) the instant
    is re-expressed in ``s.start``'s own tzinfo; naive values pass through."""
    if s.tz is not None:
        local = dt.astimezone(UTC).astimezone(ZoneInfo(s.tz))   # via UTC: normalises gaps
        return local.astimezone(timezone(local.utcoffset()))
    own = s.start.value.tzinfo
    return dt.astimezone(own) if dt.tzinfo is not None and own is not None else dt


def resolve_end(
    start: datetime, end: datetime | None, duration_minutes: int | None
) -> tuple[datetime | None, int | None]:
    """Return a consistent (end, duration_minutes). If end is time-only and lands
    before start, roll it to the next day. If only duration is known, compute end;
    if only end is known, compute duration."""
    if end is not None and _before(end, start):
        end = end + timedelta(days=1)
    if end is None and duration_minutes is not None:
        end = _add_minutes(start, duration_minutes)
    if duration_minutes is None and end is not None:
        duration_minutes = _elapsed_minutes(start, end)
    return end, duration_minutes


def is_sane(start: datetime, end: datetime | None, duration_minutes: int | None) -> bool:
    """Reject un-analyzable or impossible sessions: no end AND no duration (nothing to
    measure), non-positive or >20h duration, or end before start."""
    if end is None and duration_minutes is None:
        return False
    if end is not None and _before(end, start):
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


def _is_forgot_to_stop(s: SleepSession, awake: int = 0) -> bool:
    """A night whose ASLEEP minutes (duration minus ``awake`` in-bed waking minutes)
    betray a timer left running past the real morning wake."""
    if s.sleep_type is not SleepType.NIGHT or s.duration_minutes is None:
        return False
    asleep = s.duration_minutes - awake
    if asleep > FORGOT_STOP_NIGHT_HOURS * 60:
        return True
    end = s.end.value if s.end is not None else None
    if end is not None and (end.hour, end.minute) > FORGOT_STOP_LATE_END:
        return asleep > FORGOT_STOP_LATE_END_MIN_HOURS * 60
    return False


def _repair_forgot_to_stop(
    sessions: list[SleepSession], note: FixNote | None = None,
    awake_minutes: Mapping[str, int] | None = None,
) -> tuple[list[SleepSession], list[str]]:
    """Repair forgot-to-stop nights (D15). Truncate a left-running night's end to the
    child's typical morning wake — the median end-of-day across the *clean* nights in the
    same log — when at least ``MIN_CLEAN_NIGHTS_FOR_REPAIR`` clean nights exist; mark the
    repaired end ``INFERRED`` and warn. With too little clean history to infer a wake time,
    reset: drop the bad night with a warning rather than keep or guess at it."""
    awake = awake_minutes or {}
    flagged = {i for i, s in enumerate(sessions)
               if _is_forgot_to_stop(s, awake.get(s.record_id, 0))}
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
            if note:
                note(s, "drop", "forgot_to_stop_no_history")
            continue
        start = s.start.value
        wake = time(median_wake // 60, median_wake % 60)
        zone = ZoneInfo(s.tz) if s.tz is not None else start.tzinfo
        day = (start.astimezone(zone) if s.tz is not None else start).date()
        repaired_end = datetime.combine(day, wake, tzinfo=zone)
        if not _before(start, repaired_end):    # a new combine, never a timedelta on aware
            repaired_end = datetime.combine(day + timedelta(days=1), wake, tzinfo=zone)
        if s.tz is not None:
            repaired_end = _in_own_zone(repaired_end, s)
        new_duration = _elapsed_minutes(start, repaired_end)
        warnings.append(
            f"repaired forgot-to-stop night: truncated end from {s.end.value.isoformat()} to "
            f"{repaired_end.isoformat()} (inferred from typical morning wake)")
        if note:
            note(s, "truncate_end", "forgot_to_stop", (start, repaired_end))
        out.append(s.model_copy(update={
            "end": s.end.model_copy(update={"value": repaired_end}),
            "duration_minutes": new_duration,
            "data_quality": DataQuality.INFERRED,
        }))
    return out, warnings


def _resolve_overlaps(
    sessions: list[SleepSession], note: FixNote | None = None,
) -> tuple[list[SleepSession], list[str]]:
    """Detect and repair overlapping sessions (D15), preserving original order.

    A session fully contained in an earlier one is a double-log and is dropped; a
    partial overlap has its start trimmed forward to the earlier session's end (its
    duration recomputed, marked ``INFERRED``). Every action emits a warning naming both
    timestamps, and a data-quality note fires if more than 20% of sessions needed a fix.
    """
    if not sessions:
        return sessions, []
    order = sorted(range(len(sessions)), key=lambda i: _instant(sessions[i].start.value))
    actions: dict[int, tuple[str, datetime | None]] = {}
    warnings: list[str] = []
    fixed = 0
    frontier_end: datetime | None = None
    owner: SleepSession | None = None           # the session whose end is frontier_end
    for i in order:
        s = sessions[i]
        s_start = s.start.value
        s_end = s.end.value if s.end is not None else None
        if frontier_end is not None and _before(s_start, frontier_end):
            if s_end is not None and not _before(frontier_end, s_end):
                actions[i] = ("drop", None)
                warnings.append(
                    f"dropped overlapping session {s_start.isoformat()}–{s_end.isoformat()} "
                    "contained within an earlier session")
                if note:
                    note(s, "drop", "overlap_contained", None, owner)
                fixed += 1
                continue
            new_start = _in_own_zone(frontier_end, s)   # never the earlier record's offset
            actions[i] = ("trim", new_start)
            warnings.append(
                f"trimmed overlapping session start from {s_start.isoformat()} to "
                f"{frontier_end.isoformat()} (overlaps an earlier session)")
            if note:
                note(s, "trim_start", "overlap_partial", (new_start, s_end), owner)
            fixed += 1
        if s_end is not None and (frontier_end is None or _before(frontier_end, s_end)):
            frontier_end, owner = s_end, s

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
                _elapsed_minutes(new_start, s_end) if s_end is not None else None)
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
    log: SleepLog, start_convention: StartMarker | None = None, fixes: list[Fix] | None = None,
    awake_minutes: Mapping[str, int] | None = None,
) -> tuple[SleepLog, list[str]]:
    """Return a cleaned copy of the log plus human-readable warnings.

    Canonical ``start`` means ASLEEP. When a session's effective start marker is
    PUT_DOWN and sleep-onset latency is known, shift ``start`` forward to the
    asleep time (recording ``put_down_at`` and trimming duration); the SOL is kept
    in ``onset_latency_minutes`` and never discarded. PUT_DOWN without a known SOL
    is preserved and flagged uncertain. Impossible rows are dropped with a warning.

    When ``fixes`` is a list, every sanity drop, forgot-to-stop repair and overlap repair
    also appends a structured ``Fix`` to it (CAM-12 §3.4); the return value is unchanged.
    ``awake_minutes`` (``record_id`` -> in-bed waking minutes) makes the forgot-to-stop
    thresholds compare asleep time, not the whole record span.
    """
    note: FixNote | None = None
    if fixes is not None:
        sent = {s.record_id: s for s in log.sessions if s.record_id is not None}

        def note(s, action, reason, derived=None, other=None):
            o = sent.get(s.record_id, s) if s.record_id is not None else s
            fixes.append(Fix(
                recordId=s.record_id, action=action, reason=reason,
                original=Span(start=o.start.value, end=o.end.value if o.end else None),
                derived=Span(start=derived[0], end=derived[1]) if derived else None,
                overlapsRecordId=other.record_id if other is not None else None))
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
            start = _add_minutes(start, onset)             # canonical start = asleep
            if end is not None:
                duration = _elapsed_minutes(start, end)
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
            if note:
                note(s, "drop", "implausible_duration")
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

    kept, forgot_warnings = _repair_forgot_to_stop(kept, note, awake_minutes)
    warnings.extend(forgot_warnings)
    kept, overlap_warnings = _resolve_overlaps(kept, note)
    warnings.extend(overlap_warnings)
    return log.model_copy(update={"sessions": kept}), warnings
