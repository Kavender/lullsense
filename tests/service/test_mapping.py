"""CAM-12 P2: app mapping (P-map), night split + day assignment (P-split), DST-aware
derived instants (P-dst, P-trim-tz). lullsense-app spec §5.2–§5.5."""
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

from baby_sleep.analyze.features import build_feature_series
from baby_sleep.contract.enums import DataQuality, SleepType
from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime, TimePrecision
from baby_sleep.ingest.normalize import normalize
from baby_sleep.service import run
from baby_sleep.service.build import build_log, to_sleep_log
from baby_sleep.service.wire import AnalysisRequest

SH = "Asia/Shanghai"
NY = "America/New_York"


def _at(d: date, h: int, m: int, tz: str = SH) -> str:
    """Local wall time in ``tz`` -> ISO with that zone's offset at that instant."""
    return datetime(d.year, d.month, d.day, h, m, tzinfo=ZoneInfo(tz)).isoformat()


def _rec(rid, kind, start, end, tz=SH, wakings=(), sp="exact", ep="exact"):
    return {"id": rid, "kind": kind, "tz": tz, "start": start, "end": end,
            "startPrecision": sp, "endPrecision": ep, "wakings": list(wakings)}


def _wk(woke, back=None, unresolved=False):
    return {"wokeAt": woke, "backAsleepAt": back, "unresolved": unresolved}


def _req(records, age=9, op="review", as_of="2026-10-07T21:30:00+08:00"):
    return {"schemaVersion": 1, "op": op, "asOf": as_of, "requestedWindowDays": None,
            "child": {"ageMonths": age}, "records": records}


def _nights(n, last=date(2026, 10, 7), tz=SH, end=(6, 30)):
    """``n`` clean consecutive 19:30 -> ``end`` nights, the last waking on ``last``."""
    out = []
    for k in range(n):
        wd = last - timedelta(days=n - 1 - k)
        out.append(_rec(f"n{wd}", "night_sleep", _at(wd - timedelta(days=1), 19, 30, tz),
                        _at(wd, *end, tz), tz=tz))
    return out


def _log(records, **kw):
    return build_log(AnalysisRequest.model_validate(_req(records, **kw)))[0]


def _day(series, d: date):
    return next(x for x in series.days if x.day == d)


# --- P-map ----------------------------------------------------------------------------

def test_kind_ids_tz_and_precision_mapping():
    d = date(2026, 10, 6)
    log = to_sleep_log(AnalysisRequest.model_validate(_req([
        _rec("night", "night_sleep", _at(d, 19, 30), _at(d + timedelta(1), 6, 0)),
        _rec("nap_a", "nap", _at(d, 13, 0), _at(d, 14, 0), sp="approx"),
        _rec("nap_b", "nap", _at(d, 9, 0), _at(d, 9, 45), tz=NY, ep="approx"),
    ])))
    night, a, b = log.sessions
    assert [s.sleep_type for s in log.sessions] == [SleepType.NIGHT, SleepType.NAP, SleepType.NAP]
    assert [s.record_id for s in log.sessions] == ["night", "nap_a", "nap_b"]
    assert [s.tz for s in log.sessions] == [SH, SH, NY]
    assert night.data_quality is DataQuality.LOGGED and night.night_wakings == 0
    assert a.start.precision is TimePrecision.APPROXIMATE and a.start.uncertainty_minutes == 0
    assert a.data_quality is b.data_quality is DataQuality.REPORTED
    assert b.end.precision is TimePrecision.APPROXIMATE and b.start.precision is TimePrecision.EXACT
    assert a.night_wakings is None                       # naps carry no waking count
    # the app's corrected age is authoritative: no gestational weeks are sent on
    assert log.child.age_months == 9 and log.child.gestational_age_at_birth_weeks is None


def test_age_unknown_and_below_supported_range():
    assert run(_req(_nights(10), age=None))["status"] == "age_unknown"
    out = run(_req(_nights(10), age=3))
    assert out["status"] == "below_supported_range" and out["signals"] == []


# --- P-split --------------------------------------------------------------------------

