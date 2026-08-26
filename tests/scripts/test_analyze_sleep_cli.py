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


def _run_experiment(state, *args):
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "experiment.py"),
         "--state-dir", str(state), *args],
        capture_output=True, text=True, check=False,
    )


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


def test_manual_text_parses_with_reference_date(tmp_path):
    txt = tmp_path / "manual.txt"
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
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["days"] >= 1


def test_dob_flag_derives_age(tmp_path):
    # dob 2025-08-26, as_of 2026-08-26 => exactly 12 months
    r = _run([
        "--format", "huckleberry",
        "--input", str(FIXTURE),
        "--dob", "2025-08-26",
        "--as-of-date", "2026-08-26",
    ])
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["child"]["age_months"] == 12


def test_profile_fallback_derives_age(tmp_path):
    # save profile with dob=2025-02-26 into state-dir; as_of=2026-08-26 => 18 months
    _run_experiment(tmp_path, "save-profile", "--dob", "2025-02-26")
    r = _run([
        "--format", "huckleberry",
        "--input", str(FIXTURE),
        "--state-dir", str(tmp_path),
        "--as-of-date", "2026-08-26",
    ])
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["child"]["age_months"] == 18


def test_no_age_source_exits_nonzero_cleanly(tmp_path):
    # no --age-months, no --dob, no --state-dir with profile => error
    r = _run([
        "--format", "huckleberry",
        "--input", str(FIXTURE),
    ])
    assert r.returncode != 0
    assert "Traceback" not in r.stderr
    combined = r.stdout + r.stderr
    assert any(word in combined.lower() for word in ("age", "dob"))


def test_manual_text_without_reference_date_exits_nonzero(tmp_path):
    txt = tmp_path / "manual.txt"
    txt.write_text("Nap 1:15pm-2:35pm\nbedtime around 7pm\n")
    r = _run(
        [
            "--format",
            "manual",
            "--input",
            str(txt),
            "--age-months",
            "12",
        ]
    )
    assert r.returncode != 0
    combined = r.stdout + r.stderr
    assert "reference-date" in combined
