# Memory & state protocol — profiles, constraints, and the memory preference

**Scope:** the mechanics of the local per-child store under `~/.lullsense/` — how to discover and load a saved profile, derive age from a stored DOB, persist profiles and durable constraints, and honor the on-by-default / opt-out memory preference. `SKILL.md` Step 2 holds the **binding rules**; this file holds the **procedure**. Load it only when you actually need to **save** a profile, **disambiguate** multiple children, or **handle an opt-out** — the common case (one returning family, one profile) needs just "load it, derive age, move on."

The store is readable/writable **with or without the engine** — the engine is never required just to remember a DOB or a daycare nap.

---

## 1. Discovery — finding the child at session start

When the caller didn't supply a `--state-dir`, look in the default root **`~/.lullsense/`**, which holds **one sub-directory per child** plus an optional `settings.json` memory preference.

**First check the memory preference** (`~/.lullsense/settings.json` → `memory`):
- **`disabled`** → this family opted out before. Run **session-only**, persist nothing, and don't show the first-time notice again.
- **otherwise** (the default — memory is on) → proceed:
  - **Exactly one** child dir → load it and use its DOB. (A light "just to confirm, this is about <name>?" is fine; do not re-ask the age.)
  - **Several** child dirs → ask which child this is about, then load that one.
  - **None** (first-ever contact) → ask age once, then **save** a profile (§3) under `~/.lullsense/<child-slug>/` so the next session remembers — and the first time you save, show the first-time notice (§4).

## 2. Reading a saved profile and constraints

**Profile:**
- **With the engine:** `lullsense-experiment --state-dir ~/.lullsense/<child> get-profile` → derive age from `dob`.
- **Without the engine:** read `~/.lullsense/<child>/profile.json` directly (fields: `name`, `dob`, `dob_precision`, `gestational_age_at_birth_weeks`) and compute whole months from `dob` to today yourself.

Once loaded, **silently use the DOB → current age and move on.**

**Durable constraints** (load right after the profile, so the skill is constraint-aware from turn one):
- **With the engine:** `lullsense-experiment --state-dir ~/.lullsense/<child> list-constraints` → an array of `{key, value, note}`.
- **Without the engine:** read `~/.lullsense/<child>/constraints.json` directly (same array).
- Treat a loaded constraint as **last-known, not forever-true** — confirm currency when it's stale or the child's actual pattern has clearly shifted (daycare ramp-up, a room move, a switch, travel); see `reasoning-framework.md` → "Constraints evolve." Transient context (travel, time-zone, illness) is used for the turn but **not** persisted.

## 3. Persisting the profile — anchor on DOB, never a month count

A month count is a snapshot that goes stale — a "15-month-old" is 17 months two months later. Persist a **DOB** in the child's profile and let `lullsense-analyze` derive current age from it every session:
```
lullsense-experiment --state-dir DIR save-profile --name NAME --dob YYYY-MM-DD [--dob-precision {exact|approximate}] [--gestational-weeks K]
```
- **Soft-anchor a one-time age mention.** If the parent only says "my 15-month-old", infer an approximate DOB (≈ today − the stated age) and save it with `--dob-precision approximate` — it will age correctly over time instead of freezing.
- **Exact always wins.** When the parent gives a real birthday, save it (default `exact`); an exact DOB **supersedes and is never overwritten by an approximate one** in any downstream calculation.
- **Safety boundary** (also stated as a binding rule in `SKILL.md` Step 2): near the ~4-month tier line, don't let an *approximate* DOB flip the safety tier on its own — round conservative and confirm the real birthday first.
- Never persist a bare month-count as durable.

## 4. First-time memory notice & opt-out (on by default, opt-out anytime)

Memory is on by default, so you may save the profile without asking — but the **first time you persist anything for a new family** (first-ever contact, no prior profile), add one short, warm line so it's never a surprise: *"I'll remember her birthday so you won't have to tell me next time — just say the word if you'd rather I didn't keep it."* Fold it into your normal reply inside the persona; it does **not** block the conversation and you still help immediately. Do this **once**, not every session — a returning family already has a profile, and an opted-out family (memory `disabled`) never sees it.

- **If the parent opts out** ("don't save that", "please don't keep her info"): turn memory off (`lullsense-experiment disable-memory`, or write `~/.lullsense/settings.json` = `{"memory": "disabled"}` directly), **delete anything you saved this session** (remove that child's `~/.lullsense/<child-slug>/` dir), confirm warmly ("Done — I won't keep anything. Tell me to remember again anytime."), and continue **session-only**. The opt-out is remembered across sessions; the only thing left on disk is that non-PII flag.
- **Re-enable on request** ("you can remember her again"): `lullsense-experiment enable-memory` (or set the flag back to `enabled`), then resume normal persistence.

Memory preference commands operate on the root `~/.lullsense` and take **no** `--state-dir`:
`lullsense-experiment memory-status | disable-memory | enable-memory`.

## 5. One child per profile / state-dir

If the family has more than one child, keep a **separate state-dir per child** and confirm which child each concern is about — never mix two children's ages, constraints, or experiments.

---

## Related
- `SKILL.md` Step 2 — the binding session-start rules this file details; and "State & retention" — what is/ isn't persisted.
- `DATA_HANDLING.md` — the user-facing account of what's read, kept, session-only, and how to delete it.
