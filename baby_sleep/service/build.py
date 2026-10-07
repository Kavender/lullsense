"""Wire request -> canonical SleepLog (lullsense-app spec §5.2)."""
from __future__ import annotations

from baby_sleep.contract.enums import DataQuality, SleepType, StartMarker
from baby_sleep.contract.models import Child, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime, TimePrecision

from .wire import AnalysisRequest, Record

_KIND = {"nap": SleepType.NAP, "night_sleep": SleepType.NIGHT}
_PRECISION = {"exact": TimePrecision.EXACT, "approx": TimePrecision.APPROXIMATE}


def _session(r: Record) -> SleepSession:
    approx = "approx" in (r.startPrecision, r.endPrecision)
    return SleepSession(
        start=ApproxTime(value=r.start, precision=_PRECISION[r.startPrecision]),
        end=ApproxTime(value=r.end, precision=_PRECISION[r.endPrecision]),
        sleep_type=_KIND[r.kind],
        start_marks=StartMarker.ASLEEP,
        data_quality=DataQuality.REPORTED if approx else DataQuality.LOGGED,
    )


def to_sleep_log(req: AnalysisRequest) -> SleepLog:
    # P2 (CAM-12): record_id/tz on the session, waking counts and the post-fix split.
    return SleepLog(
        child=Child(age_months=req.child.ageMonths),
        sessions=[_session(r) for r in req.records],
    )
