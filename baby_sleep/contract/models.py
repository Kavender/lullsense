"""Canonical, vendor-neutral data contract consumed by the reasoning layer."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

from .enums import DataQuality, EventKind, Location, SleepType, StartMarker
from .time_types import ApproxTime


def corrected_age_months(age_months: int, gestational_age_at_birth_weeks: int | None) -> int:
    """Chronological age adjusted for prematurity (D20). Full term (>=40wk) or
    unknown gestation => unchanged. Never returns below 0."""
    if gestational_age_at_birth_weeks is None or gestational_age_at_birth_weeks >= 40:
        return age_months
    weeks_early = 40 - gestational_age_at_birth_weeks
    months_early = round(weeks_early / 4.345)
    return max(0, age_months - months_early)


class Child(BaseModel):
    age_months: int | None = None
    dob: date | None = None
    gestational_age_at_birth_weeks: int | None = None

    def corrected_age_months(self) -> int | None:
        if self.age_months is None:
            return None
        return corrected_age_months(self.age_months, self.gestational_age_at_birth_weeks)


class SleepSession(BaseModel):
    start: ApproxTime                       # canonical meaning: ASLEEP (sleep onset)
    end: ApproxTime | None = None
    duration_minutes: int | None = None
    sleep_type: SleepType = SleepType.UNKNOWN
    location: Location = Location.UNKNOWN
    start_marks: StartMarker = StartMarker.UNKNOWN   # what the logged anchor represents
    onset_latency_minutes: int | None = None          # SOL; never folded into start
    put_down_at: ApproxTime | None = None             # provenance when start was shifted asleep
    self_settled: bool | None = None
    night_wakings: int | None = None
    data_quality: DataQuality = DataQuality.LOGGED
    source: str = ""
    notes: str | None = None


class ContextEvent(BaseModel):
    kind: EventKind
    at: ApproxTime
    label: str | None = None
    amount_ml: int | None = None
    data_quality: DataQuality = DataQuality.LOGGED
    source: str = ""
    notes: str | None = None


class SleepLog(BaseModel):
    child: Child = Child()
    sessions: list[SleepSession] = []
    events: list[ContextEvent] = []
    source: str = ""
    parsed_at: datetime | None = None
