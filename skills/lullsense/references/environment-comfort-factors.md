# Sleep Environment / Comfort Factors — Agent Reference

**Status:** Operational reference for the consultant skill. Cross-check any change against the claims in `knowledge/claims.yaml` and the related `references/` docs.
**Last updated:** 2026-09-02
**Scope:** 4–36 months. Below 4 months this reference does **not** apply — safe sleep + adequate feeding only (see `references/safety-triage.md`).

---

## Purpose

This is the **internal differential aid** behind Hypothesis #8, "Sleep environment / comfort mismatch" (`reasoning-framework.md` Step 5). It exists so the consultant can *conversationally surface 2–3 context-relevant environmental factors to observe or rule out* — feeding the Step 7 experiment loop and Step 8 metrics.

**This is not a user-facing checklist.** Never dump the list. Surface at most **2–3** factors, opt-in, worded as things to *observe*, and only when they fit the presenting picture. Each factor is a hypothesis against *this* child, not a verdict (same-presentation ≠ same-cause).

**How to read each factor:**
- **Claim anchor** — the `claims.yaml` ID that backs it, or `[heuristic]`/`[gap]` where evidence is thin.
- **Evidence-strength label** — stated honestly and carried into the phrasing.
- **Safe-sleep / `<4mo` gate** — hard boundaries that override comfort reasoning.
- **What to observe**, **smallest experiment + metric**, and a **conservative phrasing example**.

**Ordered by usable evidence strength: light > noise (safer-use) > noise (efficacy) > temperature > surface (safety-governed, not a lever).**

---

## 1. Light — dim/dark pre-bed (strongest, but caveated)

**Claim anchor:** `env_light_dim_pre_bed`
**Evidence-strength label:** **mechanistic, preschool-aged.** Even dim evening light suppresses melatonin in 3–5 yr-olds; the endpoints are circadian markers (melatonin/DLMO), **not** measured infant sleep. Cite as mechanistic support for a dim pre-bed environment — never as a proven sleep-quality gain in babies, and never with a lux number as a home threshold.
**Gates:** `<4mo` out of scope. No safe-sleep collision.

**What to observe:** brightness and screen/stimulation in the 30–60 min before sleep; whether the sleep space is dark; whether onset is harder on brighter evenings.

**Smallest experiment + metric:** dim the wind-down and darken the sleep space for several nights → watch **sleep-onset latency** (Step 8 metric) and settling ease.

**Conservative phrasing example:**
> "One low-cost thing to try: keep the last half-hour before bed dim and the room dark. The evidence here is more about how light affects the body clock than a proven sleep fix for babies, but it's easy to test — see if she settles any faster over a few nights."

**Do not:** state an "ideal" brightness/lux; claim proven onset/duration gains in infants; imply the preschool findings transfer unchanged to a baby.

---

## 2. Noise — safer use of sound machines (documented risk)

**Claim anchor:** `env_noise_safer_use`
**Evidence-strength label:** **documented.** Infant sleep machines can exceed recommended nursery sound limits, and prolonged/high-volume exposure carries hearing and neurodevelopmental concern (Öz & Demirci 2025 review, citing AAP Balk 2023 + De Jong 2024; Hugh 2014 device-output study). This is device output capability + risk, **not** observed hearing loss in a given child.
**Gates:** applies at any age a machine is in use (0–36mo). No safe-sleep surface collision.

**What to observe:** is a sound machine used? At what volume, and how close to the crib? Left on all night?

**Smallest experiment + metric:** if used, move it **across the room** (not next to the crib), **lower the volume**, and consider **time-limiting** it → this is a safety adjustment, offered whenever a machine is mentioned; no sleep-outcome metric is required.

**Conservative phrasing example:**
> "If you're using a sound machine — those can get louder than is ideal for little ears, so the safest way is low volume, across the room rather than by the crib, and not blasting all night."

**Do not:** quote a specific decibel reading for their device; assert hearing damage has occurred.

---

## 3. Noise — whether it *helps* sleep (weak / honest-limitation)

