"""Regression guards for the packaged heuristic table (P0.1 wheel fix).

The predictor must load its age-band table without depending on the source-repo
layout, or `pip install lullsense` + `--predict` breaks even though source tests
pass. These tests exercise the *default* load path (which no other test did) and
keep the packaged copy byte-identical to the skill-bundle source.
"""
from pathlib import Path

from baby_sleep.predict.heuristics import PACKAGED_TABLE, load_heuristics, lookup

# Skill-bundle canonical copy (also shipped via `npx skills add`).
_SKILL_SOURCE = (
    Path(__file__).resolve().parents[2]
    / "skills" / "lullsense" / "knowledge" / "sleep_timing_heuristics.yaml"
)


def test_default_load_uses_packaged_table():
    """load_heuristics() with no args must resolve the packaged copy and return
    the real table — this is the call site scripts/analyze_sleep.py uses and the
    exact path that fails from an installed wheel when data isn't packaged."""
    bands = load_heuristics()
    assert len(bands) >= 3
    # A representative infant band must be present and well-formed.
    band = lookup(bands, 9)
    assert band is not None
    assert band.wake_window_minutes.max > band.wake_window_minutes.min


def test_packaged_copy_matches_skill_source():
    """Drift guard: the packaged copy and the skill-bundle source are the same
    bytes. Edit the skill copy; this test enforces syncing the packaged one."""
    packaged = PACKAGED_TABLE.read_text(encoding="utf-8")
    source = _SKILL_SOURCE.read_text(encoding="utf-8")
    assert packaged == source, (
        "baby_sleep/predict/data/sleep_timing_heuristics.yaml has drifted from "
        "skills/lullsense/knowledge/sleep_timing_heuristics.yaml — re-copy it."
    )
