"""Stateless analysis service (CAM-12): one JSON request in, one JSON response out.

``run()`` is pure: no file writes, no store/state_dir, no network, no logging. Every
failure maps to a fixed error document that carries no input values."""
from __future__ import annotations

from importlib.metadata import version

from pydantic import ValidationError

from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.analyze.summary import summarize
from baby_sleep.detect import DetectorInput, run_detectors
from baby_sleep.review import build_review_summary

from .build import build_log
from .wire import SCHEMA_VERSION, AnalysisRequest

__all__ = ["SCHEMA_VERSION", "run"]

STALENESS_DAYS = 3


def _error(code: str, **extra) -> dict:
    return {"schemaVersion": SCHEMA_VERSION, "error": code, **extra}


def _loc(err: dict) -> str:
    loc = list(err["loc"])
    if err["type"] == "extra_forbidden":
        loc[-1] = "<extra>"                 # the unknown key's name is input
    return ".".join(str(p) for p in loc)


def _compute(req: AnalysisRequest) -> dict:
    log, warnings = build_log(req)
    series = build_feature_series(log)
    baseline = build_baseline(series, log.child)
    days = series.days
    out = {
        "schemaVersion": SCHEMA_VERSION,
        "serviceVersion": version("lullsense"),
        "status": baseline.status.value,
        "reason": baseline.reason,
        "used": {
            "recordsReceived": len(req.records),
            "sessionsAnalyzed": len(log.sessions),
            "days": len(days),
            "firstDay": days[0].day.isoformat() if days else None,
            "lastDay": days[-1].day.isoformat() if days else None,
        },
        "summary": summarize(series, baseline),
        "baseline": baseline.model_dump(mode="json"),
    }
    if req.op != "analyze":
        signals = run_detectors(DetectorInput(series=series, baseline=baseline))
        out["signals"] = [s.model_dump(mode="json") for s in signals]
    if req.op == "review":
        review = build_review_summary(
            signals, series, baseline, req.asOf.date(),
            requested_window_days=req.requestedWindowDays, staleness_days=STALENESS_DAYS)
        out["review"] = review.model_dump(mode="json")
        out["status"], out["reason"] = review.status.value, review.reason
    out["fixes"] = []                       # P3 (CAM-12): normalize() fix collector
    out["warnings"] = warnings
    return out


def run(request: object) -> dict:
    """Validate a decoded §3.1 request and compute the §3.2 response (or a §3.3 error)."""
    try:
        if isinstance(request, dict) and "schemaVersion" in request and not (
                type(request["schemaVersion"]) is int and request["schemaVersion"] == 1):
            return _error("unsupported_schema")
        try:
            req = AnalysisRequest.model_validate(request)
        except ValidationError as e:
            return _error("invalid_request",
                          fields=[_loc(err) for err in e.errors(include_input=False)])
        return _compute(req)
    except Exception as e:  # noqa: BLE001 — the class name is the only detail that may leave
        return _error("internal", type=type(e).__name__)
