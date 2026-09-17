"""The red-flag quick net inlined into SKILL.md must stay in sync with safety-triage.md §2a.

This is the correctness guard behind the latency optimization of inlining the safety net
into the router (so no file read is needed to screen for red flags). If the two copies
drift, safety coverage in the hot path silently diverges from the source of truth.
"""

from scripts.check_safety_inline_sync import SAFETY, SKILL, check, extract_block


def test_red_flag_net_in_sync():
    ok, msg = check()
    assert ok, msg


def test_block_is_nonempty():
    # A silent regression where both blocks vanish (markers present, body empty) would
    # otherwise "pass" the equality check — guard against that.
    assert extract_block(SKILL).splitlines(), "inlined red-flag net is empty in SKILL.md"
    assert extract_block(SAFETY).splitlines(), "red-flag net is empty in safety-triage.md"