**Claim anchors:** `env_noise_onset_may_help` (onset/duration, weak, newborn/preterm-weighted) and `env_noise_efficacy_uncertain` (benefit limited, mostly newborn/hospital settings).
**Evidence-strength label:** **low.** White noise *may* speed onset or lengthen sleep a little for some babies, but the evidence comes from newborns and preterm infants in clinical settings (off our age band); effectiveness varies and long-term efficacy/safety isn't established, so it's best treated as a temporary, optional aid (Öz & Demirci 2025; Spencer 1990; Düken & Yayan 2024).
**Gates:** `<4mo` out of scope for behavioral framing. No surface collision.

**What to observe:** does the family already use white noise, and do they feel it helps? Is a very quiet room coinciding with hard onset?

**Smallest experiment + metric:** for a family already open to it, trial white noise at onset → watch **sleep-onset latency**. Keep it optional; don't insist either way.

**Conservative phrasing example:**
> "White noise is a maybe — some babies settle faster with it, but honestly the evidence that it improves sleep overall is weak. If it already helps you, keep it (at a safe volume); if not, there's no need to add it."

**Do not:** present white noise as a proven fix; tell a family they must use or must stop using it; extend the newborn onset finding to consolidation/duration.

---

## 4. Temperature — comfortable, not-overheated room (preference)

**Claim anchor:** `env_temperature_preference` — `[gap]`, no verified temperature→sleep-quality evidence.
**Evidence-strength label:** **low / parent-preference.** A comfortable, not-overheated room is a reasonable aim, but no verified evidence links a specific temperature to better sleep.
**Gates:** overheating is a **safe-sleep** matter → defer there, not a comfort target. `<4mo` out of scope for behavioral framing.

**What to observe:** does the parent describe the room as hot or stuffy? (Overheating/over-bundling → route to safe sleep.)

**Smallest experiment + metric:** if the room reads as hot/stuffy, a comfortable temperature and lighter layers is a gentle, preference-level adjustment → observe settling, but frame loosely.

**Conservative phrasing example:**
> "A comfortable, not-too-warm room is reasonable to aim for. There isn't good evidence pinning down an 'ideal' temperature, so I won't give you a number — mainly you want to avoid overheating, which is more of a safe-sleep point than a comfort tweak."

**Do not:** state an "ideal" nursery temperature or degree target; imply a temperature change will improve sleep quality as established fact.

---

## 5. Surface — **not a comfort lever** (safety-governed)

**Claim anchor:** `env_surface_comfort_defers_to_safety` → defers to `safe_sleep_firm_flat_surface` (never softened).
**Evidence-strength label:** **boundary, not a factor to optimize.** There is no evidence that a softer, inclined, or different surface improves sleep, and safe sleep always governs the surface.
**Gates:** hard safe-sleep override; `0–12mo` firm-flat-bare requirement.

**This is where the feedback's original "baby doesn't like this bed" example lands — and it is deliberately routed *out* of the comfort menu.** A baby who "only settles" on a soft, inclined, or different surface is a **settling-pattern** question (Hypothesis #4), never a reason to change the surface.

**What to do (acknowledge-don't-criticize, `consultant-persona.md`):** acknowledge the reality, gently hold the safe-sleep line, and redirect to the settling pattern — do **not** endorse or suggest a different surface.

**Conservative phrasing example:**
> "I hear you that she seems to settle better on the [soft/inclined] surface — that's really common. The thing I can't do is suggest moving her off a firm, flat crib surface, because that's the one safe-sleep point I won't bend on. Let's instead look at *how* she's being put down, which is usually what's really going on when a baby seems to 'only' settle one way."

**Do not:** suggest a softer/inclined/propped/different sleep surface for comfort; treat surface preference as an optimizable factor.

---

## Surfacing discipline (how this feeds the conversation)

- **Opt-in, brief.** Offer once — e.g. "want me to run through a couple of things worth ruling out?" — then surface only the 2–3 factors that fit. (`consultant-persona.md`, first-turn contract.)
- **One experiment at a time.** Each surfaced factor becomes one Step 7 change with a Step 8 metric; don't stack changes.
- **Label evidence every time.** Light = mechanistic/preschool; noise-efficacy + temperature = weak/preference; noise safer-use = documented; surface = safety, not comfort.
- **Individualize.** Present each as a hypothesis against this child, with what would confirm or disconfirm it — not a verdict.
