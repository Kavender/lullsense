"""Canonical, vendor-neutral data contract consumed by the reasoning layer."""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel


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
