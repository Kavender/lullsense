"""Ordinal grading for detectors (D14). Product heuristics, not clinical probabilities.
Documented in skills/lullsense/references/signal-taxonomy.md."""
from __future__ import annotations

from baby_sleep.analyze.models import Confidence, DailyFeatures
from baby_sleep.detect.models import Severity, SignalStatus

MADS_TRIGGER = 1.5          # deviation of >=1.5 robust SDs is the minimum interesting shift
MADS_STRONG = 3.0           # >=3 robust SDs is a strong shift
STATUS_ESTABLISHED_FRAC = 0.6
_CONF_ORDER = {Confidence.LOW: 0, Confidence.MEDIUM: 1, Confidence.HIGH: 2}


def consistency(values: list[float | None], baseline_median: float, direction: int) -> float:
    """Fraction of present recent-window values that deviate from the baseline median in
    the signal's direction (direction = +1 increase, -1 decrease)."""
    vals = [v for v in values if v is not None]
    if not vals:
        return 0.0
    hits = sum(1 for v in vals if (v - baseline_median) * direction > 0)
    return hits / len(vals)


def recent_approx_share(days: list[DailyFeatures]) -> float:
    if not days:
        return 0.0
    return sum(1 for d in days if d.approx_share > 0) / len(days)


def grade_confidence(deviation_mads: float | None, consistency_frac: float,
                     baseline_conf: Confidence, approx_share: float,
                     cap: Confidence | None = None) -> Confidence:
    strong = deviation_mads is not None and abs(deviation_mads) >= MADS_STRONG
    ok_mag = deviation_mads is None or abs(deviation_mads) >= MADS_TRIGGER
    if (strong or deviation_mads is None) and consistency_frac >= 0.8 \
            and baseline_conf is not Confidence.LOW and approx_share <= 0.34:
        conf = Confidence.HIGH
    elif ok_mag and consistency_frac >= 0.5:
        conf = Confidence.MEDIUM
    else:
        conf = Confidence.LOW
    if cap is not None and _CONF_ORDER[conf] > _CONF_ORDER[cap]:
        conf = cap
    return conf


def grade_severity(magnitude_abs: float, mild_hi: float, moderate_hi: float) -> Severity:
    if magnitude_abs >= moderate_hi:
        return Severity.SIGNIFICANT
    if magnitude_abs >= mild_hi:
        return Severity.MODERATE
    return Severity.MILD


def grade_status(consistency_frac: float) -> SignalStatus:
    return (SignalStatus.ESTABLISHED if consistency_frac >= STATUS_ESTABLISHED_FRAC
            else SignalStatus.EMERGING)
