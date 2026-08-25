"""Time representation that preserves uncertainty for approximate inputs."""
from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field


class TimePrecision(str, Enum):
    EXACT = "exact"
    APPROXIMATE = "approximate"


class ApproxTime(BaseModel):
    value: datetime
    precision: TimePrecision = TimePrecision.EXACT
    uncertainty_minutes: int = Field(default=0, ge=0)
    raw: str | None = None

    @property
    def earliest(self) -> datetime:
        return self.value - timedelta(minutes=self.uncertainty_minutes)

    @property
    def latest(self) -> datetime:
        return self.value + timedelta(minutes=self.uncertainty_minutes)
