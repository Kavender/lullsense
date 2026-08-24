from pathlib import Path

from scripts.validate_knowledge import validate

FIX = Path(__file__).parent / "fixtures"


def _run(claims_name, sources_name="valid_min.sources.yaml"):
    return validate(FIX / claims_name, FIX / sources_name)


def test_valid_fixtures_pass():
    errors = _run("valid_min.claims.yaml")
    assert errors == []


def test_bad_enum_is_rejected():
    errors = _run("invalid_bad_enum.claims.yaml")
    assert any("evidence_type" in e for e in errors)


def test_dangling_source_is_rejected():
    errors = _run("invalid_dangling_source.claims.yaml")
    assert any("does_not_exist" in e for e in errors)


def test_unsafe_safety_claim_is_rejected():
    errors = _run("invalid_unsafe_safety.claims.yaml")
    assert any("A_safety" in e or "safety" in e.lower() for e in errors)


def test_bad_age_range_is_rejected():
    errors = _run("invalid_bad_age.claims.yaml")
    assert any("age_range_months" in e for e in errors)


def test_coverage_reports_missing_goals():
    from scripts.validate_knowledge import coverage_gaps

    gaps = coverage_gaps(FIX / "valid_min.claims.yaml")
    assert "early_waking" in gaps
    assert "is_this_normal" not in gaps


def test_warns_on_unverified_high_source():
    from scripts.validate_knowledge import warnings

    warns = warnings(FIX / "valid_min.claims.yaml", FIX / "valid_min.sources.yaml")
    assert any("unverified source" in w for w in warns)


def test_warns_on_deprecated_claim():
    from scripts.validate_knowledge import warnings

    warns = warnings(FIX / "warn_deprecated.claims.yaml", FIX / "valid_min.sources.yaml")
    assert any("deprecated" in w for w in warns)


def test_warnings_do_not_fail_validation():
    errors = _run("warn_deprecated.claims.yaml")
    assert errors == []
