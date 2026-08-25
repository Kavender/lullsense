"""Best-effort manual-text parser. Handles a small set of common phrasings and
preserves uncertainty for approximate times. Unrecognized lines -> warnings."""
from __future__ import annotations

import re
from datetime import date, datetime

from baby_sleep.contract.enums import DataQuality, Location, StartMarker
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime, TimePrecision

_CLOCK = r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?"
_RANGE_RE = re.compile(_CLOCK + r"\s*-\s*" + _CLOCK, re.IGNORECASE)
_AROUND_RE = re.compile(r"around\s+" + _CLOCK, re.IGNORECASE)
APPROX_WINDOW_MINUTES = 15


def _start_marks(line: str) -> StartMarker:
    low = line.lower()
    if "asleep" in low or "fell asleep" in low:
        return StartMarker.ASLEEP
    if "put down" in low or "put her down" in low or "put him down" in low \
            or "put to bed" in low or "bedtime" in low:
        return StartMarker.PUT_DOWN
    return StartMarker.UNKNOWN


def _to_dt(ref: date, hour: str, minute: str | None, ampm: str | None) -> datetime:
    h = int(hour)
    m = int(minute) if minute else 0
    if ampm:
        ampm = ampm.lower()
        if ampm == "pm" and h != 12:
            h += 12
        elif ampm == "am" and h == 12:
            h = 0
    return datetime(ref.year, ref.month, ref.day, h, m)


def _location(line: str) -> Location:
    low = line.lower()
    if "daycare" in low or "day care" in low or "nursery" in low:
        return Location.DAYCARE
    if "home" in low:
        return Location.HOME
    return Location.UNKNOWN


def parse_manual_text(text: str, reference_date: date) -> tuple[SleepLog, list[str]]:
    sessions: list[SleepSession] = []
    warnings: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        loc = _location(line)
        marks = _start_marks(line)
        rng = _RANGE_RE.search(line)
        if rng:
            start = _to_dt(reference_date, rng.group(1), rng.group(2), rng.group(3))
            end = _to_dt(reference_date, rng.group(4), rng.group(5), rng.group(6))
            sessions.append(SleepSession(
                start=ApproxTime(value=start, raw=line),
                end=ApproxTime(value=end, raw=line),
                location=loc, start_marks=marks,
                data_quality=DataQuality.REPORTED, source="manual_text"))
            continue
        around = _AROUND_RE.search(line)
        if around:
            start = _to_dt(reference_date, around.group(1), around.group(2), around.group(3))
            sessions.append(SleepSession(
                start=ApproxTime(value=start, precision=TimePrecision.APPROXIMATE,
                                 uncertainty_minutes=APPROX_WINDOW_MINUTES, raw=line),
                location=loc, start_marks=marks,
                data_quality=DataQuality.REPORTED, source="manual_text"))
            continue
        warnings.append(f"could not parse line: {line!r}")
    return SleepLog(sessions=sessions, source="manual_text"), warnings
