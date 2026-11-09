"""Guards the claims-index + `lullsense-cite` path (T9).

Citing a claim scans `claims-index.md` and fetches only the needed entries with
`lullsense-cite`, instead of loading the ~64KB `claims.yaml` / ~30KB `sources.yaml` into the
conversation. This locks in that the generated index stays in sync with its source (so the
scan can't go stale) and that the lookup tool resolves claims, sources, and misses correctly.
"""
from pathlib import Path

import yaml

from scripts import cite
from scripts.build_knowledge_index import CLAIMS, INDEX, build

ROOT = Path(__file__).resolve().parents[1]


def _claim_ids() -> list[str]:
    return [c["claim_id"] for c in yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))]


def test_committed_index_matches_a_fresh_build():
    """The mirror of the CI drift guard — a claims.yaml edit without a rebuilt index fails."""
    assert INDEX.read_text(encoding="utf-8") == build(), (
        "claims-index.md is stale — run `python scripts/build_knowledge_index.py` and commit"
    )


def test_every_claim_appears_in_the_index():
    index_text = INDEX.read_text(encoding="utf-8")
    missing = [cid for cid in _claim_ids() if f"`{cid}`" not in index_text]
    assert not missing, f"claims absent from the index: {missing}"


def test_cite_resolves_a_claim():
    kind, entry = cite.lookup("safe_sleep_back_to_sleep")
    assert kind == "claim"
    assert entry["claim_id"] == "safe_sleep_back_to_sleep"


def test_cite_resolves_a_source():
    kind, entry = cite.lookup("aap_safe_sleep_2022")
    assert kind == "source"
    assert entry["id"] == "aap_safe_sleep_2022"


def test_cite_unknown_id_returns_none():
    assert cite.lookup("definitely_not_an_id") is None


def test_cite_main_exit_codes():
    assert cite.main(["safe_sleep_back_to_sleep"]) == 0        # found
    assert cite.main(["definitely_not_an_id"]) == 1            # missing → nonzero
    assert cite.main([]) == 2                                  # usage error


def test_every_index_id_exists_in_claims_yaml():
    import re

    index_ids = re.findall(r"^\| `([^`]+)` \|", INDEX.read_text(encoding="utf-8"), re.MULTILINE)
    assert index_ids, "no claim rows parsed from the index"
    assert set(index_ids) <= set(_claim_ids())


def test_cam160_claims_present():
    ids = set(_claim_ids())
    for cid in ("nap_timing_night_tradeoff", "early_waking_enough_vs_not",
                "sleep_diary_window_two_weeks", "one_change_then_recheck"):
        assert cid in ids
        assert cite.lookup(cid)[0] == "claim"
