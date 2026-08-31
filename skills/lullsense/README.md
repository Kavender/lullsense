# LullSense (知眠)

> Open-source baby sleep intelligence for every family.

LullSense is an Agent Skill that helps parents understand baby and toddler sleep through
evidence-informed conversation, with optional longitudinal pattern detection when sleep
data is available. It is educational and supportive — **not a medical device** — never
diagnoses, and always runs safety triage first.

## Install

```bash
npx skills add Kavender/lullsense       # project-level
npx skills add Kavender/lullsense -g     # global (user-level), all projects
```

A project install lands under `.claude/skills/lullsense/`. A global (`-g`) install lands in the shared `~/.agents/skills/lullsense/` and is symlinked into each agent's directory (for Claude Code, `~/.claude/skills/lullsense/`).
Ask a baby/toddler sleep question in natural language and the skill takes over.

## Optional analysis engine

Data-enhanced and proactive-review modes use an optional Python engine:

```bash
pip install lullsense      # exposes: lullsense-analyze, lullsense-experiment
```

The skill is fully useful from conversation alone; data is never required.

## Scope & safety

- Ages **4–36 months** for behavioral/schedule support; under 4 months → a safe-sleep
  guardrail only.
- On any safety red flag it halts optimization and routes to medical care.
- Full project, sources, and license: the repository root README.

Apache-2.0.
