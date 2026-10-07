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
        night_wakings=sum(not _resolved(w) for w in r.wakings) if night else None,
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
    """Cut a post-fix night at each resolved waking strictly inside the current segment
    (``segStart < wokeAt < backAsleepAt < end`` in real time); others are counted."""
    seg_start, end = s.start, s.end
    uncut, segs = 0, []
    for w in sorted((w for w in wakings if _resolved(w)), key=lambda w: _instant(w.wokeAt)):
        woke, back = w.wokeAt, w.backAsleepAt
        if not (_before(seg_start.value, woke) and _before(woke, back)
                and _before(back, end.value)):
            uncut += 1
            continue
        segs.append((seg_start, ApproxTime(value=woke)))
        seg_start = ApproxTime(value=back)
    segs.append((seg_start, end))
    return [s.model_copy(update={
        "start": a, "end": b,
        "duration_minutes": _elapsed_minutes(a.value, b.value),
        "night_wakings": (s.night_wakings or 0) + uncut if k == 0 else 0,
    }) for k, (a, b) in enumerate(segs)]


def build_log(req: AnalysisRequest) -> tuple[SleepLog, list[str], list[Fix]]:
    """Map, normalize (fixes on WHOLE records), then split nights at resolved wakings."""
    fixes: list[Fix] = []
    log, warnings = normalize(to_sleep_log(req), start_convention=StartMarker.ASLEEP,
                              fixes=fixes)
    wakings = {r.id: r.wakings for r in req.records}
    sessions = []
    for s in log.sessions:
        if s.sleep_type is SleepType.NIGHT and wakings.get(s.record_id):
            sessions.extend(_split(s, wakings[s.record_id]))
        else:
            sessions.append(s)
    return log.model_copy(update={"sessions": sessions}), warnings, fixes