def test_split_at_resolved_wakings_counts_unresolved():
    d = date(2026, 10, 7)
    eve = d - timedelta(days=1)
    night = _rec("n", "night_sleep", _at(eve, 19, 30), _at(d, 6, 30), wakings=[
        _wk(_at(d, 2, 0), _at(d, 2, 20)),                       # resolved: 20 min
        _wk(_at(eve, 23, 0), _at(eve, 23, 45)),                 # resolved, out of order: 45
        _wk(_at(d, 4, 0), _at(d, 4, 10), unresolved=True),      # legacy guess: count only
    ])
    log = _log([night])
    segs = log.sessions
    assert len(segs) == 3 and {s.record_id for s in segs} == {"n"}
    assert [s.start.value.strftime("%H:%M") for s in segs] == ["19:30", "23:45", "02:20"]
    assert [s.night_wakings for s in segs] == [1, 0, 0]
    assert [s.duration_minutes for s in segs] == [210, 135, 250]
    assert sum(s.duration_minutes for s in segs) == 11 * 60 - 65   # asleep time
    f = _day(build_feature_series(log), d)
    assert f.night_waking_count == 3
    assert f.total_awake_overnight_min == 65


def test_open_waking_counted_single_segment():
    d = date(2026, 10, 7)
    night = _rec("n", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 6, 30),
                 wakings=[_wk(_at(d, 1, 0))])
    log = _log([night])
    assert len(log.sessions) == 1
    assert _day(build_feature_series(log), d).night_waking_count == 1


def test_resettle_after_cutover_stays_on_the_same_wake_day():
    # §5.4.2: a 04:30 resettle segment starts after the 03:00 cutover; it must not move
    # to the next wake-day.
    d = date(2026, 10, 7)
    night = _rec("n", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 6, 30),
                 wakings=[_wk(_at(d, 4, 0), _at(d, 4, 30))])
    series = build_feature_series(_log([night]))
    assert [x.day for x in series.days] == [d]
    f = series.days[0]
    assert f.night_waking_count == 1 and f.night_sleep_duration_min == 630
    assert f.rise_time.strftime("%H:%M") == "06:30"


def test_waking_after_repaired_end_is_dropped():
    # forgot-to-stop: 19:30 -> 11:30 (16 h), three clean 06:30 wakes -> repaired to 06:30.
    # The fix runs on the WHOLE record first, so it is still detected despite the waking;
    # the 08:00 waking lies wholly after the derived end, so it is dropped (not counted).
    d = date(2026, 10, 7)
    bad = _rec("bad", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 11, 30),
               wakings=[_wk(_at(d, 2, 0), _at(d, 2, 30)), _wk(_at(d, 8, 0), _at(d, 8, 30))])
    log = _log([*_nights(3, last=d - timedelta(1)), bad])
    segs = [s for s in log.sessions if s.record_id == "bad"]
    assert len(segs) == 2
    assert segs[-1].end.value.isoformat() == "2026-10-07T06:30:00+08:00"
    assert [s.night_wakings for s in segs] == [0, 0]
    f = _day(build_feature_series(log), d)
    assert f.night_waking_count == 1 and f.night_sleep_duration_min == 630


def test_waking_before_trimmed_start_is_dropped():
    # an 18:00 -> 20:00 nap trims the 19:30 night to start 20:00; a 19:35 -> 19:50 waking
    # now lies wholly before the span and is dropped.
    d = date(2026, 10, 7)
    eve = d - timedelta(1)
    nap = _rec("nap", "nap", _at(eve, 18, 0), _at(eve, 20, 0))
    night = _rec("n", "night_sleep", _at(eve, 19, 30), _at(d, 6, 30),
                 wakings=[_wk(_at(eve, 19, 35), _at(eve, 19, 50))])
    (seg,) = [s for s in _log([nap, night]).sessions if s.record_id == "n"]
    assert seg.start.value.strftime("%H:%M") == "20:00" and seg.night_wakings == 0
    assert seg.duration_minutes == 630


