import json

from baby_sleep.contract.schema import export_json_schema


def test_schema_exports_valid_json_with_core_types():
    schema = export_json_schema()
    text = json.dumps(schema)  # must be JSON-serializable
    assert "$defs" in schema
    for typ in ("SleepLog", "SleepSession", "ContextEvent", "Child", "ApproxTime"):
        assert typ in schema["$defs"], f"{typ} missing from schema"
    # canonical enum values are present
    assert "daycare" in text and "night" in text


def test_schema_contains_no_vendor_field_names():
    text = json.dumps(export_json_schema()).lower()
    for vendor in ("start condition", "start location", "end condition",
                   "huckleberry", "start_condition", "end_condition"):
        assert vendor not in text, f"vendor token leaked into contract: {vendor!r}"
