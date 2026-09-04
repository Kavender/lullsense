<!-- Language: **English** · [中文](README_ZH.md) -->

**English** · [中文](README_ZH.md)

<p align="center">
  <img src="assets/lullsense-logo.png" alt="LullSense (知眠)" width="200">
</p>

# LullSense (知眠)

> **An open-source baby sleep support Agent Skill — there when professional support isn't immediately available, helping parents make sense of what is happening first.**

[![CI](https://github.com/Kavender/lullsense/actions/workflows/ci.yml/badge.svg)](https://github.com/Kavender/lullsense/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Scope](https://img.shields.io/badge/ages-4–36%20months-brightgreen)
![Safety](https://img.shields.io/badge/safety-first%20·%20never%20diagnoses-orange)
![Status](https://img.shields.io/badge/status-public%20alpha-brightgreen)

**A calm, evidence-informed reference for the 3am questions: why is my baby waking, should I change something, or should I wait and watch?**

LullSense is an open-source, evidence-informed baby and toddler sleep **support** Agent Skill.

It can start with conversation alone. A parent can simply say: “she has been waking at 5am,” “naps suddenly got shorter,” or “daycare controls the nap and I cannot move it.” LullSense first tries to understand what changed, what the family cannot change, and what might be worth trying next.

When recent sleep history is available, LullSense can also compare what is happening now with **that child’s own personal baseline**, helping surface meaningful changes instead of relying only on age-based norms.

> **More data can sharpen the picture, but data is never required to start.**

LullSense is educational and supportive. It is **not a medical device, and it is not intended to replace pediatricians or professional sleep consultants**. It does not diagnose. When a health or safety concern should take priority, sleep optimization stops and the family is directed toward appropriate professional care.

We see LullSense as **steady, always-available support around good sleep care**: something parents can use between consultations, when their consultant is not immediately available, or when they simply need help organizing what changed before deciding what to do next.

Keeping LullSense **free and open source** matters to us, too: whether good sleep support is within reach shouldn't come down to budget, a subscription, or which timezone you happen to be in. That's an aim we're building toward — see the honest note below on who this alpha actually reaches today.

In the long run, we do not believe good sleep support is a choice between humans and AI.

**Professional judgment, family context, longitudinal sleep observation, and always-available tools can complement one another.**

> **Who it reaches today.** LullSense currently runs inside an AI agent and installs from source, so this public alpha is best suited to technically comfortable parents, agent users, and builders. Making the experience easier for ordinary families is part of the roadmap, not something we pretend is solved already.

---

## Why this exists

Parenting creates a lot of moments like this:

A baby suddenly starts waking earlier. Night wakings return. Naps fall apart. A schedule that worked last week suddenly stops working.

There is plenty of information online about how much a child “should” sleep or what a typical wake window looks like.

But the harder questions are usually more personal:

**Why did this change now?**

**Should we adjust something, or give it a few more days?**

**If daycare nap time, pickup, work, or sibling schedules cannot move, what can we realistically change?**

Professional sleep consultants can be incredibly valuable here.

A good consultant does much more than read a schedule. They understand the child, the family, the constraints, what has already been tried, and how the parents themselves feel about different approaches.

But sleep questions do not happen only during the hour of a consultation.

Many of them happen in between:

- Something changed tonight — does it matter?
- We have tried this adjustment for three days — should we keep going?
- Sleep feels better this week — is there actually a trend?
- Before the next consultation, how do we make sense of everything that happened?

LullSense started from that gap.

**It is not designed to replace professional sleep consultants. It is designed to support the spaces around professional care.**

When no one is available, it can help a parent organize the problem.  
When sleep history exists, it can help summarize recent changes.  
When a family is trying a plan, it can help track what happened and prepare a clearer follow-up.

We want to borrow the best parts of thoughtful sleep consultation:

**understand the child and family first, then decide what to try — rather than applying a generic schedule.**

Long term, we hope LullSense can become an open, shared tool that both families and professionals can build on — bringing together practitioner expertise, longitudinal observation, and AI assistance to help more babies and families sleep better.

---

## What a conversation can look like

### No sleep log required

> **Parent:** My 8-month-old suddenly wakes at 5am every day. Is something wrong?
>
> **LullSense:** That sounds exhausting. I would not jump straight to calling it a “sleep regression” — first I want to understand what actually changed. Roughly when has bedtime been, how have naps looked, and did the 5am waking appear suddenly or creep earlier over a few days? From there we can narrow to the most likely explanations and choose one small adjustment to test.

### With recent sleep history

> **Parent:** Can you look over the last two weeks?
>
> **LullSense:** Most of the picture is actually steady: total night sleep, naps, and bedtime have not shifted much. One thing has changed — mornings have moved about 40 minutes earlier relative to her own recent baseline. I would focus on that change rather than rebuilding the whole schedule.

### Working around real-life constraints

> **Parent:** She is 15 months. Daycare only offers one nap at noon and I cannot change it, but she seems overtired.
>
> **LullSense:** Then the nap time is a fixed constraint, so I would not tell you to “move the nap earlier.” The useful levers are the things you can actually control — bedtime, how early mornings are handled, and possibly weekend recovery. We can start with one small change and see whether early waking and bedtime improve together.

### Asking about the next sleep

> **Parent:** She woke at 7. When is the next nap?
>
> **LullSense:** If I only have age information, I would give you a fairly broad range, not a “must sleep at” time. If I have several days of her own recent naps, I can tighten that range around her pattern. Tired cues still matter more than the clock.

LullSense surfaces **signals, hypotheses, and ways to test them** — not diagnoses, and not a wall of analysis dumped on a tired parent.

---

## What LullSense does

- **Conversation-first support**  
  No tracker required. Parent-reported patterns are useful information and can be enough to start discussing early waking, night waking, short naps, bedtime resistance, nap transitions, daycare schedules, and other common sleep questions.

- **Data-enhanced analysis**  
  Optionally ingest typed notes, generic CSV / JSON, or an official Huckleberry export. With recent history, the analysis engine builds a **per-child baseline** and looks for meaningful changes relative to that child. If a data provider / MCP is connected, LullSense can **auto-pull recent sleep** (vendor-neutral, with a one-line heads-up) instead of asking you to export by hand.

- **Longitudinal pattern detection**  
  The current engine can surface signals such as early waking, night waking, short naps, split nights, total-sleep drop, schedule drift, high variability, nap transition, and related changes. These are observations, not medical diagnoses.

- **Recent-sleep review**  
  A parent can ask, “How has sleep been lately?” LullSense leads with what is still stable, then highlights the few changes that appear most worth attention — deliberately avoiding alert fatigue.

- **Next-nap / bedtime ranges**  
  With limited information, it uses broad age-typical rhythm as orientation. With recent personal data, it can use the child’s own pattern. Wake windows are labeled as **product heuristics**, not clinical cutoffs.

- **Constraint-first reasoning**  
  Daycare naps, pickup, work, room-sharing, siblings, and other real-life constraints are part of the problem definition, not afterthoughts. The system works on the levers a family can actually move.

- **Minimal local state**  
  LullSense can keep a child profile, explicitly saved durable constraints, and experiment state. **Raw sleep logs are not persisted in the local store.**

---

## Principles we care about

| Principle | What it means in practice |
|---|---|
| **Safety first** | If a health or safety concern takes priority, ordinary sleep optimization stops and the family is directed toward appropriate professional care. |
| **Never diagnoses** | LullSense can discuss factors that may affect sleep, but it does not infer a medical diagnosis from sleep behavior. |
| **No pretending certainty** | Evidence-backed claims keep their sources; heuristics are labeled as heuristics; where the literature does not provide a precise cutoff, LullSense does not invent one. |
| **This child before the average child** | Age-based norms are context, not an instruction manual. When personal history exists, the child’s own baseline matters. |
| **Reality before the ideal schedule** | Daycare, work, pickup, family preferences, and other constraints are part of the recommendation from the start. |
| **Small experiments** | Prefer one low-risk, observable adjustment over rebuilding an entire schedule at once. |
| **Data is optional — but meaningful** | Conversation is enough to start; continuous sleep history can materially improve longitudinal, child-specific analysis. |
| **Complement professional support** | LullSense is designed to help in the spaces around human care, not to claim that AI replaces practitioner judgment and relationship. |

---

## Supported scope

Current public alpha scope:

- **Ages 4–36 months:** behavioral / schedule support around sleep habits, naps, bedtime, night waking, early waking, and related non-medical questions.
- **Under 4 months:** safe-sleep guardrails and safety-oriented support only; no sleep training or structured schedule optimization.

This does not mean every sleep issue after 4 months is appropriate for self-management. Safety rules take priority whenever professional evaluation may be needed.

---

## Install

### Add the Agent Skill

```bash
# Add to the current project
npx skills add Kavender/lullsense

# Or install globally (user-level)
npx skills add Kavender/lullsense -g

# See all options
npx skills add --help
```

A project-level install lands under the project’s agent skills directory. A global install uses the shared `~/.agents/skills/lullsense/` and is symlinked into the relevant agent directory; for Claude Code, that is `~/.claude/skills/lullsense/`.

Then ask a baby / toddler sleep question in natural language.

### Optional: analysis engine

For structured sleep-log analysis, longitudinal review, and timing prediction:

```bash
# Public alpha: install from source (not yet on PyPI)
pip install "git+https://github.com/Kavender/lullsense.git"
```

This exposes:

```bash
lullsense-analyze
lullsense-experiment
```

Working from a clone:

```bash
git clone https://github.com/Kavender/lullsense.git
cd lullsense
pip install .
```

> **Status: public alpha.** Core flows are implemented and covered by CI / evals. Safety content is grounded in authoritative sources and checked for provenance, but has **not yet completed independent pediatric-sleep / clinical review**. Source validation is not the same as clinical review; independent review remains an important step before a stable release.

---

## Data & privacy

LullSense itself has no cloud backend.

Its local store keeps only a small amount of cross-session state, such as:

- child profile / date of birth
- explicitly saved durable family constraints
- current experiment state

**Raw sleep logs are not written into LullSense’s local state store.**

Memory is disclosed when first used, and stored state can be inspected, disabled, or deleted.

One important boundary: **LullSense runs inside the AI agent / model provider you choose.** Conversation content, sleep logs you share, and connected-tool output may therefore be processed by that provider under its own privacy policy.

See [`DATA_HANDLING.md`](DATA_HANDLING.md) for the full data boundary.

---

## Knowledge & evidence

LullSense deliberately separates “what research says,” “what professional guidance says,” and “what is a practical sleep-support heuristic.”

The current knowledge base is organized into four layers:

| Layer | Content | How it is used |
|---|---|---|
| **A · Safety** | Safe sleep, red-flag triage, low-age guardrails | Guideline / professional consensus / systematic-review sources only; safety rules take priority. |
| **B · Development** | Sleep duration, developmental variation, nap transitions | Context and reference ranges, not a schedule prescription for one child. |
| **C · Behavioral** | Settling, night waking, bedtime, sleep-training approaches | Systematic-review-informed where available; approaches are presented without moralizing. |
| **D · Practice** | How to ask, reason around constraints, reassess, and support parents | Practical methods; heuristics are labeled rather than presented as medical fact. |

Current knowledge base: **56 claims across 34 sources**, validated by `scripts/validate_knowledge.py` for schema, provenance, and safety rules.

---

## Safety & honest limits

- **Educational / general-wellness only.** Not a substitute for pediatric medical care.
- **Red flags halt ordinary sleep optimization.**
- **Safety claims require authoritative, pre-verified sources.** Runtime web search cannot establish a safety conclusion.
- **Heuristics are labeled.** Wake-window ranges, scheduling thresholds, and signal severity are product heuristics when the evidence does not define clinical cutoffs.
- **Parent-named medical conditions may be discussed educationally, but LullSense does not infer that a child has a condition.**
- **The consultation style is itself a testable product hypothesis.** We expect practitioner and parent feedback to improve it.

---

## How it works

LullSense has two complementary parts:

1. **Sleep-support reasoning** — conversation, context, hypotheses, evidence, and a realistic small next step.
2. **Sleep observer / analysis engine** — when logs are available, normalize the data, build a personal baseline, compute features, and surface recent changes.

```text
parent question / sleep history
          │
          ▼
safety → age → goal → family constraints
          │
          ├── no data ─────> conversation + evidence
          │
          └── data ────────> normalize → personal baseline → signals
                                                   │
                                                   ▼
                                           ranked hypotheses
                                                   │
                                                   ▼
                                       one small testable change
                                                   │
                                                   ▼
                                               observe
```

Repository implementation:

```text
skills/lullsense/SKILL.md
   │
   ├─ references/*.md        16 on-demand references
   ├─ knowledge/*.yaml       versioned claims / sources / heuristics
   │
   └─ baby_sleep/            optional vendor-neutral Python engine
        ├─ contract/         canonical sleep data + provenance
        ├─ ingest/           manual / CSV / JSON / Huckleberry export
        ├─ analyze/          features + robust personal baseline
        ├─ detect/           baseline-relative signal detectors
        ├─ review/           recent-sleep change review
        ├─ predict/          next nap / bedtime range
        └─ store/            profile / constraints / experiments
```

The analysis engine and evidence validation are deterministic and inspectable. The support reasoning is model-driven, but its reasoning framework, evidence sources, and evaluation criteria are open in the repository.

The core is vendor-neutral: CSV, JSON, MCP, or future sleep-data sources should remain replaceable adapters rather than defining the product.

---

## Built with practitioners, not around them

LullSense is still a public alpha.

Engineering can help us test code, validate citations, and evaluate reasoning behavior. But engineering alone cannot define what good real-world sleep support looks like.

We especially welcome feedback from:

- baby and toddler sleep consultants
- pediatricians and child-health professionals
- pediatric sleep researchers
- postpartum doulas and newborn-care specialists
- other practitioners who work closely with families

We would love practitioner input on questions such as:

- Which responses are genuinely useful in real consultations?
- Which advice sounds reasonable but could mislead a parent?
- When should the system stop sleep optimization and encourage professional evaluation?
- What kinds of support can AI safely provide between consultations?
- What should remain firmly in the hands of a human professional?
- Could LullSense help with sleep-log summaries, plan tracking, or follow-up preparation without getting in the way of the practitioner-parent relationship?

We do not assume AI can replace good professional support.

Our goal is to find the right boundary together: **let tools handle what tools are good at, while preserving the judgment, experience, and human support that professionals uniquely provide.**

Practitioner review, criticism, collaboration, and integration ideas are all very welcome.

---

## Repository structure

| Path | Purpose |
|---|---|
| `skills/lullsense/` | Agent Skill: `SKILL.md`, references, and knowledge |
| `baby_sleep/` | Optional Python analysis engine |
| `scripts/` | Knowledge validator and CLI entry points |
| `evals/` | Detector / review evals, consultation rubric, safety cases |
| `examples/` | Synthetic example sleep logs |
| `tests/` | Automated test suite run by GitHub Actions CI |
| `assets/` | Brand assets |

---

## Contributing & community

Issues, PRs, practitioner review, and real-world product feedback are all welcome.

Code contributions require a **DCO sign-off** (`git commit -s`) — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

Medical / safety content goes through a human review gate. Please keep examples and fixtures **synthetic**: child sleep and family data are sensitive.

Contributor guardrails:

- never fabricate a citation or threshold
- safety conclusions must come from authoritative, verified sources
- `python scripts/validate_knowledge.py` must pass

---

## License

**Apache-2.0.** See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

LullSense reproduces no proprietary text from commercial sleep products or private consultants. Public practice is synthesized and cited by source where applicable.
