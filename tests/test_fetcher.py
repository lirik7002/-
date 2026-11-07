"""Tests for METADATA parsing (no network)."""

from src.fetcher import _parse_requires_dist

SAMPLE = """Name: demo
Version: 1.0
Requires-Dist: requests (>=2)
Requires-Dist: urllib3 ; extra == "security"
Requires-Dist: click
"""


def test_parse_skips_extras():
    assert _parse_requires_dist(SAMPLE) == ["click", "requests"]
