<!-- Language: **English** · [中文](README_ZH.md) -->

**English** · [中文](README_ZH.md)

<p align="center">
  <img src="assets/lullsense-logo.png" alt="LullSense (知眠)" width="200">
</p>

# LullSense (知眠)

> Open-source baby sleep intelligence for every family.

[![CI](https://github.com/Kavender/lullsense/actions/workflows/ci.yml/badge.svg)](https://github.com/Kavender/lullsense/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Scope](https://img.shields.io/badge/ages-4–36%20months-brightgreen)
![Safety](https://img.shields.io/badge/safety-first%20·%20never%20diagnoses-orange)
![Status](https://img.shields.io/badge/status-public%20alpha-brightgreen)

**A calm, evidence-literate voice for the 3am questions — free, and no tracker required.**

LullSense is an open-source **Agent Skill** that helps parents understand baby and toddler sleep through **evidence-informed conversation**, with **optional longitudinal pattern detection** when a sleep log is available. It gives real, useful help from the conversation alone — no paid app, no tracker, no subscription.

> **More data improves the answer; data is never the price of admission.**

It is educational and supportive — **not a medical device**. It never diagnoses, always runs safety triage first, and is honest about what is grounded evidence versus a recalibratable heuristic.

---

## Why this exists

It's 3am. The baby won't resettle, you're scrolling for answers, and every door is a little bit closed: the tracker app wants a subscription, a private consultant costs hundreds and is a timezone away, and a web search returns a pile of confident, contradictory blog posts. Meanwhile the *actual* authoritative guidance — AAP safe-sleep, the AASM sleep-duration consensus, the developmental literature — is public, but scattered, technical, and nearly impossible to apply to *your* child at *that* hour.

LullSense began with exactly that frustration: even a good sleep consultant is asleep at 3am, a timezone away — and plenty of families can't afford one at all. Good sleep help shouldn't depend on your budget or your timezone. So this project distills that public evidence into a calm, individualized consultation any capable AI agent can carry — free, inspectable, safety-first, and honest about the line between grounded evidence and a rule-of-thumb. Not to replace your pediatrician, but to be a steady, evidence-literate voice in the room when no one else is awake.

---

## Example

**No data, just conversation:**

> **Parent:** My 8-month-old suddenly wakes at 5am every day. Is something wrong?
>
> **Consultant:** That 5am start sounds exhausting — let's figure it out together. First, a quick check: is she otherwise well — feeding normally, no new congestion or fever? … Good. Early waking at this age is common and has a few usual drivers. Tell me roughly when she's going down and how the last few nights have looked, and I'll walk through the two most likely explanations and one small thing to try — plus exactly what to watch so we know if it's working.

**With a recent sleep log ("how has sleep been?"):**

> **Parent:** Can you look over the last two weeks?
>
> **Consultant:** Good news first — across her nights, naps, bedtimes, total sleep, and how consistent the timing's been, most of it is holding steady. One thing shifted: her mornings have crept about 40 minutes earlier this week. Here's the likely why, what would change my mind, and a single adjustment to try…

**Predicting the next nap or bedtime:**

> **Parent:** She woke at 7 — when's her next nap?
>
> **Consultant:** Likely somewhere in the **9:00–10:00** window — that's from her age-typical rhythm, so a wide guess, not a fixed time, and her tired cues win over the clock. Share a few days of her actual naps and I can tighten that to her own pattern.

**Reasoning around real-life constraints:**

> **Parent:** She's 15 months and always a bit overtired. Daycare does one nap at noon and I can't change it — am I doing something wrong?
>
> **Consultant:** That long stretch before her afternoon nap is set by the daycare schedule — that's on the schedule, not on you. It means a little overtiredness is baked in, and no bedtime tweak fully erases it while the nap's fixed. The lever I'd reach for first is a slightly earlier bedtime to take the edge off. Want a couple of other options that work *around* the fixed nap?

The skill surfaces **signals and hypotheses with evidence and limitations** — never a diagnosis, never a wall of analysis dumped at once.

---

## What it does

- **No-data mode (primary path).** Reasons from the parent's account using a versioned, cited knowledge base. A verbal report ("waking at 5am all week") is real evidence.
- **Data-enhanced mode.** Optionally ingest a sleep log — typed notes, generic CSV/JSON, or an official Huckleberry export — and fold a per-child **baseline** and **detector signals** into the reasoning. If a data provider / MCP is connected, it can **auto-pull recent sleep** (with a one-line heads-up, vendor-neutral) instead of asking you to export by hand.
- **Next-sleep timing prediction.** Answers *"when's the next nap/bedtime?"* as a **range, never a single time** — from the age-typical rhythm, or a tighter band from the child's own recent pattern — always cue-first, with wake windows labeled a *product heuristic*, not a clinical clock. Under 4 months it gives cue-based orientation, not a schedule.
- **Longitudinal (recent-sleep) review.** A parent-initiated *"review my recent sleep"* flow that turns detector signals into a calm, prioritized change summary — capped, de-duplicated, and led by what's *steady* — engineered to avoid alert fatigue. The skill doesn't monitor in the background; a host, scheduler, or automation can invoke the same detector proactively if it wants to.
- **Constraint-first & reality-based.** Elicits — and **remembers across sessions** — hard constraints (daycare nap, pickup, work) *before* recommending. When a fixed constraint forces sleep away from the age-typical ideal, it names the shortfall as **structural, not a parenting failure**, never prescribes the blocked ideal, and works the *movable* levers with honest expectations. Multi-day transitions get a day-by-day roadmap.
- **A minimal local store.** Persists only a child profile (date-of-birth so age never goes stale), explicitly-saved durable constraints, and experiment state — **never raw sleep logs**. Stored locally on your machine, never uploaded. Memory is on by default but **it tells you the first time it saves and you can turn it off anytime**; see **[DATA_HANDLING.md](DATA_HANDLING.md)** for exactly what's kept, how connected-log access works, and how to inspect or delete it.

### Core principles

| Principle | What it means |
|---|---|
| **Safety first** | Screens for red flags before any schedule advice; on a red flag it **halts** optimization and routes to medical care — warmly, never naming a cause. |
| **Never diagnoses** | Surfaces signals and hypotheses with evidence and limitations. Diagnosis is a clinician's job. |
| **No fabrication** | Every grounded figure cites a source; heuristics are labeled *product heuristics — recalibratable, not clinical cutoffs*; where the literature declines a cutoff, it says so. |
| **Individualize** | Authoritative literature is a *reference, not a manual* — the same presentation can have different causes; advice is always about *this* child and family. |
| **Data is optional** | Full value from conversation alone; a tracker is never required. |

---

## Supported scope (first alpha)

- **Ages 4–36 months** for behavioral/schedule support.
- **Under 4 months:** a **safe-sleep guardrail only** — safe-sleep essentials and red-flag screening, no schedule optimization.

---

## Install

```bash
# Add the skill to the current project
npx skills add Kavender/lullsense

# ...or install it globally (user-level), available in every project
npx skills add Kavender/lullsense -g

# See all options
npx skills add --help
```

This makes the skill available to your agent. A project install lands under `.claude/skills/lullsense/`; a global (`-g`) install lands in the shared `~/.agents/skills/lullsense/` and is symlinked into each agent's directory (for Claude Code, `~/.claude/skills/lullsense/`). Then just ask a baby/toddler sleep question in natural language.

**Optional analysis engine** (data-enhanced + longitudinal review):

```bash
# Install from source (not yet on PyPI during the alpha)
pip install "git+https://github.com/Kavender/lullsense.git"
# exposes: lullsense-analyze / lullsense-experiment
```

Once published, `pip install lullsense` will be the one-liner; until then use the source install above. The skill is fully useful from conversation alone — data is never required.

> Working from a clone? `git clone https://github.com/Kavender/lullsense.git && pip install .`

> **Status: evidence-backed public alpha.** Feature-complete for a first release and live-tested. Safety content is grounded in authoritative sources and validated for provenance, but has **not yet completed independent pediatric-sleep / clinical review** — source validation is not the same as clinical review. Independent review is planned before a stable release. Feedback and issues welcome.

---

## What it knows

A four-layer, versioned evidence base — **56 claims** across **34 sources**, validated by a schema/safety checker (`scripts/validate_knowledge.py`).

| Layer | Content | Evidence bar |
|---|---|---|
| **A — Safety** | Safe sleep, red-flag triage, newborn guardrail | Guideline / professional consensus / systematic review only; high-evidence; source-backed (enforced) |
| **B — Developmental** | Sleep norms, ranges, nap transitions, developmental phases | Cited literature (AASM, Spencer, Tham, Galland …) |
| **C — Behavioral** | Settling, night waking, sleep-training methods | Systematic-review-informed; interventions framed non-judgmentally |
| **D — Practice** | Consultation craft, constraint elicitation, reassessment | Synthesized public practice; heuristics labeled as heuristics |

Delivery, tone, and the consultation spine live in a dedicated **persona layer** — warm, non-judgmental, guilt-reducing, and calibrated (reassure on the likely-benign **and** name what would change the picture, in the same breath).

---

## Safety & honest limits

- **Educational / general-wellness only.** It does not diagnose, treat, or prevent any condition and is not a substitute for a pediatrician.
- **Red flags halt advice.** Any safety red flag stops sleep-optimization and directs you to appropriate medical care.
- **Safety content is source-backed.** It comes only from authoritative, verified sources; runtime web search may never back a safety conclusion.
- **Heuristics are labeled.** Scheduling thresholds and severity bins are product heuristics, recalibratable — not clinical standards.
- **First-hand practice is a hypothesis.** The consultation persona is a strong, testable hypothesis about good practice — to be validated with real users, not treated as proven.

---

## How it works

```
skills/lullsense/SKILL.md  ── thin router: safety → age → goal → constraints → mode → hypotheses → smallest experiment
   │
   ├─ skills/lullsense/references/*.md   14 on-demand references (safety, reasoning, persona, developmental, myths, interventions, sleep-training, sleep-timing-prediction, signal-taxonomy, provider/data-contract …)
   ├─ skills/lullsense/knowledge/*.yaml  versioned claims + sources + wake-window heuristics (+ validate_knowledge.py)
   │
   └─ baby_sleep/       optional, vendor-neutral analysis engine (pure Python)
        ├─ contract/    canonical sleep-log schema (ApproxTime, provenance)
        ├─ ingest/      manual-text / generic-CSV / JSON / official Huckleberry adapters
        ├─ analyze/     wake-day segmentation, ~22 features, robust per-child baseline
        ├─ detect/      10 baseline-relative, age-gated, non-diagnostic signal detectors
        ├─ review/      recent-sleep review summary (rank · dedupe · cap · steady domains · freshness guard)
        ├─ predict/     next nap/bedtime timing — age-band + personal-baseline wake windows (a range, never a point)
        └─ store/       minimal state: child profile + saved constraints + experiments (no raw logs)
```

The analysis engine and evidence validation are deterministic and inspectable; the consultant reasoning is model-driven, with its reasoning contract, evidence sources, and eval criteria kept open. The reasoning layer is vendor-neutral (no provider-specific behavior), and a data provider / MCP integration is entirely optional.

---

## Repository structure

| Path | Purpose |
|---|---|
| `skills/lullsense/` | Skill: SKILL.md (thin router + prime directives) + references + knowledge |
| `baby_sleep/` | Optional analysis engine (contract · ingest · analyze · detect · review · store) |
| `scripts/` | Thin CLIs: `validate_knowledge.py`; analysis via `lullsense-analyze` / `lullsense-experiment` |
| `evals/` | Deterministic evals (proactive signals + review), consultant rubric, safety red-flag cases |
| `examples/` | Synthetic example sleep logs |
| `tests/` | Test suite (run in [CI](https://github.com/Kavender/lullsense/actions/workflows/ci.yml) on every push/PR, plus a clean-wheel install smoke test) |
| `assets/` | Brand logo |

---

## Contributing & community

Contributions are welcome and require a **DCO sign-off** (`git commit -s`) — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Medical/safety content goes through a human review gate. Please keep examples and fixtures **synthetic** — child sleep data is sensitive.

Guardrails for contributors: never fabricate a citation or threshold; safety conclusions come only from authoritative, verified sources; the validator (`python scripts/validate_knowledge.py`) must pass.

---

## License

**Apache-2.0.** See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). This project reproduces **no** proprietary text from any commercial product or consultant; public practice is synthesized and cited by source.
