"""Thin CLI bridge: sleep input -> canonical analysis JSON (features, baseline, signals).
Wraps the baby_sleep package so SKILL.md can invoke analysis without inlining Python."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # make baby_sleep importable

from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.contract.enums import StartMarker
from baby_sleep.contract.models import Child
from baby_sleep.detect import DetectorInput, run_detectors
from baby_sleep.ingest.huckleberry import HuckleberryCsvAdapter
from baby_sleep.ingest.json_generic import GenericJsonAdapter
from baby_sleep.ingest.manual_text import parse_manual_text
from baby_sleep.ingest.normalize import normalize


def _load_log(fmt: str, text: str, reference_date: str | None):
    warnings = []
    if fmt == "huckleberry":
        return HuckleberryCsvAdapter().parse(text), warnings
    if fmt == "manual":
        if not reference_date:
            raise SystemExit("--reference-date is required for --format manual")
        log, w = parse_manual_text(text, date.fromisoformat(reference_date))
        return log, w
    if fmt == "json":
        return (
            GenericJsonAdapter(
                field_map={"start": "start", "end": "end", "location": "location"}
            ).parse(text),
            warnings,
        )
    raise SystemExit(f"unknown --format: {fmt}")


def _hhmm(minutes):
    if minutes is None:
        return None
    m = round(minutes)
    return f"{m // 60:02d}:{m % 60:02d}"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Analyze sleep input into features/baseline/signals JSON."
    )
    p.add_argument("--format", required=True, choices=["manual", "huckleberry", "json"])
    p.add_argument("--input", required=True)
    p.add_argument("--age-months", type=int, required=True)
    p.add_argument("--gestational-weeks", type=int, default=None)
    p.add_argument("--reference-date", default=None)
    p.add_argument("--convention", choices=["put_down", "asleep"], default=None)
    p.add_argument("--state-dir", default=None)
    args = p.parse_args(argv)

    text = Path(args.input).read_text()
    raw, parse_warnings = _load_log(args.format, text, args.reference_date)

    convention = None
    if args.convention:
        convention = StartMarker(args.convention)
    elif args.state_dir:
        from baby_sleep.store.experiment_store import ExperimentStore

        c = ExperimentStore(Path(args.state_dir)).get_constraint("sleep_start_convention")
        if c is not None:
            convention = StartMarker(c.value)

    log, norm_warnings = normalize(raw, start_convention=convention)
    child = Child(
        age_months=args.age_months,
        gestational_age_at_birth_weeks=args.gestational_weeks,
    )
    log = log.model_copy(update={"child": child})
    series = build_feature_series(log)
    baseline = build_baseline(series, child)
    signals = run_detectors(DetectorInput(series=series, baseline=baseline))

    recent = (
        series.days[-baseline.recent_window_days :]
        if baseline.recent_window_days
        else series.days
    )

    def _med(getter):
        vals = sorted(v for v in (getter(d) for d in recent) if v is not None)
        return vals[len(vals) // 2] if vals else None

    out = {
        "child": {
            "age_months": child.age_months,
            "corrected_age_months": child.corrected_age_months(),
            "gestational_age_at_birth_weeks": child.gestational_age_at_birth_weeks,
        },
        "days": len(series.days),
        "baseline": baseline.model_dump(mode="json"),
        "signals": [s.model_dump(mode="json") for s in signals],
        "warnings": parse_warnings + norm_warnings,
        "summary": {
            "rise_time": _hhmm(
                _med(
                    lambda d: d.rise_time.hour * 60 + d.rise_time.minute
                    if d.rise_time
                    else None
                )
            ),
            "sleep_onset_time": _hhmm(
                _med(
                    lambda d: d.sleep_onset_time.hour * 60 + d.sleep_onset_time.minute
                    if d.sleep_onset_time
                    else None
                )
            ),
            "night_sleep_duration_min": _med(lambda d: d.night_sleep_duration_min),
            "total_24h_sleep_min": _med(lambda d: d.total_24h_sleep_min),
            "nap_count": _med(lambda d: float(d.nap_count)),
        },
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
