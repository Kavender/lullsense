"""Compute the next-sleep-event window from age (+ optional personal baseline).

Range, never a point. Wake windows are a product heuristic (evidence_level low),
never a clinical cutoff. Confidence is low (age-only) or moderate (personal),
never high. Under 4 months: newborn guardrail — no predicted time.
"""
from __future__ import annotations

from baby_sleep.predict.heuristics import AgeBand, lookup
from baby_sleep.predict.models import Basis, NextEvent, PredictInput, Prediction

NEWBORN_MAX_MONTHS = 4
PERSONAL_HALF_WIDTH_FLOOR_MIN = 20.0
YOUNG_AGE_WIDEN_UNDER_MONTHS = 12
YOUNG_AGE_WIDEN_FACTOR = 1.5

_CUES_CAVEAT = (
    "A guide from the child's rhythm, not a fixed clock — tired cues are the real signal."
)
_HEURISTIC_CAVEAT = (
    "Wake-window timing is a product heuristic (evidence_level low), not a clinical cutoff."
)


def _hhmm(total_min: float | None) -> str | None:
    if total_min is None:
        return None
    m = round(total_min) % 1440
    return f"{m // 60:02d}:{m % 60:02d}"


def _budget(band: AgeBand | None) -> dict | None:
    if band is None:
        return None
    return {
        "total_sleep_low_h": band.total_sleep_budget_hours.min,
        "total_sleep_high_h": band.total_sleep_budget_hours.max,
        "source": "clinical_anchor",
    }


def _age_band_ww(band: AgeBand | None) -> dict | None:
    if band is None:
        return None
    return {"min": band.wake_window_minutes.min, "max": band.wake_window_minutes.max}


def _effective_age(inp: PredictInput) -> int:
    return inp.corrected_age_months if inp.corrected_age_months is not None else inp.age_months


def predict_next(inp: PredictInput, bands: list[AgeBand]) -> Prediction:
    eff_age = _effective_age(inp)
    band = lookup(bands, eff_age)

    if eff_age < NEWBORN_MAX_MONTHS:
        budget = _budget(band)
        caveats = [
            (
                "Under 4 months: no nap-time prediction (newborn guardrail). Sleep is "
                "cue- and feed-driven — watch tired cues, not the clock."
            )
        ]
        if budget is not None:
            caveats.append(
                "Any total-sleep range is a broad normalcy guide, not a target."
            )
        return Prediction(
            status="newborn_guardrail",
            next_event=None,
            budget=budget,
            caveats=caveats,
            inputs_used={"effective_age_months": eff_age},
            age_band_wake_window=_age_band_ww(band),
        )

    if band is None:
        return Prediction(
            status="age_unknown",
            next_event=None,
            caveats=["No age-band heuristic available for this age."],
            inputs_used={"effective_age_months": eff_age},
            age_band_wake_window=_age_band_ww(band),
        )

    p = inp.personal
    if p is not None and p.stable and p.wake_window_median_min is not None:
        center_ww = p.wake_window_median_min
        half = max(p.wake_window_mad_min or 0.0, PERSONAL_HALF_WIDTH_FLOOR_MIN)
        if eff_age < YOUNG_AGE_WIDEN_UNDER_MONTHS:
            half *= YOUNG_AGE_WIDEN_FACTOR
        low_ww, high_ww = center_ww - half, center_ww + half
        basis, confidence = Basis.PERSONAL_BASELINE, "moderate"
        band_reason = (
            f"centered on the child's own recent wake window (~{round(center_ww)} min "
            f"over {p.days_of_data} days); band ±{round(half)} min"
        )
    else:
        low_ww = band.wake_window_minutes.min
        high_ww = band.wake_window_minutes.max
        center_ww = (low_ww + high_ww) / 2
        basis, confidence = Basis.AGE_ONLY, "low"
        band_reason = (
            "wide because this is an age-typical heuristic with no stable personal data yet; "
            "wake windows are a practitioner heuristic, not a clinical standard"
        )

    base = inp.last_wake_min
    ne = NextEvent(
        type=inp.target,
        window_low=_hhmm(base + low_ww),
        window_high=_hhmm(base + high_ww),
        center=_hhmm(base + center_ww),
        confidence=confidence,
        basis=basis.value,
        band_reason=band_reason,
    )
    return Prediction(
        status="computed",
        next_event=ne,
        budget=_budget(band),
        caveats=[_CUES_CAVEAT, _HEURISTIC_CAVEAT],
        inputs_used={
            "effective_age_months": eff_age,
            "last_wake_min": base,
            "basis": basis.value,
        },
        age_band_wake_window=_age_band_ww(band),
    )
