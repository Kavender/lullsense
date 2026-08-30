import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANALYZE = REPO / "scripts" / "analyze_sleep.py"
RICH = REPO / "evals" / "proactive" / "fixtures" / "early_waking.json"
THIN = REPO / "tests" / "predict" / "fixtures" / "one_day.json"


def _run(fixture, *extra):
    return subprocess.run(
        [sys.executable, str(ANALYZE), "--format", "json", "--input", str(fixture),
         "--age-months", "9", "--predict", "--last-wake", "10:00", *extra],
        capture_output=True, text=True, check=False,
    )


def test_predict_flag_adds_prediction_block():
    r = _run(RICH)
    assert r.returncode == 0, r.stderr
    pred = json.loads(r.stdout)["prediction"]
    assert pred["status"] == "computed"
    assert pred["next_event"]["window_low"] < pred["next_event"]["window_high"]
    assert pred["next_event"]["confidence"] in {"low", "moderate"}


def test_no_predict_flag_omits_prediction_block():
    r = subprocess.run(
        [sys.executable, str(ANALYZE), "--format", "json", "--input", str(RICH),
         "--age-months", "9"],
        capture_output=True, text=True, check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "prediction" not in json.loads(r.stdout)


def test_predict_thin_log_is_age_only():
    r = _run(THIN)
    assert r.returncode == 0, r.stderr
    pred = json.loads(r.stdout)["prediction"]
    assert pred["next_event"]["basis"] == "age_only"


def test_predict_under_4mo_guardrail():
    r = subprocess.run(
        [sys.executable, str(ANALYZE), "--format", "json", "--input", str(THIN),
         "--age-months", "2", "--predict", "--last-wake", "10:00"],
        capture_output=True, text=True, check=False,
    )
    assert r.returncode == 0, r.stderr
    pred = json.loads(r.stdout)["prediction"]
    assert pred["status"] == "newborn_guardrail"
    assert pred["next_event"] is None


def test_predict_requires_last_wake():
    r = subprocess.run(
        [sys.executable, str(ANALYZE), "--format", "json", "--input", str(RICH),
         "--age-months", "9", "--predict"],
        capture_output=True, text=True, check=False,
    )
    assert r.returncode != 0
    assert "last-wake" in r.stderr
