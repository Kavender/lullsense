from datetime import date, datetime

from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.analyze.models import Baseline, BaselineStatus, Confidence, FeatureBaseline
from baby_sleep.contract.enums import SleepType
from baby_sleep.contract.models import Child, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime


def test_feature_baseline_defaults():
    fb = FeatureBaseline(feature="rise_time_min", baseline_median=390.0, mad=12.0, n=10)
    assert fb.source == "history"
    assert fb.confidence is Confidence.MEDIUM
    assert fb.deviation is None


def test_baseline_roundtrip():
    b = Baseline(status=BaselineStatus.COMPUTED, prior_window_days=14, recent_window_days=5,
                 features={"rise_time_min": FeatureBaseline(
                     feature="rise_time_min", baseline_median=390.0, mad=12.0, n=10)})
    restored = Baseline.model_validate(b.model_dump())
    assert restored.status is BaselineStatus.COMPUTED
    assert restored.features["rise_time_min"].baseline_median == 390.0


def _series_over_days(n, rise_hour=6, rise_min=0):
    # n consecutive nights, each ~11h, rising at a fixed time -> tight baseline
    sessions = []
    for i in range(n):
        d = 1 + i
        sessions.append(SleepSession(
            start=ApproxTime(value=datetime(2026, 9, d, 19, 30)),
            end=ApproxTime(value=datetime(2026, 9, d + 1, rise_hour, rise_min)),
            duration_minutes=(rise_hour * 60 + rise_min) + (24 - 19) * 60 - 30,
            sleep_type=SleepType.NIGHT))
    return build_feature_series(SleepLog(sessions=sessions))


def test_baseline_below_supported_range():
    series = _series_over_days(10)
    b = build_baseline(series, Child(age_months=3))
    assert b.status.value == "below_supported_range"
    assert b.features == {}
    assert b.reason


def test_baseline_age_unknown():
    series = _series_over_days(10)
    b = build_baseline(series, Child())
    assert b.status.value == "age_unknown"


def test_baseline_insufficient_data():
    series = _series_over_days(3)      # < MIN_BASELINE_DAYS usable prior days
    b = build_baseline(series, Child(age_months=10))
    assert b.status.value == "insufficient_data"


def test_baseline_computed_detects_recent_shift():
    # 10 stable days rising 06:00, then 4 recent days rising 05:00 (60 min earlier)
    late_sessions = []
    for i in range(4):
        d = 12 + i
        late_sessions.append(SleepSession(
            start=ApproxTime(value=datetime(2026, 9, d, 19, 30)),
            end=ApproxTime(value=datetime(2026, 9, d + 1, 5, 0)),
            duration_minutes=570, sleep_type=SleepType.NIGHT))
    from baby_sleep.contract.models import SleepLog as _L
    # rebuild one combined series
    combined = _L(sessions=[
        *[SleepSession(start=ApproxTime(value=datetime(2026, 9, 1 + i, 19, 30)),
                       end=ApproxTime(value=datetime(2026, 9, 2 + i, 6, 0)),
                       duration_minutes=630, sleep_type=SleepType.NIGHT) for i in range(10)],
        *late_sessions])
    series = build_feature_series(combined)
    b = build_baseline(series, Child(age_months=10), prior_window_days=10, recent_window_days=4)
    assert b.status.value == "computed"
    rt = b.features["rise_time_min"]
    assert rt.baseline_median == 360.0                 # 06:00
    assert rt.recent_median == 300.0                   # 05:00
    assert rt.deviation == -60.0                       # 60 min earlier


def test_confidence_high_when_many_tight_days():
    # 19 tight, exact days: after reserving the 5-day recent window, a full 14-day prior
    # remains -> coverage 1.0 + zero dispersion -> HIGH.
    series = _series_over_days(19)
    b = build_baseline(series, Child(age_months=12), prior_window_days=14, recent_window_days=5)
    assert b.features["rise_time_min"].confidence.value == "high"


def test_baseline_disjoint_windows_surface_short_history_shift():
    # regression (review I2): 3 stable days rising 06:00 then 5 days rising 05:00.
    # Prior and recent windows must be disjoint or the recent shift is masked to 0.
    from baby_sleep.contract.models import SleepLog
    sessions = [
        *[SleepSession(start=ApproxTime(value=datetime(2026, 9, 1 + i, 19, 30)),
                       end=ApproxTime(value=datetime(2026, 9, 2 + i, 6, 0)),
                       duration_minutes=630, sleep_type=SleepType.NIGHT) for i in range(3)],
        *[SleepSession(start=ApproxTime(value=datetime(2026, 9, 4 + i, 19, 30)),
                       end=ApproxTime(value=datetime(2026, 9, 5 + i, 5, 0)),
                       duration_minutes=570, sleep_type=SleepType.NIGHT) for i in range(5)],
    ]
    series = build_feature_series(SleepLog(sessions=sessions))
    b = build_baseline(series, Child(age_months=10))     # default windows 14/5
    assert b.status.value == "computed"
    rt = b.features["rise_time_min"]
    assert rt.baseline_median == 360.0                   # 06:00 from the 3 prior days
    assert rt.recent_median == 300.0                     # 05:00 from the 5 recent days
    assert rt.deviation == -60.0                         # the shift is surfaced, not masked


def test_stated_baseline_fallback_is_low_confidence():
    series = _series_over_days(2)       # not enough history
    b = build_baseline(series, Child(age_months=12), stated={"rise_time_min": 390.0})
    assert b.status.value == "computed"
    fb = b.features["rise_time_min"]
    assert fb.source == "self_reported"
    assert fb.confidence.value == "low"
    assert fb.baseline_median == 390.0


def test_baseline_includes_waso_and_longest_waking():
    from baby_sleep.contract.enums import SleepType
    from baby_sleep.contract.models import SleepLog, SleepSession
    from baby_sleep.contract.time_types import ApproxTime
    # 10 fragmented nights: onset 19:30, wake 00:00-00:40 (40 min WASO), up 06:00
    sessions = []
    for i in range(10):
        d = 1 + i
        sessions.append(SleepSession(start=ApproxTime(value=datetime(2026, 9, d, 19, 30)),
                                     end=ApproxTime(value=datetime(2026, 9, d + 1, 0, 0)),
                                     duration_minutes=270, sleep_type=SleepType.NIGHT))
        sessions.append(SleepSession(start=ApproxTime(value=datetime(2026, 9, d + 1, 0, 40)),
                                     end=ApproxTime(value=datetime(2026, 9, d + 1, 6, 0)),
                                     duration_minutes=320, sleep_type=SleepType.NIGHT))
    series = build_feature_series(SleepLog(sessions=sessions))
    b = build_baseline(series, Child(age_months=10), prior_window_days=10, recent_window_days=5)
    assert "total_awake_overnight_min" in b.features
    assert "longest_night_waking_min" in b.features
    assert b.features["total_awake_overnight_min"].baseline_median == 40.0


def test_feature_scalar_public():
    from baby_sleep.analyze import feature_scalar
    from baby_sleep.analyze.models import DailyFeatures
    f = DailyFeatures(day=date(2026, 9, 1), night_waking_count=2, total_awake_overnight_min=40)
    assert feature_scalar("night_waking_count", f) == 2.0
    assert feature_scalar("total_awake_overnight_min", f) == 40.0
