from baby_sleep.contract.enums import DataQuality, EventKind, Location, SleepType, StartMarker


def test_enum_string_values_are_stable():
    assert SleepType.NAP.value == "nap"
    assert SleepType.NIGHT.value == "night"
    assert SleepType.UNKNOWN.value == "unknown"
    assert Location.DAYCARE.value == "daycare"
    assert Location.HOME.value == "home"
    assert {e.value for e in EventKind} == {"feed", "diaper", "medication", "pump", "other"}
    assert {e.value for e in DataQuality} == {"logged", "reported", "inferred"}
    assert {e.value for e in StartMarker} == {"put_down", "asleep", "unknown"}
