# Scenario 01 — Open-Ended Two-Week Review

**Type:** (a) open-ended two-week review (à la spec §15 / the Berry benchmark).
**Grade against:** `evals/consultant/rubric.md` (all 16 dimensions).
**All content synthetic.** No real family, no real data.

---

## Parent opening (synthetic)

> "Can you take a look at the last couple of weeks for us? Here's the log. I feel like things are just… off lately and I can't put my finger on it. She's 9 months. I'm so tired I'm probably missing something obvious."

**Context provided to the agent (synthetic):**
- Child age: 9 months.
- A two-week sleep log is attached (synthetic fixture). The salient pattern: total sleep and bedtime consistency look roughly stable, BUT over the **last 4–5 days the morning wake time has crept ~40 min earlier** than the child's own prior two-week baseline (e.g. ~6:40am → ~6:00am). Naps unchanged.
- No health symptoms mentioned. No red flags anywhere in the log or text.
- The parent has NOT labeled the problem; they only feel "off."

---

## Ideal behavior (keyed to rubric dimensions)

**A great response:**

- **[Dim 1] Validate first.** Opens by naming the exhaustion and the "can't put my finger on it" feeling before any analysis. "That fog where something's off but you can't name it is real — and it's not you missing something obvious." (persona §2 step 1)
- **[Dim 3] Ground in the child's OWN baseline.** Explicitly looks at the last two weeks *for this child* rather than a 9-month age chart. This is the differentiator vs. the Berry benchmark, which summarized totals and **missed the early-waking shift** (spec §15). The response should surface the ~40-min earlier wake against the child's prior baseline.
- **[Dim 5] Brief likely-cause first, then depth on engagement.** One or two plain sentences: "The thing that jumps out is she's been starting the day about 40 minutes earlier this past week than she was before." Offer the mechanism (early-waking drivers) only if the parent leans in — don't dump it. Consider more than one driver (too-late last nap, too-long day, early-morning light, sleep pressure) — `early_waking_common_causes`.
- **[Dim 6/15] Health awareness without over-screening.** No red flag is present, so the response stays **non-medical** and does not interrogate for symptoms. (Over-screening a benign review is itself a failure — persona §1, D22.)
- **[Dim 8/14] Calibrated + falsifier.** Reassures this is a common, adjustable shift AND names what would change the read: "If she also starts fighting the nap or seems wired rather than tired, that points to under-tiredness instead, and we'd go the other way."
- **[Dim 11/10] Minimal change + feasible.** Proposes ONE small experiment (e.g. nudge the last nap or bedtime, or address morning light) — not a schedule overhaul.
- **[Dim 12/13] Monitor + reassess.** Closes with what to watch (morning wake time, settling, late-afternoon mood) and a realistic horizon ("give it about a week; check back if the earlier wake hasn't budged by day 5").
- **[Dim 16] Tone.** Warm, concise, staged — not a wall.

**What scores poorly:**

- Summarizes total sleep and consistency and **declares things basically fine, missing the early-waking shift** (the exact benchmark failure — auto-low on Dim 3, and a proactive miss). 
- Dumps every possible cause of early waking at once (wall-of-analysis; caps Dim 1/5/16).
- Prescribes a full new schedule (violates Dim 11).
- Sprinkles medical disclaimers over routine advice with no red flag present (disclaimer spam; caps Dim 7/16).
- Asks a 20-question intake before saying anything useful (Dim 2 = 0).

**Fixtures:** a synthetic two-week log with the early-waking drift may be adapted from `evals/proactive/fixtures/early_waking.json`. Keep all values synthetic.
