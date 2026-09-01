from datetime import datetime

from baby_sleep.contract.enums import DataQuality, SleepType, StartMarker
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime, TimePrecision
from baby_sleep.ingest.normalize import classify_sleep_type, is_sane, normalize, resolve_end


def test_resolve_end_computes_from_duration():
    start = datetime(2026, 8, 24, 13, 0)
    end, dur = resolve_end(start, None, 80)
    assert end == datetime(2026, 8, 24, 14, 20) and dur == 80


def test_resolve_end_computes_duration_from_end():
    start = datetime(2026, 8, 24, 19, 36)
    end = datetime(2026, 8, 25, 6, 0)          # crosses midnight (explicit next-day date)
    got_end, dur = resolve_end(start, end, None)
    assert got_end == end and dur == 624       # 10h24m


def test_resolve_end_rolls_time_only_end_past_midnight():
    # end earlier than start on the same date => assume next day (manual-text case)
    start = datetime(2026, 8, 24, 19, 0)
    end = datetime(2026, 8, 24, 6, 0)
    got_end, dur = resolve_end(start, end, None)
    assert got_end == datetime(2026, 8, 25, 6, 0) and dur == 660


def test_is_sane_rejects_impossible():
    start = datetime(2026, 8, 24, 13, 0)
    assert is_sane(start, datetime(2026, 8, 24, 14, 20), 80) is True
    assert is_sane(start, None, 0) is False          # zero duration
    assert is_sane(start, None, 25 * 60) is False     # > 20h
    assert is_sane(start, datetime(2026, 8, 24, 12, 0), None) is False  # end before start


def test_is_sane_rejects_no_end_and_no_duration():
    # T1c: a session with neither an end time nor a duration is not analyzable.
    start = datetime(2026, 8, 24, 13, 0)
    assert is_sane(start, None, None) is False


def test_normalize_drops_session_with_no_end_or_duration():
    # T1c: no end + no duration must be dropped with a specific warning, not kept silently.
    log = SleepLog(sessions=[
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0))),   # no end, no duration
    ])
    out, warnings = normalize(log)
    assert out.sessions == []
    assert len(warnings) == 1
    assert "no end time or duration" in warnings[0].lower()


def _nap(h1, m1, h2, m2):
    return SleepSession(
        start=ApproxTime(value=datetime(2026, 8, 24, h1, m1)),
        end=ApproxTime(value=datetime(2026, 8, 24, h2, m2)),
        sleep_type=SleepType.NAP)


def test_normalize_drops_contained_overlapping_session():
    # T1a: a nap fully inside another nap is a double-log — drop the contained one, with a warning.
    log = SleepLog(sessions=[_nap(13, 0, 14, 10), _nap(13, 15, 13, 45)])
    out, warnings = normalize(log)
    assert len(out.sessions) == 1
    assert out.sessions[0].start.value == datetime(2026, 8, 24, 13, 0)
    assert out.sessions[0].end.value == datetime(2026, 8, 24, 14, 10)
    assert any("overlap" in w.lower() for w in warnings)


def test_normalize_trims_partial_overlap_and_marks_inferred():
    # T1a: partial overlap -> trim the later session's start to the earlier session's end,
    # recompute its duration, mark it inferred, and warn.
    log = SleepLog(sessions=[_nap(13, 0, 13, 45), _nap(13, 30, 14, 10)])
    out, warnings = normalize(log)
    assert len(out.sessions) == 2
    trimmed = out.sessions[1]
    assert trimmed.start.value == datetime(2026, 8, 24, 13, 45)   # trimmed to earlier end
    assert trimmed.end.value == datetime(2026, 8, 24, 14, 10)
    assert trimmed.duration_minutes == 25                          # 13:45 -> 14:10
    assert trimmed.data_quality is DataQuality.INFERRED
    assert any("overlap" in w.lower() for w in warnings)


def _night(d1, h1, m1, d2, h2, m2):
    return SleepSession(
        start=ApproxTime(value=datetime(2026, 8, d1, h1, m1)),
        end=ApproxTime(value=datetime(2026, 8, d2, h2, m2)),
        sleep_type=SleepType.NIGHT)


def test_normalize_repairs_forgot_to_stop_night_from_history():
    # T1b: a 14h+ "night" (timer left running) is truncated to the child's typical
    # morning wake (median of clean nights), marked inferred, and warned — not left to
    # poison the baseline.
    log = SleepLog(sessions=[
        _night(20, 19, 0, 21, 6, 0),      # clean, wake 06:00
        _night(21, 19, 0, 22, 6, 15),     # clean, wake 06:15
        _night(22, 19, 0, 23, 6, 30),     # clean, wake 06:30
        _night(23, 19, 0, 24, 9, 10),     # forgot-to-stop: 14h10m
    ])
    out, warnings = normalize(log)
    repaired = out.sessions[3]
    assert repaired.end.value == datetime(2026, 8, 24, 6, 15)     # median clean wake
    assert repaired.duration_minutes == 675                       # 19:00 -> 06:15 = 11h15
    assert repaired.data_quality is DataQuality.INFERRED
    assert any("forgot-to-stop" in w.lower() for w in warnings)
    # clean nights are untouched
    assert out.sessions[0].data_quality is DataQuality.LOGGED


