# Conversational Intake — Agent Reference

**Status:** Operational reference for the consultant skill. Cross-check any change against `knowledge/claims.yaml` and the related `references/` docs.
**Last updated:** 2026-08-26

---

## Purpose

This document tells the agent **what to establish and in what order** before offering advice, which questions are high-value, and which questions to skip.

**Operational posture:** The intake is a *prioritized draw list*, not a fixed script. The agent asks only what it does not already know and only when the answer would change the recommendation.

---

## 1. Age First — Always

**Age is the single field that cannot be deferred.** Resolve it before any advice or safety tiering.

### Rules

1. **If age is stated or clearly implied** in the parent's opening message (e.g., "my 15-month-old"), do not re-ask. Proceed — and **soft-anchor** it: infer an approximate DOB (≈ today − the stated age) and persist it marked `approximate` (see rule 6), so age derives correctly in later sessions instead of freezing at the number the parent happened to say.
2. **If age is not yet known**, ask it as the first question — brief and direct. Do not bundle it with other questions at this stage.
3. **Preterm infants:** If a parent mentions prematurity (born before 37 weeks), establish gestational age at birth so corrected age can be computed.
   - Corrected age = chronological age − weeks premature
   - Use corrected age for all safety tiering, detector gating, and developmental framing.
4. **Near the ~4-month boundary (corrected ~3.5–4.5 months):** Round to the conservative side — treat as under 4 months and apply the `<4mo` safety posture. When in doubt, ask the parent to confirm exact corrected age.
5. **Age determines tier:**
   - `< 4 months (corrected)` → newborn guardrail: safe-sleep essentials + brief active red-flag screening (1–2 questions) + state that behavioral optimization is out of scope for this age. No schedule advice.
   - `≥ 4 months (corrected)` → standard supported range. Passive red-flag detection + proceed with intake.
6. **Anchor on date-of-birth, not a month count.** A stated month count ("15 months") goes stale — the same child is 17 months two months later. Persist a DOB in the child's profile and let `scripts/analyze_sleep.py` derive current age from it every session. Two grades of DOB, tracked by `dob_precision`:
   - **Approximate** (soft anchor): inferred from a stated age (rule 1). Save with `scripts/experiment.py save-profile --dob <≈today−age> --dob-precision approximate`. Good enough to age correctly over time; treat as ±a few weeks.
   - **Exact**: a real birthday the parent gives. Save with `save-profile --dob YYYY-MM-DD` (default `exact`). **An exact DOB always supersedes and can never be overwritten by an approximate one** — once you have the real birthday, it wins in every downstream calculation. Preterm: also save `--gestational-weeks` so corrected age is derived.
   - **Boundary guardrail:** near the ~4-month tier line (rule 4), do NOT let an *approximate* DOB flip safety tiering or detector gating on its own — apply the conservative rounding and gently confirm the real birthday first. Away from that boundary (e.g. the 15-month case), approximate is fine to run with.
   - Never persist a bare month count as if it were durable.
   - **First-time notice:** memory is opt-in by default, but the first time you save for a new family, say so in one warm line and honor an opt-out — see `SKILL.md` Step 2 → "First-time memory notice & opt-out".
7. **Multiple children:** keep a **separate profile / state-dir per child** and confirm which child a concern is about before reasoning. Never let one child's age, constraints, or experiments bleed into another's.

---

## 2. Identify the Presenting Problem (§11 Step 2)

Before gathering details, confirm what the parent is actually trying to solve. Common goals:

- Early morning waking
- Bedtime resistance or long sleep-onset battles
- Frequent or long night waking / split nights
- Short naps
- Nap transition uncertainty
- Schedule fit under daycare or sibling constraints
- Illness, travel, or disruption recovery
- Independent settling / parental-presence decisions (→ methods, when-to-start, non-judgment: `references/sleep-training.md`)
- General "is this normal?"

The parent often names the problem. If their opening message is ambiguous, ask one brief clarifying question. Do not assume a goal and build an intake around the wrong one.

---

## 3. High-Value Context Fields — Prioritized Draw List

Pull from this list in priority order, **skipping any field already answered** in the parent's message. The goal is the smallest set of answers that changes the recommendation.

**Do not run through all of these sequentially.** Ask the top 1–3 that are still unknown and most load-bearing for the presenting problem. Revisit others only if the initial picture is ambiguous.

### Tier 1 — Almost always load-bearing

| Field | Why it matters |
|---|---|
| **Age** (and corrected age if preterm) | Safety tiering, developmental framing, detector gating. Already covered in §1 above. |
| **Rise time (usual vs. recent)** | Anchors the entire circadian rhythm picture; a shifted rise time changes every timing recommendation downstream. |
| **Bedtime (in-bed time vs. actual sleep onset)** | Distinguishes true sleep-onset delay from time-in-bed excess (relevant to bedtime fading, split-night, early waking). |
| **Settling method and who is present** | Required before any behavioral recommendation; determines what is changeable and what the family's preference is. |
| **Daycare / childcare nap schedule** (if relevant) | A fixed external constraint that overrides idealized advice (`constraint_first_recommending`). Ask early if daycare is in the picture. |

### Tier 2 — High value for most problems

| Field | Why it matters |
|---|---|
| **Nap timing, duration, and count** | Sleep pressure going into bedtime; nap-transition signals; short-nap interpretation. |
| **Night waking pattern** (count, timing, what helps the child settle back) | Distinguishes association-driven from need-driven or developmental waking. |
| **Duration of the current pattern** | A week vs. a month vs. "always been like this" changes both the diagnosis and what's realistic. |

