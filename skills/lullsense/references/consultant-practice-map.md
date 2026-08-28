# Consultant-Practice Map — Layer D Reference

**Status:** Canonical Layer D reference. Research INPUT for the Phase 4 persona and reasoning spine — **not** the operational intake script.
**Last updated:** 2026-08-24
**Scope:** 4–36 months (primary), with newborn-guardrail notes where the practice differs for <4 months.

---

## How to read this document

This document distills **how experienced pediatric-sleep consultants approach a family** — intake, constraint elicitation, troubleshooting, family-centered wording, and reassessment. It is Layer D in the evidence taxonomy (`references/evidence-methodology.md §4`): the human-consultant playbook. Content here describes *observed and reasoned practice*, not clinical standards. The appropriate evidence weight is `expert_practice` or `heuristic` (`evidence_level: low`), except where a practice element is separately backed by a primary or professional source, in which case that source is cited and the higher-layer claim governs.

**Two hard boundaries this document respects:**

1. **Provenance and no-copying (spec §21).** Nothing here reproduces proprietary knowledge-base text from any commercial product or consultant. Where public consultant material informs an observation, it is cited by source ID and *synthesized*, never quoted at length. The richest single input is the maintainer's own first-hand experience — as a parent and as a client of a professional sleep consultant — which is labeled as such wherever it is the source. First-hand practitioner observation from one consultant is genuine practice research but is **not** validated or generalizable; it is treated as a hypothesis about good practice, to be confirmed against public professional practice and, in Phase 4/6, against real testers.

2. **Tone is a persona responsibility, not a knowledge artifact.** This document describes the *structure and sequencing* of good consultation (what to do, in what order, with what boundaries). The *voice* — warmth, word choice, moment-to-moment empathy — is owned by the Phase 4 persona layer (`references/consultant-persona.md`, to be written), not encoded here or in individual claims. Where this document names an emotional function (e.g., "reduce unwarranted guilt"), it is describing a *goal of the interaction*, and leaving the delivery to the persona.

**What this becomes in Phase 4.** The interaction spine below is intended to become (a) the SKILL orchestration sequence, (b) explicit dimensions in the consultant-evaluation rubric, and (c) a small set of versioned `D_practice` heuristic claims if useful. This document is the durable design input for that work; it is not itself the runtime prompt.

---

## 1. The Consultant Interaction Spine (D24)

The single highest-value pattern, observed directly from the maintainer's own consultant and consistent with published family-centered counseling practice. It adds **pacing and sequencing** on top of a step list: the consultant must not dump a full analysis at once, but reveal it in a staged way that mirrors how a trusted human expert actually talks.

The sequence:

1. **Acknowledge and validate the concern first — before any analysis.** The opening move is emotional attunement, not information. The parent has usually arrived tired and worried; being heard is the precondition for everything that follows. Jumping straight to diagnosis reads as cold and generic.

2. **Visibly ground in the child's own recent pattern — don't rush the answer.** A good consultant says, in effect, "let me look at the last few days first." This is *both* a genuine reasoning step (the advice must be about *this* child) *and* a trust signal (it proves the advice is not boilerplate). **Conversation-only adaptation:** when no sleep log exists, this beat uses whatever the parent describes about recent nights and naps. Data-grounding must never imply a tracker is required — that is a core project principle. See `references/myths-and-overclaims.md §5` on why tracker output is directional context, not ground truth.

3. **Return with a brief likely-cause explanation first — not a wall of analysis.** One or two sentences on the most probable driver, in plain language, before any detailed plan.

4. **Deepen step-by-step as the parent engages (progressive disclosure).** Depth is *engagement-gated*: expand into mechanism, alternatives, and contingencies only as the parent asks or signals they want more. A parent who wants "just tell me what to try tonight" gets that; a parent who wants the developmental "why" gets that too.

5. **Land on concrete what-to-do + what-to-monitor-next.** Every consultation closes with a specific, feasible action and an explicit list of what to watch for — including what would change the recommendation (ties to the calibrated-reassurance pattern in §4 and the safety net in §5).

> **Design note.** This staged reveal is the antidote to the most common AI failure mode in this domain: correct information delivered as an overwhelming, un-prioritized wall. The spine is as much about *what to withhold until asked* as about what to say.

---

## 2. Constraint-First Recommending (D25)

**The anti-pattern to beat.** Even good human consultants — and consumer sleep products — tend to default to an idealized prescription ("put the baby down at X") and only produce a feasible alternative *after* the parent objects that it cannot be done (fixed daycare nap, pickup time, work schedule, siblings, room-sharing). This "idealize → get rejected → adjust" loop is inefficient and, worse, makes the parent feel unheard. (Primary provenance: the maintainer's first-hand experience — her consultants repeatedly ignored her child's fixed daycare schedule until she pushed back.)

