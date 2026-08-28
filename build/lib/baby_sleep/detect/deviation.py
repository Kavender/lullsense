"""The six baseline-relative deviation detectors. Trigger magnitudes are product
heuristics (references/signal-taxonomy.md); the literature sets no pediatric absolute
thresholds for SOL or night-waking counts, so these are child-relative by design."""
from __future__ import annotations

from dataclasses import dataclass

from baby_sleep.analyze.baseline import feature_scalar
from baby_sleep.analyze.models import BaselineStatus
from baby_sleep.detect.grading import (
    MADS_TRIGGER,
    consistency,
    grade_confidence,
    grade_severity,
    grade_status,
    recent_approx_share,
)
from baby_sleep.detect.models import DetectorInput, Signal, SignalName, SignalWindow


@dataclass(frozen=True)
class _Cfg:
    signal: SignalName
    feature: str
    direction: int          # +1 increase is the signal, -1 decrease
    abs_floor: float        # minimum absolute change to trigger when mad is ~0
    mild_hi: float
    moderate_hi: float
    unit: str


DEVIATION_DETECTORS = [
    _Cfg(SignalName.EARLY_WAKING, "rise_time_min", -1, 20, 40, 60, "minutes"),
    _Cfg(SignalName.NIGHT_WAKING, "night_waking_count", +1, 1, 1, 2, "wakings"),
    _Cfg(SignalName.SHORT_NAP, "total_daytime_sleep_min", -1, 20, 40, 60, "minutes"),
    _Cfg(SignalName.TOTAL_SLEEP_DROP, "total_24h_sleep_min", -1, 30, 60, 90, "minutes"),
    _Cfg(SignalName.BEDTIME_RESISTANCE, "sleep_onset_latency_min", +1, 10, 20, 35, "minutes"),
    _Cfg(SignalName.SPLIT_NIGHT, "longest_night_waking_min", +1, 30, 60, 90, "minutes"),
]


def _hhmm(minutes: float | None) -> str | None:
    if minutes is None:
        return None
    m = round(minutes)
    return f"{m // 60:02d}:{m % 60:02d}"


def _detect(inp: DetectorInput, cfg: _Cfg) -> Signal | None:
    fb = inp.baseline.features.get(cfg.feature)
    if fb is None or fb.deviation is None:
        return None
    dev = fb.deviation
    if dev * cfg.direction <= 0:                     # not in the signal direction
        return None
    mag = abs(dev)
    mads = abs(fb.deviation_mads) if fb.deviation_mads is not None else None
    if not ((mads is not None and mads >= MADS_TRIGGER) or mag >= cfg.abs_floor):
        return None

    recent = inp.series.days[-inp.baseline.recent_window_days:]
    values = [feature_scalar(cfg.feature, d) for d in recent]
    cons = consistency(values, fb.baseline_median, cfg.direction)
    conf = grade_confidence(fb.deviation_mads, cons, fb.confidence, recent_approx_share(recent))
    sev = grade_severity(mag, cfg.mild_hi, cfg.moderate_hi)
    is_time = cfg.feature in ("rise_time_min", "sleep_onset_min")
    hits = sum(1 for v in values if v is not None and (v - fb.baseline_median) * cfg.direction > 0)
    direction_word = "up" if cfg.direction > 0 else "down"
    evidence = [
        (
            f"{hits} of the last {len(values)} days moved {direction_word} vs baseline "
            f"({cfg.feature}: {mag:.0f} {cfg.unit} change)"
        )
    ]
    limitations = []
    if recent_approx_share(recent) > 0:
        limitations.append("some recent values are approximate or parent-reported")
    if fb.confidence.value == "low":
        limitations.append("baseline is thin or highly variable")
    if cfg.signal is SignalName.NIGHT_WAKING:
        limitations.append("night waking is common and highly variable among healthy "
                           "infants (Tham 2017); this is a change vs this child's own norm")
    return Signal(
        signal=cfg.signal, confidence=conf, severity=sev, status=grade_status(cons),
        baseline=SignalWindow(window_days=inp.baseline.prior_window_days,
                              value=fb.baseline_median,
                              label=_hhmm(fb.baseline_median) if is_time else None),
        recent=SignalWindow(window_days=inp.baseline.recent_window_days,
                            value=fb.recent_median,
                            label=_hhmm(fb.recent_median) if is_time else None),
        change=dev, change_unit=cfg.unit,
        supporting_evidence=evidence, limitations=limitations)


def run_deviation_detectors(inp: DetectorInput) -> list[Signal]:
    if inp.baseline.status is not BaselineStatus.COMPUTED:      # age gate (C5), defense in depth
        return []
    return [s for s in (_detect(inp, cfg) for cfg in DEVIATION_DETECTORS) if s is not None]