### Tier 3 — Ask when the picture is still unclear

| Field | Why it matters |
|---|---|
| **Recent changes:** illness, congestion, teething, travel, developmental milestone (motor, language) | Temporal correlation narrows likely causes; may explain a short-lived disruption. |
| **Work / pickup time constraints** | Hard constraints on morning wake time change every downstream timing recommendation. |
| **Family preferences and what has already been tried** | Prevents recommending something the family has already rejected or is uncomfortable with. |

### What NOT to ask

- Do not turn this into a rigid 20-question intake. That posture is explicitly prohibited — it is alarmist, kills rapport, and often generates answers that do not change the recommendation.
- Do not ask about fields whose answers are already clear from context.
- Do not ask multiple questions in one message if the parent seems overwhelmed. One or two at a time is better rapport practice.

---

## 4. Constraint Elicitation Before Recommending

**Elicit hard constraints relevant to the presenting problem before the first concrete recommendation.** The aim is for the first plan to already be feasible — not to produce an idealized schedule that the parent then has to push back on.

The most common constraints to probe (only the ones that apply):
- Daycare nap schedule and pick-up time
- Parent work start time / morning departure
- Room-sharing or sibling arrangements
- Medical or feeding schedule (e.g., a child still on scheduled night feeds)

Ask these in the same natural turn as the Tier 1–2 fields above — not as a separate interrogation round. One brief, open-ended constraint question often suffices: "Before I suggest anything concrete, are there fixed times or arrangements I should work around — like a daycare schedule or work start time?"

---

## 5. Preterm and Corrected-Age Handling

When a parent mentions premature birth:

1. Ask gestational age at birth if not stated (e.g., "How many weeks early was she born?").
2. Compute corrected age = chronological age in weeks − (40 − gestational age at birth).
3. Use corrected age throughout — for safety tiering, developmental framing, detector interpretation, and all timing heuristics.
4. When near the 4-month corrected boundary, apply the conservative rounding rule: treat as `<4 months` if corrected age is between approximately 3.5 and 4.5 months and exact age is uncertain.
5. Note corrected age explicitly when presenting a recommendation, so the parent understands the framing.

---

## 6. Age-Tiered Safety Posture

The safety layer is passive for most conversations — it activates when a parent surfaces a symptom, or when a red flag appears in the parent's description. The one exception is the `<4mo` tier.

| Age tier | Posture |
|---|---|
| `< 4 months corrected` | **Active brief check (1–2 questions):** Confirm safe sleep environment (surface, position, absence of soft objects, room-sharing). If any red flag appears in the description (breathing, color, lethargy, feeding), halt schedule discussion and route to pediatrician. |
| `≥ 4 months corrected` | **Passive detection:** No routine medical screening questions. If the parent's description contains a red flag (breathing difficulty, unusual color, lethargy, dehydration signs, concerning episode), halt and route. Otherwise proceed with sleep-focused intake. |

Safe-sleep essentials (`safe_sleep_back_to_sleep`, `safe_sleep_firm_flat_surface`, `safe_sleep_bare_crib`) are worth briefly noting for any infant in the supported range — not preachy, just a sentence — because this is the highest-value preventable item and the agent may be the parent's only resource.

---

## 7. Intake Discipline — Summary Rules

1. **Age first.** Always.
2. **One or two questions per turn** for a parent who is overwhelmed or in a tense moment.
3. **Ask only what changes the recommendation.** If you can give useful guidance from what you have, do so — and leave an opening for more context if the parent wants to give it.
4. **Skip questions already answered** in the parent's message or earlier in the conversation.
5. **Elicit hard constraints before the first concrete recommendation.**
6. **Never run a rigid sequential 20-question intake.** This is an explicit prohibition.
7. **Presenting problem drives which fields you pull.** A bedtime-resistance question needs different detail than a nap-transition question.
8. **Meet the parent's vocabulary.** If they say "4-month regression," use that term as a bridge — do not correct it.

---

## 8. Developmental Context Framing

When intake reveals a recent change in sleep that coincides with a developmental period, frame it accurately:

- The 4-month shift is a genuine sleep-architecture change (`sleep_regression_reframe`).
- Motor milestones, language spurts, and separation anxiety are associated with temporary sleep disruption — this is a clinically observed pattern, not a guaranteed cause (`developmental_context_sleep_shifts`, labeled heuristic; for separation/attachment specifically, `separation_anxiety_sleep_disruption`, which also bridges the popular "8–10 month"/"18-month regression" vocabulary).
- Population-level age norms (AASM ranges, nap transition windows) are context, not targets. The child's own established pattern is the baseline (`individual_variability_baseline`).
- Wake windows are a rough orientation heuristic, not a clinical standard (`wake_windows_as_heuristic`). Do not tell a parent they made an error by falling outside a chart range.

---

## Cross-References

- Safety triage and red-flag list: `references/safety-triage.md`
- Developmental norms: `references/developmental-sleep.md`
- Myths and overclaims to avoid: `references/myths-and-overclaims.md`
- Interventions menu: `references/interventions.md`
- Relevant claim IDs: `safe_sleep_back_to_sleep`, `safe_sleep_firm_flat_surface`, `safe_sleep_bare_crib`, `individual_variability_baseline`, `wake_windows_as_heuristic`, `constraint_first_recommending`, `sleep_regression_reframe`, `developmental_context_sleep_shifts`
