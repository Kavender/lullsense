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


def test_runner_reports_malformed_case_as_fail(tmp_path):
    """A malformed YAML case file must produce a structured FAIL line, not a traceback."""
    cases_dir = tmp_path / "cases"
    cases_dir.mkdir()
    bad_yaml = cases_dir / "bad.yaml"
    bad_yaml.write_text(":\n  - [unclosed")

    r = subprocess.run(
        [
            sys.executable,
            str(REPO / "evals" / "proactive" / "run_proactive_eval.py"),
            "--cases-dir",
            str(cases_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert r.returncode != 0, "Runner should exit non-zero for a failing case"
    assert "FAIL" in r.stdout, f"Expected 'FAIL' in stdout, got: {r.stdout!r}"
    assert "Traceback" not in r.stderr, (
        f"Expected no traceback in stderr, got: {r.stderr!r}"
    )