def test_normalize_drops_forgot_to_stop_when_history_insufficient():
    # T1b reset fallback: with fewer than 3 clean nights there's no basis to repair —
    # drop the bad night with a warning rather than keep or silently repair it.
    log = SleepLog(sessions=[
        _night(20, 19, 0, 21, 6, 0),      # one clean night only
        _night(21, 19, 0, 22, 9, 20),     # forgot-to-stop: 14h20m
    ])
    out, warnings = normalize(log)
    assert len(out.sessions) == 1
    assert out.sessions[0].start.value == datetime(2026, 8, 20, 19, 0)
    assert any("forgot-to-stop" in w.lower() and "insufficient" in w.lower() for w in warnings)


def test_classify_night_when_crosses_midnight():
    assert classify_sleep_type(datetime(2026, 8, 24, 19, 36), 624, True) is SleepType.NIGHT


def test_classify_night_by_evening_start_and_long_duration():
    assert classify_sleep_type(datetime(2026, 8, 24, 20, 0), 5 * 60, False) is SleepType.NIGHT


def test_classify_nap_daytime_short():
    assert classify_sleep_type(datetime(2026, 8, 24, 13, 0), 80, False) is SleepType.NAP


def test_normalize_fills_types_and_drops_impossible():
    log = SleepLog(sessions=[
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 19, 36)),
                     end=ApproxTime(value=datetime(2026, 8, 25, 6, 0))),          # night, midnight
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)),
                     duration_minutes=80),                                         # nap
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 15, 0)),
                     duration_minutes=45),                                         # 2nd nap same day
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 9, 0)),
                     duration_minutes=0),                                          # impossible -> dropped
    ])
    out, warnings = normalize(log)   # no convention; default UNKNOWN marks => no shift
    assert [s.sleep_type for s in out.sessions] == [SleepType.NIGHT, SleepType.NAP, SleepType.NAP]
    assert out.sessions[0].duration_minutes == 624
    assert len(warnings) == 1 and "dropped" in warnings[0].lower()


def test_normalize_shifts_put_down_to_asleep_when_convention_given():
    # family logs put-down time; SOL known => canonical start becomes ASLEEP
    log = SleepLog(sessions=[
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)),
                     duration_minutes=35, onset_latency_minutes=20),   # 35-min logged nap
    ])
    out, _warnings = normalize(log, start_convention=StartMarker.PUT_DOWN)
    s = out.sessions[0]
    assert s.start.value == datetime(2026, 8, 24, 13, 20)   # asleep = put_down + 20
    assert s.put_down_at.value == datetime(2026, 8, 24, 13, 0)
    assert s.duration_minutes == 15                          # real sleep, not 35
    assert s.start_marks is StartMarker.ASLEEP
    assert s.onset_latency_minutes == 20                     # SOL retained, never discarded


def test_normalize_flags_put_down_without_onset():
    log = SleepLog(sessions=[
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)),
                     duration_minutes=60, start_marks=StartMarker.PUT_DOWN)])   # no SOL
    out, warnings = normalize(log)
    assert out.sessions[0].duration_minutes == 60            # preserved, not shifted
    assert any("uncertain" in w.lower() for w in warnings)


def test_normalize_asleep_convention_is_noop():
    log = SleepLog(sessions=[
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)),
                     duration_minutes=35, onset_latency_minutes=20)])
    out, _ = normalize(log, start_convention=StartMarker.ASLEEP)
    assert out.sessions[0].start.value == datetime(2026, 8, 24, 13, 0)   # unchanged
    assert out.sessions[0].put_down_at is None


def test_normalize_persists_rolled_end_for_time_only_midnight_crossing():
    # C1 regression: a time-only end that lands before start must be rolled to the
    # next day AND that rolled value must be persisted (not the original un-rolled end),
    # so the stored record stays internally consistent (end > start, duration matches).
    log = SleepLog(sessions=[
        SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 19, 30)),
                     end=ApproxTime(value=datetime(2026, 8, 24, 6, 30)))])   # 6:30 == next morning
    out, _ = normalize(log)
    s = out.sessions[0]
    assert s.end.value == datetime(2026, 8, 25, 6, 30)          # rolled, persisted
    assert s.end.value > s.start.value
    assert s.duration_minutes == 660
    assert int((s.end.value - s.start.value).total_seconds() // 60) == s.duration_minutes
    assert s.sleep_type is SleepType.NIGHT


def test_normalize_put_down_at_preserves_original_anchor_metadata():
    # M1 regression: when start is shifted put-down -> asleep, put_down_at must retain
    # the original anchor's precision/uncertainty/raw, not become a bare EXACT time.
    log = SleepLog(sessions=[
        SleepSession(
            start=ApproxTime(value=datetime(2026, 8, 24, 19, 0),
                             precision=TimePrecision.APPROXIMATE,
                             uncertainty_minutes=15, raw="put her down around 7pm"),
            duration_minutes=60, onset_latency_minutes=10,
            start_marks=StartMarker.PUT_DOWN)])
    out, _ = normalize(log)
    s = out.sessions[0]
    assert s.start.value == datetime(2026, 8, 24, 19, 10)       # shifted asleep
    assert s.put_down_at.value == datetime(2026, 8, 24, 19, 0)
    assert s.put_down_at.precision is TimePrecision.APPROXIMATE  # metadata preserved
    assert s.put_down_at.uncertainty_minutes == 15
    assert s.put_down_at.raw == "put her down around 7pm"
