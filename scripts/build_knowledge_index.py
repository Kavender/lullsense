#!/usr/bin/env python3
"""Generate `knowledge/claims-index.md` from `knowledge/claims.yaml`.

Citing a claim used to mean loading the full ~64KB `claims.yaml` (and ~30KB `sources.yaml`)
into the conversation just to find one entry. This builds a compact one-line-per-claim index
the agent scans to pick *which* claims to cite; it then fetches only those full entries with
`scripts/cite.py` (`lullsense-cite`). The index is generated, never hand-edited — CI
regenerates it and fails if it drifts from `claims.yaml`.

Run: python scripts/build_knowledge_index.py   (writes the index, prints its size).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CLAIMS = ROOT / "skills/lullsense/knowledge/claims.yaml"
INDEX = ROOT / "skills/lullsense/knowledge/claims-index.md"

GIST_MAX = 60  # chars of the claim text kept in the scan line; full text via lullsense-cite

HEADER = """\
# Claims Index (generated — do not edit by hand)

Generated from `claims.yaml` by `scripts/build_knowledge_index.py`. One scannable line per
claim so the agent can decide **which** claims to cite without loading the full YAML.

**Retrieval:** pick the 1–3 `claim_id`s you'll actually cite from the table below, then fetch
each full entry with `lullsense-cite <claim_id>` (it also resolves a `<source_id>` from
`sources.yaml`). **Never load `claims.yaml` or `sources.yaml` wholesale in conversation.**
A_safety citations are already embedded inline in `references/safety-triage.md`.

| claim_id | layer | evidence | claim (gist — fetch full text with `lullsense-cite`) |
|---|---|---|---|
"""


def _load(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise SystemExit(f"FAIL: {path} is not a YAML list")
    return data


def _gist(claim_text: str) -> str:
    # One line, no table-breaking pipes, truncated — the index is a scan aid, not the source.
    text = " ".join(str(claim_text).split()).replace("|", "/")
    return text if len(text) <= GIST_MAX else text[: GIST_MAX - 1].rstrip() + "…"


def build() -> str:
    rows = _load(CLAIMS)
    body = [
        f"| `{c.get('claim_id', '?')}` | {c.get('layer', '?')} | "
        f"{c.get('evidence_level', '?')} | {_gist(c.get('claim', ''))} |"
        for c in rows
    ]
    return HEADER + "\n".join(body) + "\n"


def main() -> int:
    content = build()
    INDEX.write_text(content, encoding="utf-8")
    size = len(content.encode("utf-8"))
    n = content.count("\n| `")
    print(f"wrote {INDEX.relative_to(ROOT)}: {n} claims, {size} bytes ({size / 1024:.1f}KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
