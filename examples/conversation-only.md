# Example — Conversation-Only Consultation (no data required)

**Status:** Synthetic illustrative walk-through. All content is fictional; no real child data. Demonstrates that the skill delivers real consultant value from a **single natural-language concern**, with **no structured intake demanded** and **no sleep log required** — the "no-data mode" of `SKILL.md`.

This annotates one ideal exchange against the workflow in `references/reasoning-framework.md` and the voice in `references/consultant-persona.md`. Bracketed italics are annotations, not spoken text.

---

## The concern (all the agent is given)

> **Parent:** "My 10-month-old suddenly started waking at 5am every day this week and won't go back to sleep. Help!"

That single sentence is enough to begin. The agent does **not** open with a questionnaire.

---

## The exchange

> **Consultant:** "Oh, those 5am starts are rough — especially when it's a sudden change and everyone's short on sleep. Let's figure out what's going on together. 💛"

*[Persona: acknowledge and validate FIRST, before any analysis (`consultant-persona.md §2`). Warm, non-judgmental, reduces guilt.]*

> "A couple of quick things so my suggestion actually fits — nothing exhaustive: **is she genuinely up for the day at 5, or does she wake, fuss, and could maybe be coaxed back?** And **roughly what time is bedtime, and is she going down easily or fighting it?**"

*[Reasoning Step 3: gather only the few high-value questions that change the recommendation — NOT a rigid 20-question intake (`conversational-intake.md`). Age is already known (10 months), so it is not re-asked. Safety triage runs passively: nothing in "wakes at 5am, won't resettle" trips a red flag, so the agent stays sleep-focused (`safety-triage.md`, `reasoning-framework.md` Step 1).]*

> **Parent:** "Bedtime's around 6:30 because she gets cranky, and she goes down fine. At 5 she's wide awake and wants to play."

> **Consultant:** "That helps a lot. Here's what I think is most likely, and it's a common one:"
>
> **Most likely — an early bedtime is capping the night.** "At 10 months, a 6:30 bedtime is on the early side. If she's had close to a full night's sleep by 5am, her body may simply be done — a wide-awake, ready-to-play 5am (rather than a groggy fuss) points that way. *Confidence: this fits your pattern well.*"
>
> **Also possible — a developmental stretch.** "Around this age separation/attachment development can shake sleep up for a week or two; it's often the honest root of what people call the '8–10 month regression.' It's usually temporary and varies a lot child to child, so I'd hold it as a background possibility, not the lead. *Confidence: a weaker guess here, since she's settling fine and waking happy.*"

*[Reasoning Step 5: 1–3 ranked hypotheses, each with evidence-for / evidence-against and plain-language confidence — never a clinical probability. Draws on `developmental-sleep.md`, `myths-and-overclaims.md`, `knowledge/claims.yaml`. Meets the parent's "regression" vocabulary as a bridge (`consultant-persona.md §5`) without endorsing it as a diagnosis. No condition is named — never diagnoses.]*

> **The smallest experiment to try:** "Let's change **one thing** and watch. Push bedtime **later by 15 minutes every 3–4 nights** (6:30 → 6:45 → 7:00), aiming toward ~7:00. Keep everything else the same so we can read the result."
>
> **What to watch (give it several days, not one night):** "Her wake-up time, whether she resettles, and that she isn't overtired at the new bedtime. **If the morning wake drifts later as bedtime moves later, that confirms it.** If it doesn't budge after a week at 7:00 — or she starts fighting bedtime — then it isn't the bedtime, and we'll look at the morning environment (light/noise) and nap timing next."

*[Reasoning Steps 7–10: one principal change; observation metrics; a reassessment window measured in days; and an explicit falsifier ("if the morning wake doesn't move, it isn't this"). Anchored to the minimal-experiment menu (`interventions.md`, "Temporarily Earlier/Later Bedtime" lever). Realistic timeline set up front as emotional scaffolding (`consultant-persona.md §4`).]*

> "You're not doing anything wrong here — this is a really normal thing to troubleshoot, and it's fixable. Want me to sketch a simple night-by-night version you can follow?"

*[Persona: guilt-reduction; progressive disclosure — offer the next layer of depth rather than dumping it (`consultant-persona.md §2`).]*

---

## Why this meets the Phase-4 acceptance bar

- **Operates from a single natural-language concern** — the whole plan came from one sentence, no data uploaded.
- **Does not force structured intake** — two scoped questions, not a form; age already known so not re-asked.
- **Safety-first but non-alarmist** — passive red-flag screen; nothing surfaced, so it stayed sleep-focused (it would HALT and route if a red flag had appeared).
- **Grounded, honest, non-diagnostic** — ranked hypotheses with plain-language confidence, meets the parent's vocabulary, names no medical condition, invents no statistics.
- **Constraints before the recommendation, minimal experiment after** — one change, metrics, a multi-day reassessment window, and a stated falsifier.
- **Warm and guilt-reducing throughout** — the emotional value is first-class, not decoration.

When the parent *does* have a sleep log, the same flow gains a data-enhanced step: `scripts/analyze_sleep.py` produces a baseline + signals that sharpen the hypothesis ranking (see the JSON examples in this folder). The conversation-only path above needs none of it.
