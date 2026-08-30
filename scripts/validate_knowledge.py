"""Validate skills/lullsense/knowledge/claims.yaml and skills/lullsense/knowledge/sources.yaml against the schema
defined in skills/lullsense/references/evidence-methodology.md.

Exit code 0 = valid, 1 = errors found. Safety rule (S2) is enforced hard.
Warnings are advisory and do NOT affect the exit code.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import yaml

EVIDENCE_TYPES = {
    "guideline", "professional_consensus", "systematic_review",
    "primary_research", "expert_practice", "heuristic",
}
EVIDENCE_LEVELS = {"high", "moderate", "low"}
LAYERS = {"A_safety", "B_developmental", "C_behavioral", "D_practice"}
VARIABILITY = {"high", "moderate", "low"}
SOURCE_TYPES = {
    "guideline", "consensus_statement", "systematic_review",
    "primary_research", "review", "consultant_public_material",
}
PARENT_GOALS = {
    "early_waking", "bedtime_resistance", "night_waking", "split_night",
    "short_naps", "nap_transition", "daycare_schedule_fit",
    "illness_travel_recovery", "independent_settling", "is_this_normal",
}
SAFETY_OK_EVIDENCE = {"guideline", "professional_consensus", "systematic_review"}

CLAIM_FIELDS = {
    "claim_id", "layer", "topic", "parent_goals", "age_range_months",
    "evidence_type", "evidence_level", "claim", "sources", "use_for",
    "do_not_use_for", "individual_variability", "last_reviewed",
}
SOURCE_FIELDS = {
    "id", "organization", "title", "url", "source_type", "verified", "last_accessed",
}

HEURISTIC_FIELDS = {
    "age_band_months", "wake_window_minutes", "typical_nap_minutes",
    "expected_nap_count", "total_sleep_budget_hours", "source_type",
}
_MINMAX_KEYS = {"min", "max"}


def validate_heuristics(path: Path) -> list[str]:
    rows = _load(path)
    errors: list[str] = []
    for i, r in enumerate(rows):
        tag = f"heuristic[{i}]"
        missing = HEURISTIC_FIELDS - set(r)
        if missing:
            errors.append(f"{tag}: missing fields {sorted(missing)}")
            continue
        ab = r["age_band_months"]
        if (not isinstance(ab, list) or len(ab) != 2
                or not all(isinstance(x, int) for x in ab) or not (0 <= ab[0] < ab[1])):
            errors.append(f"{tag}: bad age_band_months {ab!r}")
        for key in ("wake_window_minutes", "typical_nap_minutes",
                    "expected_nap_count", "total_sleep_budget_hours"):
            mm = r[key]
            if (not isinstance(mm, dict) or set(mm) != _MINMAX_KEYS
                    or not all(isinstance(mm[k], (int, float)) for k in _MINMAX_KEYS)
                    or mm["min"] > mm["max"]):
                errors.append(f"{tag}: bad {key} {mm!r}")
        if r["source_type"] != "heuristic":
            errors.append(f"{tag}: source_type must be 'heuristic' (got {r['source_type']!r})")
    return errors


def _load(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or []


def _validate_sources(sources) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    ids: set[str] = set()
    for i, s in enumerate(sources):
        tag = f"source[{i}]"
        missing = SOURCE_FIELDS - set(s)
        if missing:
            errors.append(f"{tag}: missing fields {sorted(missing)}")
            continue
        if s["id"] in ids:
            errors.append(f"{tag}: duplicate id {s['id']!r}")
        ids.add(s["id"])
        if s["source_type"] not in SOURCE_TYPES:
            errors.append(f"{tag} {s['id']}: bad source_type {s['source_type']!r}")
        if not str(s["url"]).startswith("http"):
            errors.append(f"{tag} {s['id']}: url must be http(s)")
        if not isinstance(s["verified"], bool):
            errors.append(f"{tag} {s['id']}: verified must be bool")
    return errors, ids


def _validate_claims(claims, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for i, c in enumerate(claims):
        tag = f"claim[{i}]"
        missing = CLAIM_FIELDS - set(c)
        if missing:
            errors.append(f"{tag}: missing fields {sorted(missing)}")
            continue
        cid = c["claim_id"]
        if cid in seen:
            errors.append(f"{tag}: duplicate claim_id {cid!r}")
        seen.add(cid)
        if c["layer"] not in LAYERS:
            errors.append(f"{tag} {cid}: bad layer {c['layer']!r}")
        if c["evidence_type"] not in EVIDENCE_TYPES:
            errors.append(f"{tag} {cid}: bad evidence_type {c['evidence_type']!r}")
        if c["evidence_level"] not in EVIDENCE_LEVELS:
            errors.append(f"{tag} {cid}: bad evidence_level {c['evidence_level']!r}")
        if c["individual_variability"] not in VARIABILITY:
            errors.append(f"{tag} {cid}: bad individual_variability")
        ar = c["age_range_months"]
        if (not isinstance(ar, list) or len(ar) != 2
                or not all(isinstance(x, int) for x in ar)
                or not (0 <= ar[0] <= ar[1])):
            errors.append(f"{tag} {cid}: bad age_range_months {ar!r}")
        for g in c["parent_goals"]:
            if g not in PARENT_GOALS:
                errors.append(f"{tag} {cid}: unknown parent_goal {g!r}")
        for sid in c["sources"]:
            if sid not in source_ids:
                errors.append(f"{tag} {cid}: source {sid!r} not in sources.yaml")
        if not isinstance(c["last_reviewed"], date):
            errors.append(f"{tag} {cid}: last_reviewed must be a YYYY-MM-DD date")
        is_safety = c["layer"] == "A_safety"
        if c["evidence_type"] == "heuristic":
            if is_safety:
                errors.append(f"{tag} {cid}: heuristic may NEVER back an A_safety claim")
            if c["evidence_level"] != "low":
                errors.append(f"{tag} {cid}: heuristic must be evidence_level low")
        if is_safety:
            if c["evidence_type"] not in SAFETY_OK_EVIDENCE:
                errors.append(
                    f"{tag} {cid}: A_safety needs evidence_type in {sorted(SAFETY_OK_EVIDENCE)}")
            if c["evidence_level"] != "high":
                errors.append(f"{tag} {cid}: A_safety must be evidence_level high")
            if not c["sources"]:
                errors.append(f"{tag} {cid}: A_safety must cite >=1 source")
    return errors


def validate(claims_path: Path, sources_path: Path) -> list[str]:
    sources = _load(sources_path)
    claims = _load(claims_path)
    src_errors, source_ids = _validate_sources(sources)
    claim_errors = _validate_claims(claims, source_ids)
    return src_errors + claim_errors


def coverage_gaps(claims_path: Path) -> set[str]:
    claims = _load(claims_path)
    covered: set[str] = set()
    for c in claims:
        covered.update(c.get("parent_goals", []))
    return PARENT_GOALS - covered


def warnings(claims_path: Path, sources_path: Path) -> list[str]:
    """Non-failing advisories (do NOT affect exit code). Keeps the validator
    honest with skills/lullsense/references/evidence-methodology.md sections 7 and 10."""
    sources = {s["id"]: s for s in _load(sources_path) if isinstance(s, dict) and "id" in s}
    claims = _load(claims_path)
    warns: list[str] = []
    for c in claims:
        cid = c.get("claim_id", "?")
        if c.get("deprecated") is True:
            warns.append(f"{cid}: claim is deprecated")
        if c.get("evidence_level") == "high":
            for sid in c.get("sources", []):
                s = sources.get(sid)
                if s is not None and s.get("verified") is False:
                    warns.append(
                        f"{cid}: evidence_level high backed by unverified source {sid!r}")
    return warns


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    claims_path = root / "skills" / "lullsense" / "knowledge" / "claims.yaml"
    sources_path = root / "skills" / "lullsense" / "knowledge" / "sources.yaml"
    errors = validate(claims_path, sources_path)
    heuristics_path = root / "skills" / "lullsense" / "knowledge" / "sleep_timing_heuristics.yaml"
    if heuristics_path.exists():
        errors = errors + validate_heuristics(heuristics_path)
    gaps = coverage_gaps(claims_path)
    warns = warnings(claims_path, sources_path)
    for e in errors:
        print(f"ERROR: {e}")
    for w in warns:
        print(f"WARNING: {w}")
    if gaps:
        print(f"COVERAGE GAP: parent goals with no claim: {sorted(gaps)}")
    if errors:
        print(f"\n{len(errors)} error(s).")
        return 1
    print("Knowledge base is valid." + (" (warnings/coverage gaps above)" if warns or gaps else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
