"""One-shot session bootstrap: full session state (memory pref + every child) in one call.

Guards the latency optimization that replaces three serial session-start reads
(settings.json → profile.json → constraints.json) with a single bootstrap call.
"""
import json
import subprocess
import sys
from pathlib import Path

from baby_sleep.store import settings
from baby_sleep.store.bootstrap import bootstrap
from baby_sleep.store.experiment_store import ExperimentStore
from baby_sleep.store.models import ChildProfile, SavedConstraint

REPO = Path(__file__).resolve().parents[2]


def _seed_child(root: Path, slug: str, *, name: str, dob: str) -> Path:
    d = root / slug
    store = ExperimentStore(d)
    store.save_profile(ChildProfile(name=name, dob=dob))
    store.save_constraint(SavedConstraint(key="daycare_nap", value="12:30", note=None))
    return d


def test_empty_home_is_enabled_with_no_children(tmp_path):
    root = tmp_path / "lullsense"  # does not exist
    out = bootstrap(root=root)
    assert out == {"memory": "enabled", "children": []}
    assert not root.exists(), "bootstrap must not create the root dir just by reading"


def test_memory_disabled_returns_only_the_flag_and_never_scans(tmp_path):
    root = tmp_path / "lullsense"
    _seed_child(root, "ada", name="Ada", dob="2025-02-26")  # real child on disk
    settings.set_memory(False, root)
    out = bootstrap(root=root)
    assert out == {"memory": "disabled", "children": []}, (
        "opt-out must suppress the child scan, surfacing only the flag"
    )


def test_single_child_via_state_dir(tmp_path):
    root = tmp_path / "lullsense"
    d = _seed_child(root, "ada", name="Ada", dob="2025-02-26")
    out = bootstrap(state_dir=d)
    assert out["memory"] == "enabled"
    assert len(out["children"]) == 1
    child = out["children"][0]
    assert child["dir"] == str(d)
    assert child["profile"]["name"] == "Ada"
    assert child["profile"]["dob"] == "2025-02-26"
    assert child["constraints"][0]["key"] == "daycare_nap"


def test_state_dir_with_no_saved_state_is_null_profile_empty_constraints(tmp_path):
    d = tmp_path / "lullsense" / "newchild"  # never written
    out = bootstrap(state_dir=d)
    assert out["children"] == [{"dir": str(d), "profile": None, "constraints": []}]


def test_multi_child_scan_discovers_all_sorted(tmp_path):
    root = tmp_path / "lullsense"
    _seed_child(root, "sam", name="Sam", dob="2024-01-01")
    _seed_child(root, "ada", name="Ada", dob="2025-02-26")
    out = bootstrap(root=root)
    names = [c["profile"]["name"] for c in out["children"]]
    assert names == ["Ada", "Sam"], "children discovered and sorted by dir name"


def test_scan_skips_dirs_without_store_files(tmp_path):
    root = tmp_path / "lullsense"
    _seed_child(root, "ada", name="Ada", dob="2025-02-26")
    (root / "not-a-child").mkdir(parents=True)  # stray dir, no store files
    out = bootstrap(root=root)
    dirs = [Path(c["dir"]).name for c in out["children"]]
    assert dirs == ["ada"]


def test_corrupt_profile_degrades_to_warning_not_crash(tmp_path):
    root = tmp_path / "lullsense"
    d = _seed_child(root, "ada", name="Ada", dob="2025-02-26")
    (d / "profile.json").write_text("{ this is not valid json", encoding="utf-8")
    out = bootstrap(root=root)  # must not raise
    child = out["children"][0]
    assert child["profile"] is None
    assert "warning" in child and "profile.json" in child["warning"]
    # constraints for the same child still read fine
    assert child["constraints"][0]["key"] == "daycare_nap"


# --- CLI surface ---

def _run_cli(*args):
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "experiment.py"), *args],
        capture_output=True, text=True, check=False,
    )


def test_cli_bootstrap_single_call(tmp_path):
    root = tmp_path / "lullsense"
    _seed_child(root, "ada", name="Ada", dob="2025-02-26")
    r = _run_cli("bootstrap", "--root", str(root))
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["memory"] == "enabled"
    assert out["children"][0]["profile"]["name"] == "Ada"


def test_cli_bootstrap_state_dir(tmp_path):
    d = tmp_path / "lullsense" / "ada"
    ExperimentStore(d).save_profile(ChildProfile(name="Ada", dob="2025-02-26"))
    r = _run_cli("--state-dir", str(d), "bootstrap")
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert len(out["children"]) == 1
    assert out["children"][0]["profile"]["name"] == "Ada"
