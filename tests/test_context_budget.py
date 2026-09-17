"""Context-budget tripwire (T14) so the router can't silently re-grow.

SKILL.md is always in context when the skill triggers, and SKILL.md + voice-card.md is the
"hot tier" an ordinary turn relies on — the two files that gate time-to-first-reply. SKILL.md
already re-grew once after being slimmed; this guard locks in the Phase-4 slim so a future
edit that pushes verbose detail back into the router fails loudly instead of quietly taxing
every turn. Move the detail into a reference instead.

Ceilings are set with headroom above the current sizes (not at the aspirational floor): the
inline safety net + persona core moves + the load-on-demand index have a real, intentional
floor (they exist so an ordinary turn needs zero reference reads — the latency win). If you
need to raise a ceiling, that's a signal to move content out, not to bump the number.
"""
import os

SKILL = "skills/lullsense/SKILL.md"
VOICE_CARD = "skills/lullsense/references/voice-card.md"
CLAIMS_INDEX = "skills/lullsense/knowledge/claims-index.md"

# Ceilings (bytes). Headroom over the Phase-4 sizes (SKILL ~21.7KB, hot tier ~24.7KB) for
# routine edits; well under the pre-slim 30.5KB the guard exists to prevent returning to.
SKILL_MAX = 23 * 1024        # 23552
HOT_TIER_MAX = 27 * 1024     # 27648
CLAIMS_INDEX_MAX = 9 * 1024  # 9216 — the scan aid must stay far smaller than claims.yaml (~64KB)


def test_skill_md_within_budget():
    size = os.path.getsize(SKILL)
    assert size <= SKILL_MAX, (
        f"SKILL.md is {size}B (> {SKILL_MAX}B). Move verbose per-step detail into a "
        f"references/*.md file rather than growing the router."
    )


def test_hot_tier_within_budget():
    size = os.path.getsize(SKILL) + os.path.getsize(VOICE_CARD)
    assert size <= HOT_TIER_MAX, (
        f"hot tier (SKILL.md + voice-card.md) is {size}B (> {HOT_TIER_MAX}B). The hot tier "
        f"gates time-to-first-reply — keep it lean."
    )


def test_claims_index_within_budget():
    size = os.path.getsize(CLAIMS_INDEX)
    assert size <= CLAIMS_INDEX_MAX, (
        f"claims-index.md is {size}B (> {CLAIMS_INDEX_MAX}B) — tighten GIST_MAX in "
        f"scripts/build_knowledge_index.py so the scan aid stays small."
    )
