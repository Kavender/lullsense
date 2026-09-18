# Contributing

## Developer Certificate of Origin (DCO)

This project uses the DCO instead of a CLA. Sign off every commit:

```
git commit -s -m "your message"
```

The `Signed-off-by` line certifies you wrote the change or have the right to
submit it under the project's Apache-2.0 license (see https://developercertificate.org/).

## Local install & the `skills remove` footgun

If you install the skill from your clone to test it (`skills add ./skills/lullsense …`),
be careful uninstalling. Some agents — **OpenClaw**, and any agent that registers a skill
**in place** — point their skill directory straight at your source. For those,
`skills remove lullsense` **deletes `skills/lullsense/` from your working tree** (the `--copy`
flag does not prevent it). Claude Code, by contrast, installs a *copy* under `.claude/skills/`
(or `~/.claude/skills/` with `-g`), which is safe to remove.

Before removing, run `skills ls` and read the `Source:` line: if it points inside this repo,
don't `skills remove` it — just re-run `skills add` to refresh in place, or delete the agent
registration by hand. Everything under `skills/` is git-tracked, so an accidental delete is
recoverable with `git restore skills/lullsense`.

## Evidence & safety rules

- Never fabricate a citation, URL, or statistic. Mark unverifiable content as
  uncertain.
- Safety claims must cite an authoritative source (AAP / AASM / pediatric
  sleep medicine). Heuristics may back non-safety scheduling only.
- Run `python scripts/validate_knowledge.py` before submitting knowledge changes.

## Context budget & latency (which tier am I editing?)

The skill is loaded in tiers, and time-to-first-reply is dominated by how many files an
ordinary turn must read. Keep the router lean; push detail down a tier.

- **Tier 0 — `SKILL.md`** (always in context when the skill triggers). A **thin router**:
  the ten-step workflow skeleton, the inline safety red-flag net, the persona core moves,
  and a load-on-demand index. Binding rules + a pointer per topic — never the full
  mechanics. CI caps it (see below).
- **Tier 1 — inline hot path** (`SKILL.md` Prime Directive 2 net + `references/voice-card.md`).
  This is what lets an **ordinary turn answer with zero reference reads** — don't bloat it.
- **Tier 2 — topic references** (`references/*.md`), loaded only when a step calls for them,
  and **in one batch** when several are needed (serial reads are the main latency source).
- **Tier 3 — knowledge YAMLs** (`knowledge/*.yaml`), never loaded wholesale in conversation.

**Guards (CI + `pytest`):** `SKILL.md` ≤ 23KB and `SKILL.md + voice-card.md` ≤ 27KB
(`tests/test_context_budget.py`); the inline red-flag net stays byte-identical to
`safety-triage.md §2a` (`scripts/check_safety_inline_sync.py`). If a change trips a cap, move
the detail into a Tier-2 reference rather than raising the ceiling.

## Commits

Sign off every commit (DCO, above). Small, reviewable commits; keep the test suite,
`ruff check .`, and `python scripts/validate_knowledge.py` green.
