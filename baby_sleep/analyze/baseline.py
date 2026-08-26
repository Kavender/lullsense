"""Robust personal baseline over per-day features. Pure, recomputed on demand (D21).
Thresholds here are product heuristics, not medical standards."""
from __future__ import annotations

from baby_sleep.analyze.models import (
    Baseline,
    BaselineStatus,
    Confidence,
    FeatureBaseline,
    FeatureSeries,
)
from baby_sleep.analyze.robust import mad, median
from baby_sleep.contract.models import Child

SUPPORTED_MIN_MONTHS = 4
MIN_BASELINE_DAYS = 5


def _minutes_of_day(dt) -> float:
    return dt.hour * 60 + dt.minute


# feature name -> callable extracting a per-day scalar (minutes/counts), or None if absent
_EXTRACTORS = {
    "rise_time_min": lambda f: _minutes_of_day(f.rise_time) if f.rise_time else None,
    "sleep_onset_min": lambda f: _minutes_of_day(f.sleep_onset_time) if f.sleep_onset_time else None,
    "night_sleep_duration_min": lambda f: f.night_sleep_duration_min,
    "total_24h_sleep_min": lambda f: f.total_24h_sleep_min,
    "total_daytime_sleep_min": lambda f: f.total_daytime_sleep_min,
    "nap_count": lambda f: float(f.nap_count),
    "night_waking_count": lambda f: f.night_waking_count,
    "sleep_onset_latency_min": lambda f: f.sleep_onset_latency_min,
}
BASELINE_FEATURES = list(_EXTRACTORS)


def _series_values(days, extractor) -> list[float]:
    return [float(v) for v in (extractor(f) for f in days) if v is not None]


def _feature_confidence(n: int, window: int, b_med: float, b_mad: float) -> Confidence:
    """Heuristic ordinal confidence. High only with near-full, tight, consistent data."""
    coverage = n / window if window else 0.0
    rel_disp = (b_mad / abs(b_med)) if b_med else 1.0
    if coverage >= 0.8 and rel_disp <= 0.10:
        return Confidence.HIGH
    if coverage >= 0.5 and rel_disp <= 0.25:
        return Confidence.MEDIUM
    return Confidence.LOW


def build_baseline(
    series: FeatureSeries,
    child: Child,
    prior_window_days: int = 14,
    recent_window_days: int = 5,
    stated: dict[str, float] | None = None,
) -> Baseline:
    age = child.corrected_age_months()
    if age is None:
        return Baseline(
            status=BaselineStatus.AGE_UNKNOWN,
            reason="Corrected age must be established before baseline analysis (D20).",
        )
    if age < SUPPORTED_MIN_MONTHS:
        return Baseline(
            status=BaselineStatus.BELOW_SUPPORTED_RANGE,
            corrected_age_months=age,
            reason=(
                f"Corrected age ~{age}mo is below the {SUPPORTED_MIN_MONTHS}-month "
                "behavioral-support floor; newborn sleep is not yet developmentally "
                "stable, so no personal baseline is computed (safe-sleep guardrail only)."
            ),
        )

    days = series.days
    if len([f for f in days if f.night_sleep_duration_min is not None]) < MIN_BASELINE_DAYS:
        if stated:
            return _stated_baseline(stated, age)
        return Baseline(
            status=BaselineStatus.INSUFFICIENT_DATA,
            corrected_age_months=age,
            reason=(
                f"Fewer than {MIN_BASELINE_DAYS} usable days of history; cannot form a "
                "stable personal baseline."
            ),
        )

    prior = days[:prior_window_days]
    recent = days[-recent_window_days:]
    features: dict[str, FeatureBaseline] = {}
    for name, extractor in _EXTRACTORS.items():
        base_vals = _series_values(prior, extractor)
        if len(base_vals) < 2:
            continue
        b_med, b_mad = median(base_vals), mad(base_vals)
        recent_vals = _series_values(recent, extractor)
        r_med = median(recent_vals) if recent_vals else None
        dev = (r_med - b_med) if r_med is not None else None
        dev_mads = (dev / b_mad) if (dev is not None and b_mad) else None
        features[name] = FeatureBaseline(
            feature=name,
            baseline_median=b_med,
            mad=b_mad,
            n=len(base_vals),
            recent_median=r_med,
            deviation=dev,
            deviation_mads=dev_mads,
            confidence=_feature_confidence(len(base_vals), prior_window_days, b_med, b_mad),
        )
    return Baseline(
        status=BaselineStatus.COMPUTED,
        features=features,
        prior_window_days=prior_window_days,
        recent_window_days=recent_window_days,
        corrected_age_months=age,
    )


def _stated_baseline(stated: dict[str, float], age: int) -> Baseline:
    features = {
        name: FeatureBaseline(
            feature=name,
            baseline_median=float(val),
            mad=0.0,
            n=0,
            source="self_reported",
            confidence=Confidence.LOW,
        )
        for name, val in stated.items()
    }
    return Baseline(status=BaselineStatus.COMPUTED, features=features, corrected_age_months=age)
