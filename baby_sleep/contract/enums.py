"""Controlled vocabularies for the canonical contract. No vendor terms here."""
from __future__ import annotations

from enum import Enum


class SleepType(str, Enum):
    NAP = "nap"
    NIGHT = "night"
    UNKNOWN = "unknown"


class Location(str, Enum):
    HOME = "home"
    DAYCARE = "daycare"
    OTHER = "other"
    UNKNOWN = "unknown"


class EventKind(str, Enum):
    FEED = "feed"
    DIAPER = "diaper"
    MEDICATION = "medication"
    PUMP = "pump"
    OTHER = "other"


class DataQuality(str, Enum):
    LOGGED = "logged"
    REPORTED = "reported"
    INFERRED = "inferred"


class StartMarker(str, Enum):
    """What a sleep session's logged start timestamp represents."""
    PUT_DOWN = "put_down"   # laid down / settling began
    ASLEEP = "asleep"       # actually asleep (sleep onset) — the canonical meaning
    UNKNOWN = "unknown"
