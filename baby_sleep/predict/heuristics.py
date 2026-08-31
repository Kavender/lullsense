"""Load the age-band sleep-timing heuristic table.

The canonical table is edited under ``skills/lullsense/knowledge/`` (alongside
``claims.yaml`` / ``sources.yaml``) because the skill bundle ships that copy for
the no-engine path. A byte-identical copy is packaged inside this module at
``data/sleep_timing_heuristics.yaml`` so prediction works from an installed
wheel with no dependency on the source-repo layout. A drift-guard test keeps the
two in sync (``tests/predict/test_packaged_heuristics.py``).
"""
from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import yaml
from pydantic import BaseModel

#: Packaged copy, resolved via importlib.resources so it works in a wheel.
PACKAGED_TABLE = files(__package__).joinpath("data", "sleep_timing_heuristics.yaml")


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


def load_heuristics(path: Path | str | None = None) -> list[AgeBand]:
    """Load the age-band table. Defaults to the packaged copy (wheel-safe);
    pass ``path`` to load an alternate table (used by tests with fixtures)."""
    text = (
        PACKAGED_TABLE.read_text(encoding="utf-8")
        if path is None
        else Path(path).read_text(encoding="utf-8")
    )
    rows = yaml.safe_load(text) or []
    return [AgeBand(**row) for row in rows]


def lookup(bands: list[AgeBand], age_months: float) -> AgeBand | None:
    for b in bands:
        lo, hi = b.age_band_months
        if lo <= age_months < hi:
            return b
    return None
