"""Structured I/O for the next-sleep-event predictor. Pure data, no logic."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Basis(str, Enum):
    AGE_ONLY = "age_only"
    PERSONAL_BASELINE = "personal_baseline"


class PersonalStats(BaseModel):
    wake_window_median_min: float | None = None
    wake_window_mad_min: float | None = None
    typical_nap_minutes: float | None = None
    days_of_data: int = 0
    stable: bool = False


class PredictInput(BaseModel):
    age_months: int
    corrected_age_months: int | None = None
    last_wake_min: int                 # minutes since midnight of the last wake
    target: str = "nap"                # "nap" | "bedtime" (label only in Phase 1)
    as_of: datetime | None = None
    personal: PersonalStats | None = None


class NextEvent(BaseModel):
    type: str                          # "nap" | "bedtime"
    window_low: str | None             # HH:MM
    window_high: str | None
    center: str | None
    confidence: str                    # "low" | "moderate" — never "high"
    basis: str
    band_reason: str


class Prediction(BaseModel):
    status: str                        # "computed" | "newborn_guardrail" | "age_unknown"
    next_event: NextEvent | None = None
    budget: dict | None = None
    caveats: list[str] = []
    inputs_used: dict = {}
