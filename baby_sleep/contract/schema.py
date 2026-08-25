"""Export the canonical contract as a JSON Schema document for external consumers."""
from __future__ import annotations

from typing import Any

from .models import SleepLog


def export_json_schema() -> dict[str, Any]:
    """Return the JSON Schema for the whole SleepLog contract (with $defs for
    every nested model including the root SleepLog)."""
    schema = SleepLog.model_json_schema(ref_template="#/$defs/{model}")
    # Pydantic v2 places the root model at the top level; move a copy into $defs
    # so the no-leak test and downstream consumers can find all types consistently.
    defs = schema.setdefault("$defs", {})
    if "SleepLog" not in defs:
        root_copy = {k: v for k, v in schema.items() if k != "$defs"}
        defs["SleepLog"] = root_copy
    return schema
