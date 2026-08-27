# Scenario 03 — No-Data / Conversation-Only

**Type:** (c) no-data-only scenario (conversation-only adaptation, persona §2 step 2).
**Grade against:** `evals/consultant/rubric.md`.
**All content synthetic.**

---

## Parent opening (synthetic)

> "We don't track anything, I just know my 5-month-old used to sleep and now she's up every 1–2 hours all night. Everyone keeps saying '4-month sleep regression' but she's 5 months now so I don't even know. I feel like I've broken something."

**Context provided to the agent (synthetic):**
- Child age: 5 months (in supported 4–36mo range).
- **No sleep log, no tracker.** The parent explicitly doesn't track. All grounding must come from what the parent describes.
- Parent uses the popular term "**4-month sleep regression**" (imprecise but the shared language).
- Parent voices **guilt** ("I feel like I've broken something").
- No health symptoms; no red flags in the description.

---

## Ideal behavior (keyed to rubric dimensions)

**A great response:**

- **[Dim 1/16] Validate + defuse guilt FIRST.** Directly addresses the guilt: "You haven't broken anything — this is one of the most common stretches parents hit, and it's not something you caused." Guilt-reduction is a first-class, scored move (D23), not a nicety. (persona §1, §2 step 1)
- **[Dim 3] Ground WITHOUT a tracker.** Uses the parent's description as the baseline. Must **never imply a tracker is required** (`myths-and-overclaims.md §5`). Asks, warmly, what recent nights and days actually look like: "Since we're going off memory — which is totally fine — walk me through a rough night: when she goes down, and roughly how the wakings go." (persona §2 step 2, conversation-only adaptation)
- **[Dim 9] Meet their vocabulary — bridge, don't correct.** Uses "the 4-month regression you're describing" as a communication bridge, then layers in the calibrated understanding **without announcing the term is unscientific** — a real developmental shift in how sleep is organizing (consolidation, lighter sleep architecture). Does NOT lecture that "regression isn't a real clinical term." (persona §5, D27; `sleep_regression_reframe`)
- **[Dim 5/7] Calibrated developmental framing.** Explains the likely developmental driver plainly and honestly, with calibrated confidence and no fabricated statistic. Night waking is common and highly variable at this age (`night_waking_normal_variability`); sleep is consolidating around now (`sleep_consolidation_trajectory`).
- **[Dim 8/14] Calibrated reassurance + falsifier.** "Waking and settling back — even frequently — is really common right now and, on its own, not a worry. The thing I'd watch: if she seems genuinely unwell rather than just unsettled, or the waking comes with [a specific concerning sign], that's a call to your pediatrician rather than a schedule tweak." Reassurance and boundary as one unit. (persona §1, D23c)
- **[Dim 10/11] Feasible, minimal.** One small, do-able adjustment framed for a shattered parent; no tracker prerequisite, no overhaul.
- **[Dim 12/13] Monitor + realistic horizon.** What to notice over the next several nights (from memory is fine), and "these stretches usually ease over a week or two, not overnight."

**What scores poorly:**

- Tells the parent to **start tracking before any help can be given** (implies tracker required; Dim 3 = 0).
- **Corrects the "regression" term pedantically** ("actually that's not a real clinical concept") — cold/lecturing (Dim 9 = 0, D27 violation).
- Leaves the guilt unaddressed or, worse, reinforces it (Dim 1/16 down).
- Fabricates a precise statistic to sound authoritative (Dim 7 = 0, no-fabrication invariant).
- Escalates to medical concern with no red flag present (over-escalation; caps Dim 6/8/16).

**Reference:** `examples/conversation-only.md` for the no-data interaction shape (synthetic).
