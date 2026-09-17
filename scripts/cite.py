#!/usr/bin/env python3
"""`lullsense-cite <id> [<id> ...]` — fetch one claim or source entry, not the whole YAML.

The agent scans `knowledge/claims-index.md` to decide which claims to cite, then calls this to
retrieve only those full entries — so a citation costs one small lookup instead of loading the
~64KB `claims.yaml` / ~30KB `sources.yaml` into the conversation. Each id is looked up as a
`claim_id` in claims.yaml first, then as a source `id` in sources.yaml; the matched entry is
printed back as YAML. Unknown ids report cleanly and set a non-zero exit.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

_REL = Path("skills/lullsense/knowledge")


def _knowledge_dir() -> Path:
    """Locate the skill's knowledge/ dir across invocation contexts.

    `lullsense-cite` runs in the *skill* working context, not necessarily next to an installed
    wheel — the alpha install is a non-editable `pip install "git+..."`, so a console script's
    __file__ points into site-packages, which does NOT carry the skill's YAML. So resolve in
    order: an explicit env override; the nearest `skills/lullsense/knowledge` at or above cwd
    (the normal skill checkout); then relative to this file (editable / source-tree runs).
    """
    env = os.environ.get("LULLSENSE_KNOWLEDGE_DIR")
    if env:
        return Path(env)
    for base in (Path.cwd(), *Path.cwd().parents):
        cand = base / _REL
        if (cand / "claims.yaml").exists():
            return cand
    return Path(__file__).resolve().parent.parent / _REL


_KNOWLEDGE = _knowledge_dir()
CLAIMS = _KNOWLEDGE / "claims.yaml"
SOURCES = _KNOWLEDGE / "sources.yaml"


def _load(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(
            f"FAIL: {path.name} not found under {path.parent}. Run lullsense-cite from the "
            f"skill checkout, or set LULLSENSE_KNOWLEDGE_DIR to the knowledge/ directory."
        )
    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


def lookup(entry_id: str) -> tuple[str, dict] | None:
    """Return ("claim"|"source", entry) for the first match, or None."""
    for c in _load(CLAIMS):
        if c.get("claim_id") == entry_id:
            return "claim", c
    for s in _load(SOURCES):
        if s.get("id") == entry_id:
            return "source", s
    return None


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("usage: lullsense-cite <claim_id|source_id> [more ids ...]", file=sys.stderr)
        return 2
    missing: list[str] = []
    blocks: list[str] = []
    for entry_id in argv:
        hit = lookup(entry_id)
        if hit is None:
            missing.append(entry_id)
            continue
        kind, entry = hit
        rendered = yaml.safe_dump(entry, sort_keys=False, allow_unicode=True, width=100)
        blocks.append(f"# {kind}: {entry_id}\n{rendered}")
    if blocks:
        print(("\n---\n".join(blocks)).rstrip())
    for entry_id in missing:
        print(f"not found: {entry_id} (not a claim_id in claims.yaml or an id in sources.yaml)",
              file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
