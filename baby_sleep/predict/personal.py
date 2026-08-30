"""Derive PersonalStats from an analyze FeatureSeries (recent-days window only)."""
from __future__ import annotations

from baby_sleep.analyze.models import FeatureSeries
from baby_sleep.analyze.robust import mad, median
from baby_sleep.predict.models import PersonalStats

STABLE_MIN_DAYS = 5


def personal_stats_from_series(series: FeatureSeries,
                               min_days: int = STABLE_MIN_DAYS,
                               recent_days: int = 14) -> PersonalStats:
    recent = series.days[-recent_days:] if recent_days else series.days
    windows: list[float] = []
    naps: list[float] = []
    days_with_ww = 0
    for d in recent:
        if d.wake_windows_min:
            windows.extend(float(w) for w in d.wake_windows_min)
            days_with_ww += 1
        naps.extend(float(n.duration_minutes) for n in d.naps
                    if n.duration_minutes is not None)
    return PersonalStats(
        wake_window_median_min=median(windows) if windows else None,
        wake_window_mad_min=mad(windows) if len(windows) >= 2 else None,
        typical_nap_minutes=median(naps) if naps else None,
        days_of_data=days_with_ww,
        stable=days_with_ww >= min_days,
    )