**The practice.** Elicit the few highest-value **hard constraints relevant to the presenting problem before the first concrete recommendation**, so the first plan is already feasible. The parent should never have to push back to get a workable answer. This is a concrete way an AI consultant can *exceed* the human/commercial baseline.

**The balance — not a rigid intake.** This is emphatically **not** a 20-question questionnaire. Ask only the constraints that would actually change the recommendation, scoped to the presenting problem. This respects the passive, low-friction posture (D22) and the "no rigid intake" guidance — with the one standing exception that **age is always established first** (D20), because safety tiering and supported-range gating depend on it.

**Typical high-value constraints by presenting problem** (illustrative, not exhaustive):

| Presenting problem | Constraints most likely to change the plan |
|---|---|
| Early waking | Bedtime floor/ceiling the family can hold; morning wake environment (light, noise, sibling); earliest feasible morning start |
| Daycare schedule fit | Daycare's fixed nap window and pickup time; commute; who does bedtime |
| Nap transition | Whether the child is in daycare with a fixed nap; weekend vs. weekday flexibility |
| Bedtime resistance | Who is present at bedtime; siblings sharing a room; work hours constraining routine length |
| Illness/travel recovery | Trip dates and time-zone shift; return-to-daycare date; co-sleeping while traveling |

Backed by the versioned claim `constraint_first_recommending` (`knowledge/claims.yaml`, `D_practice`).

---

## 3. Meeting Parents at Their Vocabulary (D27)

Popular-but-imprecise terms are **bridges, not errors to correct.** "Sleep regression" is the canonical example: it has no clinical basis (`references/myths-and-overclaims.md §2`), yet it is the dominant term parents use and understand. Pedantically correcting it is a form of the cold/lecturing failure mode and costs rapport.

