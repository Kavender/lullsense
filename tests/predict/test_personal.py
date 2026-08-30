from datetime import date, datetime

from baby_sleep.analyze.models import DailyFeatures, FeatureSeries, NapFeature
from baby_sleep.predict.personal import personal_stats_from_series


def _day(d, windows, nap_durs):
    return DailyFeatures(
        day=date(2026, 7, d),
        wake_windows_min=windows,
        naps=[NapFeature(start=datetime(2026, 7, d, 12, 0), duration_minutes=x)
              for x in nap_durs],
        nap_count=len(nap_durs),
    )


def test_personal_stats_stable_after_enough_days():
    series = FeatureSeries(days=[_day(d, [150, 180], [60, 45]) for d in range(1, 8)])
    stats = personal_stats_from_series(series)
    assert stats.days_of_data == 7
    assert stats.stable is True
    assert stats.wake_window_median_min == 165   # median of [150,180]*7
    assert stats.typical_nap_minutes in (45.0, 52.5, 60.0)  # median of nap durations


def test_personal_stats_unstable_when_few_days():
    series = FeatureSeries(days=[_day(d, [150], [60]) for d in range(1, 4)])
    stats = personal_stats_from_series(series)
    assert stats.days_of_data == 3
    assert stats.stable is False


def test_personal_stats_empty_series():
    stats = personal_stats_from_series(FeatureSeries(days=[]))
    assert stats.stable is False
    assert stats.wake_window_median_min is None


def test_personal_stats_uses_only_recent_window():
    # 30 old days with SHORT windows (infancy) + 10 recent days with LONG windows (toddler).
    old = [_day((i % 27) + 1, [90, 100], [40]) for i in range(30)]
    recent = [_day((i % 27) + 1, [300, 320], [90]) for i in range(10)]
    series = FeatureSeries(days=old + recent)
    # recent_days=10 captures exactly the 10 toddler-stage days, excluding all infancy history
    stats = personal_stats_from_series(series, recent_days=10)
    # must reflect the recent long windows, NOT the old short ones
    assert stats.wake_window_median_min == 310   # median of [300,320]*10
    assert stats.days_of_data == 10
    assert stats.stable is True
