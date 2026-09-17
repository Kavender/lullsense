"""One-shot session bootstrap: full session state in a single read.

Session start needs three things — the global memory preference, the child profile, and the
saved durable constraints. Reading them as three serial calls (settings.json → profile.json
→ constraints.json) puts three blocking round-trips before the agent's first reply. This
collapses them into one: ``lullsense-experiment bootstrap`` returns everything at once.

Shape::

    {
      "memory": "enabled" | "disabled",
      "children": [
        {"dir": "...", "profile": {...}|null, "constraints": [...], "warning"?: "..."}
      ]
    }

Rules that keep it safe to call blind at session start:
- ``memory: disabled`` (the user opted out) returns ONLY the flag and an empty child list —
  no scan, nothing read from any child dir.
- With ``state_dir`` given, that one dir is the sole child (profile null / constraints []
  if it has no saved state yet). Without it, ``root`` (``~/.lullsense``) is scanned for
  child dirs, so a returning family is discovered without the agent knowing the slug.
- Missing files are nulls, never errors. A corrupt file degrades to a per-child ``warning``
  field instead of crashing the whole bootstrap — one unreadable child never blocks the rest.
"""
from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from baby_sleep.store.experiment_store import ExperimentStore
from baby_sleep.store.settings import DEFAULT_ROOT, SETTINGS_FILENAME, memory_enabled

# A directory under the root is a child state-dir if it holds any of these.
_STORE_FILES = ("profile.json", "constraints.json", "experiments.json")
# Reads that may fail on a hand-corrupted file; caught per-child so one bad dir
# doesn't sink the whole session bootstrap.
_READ_ERRORS = (ValueError, OSError, ValidationError)


def _read_child(child_dir: Path) -> dict:
    store = ExperimentStore(child_dir)
    entry: dict = {"dir": str(child_dir), "profile": None, "constraints": []}
    warnings: list[str] = []
    try:
        profile = store.get_profile()
        entry["profile"] = profile.model_dump(mode="json") if profile is not None else None
    except _READ_ERRORS as e:
        warnings.append(f"profile.json unreadable ({e.__class__.__name__})")
    try:
        entry["constraints"] = [c.model_dump(mode="json") for c in store.list_constraints()]
    except _READ_ERRORS as e:
        entry["constraints"] = None
        warnings.append(f"constraints.json unreadable ({e.__class__.__name__})")
    if warnings:
        entry["warning"] = "; ".join(warnings)
    return entry


def _scan_child_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return [
        child
        for child in sorted(root.iterdir())
        if child.is_dir() and any((child / f).exists() for f in _STORE_FILES)
    ]


def bootstrap(root: Path | str | None = None, state_dir: Path | str | None = None) -> dict:
    """Return the whole session's persisted state in one payload. See module docstring."""
    root_path = Path(root) if root is not None else DEFAULT_ROOT
    enabled = memory_enabled(root)
    result: dict = {"memory": "enabled" if enabled else "disabled", "children": []}
    if not enabled:
        # Opted out: the flag is the only thing we're allowed to surface — do not scan.
        return result

    if state_dir is not None:
        child_dirs = [Path(state_dir)]
    else:
        child_dirs = _scan_child_dirs(root_path)
        # Never treat the settings file's own root as a child dir.
        child_dirs = [d for d in child_dirs if d.name != SETTINGS_FILENAME]

    result["children"] = [_read_child(d) for d in child_dirs]
    return result
