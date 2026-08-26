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
