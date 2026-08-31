"""Global LullSense memory preference.

Memory is **opt-in by default**: unless the user has explicitly turned it off,
the skill may persist a child profile / constraints (see SKILL.md "State &
retention"). The first time it saves anything it tells the parent, who can opt
out. That opt-out is remembered here — a single non-PII flag at the state root
(``~/.lullsense/settings.json``), the *only* thing stored for an opted-out user.

    {"memory": "enabled" | "disabled"}

Absent file / unreadable / unset field → enabled (the default). Reading never
creates the file or directory.
"""
from __future__ import annotations

import json
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".lullsense"
SETTINGS_FILENAME = "settings.json"


def _settings_path(root: Path | str | None = None) -> Path:
    return Path(root) / SETTINGS_FILENAME if root is not None else DEFAULT_ROOT / SETTINGS_FILENAME


def memory_enabled(root: Path | str | None = None) -> bool:
    """True unless the user has explicitly disabled memory (opt-in by default).

    A missing or unreadable settings file means enabled, and reading it creates
    nothing on disk."""
    path = _settings_path(root)
    if not path.exists():
        return True
    try:
        data = json.loads(path.read_text(encoding="utf-8") or "{}")
    except json.JSONDecodeError:
        return True
    return data.get("memory", "enabled") != "disabled"


def set_memory(enabled: bool, root: Path | str | None = None) -> None:
    """Persist the memory preference. Writing the flag is the one thing we do
    for an opted-out user; it's a non-PII setting, not child data."""
    root_path = Path(root) if root is not None else DEFAULT_ROOT
    root_path.mkdir(parents=True, exist_ok=True)
    path = root_path / SETTINGS_FILENAME
    data: dict = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            data = {}
    data["memory"] = "enabled" if enabled else "disabled"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
