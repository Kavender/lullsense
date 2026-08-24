# Baby Sleep Specialist

An open-source Agent Skill that gives parents thoughtful, evidence-informed
baby/toddler sleep support through conversation — useful without any paid app,
tracker, or subscription. When sleep data is available, it adds inspectable,
provenance-tracked analysis.

> **More data improves the answer; data is never the price of admission.**

## Status

Pre-alpha. Building P0 phase-by-phase. See project scope in the maintainers' notes.

## Supported scope (first alpha)

- Ages **4–36 months** for behavioral/schedule support.
- Under 4 months: a **safe-sleep guardrail only** — safe-sleep essentials and
  red-flag screening, no schedule optimization.

## Safety & limitations

- This tool is **educational / general wellness**. It does not diagnose, treat,
  or prevent any disease or condition, and is not a substitute for a pediatrician.
- On any safety red flag it will **stop** sleep-optimization advice and direct you
  to appropriate medical care.
- Safety guidance is drawn from authoritative sources (AAP, AASM). Scheduling
  heuristics are labeled as heuristics, not clinical standards.
- **Known alpha limitation:** replies in non-English languages may include an
  un-reviewed machine translation of safety text (English original appended).

## License

Apache-2.0. See `LICENSE` and `NOTICE`. Contributions require a DCO sign-off
(`git commit -s`); see `CONTRIBUTING.md`.
