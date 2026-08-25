from baby_sleep.contract.enums import Location, SleepType
from baby_sleep.ingest.csv_generic import GenericCsvAdapter

CSV = """start,end,where
2026-08-24 13:00,2026-08-24 14:20,daycare
2026-08-24 19:30,2026-08-25 06:30,home
"""


def test_generic_csv_maps_columns_and_location():
    adapter = GenericCsvAdapter(column_map={"start": "start", "end": "end", "location": "where"})
    log = adapter.parse(CSV)
    assert len(log.sessions) == 2
    assert log.sessions[0].location is Location.DAYCARE
    assert log.sessions[1].location is Location.HOME
    assert log.sessions[0].start.value.hour == 13
    # types are UNKNOWN until normalize() runs
    assert log.sessions[0].sleep_type is SleepType.UNKNOWN
    assert log.source == "generic_csv"


def test_generic_csv_skips_unparseable_rows():
    bad = "start,end\nnot-a-date,also-bad\n2026-08-24 13:00,2026-08-24 14:20\n"
    adapter = GenericCsvAdapter(column_map={"start": "start", "end": "end"})
    log = adapter.parse(bad)
    assert len(log.sessions) == 1
