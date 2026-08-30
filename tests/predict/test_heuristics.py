from pathlib import Path

from baby_sleep.predict.heuristics import AgeBand, load_heuristics, lookup

FIX = Path(__file__).parent / "fixtures" / "heuristics_min.yaml"


def test_load_and_lookup():
    bands = load_heuristics(FIX)
    assert len(bands) == 2
    b = lookup(bands, 9)
    assert isinstance(b, AgeBand)
    assert b.wake_window_minutes.min == 120 and b.wake_window_minutes.max == 180


def test_lookup_band_boundaries_are_inclusive_exclusive():
    bands = load_heuristics(FIX)
    assert lookup(bands, 12).wake_window_minutes.max == 300   # 12 falls in [12,36)
    assert lookup(bands, 4).wake_window_minutes.min == 120    # 4 falls in [4,12)


def test_lookup_out_of_range_returns_none():
    bands = load_heuristics(FIX)
    assert lookup(bands, 48) is None
    assert lookup(bands, 3) is None
