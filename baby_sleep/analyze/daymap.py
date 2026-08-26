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
    """A night is attributed to the morning it ends on; naps to the day they start.

    We key a night off its START clock position (not its end), so every segment of one
    fragmented night lands in the SAME wake-day regardless of when each segment ends:
    - an evening/overnight start (>= 03:00 cutover, e.g. 19:36 or a 22:10 resettle after
      an evening waking) -> the NEXT calendar date's morning;
    - a post-midnight start (< 03:00, e.g. a 01:10 resettle) -> that same calendar date's
      morning.
    This is robust to end=None and to evening wakings, which an end-based rule split apart.
    Naps are attributed by start via wake_day()."""
    if session.sleep_type is SleepType.NIGHT:
        start = session.start.value
        return start.date() + timedelta(days=1) if start.time() >= CUTOVER else start.date()
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
