---
type: Reference
title: Application
description: Python SDK for the OddsHawk data feed
tags: [oddshawk-python-sdk, oddshawk, sdk, python]
timestamp: 2026-08-21T00:00:00Z
---

# Application

Installable Python client for the OddsHawk public odds REST catalog (`https://www.odds.software`). Package name on PyPI: `oddshawk-sdk`. Consumers construct `Rest(user, key)` and call catalog helpers (`sports`, `competitions`, `events`, `markets`, `providers`, `odds`). Auth is username + time-based HMAC-SHA256 via `X-OH-User` / `X-OH-Hash` headers (same wire format as the JS SDK). No WebSocket client in this repo today.

## Runtime flow

1. Consumer `pip install oddshawk-sdk` (or editable `pip install -e .`) and `from oddshawk_sdk import Rest`.
2. Each public method builds query params and calls `__get`, which GETs `https://www.odds.software` + path with HMAC headers.
3. `__generate_hash` computes `sha256(key + unix_timestamp)` hexdigest concatenated with hex timestamp; sent as `X-OH-Hash` with `X-OH-User`.
4. Response body is parsed as JSON and returned to the caller.

## Key modules

| Path | Role |
|------|------|
| `src/oddshawk_sdk/__init__.py` | Public exports (`Rest`) |
| `src/oddshawk_sdk/rest.py` | `Rest` client: HMAC headers + catalog GET helpers |
| `example.py` | Manual smoke script walking sports → markets → competitions → events → odds |
| `tests/` | pytest unit suite (hash / headers; no live API) |

## Environment variables

None required by the library. Credentials are constructor args (`user`, `key`). Do not commit real credentials in `example.py` or elsewhere.

## Deployment

- **Distribution:** PyPI (`oddshawk-sdk`) — Nathan publishes after green merge (cn-123).
- **CI/CD:** CircleCI `test` — pytest + blocking `pip-audit --strict`.
- **Runtime:** library only — no long-running service.

## Related systems

- **OddsHawk REST API** — `https://www.odds.software` (`/rest/odds*`, public catalog)
- **oddshawk-rest** — API implementation and OpenAPI/`/docs` (sibling www repo)
- **oddshawk-sdk** — JS sibling client (`@oddshawk/oddshawk-sdk`); same auth headers; includes WebSocket client this Python repo lacks
- **cn-127** — parallel catalog/docs refresh (may deepen this SDK further)
