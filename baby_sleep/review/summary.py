"""Build a calm, capped, honest ReviewSummary from detector signals (product heuristics).

Deterministic and prose-free: the persona layer owns all voice. Freshness-guarded so
stale data is never presented as 'recent'."""
from __future__ import annotations

from datetime import date

from baby_sleep.analyze.models import Baseline, BaselineStatus, Confidence, FeatureSeries
from baby_sleep.detect.models import Severity, Signal, SignalName, SignalStatus
from baby_sleep.review.models import (
    DOMAINS,
    DOMINANCE,
    SIGNAL_DOMAIN,
    Coverage,
    ReviewStatus,
    ReviewSummary,
)

DEFAULT_STALENESS_DAYS = 3
CAP = 2

_SEV_ORDER = {Severity.SIGNIFICANT: 3, Severity.MODERATE: 2, Severity.MILD: 1}
_CONF_ORDER = {Confidence.HIGH: 3, Confidence.MEDIUM: 2, Confidence.LOW: 1}
_STATUS_ORDER = {SignalStatus.ESTABLISHED: 2, SignalStatus.EMERGING: 1}
_NAME_ORDER = {name: i for i, name in enumerate(SignalName)}  # stable, reproducible tiebreak

_CONTEXT = SignalName.POSSIBLE_CONTEXT_RELATED_DISRUPTION


def _rank_key(s: Signal) -> tuple[int, int, int, int]:
    # sort ascending → most important first (negate the descending dimensions)
    return (-_SEV_ORDER[s.severity], -_CONF_ORDER[s.confidence],
            -_STATUS_ORDER[s.status], _NAME_ORDER[s.signal])


def _derive_coverage(series: FeatureSeries, as_of: date, staleness_days: int,
                     requested_window_days: int | None) -> Coverage:
    days = series.days
    if not days:
        return Coverage(covers_window=(False if requested_window_days is not None else None))
    start, end = min(d.day for d in days), max(d.day for d in days)
    span_days = (end - start).days + 1
    dsle = (as_of - end).days
    is_current = dsle <= staleness_days
    covers_window = None
    if requested_window_days is not None:
        covers_window = is_current and span_days >= requested_window_days - staleness_days
    return Coverage(start_date=start, end_date=end, n_days=len(days), span_days=span_days,
                    days_since_last_entry=dsle, is_current=is_current, covers_window=covers_window)


def build_review_summary(
    signals: list[Signal],
    series: FeatureSeries,
    baseline: Baseline,
    as_of: date,
    *,
    requested_window_days: int | None = None,
    staleness_days: int = DEFAULT_STALENESS_DAYS,
) -> ReviewSummary:
    coverage = _derive_coverage(series, as_of, staleness_days, requested_window_days)

    # Non-computed baseline: detection was not supported. Pass the status through; the
    # persona falls back to no-data reasoning. (run_detectors already returned [].)
    if baseline.status is not BaselineStatus.COMPUTED:
        return ReviewSummary(status=ReviewStatus(baseline.status.value),
                             coverage=coverage, reason=baseline.reason)

    # Computed, but the freshest data is too old to answer "recent" honestly.
    if not coverage.is_current:
        if coverage.days_since_last_entry is None:
            reason = "no dated sleep data available for the review window"
        else:
            reason = (f"newest entry is {coverage.days_since_last_entry} days before the "
                      f"review date; ask for a current export or review conversationally")
        return ReviewSummary(status=ReviewStatus.STALE_DATA, coverage=coverage, reason=reason)

    # Pull the context wrapper out (reframes the review; never competes for a cap slot).
    context_note = next((s for s in signals if s.signal is _CONTEXT), None)
    working = [s for s in signals if s.signal is not _CONTEXT]

    # Dedupe correlated signals: a dominant signal explains the dominated ones.
    present = {s.signal for s in working}
    dominated: set[SignalName] = set()
    for dominant, subs in DOMINANCE.items():
        if dominant in present:
            dominated |= subs

    # Promote dominant severity to the max of itself + any folded-in dominated signals.
    sev_by_name = {s.signal: s.severity for s in working}

    def _promote(s: Signal) -> Signal:
        subs = DOMINANCE.get(s.signal)
        if not subs:
            return s
        folded = [sev_by_name[n] for n in subs if n in sev_by_name]
        if not folded:
            return s
        eff = max([s.severity, *folded], key=lambda sv: _SEV_ORDER[sv])
        if _SEV_ORDER[eff] <= _SEV_ORDER[s.severity]:
            return s
        return s.model_copy(update={
            "severity": eff,
            "limitations": [*s.limitations,
                            "severity reflects a more-severe related pattern folded into this signal"],
        })

    candidates = sorted(
        (_promote(s) for s in working if s.signal not in dominated),
        key=_rank_key,
    )

    # Cap = top 2 detailed, but any significant-severity signal is always surfaced.
    surfaced = list(candidates[:CAP])
    surfaced += [s for s in candidates[CAP:] if s.severity is Severity.SIGNIFICANT]
    also_noted_count = len(candidates) - len(surfaced)

    # Steady = domains untouched by ANY non-context signal (dominated ones still count).
    touched = {SIGNAL_DOMAIN[s.signal] for s in working if s.signal in SIGNAL_DOMAIN}
    steady_domains = [d for d in DOMAINS if d not in touched]

    return ReviewSummary(
        status=ReviewStatus.COMPUTED, coverage=coverage, surfaced=surfaced,
        also_noted_count=also_noted_count, steady_domains=steady_domains,
        context_note=context_note,
    )