def test_waking_straddling_end_clips_last_segment():
    # woke 06:00, back 06:45, end 06:30: counted; the night ends at 06:00.
    d = date(2026, 10, 7)
    night = _rec("n", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 6, 30),
                 wakings=[_wk(_at(d, 2, 0), _at(d, 2, 30)), _wk(_at(d, 6, 0), _at(d, 6, 45))])
    segs = _log([night]).sessions
    assert [s.end.value.strftime("%H:%M") for s in segs] == ["02:00", "06:00"]
    assert [s.night_wakings for s in segs] == [1, 0]
    assert sum(s.duration_minutes for s in segs) == 11 * 60 - 30 - 30
    f = _day(build_feature_series(_log([night])), d)
    assert f.night_waking_count == 2


def test_unresolved_waking_outside_span_is_dropped():
    d = date(2026, 10, 7)
    bad = _rec("bad", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 11, 30),
               wakings=[_wk(_at(d, 3, 0)), _wk(_at(d, 8, 0)),
                        _wk(_at(d, 9, 0), _at(d, 9, 10), unresolved=True)])
    log = _log([*_nights(3, last=d - timedelta(1)), bad])
    (seg,) = [s for s in log.sessions if s.record_id == "bad"]
    assert seg.end.value.strftime("%H:%M") == "06:30" and seg.night_wakings == 1


def test_outer_edge_approx_precision_survives_split():
    d = date(2026, 10, 7)
    night = _rec("n", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 6, 30),
                 wakings=[_wk(_at(d, 2, 0), _at(d, 2, 30))], sp="approx", ep="approx")
    first, last = _log([night]).sessions
    assert first.start.precision is last.end.precision is TimePrecision.APPROXIMATE
    assert first.end.precision is last.start.precision is TimePrecision.EXACT
    assert first.data_quality is last.data_quality is DataQuality.REPORTED


def test_six_nights_insufficient_seven_computed():
    assert run(_req(_nights(6)))["status"] == "insufficient_data"
    assert run(_req(_nights(7)))["status"] == "computed"


def test_sessions_analyzed_counts_segments():
    d = date(2026, 10, 7)
    night = _rec("n", "night_sleep", _at(d - timedelta(1), 19, 30), _at(d, 6, 30),
                 wakings=[_wk(_at(d, 2, 0), _at(d, 2, 20))])
    assert run(_req([night]))["used"]["sessionsAnalyzed"] == 2


# --- P-dst ----------------------------------------------------------------------------

def _ny_month():
    """28 America/New_York nights waking 2026-10-15 .. 2026-11-11, 19:00 -> 06:00 local,
    each with a resolved 01:30 -> 01:45 waking, except the fall-back night (wake-day
    2026-11-01), which is a forgot-to-stop 19:00 -> 11:30 with no waking."""
    recs = []
    for k in range(28):
        wd = date(2026, 10, 15) + timedelta(days=k)
        eve = wd - timedelta(days=1)
        if wd == date(2026, 11, 1):
            recs.append(_rec("fallback", "night_sleep", "2026-10-31T19:00:00-04:00",
                             "2026-11-01T11:30:00-05:00", tz=NY))
            continue
        recs.append(_rec(f"n{wd}", "night_sleep", _at(eve, 19, 0, NY), _at(wd, 6, 0, NY),
                         tz=NY, wakings=[_wk(_at(wd, 1, 30, NY), _at(wd, 1, 45, NY))]))
    return recs


