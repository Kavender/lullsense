"""Generic CSV adapter: map arbitrary columns onto the canonical contract."""
from __future__ import annotations

import csv
import io
from datetime import datetime

from baby_sleep.contract.enums import DataQuality, Location
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime

DEFAULT_FORMATS = ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M")


def _parse_dt(text: str, formats: tuple[str, ...]) -> datetime | None:
    text = (text or "").strip()
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _parse_location(text: str | None) -> Location:
    t = (text or "").strip().lower()
    if t in ("home", "house"):
        return Location.HOME
    if t in ("daycare", "day care", "nursery"):
        return Location.DAYCARE
    if not t:
        return Location.UNKNOWN
    return Location.OTHER


class GenericCsvAdapter:
    def __init__(self, column_map: dict[str, str], datetime_formats: list[str] | None = None):
        self.column_map = column_map
        self.formats = tuple(datetime_formats) if datetime_formats else DEFAULT_FORMATS

    def parse(self, text: str) -> SleepLog:
        reader = csv.DictReader(io.StringIO(text))
        sessions: list[SleepSession] = []
        for row in reader:
            start = _parse_dt(row.get(self.column_map.get("start", "start"), ""), self.formats)
            if start is None:
                continue
            end = _parse_dt(row.get(self.column_map.get("end", ""), ""), self.formats)
            loc_col = self.column_map.get("location")
            location = _parse_location(row.get(loc_col) if loc_col else None)
            sessions.append(SleepSession(
                start=ApproxTime(value=start),
                end=ApproxTime(value=end) if end else None,
                location=location,
                data_quality=DataQuality.LOGGED,
                source="generic_csv",
            ))
        return SleepLog(sessions=sessions, source="generic_csv")
