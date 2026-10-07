"""CAM-12 wire contract, schema version 1 (lullsense-app spec §3.1). Mirrors the TS
validator: unknown keys rejected, every timestamp ISO 8601 with an offset."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

SCHEMA_VERSION = 1


def _aware(v: object) -> datetime:
    if not isinstance(v, str):
        raise ValueError("expected an ISO 8601 string")  # noqa: TRY004 — pydantic maps ValueError
    dt = datetime.fromisoformat(v)          # fixed offset, as sent
    if dt.tzinfo is None:
        raise ValueError("timestamp needs an offset")
    return dt


def _zone(v: str) -> str:
    try:
        ZoneInfo(v)
    except (ZoneInfoNotFoundError, ValueError, OSError):   # not-found is a KeyError
        raise ValueError("unknown time zone") from None
    return v


AwareDt = Annotated[datetime, BeforeValidator(_aware)]
Precision = Literal["exact", "approx"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class Waking(_Strict):
    wokeAt: AwareDt
    backAsleepAt: AwareDt | None = None
    unresolved: bool = False


class Record(_Strict):
    id: str = Field(min_length=1, max_length=64)
    kind: Literal["nap", "night_sleep"]
    tz: Annotated[str, Field(min_length=1, max_length=64), AfterValidator(_zone)]
    start: AwareDt
    end: AwareDt
    startPrecision: Precision
    endPrecision: Precision
    wakings: list[Waking] = Field(default=[], max_length=20)

    @model_validator(mode="after")
    def _shape(self) -> Record:
        if self.end <= self.start:          # aware: compares instants
            raise ValueError("end must be after start")
        if self.wakings and self.kind != "night_sleep":
            raise ValueError("wakings only on night_sleep")
        return self


class ChildIn(_Strict):
    ageMonths: int | None = Field(default=None, ge=0, le=72)


class AnalysisRequest(_Strict):
    schemaVersion: Literal[1]
    op: Literal["analyze", "detect", "review"]
    asOf: AwareDt
    requestedWindowDays: int | None = Field(default=None, ge=1, le=28)
    child: ChildIn
    records: list[Record] = Field(max_length=400)

    @field_validator("records")
    @classmethod
    def _unique_ids(cls, v: list[Record]) -> list[Record]:
        if len({r.id for r in v}) != len(v):
            raise ValueError("record ids must be unique")
        return v
