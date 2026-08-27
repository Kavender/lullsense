# Scenario 02 — Daycare Nap Constraint

**Type:** (b) daycare-constraint scenario (constraint-first recommending, D25).
**Grade against:** `evals/consultant/rubric.md`.
**All content synthetic.**

---

## Parent opening (synthetic)

> "My 16-month-old has been a nightmare at bedtime the last two weeks — takes forever to go down, then fights it, and he's crabby by dinner. He's at daycare all day. Just tell me what to do tonight, I don't have bandwidth for a project."

**Context provided to the agent (synthetic):**
- Child age: 16 months.
- In daycare full-time. The parent has NOT yet stated the daycare nap details — this is exactly the high-value constraint to elicit.
- Underlying (revealed if the agent asks): daycare runs **one fixed nap ~12:00–1:30pm, not movable**. Pickup is 5:15pm; bedtime routine can't realistically start before 7:15pm. So the pre-bed awake window is long.
- Parent has explicitly signaled **low bandwidth** ("just tell me what to do tonight").
- No health symptoms. No red flags.

---

## Ideal behavior (keyed to rubric dimensions)

**A great response:**

- **[Dim 1] Validate first.** "Bedtime battles when you're already fried at the end of the day are genuinely draining — let's get you something workable for tonight." (persona §2 step 1)
- **[Dim 2/4] Constraint-first, scoped.** Asks the *one or two* questions that actually change the plan — daycare nap timing/fixity and who does bedtime — and says why: "A couple of quick things so my suggestion actually fits your evening: is his daycare nap at a fixed time, and what time does bedtime realistically start?" It does **not** run a long intake. (persona §3, D25; `constraint_first_recommending`)
- **[Dim 4] Respect the fixed nap — first plan already feasible.** Once the fixed noon-ish nap is known, the recommendation must **not** touch the daycare nap (that's the forbidden move). It works within the constraint — e.g. an **earlier "rescue" bedtime** to shrink the overtired pre-bed window (parallels the Berry benchmark's earlier-bedtime rescue) — and checks feasibility against pickup/routine time rather than idealizing 7:00pm. (`daycare_schedule_alignment`)
- **[Dim 5] Likely cause, brief.** Names the probable driver plainly — a long awake stretch between a fixed early-afternoon nap and bedtime building sleep pressure and overtiredness → harder settling and crabbiness. Depth only if asked. (`wake_windows_as_heuristic` as a heuristic, not a rule)
- **[Dim 10/11] Minimal, feasible change.** ONE change tonight — e.g. bring bedtime forward ~20–30 min and tighten wind-down — not a multi-front overhaul. Respect the "just tell me tonight" bandwidth signal (progressive disclosure: offer the "why" but don't force it). (persona §2 step 4, §4)
- **[Dim 12/13/14] Monitor, reassess, falsifier.** Watch bedtime settling latency and evening mood; give it several nights, not one; and name the falsifier: "If he starts taking *ages* to fall asleep at the earlier time or seems under-tired, that means we went too far and we'd nudge back." (mirrors §15 "state evidence that would change its mind" — emerging under-tired behavior)
- **[Dim 16] Tone.** Warm, concise, honors low bandwidth.

**What scores poorly:**

- Recommends **moving or dropping the daycare nap** (the forbidden recommendation; Dim 4 = 0).
- Idealizes "put him down at 7:00" and only adapts after the parent objects (the idealize→reject→adjust anti-pattern, D25; caps Dim 2/4).
- Delivers a 5-step multi-week program to a parent who asked for tonight (Dim 11 low; ignores bandwidth signal; Dim 16 down).
- Over-medicalizes ordinary bedtime resistance at 16 months (over-escalation — caps Dim 6/8/16). Toddler bedtime resistance is developmentally common (`bedtime_resistance_toddler_autonomy`); absent a red flag it is a sleep question, not a medical one.

**Fixture (optional):** `evals/proactive/fixtures/` daycare-style logs may be adapted; keep synthetic.
