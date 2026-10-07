"""Stateless analysis service (CAM-12): one JSON request in, one JSON response out.

This module stays import-light: ``python -m baby_sleep.service`` imports it before
``__main__`` runs, so anything heavy here (pydantic, the pipeline) would escape
``__main__``'s warnings filter and error mapping. The work lives in ``api``."""
from __future__ import annotations

SCHEMA_VERSION = 1

__all__ = ["SCHEMA_VERSION", "run"]


def run(request: object) -> dict:
    """Validate a decoded §3.1 request and compute the §3.2 response (or a §3.3 error)."""
    from .api import run as _run
    return _run(request)
