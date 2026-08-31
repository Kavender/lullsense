# Sleep-Timing Prediction — Predicting the Next Nap / Bedtime as a Calibrated Range

**Status:** Operational reference for the consultant skill. Cross-check any change against the claims in `knowledge/claims.yaml`, the timing table in `knowledge/sleep_timing_heuristics.yaml`, and the persona contract in `references/consultant-persona.md`.
**Scope:** 4–36 months for a predicted *time*. Below 4 months the newborn guardrail governs and no time is given (`references/safety-triage.md §4–§5`).
**Last updated:** 2026-08-29

> **A next-sleep time is always a RANGE, never a magic minute — and the child's tired cues outrank any clock.** Wake windows are a product heuristic, not a clinical standard; no peer-reviewed source publishes wake-window values (`wake_window_typical_by_age`, `sleep_timing_prediction_is_a_range`).

---

## 1. When to Trigger

Use this reference when the parent is asking, in effect, *"when is the next sleep?"* — for example:

- "When's the next nap?" / "When should bedtime be?"
- "How long can she stay up?" / "What's her wake window right now?"
- "When will she be tired again?" / "She just woke up — when do I put her down next?"

This is a forward-looking timing question. It is distinct from the reactive problem workflow (early waking, resistance, night waking — `references/reasoning-framework.md`) and from a proactive review (`references/reasoning-framework.md` → "Review mode"). Those may *lead into* a timing question, but this reference owns only the "next-event time" answer.

**Whole-day map is out of scope for now (Phase 1).** This predicts the **next single event**, not a full-day schedule. If the parent asks for a whole day laid out, give the next event and say plainly that a full-day map needs a sense of the child's typical nap lengths (logged or stated) — do **not** fabricate a multi-nap schedule from age alone. See §6.

---

## 2. Order of Operations — Safety, Then Age, Then Predict

The timing answer is gated. Run these in order; earlier steps stop later ones.

1. **Safety triage first** (`references/safety-triage.md`). A red flag halts sleep-optimization entirely — including timing (Prime Directive 2). A feverish, unwell, or breathing-labored child is a medical question first; do not answer "when's the next nap" over a live red flag.
2. **Establish age** (age-first, `references/conversational-intake.md §1`; corrected age for preterm, rounding conservatively near the ~4-month line).
3. **Then predict** — and only at or above 4 months does a predicted *time* exist at all.

### `< 4 months` → no predicted time (newborn guardrail)

For an infant under 4 months (corrected), **give no clock time and no schedule.** Sleep at this age is cue- and feed-driven, and a day-night circadian rhythm is only beginning to firm up around 3–4 months (`circadian_emergence_infancy`). Deliver only:

- **Cue-first orientation** — orient the parent to watching the baby's tired cues and feeding rhythm, not a wake-window clock.
- **Optional broad total-sleep normalcy range** — if it helps reassure, you may offer the wide *total-sleep-per-24h* range as a normalcy guide (cite `total_sleep_4_12_months` for 4–12 months context, applied here only as a broad "this much sleep across the day is typical" band, never as a schedule). Frame it as a range, not a target.
- **Safe-sleep essentials** (`references/safety-triage.md §5`) and routing of any concern.

Say warmly that structured timing coaching for this age is out of scope for now — this mirrors the newborn-guardrail scope boundary the whole skill holds.

**Synthetic (10-week-old, no clock time):**
> "At ten weeks, I'd steer you away from the clock entirely — her sleep is still driven by her cues and her feeds, and the day-night rhythm usually only starts to firm up around three or four months. So rather than a next-nap time, watch her cues, not the clock: the yawns, the stare-off, rubbing her eyes, going quiet — that's your signal she's ready. Over a full day babies this age still need a lot of sleep in total, in lots of short stretches, and that's exactly what you'd expect right now. Want me to run through the safe-sleep basics while we're here?"

Note there is **no HH:MM** anywhere in that answer. That is the guardrail working.

---

## 3. Mode Select — Personal Data vs. Age-Only

Once safety and age clear (≥ 4 months), choose the source of the estimate. Both produce a range; they differ in *width* and *basis*.

### Data present (log / store / MCP) → engine, personal baseline

If the parent has supplied a sleep log — typed notes, CSV, JSON, an official Huckleberry export — or a connected provider can furnish recent sessions, run the engine. It computes the child's own recent wake-window median and, if that pattern is stable, centers a **tighter** band on it:

