from datetime import date

from baby_sleep.detect.models import SignalName
from baby_sleep.review.models import (
    DOMAINS,
    DOMINANCE,
    SIGNAL_DOMAIN,
    Coverage,
    ReviewStatus,
    ReviewSummary,
)


def test_domain_map_covers_all_non_context_signals():
    # every detector signal except the context wrapper maps to exactly one domain
    non_context = {n for n in SignalName if n is not SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION}
    assert set(SIGNAL_DOMAIN) == non_context
    assert set(SIGNAL_DOMAIN.values()) <= set(DOMAINS)
    assert len(DOMAINS) == 5


def test_dominance_map_shape():
    assert DOMINANCE[SignalName.SPLIT_NIGHT] == {SignalName.NIGHT_WAKING, SignalName.EARLY_WAKING}
    assert DOMINANCE[SignalName.NAP_TRANSITION] == {SignalName.SHORT_NAP}


def test_review_summary_roundtrip():
    cov = Coverage(start_date=date(2026, 9, 1), end_date=date(2026, 9, 14),
                   n_days=14, span_days=14, days_since_last_entry=1, is_current=True,
                   covers_window=True)
    rs = ReviewSummary(status=ReviewStatus.COMPUTED, coverage=cov, steady_domains=list(DOMAINS))
    r = ReviewSummary.model_validate(rs.model_dump())
    assert r.status is ReviewStatus.COMPUTED
    assert r.coverage.n_days == 14
    assert r.also_noted_count == 0
