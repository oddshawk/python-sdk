---
type: Reference
title: Dependencies
description: Dependency locations, human pins, and check/update cadence for oddshawk-python-sdk.
tags: [okf, dependencies, oddshawk-python-sdk]
timestamp: 2026-08-21T00:00:00Z
---

# Dependencies — oddshawk-python-sdk

cn-123 SDK wave (Phase 3). PyPI package name `oddshawk-sdk` (GitHub `oddshawk/python-sdk`).

## Summary

| Class | Locations | Human pins | Check | Owner |
|-------|-----------|------------|-------|-------|
| pip | `pyproject.toml` | `requests>=2.32,<3` | weekly | agent → nathan |
| Python CI | `.circleci/config.yml` | `cimg/python:3.12`; `requires-python >=3.10` | monthly | agent → nathan |
| CI audit | `pip-audit --strict` | blocking on `test` | weekly | agent |
| Publish | PyPI | Nathan-only twine/upload | on merge | nathan |

## (a) Locations and pins

- Dependabot weekly pip (no Docker — no Dockerfile)
- CircleCI `test`: editable install `.[dev]` + `py_compile` + `pytest` + blocking `pip-audit --strict`
- **Highlights:** `requests` runtime; `pytest` + `pip-audit` as optional `dev` extras
- **Packaging note:** minimal installable layout for PyPI (`src/oddshawk_sdk`). Parallel cn-127 tip has a richer catalog refresh on a separate branch — reconcile before dual-merge if both land.

## (b) Cadence

Weekly Dependabot + audit CI; Python image hop with LTS/policy; publish handoff after green merge (Nathan).

## (c) Host stack

| Layer | Detail |
|-------|--------|
| Deploy | Library only — no VM/K8s deploy from this repo |
| Runtime | Consumer Python ≥3.10; CI image 3.12 |

## Inherited / out-of-repo

- Credentials rotation: cn-37
- Catalog / OpenAPI surface refresh + WS client: cn-127
- Direct consumers (Phase 4): **none found** in workspace as of 2026-08-21 (path/venv only historically)
