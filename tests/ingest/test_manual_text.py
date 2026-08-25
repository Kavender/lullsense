from datetime import date

from baby_sleep.contract.enums import Location, StartMarker
from baby_sleep.contract.time_types import TimePrecision
from baby_sleep.ingest.manual_text import parse_manual_text

REF = date(2026, 8, 24)


def test_parses_time_range_nap():
    log, _warnings = parse_manual_text("Nap 1:15pm-2:35pm", REF)
    assert len(log.sessions) == 1
    s = log.sessions[0]
    assert s.start.value.hour == 13 and s.start.value.minute == 15
    assert s.end.value.hour == 14 and s.end.value.minute == 35


def test_parses_approximate_bedtime_with_uncertainty():
    log, _ = parse_manual_text("bedtime around 7pm", REF)
    s = log.sessions[0]
    assert s.start.precision is TimePrecision.APPROXIMATE
    assert s.start.uncertainty_minutes == 15
    assert s.start.value.hour == 19


def test_parses_daycare_label():
    log, _ = parse_manual_text("nap at daycare 12:30pm-1:30pm", REF)
    assert log.sessions[0].location is Location.DAYCARE


def test_unrecognized_line_becomes_warning():
    log, warnings = parse_manual_text("he was cranky all afternoon", REF)
    assert log.sessions == []
    assert len(warnings) == 1


def test_detects_start_marker_from_phrasing():
    asleep, _ = parse_manual_text("fell asleep 7:30pm-6:30am", REF)
    assert asleep.sessions[0].start_marks is StartMarker.ASLEEP
    putdown, _ = parse_manual_text("put her down around 7pm", REF)
    assert putdown.sessions[0].start_marks is StartMarker.PUT_DOWN
    neutral, _ = parse_manual_text("Nap 1:15pm-2:35pm", REF)
    assert neutral.sessions[0].start_marks is StartMarker.UNKNOWN
