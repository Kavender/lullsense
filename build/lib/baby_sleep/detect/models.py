"""Structured, inspectable detector output (spec §10). No diagnosis, ever."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

from baby_sleep.analyze.models import Baseline, Confidence, FeatureSeries
from baby_sleep.contract.models import ContextEvent


class SignalName(str, Enum):
    EARLY_WAKING = "early_waking"
    NIGHT_WAKING = "night_waking"
    SHORT_NAP = "short_nap"
    TOTAL_SLEEP_DROP = "total_sleep_drop"
    BEDTIME_RESISTANCE = "bedtime_resistance"
    SPLIT_NIGHT = "split_night"
    HIGH_VARIABILITY = "high_variability"
    SCHEDULE_DRIFT = "schedule_drift"
    NAP_TRANSITION = "nap_transition"
    POSSIBLE_CONTEXT_RELATED_DISRUPTION = "possible_context_related_disruption"


class Severity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"


class SignalStatus(str, Enum):
    EMERGING = "emerging"
    ESTABLISHED = "established"


class SignalWindow(BaseModel):
    window_days: int
    value: float | None = None
    label: str | None = None


class Signal(BaseModel):
    signal: SignalName
    confidence: Confidence
    severity: Severity
    status: SignalStatus
    baseline: SignalWindow | None = None
    recent: SignalWindow | None = None
    change: float | None = None
    change_unit: str = "minutes"
    supporting_evidence: list[str] = []
    limitations: list[str] = []


class DetectorInput(BaseModel):
    series: FeatureSeries
    baseline: Baseline
    events: list[ContextEvent] = []
    reported_context: list[str] = []
