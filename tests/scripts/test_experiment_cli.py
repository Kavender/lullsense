import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _run(state, *args):
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "experiment.py"),
         "--state-dir", str(state), *args],
        capture_output=True, text=True, check=False,
    )


def test_constraint_roundtrip_and_convention(tmp_path):
    r = _run(tmp_path, "save-constraint", "--key", "sleep_start_convention", "--value", "put_down")
    assert r.returncode == 0
    got = json.loads(_run(tmp_path, "get-constraint", "--key", "sleep_start_convention").stdout)
    assert got["value"] == "put_down"


def test_experiment_save_list_update(tmp_path):
    _run(tmp_path, "save-experiment", "--id", "e1", "--hypothesis", "bedtime too late",
         "--change", "bedtime 30m earlier", "--metrics", "sol,night_wakings",
         "--start-date", "2026-08-25", "--review-after-days", "7")
    lst = json.loads(_run(tmp_path, "list-experiments").stdout)
    assert lst[0]["id"] == "e1" and lst[0]["status"] == "proposed"
    r_upd = _run(tmp_path, "update-status", "--id", "e1", "--status", "active")
    assert r_upd.returncode == 0
    lst2 = json.loads(_run(tmp_path, "list-experiments").stdout)
    assert lst2[0]["status"] == "active"


def test_update_status_unknown_id_errors_cleanly(tmp_path):
    r = _run(tmp_path, "update-status", "--id", "nope", "--status", "active")
    assert r.returncode == 1
    assert r.stdout == ""
    assert "not found" in r.stderr
    assert "Traceback" not in r.stderr


def test_save_experiment_bad_date_errors_cleanly(tmp_path):
    r = _run(tmp_path, "save-experiment", "--id", "e1", "--hypothesis", "h",
             "--change", "c", "--metrics", "sol",
             "--start-date", "not-a-date", "--review-after-days", "7")
    assert r.returncode == 1
    assert "invalid --start-date" in r.stderr
    assert "Traceback" not in r.stderr


def test_save_profile_roundtrip(tmp_path):
    r = _run(tmp_path, "save-profile", "--dob", "2025-02-26", "--name", "Ada")
    assert r.returncode == 0, r.stderr
    got = json.loads(_run(tmp_path, "get-profile").stdout)
    assert got["name"] == "Ada"
    assert got["dob"] == "2025-02-26"


def test_get_profile_empty_dir_returns_null(tmp_path):
    r = _run(tmp_path, "get-profile")
    assert r.returncode == 0
    assert json.loads(r.stdout) is None


def test_save_profile_bad_dob_errors_cleanly(tmp_path):
    r = _run(tmp_path, "save-profile", "--dob", "not-a-date")
    assert r.returncode == 1
    assert "invalid" in r.stderr.lower()
    assert "Traceback" not in r.stderr


# --- dob_precision CLI tests (Task 6c) ---

def test_cli_save_approximate_dob(tmp_path):
    r = _run(tmp_path, "save-profile", "--dob", "2025-02-26", "--dob-precision", "approximate")
    assert r.returncode == 0, r.stderr
    got = json.loads(_run(tmp_path, "get-profile").stdout)
    assert got["dob"] == "2025-02-26"
    assert got["dob_precision"] == "approximate"


def test_cli_exact_replaces_approximate(tmp_path):
    _run(tmp_path, "save-profile", "--dob", "2025-02-26", "--dob-precision", "approximate")
    _run(tmp_path, "save-profile", "--dob", "2025-03-01")  # default exact
    got = json.loads(_run(tmp_path, "get-profile").stdout)
    assert got["dob"] == "2025-03-01"
    assert got["dob_precision"] == "exact"


def test_cli_exact_dob_not_clobbered_by_approximate(tmp_path):
    """End-to-end proof: approximate save after an exact one does NOT clobber the exact DOB."""
    # First set exact
    _run(tmp_path, "save-profile", "--dob", "2025-03-01")
    # Attempt to overwrite with approximate
    _run(tmp_path, "save-profile", "--dob", "2024-01-01", "--dob-precision", "approximate")
    got = json.loads(_run(tmp_path, "get-profile").stdout)
    assert got["dob"] == "2025-03-01", "approximate must NOT clobber exact DOB"
    assert got["dob_precision"] == "exact"


def test_cli_name_only_after_exact_preserves_dob_and_reflects_persisted_state(tmp_path):
    """save-profile --name only (no --dob) after an exact DOB:
    1. get-profile must still show the exact DOB + new name (persistence check).
    2. The save-profile command's OWN stdout must reflect persisted state —
       i.e. show the exact DOB, not dob: null (locks the bug fix).
    """
    # Step 1: store an exact DOB
    _run(tmp_path, "save-profile", "--dob", "2025-03-01")

    # Step 2: update name only (no --dob supplied → dob=None, default precision=exact)
    r_name = _run(tmp_path, "save-profile", "--name", "Alex")
    assert r_name.returncode == 0, r_name.stderr

    # The save-profile stdout must reflect persisted state, not the incoming profile
    saved_response = json.loads(r_name.stdout)
    assert saved_response["dob"] == "2025-03-01", (
        "save-profile stdout must show the persisted exact DOB, not null"
    )
    assert saved_response["dob_precision"] == "exact", (
        "save-profile stdout must show dob_precision=exact from persisted state"
    )
    assert saved_response["name"] == "Alex", (
        "save-profile stdout must show the updated name"
    )

    # Step 3: get-profile must agree
    got = json.loads(_run(tmp_path, "get-profile").stdout)
    assert got["dob"] == "2025-03-01", "persisted DOB must be preserved after name-only save"
    assert got["dob_precision"] == "exact"
    assert got["name"] == "Alex"
