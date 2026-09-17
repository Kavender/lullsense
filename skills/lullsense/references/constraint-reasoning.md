# Constraint Reasoning — conflict checks, structural vs. behavioral debt, currency

**Loaded on demand** from `SKILL.md` Step 7 (respect constraints before recommending) and when a saved/loaded constraint exists.
**Terminating leaf** — provenance tags (e.g. `consultant-persona.md §3b`, `interventions.md §8`, claim ids) are attribution, not load-now instructions.

---

## `constraint_conflict` reasoning (realized here, not as code)

In Phase 3 the `constraint_conflict` signal was deferred as *code*; it is realized here as *reasoning*. It is a **recommendation-quality signal, not a disorder signal**. The job: catch, in conversation, that an idealized change collides with a saved hard constraint, and re-plan before speaking.

### The check (run before Step 6/7 output)

```
for each proposed_change under consideration:
    if proposed_change conflicts with any c in SavedConstraint set:
        mark proposed_change as forbidden
        re-plan: optimize only the movable variables
```

- **SavedConstraint set:** family constraints the user explicitly saved — retrievable via the local experiment store (`ExperimentStore.get_constraint(key)` → `SavedConstraint{key, value, note}`). Only *explicitly saved* constraints persist; raw logs stay ephemeral. Also honor constraints the parent states in the current conversation even if not yet saved.
- **Conflict = an idealized change that would require moving a fixed event.** Canonical example: with a saved daycare-nap constraint, "move daycare nap to noon" is a **forbidden_recommendation** — the nap cannot move. The eval encodes this: input has `daycare_nap_fixed: true`; expected signals include `constraint_conflict`; `forbidden_recommendations: [move daycare nap to noon]`.
- **Re-plan over movable variables only.** If the daycare nap is fixed and creates a long pre-nap awake stretch, do not "recommend the nap away." Instead adjust what *is* movable — morning wake time, bedtime, weekend nap timing, or pre-nap wind-down — and say plainly which variable is fixed and why the plan works around it. This is how the agent exceeds the "idealize → get rejected → adjust" default: the first plan offered is already feasible.
- **Never** frame the constraint as the parent's failing. Acknowledge the fixed reality, then optimize within it.

---

## Reality baseline vs. age-typical ideal; structural vs. behavioral debt

`constraint_conflict` above says *don't prescribe the blocked thing*. This section says what to do instead when a constraint has pushed the child's actual pattern away from the age-typical ideal: **name the shortfall as structural, reassure it isn't a failing, and optimize the movable levers with honest expectations.** Hold two numbers at once and reason from the gap.

- **Reality baseline** = what actually happens for this child — the predictor's personal wake-window/nap baseline, the review's per-child features. This is the truth to work from.
- **Age-typical ideal** = what the heuristics suggest — the age-band table, developmental norms. The predictor now surfaces this as `prediction.age_band_wake_window` (`{min, max}`) *alongside* the personal band, so reality-vs-ideal is visible.

### Classify the debt before recommending

When the reality baseline sits **worse** than the age-typical ideal (e.g. a much longer wake window, less total sleep), ask one question first: **is a hard constraint forcing it?** (Check loaded/elicited constraints.)

- **Structural (constraint-driven) debt** — imposed by an immovable constraint (fixed daycare nap, pickup, work, a sibling's schedule). It **cannot be scheduled away**; it can only be *mitigated* within the movable levers, and some shortfall remains while the constraint holds.
  - **Name it as structural, warmly** — this is the schedule the family is boxed into, not a parenting failure (acknowledge-don't-criticize; delivery in `consultant-persona.md §3b`).
  - **Do NOT prescribe the blocked ideal** (`constraint_conflict`) — no "switch to two naps" / "move the nap earlier" when daycare fixes it.
  - **Pivot to the movable levers** (`interventions.md §8`) and **calibrate expectations honestly**: mitigation reduces the overtired load; it won't fully erase structural debt while the constraint holds. Never over-promise.
- **Behavioral debt** — fixable by a change the family controls (bedtime drifted late, inconsistent routine). Unchanged: normal hypothesis ranking (Step 5) + smallest experiment (Step 7).

**The core failure to prevent:** misclassifying structural debt as behavioral → prescribing the blocked ideal → the parent feels unheard.

### Constraint-driven deviation as a signal — ask, never infer

A personal wake window that runs far longer than the age band is often the **fingerprint of a hard constraint**, not noise and not a problem to "fix" in the child. Read the gap against `prediction.age_band_wake_window` using two **tunable product heuristics** (not clinical cutoffs):

- **`DEVIATION_ASK_MULTIPLE ≈ 1.3×`** the age-band max → worth a targeted question.
- **`DEVIATION_STRONG_MULTIPLE ≈ 1.5×`** the age-band max → a strong constraint-fingerprint signal.

Then:

- If a **saved/durable constraint already explains it**, use it — apply the structural frame above.
- If **no constraint is on file**, **ask one targeted question** — *"is her nap timing fixed by daycare or an outside schedule?"* — and **do not assume a constraint exists.** Only after it's confirmed does the structural frame apply; otherwise the long window is behavioral (or simply this child's wide-but-fine pattern) and reasoning proceeds normally.
- **Review mode gets the same lens:** a persistent deficit that lines up with a fixed schedule is read as (confirmed) structural, not as a fixable regression.

### Constraints evolve — currency and transitions

A saved constraint is **last-known, not forever-true**; the reality baseline re-forms around changes. These are hard to auto-detect precisely — **confirm rather than assume.**

- **Currency check.** When a durable constraint is stale, or the reality baseline has clearly shifted, confirm it's still current before leaning on it (*"is her daycare schedule still the noon nap?"*). Don't silently trust a stale constraint.
- **Recognized transition events** (transient, schedule-shifting — do NOT persist; support through them like illness/travel, don't over-optimize, expect re-stabilization over days–weeks):
  - **Daycare start / ramp-up** — the first ~2–5 days (often part-time) before the schedule settles.
  - **Within-daycare program transition** — moving up a room/age group → new nap rules.
  - **Daycare-to-daycare switch** — an entirely new fixed schedule.
  - **Travel / time-zone change** — a temporary shift of the whole clock; pairs with the multi-day jet-lag roadmap (`consultant-persona.md §4`).
- **Change detection → confirm, then re-baseline.** A sudden reality-baseline shift that coincides with (or hints at) one of these → **ask** whether something changed; if yes, treat the current stretch as a transition (support-first), let the recent-window baseline re-form, and update/replace the saved constraint. The predictor's recent-days window and the review's drift lens already re-adapt the *numbers*; this adds the *interpretation* ("this looks like a schedule change, not a regression").
- **Honest limit.** Distinguishing ramp-up wobble from a new stable constraint from a behavioral regression is genuinely hard early — say so; watch over a couple of weeks rather than over-diagnosing the first few days.
