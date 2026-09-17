"""Guards the Phase-3 split of the reasoning-framework god-file into focused leaves.

The 32KB `reasoning-framework.md` was split so a turn no longer loads the whole workflow to
answer one question (a latency win). This test locks that in: the god-file stays a tombstone,
the new leaves exist and carry their content, and no doc silently re-points at the god-file
(which would resurrect the cascade-loading the split removed).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "lullsense"
REFS = SKILL_DIR / "references"

# New leaf → a distinctive token that must be present (proves content, not just an empty file).
NEW_LEAVES = {
    "hypothesis-menu.md": "Accumulated sleep pressure",
    "constraint-reasoning.md": "DEVIATION_ASK_MULTIPLE",
    "analysis-json.md": "BaselineStatus",
    "review-mode.md": "also_noted_count",
    "evidence-rules.md": "Galland 2012",
}


def test_new_leaves_exist_and_carry_content():
    for name, token in NEW_LEAVES.items():
        path = REFS / name
        assert path.exists(), f"missing new leaf {name}"
        text = path.read_text(encoding="utf-8")
        assert token in text, f"{name} is missing its distinctive content token {token!r}"


def test_god_file_is_a_tombstone():
    text = (REFS / "reasoning-framework.md").read_text(encoding="utf-8")
    assert "tombstone" in text.lower(), "reasoning-framework.md should be a tombstone"
    # It must point readers to the new homes.
    for name in NEW_LEAVES:
        assert name in text, f"tombstone should point to {name}"
    # The bulky workflow must be gone, not merely re-titled.
    assert len(text.splitlines()) < 30, "tombstone should be short (content moved out)"


def test_no_doc_repoints_at_the_god_file():
    """Only the tombstone itself may mention reasoning-framework; every other skill/eval/example
    doc must point at the new leaves (or SKILL.md), so cascade-loading can't creep back."""
    offenders = []
    for base in (SKILL_DIR, ROOT / "evals", ROOT / "examples"):
        for md in base.rglob("*.md"):
            if md.name == "reasoning-framework.md":
                continue
            if "reasoning-framework" in md.read_text(encoding="utf-8"):
                offenders.append(str(md.relative_to(ROOT)))
    assert not offenders, f"these docs still point at the retired god-file: {offenders}"
