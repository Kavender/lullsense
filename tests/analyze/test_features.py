from datetime import datetime

from baby_sleep.analyze.daymap import segment_days
from baby_sleep.analyze.features import compute_daily_features
from baby_sleep.analyze.models import BaselineStatus, Confidence
from baby_sleep.analyze.robust import iqr, mad, median
from baby_sleep.contract.enums import DataQuality, Location, SleepType
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime, TimePrecision


def test_robust_stats_basic():
    assert median([1, 2, 3, 4]) == 2.5
    assert median([]) is None
    # MAD of [1,2,3,4,100]: median=3, deviations=[2,1,0,1,97] -> median=1
    assert mad([1, 2, 3, 4, 100]) == 1
    assert mad([]) is None
    # IQR of 1..9 (Q3=7, Q1=3) -> 4
    assert iqr([1, 2, 3, 4, 5, 6, 7, 8, 9]) == 4
    assert iqr([]) is None


def test_enum_values_stable():
    assert {c.value for c in Confidence} == {"low", "medium", "high"}
    assert BaselineStatus.BELOW_SUPPORTED_RANGE.value == "below_supported_range"


def _night(sh, smin, eh, emin, dur, wakings=None, segs=None):
    return SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, sh, smin)),
                        end=ApproxTime(value=datetime(2026, 8, 25, eh, emin)),
                        duration_minutes=dur, sleep_type=SleepType.NIGHT,
                        night_wakings=wakings)


def _nap(sd, sh, smin, ed, eh, emin, dur):
    return SleepSession(start=ApproxTime(value=datetime(2026, 8, sd, sh, smin)),
                        end=ApproxTime(value=datetime(2026, 8, ed, eh, emin)),
                        duration_minutes=dur, sleep_type=SleepType.NAP)


def test_single_night_and_naps_totals():
    night = _night(19, 36, 6, 0, 624, wakings=1)
    nap1 = _nap(25, 9, 30, 25, 10, 5, 35)      # 09:30 -> 10:05, 35 min
    nap2 = _nap(25, 13, 0, 25, 14, 20, 80)     # 13:00 -> 14:20, 80 min
    day = segment_days(SleepLog(sessions=[night, nap1, nap2]))[0]
    f = compute_daily_features(day)
    assert f.sleep_onset_time == datetime(2026, 8, 24, 19, 36)
    assert f.rise_time == datetime(2026, 8, 25, 6, 0)
    assert f.night_sleep_duration_min == 624
    assert f.night_waking_count == 1          # from the field (single segment)
    assert f.total_awake_overnight_min is None
    assert f.nap_count == 2
    assert f.total_daytime_sleep_min == 115   # 35 + 80
    assert f.total_24h_sleep_min == 624 + 115


def test_fragmented_night_waso_from_gaps():
    seg1 = SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 19, 36)),
                        end=ApproxTime(value=datetime(2026, 8, 25, 1, 0)),
                        duration_minutes=324, sleep_type=SleepType.NIGHT)
    seg2 = SleepSession(start=ApproxTime(value=datetime(2026, 8, 25, 1, 40)),
                        end=ApproxTime(value=datetime(2026, 8, 25, 6, 0)),
                        duration_minutes=260, sleep_type=SleepType.NIGHT)
    day = segment_days(SleepLog(sessions=[seg1, seg2]))[0]
    f = compute_daily_features(day)
    assert f.night_sleep_duration_min == 584          # 324 + 260 (asleep only)
    assert f.night_waking_count == 1                  # one gap
    assert f.total_awake_overnight_min == 40          # the 01:00->01:40 gap
    assert f.longest_night_waking_min == 40
    assert f.sleep_onset_time == datetime(2026, 8, 24, 19, 36)
    assert f.rise_time == datetime(2026, 8, 25, 6, 0)


def test_in_bed_uses_put_down_when_present():
    night = SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 19, 36)),
                         end=ApproxTime(value=datetime(2026, 8, 25, 6, 0)),
                         duration_minutes=624, sleep_type=SleepType.NIGHT,
                         onset_latency_minutes=15,
                         put_down_at=ApproxTime(value=datetime(2026, 8, 24, 19, 21)))
    day = segment_days(SleepLog(sessions=[night]))[0]
    f = compute_daily_features(day)
    assert f.in_bed_time == datetime(2026, 8, 24, 19, 21)
    assert f.sleep_onset_latency_min == 15


def test_wake_windows_intra_day_and_pre_nap():
    night = _night(19, 36, 6, 0, 624)
    nap1 = _nap(25, 9, 30, 25, 10, 5, 35)     # rise 06:00 -> nap1 09:30 = 210 min
    nap2 = _nap(25, 13, 0, 25, 14, 20, 80)    # nap1 end 10:05 -> nap2 13:00 = 175 min
    day = segment_days(SleepLog(sessions=[night, nap1, nap2]))[0]
    f = compute_daily_features(day)
    assert f.pre_nap_awake_min == [210, 175]
    assert f.wake_windows_min[:2] == [210, 175]   # terminal window appended later at series level


def test_is_weekend_and_location():
    # 2026-08-29 is a Saturday
    sat_night = SleepSession(start=ApproxTime(value=datetime(2026, 8, 28, 19, 30)),
                             end=ApproxTime(value=datetime(2026, 8, 29, 6, 30)),
                             duration_minutes=660, sleep_type=SleepType.NIGHT,
                             location=Location.HOME)
    day = segment_days(SleepLog(sessions=[sat_night]))[0]
    f = compute_daily_features(day)
    assert f.is_weekend is True
    assert f.location is Location.HOME


def test_approx_share_lowers_day_confidence():
    night = SleepSession(
        start=ApproxTime(value=datetime(2026, 8, 24, 19, 30),
                         precision=TimePrecision.APPROXIMATE, uncertainty_minutes=15),
        end=ApproxTime(value=datetime(2026, 8, 25, 6, 30)),
        duration_minutes=660, sleep_type=SleepType.NIGHT,
        data_quality=DataQuality.REPORTED)
    day = segment_days(SleepLog(sessions=[night]))[0]
    f = compute_daily_features(day)
    assert f.approx_share == 1.0
    assert f.day_confidence is not None
