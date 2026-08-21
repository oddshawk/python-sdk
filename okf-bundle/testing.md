---
type: Reference
title: Testing
description: How agents and humans verify changes in oddshawk-python-sdk.
tags: [okf, testing, oddshawk-python-sdk]
timestamp: 2026-08-21T00:00:00Z
---

# Testing — oddshawk-python-sdk

Implements workspace [testing-policy.md](../../www/okf-bundle/testing-policy.md).

## Agent testing

### Prerequisites

- Python 3.10+ (prefer 3.12 to match CI)
- Fresh venv: `python -m venv .venv && source .venv/bin/activate`
- `pip install -e ".[dev]"`

### Commands

Run **all** rows before handoff:

| Check | Command | Pass signal |
|-------|---------|-------------|
| Syntax | `python -m py_compile src/oddshawk_sdk/rest.py src/oddshawk_sdk/__init__.py example.py` | Exit 0 |
| Unit tests | `pytest` | Exit 0 — **full** suite |
| High+ audit | `pip-audit --strict --desc on` | Exit 0 (local editable package may log “not on PyPI”; exit must still be 0) |

### Agent constraints

- Do **not** run against production OddsHawk with real credentials unless Nathan explicitly scopes a live smoke
- Do **not** commit credentials, API keys, or filled-in `example.py` secrets
- Do **not** `pip publish` / Twine upload unless Nathan explicitly scopes a release

### Agent-only insufficient when

- Auth / hash header behaviour changes (needs human confirmation against live or staging API)
- Catalog method signature or response-shape changes that affect published consumers
- First packaging / PyPI publish (Nathan publish checklist)

## Adversarial review

### Required when

- Any change under `src/oddshawk_sdk/` (auth headers, URL building, catalog methods)
- Security-sensitive changes (credential handling, hash construction)
- More than five files changed in one handoff
- Packaging / publish metadata changes

### Subagent and brief

- Subagent: `bugbot` for diff review; `security-review` if auth, HMAC, or credential handling changes
- Provide: diff/branch, changed files, this doc's agent commands, link to [application.md](application.md)
- Block handoff on: critical/high findings unresolved

Primary agent must not self-review in the same context that wrote the code.

## Human handoff

Present to Nathan:

1. **Summary** — what changed and why (client API, auth, packaging, tests)
2. **Agent test results** — table of commands run and pass/fail
3. **Adversarial review** — verdict and open items (or "not required" with reason)
4. **Manual test steps** — e.g. set credentials, run `example.py` against staging/prod only if scoped
5. **Artifacts** — branch name, PR link, version bump / PyPI checklist if applicable
6. **Ask** — checklist: syntax/tests green, auth headers still correct, consumer impact, publish readiness
