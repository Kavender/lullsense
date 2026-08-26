from datetime import datetime

from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.contract.enums import SleepType
from baby_sleep.contract.models import Child, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.detect.models import DetectorInput, SignalName
from baby_sleep.detect.trend import run_trend_detectors


def _night(d, on_h, on_m, rise_d, rise_h, rise_m, dur):
    return SleepSession(start=ApproxTime(value=datetime(2026, 9, d, on_h, on_m)),
                        end=ApproxTime(value=datetime(2026, 9, rise_d, rise_h, rise_m)),
                        duration_minutes=dur, sleep_type=SleepType.NIGHT)


def _inp(sessions, age=14):
    series = build_feature_series(SleepLog(sessions=sessions))
    return DetectorInput(series=series, baseline=build_baseline(series, Child(age_months=age)))


def test_schedule_drift_detects_progressive_bedtime_shift():
    # bedtime creeps 15 min later each of the last 5 nights (net +60)
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 30, 660) for i in range(9)]        # stable prior
    drift = [19*60+30 + 15*(i+1) for i in range(5)]                            # 19:45..20:45
    for i, mins in enumerate(drift):
        d = 10 + i
        sess.append(_night(d, mins // 60, mins % 60, d + 1, 6, 30, 660 - 15*(i+1)))
    names = {s.signal for s in run_trend_detectors(_inp(sess))}
    assert SignalName.SCHEDULE_DRIFT in names


def test_high_variability_detects_destabilized_bedtime():
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 30, 660) for i in range(9)]        # rock-steady prior
    # wild recent swings: minutes 1080,1260,1110,1290,1140 -> MAD 60 (>= 40 floor for a stable prior)
    jitter = [18*60, 21*60, 18*60+30, 21*60+30, 19*60]
    for i, mins in enumerate(jitter):
        d = 10 + i
        sess.append(_night(d, mins // 60, mins % 60, d + 1, 6, 30, 660))
    names = {s.signal for s in run_trend_detectors(_inp(sess))}
    assert SignalName.HIGH_VARIABILITY in names


def test_nap_transition_detects_nap_count_drop():
    # prior days: 2 naps; recent days: 1 nap
    def day(d, naps):
        s = [_night(d, 19, 30, d + 1, 6, 30, 660)]
        for k in range(naps):
            s.append(SleepSession(start=ApproxTime(value=datetime(2026, 9, d + 1, 9 + 4 * k, 0)),
                                  end=ApproxTime(value=datetime(2026, 9, d + 1, 10 + 4 * k, 0)),
                                  duration_minutes=60, sleep_type=SleepType.NAP))
        return s
    sess = []
    for d in range(1, 10):
        sess += day(d, 2)
    for d in range(10, 15):
        sess += day(d, 1)
    names = {s.signal for s in run_trend_detectors(_inp(sess, age=15))}
    assert SignalName.NAP_TRANSITION in names


def test_trend_quiet_when_stable():
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 30, 660) for i in range(19)]
    assert run_trend_detectors(_inp(sess)) == []


def test_schedule_drift_reports_net_shift_value():
    # regression (review nit 5): assert a concrete computed value, not just presence
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 30, 660) for i in range(9)]
    drift = [19*60+30 + 15*(i+1) for i in range(5)]                            # 19:45..20:45, net +60
    for i, mins in enumerate(drift):
        d = 10 + i
        sess.append(_night(d, mins // 60, mins % 60, d + 1, 6, 30, 660 - 15*(i+1)))
    sig = next(s for s in run_trend_detectors(_inp(sess))
               if s.signal is SignalName.SCHEDULE_DRIFT)
    assert sig.change == 60.0                       # net first->last bedtime shift
    assert sig.severity.value == "mild"             # 60 < schedule_drift moderate_hi (75)


def test_trend_detectors_age_gated():
    # regression (review important 1): the exported sub-runner must itself honor the
    # age gate (C5), not rely on the top-level runner. The same drifting series that
    # fires schedule_drift at a supported age must produce NO signals at age 3
    # (below_supported_range).
    sess = [_night(1 + i, 19, 30, 2 + i, 6, 30, 660) for i in range(9)]
    drift = [19*60+30 + 15*(i+1) for i in range(5)]
    for i, mins in enumerate(drift):
        d = 10 + i
        sess.append(_night(d, mins // 60, mins % 60, d + 1, 6, 30, 660 - 15*(i+1)))
    assert run_trend_detectors(_inp(sess, age=14)) != []       # fires at supported age
    assert run_trend_detectors(_inp(sess, age=3)) == []        # gated below supported range
