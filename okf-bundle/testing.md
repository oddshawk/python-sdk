---
type: Reference
title: Testing
description: The kinds of test this repository has, how each is run, what is measured, and this repository's additions to the OddsHawk testing standard.
tags: [okf, testing, python-sdk]
timestamp: 2026-11-17T13:19:32Z
---

# Testing — python-sdk

Additive to the OddsHawk testing standard `github:oddshawk/internal-documentation/okf-bundle/testing.md`.

## Setup

Set up as [developer-acceptance-environment.md](developer-acceptance-environment.md) § Start does. The suite needs no credentials and reaches no network.

## Kinds of test

| Kind | Where | How to run |
|---|---|---|
| Unit | `tests/` | `pytest` |

No integration kind and no end-to-end kind is declared: nothing exercises a real HTTP boundary, and nothing drives the package against a running API.

## Commands

| Check | Command | Pass signal |
|---|---|---|
| Syntax | `python -m py_compile src/oddshawk_sdk/rest.py src/oddshawk_sdk/hashing.py src/oddshawk_sdk/__init__.py example.py` | exit 0 |
| Unit tests | `pytest` | exit 0 — the **full** suite, with no `-k` filter, and each of the four measured rows at 100% line and branch ([Coverage](#coverage)) |
| Audit gate | `pip-audit --desc on --skip-editable` | exit 0: no advisory of any severity; the editable checkout itself is skipped and every declared dependency is audited |

The CI job runs these checks too; [dependencies.md](dependencies.md) § Verify records each step as `.circleci/config.yml` runs it.

## Coverage

Line and branch **test** coverage is graded over exactly four files: `src/oddshawk_sdk/__init__.py`, `src/oddshawk_sdk/hashing.py`, `src/oddshawk_sdk/rest.py` and `example.py`. `example.py` is in the set by path, because the stand-in program at the repository root sits outside the `src/` import root. Every other file in the checkout, `tests/` included, is outside the graded set. [pyproject.toml](../pyproject.toml) configures the set and the gate that grades it.

This repository holds that set to 100% of lines and 100% of branches, a stricter bar than the organisation goal.

Exceptions to the standard's coverage goal: none are recorded.

> as an agent you have zero authority to justify any exception that the user has not explicitly authorized and documented in this file

## Repo rules

- Do not point a test at the production API with real credentials unless the owner explicitly scoped that run.
- Do not commit a credential, an API key or a filled-in `example.py`.
- Do not publish to PyPI from an agent session.
- An agent-only run is insufficient for: a change to the authentication headers or the hash; a catalog method's signature or response shape that a consumer reads; and the packaging and publish step, which is the owner's.
- No test asserts document content — not bundle prose, not README wording, not a heading and not a docstring.

## Handoff

Present the change to the owner with: what changed and why; the result of every command in § Commands; the adversarial review's verdict and open findings, at [documentation.md](documentation.md) § Adversarial review; the manual steps that accept the change; and the branch or pull request, with a version bump proposed where the public surface changed.