```
lullsense-analyze --predict --last-wake HH:MM --target {nap|bedtime} \
    --format {manual|huckleberry|json} --input PATH \
    (--age-months N | --dob YYYY-MM-DD | a --state-dir with a saved profile DOB) \
    [--reference-date YYYY-MM-DD]   # required for --format manual \
    [--state-dir DIR]
```

`--last-wake HH:MM` (the time the child last woke) is **required** with `--predict`. The prediction is emitted as a top-level `prediction` block in the analysis JSON (§5). When the child's recent wake window is stable, the engine returns `basis: personal_baseline`, `confidence: moderate`, and a band centered on the child's own median — a precise, personal estimate.

### No engine / no data → read the heuristics table

With no engine installed and no data, do **not** guess a number. Read `knowledge/sleep_timing_heuristics.yaml`, find the row whose `age_band_months` contains the child's age, take that band's `wake_window_minutes` `{min, max}`, and **add both ends to the last wake time**. Present the resulting *wide* window — never a single time.

Worked example (age-only, conversational): a 7-month-old last woke at 07:00. The 6–9-month band is `wake_window_minutes: {min: 120, max: 180}` → 2h00m–3h00m awake → **next nap roughly 09:00–10:00**. That two-hour spread *is* the answer; its width is the honesty.

The table's wake-window and nap-length numbers are **practitioner heuristics** (`source_type: heuristic`), deliberately wide where consumer tables disagree; the `total_sleep_budget_hours` and `clinical_anchors` carry the sourced backing. Never launder a band edge into "the clinical wake window is X."

### 3.5 When a long personal window signals a constraint

The prediction now surfaces `prediction.age_band_wake_window` (`{min, max}`, the age-typical ideal) **alongside** the personal band — hold both. When the child's personal wake window runs **materially longer** than the age band, read it as a *possible constraint fingerprint*, not noise and not a problem to "fix" in the child. Two **tunable product heuristics** set the read (not clinical cutoffs): **≈1.3× the band max → worth a targeted question; ≈1.5× → a strong signal.**

**Ask, never infer.** If a saved constraint (a fixed daycare nap/pickup) already explains the long window, use it. If none is on file, **ask one targeted question** — *"is her nap timing fixed by daycare or an outside schedule?"* — before applying any structural framing; never assume a constraint exists. The full logic (structural vs. behavioral debt, currency, transitions) lives in `references/reasoning-framework.md` → "Reality baseline vs. age-typical ideal." This is interpretation, not a new number — the §4 rendering rules (range, basis, cues-win, first-turn brevity) still hold exactly.

---

## 4. Rendering Rules (Hard)

Every timing answer, whichever mode produced it, obeys all of the following:

- **Always a RANGE.** Never a single magic minute. Width encodes confidence: **wide** when the estimate is age-only, **tighter** when it comes from the child's own stable pattern.
- **State the BASIS in-line.** Say where the number came from in the sentence: *"from her age-typical rhythm"* (age-only) vs. *"from her own last ~N days"* (personal baseline). The parent should never have to ask whether this is about *their* child or a chart.
- **Always cues-win + heuristic tag.** Close every timing answer with the calibration: *a guide, not a fixed clock; her tired cues are the real signal; wake windows are a practitioner heuristic, not a clinical standard.* This is non-negotiable (`wake_window_typical_by_age`, `wake_windows_as_heuristic`, `myths-and-overclaims.md §1`).
- **First-turn brevity applies.** Turn one is a one-line answer plus an offer to go deeper — not the reasoning, not the table, not a full day. This is the *first-turn contract* (`references/consultant-persona.md §2`): a headline, then let the parent steer. Withhold the wake-window math, the band mechanics, and any schedule until they lean in.
- **Whole-day map out of scope.** If asked for a full day, give the *next* event and say a full-day map needs a sense of the child's typical nap lengths (logged or stated). Do not fabricate a multi-nap schedule (§6).

**Right (age-only, wide, one line + offer):**
> "Since she woke at 7, her next nap is likely somewhere in the **9 to 10** window — that's from her age-typical rhythm, so it's a wide guess, not a fixed time; her tired cues are the real signal. Want me to tighten that up if you can share a few days of her actual naps?"

**Right (personal baseline, tighter):**
> "From her own last week or so, her wake window's been running close to 2h15, so I'd watch for the next nap around **9:00–9:40** today — tighter because it's her own pattern, but still a guide, not a clock. Her cues win if she's telling you sooner."

**Wrong (magic time):**
> "Her next nap is at 9:17." *(A single minute implies a precision the evidence does not support — the exact failure `sleep_timing_prediction_is_a_range` exists to prevent.)*

