"""Output models for the analyze layer. Vendor-neutral, computed from the contract."""
from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel

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
