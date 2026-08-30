from baby_sleep.predict.models import Basis, NextEvent, PredictInput, Prediction


def test_predict_input_defaults():
    inp = PredictInput(age_months=12, last_wake_min=600)
    assert inp.target == "nap"
    assert inp.personal is None
    assert inp.corrected_age_months is None


def test_prediction_roundtrips_json():
    ne = NextEvent(type="nap", window_low="11:30", window_high="12:30",
                   center="12:00", confidence="low", basis=Basis.AGE_ONLY.value,
                   band_reason="wide")
    pred = Prediction(status="computed", next_event=ne, caveats=["cues win"])
    dumped = pred.model_dump(mode="json")
    assert dumped["next_event"]["confidence"] == "low"
    assert dumped["status"] == "computed"
