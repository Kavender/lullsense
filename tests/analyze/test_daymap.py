from datetime import date, datetime

from baby_sleep.analyze.daymap import segment_days, wake_day
from baby_sleep.contract.enums import EventKind, SleepType
from baby_sleep.contract.models import ContextEvent, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime


def _sess(sy, sm, sd, sh, smin, ey, em, ed, eh, emin, typ):
    return SleepSession(
        start=ApproxTime(value=datetime(sy, sm, sd, sh, smin)),
        end=ApproxTime(value=datetime(ey, em, ed, eh, emin)),
        sleep_type=typ)


def test_wake_day_cutover():
    # after 3am -> same date; before 3am -> previous date
    assert wake_day(datetime(2026, 8, 25, 6, 30)) == date(2026, 8, 25)
    assert wake_day(datetime(2026, 8, 25, 2, 30)) == date(2026, 8, 24)
    assert wake_day(datetime(2026, 8, 25, 3, 0)) == date(2026, 8, 25)


def test_night_attributed_to_wake_up_day():
    # night starts 24th 19:36, ends 25th 06:00 -> wake-day 25th
    night = _sess(2026, 8, 24, 19, 36, 2026, 8, 25, 6, 0, SleepType.NIGHT)
    nap = _sess(2026, 8, 25, 13, 0, 2026, 8, 25, 14, 20, SleepType.NAP)
    days = segment_days(SleepLog(sessions=[night, nap]))
    assert len(days) == 1
    d = days[0]
    assert d.day == date(2026, 8, 25)
    assert len(d.night_segments) == 1 and len(d.naps) == 1


def test_two_nights_two_days_sorted():
    n1 = _sess(2026, 8, 23, 20, 0, 2026, 8, 24, 6, 30, SleepType.NIGHT)
    n2 = _sess(2026, 8, 24, 19, 36, 2026, 8, 25, 6, 0, SleepType.NIGHT)
    days = segment_days(SleepLog(sessions=[n2, n1]))     # unsorted input
    assert [d.day for d in days] == [date(2026, 8, 24), date(2026, 8, 25)]


def test_events_attached_by_wake_day():
    night = _sess(2026, 8, 24, 19, 36, 2026, 8, 25, 6, 0, SleepType.NIGHT)
    ev = ContextEvent(kind=EventKind.FEED, at=ApproxTime(value=datetime(2026, 8, 25, 11, 20)))
    days = segment_days(SleepLog(sessions=[night], events=[ev]))
    assert len(days[0].events) == 1


def test_fragmented_night_segments_kept_together():
    seg1 = _sess(2026, 8, 24, 19, 36, 2026, 8, 25, 1, 0, SleepType.NIGHT)
    seg2 = _sess(2026, 8, 25, 1, 40, 2026, 8, 25, 6, 0, SleepType.NIGHT)   # after a waking
    days = segment_days(SleepLog(sessions=[seg1, seg2]))
    assert len(days) == 1
    assert len(days[0].night_segments) == 2
