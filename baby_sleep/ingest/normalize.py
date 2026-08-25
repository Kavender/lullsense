"""Normalize adapter output into a clean canonical SleepLog:
resolve midnight crossings, reconcile durations, classify nap vs night,
and drop impossible rows (D15 sanity pre-filter)."""
from __future__ import annotations

from datetime import datetime, timedelta

from baby_sleep.contract.enums import SleepType

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
    if duration_minutes is not None:
        if duration_minutes <= 0 or duration_minutes > MAX_SANE_MINUTES:
            return False
    return True
