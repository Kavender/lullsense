"""Compute per-day and rolling sleep features from wake-day-segmented data."""
from __future__ import annotations

import itertools
from datetime import datetime

from baby_sleep.analyze.daymap import segment_days
from baby_sleep.analyze.models import Confidence, DailyFeatures, FeatureSeries, NapFeature, SleepDay
from baby_sleep.analyze.robust import mad, median
from baby_sleep.contract.enums import DataQuality, Location
from baby_sleep.contract.models import SleepLog
from baby_sleep.contract.time_types import TimePrecision


def _minutes(a, b) -> int:
    return int((b - a).total_seconds() // 60)


def _night_features(day: SleepDay) -> dict:
    segs = day.night_segments
    if not segs:
        return {}
    onset = segs[0].start.value
    rise = segs[-1].end.value if segs[-1].end is not None else None
    asleep = sum(s.duration_minutes for s in segs if s.duration_minutes is not None)
    in_bed = segs[0].put_down_at.value if segs[0].put_down_at is not None else onset
    out = {
        "sleep_onset_time": onset,
        "rise_time": rise,
        "in_bed_time": in_bed,
        "sleep_onset_latency_min": segs[0].onset_latency_minutes,
        "night_sleep_duration_min": asleep or None,
    }
    if len(segs) > 1:
        gaps = []
        for a, b in itertools.pairwise(segs):
            if a.end is not None and b.start is not None:
                gaps.append(_minutes(a.end.value, b.start.value))
        out["night_waking_count"] = len(gaps)
        out["total_awake_overnight_min"] = sum(gaps) if gaps else None
        out["longest_night_waking_min"] = max(gaps) if gaps else None
    else:
        out["night_waking_count"] = segs[0].night_wakings
    return out


def _nap_features(day: SleepDay) -> dict:
    naps = [NapFeature(start=n.start.value,
                       end=n.end.value if n.end is not None else None,
                       duration_minutes=n.duration_minutes) for n in day.naps]
    daytime = [n.duration_minutes for n in naps if n.duration_minutes is not None]
    return {
        "nap_count": len(naps),
        "naps": naps,
        "total_daytime_sleep_min": sum(daytime) if daytime else None,
    }


def _wake_windows(day: SleepDay) -> tuple[list[int], list[int]]:
    """Return (pre_nap_awake, intra_day_wake_windows). Terminal window added at series level."""
    rise = day.night_segments[-1].end.value if (
        day.night_segments and day.night_segments[-1].end is not None) else None
    pre_nap, windows = [], []
    prev_end = rise
    for nap in day.naps:
        if prev_end is not None and nap.start.value >= prev_end:
            gap = _minutes(prev_end, nap.start.value)
            pre_nap.append(gap)
            windows.append(gap)
        prev_end = nap.end.value if nap.end is not None else prev_end
    return pre_nap, windows


def _approx_share(day: SleepDay) -> float:
    sessions = list(day.night_segments) + list(day.naps)
    if not sessions:
        return 0.0

    def lower_quality(s) -> bool:
        return (s.start.precision is TimePrecision.APPROXIMATE
                or s.data_quality is not DataQuality.LOGGED)

    return sum(1 for s in sessions if lower_quality(s)) / len(sessions)


def _dominant_location(day: SleepDay) -> Location:
    from collections import Counter
    locs = [s.location for s in list(day.night_segments) + list(day.naps)
            if s.location is not Location.UNKNOWN]
    return Counter(locs).most_common(1)[0][0] if locs else Location.UNKNOWN


def compute_daily_features(day: SleepDay) -> DailyFeatures:
    f = DailyFeatures(day=day.day)
    night = _night_features(day)
    nap = _nap_features(day)
    for k, v in {**night, **nap}.items():
        setattr(f, k, v)
    n_min = f.night_sleep_duration_min or 0
    d_min = f.total_daytime_sleep_min or 0
    if night or nap.get("total_daytime_sleep_min") is not None:
        f.total_24h_sleep_min = n_min + d_min if (n_min or d_min) else None
    pre_nap, windows = _wake_windows(day)
    f.pre_nap_awake_min = pre_nap
    f.wake_windows_min = list(windows)
    f.is_weekend = day.day.weekday() >= 5
    f.location = _dominant_location(day)
    f.approx_share = _approx_share(day)
    f.day_confidence = (Confidence.HIGH if f.approx_share == 0
                        else Confidence.MEDIUM if f.approx_share <= 0.5
                        else Confidence.LOW)
    return f


def _minutes_of_day(dt: datetime) -> float:
    return dt.hour * 60 + dt.minute


def _has_core_data(f: DailyFeatures) -> bool:
    return f.night_sleep_duration_min is not None or f.total_24h_sleep_min is not None


def build_feature_series(log: SleepLog) -> FeatureSeries:
    days = [compute_daily_features(d) for d in segment_days(log)]
    series = FeatureSeries(days=days)

    # terminal wake window: last nap end (day D) -> next day's night onset (the evening bedtime)
    for i, f in enumerate(days):
        if not f.naps or f.naps[-1].end is None:
            continue
        nxt = days[i + 1] if i + 1 < len(days) else None
        if nxt is not None and nxt.sleep_onset_time is not None:
            gap = _minutes(f.naps[-1].end, nxt.sleep_onset_time)
            if gap > 0:
                f.wake_windows_min.append(gap)

    def var(getter) -> float | None:
        xs = [getter(f) for f in days if getter(f) is not None]
        return mad([float(x) for x in xs]) if len(xs) >= 2 else None

    series.bedtime_variability_min = var(
        lambda f: _minutes_of_day(f.sleep_onset_time) if f.sleep_onset_time else None)
    series.rise_time_variability_min = var(
        lambda f: _minutes_of_day(f.rise_time) if f.rise_time else None)
    series.nap_time_variability_min = var(
        lambda f: _minutes_of_day(f.naps[0].start) if f.naps else None)
    series.total_sleep_variability_min = var(lambda f: f.total_24h_sleep_min)

    # weekday vs weekend deltas (weekend median - weekday median), for a few key features
    def delta(getter) -> float | None:
        wk = [float(getter(f)) for f in days if f.is_weekend is False and getter(f) is not None]
        we = [float(getter(f)) for f in days if f.is_weekend is True and getter(f) is not None]
        if not wk or not we:
            return None
        return median(we) - median(wk)

    for name, getter in {
        "total_24h_sleep_min": lambda f: f.total_24h_sleep_min,
        "rise_time_min": lambda f: _minutes_of_day(f.rise_time) if f.rise_time else None,
    }.items():
        d = delta(getter)
        if d is not None:
            series.weekday_vs_weekend[name] = d

    if days:
        series.missing_data_rate = sum(0 if _has_core_data(f) else 1 for f in days) / len(days)
    return series
