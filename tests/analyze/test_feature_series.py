from datetime import datetime

from baby_sleep.analyze.features import build_feature_series
from baby_sleep.contract.enums import Location, SleepType
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime


def _night(d, sh, smin, ed, eh, emin, dur, loc=Location.UNKNOWN):
    return SleepSession(start=ApproxTime(value=datetime(2026, 8, d, sh, smin)),
                        end=ApproxTime(value=datetime(2026, 8, ed, eh, emin)),
                        duration_minutes=dur, sleep_type=SleepType.NIGHT, location=loc)


def _nap(d, sh, smin, eh, emin, dur):
    return SleepSession(start=ApproxTime(value=datetime(2026, 8, d, sh, smin)),
                        end=ApproxTime(value=datetime(2026, 8, d, eh, emin)),
                        duration_minutes=dur, sleep_type=SleepType.NAP)


def test_series_orders_days_and_computes_variability():
    # three nights -> three wake-days
    sessions = [
        _night(23, 20, 0, 24, 6, 30, 630),
        _night(24, 19, 36, 25, 6, 0, 624),
        _night(25, 20, 30, 26, 6, 30, 600),
    ]
    series = build_feature_series(SleepLog(sessions=sessions))
    assert [d.day.day for d in series.days] == [24, 25, 26]
    assert series.rise_time_variability_min is not None
    assert series.total_sleep_variability_min is not None


def test_terminal_wake_window_stitched_across_days():
    # day 25 last nap ends 25th 14:20; that night's bedtime is 25th 20:30 (belongs to day 26)
    sessions = [
        _night(24, 19, 36, 25, 6, 0, 624),
        _nap(25, 13, 0, 14, 20, 80),
        _night(25, 20, 30, 26, 6, 30, 600),
    ]
    series = build_feature_series(SleepLog(sessions=sessions))
    day25 = next(d for d in series.days if d.day.day == 25)
    # terminal window = 14:20 -> 20:30 = 370 min, appended after the intra-day windows
    assert day25.wake_windows_min[-1] == 370


def test_missing_data_rate_counts_low_days():
    good = _night(24, 19, 36, 25, 6, 0, 624)
    # a day with only a stray nap and no night -> low core data
    lonely_nap = _nap(26, 13, 0, 14, 0, 60)
    series = build_feature_series(SleepLog(sessions=[good, lonely_nap]))
    assert 0.0 < series.missing_data_rate <= 1.0


def test_terminal_wake_window_not_stitched_across_a_data_gap():
    # regression (review I1): a logging gap must NOT produce an absurd multi-day
    # "wake window". Night+nap on the 24th, then the next recorded night is the 4th
    # of next month; the 24th must get no terminal window (its next day is missing).
    night = _night(24, 19, 30, 25, 6, 0, 630)
    nap = _nap(25, 13, 0, 14, 0, 60)
    far_night = SleepSession(start=ApproxTime(value=datetime(2026, 9, 4, 19, 30)),
                             end=ApproxTime(value=datetime(2026, 9, 5, 6, 0)),
                             duration_minutes=630, sleep_type=SleepType.NIGHT)
    series = build_feature_series(SleepLog(sessions=[night, nap, far_night]))
    day25 = next(d for d in series.days if d.day.day == 25)
    # only the (nonexistent) intra-day windows; no giant terminal window appended
    assert all(w < 24 * 60 for w in day25.wake_windows_min)
