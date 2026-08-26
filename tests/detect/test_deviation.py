from datetime import datetime

from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.contract.enums import SleepType
from baby_sleep.contract.models import Child, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.detect.deviation import run_deviation_detectors
from baby_sleep.detect.models import DetectorInput, SignalName


def _night(d, on_h, on_m, rise_d, rise_h, rise_m, dur):
    return SleepSession(start=ApproxTime(value=datetime(2026, 9, d, on_h, on_m)),
                        end=ApproxTime(value=datetime(2026, 9, rise_d, rise_h, rise_m)),
                        duration_minutes=dur, sleep_type=SleepType.NIGHT)


def _early_waking_input():
    # 14 stable nights rising 06:00, then 5 rising 05:00 (60 min earlier)
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 0, 630) for i in range(14)]
    sess += [_night(15 + i, 19, 30, 16 + i, 5, 0, 570) for i in range(5)]
    series = build_feature_series(SleepLog(sessions=sess))
    baseline = build_baseline(series, Child(age_months=12))
    return DetectorInput(series=series, baseline=baseline)


def test_early_waking_fires_with_direction_and_change():
    signals = run_deviation_detectors(_early_waking_input())
    ew = next(s for s in signals if s.signal is SignalName.EARLY_WAKING)
    assert ew.change == -60.0
    assert ew.recent.value == 300.0 and ew.baseline.value == 360.0
    assert ew.severity.value == "significant"        # 60 >= moderate_hi
    assert ew.supporting_evidence


def test_no_signal_when_stable():
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 0, 630) for i in range(19)]
    series = build_feature_series(SleepLog(sessions=sess))
    inp = DetectorInput(series=series, baseline=build_baseline(series, Child(age_months=12)))
    assert run_deviation_detectors(inp) == []


def test_wrong_direction_does_not_fire():
    # rising LATER should not trigger early_waking
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 0, 630) for i in range(14)]
    sess += [_night(15 + i, 19, 30, 16 + i, 7, 0, 690) for i in range(5)]   # 07:00, later
    series = build_feature_series(SleepLog(sessions=sess))
    inp = DetectorInput(series=series, baseline=build_baseline(series, Child(age_months=12)))
    names = {s.signal for s in run_deviation_detectors(inp)}
    assert SignalName.EARLY_WAKING not in names
