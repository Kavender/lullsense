"""CAM-12 P3: structured fixes[] (P-fix) and the 28-day golden review response (P-golden).
lullsense-app spec §3.4, §5.4.1, §5.5, §9."""
import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path

from baby_sleep.contract.enums import SleepType
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.ingest.normalize import normalize
from baby_sleep.service import run

from .test_mapping import NY, _at, _nights, _rec, _req, _wk

GOLDEN = Path(__file__).parent.parent / "fixtures" / "service"


def _fixes(records, **kw):
    out = run(_req(records, **kw))
    assert "error" not in out, out
    return out["fixes"]


def _offset_hours(iso: str) -> float:
    return datetime.fromisoformat(iso).utcoffset().total_seconds() / 3600


# --- P-fix: one test per §3.4 row -----------------------------------------------------

def test_fix_implausible_duration_drop():
    d = date(2026, 10, 6)
    nap = _rec("long", "nap", _at(d, 8, 0), _at(d + timedelta(1), 5, 0))     # 21 h
    assert _fixes([*_nights(7), nap]) == [{
        "recordId": "long", "action": "drop", "reason": "implausible_duration",
        "original": {"start": "2026-10-06T08:00:00+08:00", "end": "2026-10-07T05:00:00+08:00"},
        "derived": None, "overlapsRecordId": None}]


def test_fix_forgot_to_stop_truncate_end_carries_the_records_own_offset():
    # §5.5 example 1: New York fall-back night; three clean 06:00 wakes.
    clean = _nights(3, last=date(2026, 10, 31), tz=NY, end=(6, 0))
    bad = _rec("fb", "night_sleep", "2026-10-31T19:00:00-04:00", "2026-11-01T11:30:00-05:00",
               tz=NY)
    (fix,) = _fixes([*clean, bad], as_of="2026-11-01T20:00:00-05:00")
    assert fix == {
        "recordId": "fb", "action": "truncate_end", "reason": "forgot_to_stop",
        "original": {"start": "2026-10-31T19:00:00-04:00", "end": "2026-11-01T11:30:00-05:00"},
        "derived": {"start": "2026-10-31T19:00:00-04:00", "end": "2026-11-01T06:00:00-05:00"},
        "overlapsRecordId": None}
    assert _offset_hours(fix["derived"]["end"]) == -5          # not the start's -04:00


def test_fix_forgot_to_stop_no_history_drop():
    d = date(2026, 10, 7)
    bad = _rec("bad", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 11, 0))
    assert _fixes([*_nights(1, last=d - timedelta(1)), bad]) == [{
        "recordId": "bad", "action": "drop", "reason": "forgot_to_stop_no_history",
        "original": {"start": "2026-10-06T19:30:00+08:00", "end": "2026-10-07T11:00:00+08:00"},
        "derived": None, "overlapsRecordId": None}]


def test_fix_overlap_contained_drop_names_the_earlier_record():
    d = date(2026, 10, 6)
    outer = _rec("outer", "nap", _at(d, 13, 0), _at(d, 15, 0))
    inner = _rec("inner", "nap", _at(d, 13, 30), _at(d, 14, 0))
    assert _fixes([inner, outer]) == [{
        "recordId": "inner", "action": "drop", "reason": "overlap_contained",
        "original": {"start": "2026-10-06T13:30:00+08:00", "end": "2026-10-06T14:00:00+08:00"},
        "derived": None, "overlapsRecordId": "outer"}]


def test_fix_overlap_partial_trim_start_in_the_trimmed_records_zone():
    # §5.5 example 2: the earlier record ends 04:00Z; the NY nap's derived start is NY local.
    earlier = _rec("e", "night_sleep", "2026-09-30T20:00:00+00:00", "2026-10-01T04:00:00+00:00",
                   tz="UTC")
    nap = _rec("p", "nap", "2026-09-30T23:00:00-04:00", "2026-10-01T01:00:00-04:00", tz=NY)
    (fix,) = _fixes([earlier, nap], as_of="2026-10-01T20:00:00-04:00")
    assert fix == {
        "recordId": "p", "action": "trim_start", "reason": "overlap_partial",
        "original": {"start": "2026-09-30T23:00:00-04:00", "end": "2026-10-01T01:00:00-04:00"},
        "derived": {"start": "2026-10-01T00:00:00-04:00", "end": "2026-10-01T01:00:00-04:00"},
        "overlapsRecordId": "e"}
    assert _offset_hours(fix["derived"]["start"]) == -4        # not the earlier record's +00:00


def test_two_fixes_on_one_record_in_pipeline_order_original_as_sent():
    # truncated (forgot-to-stop), then trimmed (an evening nap overlaps its start)
    d = date(2026, 10, 7)
    eve = d - timedelta(1)
    nap = _rec("nap", "nap", _at(eve, 18, 0), _at(eve, 20, 0))
    bad = _rec("bad", "night_sleep", _at(eve, 19, 30), _at(d, 11, 30))
    sent = {"start": "2026-10-06T19:30:00+08:00", "end": "2026-10-07T11:30:00+08:00"}
    fixes = _fixes([*_nights(3, last=eve), nap, bad])
    assert [(f["recordId"], f["action"]) for f in fixes] == [
        ("bad", "truncate_end"), ("bad", "trim_start")]
    assert fixes[0]["original"] == fixes[1]["original"] == sent
    assert fixes[0]["derived"] == {"start": sent["start"], "end": "2026-10-07T06:30:00+08:00"}
    assert fixes[1]["derived"] == {"start": "2026-10-06T20:00:00+08:00",
                                   "end": "2026-10-07T06:30:00+08:00"}
    assert fixes[1]["overlapsRecordId"] == "nap"


