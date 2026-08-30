from pathlib import Path

from baby_sleep.predict.core import predict_next
from baby_sleep.predict.heuristics import load_heuristics
from baby_sleep.predict.models import PredictInput

BANDS = load_heuristics(Path(__file__).parent / "fixtures" / "heuristics_min.yaml")


def test_age_only_returns_wide_range_low_confidence():
    # 9-month-old, last woke at 10:00 (600 min). Band 4-12: WW 120-180.
    inp = PredictInput(age_months=9, last_wake_min=600)
    pred = predict_next(inp, BANDS)
    assert pred.status == "computed"
    ne = pred.next_event
    assert ne.basis == "age_only"
    assert ne.confidence == "low"
    assert ne.window_low == "12:00"    # 600 + 120
    assert ne.window_high == "13:00"   # 600 + 180
    assert ne.center == "12:30"        # 600 + 150
    assert ne.type == "nap"


def test_age_only_has_budget_and_cues_caveat():
    pred = predict_next(PredictInput(age_months=9, last_wake_min=600), BANDS)
    assert pred.budget["total_sleep_low_h"] == 12
    assert any("tired cues" in c for c in pred.caveats)
    assert any("heuristic" in c.lower() for c in pred.caveats)
