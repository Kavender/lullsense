"""Trend/structural detectors over the day series. Product heuristics throughout."""
from __future__ import annotations

import itertools

from baby_sleep.analyze.models import BaselineStatus
from baby_sleep.analyze.robust import mad, median
from baby_sleep.detect.grading import grade_severity, grade_status
from baby_sleep.detect.models import (
    Confidence,
    DetectorInput,
    Severity,
    Signal,
    SignalName,
    SignalStatus,
    SignalWindow,
)

# --- product-heuristic thresholds (skills/lullsense/references/signal-taxonomy.md) ---
VAR_RATIO_TRIGGER = 1.75        # recent MAD >= 1.75x prior MAD ...
VAR_ABS_FLOOR_MIN = 25          # ... and recent MAD >= 25 min (avoid flagging tiny jitter)
VAR_STABLE_PRIOR_FLOOR = 40     # if prior perfectly stable (MAD 0), require recent MAD >= 40
DRIFT_NET_MIN = 45              # net first->last shift across the recent window
DRIFT_MONOTONIC_FRAC = 0.7      # >= 70% of day-to-day steps in the same direction
NAP_COUNT_DELTA = 1             # baseline vs recent median nap_count differs by >= 1
NAP_CONSISTENT_FRAC = 0.6       # on >= 60% of recent days


def _clock(days, getter):
    return [getter(f) for f in days if getter(f) is not None]


def _high_variability(inp: DetectorInput) -> Signal | None:
    b = inp.baseline
    days = inp.series.days
    prior = days[:-b.recent_window_days][-b.prior_window_days:] if len(days) > b.recent_window_days else []
    recent = days[-b.recent_window_days:]
    for name, getter in (("bedtime", lambda f: f.sleep_onset_time),
                         ("rise", lambda f: f.rise_time)):
        pv = [(dt.hour * 60 + dt.minute) for dt in _clock(prior, getter)]
        rv = [(dt.hour * 60 + dt.minute) for dt in _clock(recent, getter)]
        if len(pv) < 2 or len(rv) < 2:
            continue
        pm, rm = mad([float(x) for x in pv]) or 0.0, mad([float(x) for x in rv]) or 0.0
        fired = ((pm > 1 and rm >= VAR_RATIO_TRIGGER * pm and rm >= VAR_ABS_FLOOR_MIN)
                 or (pm <= 1 and rm >= VAR_STABLE_PRIOR_FLOOR))
        if fired:
            ratio = (rm / pm) if pm > 1 else float("inf")
            sev = (Severity.SIGNIFICANT if ratio > 4 or rm >= 90
                   else Severity.MODERATE if ratio > 2.5 or rm >= 50 else Severity.MILD)
            return Signal(
                signal=SignalName.HIGH_VARIABILITY, confidence=Confidence.MEDIUM,
                severity=sev, status=SignalStatus.ESTABLISHED,
                baseline=SignalWindow(window_days=b.prior_window_days, value=round(pm, 1)),
                recent=SignalWindow(window_days=b.recent_window_days, value=round(rm, 1)),
                change=round(rm - pm, 1),
                supporting_evidence=[
                    (
                        f"{name} timing spread widened from ~{pm:.0f} to ~{rm:.0f} "
                        "min (MAD) vs the prior window"
                    )
                ],
                limitations=["variability is a pattern signal, not a problem by itself"])
    return None


def _schedule_drift(inp: DetectorInput) -> Signal | None:
    b = inp.baseline
    recent = inp.series.days[-b.recent_window_days:]
    for name, getter in (("bedtime", lambda f: f.sleep_onset_time),
                         ("rise", lambda f: f.rise_time)):
        pts = [(dt.hour * 60 + dt.minute) for dt in _clock(recent, getter)]
        if len(pts) < 3:
            continue
        net = pts[-1] - pts[0]
        steps = [b_ - a_ for a_, b_ in itertools.pairwise(pts)]
        same = sum(1 for s in steps if (s > 0) == (net > 0) and s != 0)
        if abs(net) >= DRIFT_NET_MIN and steps and same / len(steps) >= DRIFT_MONOTONIC_FRAC:
            sev = grade_severity(abs(net), 75, 120)
            return Signal(
                signal=SignalName.SCHEDULE_DRIFT, confidence=Confidence.MEDIUM,
                severity=sev, status=SignalStatus.ESTABLISHED,
                recent=SignalWindow(window_days=b.recent_window_days, value=float(net)),
                change=float(net), change_unit="minutes",
                supporting_evidence=[
                    (
                        f"{name} shifted progressively by {net:+d} min across the "
                        f"last {len(pts)} days ({same}/{len(steps)} steps same direction)"
                    )
                ],
                limitations=[
                    (
                        "progressive drift can reflect developmental change or daylight; "
                        "not a problem by itself"
                    )
                ])
    return None


def _nap_transition(inp: DetectorInput) -> Signal | None:
    b = inp.baseline
    days = inp.series.days
    prior = days[:-b.recent_window_days][-b.prior_window_days:] if len(days) > b.recent_window_days else []
    recent = days[-b.recent_window_days:]
    if len(prior) < 2 or len(recent) < 2:
        return None
    base_ct = median([float(f.nap_count) for f in prior])
    recent_cts = [f.nap_count for f in recent]
    rec_ct = median([float(c) for c in recent_cts])
    if base_ct is None or rec_ct is None or abs(rec_ct - base_ct) < NAP_COUNT_DELTA:
        return None
    target = round(rec_ct)
    frac = sum(1 for c in recent_cts if c == target) / len(recent_cts)
    if frac < NAP_CONSISTENT_FRAC:
        return None
    direction_down = rec_ct < base_ct
    sev = Severity.MODERATE if direction_down else Severity.MILD
    return Signal(
        signal=SignalName.NAP_TRANSITION, confidence=Confidence.MEDIUM,
        severity=sev, status=grade_status(frac),
        baseline=SignalWindow(window_days=b.prior_window_days, value=base_ct),
        recent=SignalWindow(window_days=b.recent_window_days, value=rec_ct),
        change=rec_ct - base_ct, change_unit="naps",
        supporting_evidence=[
            (
                f"nap count moved from ~{base_ct:.0f} to ~{rec_ct:.0f} on "
                f"{frac*100:.0f}% of recent days"
            )
        ],
        limitations=[
            (
                "nap transitions unfold over months and are not age-fixed "
                "(Spencer 2022); treat as a hypothesis, not a completed transition"
            )
        ])


def run_trend_detectors(inp: DetectorInput) -> list[Signal]:
    if inp.baseline.status is not BaselineStatus.COMPUTED:      # age gate (C5), defense in depth
        return []
    return [s for s in (_high_variability(inp), _schedule_drift(inp), _nap_transition(inp))
            if s is not None]
