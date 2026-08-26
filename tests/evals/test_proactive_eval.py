"""Deterministic proactive eval: proves the analysis pipeline surfaces the right
signals on synthetic fixtures WITHOUT being told the expected label."""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def test_proactive_eval_all_cases_pass():
    r = subprocess.run(
        [sys.executable, str(REPO / "evals" / "proactive" / "run_proactive_eval.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAIL" not in r.stdout
