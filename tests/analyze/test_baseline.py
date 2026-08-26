from baby_sleep.analyze.models import Baseline, BaselineStatus, Confidence, FeatureBaseline


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
