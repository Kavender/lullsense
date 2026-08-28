"""Robust, None-safe summary statistics used by the baseline engine."""
from __future__ import annotations

import statistics


def median(xs: list[float]) -> float | None:
    return statistics.median(xs) if xs else None


def mad(xs: list[float]) -> float | None:
    """Median absolute deviation about the median."""
    if not xs:
        return None
    m = statistics.median(xs)
    return statistics.median([abs(x - m) for x in xs])


def iqr(xs: list[float]) -> float | None:
    """Interquartile range (Q3 - Q1) using inclusive quartiles."""
    if len(xs) < 2:
        return None
    q = statistics.quantiles(xs, n=4, method="inclusive")
    return q[2] - q[0]
