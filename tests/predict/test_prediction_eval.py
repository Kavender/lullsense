"""Deterministic guardrail/shape checks over the --predict CLI (not LLM-graded)."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANALYZE = REPO / "scripts" / "analyze_sleep.py"
RICH = REPO / "evals" / "proactive" / "fixtures" / "early_waking.json"


def _predict(age, last_wake="10:00"):
    r = subprocess.run(
        [sys.executable, str(ANALYZE), "--format", "json", "--input", str(RICH),
         "--age-months", str(age), "--predict", "--last-wake", last_wake],
        capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)["prediction"]


def test_never_high_confidence():
    for age in (4, 9, 12, 18, 24):
        assert _predict(age)["next_event"]["confidence"] in {"low", "moderate"}


def test_always_a_range_not_a_point():
    for age in (9, 18):
        ne = _predict(age)["next_event"]
        assert ne["window_low"] != ne["window_high"]


def test_caveats_always_flag_heuristic_and_cues():
    pred = _predict(12)
    joined = " ".join(pred["caveats"]).lower()
    assert "cue" in joined and "heuristic" in joined
