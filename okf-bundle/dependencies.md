---
type: Reference
title: Dependencies
description: The dependency classes of oddshawk-sdk, its human pins and holds, its cross-repo consumers, and the commands that verify them, per `github:oddshawk/internal-documentation/okf-bundle/dependencies.md`.
tags: [okf, oddshawk, dependencies, python-sdk]
timestamp: 2026-11-12T21:56:00Z
---

## Summary and classes

| kind | class | members |
|---|---|---|
| package | Application packages | `pyproject.toml`: the runtime dependency `requests>=2.32,<3` |
| package | Application packages | `pyproject.toml`: the `dev` extra, `pytest>=8.3` and `pip-audit>=2.7` |
| package | Application packages | `pyproject.toml`: the build requirements `setuptools>=68` and `wheel` |
| package | Application packages | `.github/dependabot.yml`: weekly pip updates at `open-pull-requests-limit: 10` |
| runtime | Language runtime | `pyproject.toml`: `requires-python = ">=3.10"`, claiming 3.10 through 3.13 in its classifiers |
| ci | CI toolchain | `.circleci/config.yml`: the image `cimg/python:3.12`, the orb `circleci/slack@6.1.3`, and the `test` job's steps |
| deploy | — | none: no container image, service, server or database is deployed from this repository |

## Human pins

| kind | item | repos | pinned at |
|---|---|---|---|

## Held / do-not-bump

| kind | item | repos | held at | blocking reason | unblock condition |
|---|---|---|---|---|---|

## Cross-repo consumers

| kind | item | provider | consumers | version constraint |
|---|---|---|---|---|
| package | `oddshawk-sdk` | `python-sdk` | none known | — |

## Verify

| kind | item | command | expected result |
|---|---|---|---|
| package | install | `pip install -e ".[dev]"` | exit 0: the package and its `dev` extra are installed |
| package | unit tests | `pytest` | exit 0: the full suite passes |
| package | syntax | `python -m py_compile src/oddshawk_sdk/rest.py src/oddshawk_sdk/hashing.py src/oddshawk_sdk/__init__.py example.py` | exit 0 |
| package | audit gate | `pip-audit --desc on --skip-editable` | exit 0: no advisory of any severity; the editable package itself is skipped |
| ci | image the suite runs on | `grep 'image: cimg/python' .circleci/config.yml` | `- image: cimg/python:3.12` |
| ci | slack orb | `grep 'slack:' .circleci/config.yml` | `slack: circleci/slack@6.1.3` |
| ci | syntax step as this job runs it | `grep -A2 'name: Syntax' .circleci/config.yml` | the step compiles `rest.py`, `__init__.py` and `example.py`; the command above adds `hashing.py` |
| ci | audit step as this job runs it | `grep -A2 'name: pip-audit' .circleci/config.yml` | the step runs `pip-audit --desc on --skip-editable` and blocks the job |
