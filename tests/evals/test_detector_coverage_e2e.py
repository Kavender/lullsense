"""End-to-end detector coverage (P0.5.3).

Every advertised detector in the taxonomy gets a positive end-to-end case (raw
SleepLog -> features -> baseline -> run_detectors, asserting the signal fires)
and a negative/control (asserting it stays silent on a stable child). Two
detectors — bedtime_resistance (needs sleep-onset latency) and
possible_context_related_disruption (needs context events) — cannot be expressed
through the CLI's generic-JSON fixtures (start/end/location only), so they are
covered here at the engine-pipeline level, which is where they must be exercised.

Prior window = 14 days, recent = 5 (baseline defaults); nights run one per calendar
day (onset evening d, rise morning d+1), naps attach to the rise day, mirroring
evals/proactive/fixtures/*.json.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.analyze.models import BaselineStatus
from baby_sleep.contract.enums import EventKind, SleepType
from baby_sleep.contract.models import Child, ContextEvent, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.detect import DetectorInput, SignalName, run_detectors

Y, M = 2026, 9
AGE = 12
PRIOR, RECENT = 14, 5
RECENT_START = 15  # onset-days 15..19 are the recent window


def _night(d, *, onset=(19, 30), rise=(6, 0), sol=None, wakings=None, split=None):
    """One night starting evening of day d. `split` = (wake_h, wake_m, resume_h, resume_m)
    to break it into two segments (a mid-night gap) for split_night / night_waking."""
    on = datetime(Y, M, d, *onset)
    ri = datetime(Y, M, d + 1, *rise)
    if split:
        w = datetime(Y, M, d + 1, split[0], split[1])
        r = datetime(Y, M, d + 1, split[2], split[3])
        return [
            SleepSession(start=ApproxTime(value=on), end=ApproxTime(value=w),
                         duration_minutes=int((w - on).total_seconds() // 60),
                         sleep_type=SleepType.NIGHT),
            SleepSession(start=ApproxTime(value=r), end=ApproxTime(value=ri),
                         duration_minutes=int((ri - r).total_seconds() // 60),
                         sleep_type=SleepType.NIGHT),
        ]
    return [SleepSession(start=ApproxTime(value=on), end=ApproxTime(value=ri),
                         duration_minutes=int((ri - on).total_seconds() // 60),
                         sleep_type=SleepType.NIGHT,
                         onset_latency_minutes=sol, night_wakings=wakings)]


def _naps(d, specs):
    """Naps on the rise day (d+1). specs = list of (start_h, start_m, duration_min)."""
    out = []
    for sh, sm, dur in specs:
        st = datetime(Y, M, d + 1, sh, sm)
        out.append(SleepSession(start=ApproxTime(value=st),
                                end=ApproxTime(value=st + timedelta(minutes=dur)),
                                duration_minutes=dur, sleep_type=SleepType.NAP))
    return out


def _fire(sessions, *, events=None, reported=None, age=AGE):
    series = build_feature_series(SleepLog(sessions=sessions))
    baseline = build_baseline(series, Child(age_months=age))
    signals = run_detectors(DetectorInput(series=series, baseline=baseline,
                                          events=events or [], reported_context=reported or []))
    return baseline, {s.signal for s in signals}


def _is_recent(d):
    return d >= RECENT_START


# ---- builders: 14 stable prior days, then a mutated recent window ----

def _stable_nights():
    out = []
    for d in range(1, 20):
        out += _night(d)
    return out


def _with_naps(two_naps_recent=True, naps_prior=((9, 0, 60), (13, 0, 60))):
    out = []
    for d in range(1, 20):
        out += _night(d)
        out += _naps(d, list(naps_prior))
    return out


# =========================== POSITIVE CASES ===========================

def test_early_waking_fires():
    sess = []
    for d in range(1, 20):
        sess += _night(d, rise=(5, 0)) if _is_recent(d) else _night(d, rise=(6, 0))
    _, sig = _fire(sess)
    assert SignalName.EARLY_WAKING in sig
    assert SignalName.SPLIT_NIGHT not in sig  # neighboring pattern stays silent


def test_night_waking_fires():
    # baseline ~1 waking/night, recent ~3 — small gaps so longest stays < split floor
    sess = []
    for d in range(1, 20):
        sess += _night(d, wakings=3 if _is_recent(d) else 1)
    _, sig = _fire(sess)
    assert SignalName.NIGHT_WAKING in sig
    assert SignalName.SPLIT_NIGHT not in sig


def test_short_nap_fires():
    sess = []
    for d in range(1, 20):
        sess += _night(d)
        sess += _naps(d, [(9, 0, 20), (13, 0, 20)] if _is_recent(d) else [(9, 0, 60), (13, 0, 60)])
    _, sig = _fire(sess)
    assert SignalName.SHORT_NAP in sig


def test_total_sleep_drop_fires():
    # recent bedtime 90 min later, rise unchanged -> ~90 min less night sleep
    sess = []
    for d in range(1, 20):
        sess += _night(d, onset=(21, 0)) if _is_recent(d) else _night(d, onset=(19, 30))
    _, sig = _fire(sess)
    assert SignalName.TOTAL_SLEEP_DROP in sig
    assert SignalName.EARLY_WAKING not in sig  # rise unchanged


def test_bedtime_resistance_fires():
    # sleep-onset latency 10 -> 35 min (pipeline-only: SOL not expressible via CLI JSON)
    sess = []
    for d in range(1, 20):
        sess += _night(d, sol=35 if _is_recent(d) else 10)
    _, sig = _fire(sess)
    assert SignalName.BEDTIME_RESISTANCE in sig


def test_split_night_fires():
    # prior nights have a brief settle-back gap (~15 min) so the baseline exists;
    # recent nights develop a long mid-night awake stretch (~90 min).
    sess = []
    for d in range(1, 20):
        sess += _night(d, split=(1, 0, 2, 30)) if _is_recent(d) else _night(d, split=(2, 0, 2, 15))
    _, sig = _fire(sess)
    assert SignalName.SPLIT_NIGHT in sig


def test_high_variability_fires():
    # stable prior bedtime; recent bedtime scattered around the same mean (rise fixed)
    scatter = {15: (18, 15), 16: (20, 45), 17: (18, 30), 18: (20, 30), 19: (19, 30)}
    sess = []
    for d in range(1, 20):
        sess += _night(d, onset=scatter[d]) if _is_recent(d) else _night(d)
    _, sig = _fire(sess)
    assert SignalName.HIGH_VARIABILITY in sig


def test_schedule_drift_fires():
    # whole schedule drifts progressively later across the recent window (duration constant)
    onset = {15: (19, 30), 16: (19, 50), 17: (20, 10), 18: (20, 30), 19: (20, 50)}
    rise = {15: (6, 0), 16: (6, 20), 17: (6, 40), 18: (7, 0), 19: (7, 20)}
    sess = []
    for d in range(1, 20):
        sess += _night(d, onset=onset[d], rise=rise[d]) if _is_recent(d) else _night(d)
    _, sig = _fire(sess)
    assert SignalName.SCHEDULE_DRIFT in sig


def test_nap_transition_fires():
    # 2 naps -> 1 nap, but total daytime sleep held constant (avoid short_nap)
    sess = []
    for d in range(1, 20):
        sess += _night(d)
        sess += _naps(d, [(12, 0, 120)] if _is_recent(d) else [(9, 0, 60), (13, 0, 60)])
    _, sig = _fire(sess)
    assert SignalName.NAP_TRANSITION in sig
    assert SignalName.SHORT_NAP not in sig  # total daytime unchanged


def test_context_disruption_fires():
    # a real deviation (early waking) + a reported context overlapping the recent window
    sess = []
    for d in range(1, 20):
        sess += _night(d, rise=(5, 0)) if _is_recent(d) else _night(d, rise=(6, 0))
    ev = ContextEvent(kind=EventKind.MEDICATION,
                      at=ApproxTime(value=datetime(Y, M, 17, 15, 0)), label="teething gel")
    _, sig = _fire(sess, events=[ev], reported=["teething"])
    assert SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION in sig


# =========================== NEGATIVE / CONTROL CASES ===========================

def test_stable_child_fires_nothing():
    baseline, sig = _fire(_with_naps())
    assert baseline.status is BaselineStatus.COMPUTED
    assert sig == set(), f"stable child should surface no signals, got {sig}"


def test_insufficient_data_yields_no_signals():
    sess = []
    for d in range(1, 5):  # only 4 nights
        sess += _night(d)
    baseline, sig = _fire(sess)
    assert baseline.status is BaselineStatus.INSUFFICIENT_DATA
    assert sig == set()


def test_below_supported_age_yields_no_signals():
    baseline, sig = _fire(_stable_nights(), age=3)
    assert baseline.status is BaselineStatus.BELOW_SUPPORTED_RANGE
    assert sig == set()


def test_context_silent_without_a_coincident_signal():
    # stable child + a reported context must NOT invent a disruption (needs a real signal too)
    ev = ContextEvent(kind=EventKind.MEDICATION,
                      at=ApproxTime(value=datetime(Y, M, 17, 15, 0)), label="teething gel")
    _, sig = _fire(_stable_nights(), events=[ev], reported=["teething"])
    assert SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION not in sig


ALL_DETECTORS = {s for s in SignalName}


def test_every_advertised_detector_has_a_positive_case():
    """Guard: the positive tests above must name every detector in the taxonomy."""
    import pathlib
    src = pathlib.Path(__file__).read_text()
    covered = {name for name in SignalName if f"SignalName.{name.name} in sig" in src}
    missing = ALL_DETECTORS - covered
    assert not missing, f"detectors with no positive E2E case: {sorted(s.value for s in missing)}"
