#!/usr/bin/env python3
"""Guard: the red-flag quick net inlined into SKILL.md must stay byte-identical
(whitespace-normalized) to its source block in references/safety-triage.md.

The safety net is inlined into SKILL.md's Prime Directive 2 so the agent can screen
every turn without reading a file (a latency win). That duplication is only safe if the
two copies cannot drift — so this check is wired into CI. `references/safety-triage.md §2a`
is the source of truth; edit there first, then re-sync SKILL.md.

Run: python scripts/check_safety_inline_sync.py   (exit 0 = in sync, 1 = drift).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/lullsense/SKILL.md"
SAFETY = ROOT / "skills/lullsense/references/safety-triage.md"
START = "<!-- RED-FLAG-QUICKLIST:START -->"
END = "<!-- RED-FLAG-QUICKLIST:END -->"


def extract_block(path: Path) -> str:
    """Return the normalized text between the sync markers in `path`.

    Normalization strips each line and drops blank lines, so indentation added when the
    block is nested inside a list item in SKILL.md does not count as drift.
    """
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"FAIL: sync markers not found in {path}")
    body = text.split(START, 1)[1].split(END, 1)[0]
    lines = [ln.strip() for ln in body.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def check() -> tuple[bool, str]:
    skill_block = extract_block(SKILL)
    safety_block = extract_block(SAFETY)
    if skill_block == safety_block:
        n = len(skill_block.splitlines())
        return True, f"OK: red-flag quick net in sync ({n} lines) between SKILL.md and safety-triage.md §2a"
    # Produce a readable first-difference for the failure message.
    s, f = skill_block.splitlines(), safety_block.splitlines()
    for i, (a, b) in enumerate(zip(s, f)):
        if a != b:
            return False, (
                "FAIL: red-flag quick net drifted at line "
                f"{i + 1}:\n  SKILL.md      : {a!r}\n  safety-triage : {b!r}"
            )
    return False, (
        "FAIL: red-flag quick net length differs "
        f"(SKILL.md {len(s)} lines vs safety-triage {len(f)} lines)"
    )


def main() -> int:
    ok, msg = check()
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
