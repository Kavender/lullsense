"""Huckleberry official-CSV adapter. Maps the vendor's per-Type overloaded
columns onto the canonical contract. Official CSV export only — no vendor API."""
from __future__ import annotations

import csv
import io
import re
from datetime import datetime

from baby_sleep.contract.enums import DataQuality, EventKind
from baby_sleep.contract.models import ContextEvent, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime

_HB_DT = "%Y-%m-%d %H:%M"
_RANGE = re.compile(r"(\d+)\s*-\s*(\d+)_minutes")
_SINGLE = re.compile(r"(\d+)_minutes")
_ML = re.compile(r"(\d+)\s*ml", re.IGNORECASE)

# Normalize a few common vendor med labels to a generic vocabulary.
_MED_NORMALIZE = {
    "tylenol": "acetaminophen",
    "motrin": "ibuprofen",
    "advil": "ibuprofen",
    "ibuprofen": "ibuprofen",
    "acetaminophen": "acetaminophen",
}


def _dt(text: str) -> datetime | None:
    text = (text or "").strip()
    try:
        return datetime.strptime(text, _HB_DT)
    except ValueError:
        return None


def _duration_to_minutes(text: str) -> int | None:
    text = (text or "").strip()
    if not text or ":" not in text:
        return None
    try:
        h, m = text.split(":")
        return int(h) * 60 + int(m)
    except ValueError:
        return None


def _onset_minutes(start_condition: str) -> int | None:
    m = _RANGE.search(start_condition or "")
    if m:
        return (int(m.group(1)) + int(m.group(2))) // 2
    m = _SINGLE.search(start_condition or "")
    if m:
        return int(m.group(1))
    return None


def _ml(text: str) -> int | None:
    m = _ML.search(text or "")
    return int(m.group(1)) if m else None


def _normalize_med(name: str) -> str | None:
    low = (name or "").lower()
    for key, norm in _MED_NORMALIZE.items():
        if key in low:
            return norm
    return (name or "").strip().lower() or None


class HuckleberryCsvAdapter:
    def parse(self, text: str) -> SleepLog:
        reader = csv.DictReader(io.StringIO(text))
        sessions: list[SleepSession] = []
        events: list[ContextEvent] = []
        for row in reader:
            kind = (row.get("Type") or "").strip()
            start = _dt(row.get("Start", ""))
            if start is None:
                continue
            at = ApproxTime(value=start)
            if kind == "Sleep":
                end = _dt(row.get("End", ""))
                cond = row.get("Start Condition", "") or ""
                loc = (row.get("Start Location", "") or "").strip().lower()
                sessions.append(SleepSession(
                    start=at,
                    end=ApproxTime(value=end) if end else None,
                    duration_minutes=_duration_to_minutes(row.get("Duration", "")),
                    onset_latency_minutes=_onset_minutes(cond),
                    self_settled=True if "on own" in loc else (False if loc else None),
                    data_quality=DataQuality.LOGGED,
                    source="huckleberry_csv",
                ))
            elif kind == "Feed":
                events.append(ContextEvent(
                    kind=EventKind.FEED, at=at,
                    label=(row.get("Start Condition", "") or "").strip().lower() or None,
                    amount_ml=_ml(row.get("End Condition", "")),
                    source="huckleberry_csv"))
            elif kind == "Diaper":
                events.append(ContextEvent(
                    kind=EventKind.DIAPER, at=at,
                    label=(row.get("Start Condition", "") or "").strip().lower() or None,
                    notes=(row.get("End Condition", "") or "").strip() or None,
                    source="huckleberry_csv"))
            elif kind == "Meds":
                events.append(ContextEvent(
                    kind=EventKind.MEDICATION, at=at,
                    label=_normalize_med(row.get("Start Location", "")),
                    notes=(row.get("Start Condition", "") or "").strip() or None,
                    source="huckleberry_csv"))
            elif kind == "Pump":
                events.append(ContextEvent(
                    kind=EventKind.PUMP, at=at,
                    amount_ml=_ml(row.get("Duration", "")),
                    source="huckleberry_csv"))
            else:
                events.append(ContextEvent(kind=EventKind.OTHER, at=at, source="huckleberry_csv"))
        return SleepLog(sessions=sessions, events=events, source="huckleberry_csv")
