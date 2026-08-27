# Interventions — Agent Reference

**Status:** Operational reference for the consultant skill. Cross-check any change against the claims in `knowledge/claims.yaml` and the related `references/` docs.
**Last updated:** 2026-08-26

---

## Purpose

This document is the **minimal-experiment menu** (§11 Step 7). It lists the behavioral interventions the agent may recommend, each anchored to a verified `claims.yaml` claim ID where one exists, or explicitly labeled `[heuristic]` where none does.

**Minimal-change discipline (§11 Step 7, D26):** Prefer one principal change at a time. Recommend a second change only when safety or feasibility requires it, or when an inherently multi-step transition (bedtime fading, jet-lag adjustment, nap transition) makes a day-by-day plan the smallest useful experiment.

**Medical-first gate:** No behavioral intervention is appropriate until medical and physical causes (illness, pain, reflux, hunger) have been screened out. This is a hard prerequisite — see `medical_ruleout_before_behavioral` below.

---

## 0. Prerequisite — Medical Causes Screened First

**Claim:** `medical_ruleout_before_behavioral`
**Evidence type:** expert practice | **Evidence level:** moderate
**Source:** `aasm_2006_practice_parameters_bedtime`

Behavioral sleep approaches are appropriate only after ruling out illness, pain, reflux, and hunger. Crying at sleep time is a differential-diagnosis question first and a behavioral one second. If any of these causes are plausibly present, address them before selecting an intervention from this menu. See also `references/safety-triage.md`.

---

## Intervention Menu

### 1. Temporarily Earlier Bedtime

**Claim anchor:** `[heuristic]` — no single claim directly supports this as a standalone intervention. Grounded indirectly in `early_waking_common_causes` (bedtime timing as a contributor to early waking) and homeostatic reasoning per `wake_windows_as_heuristic`. **Labeled heuristic.**

