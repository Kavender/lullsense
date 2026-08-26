from datetime import datetime

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


from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.contract.enums import SleepType
from baby_sleep.contract.models import Child, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.detect.runner import run_detectors


def _n(d, rh, rm, dur):
    return SleepSession(start=ApproxTime(value=datetime(2026, 9, d, 19, 30)),
                        end=ApproxTime(value=datetime(2026, 9, d + 1, rh, rm)),
                        duration_minutes=dur, sleep_type=SleepType.NIGHT)


def test_runner_age_gate_returns_empty_for_newborn():
    sess = [_n(1 + i, 6, 0, 630) for i in range(19)]
    series = build_feature_series(SleepLog(sessions=sess))
    inp = DetectorInput(series=series, baseline=build_baseline(series, Child(age_months=3)))
    assert run_detectors(inp) == []            # below supported range -> no detectors


def test_runner_returns_signals_when_computed():
    sess = [_n(1 + i, 6, 0, 630) for i in range(14)] + [_n(15 + i, 5, 0, 570) for i in range(5)]
    series = build_feature_series(SleepLog(sessions=sess))
    inp = DetectorInput(series=series, baseline=build_baseline(series, Child(age_months=12)))
    names = {s.signal for s in run_detectors(inp)}
    assert SignalName.EARLY_WAKING in names
