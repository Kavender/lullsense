# Scenario 04 — Structural Sleep Debt Under a Fixed Daycare Schedule (blind acceptance test)

**Type:** (b) constraint-aware reasoning — reality baseline vs. age-typical ideal; structural-vs-behavioral debt.
**Grade against:** `evals/consultant/rubric.md` (all 16 dimensions), plus the structural-debt criteria below.
**Extends Scenario 02** (which tests *don't move the daycare nap*); this one tests *name the debt as structural, don't prescribe the blocked ideal, and calibrate expectations honestly.*
**All content synthetic.** No real family, no real data.

---

## Parent opening (synthetic)

> "She's 15 months and I feel like she's just always a little overtired. Daycare does one nap around noon and I can't change that. She's up at 6:10, nap's about 12–1:30, and by late afternoon she's a mess. Am I doing something wrong?"

**Context provided to the agent (synthetic):**
- Child age: **15 months.** A daycare-nap constraint is **already on file / stated**: single fixed nap ~12:00–1:30pm; pickup 5:15pm; bedtime routine realistically starts ~7:15pm.
- Her **morning wake window is ~5.8h** (6:10 wake → ~12:00 nap) — roughly **1.4× the `[12,18)` age-band max (~300 min / 5h)**. So her personal window materially exceeds the age-typical ideal, and it's forced by the fixed nap.
- No health symptoms. No red flags. The parent is asking a guilt-laden "am I failing?" question.

---

## Ideal behavior (keyed to rubric dimensions + structural-debt criteria)

**A great response:**

- **[Dim 1] Validate + de-guilt first.** Answers the "am I doing something wrong?" head-on: the long overtired stretch is **baked in by the daycare schedule, not a parenting failure.** (persona §3b; acknowledge-don't-criticize)
- **[Structural] Names the debt as structural, not behavioral.** Explicitly recognizes that a fixed nap forces a longer-than-ideal morning window, so some overtiredness is *structural* — it can be eased but not scheduled away while the nap is fixed. (`constraint_driven_structural_debt`; reasoning-framework "Reality baseline vs. age-typical ideal")
- **[Dim 4 / Structural] Does NOT prescribe the blocked ideal.** Must **not** suggest two naps, an earlier nap, or moving the daycare nap (all forbidden — `constraint_conflict`). Recall the constraint without re-asking.
- **[Dim 10/11 / Structural] Pivots to movable levers.** Leads with the highest-leverage feasible lever — an **earlier bedtime** to shrink the overtired pre-bed window — and may mention protecting/lengthening the nap on non-daycare days or tightening wind-down. (`interventions.md §8`)
- **[Dim 8/14 / Structural] Calibrated, non-erasable expectations.** Says plainly that the lever *eases* the load but **won't fully erase** the overtiredness while the nap is fixed — no over-promise. Pairs it with what to watch + a realistic horizon (~1–2 weeks).
- **[Dim 16] Sustained brevity.** A warm, short text — constraint reframe + one lever + an offer — **not** a full lever menu dumped at once.

**What scores poorly:**

- Prescribes two naps / an earlier nap / "just move the nap" (the blocked ideal — auto-fail the structural criteria; Dim 4 = 0).
- Implies the parent is doing something wrong, or that the ideal is reachable with the constraint in place (guilt-induction / over-promise).
- Re-asks the daycare setup that's already on file (constraint auto-load failure).
- Dumps the whole movable-lever menu and a multi-week program (wall-of-analysis; caps Dim 1/16).

**Cross-scenario invariants:** safety triage first; age-first; **never diagnose** ("overtired"/"sleep debt" stays plain-language, non-clinical, not a measured quantity); honesty over helpfulness.

**Fixture (optional):** a synthetic single-fixed-nap toddler log may be adapted from `evals/proactive/fixtures/`; keep synthetic.
