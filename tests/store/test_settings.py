"""Global memory preference (opt-in by default; opt-out is remembered)."""
import json

from baby_sleep.store import settings


def test_memory_enabled_by_default(tmp_path):
    # No settings file → memory is on (opt-in by default), and reading creates nothing.
    root = tmp_path / "lullsense"
    assert settings.memory_enabled(root) is True
    assert not root.exists(), "reading the preference must not create the root dir"


def test_disable_then_enable_roundtrips(tmp_path):
    root = tmp_path / "lullsense"
    settings.set_memory(False, root)
    assert settings.memory_enabled(root) is False
    # The only thing written is the non-PII flag.
    data = json.loads((root / "settings.json").read_text())
    assert data == {"memory": "disabled"}

    settings.set_memory(True, root)
    assert settings.memory_enabled(root) is True


def test_corrupt_settings_defaults_to_enabled(tmp_path):
    root = tmp_path / "lullsense"
    root.mkdir()
    (root / "settings.json").write_text("{not valid json")
    assert settings.memory_enabled(root) is True


def test_set_memory_preserves_other_keys(tmp_path):
    root = tmp_path / "lullsense"
    root.mkdir()
    (root / "settings.json").write_text(json.dumps({"other": "keep", "memory": "enabled"}))
    settings.set_memory(False, root)
    data = json.loads((root / "settings.json").read_text())
    assert data["other"] == "keep"
    assert data["memory"] == "disabled"


# --- CLI ---

def test_cli_memory_status_default_enabled(tmp_path, capsys):
    from scripts.experiment import main
    rc = main(["memory-status", "--root", str(tmp_path / "ls")])
    assert rc == 0
    assert json.loads(capsys.readouterr().out) == {"memory": "enabled"}


def test_cli_disable_and_enable_memory(tmp_path, capsys):
    from scripts.experiment import main
    root = str(tmp_path / "ls")
    assert main(["disable-memory", "--root", root]) == 0
    assert json.loads(capsys.readouterr().out) == {"memory": "disabled"}
    # persisted across a fresh invocation
    assert main(["memory-status", "--root", root]) == 0
    assert json.loads(capsys.readouterr().out) == {"memory": "disabled"}
    assert main(["enable-memory", "--root", root]) == 0
    assert json.loads(capsys.readouterr().out) == {"memory": "enabled"}


def test_cli_store_command_requires_state_dir(capsys):
    from scripts.experiment import main
    rc = main(["get-profile"])  # no --state-dir
    assert rc == 1
    assert "state-dir" in json.loads(capsys.readouterr().err)["error"]
