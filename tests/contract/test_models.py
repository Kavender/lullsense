from datetime import date, datetime

from baby_sleep.contract.enums import DataQuality, EventKind, Location, SleepType, StartMarker
from baby_sleep.contract.models import (
    Child,
    ContextEvent,
    SleepLog,
    SleepSession,
    age_months_from_dob,
    corrected_age_months,
)
from baby_sleep.contract.time_types import ApproxTime


def test_age_months_from_dob_full_year():
    # dob 2025-01-15, as_of 2026-01-15 => exactly 12 months
    assert age_months_from_dob(date(2025, 1, 15), date(2026, 1, 15)) == 12


def test_age_months_from_dob_pre_birthday_rollover():
    # dob 2025-01-20, as_of 2026-01-15 => 11 months (Jan 20 birthday not yet reached)
    assert age_months_from_dob(date(2025, 1, 20), date(2026, 1, 15)) == 11


def test_age_months_from_dob_exact_same_day():
    # dob 2025-01-15, as_of 2025-01-15 => 0 months (just born)
    assert age_months_from_dob(date(2025, 1, 15), date(2025, 1, 15)) == 0


def test_age_months_from_dob_newborn_guard():
    # as_of before dob => 0 (never negative)
    assert age_months_from_dob(date(2025, 6, 1), date(2025, 1, 1)) == 0


def test_age_months_from_dob_leap_day_dob():
    # Feb-29 DOB: on the month-end anniversary (Feb 28 in a non-leap year) => 12 months
    assert age_months_from_dob(date(2024, 2, 29), date(2025, 2, 28)) == 12


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
