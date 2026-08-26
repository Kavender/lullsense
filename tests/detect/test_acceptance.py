"""Phase 3 acceptance (spec §18): structured evidence/limitations; no clinical diagnosis;
age-gated; analyze/contract-only dependency."""
import ast
from datetime import datetime
from pathlib import Path

from baby_sleep.analyze.baseline import build_baseline
from baby_sleep.analyze.features import build_feature_series
from baby_sleep.contract.enums import EventKind, SleepType
from baby_sleep.contract.models import Child, ContextEvent, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.detect import DetectorInput, SignalName, run_detectors

# a diagnosis-word denylist the detector output must never contain
_FORBIDDEN = ("infection", "apnea", "reflux", "ear infection", "diagnos", "disease", "disorder")


def _n(d, rh, rm, dur):
    return SleepSession(start=ApproxTime(value=datetime(2026, 9, d, 19, 30)),
                        end=ApproxTime(value=datetime(2026, 9, d + 1, rh, rm)),
                        duration_minutes=dur, sleep_type=SleepType.NIGHT)


def _shift_input(age=12, events=None, reported=None):
    sess = [_n(1 + i, 6, 0, 630) for i in range(14)] + [_n(15 + i, 5, 0, 570) for i in range(5)]
    series = build_feature_series(SleepLog(sessions=sess))
    return DetectorInput(series=series, baseline=build_baseline(series, Child(age_months=age)),
                         events=events or [], reported_context=reported or [])


def test_signals_carry_structured_evidence_and_limitations():
    signals = run_detectors(_shift_input())
    ew = next(s for s in signals if s.signal is SignalName.EARLY_WAKING)
    assert ew.supporting_evidence and isinstance(ew.supporting_evidence, list)
    assert ew.baseline is not None and ew.recent is not None
    assert ew.confidence.value in ("low", "medium", "high")     # ordinal (D14), not numeric


def test_no_clinical_diagnosis_language():
    ev = ContextEvent(kind=EventKind.MEDICATION,
                      at=ApproxTime(value=datetime(2026, 9, 16, 15, 0)), label="teething gel")
    signals = run_detectors(_shift_input(events=[ev], reported=["teething"]))
    # no detector may CLAIM a diagnosis in its evidence (limitations legitimately say
    # "not a medical diagnosis", so they are scanned separately for a negation instead).
    for s in signals:
        blob = " ".join(s.supporting_evidence).lower()
        for word in _FORBIDDEN:
            assert word not in blob, f"diagnosis-adjacent word leaked in evidence: {word}"
    ctx = next(s for s in signals if s.signal.value == "possible_context_related_disruption")
    assert any("not" in lim.lower() for lim in ctx.limitations)


def test_context_quotes_parent_medical_word_without_asserting_it():
    # review Minor 2: the context detector may ECHO a parent's medical word (traceability),
    # but must never ASSERT it — confidence stays capped at <= medium and the output always
    # carries the explicit "not a medical diagnosis" limitation.
    ev = ContextEvent(kind=EventKind.MEDICATION,
                      at=ApproxTime(value=datetime(2026, 9, 16, 15, 0)), label="reflux meds")
    signals = run_detectors(_shift_input(events=[ev], reported=["ear infection"]))
    ctx = next(s for s in signals if s.signal.value == "possible_context_related_disruption")
    assert ctx.confidence.value in ("low", "medium")            # never high (correlational cap)
    assert any("not" in lim.lower() and "diagnos" in lim.lower() for lim in ctx.limitations)


def test_age_gate_blocks_newborn():
    assert run_detectors(_shift_input(age=3)) == []


def test_detect_imports_only_contract_and_analyze():
    root = Path(__file__).parent.parent.parent / "baby_sleep" / "detect"
    for py in root.glob("*.py"):
        for node in ast.walk(ast.parse(py.read_text())):
            mod = node.module if isinstance(node, ast.ImportFrom) else None
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else []
            for t in ([mod] if mod else []) + names:
                if t and t.startswith("baby_sleep."):
                    assert t.startswith(("baby_sleep.detect", "baby_sleep.analyze",
                                         "baby_sleep.contract")), \
                        f"{py.name} imports {t} — detect may depend only on analyze/contract"
