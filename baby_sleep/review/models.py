"""Structured, inspectable review output. No prose, no diagnosis — the persona owns voice."""
from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel

from baby_sleep.detect.models import Signal, SignalName

# Ordered parent-facing domains. A "quiet" review names the steady ones.
DOMAINS: list[str] = ["night_sleep", "naps", "bedtime", "total_sleep", "schedule_consistency"]

# Each detector signal maps to exactly one domain. The context wrapper is intentionally
# excluded (it reframes the whole review; it is not a domain finding).
SIGNAL_DOMAIN: dict[SignalName, str] = {
    SignalName.EARLY_WAKING: "night_sleep",
    SignalName.NIGHT_WAKING: "night_sleep",
    SignalName.SPLIT_NIGHT: "night_sleep",
    SignalName.SHORT_NAP: "naps",
    SignalName.NAP_TRANSITION: "naps",
    SignalName.BEDTIME_RESISTANCE: "bedtime",
    SignalName.TOTAL_SLEEP_DROP: "total_sleep",
    SignalName.HIGH_VARIABILITY: "schedule_consistency",
    SignalName.SCHEDULE_DRIFT: "schedule_consistency",
}

# Correlated-signal dedupe: a dominant signal explains the dominated ones, which then
# fold into it (not surfaced, not counted separately).
DOMINANCE: dict[SignalName, set[SignalName]] = {
    SignalName.SPLIT_NIGHT: {SignalName.NIGHT_WAKING, SignalName.EARLY_WAKING},
    SignalName.NAP_TRANSITION: {SignalName.SHORT_NAP},
}


class ReviewStatus(str, Enum):
    COMPUTED = "computed"
    STALE_DATA = "stale_data"
    INSUFFICIENT_DATA = "insufficient_data"
    BELOW_SUPPORTED_RANGE = "below_supported_range"
    AGE_UNKNOWN = "age_unknown"


class Coverage(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    n_days: int = 0
    span_days: int = 0
    days_since_last_entry: int | None = None
    is_current: bool = False
    covers_window: bool | None = None


class ReviewSummary(BaseModel):
    status: ReviewStatus
    coverage: Coverage
    surfaced: list[Signal] = []
    also_noted_count: int = 0
    steady_domains: list[str] = []
    context_note: Signal | None = None
    reason: str | None = None
