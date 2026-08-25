from baby_sleep.contract.enums import Location
from baby_sleep.ingest.json_generic import GenericJsonAdapter

JSON = """[
  {"begin": "2026-08-24 13:00", "finish": "2026-08-24 14:20", "place": "home"},
  {"begin": "2026-08-24 19:30", "finish": "2026-08-25 06:30", "place": "daycare"}
]"""


def test_generic_json_maps_fields():
    adapter = GenericJsonAdapter(field_map={"start": "begin", "end": "finish", "location": "place"})
    log = adapter.parse(JSON)
    assert len(log.sessions) == 2
    assert log.sessions[1].location is Location.DAYCARE
    assert log.source == "generic_json"


def test_generic_json_skips_bad_records():
    bad = '[{"begin": "nope"}, {"begin": "2026-08-24 13:00"}]'
    adapter = GenericJsonAdapter(field_map={"start": "begin"})
    log = adapter.parse(bad)
    assert len(log.sessions) == 1