def test_forgot_to_stop_with_resolved_wakings_is_still_fixed():
    # fixes run on the WHOLE record, before the split hides the long last segment
    d = date(2026, 10, 7)
    bad = _rec("bad", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 11, 30),
               wakings=[_wk(_at(d, 2, 0), _at(d, 2, 30)), _wk(_at(d, 5, 0), _at(d, 5, 10))])
    (fix,) = _fixes([*_nights(3, last=d - timedelta(1)), bad])
    assert (fix["recordId"], fix["action"]) == ("bad", "truncate_end")
    assert fix["derived"]["end"] == "2026-10-07T06:30:00+08:00"


def test_clean_request_has_no_fixes():
    assert _fixes(_nights(7)) == []


def _messy_log() -> SleepLog:
    def s(a, b, kind=SleepType.NIGHT, rid=None):
        return SleepSession(start=ApproxTime(value=datetime.fromisoformat(a)),
                            end=ApproxTime(value=datetime.fromisoformat(b)),
                            sleep_type=kind, record_id=rid)
    return SleepLog(sessions=[
        s("2026-08-20T19:00+08:00", "2026-08-21T06:00+08:00", rid="a"),
        s("2026-08-21T19:00+08:00", "2026-08-22T06:15+08:00", rid="b"),
        s("2026-08-22T19:00+08:00", "2026-08-23T06:30+08:00", rid="c"),
        s("2026-08-23T19:00+08:00", "2026-08-24T09:10+08:00", rid="d"),     # forgot-to-stop
        s("2026-08-24T13:00+08:00", "2026-08-25T10:00+08:00", SleepType.NAP),  # 21 h
        s("2026-08-22T20:00+08:00", "2026-08-22T21:00+08:00", SleepType.NAP),  # contained
    ])


def test_normalize_output_unchanged_by_the_collector():
    fixes = []
    with_c = normalize(_messy_log(), fixes=fixes)
    assert normalize(_messy_log()) == with_c
    assert [(f.recordId, f.action, f.reason) for f in fixes] == [
        (None, "drop", "implausible_duration"),
        ("d", "truncate_end", "forgot_to_stop"),
        (None, "drop", "overlap_contained"),
    ]
    assert fixes[2].overlapsRecordId == "c"


# --- P-golden -------------------------------------------------------------------------

def _golden_request() -> dict:
    """28 Asia/Shanghai wake-days ending 2026-10-07: varied nights with resolved and
    unresolved wakings, one or two naps a day, an early-waking last 5 days, plus a forgot-to-stop night, a contained
    double-log, a partial overlap and a 21-hour row."""
    recs = []
    last = date(2026, 10, 7)
    for k in range(28):
        wd = last - timedelta(days=27 - k)
        eve = wd - timedelta(days=1)
        start_m, wake_m = 19 * 60 + 15 + (k * 7) % 40, 6 * 60 + 10 + (k * 11) % 45
        if k >= 23:                                                        # early-waking drift
            wake_m -= 70
        wakings = [_wk(_at(wd, 1, 10 + k % 20), _at(wd, 1, 35 + k % 20))] if k % 3 else []
        if k % 5 == 0:
            wakings.append(_wk(_at(wd, 4, 0), _at(wd, 4, 5), unresolved=True))
        end = (11, 40) if k == 20 else divmod(wake_m, 60)                  # forgot-to-stop
        recs.append(_rec(f"n{k:02d}", "night_sleep", _at(eve, *divmod(start_m, 60)),
                         _at(wd, *end), wakings=wakings, sp="approx" if k % 7 == 0 else "exact"))
        recs.append(_rec(f"a{k:02d}", "nap", _at(eve, 9, 30 + k % 15), _at(eve, 10, 40)))
        if k % 2:
            recs.append(_rec(f"b{k:02d}", "nap", _at(eve, 13, 30), _at(eve, 14, 45 + k % 10)))
    d = last - timedelta(days=10)
    recs += [
        _rec("dup", "nap", _at(d, 9, 50), _at(d, 10, 20)),                 # contained
        _rec("late", "nap", _at(d, 10, 30), _at(d, 11, 10)),               # partial overlap
        _rec("long", "nap", _at(d, 15, 0), _at(d + timedelta(1), 12, 0)),  # 21 h
    ]
    return _req(recs, age=10, as_of="2026-10-07T21:30:00+08:00")


def test_golden_28_day_review_response():
    out = run(_golden_request())
    assert out["status"] == "computed" and len(out["fixes"]) == 4 and out["signals"]
    out["serviceVersion"] = "<version>"          # P-version pins it separately
    path = GOLDEN / "golden_28d_review.json"
    if os.environ.get("UPDATE_GOLDEN"):
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    assert out == json.loads(path.read_text())