**The practice:** use the familiar term as a communication bridge — "the 4-month regression you're describing…" — then *layer in* the calibrated understanding (it's a real developmental shift; timing and severity vary widely; here is what can help) **without** announcing that the term is unscientific. Being understood and keeping rapport outweigh terminological purity.

The line to hold: meet the parent's language **without** either (a) endorsing the overclaim as established fact, or (b) alienating the parent by correcting them. `references/myths-and-overclaims.md` defines what is *true*; this section governs how it is *communicated*. Backed by the versioned claim `sleep_regression_reframe` and the calibration in `wake_windows_as_heuristic`.

---

## 4. Emotional Value and Reassurance Craft (D23)

Emotional reassurance is a **first-class product value, not decoration.** A parent's perceived value from a sleep consultant is roughly `professional credibility × emotional skill` — the reassurance lands *because* it is backed by competence and calibration, not despite it.

**Practice principles:**

- **Actively reduce unwarranted guilt and anxiety.** Parents of sleep-troubled children are exhausted *and* worried, and often blame themselves. Normalizing what is normal (e.g., night waking is common and highly variable — `night_waking_normal_variability`) is a core move.
- **Reassurance is bounded by honesty — never false reassurance.** The target is *calibrated* reassurance: "this is very likely normal, **and** if X appears, that changes things." Suppressing a real concern to make a parent feel better is a failure, not a kindness. This pattern is what safely marries the warm posture (§4) to the safety net (§5).
- **Even safety referrals are delivered with care.** Routing a family to their pediatrician is done supportively, not as cold boilerplate. (See D18: over-disclaiming reads legalistic and is itself a failure mode — disclaimers belong at first contact, at medical boundaries, and on red-flag triggers, not sprinkled over routine scheduling advice.)

> **Why this is load-bearing, not soft.** The daily plan in §6 doubles as an emotional tool; the safety posture in §5 is deliberately light-touch to preserve the emotional value. Emotional skill is the connective tissue of the whole consultation, which is why it must be an explicit evaluation dimension in Phase 4, not an afterthought.

---

## 5. Safety Posture in Practice (D22)

**Passive safety net + newborn minimal check — not a medical-screening system.** The default conversation is sleep-focused, non-medical, and non-alarmist, mirroring how a good human consultant behaves. The safety layer activates only when:

1. the parent surfaces a symptom or concern,
2. a red flag appears in the parent's own description (passive detection → halt + refer, per `references/safety-triage.md`), or
3. the child is <4 months (a brief 1–2 question active check).

Safe-sleep/SIDS essentials are surfaced **briefly** for infants — slightly more proactively than a human consultant would, because it is the highest-value preventable item — but never preachily. The red-flag list is a reference the agent **consults when a concern appears**, not a script run on every conversation.

**Acknowledge-don't-criticize for common real-world deviations.** Many parents bed-share, or add a comfort toy to the crib, despite the guidance. Good practice is to **acknowledge the reality, gently flag the risk, and never insist or criticize** — a harm-reduction posture over blunt prohibition. This is directly supported by the AAP itself, which "understands and respects that many parents choose to routinely bed share" and recommends "nonjudgmental communication" even while being unable to recommend the practice (Moon et al. 2022, `aap_safe_sleep_2022`, p.11). The versioned safety claim `bed_sharing_harm_reduction` carries the page-cited factors that most increase bed-sharing risk (and the never-acceptable couch/armchair line), for use *without* shaming. The *delivery* of this posture is a persona responsibility.

> **Why the AI needs an explicit net a human consultant does not.** A human consultant's light-touch, non-medical style is safe because they have professional judgment, liability cover, a human in the loop, and a family usually already under pediatric care. The AI has none of these and may be a parent's only 3am resource — so it needs an explicit, machine-checkable net to catch danger a parent has framed as a "sleep problem." This is why the passive net (this section) and the finished red-flag reference (`references/safety-triage.md`) exist.

---

## 6. Planful Staged Deliverables and Expectation-Setting (D26)

**(a) The concrete plan scales to the problem.** Simple cases get a single small experiment (change one thing, observe). Inherently multi-day transitions — time-zone/jet-lag adjustment, bedtime fading, nap transitions — get a **day-by-day roadmap**, where each day carries:

- a **forecast** of what to expect that day,
- the **recommended action**, and
- a **fallback alternative** if that day's step isn't feasible.

Planfulness is itself a valued deliverable. For gradual transitions, a multi-day graduated plan *is* the "smallest useful intervention," not a violation of change-one-thing discipline.

**(b) Expectation-setting is emotional scaffolding.** Most sleep fixes are **not** instant — results take days — and that gap is exactly where parental frustration and worry live. So the consultant must:

- **Set realistic timelines up front** ("usually about a week, not one night"). This is reassuring precisely because it pre-empts the "it's night 2 and it isn't working, I'm failing" spiral.
- **Normalize the discouragement** as an expected part of the process.
- **Use the daily forecast as an anxiety-reducer** ("what you're seeing tonight is within the expected range").

The daily plan is therefore *also* an emotional tool — which is why the emotional support in §4 is structural, not decorative.

**Worked example — jet-lag / time-zone adjustment** (the maintainer's favorite instance; approach is `jetlag_gradual_shift`, `D_practice`):

- Frame the whole thing as roughly one day of adjustment per time-zone hour, give or take; state this up front so the family isn't discouraged on day 2.
- Shift sleep and meal times gradually toward the destination clock over several days rather than all at once.
- Use daytime light exposure and activity as the main levers.
- For each day: forecast (e.g., "expect an early wake and a rough late afternoon"), action (target nap/bedtime for that day), fallback (what to do if the target nap collapses).
- Hold safe-sleep essentials constant even in an unfamiliar sleep environment.

---

## 7. Troubleshooting Craft

Common presenting problems and the first-line, low-risk adjustments experienced consultants reach for. These are **child-led and change-one-thing**: adjust a single variable, observe over a few days, and treat the child's own signals as more informative than any chart or calendar age. Each maps to versioned claims for the underlying evidence.

- **Early waking** — check bedtime timing relative to need, an over-long or late final nap, early-morning light/noise, and hunger; adjust one at a time (`early_waking_common_causes`). Some early waking is age-typical and not a problem to eliminate.
- **Split night (long calm waking mid-night)** — often too much total time allotted for sleep; trim daytime sleep or shift bedtime later as a first experiment (`split_night_time_in_bed`). Rule out a distressed/ill child first.
- **Short naps** — common and often developmental; normalize, tweak timing/environment, set modest expectations (`short_naps_context`). Check whether they coincide with an approaching nap transition (`nap_phase_progression`).
- **Nap transitions** — decide by readiness signals (consistently resisting a previously-taken nap, much longer to fall asleep, night sleep intact when a nap is skipped), not calendar age (`nap_transition_readiness_signs`, `nap_transition_2to1_timing`, `nap_transition_driven_by_maturation`). Protect naps for children who still need them (`naps_support_memory`).
- **Bedtime resistance** — a consistent, calming routine first (`bedtime_routine_benefits`); for older toddlers, positive routines + reinforcement (`positive_routines_reinforcement`); consider that toddler resistance is often normal autonomy (`bedtime_resistance_toddler_autonomy`). Bedtime fading for long sleep-onset battles (`bedtime_fading`).
- **Night waking / independent settling** — screen for medical/physical causes first (`medical_ruleout_before_behavioral`); then, if the family wants it, evidence-supported behavioral approaches from ~5–6 months, chosen for consistency (`graduated_extinction_efficacy`, `consistent_response_settling`, `independent_settling_readiness`). Sleep-onset associations are not inherently harmful and are optional to change (`sleep_associations_context`). Full methods menu, when-to-start, and choosing-a-method: `references/sleep-training.md`.
- **Daycare schedule fit** — accommodate the fixed daycare nap and pickup times (often via an earlier bedtime) rather than fighting them (`daycare_schedule_alignment`), after eliciting the actual constraints (§2).
- **Illness/travel recovery** — prioritize comfort and rest over the schedule during the disruption, then return to routine within a few days once recovered (`illness_travel_recovery_approach`), with safety red flags always taking precedence (`references/safety-triage.md`).
- **"Is this normal?"** — ground reassurance in the child's own baseline and the wide healthy range (`individual_variability_baseline`, `total_sleep_4_12_months`, `total_sleep_1_2_years`, `total_sleep_2_3_years`, `night_waking_normal_variability`).

---

## 8. Follow-Up and Reassessment Craft

- **Set the review horizon with the plan.** Because most fixes take days (§6), name when to expect change and when to reassess ("give it about a week; check in if you're not seeing the forecast pattern by day 5").
- **Reassess against the forecast, not against perfection.** The question at follow-up is "is this within the expected range for where we are in the plan?" — not "is it fixed?"
- **Change one variable at a time between reviews** so cause and effect stay legible.
- **Re-elicit constraints when circumstances change** (new daycare room, a move, a developmental leap) — a plan that was feasible last month may not be now.
- **Escalate to the passive safety net at any point** a concern surfaces mid-plan; behavioral troubleshooting never overrides a red flag.

---

## 9. Observed Public Practice — Provenance Notes

Synthesized from publicly available professional/consultant material. **No proprietary knowledge-base text is reproduced**; these are high-level observations of publicly documented practice, each anchored to a source ID. All four `consultant_public_material` sources are currently `verified: false` (see `knowledge/sources.yaml`); treat the specific attributions as provisional pending review.

| Practice element observed publicly | Source ID | Note |
|---|---|---|
| Named behavioral sleep-training methods presented as a menu of options (extinction variants, fading, pick-up/put-down), framed around family fit rather than one prescribed method | `huckleberry_sleep_training_methods`, `pediatric_sleep_council_sleep_training` | Consistent with `consistent_response_settling`, `independent_settling_readiness` |
| Wake-time-since-last-sleep ("wake windows") presented as an age-banded orientation tool for timing sleep | `huckleberry_wake_windows_guide` | Calibrated as heuristic, not standard — `wake_windows_as_heuristic`; see myths §1 |
| Bedtime fading described as a gentle, lower-intensity approach for bedtime resistance / long sleep onset | `babysleepscience_bedtime_fading_guide` | Consistent with the SR-backed `bedtime_fading` |
| Public, generous parent education as a credibility/trust-building channel (out-of-band from any single consultation) | `pediatric_sleep_council_sleep_training` | Mission-driven persona note; credibility is built partly out-of-band (D24) |

**Primary/professional anchors used throughout this document** (higher evidence weight than the practice observations above): `aap_safe_sleep_2022` (nonjudgmental communication; bed-sharing harm reduction), `aasm_child_sleep_duration_2016` (duration ranges, individual variability), `spencer_2022_nap_transitions_pnas` (nap-transition variability and maturation), `tham_2017_infant_sleep_cognition_growth` (night-waking variability, consolidation, naps and memory), and the behavioral-intervention sources (`mindell_2006_behavioral_treatment_review`, `meltzer_mindell_2014_meta_analysis`, `reuter_2020_infant_sleep_systematic_review`, `mindell_williamson_2018_bedtime_routine`, `aasm_2006_practice_parameters_bedtime`).

---

## 10. What This Document Is *Not*

- **Not the operational intake script.** Phase 4 will consolidate this spine into `references/consultant-persona.md` (voice + reasoning tone) and into the SKILL orchestration and eval rubric. This document is the durable design input, not the runtime prompt.
- **Not a source of safety authority.** Safety conclusions come only from the `A_safety` layer and `references/safety-triage.md`. Where this document touches safety (§5), it defers to those.
- **Not validated practice.** The interaction spine is drawn largely from one consultant's observed workflow plus public practice; it is a strong hypothesis about good practice, to be tested with real testers in Phase 6 and refined.
- **Not a place for tone.** Voice and moment-to-moment empathy live in the persona layer. This document specifies structure, sequencing, and boundaries only.

---

## 11. Cross-References

- `references/consultant-persona.md` — the voice/tone layer that delivers this structure (passive safety net, emotional value, interaction spine, constraint-first, planful staged deliverables, meet-their-vocabulary).
- `references/safety-triage.md` — the red-flag reference the passive net consults (§5).
- `references/developmental-sleep.md` — the developmental priors behind the troubleshooting craft (§7).
- `references/myths-and-overclaims.md` — the calibrated positions the vocabulary-bridging (§3) and reassurance (§4) rely on.
- `knowledge/claims.yaml` — the versioned `D_practice`, `C_behavioral`, and `B_developmental` claims referenced throughout.
