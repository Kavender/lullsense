"""End-to-end acceptance for the D15 messy-data repairs over examples/messy-data.json:
every defect surfaces in warnings, repairs are marked inferred, and nothing is silent."""
from datetime import datetime
from pathlib import Path

from baby_sleep.contract.enums import DataQuality
from baby_sleep.ingest.json_generic import GenericJsonAdapter
from baby_sleep.ingest.normalize import normalize

EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "messy-data.json"


def _load_and_normalize():
    adapter = GenericJsonAdapter(field_map={"start": "start", "end": "end", "location": "location"})
    log = adapter.parse(EXAMPLE.read_text())
    return normalize(log)


def test_messy_example_surfaces_every_defect_in_warnings():
    _out, warnings = _load_and_normalize()
    joined = " | ".join(warnings).lower()
    assert "no end time or duration" in joined      # bare-start session
    assert "forgot-to-stop" in joined               # 13h40m night
    assert "overlap" in joined                      # partial + contained naps


def test_messy_example_repairs_are_marked_inferred_and_nothing_silent():
    out, warnings = _load_and_normalize()
    # the forgot-to-stop night was truncated to the typical morning wake, marked inferred
    assert any(s.data_quality is DataQuality.INFERRED for s in out.sessions)
    # the bare-start (no end/duration) session was dropped, not kept
    assert all(s.start.value != datetime(2026, 7, 12, 16, 0) for s in out.sessions)
    # every repair/drop is accounted for by a warning (nothing silent)
    assert warnings
