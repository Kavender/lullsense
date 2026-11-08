"""Validate skills/lullsense/knowledge/claims.yaml and skills/lullsense/knowledge/sources.yaml against the schema
defined in skills/lullsense/references/evidence-methodology.md.

Exit code 0 = valid, 1 = errors found. Safety rule (S2) is enforced hard.
A high-evidence claim resting on an unverified source is also a hard error
(promoted from an advisory warning that had gone stale — see §7). Remaining
warnings are advisory and do NOT affect the exit code.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

import yaml

EVIDENCE_TYPES = {
    "guideline", "professional_consensus", "systematic_review",
    "primary_research", "expert_practice", "heuristic",
}
EVIDENCE_LEVELS = {"high", "moderate", "low"}
LAYERS = {"A_safety", "B_developmental", "C_behavioral", "D_practice", "E_environment"}
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
# CAM-160 §5.2 tier-2 fields (null allowed for the cap / latest end / transition).
TIER2_FIELDS = {
    "sequences", "daytime_sleep_cap_hours", "latest_nap_end_local",
    "nap_transition", "basis", "sources",
}


def validate_heuristics(path: Path, source_ids: set[str] | None = None) -> list[str]:
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
        errors += _validate_tier2(tag, r, source_ids)
    return errors


def _is_range(x, lo: float = 0, hi: float = float("inf")) -> bool:
    return (isinstance(x, list) and len(x) == 2
            and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in x)
            and lo <= x[0] <= x[1] <= hi)


def _is_int(x, lo: int, hi: int) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and lo <= x <= hi


def _validate_tier2(tag: str, r: dict, source_ids: set[str] | None) -> list[str]:
    """CAM-160 §5.2 fields, mirrored by the app as `ageRef` (same bounds as its isAgeRef)."""
    errors: list[str] = []
    missing = TIER2_FIELDS - set(r)
    if missing:
        return [f"{tag}: missing CAM-160 fields {sorted(missing)}"]
    seqs = r["sequences"]
    if not isinstance(seqs, list) or len(seqs) > 6:
        errors.append(f"{tag}: sequences must be a list of <=6")
        seqs = []
    for j, s in enumerate(seqs):
        ok = (isinstance(s, dict) and set(s) == {"months", "naps", "wake_windows_minutes"}
              and _is_range(s["months"], 4, 36) and s["months"][0] < s["months"][1]
              and _is_int(s["naps"], 0, 8)
              and isinstance(s["wake_windows_minutes"], list)
              and len(s["wake_windows_minutes"]) == s["naps"] + 1
              and all(_is_range(w) for w in s["wake_windows_minutes"]))
        if not ok:
            errors.append(f"{tag}: bad sequences[{j}] {s!r}")
    cap = r["daytime_sleep_cap_hours"]
    if cap is not None and not (isinstance(cap, dict) and set(cap) == {"max"}
                                and isinstance(cap["max"], (int, float)) and 0 < cap["max"] <= 24):
        errors.append(f"{tag}: bad daytime_sleep_cap_hours {cap!r}")
    end = r["latest_nap_end_local"]
    if end is not None and not (isinstance(end, str) and re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", end)):
        errors.append(f"{tag}: bad latest_nap_end_local {end!r}")
    tr = r["nap_transition"]
    if tr is not None and not (isinstance(tr, dict) and set(tr) == {"from", "to", "months"}
                               and _is_int(tr["from"], 0, 8) and _is_int(tr["to"], 0, 8)
                               and _is_range(tr["months"], 4, 36)):
        errors.append(f"{tag}: bad nap_transition {tr!r}")
    if not (isinstance(r["basis"], str) and 1 <= len(r["basis"]) <= 80):
        errors.append(f"{tag}: basis must be a 1-80 char string")
    srcs = r["sources"]
    if not (isinstance(srcs, list) and srcs):
        errors.append(f"{tag}: sources must be a non-empty list")
    elif source_ids is not None:
        errors += [f"{tag}: source {s!r} not in sources.yaml" for s in srcs if s not in source_ids]
    return errors


def _load(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or []


def _validate_sources(sources) -> tuple[list[str], set[str], set[str]]:
    errors: list[str] = []
    ids: set[str] = set()
    verified: set[str] = set()
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
        elif s["verified"] is True:
            verified.add(s["id"])
    return errors, ids, verified


def _validate_claims(claims, source_ids: set[str], verified_ids: set[str]) -> list[str]:
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
        # A high-evidence claim must rest on verified sources. This was an advisory
        # warning for ~a dozen PRs; everyone learned to ignore it, which is exactly
        # how a real regression would slip past. Now a hard error: verify the source
        # (set verified: true after confirming it) or lower evidence_level.
        if c["evidence_level"] == "high":
            for sid in c["sources"]:
                if sid in source_ids and sid not in verified_ids:
                    errors.append(
                        f"{tag} {cid}: evidence_level high must cite verified sources; "
                        f"{sid!r} is unverified")
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
    src_errors, source_ids, verified_ids = _validate_sources(sources)
    claim_errors = _validate_claims(claims, source_ids, verified_ids)
    return src_errors + claim_errors


def coverage_gaps(claims_path: Path) -> set[str]:
    claims = _load(claims_path)
    covered: set[str] = set()
    for c in claims:
        covered.update(c.get("parent_goals", []))
    return PARENT_GOALS - covered


def warnings(claims_path: Path, sources_path: Path) -> list[str]:
    """Non-failing advisories (do NOT affect exit code). Keeps the validator
    honest with skills/lullsense/references/evidence-methodology.md sections 7 and 10.

    Note: high-evidence claims backed by unverified sources used to warn here; that
    is now a hard error in _validate_claims (§7), so it is no longer an advisory.
    """
    del sources_path  # retained for signature stability; no longer needed here
    claims = _load(claims_path)
    warns: list[str] = []
    for c in claims:
        cid = c.get("claim_id", "?")
        if c.get("deprecated") is True:
            warns.append(f"{cid}: claim is deprecated")
    return warns


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    claims_path = root / "skills" / "lullsense" / "knowledge" / "claims.yaml"
    sources_path = root / "skills" / "lullsense" / "knowledge" / "sources.yaml"
    errors = validate(claims_path, sources_path)
    heuristics_path = root / "skills" / "lullsense" / "knowledge" / "sleep_timing_heuristics.yaml"
    if heuristics_path.exists():
        _, source_ids, _ = _validate_sources(_load(sources_path))
        errors = errors + validate_heuristics(heuristics_path, source_ids)
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
