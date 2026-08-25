"""Phase 1 acceptance (spec §18): no vendor field leaks; approximate times keep
uncertainty; midnight crossing, missing values, multiple naps, daycare/home labels."""
from datetime import date
from pathlib import Path

from baby_sleep.contract.enums import Location, SleepType
from baby_sleep.contract.schema import export_json_schema
from baby_sleep.contract.time_types import TimePrecision
from baby_sleep.ingest.csv_generic import GenericCsvAdapter
from baby_sleep.ingest.huckleberry import HuckleberryCsvAdapter
from baby_sleep.ingest.manual_text import parse_manual_text
from baby_sleep.ingest.normalize import normalize

FIXTURE = Path(__file__).parent.parent / "fixtures" / "huckleberry_sample.csv"


def test_no_vendor_field_leaks_end_to_end():
    import json
    text = json.dumps(export_json_schema()).lower()
    assert "start condition" not in text and "huckleberry" not in text


def test_midnight_crossing_and_multiple_naps_and_missing_values():
    log = HuckleberryCsvAdapter().parse(FIXTURE.read_text())
    out, warnings = normalize(log)
    nights = [s for s in out.sessions if s.sleep_type is SleepType.NIGHT]
    naps = [s for s in out.sessions if s.sleep_type is SleepType.NAP]
    assert len(nights) == 2                      # both cross midnight
    assert len(naps) == 3                        # multiple naps in one day
    assert any(s.duration_minutes == 624 for s in nights)   # midnight duration preserved
    assert len(warnings) == 1                    # missing/impossible row dropped, reported


def test_daycare_home_labels_from_structured_and_text():
    csv_log = GenericCsvAdapter(column_map={"start": "start", "end": "end", "location": "where"}).parse(
        "start,end,where\n2026-08-24 12:30,2026-08-24 14:00,daycare\n")
    assert csv_log.sessions[0].location is Location.DAYCARE
    text_log, _ = parse_manual_text("nap at home 1:00pm-2:00pm", date(2026, 8, 24))
    assert text_log.sessions[0].location is Location.HOME


def test_approximate_time_retains_uncertainty():
    log, _ = parse_manual_text("bedtime around 7pm", date(2026, 8, 24))
    s = log.sessions[0]
    assert s.start.precision is TimePrecision.APPROXIMATE
    assert s.start.uncertainty_minutes > 0
    assert s.start.earliest < s.start.value < s.start.latest


def test_saved_family_convention_drives_normalization(tmp_path):
    # D21 loop: a saved per-family convention shifts logged put-down times to asleep,
    # so canonical start/duration are consistent and SOL is preserved.
    from baby_sleep.contract.enums import StartMarker
    from baby_sleep.store.experiment_store import ExperimentStore
    from baby_sleep.store.models import SavedConstraint
    store = ExperimentStore(tmp_path / "state")
    store.save_constraint(SavedConstraint(key="sleep_start_convention", value="put_down"))
    convention = StartMarker(store.get_constraint("sleep_start_convention").value)

    log = HuckleberryCsvAdapter().parse(FIXTURE.read_text())
    out, _ = normalize(log, start_convention=convention)
    nap = next(s for s in out.sessions if s.put_down_at and s.put_down_at.value.hour == 9)
    assert nap.start.value.minute == 35        # 09:30 put-down + 5-min SOL -> 09:35 asleep
    assert nap.duration_minutes == 30          # real sleep, trimmed from logged 35
    assert nap.onset_latency_minutes == 5      # SOL retained
