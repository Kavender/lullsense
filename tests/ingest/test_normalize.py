from datetime import datetime
from baby_sleep.ingest.normalize import resolve_end, is_sane


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
