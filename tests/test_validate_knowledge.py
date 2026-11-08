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


def test_rejects_unverified_high_source():
    # Promoted from an advisory warning to a hard error: a high-evidence claim
    # that cites an unverified source must fail validation.
    errors = _run(
        "invalid_unverified_high.claims.yaml",
        sources_name="invalid_unverified_high.sources.yaml",
    )
    assert any("unverified" in e and "high" in e for e in errors)


def test_warns_on_deprecated_claim():
    from scripts.validate_knowledge import warnings

    warns = warnings(FIX / "warn_deprecated.claims.yaml", FIX / "valid_min.sources.yaml")
    assert any("deprecated" in w for w in warns)


def test_warnings_do_not_fail_validation():
    errors = _run("warn_deprecated.claims.yaml")
    assert errors == []


def test_heuristics_table_valid():
    import scripts.validate_knowledge as vk
    root = Path(vk.__file__).resolve().parent.parent
    path = root / "skills" / "lullsense" / "knowledge" / "sleep_timing_heuristics.yaml"
    errors = vk.validate_heuristics(path)
    assert errors == [], errors


def _heuristics_rows():
    import yaml

    import scripts.validate_knowledge as vk
    root = Path(vk.__file__).resolve().parent.parent
    path = root / "skills" / "lullsense" / "knowledge" / "sleep_timing_heuristics.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_heuristics_tier2_fields_parse():
    """CAM-160 §5.2: every band carries the ageRef fields the app transcribes, and they
    are internally consistent (one more wake window than naps; sequences inside the band
    months or the next transition; sources resolve)."""
    import yaml

    import scripts.validate_knowledge as vk
    root = Path(vk.__file__).resolve().parent.parent
    sources = yaml.safe_load(
        (root / "skills/lullsense/knowledge/sources.yaml").read_text(encoding="utf-8"))
    ids = {s["id"] for s in sources}
    rows = _heuristics_rows()
    assert [r["age_band_months"] for r in rows] == [[4, 6], [6, 9], [9, 12], [12, 18], [18, 36]]
    for r in rows:
        assert vk._validate_tier2("t", r, ids) == []
        assert r["basis"] == "育儿经验范围，按你家数据调"
        assert r["source_type"] == "heuristic"
        for s in r["sequences"]:
            assert len(s["wake_windows_minutes"]) == s["naps"] + 1


def test_heuristics_tier2_rejects_bad_rows():
    import copy

    import scripts.validate_knowledge as vk
    good = _heuristics_rows()[3]
    for mutate in (
        lambda r: r["sequences"][0]["wake_windows_minutes"].pop(),
        lambda r: r.__setitem__("latest_nap_end_local", "25:00"),
        lambda r: r.__setitem__("nap_transition", {"from": 2, "to": 1, "months": [15, 40]}),
        lambda r: r.__setitem__("sources", ["no_such_source"]),
        lambda r: r.pop("basis"),
    ):
        r = copy.deepcopy(good)
        mutate(r)
        assert vk._validate_tier2("t", r, {"huckleberry_sleep_expectations"}) != []
