# Changelog

All notable changes to LullSense (知眠) are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Tagline reframed from claim to aspiration.** "…for every family" → "…built
  to reach every family," and both READMEs now name the real first-user ICP
  (technically comfortable parents, agent users, builders) rather than implying
  the experience is turnkey for everyone in this alpha.
- **Positioning reframed from "consultant skill" to "intelligence layer."** The
  README intros now lead with LullSense as an open-source baby sleep
  *intelligence layer* — turning a child's real sleep history, family context,
  and evidence into individualized guidance — rather than only a Q&A skill. The
  conversation-first, no-tracker-required, and optional-longitudinal-detection
  claims are preserved.

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
