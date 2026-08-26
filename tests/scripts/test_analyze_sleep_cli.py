import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "fixtures" / "huckleberry_sample.csv"


def _run(args):
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "analyze_sleep.py"), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return r


def test_huckleberry_analysis_emits_json_with_baseline_and_signals():
    r = _run(["--format", "huckleberry", "--input", str(FIXTURE), "--age-months", "10"])
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert "baseline" in out and "signals" in out and "summary" in out
    assert out["child"]["age_months"] == 10


def test_newborn_is_age_gated_but_still_succeeds():
    r = _run(["--format", "huckleberry", "--input", str(FIXTURE), "--age-months", "3"])
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["baseline"]["status"] == "below_supported_range"
    assert out["signals"] == []


def test_manual_text_requires_reference_date():
    txt = REPO / "tests" / "fixtures" / "_manual_tmp.txt"
    txt.write_text("Nap 1:15pm-2:35pm\nbedtime around 7pm\n")
    r = _run(
        [
            "--format",
            "manual",
            "--input",
            str(txt),
            "--age-months",
            "12",
            "--reference-date",
            "2026-08-24",
        ]
    )
    txt.unlink()
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["days"] >= 1
