"""Output models for the analyze layer. Vendor-neutral, computed from the contract."""
from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel

from baby_sleep.contract.enums import Location
from baby_sleep.contract.models import ContextEvent, SleepSession


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BaselineStatus(str, Enum):
    COMPUTED = "computed"
    BELOW_SUPPORTED_RANGE = "below_supported_range"
    AGE_UNKNOWN = "age_unknown"
    INSUFFICIENT_DATA = "insufficient_data"


class NapFeature(BaseModel):
    start: datetime
    end: datetime | None = None
    duration_minutes: int | None = None


class SleepDay(BaseModel):
    day: date
    night_segments: list[SleepSession] = []
    naps: list[SleepSession] = []
    events: list[ContextEvent] = []


class DailyFeatures(BaseModel):
    day: date
    rise_time: datetime | None = None
    in_bed_time: datetime | None = None
    sleep_onset_time: datetime | None = None
    sleep_onset_latency_min: int | None = None
    night_sleep_duration_min: int | None = None
    night_waking_count: int | None = None
    total_awake_overnight_min: int | None = None
    longest_night_waking_min: int | None = None
    nap_count: int = 0
    naps: list[NapFeature] = []
    total_daytime_sleep_min: int | None = None
    total_24h_sleep_min: int | None = None
    pre_nap_awake_min: list[int] = []
    wake_windows_min: list[int] = []
    is_weekend: bool | None = None
    location: Location = Location.UNKNOWN
    approx_share: float = 0.0
    repaired_share: float = 0.0            # share of sessions repaired by the D15 ingest layer
    day_confidence: Confidence = Confidence.HIGH


class FeatureSeries(BaseModel):
    days: list[DailyFeatures] = []
    bedtime_variability_min: float | None = None
    rise_time_variability_min: float | None = None
    nap_time_variability_min: float | None = None
    total_sleep_variability_min: float | None = None
    weekday_vs_weekend: dict[str, float] = {}
    missing_data_rate: float = 0.0


class FeatureBaseline(BaseModel):
    feature: str
    baseline_median: float
    mad: float
    n: int
    recent_median: float | None = None
    deviation: float | None = None
    deviation_mads: float | None = None
    source: str = "history"
    confidence: Confidence = Confidence.MEDIUM


class Baseline(BaseModel):
    status: BaselineStatus
    reason: str | None = None
    features: dict[str, FeatureBaseline] = {}
    prior_window_days: int = 0
    recent_window_days: int = 0
    corrected_age_months: int | None = None
