"""Public-doc guard tests: shipped docs must not leak internal-only material.

The API's per-provider internals and our internal task references stay out of the public doc set
(the README, package metadata and shipped docstrings) — see the coverage/error guides at
https://odds.software/docs/ and the rest repo's okf-bundle § Internal-only details.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PUBLIC_FILES = [
    ROOT / "README.md",
    ROOT / "pyproject.toml",
    ROOT / "example.py",
    *sorted((ROOT / "src" / "oddshawk_sdk").glob("*.py")),
]

INTERNAL_PROVIDER_MARKERS = [r"betfair", r"\bexchange\b"]
INTERNAL_TASK_MARKERS = [r"\bcn-\d+", r"\bT1\b", r"\bT2\b", r"\bT6\b"]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ships_no_internal_provider_detail():
    for path in PUBLIC_FILES:
        text = _read(path)
        for pattern in INTERNAL_PROVIDER_MARKERS:
            assert not re.search(pattern, text, re.I), f"{path.name} must not name the internal provider ({pattern})"


def test_ships_no_internal_task_references():
    for path in PUBLIC_FILES:
        text = _read(path)
        for pattern in INTERNAL_TASK_MARKERS:
            assert not re.search(pattern, text), f"{path.name} must not carry an internal task reference ({pattern})"


def test_readme_documents_live_metering():
    readme = _read(ROOT / "README.md")
    assert not re.search(r"reserved|forthcoming", readme, re.I)
    for header in ("X-Data-Points-This-Hour", "X-Data-Points-Limit", "X-Hour-Resets-At"):
        assert header in readme, f"README.md must document the live {header} header"


def test_readme_documents_live_coverage_and_throttle():
    readme = _read(ROOT / "README.md")
    assert "coverage_not_entitled" in readme
    assert "throttled" in readme
    assert "/rest/account" in readme


def test_readme_keeps_planned_codes_marked_as_planned():
    readme = _read(ROOT / "README.md")
    for code in ("feed_down", "catalog_dropped", "payment_required"):
        assert code in readme, f"README.md must still list {code}"
    assert re.search(r"planned", readme, re.I)


def test_docs_do_not_publish_the_internal_event_id_key():
    for path in (ROOT / "README.md", ROOT / "src" / "oddshawk_sdk" / "rest.py"):
        assert "eventId" not in _read(path), f"{path.name} must not document the internal eventId key"


def test_docs_still_cover_the_catalog_and_matching_surface():
    readme = _read(ROOT / "README.md")
    for method in ("authenticate", "version", "sports", "competitions", "events", "markets", "providers", "odds"):
        assert method in readme, f"README.md must document {method}"
    for method in ("match_event", "match_selection", "match_team", "match_competition"):
        assert method in readme, f"README.md must document {method}"
