from datetime import date, datetime

from baby_sleep.analyze.models import (
    Baseline,
    BaselineStatus,
    Confidence,
    DailyFeatures,
    FeatureSeries,
)
from baby_sleep.contract.enums import EventKind
from baby_sleep.contract.models import ContextEvent
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.detect.context import run_context_detector
from baby_sleep.detect.models import DetectorInput, Severity, Signal, SignalName, SignalStatus


def _series_recent_dates():
    days = [DailyFeatures(day=date(2026, 9, 10 + i)) for i in range(5)]
    return FeatureSeries(days=days)


def _other_signal():
    return Signal(signal=SignalName.NIGHT_WAKING, confidence=Confidence.MEDIUM,
                  severity=Severity.MODERATE, status=SignalStatus.ESTABLISHED)


def _base():
    return Baseline(status=BaselineStatus.COMPUTED, prior_window_days=14, recent_window_days=5)


def test_context_fires_on_reported_label_with_cooccurring_signal():
    inp = DetectorInput(series=_series_recent_dates(), baseline=_base(),
                        reported_context=["teething"])
    sig = run_context_detector(inp, [_other_signal()])
    assert sig is not None
    assert sig.signal is SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION
    assert sig.confidence in (Confidence.LOW, Confidence.MEDIUM)   # capped
    assert any("teething" in e.lower() for e in sig.supporting_evidence)
    assert any("not" in lim.lower() and "diagnos" in lim.lower() for lim in sig.limitations)


def test_context_fires_on_event_in_recent_window():
    ev = ContextEvent(kind=EventKind.MEDICATION,
                      at=ApproxTime(value=datetime(2026, 9, 12, 15, 0)), label="acetaminophen")
    inp = DetectorInput(series=_series_recent_dates(), baseline=_base(), events=[ev])
    sig = run_context_detector(inp, [_other_signal()])
    assert sig is not None


def test_context_silent_without_cooccurring_signal():
    inp = DetectorInput(series=_series_recent_dates(), baseline=_base(),
                        reported_context=["travel"])
    assert run_context_detector(inp, []) is None


def test_context_silent_without_context():
    inp = DetectorInput(series=_series_recent_dates(), baseline=_base())
    assert run_context_detector(inp, [_other_signal()]) is None
