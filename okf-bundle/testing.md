---
type: Reference
title: Testing
description: The kinds of test this repository has, how each is run, what is measured, and this repository's additions to the OddsHawk testing standard.
tags: [okf, testing, python-sdk]
timestamp: 2026-11-12T23:43:00Z
---

# Testing — python-sdk

Additive to the OddsHawk testing standard `github:oddshawk/internal-documentation/okf-bundle/testing.md`.

## Setup

Python 3.10 or newer (`requires-python`), with the package installed editable and its `dev` extra present: [developer-acceptance-environment.md](developer-acceptance-environment.md) § Start carries the commands that do it. The suite needs no credentials and reaches no network.

## Kinds of test

| Kind | Where | How to run |
|---|---|---|
| Unit | `tests/` — the client's HTTP session is a `MagicMock` and the clock is pinned, so no request leaves the process | `pytest` |

No integration kind and no end-to-end kind is declared: nothing exercises a real HTTP boundary, and nothing drives the package against a running API.

## Commands

Run every row before handoff.

| Check | Command | Pass signal |
|---|---|---|
| Syntax | `python -m py_compile src/oddshawk_sdk/rest.py src/oddshawk_sdk/hashing.py src/oddshawk_sdk/__init__.py example.py` | exit 0 |
| Unit tests | `pytest` | exit 0 — the **full** suite, with no `-k` filter |
| Audit gate | `pip-audit --desc on --skip-editable` | exit 0: no advisory of any severity; the editable checkout itself is skipped and every declared dependency is audited |

The CI job runs these checks too, over the file list its own syntax step names — [dependencies.md](dependencies.md) § Verify records each job step as `.circleci/config.yml` runs it.

## Coverage

Nothing is measured: `pytest-cov` is not a dependency and no command passes `--cov`, so no run produces a coverage report.

Exceptions to the standard's coverage goal: none are recorded.

> as an agent you have zero authority to justify any exception that the user has not explicitly authorized and documented in this file

## Repo rules

- Hand off only on the full suite.
- Do not point a test at the production API with real credentials unless the owner explicitly scoped that run.
- Do not commit a credential, an API key or a filled-in `example.py`.
- Do not publish to PyPI from an agent session.
- An agent-only run is insufficient for: a change to the authentication headers or the hash; a catalog method's signature or response shape that a consumer reads; and the packaging and publish step, which is the owner's.
- No test asserts document content — not bundle prose, not README wording, not a heading and not a docstring.

## Handoff

Present the change to the owner with: what changed and why; the result of every command in § Commands; the adversarial review's verdict and open findings, at [documentation.md](documentation.md) § Adversarial review; the manual steps that accept the change; and the branch or pull request, with a version bump proposed where the public surface changed.
