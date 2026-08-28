"""Detector runner. Age-gated per C5: no output unless the baseline was computed."""
from __future__ import annotations

from baby_sleep.analyze.models import BaselineStatus
from baby_sleep.detect.context import run_context_detector
from baby_sleep.detect.deviation import run_deviation_detectors
from baby_sleep.detect.models import DetectorInput, Signal
from baby_sleep.detect.trend import run_trend_detectors


def run_detectors(inp: DetectorInput) -> list[Signal]:
    if inp.baseline.status is not BaselineStatus.COMPUTED:
        return []
    signals = run_deviation_detectors(inp) + run_trend_detectors(inp)
    context = run_context_detector(inp, signals)
    if context is not None:
        signals.append(context)
    return signals
