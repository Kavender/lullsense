# Changelog

All notable changes to LullSense (知眠) are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Sleep environment / comfort hypothesis (#8) with a new `E_environment`
  evidence layer.** The consultant can now conversationally surface 2–3
  context-relevant environmental factors (light, noise, temperature) to observe
  and rule out — never a checklist dump. Backed by a new evidence layer in
  `knowledge/sources.yaml` and `knowledge/claims.yaml` (light ×4, noise ×3),
  with evidence labeled honestly rather than dropped: light is mechanistic and
  preschool-aged, noise efficacy and temperature are low/preference-level, and
  noise safer-use (sound-machine output limits) is documented. The sleep
  **surface** is deliberately *not* a comfort lever — `env_surface_comfort_defers
  _to_safety` routes it to the firm-flat-bare safe-sleep requirement and never
  softens it. New `references/environment-comfort-factors.md`, Hypothesis #8 in
  `references/reasoning-framework.md`, an opt-in "quick rule-out" offer in
  `references/consultant-persona.md`, and consultant eval scenarios 09
  (factor surfaced conversationally) and 10 (surface safety override). All eight
  new sources are human-verified against the primary full-text PDFs (the four
  light circadian studies, Spencer 1990, the Öz & Demirci 2025 white-noise
  review, Düken & Yayan 2024, and Hugh 2014). The two originally-planned noise sources
  whose DOIs did not resolve (Riedy 2021, De Jong 2024) were replaced by the
  Öz & Demirci 2025 review, which synthesizes both — and the noise-efficacy
  claim was reworded to match what that review actually supports (limited,
  mostly newborn/hospital, short-term/variable) rather than a "very-low-GRADE"
  framing.

### Changed

- **Tagline reframed from claim to aspiration.** "…for every family" → "…built
  to reach every family," and both READMEs now name the real first-user ICP
  (technically comfortable parents, agent users, builders) rather than implying
  the experience is turnkey for everyone in this alpha.
- **README intros sharpened.** Both intros now make explicit that LullSense
  helps from conversation alone (no tracker required), remembers a child's
  context, and gets sharper with *recent* sleep history — while still described
  as an evidence-informed sleep consultant delivered as an Agent Skill.
- **Framing aligned across secondary surfaces.** The `pyproject.toml`
  description, the `skills/lullsense/README.md` intro, and the GitHub repo
  "About" now carry the same "sleep consultant, conversation-first, sharper with
  recent sleep history" wording.

### Fixed

- **Prediction now auto-pulls from a connected provider before falling back to
  age-only.** `references/sleep-timing-prediction.md` described mode selection
  passively and its worked examples closed by asking the parent to share a log —
  so the skill would give an age-only band and *offer* to pull instead of
  auto-pulling, contradicting `SKILL.md` Step 5c and `mcp-data-provider.md §5a`.
  The auto-pull step now lives at the decision point in §3, "age-only" is labeled
  the fallback, and the examples model auto-pull-first (with the offer-instead-of-
  pull case added as an explicit Wrong example).

## [0.1.0] — first public alpha

First public alpha. Educational and supportive only — LullSense never diagnoses,
and it runs safety triage before any sleep advice.

### Added

- **LullSense Agent Skill** — conversation-first baby/toddler sleep support
  (roughly 4–36 months). Gives real value from conversation alone; goes deeper
  when a sleep log is provided.
- **Safety triage, always first.** AAP-sourced red-flag recognition and
  escalation, a halt rule that stops sleep-optimization behind any red flag, and
  a newborn guardrail: for infants under 4 months no behavioral/schedule advice
  is given — only safe-sleep essentials, a brief screening, and routing to care.
- **Sleep analysis engine** (`lullsense-analyze`) — accepts typed notes, generic
  CSV/JSON, or an official Huckleberry CSV export. Raw logs are analyzed in memory
  and never written to disk.
- **Messy-data repair & detection** — handles no-end, overlapping, and
  forgot-to-stop sessions, with a confidence cap on low-quality logs.
- **Nap/bedtime predictor** — range-based (never a false-precision single time),
  heuristic wake-windows, with recent-window personalization; no clock times for
  infants under 4 months.
- **Local profile/constraint/experiment store** (`lullsense-experiment`) — a small
  per-child profile (date-of-birth so age never goes stale, durable constraints,
  experiment state) kept on your machine only. Memory is on by default, disclosed
  the first time it saves, and revocable at any time.
- **Documentation** — `README.md` / `README_ZH.md`, and `DATA_HANDLING.md`
  describing what is read, what is persisted locally, the AI-model boundary, and
  how to inspect or delete state.
- **CI and Release workflows** — lint/test on PRs; tagging `v*` builds and
  smoke-tests the wheel + sdist and attaches them to a GitHub Release (no PyPI).

[Unreleased]: https://github.com/Kavender/lullsense/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Kavender/lullsense/releases/tag/v0.1.0
