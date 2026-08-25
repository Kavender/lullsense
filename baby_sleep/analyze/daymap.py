"""Group a normalized SleepLog into wake-days (morning-anchored, 3am cutover)."""
from __future__ import annotations

from datetime import date, datetime, time, timedelta

from baby_sleep.analyze.models import SleepDay
from baby_sleep.contract.enums import SleepType
from baby_sleep.contract.models import SleepLog

CUTOVER: time = time(3, 0)


def wake_day(dt: datetime) -> date:
    """The calendar date the child is considered to wake up on: the datetime's own
    date, unless it falls before the 03:00 cutover (then the previous day)."""
    return dt.date() if dt.time() >= CUTOVER else dt.date() - timedelta(days=1)


def _anchor_day(session) -> date:
    """Nights are attributed to the morning they (conceptually) end on.
    For a well-formed night, wake_day(end) == wake_day(start) + 1 day.
    For fragmented night segments that end before the 3am cutover, we anchor
    by start+1-day so all segments of the same night fall into the same bucket.
    Naps are attributed by start."""
    if session.sleep_type is SleepType.NIGHT:
        # Use end when available and it's after the cutover (the true morning rise).
        # Fall back to wake_day(start) + 1 day to handle mid-night segments whose
        # end time falls before the 3am cutover.
        if session.end is not None and session.end.value.time() >= CUTOVER:
            return wake_day(session.end.value)
        # Anchor = "the morning after the evening the night started"
        return wake_day(session.start.value) + timedelta(days=1)
    return wake_day(session.start.value)


def segment_days(log: SleepLog) -> list[SleepDay]:
    buckets: dict[date, SleepDay] = {}

    def bucket(d: date) -> SleepDay:
        if d not in buckets:
            buckets[d] = SleepDay(day=d)
        return buckets[d]

    for s in log.sessions:
        d = _anchor_day(s)
        day = bucket(d)
        if s.sleep_type is SleepType.NIGHT:
            day.night_segments.append(s)
        else:
            day.naps.append(s)
    for e in log.events:
        bucket(wake_day(e.at.value)).events.append(e)

    for day in buckets.values():
        day.night_segments.sort(key=lambda s: s.start.value)
        day.naps.sort(key=lambda s: s.start.value)
        day.events.sort(key=lambda e: e.at.value)
    return [buckets[d] for d in sorted(buckets)]