**Wrong (no basis, no cues caveat):**
> "Next nap 9–10." *(No basis line, no cues-win tag — reads like a clinical schedule.)*

---

## 5. Reading the Prediction JSON

`lullsense-analyze --predict` emits a top-level `prediction` object (alongside `child`, `baseline`, `signals`, etc.). **Gate on `status` first:**

| `status` | What it means | How to render |
|---|---|---|
| `computed` | A range was produced (≥ 4 months, age band found) | Render the `next_event` window per §4 |
| `newborn_guardrail` | Child is under 4 months | Guardrail wording, **no time** — cue-first + optional normalcy line (§2) |
| `age_unknown` | Age missing / no band for this age | Fall back to conversation — ask age, or reason without a number |

When `status: computed`, read `next_event`:

- **`window_low` / `window_high`** (`HH:MM`) — the range to present. These are the answer; do not collapse them to `center` when speaking to the parent (`center` exists for internal reference only).
- **`basis`** — `age_only` or `personal_baseline`. This drives the in-line basis line (§4): `age_only` → "from her age-typical rhythm"; `personal_baseline` → "from her own last N days."
- **`confidence`** — `low` (age-only) or `moderate` (personal). Never `high`. A wider, lower-confidence band is stated as such, not sharpened.
- **`band_reason`** — plain-language why the band is wide or tight; useful raw material for the "why" *if the parent asks*, withheld on turn one.
- **`age_band_wake_window`** — `{min, max}` of the age-typical band (present whenever a band exists). It is the *ideal* to compare the personal band against for reality-vs-ideal reasoning (§3.5); an internal reasoning input, **never spoken as a target**.

**Optional normalcy line** — `prediction.budget` carries `total_sleep_low_h` / `total_sleep_high_h` (from the band's clinical anchor). Use it only if a total-sleep normalcy line would help; present it as a broad *per-24h* range, never as a schedule or a target. It is the same field that carries the guardrail's optional total-sleep line under `newborn_guardrail`.

**`caveats`** — the engine's own cues-win and heuristic caveats; surface them (they satisfy the §4 tag), do not drop them.

---

## 6. Whole-Day Map — Explicitly Out of Scope (Phase 1)

This predictor answers the **next event only.** A full-day schedule requires knowing how long each of the child's naps typically runs (which shifts bedtime and every subsequent window), and that is not derivable from age alone.

When a parent asks for a whole day:

1. Give the **next event** as a calibrated range (§4).
2. Say plainly that a full-day map needs a sense of the child's **typical nap lengths** — logged or stated — before it would be honest rather than invented.
3. **Do not fabricate** a multi-nap clock schedule from the age band. Offer to build toward it once the parent can share (or the log shows) real nap durations.

**Synthetic:**
> "I can give you the next one now — she woke at 7, so the next nap is likely around **9 to 10** from her age-typical rhythm. A full day laid out I'd rather not guess at, because it really depends on how long her naps actually run. If you can tell me roughly how long she naps, or share a few days, I can map the rest of the day with you instead of making it up."

---

## 7. Invariants for This Reference

- **Never diagnose, never a clinical schedule.** A predicted window is a scheduling guide, not a medical target; falling outside a band is not an error to correct in the child (`wake_windows_as_heuristic` `do_not_use_for`).
- **Wake windows are a product heuristic, not a clinical standard.** No clinical wake-window table exists (Galland 2012 confirms the literature is sparse); the bands in `knowledge/sleep_timing_heuristics.yaml` are practitioner heuristics, `evidence_level: low`.
- **Cues outrank the clock, always.** The child's own tired cues are the primary signal; the range is a secondary orientation.
- **Range, never a point; basis stated; cues-win tag every time; first-turn brevity.** These four are the load-bearing rendering rules (§4).

---

## 8. Cross-References

- Newborn guardrail + safe sleep (the `< 4mo` gate): `references/safety-triage.md §4–§5`
- First-turn contract, calibrated reassurance, delivery voice: `references/consultant-persona.md §1–§2`
- Wake windows as a heuristic; "regression" and overclaim guardrails: `references/myths-and-overclaims.md §1`
- The ten-step workflow and reading analysis JSON generally: `references/reasoning-framework.md`
- Nap-timing intervention (the reactive counterpart): `references/interventions.md §7`
- The age-band timing table this reference reads: `knowledge/sleep_timing_heuristics.yaml`
- Claims: `wake_window_typical_by_age`, `sleep_timing_prediction_is_a_range`, `wake_windows_as_heuristic`, `total_sleep_4_12_months`, `circadian_emergence_infancy` — all in `knowledge/claims.yaml`
