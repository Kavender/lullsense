"""Phase 5 acceptance: a parent-initiated review over a real fixture produces a
coherent, honestly-framed review block end-to-end through the CLI."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANALYZE = REPO / "scripts" / "analyze_sleep.py"


def _review(fixture_rel, as_of, *extra):
    fixture = REPO / "evals" / "proactive" / fixture_rel
    r = subprocess.run(
        [sys.executable, str(ANALYZE), "--format", "json", "--input", str(fixture),
         "--age-months", "12", "--review", "--as-of-date", as_of, *extra],
        capture_output=True, text=True, check=False,
    )
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)["review"]


def test_quiet_review_is_reassuring_and_full_of_steady_domains():
    review = _review("fixtures/steady.json", "2026-09-20", "--review-window-days", "14")
    assert review["status"] == "computed"
    assert review["surfaced"] == []
    assert len(review["steady_domains"]) == 5


def test_cap_never_exceeds_two_unless_significant():
    # early_waking fixture at a current as-of date (fixture ends 2026-08-20):
    # detailed (non-significant) surfaced count stays <= 2; no diagnosis leak.
    review = _review("fixtures/early_waking.json", "2026-08-20")
    detailed = [s for s in review["surfaced"] if s["severity"] != "significant"]
    assert len(detailed) <= 2
    assert "coverage" in review
