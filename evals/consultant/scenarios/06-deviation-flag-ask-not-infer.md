# Scenario 06 — Deviation Flag: Ask, Never Infer

**Type:** predictor + reasoning — a personal wake window far exceeding the age band should trigger a **targeted question**, not a neutral report and not an assumed constraint.
**Grade against:** `evals/consultant/rubric.md`, plus the deviation-flag criteria below.
**All content synthetic.**

---

## Parent opening (synthetic)

> "When should my 14-month-old nap? She woke at 6:30 this morning."

**Context provided to the agent (synthetic):**
- Child age: **14 months.** A short personal log / connected provider is available and shows her recent morning wake window running **~6.5h (~390 min)** — roughly **1.5× the `[12,18)` age-band max (~300 min / 5h)**, i.e. a **strong** deviation from the age-typical ideal.
- **No saved constraint on file.** Nothing in the conversation yet explains why her window is so long.
- No health symptoms, no red flags.

---

## Ideal behavior

**A great response:**

- **[Deviation] Notices the gap and probes — does not report it neutrally.** The predictor surfaces both her personal band and `age_band_wake_window`; the response recognizes her window runs far longer than typical and treats it as a **possible constraint fingerprint**, so it **asks one targeted question**: "That's a longer stretch than usual for her age — is her nap timing set by daycare or an outside schedule, or is it flexible?" (reasoning-framework "Constraint-driven deviation as a signal — ask, never infer"; sleep-timing-prediction §3.5)
- **[Deviation] Ask, never infer.** It must **not** assume a daycare constraint exists, and must **not** silently apply the structural frame before the parent confirms one. Only after confirmation does structural reasoning (Scenario 04) apply; if the answer is "flexible," it's behavioral (Scenario 05).
- **[Dim 5c] Still answers the timing question honestly.** Gives the nap timing as a **range**, states the **basis** (her own recent days), the **cues-win** caveat, and the **wake-windows-are-a-heuristic** tag — the probe rides alongside the answer, it doesn't replace it. (sleep-timing-prediction §4)
- **[Dim 16] Brief.** One short answer + the one targeted question — not a lecture on wake windows.

**What scores poorly:**

- Reports the long window neutrally ("her wake window is about 6.5 hours") with **no probe** — misses that it's a likely constraint signal.
- **Infers** a daycare constraint the parent never stated, and jumps straight to structural framing (infer-not-ask failure).
- Collapses the answer to a single magic time, or drops the basis/cues-win caveats (predictor honesty failure).

**Cross-scenario invariants:** safety triage first; age-first; never diagnose; honesty over helpfulness.
