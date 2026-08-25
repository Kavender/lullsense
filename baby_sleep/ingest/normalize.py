"""Normalize adapter output into a clean canonical SleepLog:
resolve midnight crossings, reconcile durations, classify nap vs night,
and drop impossible rows (D15 sanity pre-filter)."""
from __future__ import annotations

from datetime import datetime, timedelta

from baby_sleep.contract.enums import SleepType, StartMarker
from baby_sleep.contract.models import SleepLog, SleepSession

MAX_SANE_MINUTES = 20 * 60


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
    """Reject impossible sessions: non-positive or >20h duration, end before start."""
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
    return log.model_copy(update={"sessions": kept}), warnings
