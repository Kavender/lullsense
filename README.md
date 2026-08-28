<!-- Language: **English** · [中文](README_ZH.md) -->

**English** · [中文](README_ZH.md)

<p align="center">
  <img src="assets/lullsense-logo.png" alt="LullSense (知眠)" width="200">
</p>

# LullSense (知眠)

> Open-source baby sleep intelligence for every family.

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Scope](https://img.shields.io/badge/ages-4–36%20months-brightgreen)
![Safety](https://img.shields.io/badge/safety-first%20·%20never%20diagnoses-orange)
![Status](https://img.shields.io/badge/status-pre--release%20(private)-lightgrey)

LullSense is an Agent Skill that helps parents understand baby and toddler sleep through **evidence-informed conversation**, with **optional longitudinal pattern detection** when sleep data is available. It gives real, useful help from the conversation alone — no paid app, tracker, or subscription required.

> **More data improves the answer; data is never the price of admission.**

It is educational and supportive — **not a medical device**. It never diagnoses, always runs safety triage first, and is honest about what is grounded evidence versus a recalibratable heuristic.

---

## Why this exists

Good sleep help is expensive, gated behind subscriptions, or a timezone away at 3am. The authoritative guidance (AAP safe-sleep, AASM sleep-duration consensus, the developmental literature) is public but scattered and hard to apply to *your* child at 3am. This skill distills that public evidence into a calm, individualized consultation that any capable AI agent can carry — for free, inspectably, and safely.

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

The skill surfaces **signals and hypotheses with evidence and limitations** — never a diagnosis, never a wall of analysis dumped at once.

---

## What it does

- **No-data mode (primary path).** Reasons from the parent's account using a versioned, cited knowledge base. A verbal report ("waking at 5am all week") is real evidence.
- **Data-enhanced mode.** Optionally ingest a sleep log — typed notes, generic CSV/JSON, or an official Huckleberry export — and fold a per-child **baseline** and **detector signals** into the reasoning.
- **Proactive review.** A parent-initiated *"review my recent sleep"* flow that turns detector signals into a calm, prioritized change summary — capped, de-duplicated, and led by what's *steady* — engineered to avoid alert fatigue.
- **Constraint-first & planful.** Elicits hard constraints (daycare nap, pickup, work) *before* recommending, proposes the smallest useful experiment, and gives multi-day transitions a day-by-day roadmap.
- **A minimal local store.** Persists only a child profile (date-of-birth so age never goes stale), explicitly-saved durable constraints, and experiment state — **never raw sleep logs**.

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
npx skills add Kavender/lullsense
```

Installs the skill into your agent (e.g. `~/.claude/skills/lullsense/`). Then just ask a baby/toddler sleep question in natural language.

**Optional analysis engine** (data-enhanced + proactive review):

```bash
pip install lullsense       # exposes lullsense-analyze / lullsense-experiment
```

The skill is fully useful from conversation alone — data is never required.

> Working from source? `git clone https://github.com/Kavender/lullsense.git`

> **Status:** pre-release and **private** — released publicly only once fully built and tested.

---

## What it knows

A four-layer, versioned evidence base — **53 claims** across **29 sources**, validated by a schema/safety checker (`scripts/validate_knowledge.py`).

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
   ├─ skills/lullsense/references/*.md   13 on-demand references (safety, reasoning, persona, developmental, myths, interventions, sleep-training, signal-taxonomy, provider/data-contract …)
   ├─ skills/lullsense/knowledge/*.yaml  versioned claims + sources (+ validate_knowledge.py)
   │
   └─ baby_sleep/       optional, vendor-neutral analysis engine (pure Python)
        ├─ contract/    canonical sleep-log schema (ApproxTime, provenance)
        ├─ ingest/      manual-text / generic-CSV / JSON / official Huckleberry adapters
        ├─ analyze/     wake-day segmentation, ~22 features, robust per-child baseline
        ├─ detect/      10 baseline-relative, age-gated, non-diagnostic signal detectors
        ├─ review/      proactive review summary (rank · dedupe · cap · steady domains · freshness guard)
        └─ store/       minimal state: child profile + saved constraints + experiments (no raw logs)
```

Everything is inspectable and deterministic; the reasoning layer is vendor-neutral (no provider-specific behavior), and a data provider / MCP integration is entirely optional.

---

## Repository structure

| Path | Purpose |
|---|---|
| `skills/lullsense/` | Skill: SKILL.md (thin router + prime directives) + references + knowledge |
| `baby_sleep/` | Optional analysis engine (contract · ingest · analyze · detect · review · store) |
| `scripts/` | Thin CLIs: `validate_knowledge.py`; analysis via `lullsense-analyze` / `lullsense-experiment` |
| `evals/` | Deterministic evals (proactive signals + review), consultant rubric, safety red-flag cases |
| `examples/` | Synthetic example sleep logs |
| `tests/` | Test suite (**188 passing**) |
| `assets/` | Brand logo |

---

## Contributing & community

Contributions are welcome and require a **DCO sign-off** (`git commit -s`) — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Medical/safety content goes through a human review gate. Please keep examples and fixtures **synthetic** — child sleep data is sensitive.

Guardrails for contributors: never fabricate a citation or threshold; safety conclusions come only from authoritative, verified sources; the validator (`python scripts/validate_knowledge.py`) must pass.

---

## Status & roadmap

Built phase-by-phase; Phases 0–5 are complete and merged:

- **P0** — evidence base: claims/sources, safety triage, coverage matrix.
- **P1** — canonical schema, ingest adapters, minimal store.
- **P2** — features + robust per-child baseline.
- **P3** — 10 non-diagnostic, age-gated signal detectors.
- **P4** — conversational consultant skill (persona, reasoning, intake, interventions, sleep-training).
- **P5** — proactive *"review my recent sleep"* flow.
- **P6 (next)** — open-source documentation hygiene, then public release.

---

## License

**Apache-2.0.** See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). This project reproduces **no** proprietary text from any commercial product or consultant; public practice is synthesized and cited by source.
