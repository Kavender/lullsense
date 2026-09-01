"""Detector runner. Age-gated per C5: no output unless the baseline was computed."""
from __future__ import annotations

from baby_sleep.analyze.models import BaselineStatus, Confidence
from baby_sleep.detect.context import run_context_detector
from baby_sleep.detect.deviation import run_deviation_detectors
from baby_sleep.detect.grading import _CONF_ORDER
from baby_sleep.detect.models import DetectorInput, Signal
from baby_sleep.detect.trend import run_trend_detectors

BASELINE_REPAIRED_CAP_FRACTION = 0.25   # >25% repaired baseline-window sessions => cap at MEDIUM


def _baseline_repaired_share(inp: DetectorInput) -> float:
    """Mean repaired-session share across the baseline (pre-recent) window days (D15)."""
    days = inp.series.days
    recent = inp.baseline.recent_window_days
    baseline_days = days[:-recent] if 0 < recent < len(days) else days
    if not baseline_days:
        return 0.0
    return sum(d.repaired_share for d in baseline_days) / len(baseline_days)


def _cap_for_repaired_baseline(signals: list[Signal], repaired_share: float) -> list[Signal]:
    """A baseline built substantially on repaired data can't support high confidence.
    Cap every signal at MEDIUM and disclose why (honesty over false precision)."""
    if repaired_share <= BASELINE_REPAIRED_CAP_FRACTION:
        return signals
    note = (f"baseline includes repaired sessions ({repaired_share:.0%} of baseline-window "
            "days); confidence capped")
    out: list[Signal] = []
    for s in signals:
        conf = (Confidence.MEDIUM
                if _CONF_ORDER[s.confidence] > _CONF_ORDER[Confidence.MEDIUM] else s.confidence)
        out.append(s.model_copy(update={"confidence": conf, "limitations": [*s.limitations, note]}))
    return out


def run_detectors(inp: DetectorInput) -> list[Signal]:
    if inp.baseline.status is not BaselineStatus.COMPUTED:
        return []
    signals = run_deviation_detectors(inp) + run_trend_detectors(inp)
    context = run_context_detector(inp, signals)
    if context is not None:
        signals.append(context)
    return _cap_for_repaired_baseline(signals, _baseline_repaired_share(inp))