**When to consider:** Child is accumulating sleep debt signs (overtired at bedtime, hard to settle, waking earlier than the family's goal), or the presenting pattern suggests insufficient overnight opportunity.

**What to try:** Shift bedtime earlier by 15–30 minutes for several nights. Do not shift so early that it curtails total sleep or conflicts with a daycare pickup constraint.

**What to observe:**
- Sleep-onset latency (does settling become faster or slower?)
- Morning wake time (does it shift later, stay the same, or come earlier?)
- Night waking count and duration
- Parent-reported daytime mood and energy

**Reassessment window:** 5–7 nights minimum. One night is not sufficient to assess a timing shift. If settling becomes consistently longer while morning wake time does not improve, earlier bedtime is not helping and may not be the right lever (§11 Step 10).

**Contraindication:** If a split-night pattern is present, consider whether total time-in-bed is already too long before moving bedtime earlier (see Intervention 6).

---

### 2. Bedtime Fading (Under-Tired Pattern)

**Claim anchor:** `bedtime_fading`
**Evidence type:** systematic review | **Evidence level:** moderate
**Sources:** `meltzer_mindell_2014_meta_analysis`, `babysleepscience_bedtime_fading_guide`

**When to consider:** Child resists sleep for a long time after being put down (prolonged sleep-onset latency), seems alert and not tired at the scheduled bedtime, or the family is experiencing a long, contentious bedtime battle each night. The pattern suggests bedtime is set earlier than the child's natural sleep-onset time.

**What to try:** Temporarily set bedtime at or close to the child's natural sleep-onset time (where they fall asleep without extended protest). Over several nights to a couple of weeks, gradually shift that bedtime earlier in small increments (15 minutes every few nights) toward the family's target time.

**What to observe:**
- Sleep-onset latency (should shorten within the first few nights)
- Bedtime protest duration and intensity
- Morning wake time and total overnight sleep (watch that total sleep is not curtailed)

**Reassessment window:** Allow at least 3–5 nights at the starting (faded-out) bedtime before beginning to shift earlier. Each 15-minute shift warrants another 3–5 nights of observation before the next increment.

**Note:** Bedtime fading is appropriate as a lower-intensity alternative when the family prefers not to use extinction-based approaches. It does not directly address night waking driven by causes other than bedtime timing.

---

### 3. Restore / Strengthen Consistent Bedtime Routine

**Claim anchor:** `bedtime_routine_benefits`
**Evidence type:** primary research | **Evidence level:** moderate
**Source:** `mindell_williamson_2018_bedtime_routine`

**Also relevant for older toddlers (18–36 months):** `positive_routines_reinforcement`
**Evidence type:** systematic review | **Evidence level:** moderate
**Source:** `mindell_2006_behavioral_treatment_review`

**When to consider:** Bedtime is inconsistent or has been disrupted (illness, travel, schedule change); the child shows resistance that may be partly a response to unpredictability; the family has never established a clear wind-down sequence.

**What to try:** Establish a consistent, calming pre-bed sequence of 3–5 steps in the same order each night (e.g., bath → pajamas → book → song → lights out). The content matters less than the consistency and predictability. For older toddlers (roughly 18 months+), simple reinforcement — verbal praise, a sticker chart — can be layered on top to reduce resistance (`positive_routines_reinforcement`).

**What to observe:**
- How quickly the child settles once the routine ends
- Bedtime resistance and protest duration
- Night waking frequency (routines are associated with fewer nighttime awakenings as well)

**Reassessment window:** 5–7 nights for a new routine to begin producing a visible settling pattern. Routine benefits accrue over time; do not judge after one or two nights.

**Note:** Prescribing a specific routine length or set of steps as required is not supported. The family should choose steps they can apply consistently.

---

### 4. Modify Parent Response / Check-In Approach (Consistent with Family Preference)

**Claim anchor (core evidence):** `graduated_extinction_efficacy`
**Evidence type:** systematic review | **Evidence level:** high (source verification pending — see `claims.yaml` header note)
**Sources:** `mindell_2006_behavioral_treatment_review`, `meltzer_mindell_2014_meta_analysis`, `reuter_2020_infant_sleep_systematic_review`

**Also relevant:** `consistent_response_settling`
**Evidence type:** expert practice | **Evidence level:** moderate
**Sources:** `mindell_2006_behavioral_treatment_review`, `huckleberry_sleep_training_methods`

**Also relevant (safety context):** `behavioral_interventions_safety`
**Evidence type:** systematic review | **Evidence level:** moderate
**Sources:** `reuter_2020_infant_sleep_systematic_review`, `gradisar_2016_infant_sleep_rct` (RCT measuring infant cortisol + attachment; no adverse effect found — "in studied populations")

**Age floor:** Not appropriate below approximately 5–6 months (developmental readiness convention; the exact lower bound is a clinical-readiness heuristic, not established by the systematic-review sources — see `graduated_extinction_efficacy` note in `claims.yaml`).

**When to consider:** The family wants to change the child's independent settling ability or reduce nighttime waking driven by learned sleep-onset associations. The family has a preference — or can be helped to choose — a method they can apply consistently. Medical causes have been excluded.

**What to try:** Choose a check-in approach that fits the family's comfort level. The spectrum includes:
- More presence: parent stays in the room but reduces active soothing over several nights
- Check-in with graduated intervals: parent checks in at progressively longer intervals without fully settling the child (the "graduated extinction" or Ferber-style approach)
- More independence: parent does not return after a consistent goodbye unless a distress signal warrants it

**The critical principle (`consistent_response_settling`):** Consistency across nights matters more than which specific method is chosen. Switching methods nightly tends to produce worse outcomes than a less optimal but consistently applied method.

**What to observe:**
- Bedtime crying / protest trajectory (expect variability across the first several nights; improvement is not linear)
- Sleep-onset latency
- Night waking frequency and whether the child needs active settling to return to sleep

**Reassessment window:** Most methods require 1–2 weeks of consistent application before a reliable pattern is visible. Two nights of data is insufficient. Set the expectation explicitly: "You're likely to see variability in the first few nights; the signal is the trajectory across a week."

**Family autonomy note:** There is no obligation to sleep-train. If the family's preference is to continue attending to the child, validate that and focus on other levers (`independent_settling_readiness`). Safety evidence does not show lasting harm from standard methods in appropriate-age children (`behavioral_interventions_safety`), but that evidence does not obligate any family to use them.

**Separation-anxiety phase note:** When night waking or bedtime protest coincides with a separation-anxiety phase (commonly around 9 months, sometimes recurring in the toddler year), favor a responsive, continuity-first response — brief, calm, consistent reassurance is developmentally appropriate, not a harmful habit (`responding_to_separation_protest`) — and weigh timing before starting a *new* extinction program, since starting mid-phase is often harder and a mid-phase worsening may reflect the phase rather than method failure (`sleep_training_timing_developmental`). Full topic: `references/sleep-training.md` and `references/developmental-sleep.md §6`.

The full methods menu (extinction, graduated/Ferber, camping-out/chair, pick-up-put-down, gentle/no-cry), when-to-start guidance, and choosing-a-method framing are in `references/sleep-training.md`.

---

### 5. Manage Non-Urgent Comfort or Environment Issues Before Bedtime

**Claim anchor:** `[heuristic]` — no single claim directly covers environment management as a standalone intervention. Grounded in `medical_ruleout_before_behavioral` (screen physical causes) and `early_waking_common_causes` (light, noise as early-waking contributors). **Labeled heuristic.**

**When to consider:** Environmental factors plausibly contribute to the presenting problem: early-morning light waking up the child, noise triggering night waking, a room that is too warm or too cold, or non-urgent physical discomfort (teething, congestion, minor GI) that may be addressed with standard comfort measures before bedtime.

**What to try (prioritize before behavioral interventions):**
- Blackout curtains or window coverings if early-morning light appears to be causing early waking
- White noise machine if household or external noise coincides with wake events
- Comfortable room temperature (a rough population heuristic is ~68–72°F / 20–22°C, though this is not a validated clinical standard — **[heuristic]**)
- Pre-bedtime comfort measures for teething or minor congestion where appropriate and consistent with pediatric guidance

**What to observe:**
- Whether the specific suspected environmental trigger is associated with wake events
- Sleep-onset and night-waking pattern after the change

**Reassessment window:** 3–5 nights to isolate the effect of an environmental change. If the problem persists unchanged after the environmental factor is addressed, it is unlikely to be the primary driver.

**Important:** If congestion is severe, there is a fever, or other illness signs are present, halt behavioral advice and check safety triage first.

---

### 6. Stabilize Morning Wake Time and Environmental Cues

**Claim anchor:** `[heuristic]` — no single claim directly supports morning-anchor stabilization as a standalone intervention. Grounded in circadian biology described in `references/developmental-sleep.md §1` and the early-waking heuristic in `early_waking_common_causes`. **Labeled heuristic.**

**When to consider:** The child's schedule is drifting (later bedtimes leading to later rises, or chaotic day-to-day timing); the family wants to shift the schedule direction; early waking is the presenting problem and other levers have been tried.

**What to try:**
- Hold the morning wake time consistent within a 30-minute window, even on weekends, to stabilize the circadian anchor.
- Use morning light exposure (brief time in a bright room or outdoors) to reinforce the biological clock signal.
- Where a daycare schedule imposes a fixed rise time, use that as the anchor and adjust bedtime to protect total sleep.

**What to observe:**
- Whether the sleep-wake schedule stabilizes over the following week
- Effect on bedtime (a consistent morning often pulls bedtime earlier organically)
- Morning wake time trend

**Reassessment window:** Circadian shifts are slow. Allow 1–2 weeks before assessing whether the anchor is holding.

---

### 7. Nap Timing Adjustment (Short Naps, Under-Tired Pattern)

**Claim anchor:** `wake_windows_as_heuristic`
**Evidence type:** heuristic | **Evidence level:** low
**Source:** `huckleberry_wake_windows_guide`

**Also relevant:** `short_naps_context` (heuristic), `nap_transition_readiness_signs` (heuristic)

**When to consider:** The child's nap timing appears systematically misaligned with their sleep pressure (put down too soon and taking a long time to settle, or falling asleep too easily at the wrong time and then waking early from the nap). May also be relevant when short naps or bedtime resistance suggests the nap-to-wake interval going into bedtime is too short.

**What to try:** Shift nap start time by 15–30 minutes in the direction indicated by the pattern (earlier if child seems overtired by nap time; later if child seems insufficiently tired). If short naps coincide with nap-transition readiness signs, consider whether this is the right moment to begin a gradual nap transition rather than trying to extend the nap.

**What to observe:**
- Nap duration after the timing shift
- Ease of nap settling
- Bedtime timing and sleep-onset latency (nap timing affects evening sleep pressure)

**Reassessment window:** 3–5 days per incremental timing change.

**Calibration note:** Wake windows are a rough orientation heuristic, not a validated clinical standard (`wake_windows_as_heuristic`, `myths-and-overclaims.md §1`). Use the child's own tired cues and historical pattern alongside elapsed time. Do not tell a parent they made an error by falling outside a chart range.

---

## Selecting the Right Lever — Quick Decision Guide

| Presenting pattern | Primary lever to consider | Claim anchors |
|---|---|---|
| Long sleep-onset battle, child alert at scheduled bedtime | Bedtime fading | `bedtime_fading` |
| Inconsistent or recently disrupted routine | Restore consistent routine | `bedtime_routine_benefits`, `positive_routines_reinforcement` |
| Night waking tied to parental settling (association-driven) | Modify parent response | `graduated_extinction_efficacy`, `consistent_response_settling` |
| Early morning waking, suspect light / noise | Environment management | heuristic |
| Chaotic schedule or circadian drift | Stabilize morning anchor | heuristic |
| Apparently under-tired at bedtime, or under-tired at nap | Nap timing adjustment | `wake_windows_as_heuristic` (heuristic) |
| Signs of accumulated sleep debt | Earlier bedtime | heuristic |

---

## Change-One-Thing Discipline (§11 Step 7)

- Recommend **one principal change** per experiment unless safety or feasibility clearly requires otherwise.
- Exception: inherently multi-step transitions (bedtime fading over several weeks, jet-lag recovery, nap transition) are themselves the smallest useful experiment; a day-by-day plan for these is not a violation of this rule (D26).
- When recommending a change, always pair it with:
  1. **What to observe** — the 2–3 metrics that will tell the family whether it is working.
  2. **A realistic reassessment window** — typically several days, not one night.
  3. **What would change the conclusion** — make the experiment falsifiable (§11 Step 10).

---

## Cross-References

- Medical screening and safety triage: `references/safety-triage.md`
- Intake and constraint elicitation: `references/conversational-intake.md`
- Developmental norms: `references/developmental-sleep.md`
- Overclaim guardrails: `references/myths-and-overclaims.md`
- All claim IDs: `knowledge/claims.yaml`
- Decisions: D26 (planful staged deliverables), §11 Steps 7–10
