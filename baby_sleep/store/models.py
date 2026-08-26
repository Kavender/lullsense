"""Persistable state for the experiment loop (D5) and explicitly-saved family
constraints (D21). Raw sleep logs are NOT modeled here — they stay ephemeral."""
from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel


class ExperimentStatus(str, Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    REVIEWING = "reviewing"
    CONCLUDED = "concluded"


class Experiment(BaseModel):
    id: str
    hypothesis: str
    change: str
    metrics: list[str]
    start_date: date
    review_after_days: int
    status: ExperimentStatus = ExperimentStatus.PROPOSED
    outcome: str | None = None


class SavedConstraint(BaseModel):
    key: str
    value: str
    note: str | None = None


class ChildProfile(BaseModel):
    name: str | None = None
    dob: date | None = None
    gestational_age_at_birth_weeks: int | None = None
