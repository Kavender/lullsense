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


from baby_sleep.analyze.models import (
    Baseline,
    BaselineStatus,
    Confidence,
    DailyFeatures,
    FeatureSeries,
)
from baby_sleep.detect.models import Severity, Signal, SignalStatus
from baby_sleep.review.summary import build_review_summary


def _sig(name, sev=Severity.MODERATE, conf=Confidence.MEDIUM,
         status=SignalStatus.ESTABLISHED):
    return Signal(signal=name, confidence=conf, severity=sev, status=status)


def _series(end_day, n=14):
    # n consecutive days ending on end_day (a datetime.date)
    from datetime import timedelta
    days = [DailyFeatures(day=end_day - timedelta(days=n - 1 - i)) for i in range(n)]
    return FeatureSeries(days=days)


_COMPUTED = Baseline(status=BaselineStatus.COMPUTED, recent_window_days=5)


def test_ranks_and_caps_to_two_detailed():
    signals = [
        _sig(SignalName.BEDTIME_RESISTANCE, sev=Severity.MILD, conf=Confidence.LOW),
        _sig(SignalName.EARLY_WAKING, sev=Severity.MODERATE, conf=Confidence.HIGH),
        _sig(SignalName.HIGH_VARIABILITY, sev=Severity.MODERATE, conf=Confidence.MEDIUM),
    ]
    rs = build_review_summary(signals, _series(date(2026, 9, 20)), _COMPUTED, date(2026, 9, 20))
    assert rs.status is ReviewStatus.COMPUTED
    assert [s.signal for s in rs.surfaced] == [SignalName.EARLY_WAKING, SignalName.HIGH_VARIABILITY]
    assert rs.also_noted_count == 1  # bedtime_resistance folded into the count line


def test_significant_severity_always_surfaced_past_cap():
    signals = [
        _sig(SignalName.EARLY_WAKING, sev=Severity.SIGNIFICANT, conf=Confidence.HIGH),
        _sig(SignalName.HIGH_VARIABILITY, sev=Severity.SIGNIFICANT, conf=Confidence.HIGH),
        _sig(SignalName.BEDTIME_RESISTANCE, sev=Severity.SIGNIFICANT, conf=Confidence.MEDIUM),
    ]
    rs = build_review_summary(signals, _series(date(2026, 9, 20)), _COMPUTED, date(2026, 9, 20))
    assert len(rs.surfaced) == 3  # all three significant → none buried by the cap
    assert rs.also_noted_count == 0


def test_split_night_dominates_night_and_early_waking():
    signals = [
        _sig(SignalName.SPLIT_NIGHT, sev=Severity.MODERATE),
        _sig(SignalName.NIGHT_WAKING, sev=Severity.MODERATE),
        _sig(SignalName.EARLY_WAKING, sev=Severity.MILD),
    ]
    rs = build_review_summary(signals, _series(date(2026, 9, 20)), _COMPUTED, date(2026, 9, 20))
    surfaced = {s.signal for s in rs.surfaced}
    assert SignalName.SPLIT_NIGHT in surfaced
    assert SignalName.NIGHT_WAKING not in surfaced
    assert SignalName.EARLY_WAKING not in surfaced
    assert rs.also_noted_count == 0  # dominated signals fold in, not counted


def test_context_pulled_out_as_note_not_surfaced():
    signals = [
        _sig(SignalName.SHORT_NAP, sev=Severity.MODERATE),
        _sig(SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION, sev=Severity.MILD),
    ]
    rs = build_review_summary(signals, _series(date(2026, 9, 20)), _COMPUTED, date(2026, 9, 20))
    assert {s.signal for s in rs.surfaced} == {SignalName.SHORT_NAP}
    assert rs.context_note is not None
    assert rs.context_note.signal is SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION


def test_quiet_review_names_all_five_steady_domains():
    rs = build_review_summary([], _series(date(2026, 9, 20)), _COMPUTED, date(2026, 9, 20))
    assert rs.status is ReviewStatus.COMPUTED
    assert rs.surfaced == []
    assert rs.steady_domains == DOMAINS


def test_steady_domains_exclude_touched_including_dominated():
    signals = [
        _sig(SignalName.SPLIT_NIGHT),   # night_sleep
        _sig(SignalName.NIGHT_WAKING),  # night_sleep (dominated, still marks domain non-steady)
        _sig(SignalName.SHORT_NAP),     # naps
    ]
    rs = build_review_summary(signals, _series(date(2026, 9, 20)), _COMPUTED, date(2026, 9, 20))
    assert "night_sleep" not in rs.steady_domains
    assert "naps" not in rs.steady_domains
    assert set(rs.steady_domains) == {"bedtime", "total_sleep", "schedule_consistency"}


def test_stale_data_yields_stale_status_and_no_signals():
    signals = [_sig(SignalName.EARLY_WAKING, sev=Severity.SIGNIFICANT)]
    # data ends 2026-09-14 but we review as of 2026-10-01 → 17 days stale (> 3)
    rs = build_review_summary(signals, _series(date(2026, 9, 14)), _COMPUTED, date(2026, 10, 1))
    assert rs.status is ReviewStatus.STALE_DATA
    assert rs.surfaced == []
    assert rs.coverage.is_current is False
    assert rs.coverage.days_since_last_entry == 17
    assert rs.reason is not None


def test_current_within_tolerance_is_computed():
    signals = [_sig(SignalName.EARLY_WAKING)]
    # data ends 2026-09-14, review 2026-09-17 → 3 days (== tolerance) → current
    rs = build_review_summary(signals, _series(date(2026, 9, 14)), _COMPUTED, date(2026, 9, 17))
    assert rs.status is ReviewStatus.COMPUTED
    assert rs.coverage.is_current is True


def test_covers_window_flag():
    rs = build_review_summary([], _series(date(2026, 9, 20), n=14), _COMPUTED,
                              date(2026, 9, 20), requested_window_days=14)
    assert rs.coverage.covers_window is True
    rs2 = build_review_summary([], _series(date(2026, 9, 20), n=3), _COMPUTED,
                               date(2026, 9, 20), requested_window_days=14)
    assert rs2.coverage.covers_window is False


def test_non_computed_baseline_passes_through():
    rs = build_review_summary(
        [], _series(date(2026, 9, 20)),
        Baseline(status=BaselineStatus.INSUFFICIENT_DATA, reason="only 3 days of data"),
        date(2026, 9, 20),
    )
    assert rs.status is ReviewStatus.INSUFFICIENT_DATA
    assert rs.surfaced == []
    assert rs.reason == "only 3 days of data"
