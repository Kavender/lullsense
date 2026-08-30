"""Load the age-band sleep-timing heuristic table (single source of truth)."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

DEFAULT_TABLE = (
    Path(__file__).resolve().parents[2]
    / "skills" / "lullsense" / "knowledge" / "sleep_timing_heuristics.yaml"
)


class MinMax(BaseModel):
    min: float
    max: float


class AgeBand(BaseModel):
    age_band_months: list[int]         # [lo, hi] inclusive-exclusive
    wake_window_minutes: MinMax
    typical_nap_minutes: MinMax
    expected_nap_count: MinMax
    total_sleep_budget_hours: MinMax
    source_type: str
    clinical_anchors: list[str] = []
    notes: str = ""


def load_heuristics(path: Path | str = DEFAULT_TABLE) -> list[AgeBand]:
    rows = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    return [AgeBand(**row) for row in rows]


def lookup(bands: list[AgeBand], age_months: float) -> AgeBand | None:
    for b in bands:
        lo, hi = b.age_band_months
        if lo <= age_months < hi:
            return b
    return None
