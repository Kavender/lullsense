"""Wire request -> canonical SleepLog (lullsense-app spec §5.2) and the post-fix night
split (§5.3)."""
from __future__ import annotations

from baby_sleep.contract.enums import DataQuality, SleepType, StartMarker
from baby_sleep.contract.models import Child, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime, TimePrecision
from baby_sleep.ingest.normalize import Fix, _before, _elapsed_minutes, _instant, normalize

from .wire import AnalysisRequest, Record, Waking

_KIND = {"nap": SleepType.NAP, "night_sleep": SleepType.NIGHT}
_PRECISION = {"exact": TimePrecision.EXACT, "approx": TimePrecision.APPROXIMATE}


def _resolved(w: Waking) -> bool:
    """Only a resolved waking may split; an unresolved one's backAsleepAt is a guess."""
    return w.backAsleepAt is not None and not w.unresolved


def _session(r: Record) -> SleepSession:
    approx = "approx" in (r.startPrecision, r.endPrecision)
    night = r.kind == "night_sleep"
    return SleepSession(
        start=ApproxTime(value=r.start, precision=_PRECISION[r.startPrecision]),
        end=ApproxTime(value=r.end, precision=_PRECISION[r.endPrecision]),
        sleep_type=_KIND[r.kind],
        start_marks=StartMarker.ASLEEP,
        data_quality=DataQuality.REPORTED if approx else DataQuality.LOGGED,
        night_wakings=0 if night else None,       # wakings are counted post-fix by _split
        record_id=r.id,
        tz=r.tz,
    )


def to_sleep_log(req: AnalysisRequest) -> SleepLog:
    """One whole session per record; resolved wakings are applied later by the split."""
    return SleepLog(
        child=Child(age_months=req.child.ageMonths),
        sessions=[_session(r) for r in req.records],
    )


def _split(s: SleepSession, wakings: list[Waking]) -> list[SleepSession]:
    """Apply wakings to a post-fix night [start, end] (real time).

    Resolved: wholly outside the span -> dropped; strictly inside the current segment ->
    cut (the gap is the waking); straddling an edge -> counted and the span is clipped so
    awake time is not asleep (start moves to backAsleepAt / end moves to wokeAt); a clip
    that would leave nothing (the waking covers the rest of the span) ends the record
    there, so a wholly-awake record emits no segment; any other (overlapping) -> counted,
    uncut. Unresolved/open: counted iff start <= wokeAt <= end. Every segment carries the
    record's post-fix start as ``record_start`` (its wake-day anchor).
    """
    start, end = s.start.value, s.end.value
    count = sum(not _resolved(w) and not _before(w.wokeAt, start)
                and not _before(end, w.wokeAt) for w in wakings)
    seg_start, seg_end, segs, tail = s.start, s.end, [], True
    for w in sorted((w for w in wakings if _resolved(w)), key=lambda w: _instant(w.wokeAt)):
        woke, back = w.wokeAt, w.backAsleepAt
        if not _before(woke, end) or not _before(start, back):
            continue                                       # wholly outside: dropped
        if not _before(start, woke):                       # straddles start
            count += 1
            if not _before(back, seg_end.value):
                tail = False                               # covers the rest: awake
                break                                      # record ends here
            if _before(seg_start.value, back):
                seg_start = ApproxTime(value=back)
        elif not _before(back, end):                       # straddles end
            count += 1
            if not _before(seg_start.value, woke):
                tail = False                               # covers the rest: awake
                break                                      # record ends here
            if _before(woke, seg_end.value):
                seg_end = ApproxTime(value=woke)
        elif (_before(seg_start.value, woke) and _before(woke, back)
              and _before(back, seg_end.value)):
            segs.append((seg_start, ApproxTime(value=woke)))   # inside: cut, gap counts
            seg_start = ApproxTime(value=back)
        else:
            count += 1                                     # overlapping: counted, uncut
    if tail:
        segs.append((seg_start, seg_end))
    elif segs:
        count += 1      # the last cut's gap lost its following segment: count it explicitly
    return [s.model_copy(update={
        "start": a, "end": b,
        "duration_minutes": _elapsed_minutes(a.value, b.value),
        "night_wakings": count if k == 0 else 0,
        "record_start": start,
    }) for k, (a, b) in enumerate(segs)]


def _awake_minutes(r: Record) -> int:
    """Resolved waking minutes inside the record's span (unresolved contribute 0)."""
    total = 0
    for w in r.wakings:
        if _resolved(w):
            a = max(w.wokeAt, r.start, key=_instant)
            b = min(w.backAsleepAt, r.end, key=_instant)
            total += max(0, _elapsed_minutes(a, b))
    return total


def build_log(req: AnalysisRequest) -> tuple[SleepLog, list[str], list[Fix]]:
    """Map, normalize (fixes on WHOLE records), then split nights at resolved wakings."""
    fixes: list[Fix] = []
    log, warnings = normalize(to_sleep_log(req), start_convention=StartMarker.ASLEEP,
                              fixes=fixes,
                              awake_minutes={r.id: _awake_minutes(r) for r in req.records})
    wakings = {r.id: r.wakings for r in req.records}
    sessions = []
    for s in log.sessions:
        if s.sleep_type is SleepType.NIGHT and wakings.get(s.record_id):
            sessions.extend(_split(s, wakings[s.record_id]))
        else:
            sessions.append(s)
    return log.model_copy(update={"sessions": sessions}), warnings, fixes
