from pathlib import Path
from baby_sleep.ingest.huckleberry import HuckleberryCsvAdapter
from baby_sleep.ingest.normalize import normalize
from baby_sleep.contract.enums import EventKind, SleepType, StartMarker

FIXTURE = Path(__file__).parent.parent / "fixtures" / "huckleberry_sample.csv"


def test_huckleberry_parses_sleep_and_events():
    log = HuckleberryCsvAdapter().parse(FIXTURE.read_text())
    assert len(log.sessions) == 6          # all Sleep rows (impossible one dropped later)
    kinds = sorted({e.kind for e in log.events}, key=lambda k: k.value)
    assert kinds == [EventKind.DIAPER, EventKind.FEED, EventKind.MEDICATION, EventKind.PUMP]
    assert log.source == "huckleberry_csv"


def test_huckleberry_maps_onset_latency_midpoint():
    log = HuckleberryCsvAdapter().parse(FIXTURE.read_text())
    night = next(s for s in log.sessions if s.start.value.hour == 19)
    assert night.onset_latency_minutes == 15   # "10-20_minutes" -> midpoint
    assert night.self_settled is True          # "On own in bed"


def test_huckleberry_feed_amount_and_med_label():
    log = HuckleberryCsvAdapter().parse(FIXTURE.read_text())
    feed = next(e for e in log.events if e.kind is EventKind.FEED and e.amount_ml == 110)
    assert feed.label == "formula"
    med = next(e for e in log.events if e.kind is EventKind.MEDICATION)
    assert med.label == "acetaminophen"       # normalized from "Infant tylenol"


def test_huckleberry_then_normalize_drops_impossible_and_types():
    raw = HuckleberryCsvAdapter().parse(FIXTURE.read_text())
    # adapter leaves start_marks UNKNOWN (it can't know the family's convention)
    assert all(s.start_marks is StartMarker.UNKNOWN for s in raw.sessions)
    out, warnings = normalize(raw)            # no convention => no shift
    assert len(out.sessions) == 5             # impossible 12:00->11:00 row dropped
    assert len(warnings) == 1
    nights = [s for s in out.sessions if s.sleep_type is SleepType.NIGHT]
    naps = [s for s in out.sessions if s.sleep_type is SleepType.NAP]
    assert len(nights) == 2 and len(naps) == 3
    assert out.sessions[0].duration_minutes == 624   # 10:24 preserved across midnight


def test_huckleberry_with_put_down_convention_shifts_by_sol():
    raw = HuckleberryCsvAdapter().parse(FIXTURE.read_text())
    out, _ = normalize(raw, start_convention=StartMarker.PUT_DOWN)
    # the 09:30 contact nap logged 35min with a 5-min onset -> asleep 09:35, real 30min
    nap = next(s for s in out.sessions if s.put_down_at and s.put_down_at.value.hour == 9)
    assert nap.start.value == nap.put_down_at.value.replace(minute=35)
    assert nap.duration_minutes == 30
    assert nap.start_marks is StartMarker.ASLEEP
