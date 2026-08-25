from datetime import datetime

from baby_sleep.contract.enums import DataQuality, EventKind, Location, SleepType, StartMarker
from baby_sleep.contract.models import (
    Child,
    ContextEvent,
    SleepLog,
    SleepSession,
    corrected_age_months,
)
from baby_sleep.contract.time_types import ApproxTime


def test_corrected_age_full_term_unchanged():
    # 40 weeks gestation => no correction
    assert corrected_age_months(10, 40) == 10
    assert corrected_age_months(10, None) == 10


def test_corrected_age_preterm_subtracts_prematurity():
    # born at 32 weeks => 8 weeks early ~= 2 months; a 6mo chrono => ~4mo corrected
    assert corrected_age_months(6, 32) == 4


def test_corrected_age_never_negative():
    assert corrected_age_months(1, 28) == 0


def test_child_method_uses_age_months():
    assert Child(age_months=6, gestational_age_at_birth_weeks=32).corrected_age_months() == 4
    assert Child().corrected_age_months() is None


def test_sleep_session_defaults():
    s = SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)))
    assert s.sleep_type is SleepType.UNKNOWN
    assert s.location is Location.UNKNOWN
    assert s.data_quality is DataQuality.LOGGED
    assert s.start_marks is StartMarker.UNKNOWN
    assert s.put_down_at is None
    assert s.end is None and s.duration_minutes is None


def test_context_event_amount():
    e = ContextEvent(kind=EventKind.FEED, at=ApproxTime(value=datetime(2026, 8, 24, 11, 20)),
                     label="formula", amount_ml=110)
    assert e.kind is EventKind.FEED and e.amount_ml == 110


def test_sleep_log_aggregates_and_roundtrips():
    log = SleepLog(
        sessions=[SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)),
                               duration_minutes=80, sleep_type=SleepType.NAP)],
        events=[ContextEvent(kind=EventKind.DIAPER, at=ApproxTime(value=datetime(2026, 8, 24, 7, 44)))],
        source="unit-test",
    )
    dumped = log.model_dump()
    restored = SleepLog.model_validate(dumped)
    assert restored.sessions[0].duration_minutes == 80
    assert restored.events[0].kind is EventKind.DIAPER