def _real_minutes(a: datetime, b: datetime) -> int:
    return int((b.astimezone(UTC) - a.astimezone(UTC)).total_seconds() // 60)


def test_ny_month_segments_real_minutes_and_fall_back_repair():
    log = _log(_ny_month(), as_of="2026-11-11T20:00:00-05:00")
    for s in log.sessions:
        assert s.duration_minutes == _real_minutes(s.start.value, s.end.value)
    (rep,) = [s for s in log.sessions if s.record_id == "fallback"]
    assert rep.end.value.isoformat() == "2026-11-01T06:00:00-05:00"     # not 06:00-04:00
    assert rep.duration_minutes == 720
    f = _day(build_feature_series(log), date(2026, 11, 1))
    assert f.night_sleep_duration_min == 720
    assert f.rise_time.strftime("%H:%M") == "06:00"


def test_split_in_repeated_fall_back_hour_uses_real_time():
    # wokeAt 01:30 EDT (05:30Z), backAsleepAt 01:15 EST (06:15Z): 45 real minutes later
    # although the wall clock goes backwards.
    night = _rec("n", "night_sleep", "2026-10-31T19:00:00-04:00", "2026-11-01T06:00:00-05:00",
                 tz=NY, wakings=[_wk("2026-11-01T01:30:00-04:00", "2026-11-01T01:15:00-05:00")])
    segs = _log([night]).sessions
    assert [s.duration_minutes for s in segs] == [390, 285]
    f = build_feature_series(_log([night])).days[0]
    assert f.total_awake_overnight_min == 45 and f.night_waking_count == 1


def test_spring_forward_repair_in_the_gap_resolves_to_a_real_instant():
    # median clean wake 02:30 local; 2027-03-14 02:30 does not exist in New York.
    clean = [_rec(f"c{k}", "night_sleep", _at(date(2027, 3, 9 + k), 19, 0, NY),
                  _at(date(2027, 3, 10 + k), 2, 30, NY), tz=NY) for k in range(3)]
    bad = _rec("bad", "night_sleep", "2027-03-13T19:00:00-05:00", "2027-03-14T12:00:00-04:00",
               tz=NY)
    (rep,) = [s for s in _log([*clean, bad], as_of="2027-03-14T20:00:00-04:00").sessions
              if s.record_id == "bad"]
    assert rep.end.value.isoformat() == "2027-03-14T03:30:00-04:00"
    assert rep.duration_minutes == 450                                  # 00:00Z -> 07:30Z


# --- P-trim-tz ------------------------------------------------------------------------

def test_trimmed_start_takes_the_trimmed_records_offset():
    # §5.5 example 2: an earlier UTC-zone record ends 04:00Z; the NY nap is trimmed to
    # 2026-10-01T00:00-04:00, which is before the 03:00 cutover -> wake-day 2026-09-30.
    earlier = _rec("e", "night_sleep", "2026-09-30T20:00:00+00:00", "2026-10-01T04:00:00+00:00",
                   tz="UTC")
    nap = _rec("p", "nap", "2026-09-30T23:00:00-04:00", "2026-10-01T01:00:00-04:00", tz=NY)
    log = _log([earlier, nap], as_of="2026-10-01T20:00:00-04:00")
    (p,) = [s for s in log.sessions if s.record_id == "p"]
    assert p.start.value.isoformat() == "2026-10-01T00:00:00-04:00"
    assert p.duration_minutes == 60
    days = build_feature_series(log).days
    assert [x.day for x in days if x.nap_count] == [date(2026, 9, 30)]


def _fixed(iso: str) -> ApproxTime:
    return ApproxTime(value=datetime.fromisoformat(iso))


def test_trim_same_zone_fall_back_uses_offset_at_the_instant():
    # earlier ends 01:30 EST (06:30Z, -05:00); the later record was sent at -04:00.
    a = SleepSession(start=_fixed("2026-10-31T19:00:00-04:00"),
                     end=_fixed("2026-11-01T01:30:00-05:00"), sleep_type=SleepType.NIGHT, tz=NY)
    b = SleepSession(start=_fixed("2026-11-01T01:15:00-04:00"),
                     end=_fixed("2026-11-01T03:00:00-05:00"), sleep_type=SleepType.NAP, tz=NY)
    out, _ = normalize(SleepLog(sessions=[a, b]))
    tb = out.sessions[1]
    assert tb.start.value.isoformat() == "2026-11-01T01:30:00-05:00"
    assert tb.duration_minutes == 90
    # tz = None (adapters): the instant is kept but in the trimmed record's own offset
    out, _ = normalize(SleepLog(sessions=[a.model_copy(update={"tz": None}),
                                          b.model_copy(update={"tz": None})]))
    tb = out.sessions[1]
    assert tb.start.value.isoformat() == "2026-11-01T02:30:00-04:00"
    assert tb.duration_minutes == 90
