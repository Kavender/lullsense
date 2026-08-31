from pathlib import Path

from baby_sleep.predict.core import predict_next
from baby_sleep.predict.heuristics import load_heuristics
from baby_sleep.predict.models import PredictInput

BANDS = load_heuristics(Path(__file__).parent / "fixtures" / "heuristics_min.yaml")


def test_under_4_months_returns_newborn_guardrail_no_time():
    pred = predict_next(PredictInput(age_months=2, last_wake_min=600), BANDS)
    assert pred.status == "newborn_guardrail"
    assert pred.next_event is None
    assert any("newborn guardrail" in c.lower() for c in pred.caveats)


def test_corrected_age_under_4_months_triggers_guardrail():
    pred = predict_next(
        PredictInput(age_months=5, corrected_age_months=3, last_wake_min=600), BANDS)
    assert pred.status == "newborn_guardrail"
    assert pred.next_event is None


def test_guardrail_omits_range_caveat_when_no_budget():
    # fixture has no band < 4mo, so budget is None -> the "total-sleep range" caveat
    # must NOT appear (no contradiction).
    pred = predict_next(PredictInput(age_months=2, last_wake_min=600), BANDS)
    assert pred.budget is None
    assert not any("total-sleep range" in c for c in pred.caveats)


def test_age_above_table_returns_age_unknown():
    pred = predict_next(PredictInput(age_months=60, last_wake_min=600), BANDS)
    assert pred.status == "age_unknown"
    assert pred.next_event is None


def test_age_unknown_has_no_age_band_wake_window():
    inp = PredictInput(age_months=60, last_wake_min=600)   # beyond the table
    pred = predict_next(inp, BANDS)
    assert pred.status == "age_unknown"
    assert pred.age_band_wake_window is None


def test_package_exports_predict_next():
    import baby_sleep.predict as pkg
    assert hasattr(pkg, "predict_next")
    assert hasattr(pkg, "personal_stats_from_series")
