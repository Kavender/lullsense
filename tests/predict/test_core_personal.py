from pathlib import Path

from baby_sleep.predict.core import predict_next
from baby_sleep.predict.heuristics import load_heuristics
from baby_sleep.predict.models import PersonalStats, PredictInput

BANDS = load_heuristics(Path(__file__).parent / "fixtures" / "heuristics_min.yaml")


def test_personal_baseline_tightens_center_moderate_confidence():
    # 18-month-old (>=12 so NO young-age widening). Own WW median 200, mad 25.
    personal = PersonalStats(wake_window_median_min=200, wake_window_mad_min=25,
                             days_of_data=10, stable=True)
    inp = PredictInput(age_months=18, last_wake_min=600, personal=personal)
    pred = predict_next(inp, BANDS)
    ne = pred.next_event
    assert ne.basis == "personal_baseline"
    assert ne.confidence == "moderate"
    assert ne.center == "13:20"        # 600 + 200
    assert ne.window_low == "12:55"    # 600 + 200 - 25
    assert ne.window_high == "13:45"   # 600 + 200 + 25


def test_personal_half_width_floored_at_20():
    # tiny mad -> band must not collapse below +/-20 min
    personal = PersonalStats(wake_window_median_min=200, wake_window_mad_min=5,
                             days_of_data=14, stable=True)
    pred = predict_next(PredictInput(age_months=18, last_wake_min=600, personal=personal), BANDS)
    ne = pred.next_event
    assert ne.window_low == "13:00"    # 800 - 20
    assert ne.window_high == "13:40"    # 800 + 20


def test_young_age_widens_personal_band():
    # 9-month-old (<12) -> half-width * 1.5. mad 20 -> floor 20 -> *1.5 = 30.
    personal = PersonalStats(wake_window_median_min=150, wake_window_mad_min=20,
                             days_of_data=10, stable=True)
    pred = predict_next(PredictInput(age_months=9, last_wake_min=600, personal=personal), BANDS)
    ne = pred.next_event
    assert ne.window_low == "12:00"    # 750 - 30
    assert ne.window_high == "13:00"   # 750 + 30


def test_unstable_personal_falls_back_to_age_only():
    personal = PersonalStats(wake_window_median_min=150, wake_window_mad_min=10,
                             days_of_data=2, stable=False)
    pred = predict_next(PredictInput(age_months=9, last_wake_min=600, personal=personal), BANDS)
    assert pred.next_event.basis == "age_only"
    assert pred.next_event.confidence == "low"


def test_age_band_wake_window_surfaced_alongside_personal():
    # 18mo, stable personal window 200±25 → personal band drives the answer,
    # but the age-typical band must ALSO be surfaced for reality-vs-ideal reasoning.
    personal = PersonalStats(wake_window_median_min=200, wake_window_mad_min=25,
                             days_of_data=10, stable=True)
    inp = PredictInput(age_months=18, last_wake_min=600, personal=personal)
    pred = predict_next(inp, BANDS)
    band = next(b for b in BANDS if b.age_band_months[0] <= 18 < b.age_band_months[1])
    assert pred.age_band_wake_window == {
        "min": band.wake_window_minutes.min,
        "max": band.wake_window_minutes.max,
    }
    # personal basis still drives next_event
    assert pred.next_event.basis == "personal_baseline"
