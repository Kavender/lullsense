import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANALYZE = REPO / "scripts" / "analyze_sleep.py"
FIXTURE = REPO / "evals" / "proactive" / "fixtures" / "early_waking.json"


def _run(*extra):
    return subprocess.run(
        [sys.executable, str(ANALYZE), "--format", "json", "--input", str(FIXTURE),
         "--age-months", "12", *extra],
        capture_output=True, text=True, check=False,
    )


def test_no_review_flag_omits_review_block():
    r = _run()
    assert r.returncode == 0, r.stderr
    assert "review" not in json.loads(r.stdout)


def test_review_flag_adds_review_block():
    r = _run("--review", "--as-of-date", "2026-09-20", "--review-window-days", "14")
    assert r.returncode == 0, r.stderr
    review = json.loads(r.stdout)["review"]
    assert review["status"] in {
        "computed", "stale_data", "insufficient_data",
        "below_supported_range", "age_unknown",
    }
    assert "coverage" in review and "steady_domains" in review


def test_review_stale_when_as_of_far_future():
    r = _run("--review", "--as-of-date", "2030-01-01")
    assert r.returncode == 0, r.stderr
    review = json.loads(r.stdout)["review"]
    assert review["status"] == "stale_data"
    assert review["surfaced"] == []
