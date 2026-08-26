"""Context-overlap detector. Correlational ONLY — never diagnoses causality (spec §9)."""
from __future__ import annotations

from baby_sleep.analyze.models import Confidence
from baby_sleep.detect.models import (
    DetectorInput,
    Severity,
    Signal,
    SignalName,
    SignalStatus,
    SignalWindow,
)

_SEV_ORDER = {Severity.MILD: 0, Severity.MODERATE: 1, Severity.SIGNIFICANT: 2}
_NON_DIAGNOSIS = ("temporal overlap only; causality is not established and this is not a "
                  "medical diagnosis")


def run_context_detector(inp: DetectorInput, other_signals: list[Signal]) -> Signal | None:
    disruptions = [s for s in other_signals
                   if s.signal is not SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION]
    if not disruptions:
        return None

    days = inp.series.days[-inp.baseline.recent_window_days:]
    if not days:
        return None
    lo, hi = days[0].day, days[-1].day

    reasons: list[str] = []
    for label in inp.reported_context:
        reasons.append(f"reported context '{label}' during the recent window")
    for ev in inp.events:
        if lo <= ev.at.value.date() <= hi:
            what = ev.label or ev.kind.value
            reasons.append(f"logged {ev.kind.value} '{what}' on {ev.at.value.date().isoformat()} "
                           "overlaps the recent window")
    if not reasons:
        return None

    worst = max(disruptions, key=lambda s: _SEV_ORDER[s.severity])
    co = ", ".join(sorted({s.signal.value for s in disruptions}))
    return Signal(
        signal=SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION,
        confidence=Confidence.MEDIUM,          # correlational: capped here, never HIGH
        severity=worst.severity,
        status=SignalStatus.ESTABLISHED,
        recent=SignalWindow(window_days=inp.baseline.recent_window_days),
        supporting_evidence=reasons + [f"overlaps sleep changes: {co}"],
        limitations=[_NON_DIAGNOSIS])
