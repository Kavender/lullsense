"""Recent-window medians shared by the CLI (`scripts/analyze_sleep.py`) and the service."""
from __future__ import annotations

from .models import Baseline, FeatureSeries


def _hhmm(minutes):
    if minutes is None:
        return None
    m = round(minutes)
    return f"{m // 60:02d}:{m % 60:02d}"


def summarize(series: FeatureSeries, baseline: Baseline) -> dict:
    """Medians over the baseline's recent window (all days when it has none)."""
    recent = (
        series.days[-baseline.recent_window_days :]
        if baseline.recent_window_days
        else series.days
    )

    def _med(getter):
        vals = sorted(v for v in (getter(d) for d in recent) if v is not None)
        return vals[len(vals) // 2] if vals else None

    def _clock(attr):
        return _hhmm(_med(lambda d: t.hour * 60 + t.minute if (t := getattr(d, attr)) else None))

    return {
        "rise_time": _clock("rise_time"),
        "sleep_onset_time": _clock("sleep_onset_time"),
        "night_sleep_duration_min": _med(lambda d: d.night_sleep_duration_min),
        "total_24h_sleep_min": _med(lambda d: d.total_24h_sleep_min),
        "nap_count": _med(lambda d: float(d.nap_count)),
    }
