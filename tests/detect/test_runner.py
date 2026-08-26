from baby_sleep.analyze.models import Baseline, BaselineStatus, Confidence, FeatureSeries
from baby_sleep.detect.models import (
    DetectorInput,
    Severity,
    Signal,
    SignalName,
    SignalStatus,
    SignalWindow,
)


def test_signal_model_defaults_and_roundtrip():
    s = Signal(signal=SignalName.EARLY_WAKING, confidence=Confidence.MEDIUM,
               severity=Severity.MODERATE, status=SignalStatus.ESTABLISHED,
               change=-53.0,
               baseline=SignalWindow(window_days=10, value=387.0, label="06:27"),
               recent=SignalWindow(window_days=5, value=334.0, label="05:34"),
               supporting_evidence=["4 of 5 recent rises earlier than baseline"],
               limitations=["two recent times parent-reported"])
    r = Signal.model_validate(s.model_dump())
    assert r.signal is SignalName.EARLY_WAKING and r.change == -53.0
    assert r.change_unit == "minutes"


def test_detector_input_defaults():
    inp = DetectorInput(series=FeatureSeries(),
                        baseline=Baseline(status=BaselineStatus.COMPUTED))
    assert inp.events == [] and inp.reported_context == []
