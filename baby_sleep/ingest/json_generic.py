"""Generic JSON adapter: map a list of records onto the canonical contract."""
from __future__ import annotations

import json

from baby_sleep.contract.enums import DataQuality
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.ingest.csv_generic import _parse_dt, _parse_location, DEFAULT_FORMATS


class GenericJsonAdapter:
    def __init__(self, field_map: dict[str, str], datetime_formats: list[str] | None = None):
        self.field_map = field_map
        self.formats = tuple(datetime_formats) if datetime_formats else DEFAULT_FORMATS

    def parse(self, text: str) -> SleepLog:
        records = json.loads(text)
        sessions: list[SleepSession] = []
        for rec in records:
            start = _parse_dt(str(rec.get(self.field_map.get("start", "start"), "")), self.formats)
            if start is None:
                continue
            end = _parse_dt(str(rec.get(self.field_map.get("end", ""), "")), self.formats)
            loc_field = self.field_map.get("location")
            location = _parse_location(rec.get(loc_field) if loc_field else None)
            sessions.append(SleepSession(
                start=ApproxTime(value=start),
                end=ApproxTime(value=end) if end else None,
                location=location,
                data_quality=DataQuality.LOGGED,
                source="generic_json",
            ))
        return SleepLog(sessions=sessions, source="generic_json")
