---
type: Reference
title: Application
description: Python SDK for the OddsHawk data feed
tags: [oddshawk-python-sdk, oddshawk, sdk, python]
timestamp: 2026-08-21T00:00:00Z
---

# Application

Installable Python client (`oddshawk-sdk` on PyPI) for the OddsHawk public odds REST catalog (`https://www.odds.software`). Consumers construct `Rest(user, key)` and call catalog helpers matching the public OpenAPI surface: `authenticate`, `version`, `sports`, `competitions`, `events`, `markets`, `providers`, `odds`. The `match_event`, `match_selection`, `match_team`, and `match_competition` helpers wrap the `/rest/match/*` endpoints — documented in the OpenAPI `Matching` section, authenticated like the rest of the API — and return `False` on failure (mirroring the JS SDK). Auth is username + time-based HMAC-SHA256 via `X-OH-User` / `X-OH-Hash` headers (same wire format as the JS SDK). No WebSocket client in this repo today (REST-first; WS is a follow-up).

## Runtime flow

1. Consumer installs the package (`pip install oddshawk-sdk` or editable `pip install -e .`) and imports `from oddshawk_sdk import Rest`.
2. Each public method builds a query string (`fromNow` as lowercase `true`/`false`) via `build_query`/`build_url` and GETs `base_url` + path with HMAC headers.
3. `generate_hash` (`hashing.py`) computes `sha256(key + str(unix_timestamp))` hexdigest concatenated with hex timestamp; sent as `X-OH-Hash` with `X-OH-User`.
4. Non-2xx responses raise `requests.HTTPError`; successful bodies are parsed as JSON and returned to the caller. The `match_*` helpers catch that (and transport/JSON errors) and return `False` instead, matching the JS SDK contract.

## Key modules

| Path | Role |
|------|------|
| `src/oddshawk_sdk/__init__.py` | Public exports: `Rest`, `generate_hash` |
| `src/oddshawk_sdk/hashing.py` | `generate_hash` — time-based HMAC-SHA256 header value |
| `src/oddshawk_sdk/rest.py` | `Rest` client: HMAC headers, `build_query`/`build_url`, catalog GET helpers, `match_*` helpers |
| `example.py` | Manual smoke script walking sports → markets → competitions → events → odds |
| `tests/` | pytest unit suite (hash / headers / URL building; no live API) |

## Environment variables

None required by the library. Credentials are constructor args (`user`, `key`). Do not commit real credentials in `example.py` or elsewhere.

## Deployment

- **Distribution:** PyPI (`oddshawk-sdk`) — Nathan publishes after green merge (cn-123).
- **CI/CD:** CircleCI `test` — pytest + blocking `pip-audit --desc on --skip-editable` (no `--strict` until first PyPI upload).
- **Runtime:** library only — no long-running service.

## Related systems

- **OddsHawk REST API** — `https://www.odds.software` (`/rest/odds*`, public catalog)
- **oddshawk-rest** — API implementation and OpenAPI/`/docs` (sibling www repo)
- **oddshawk-sdk** — JS sibling client (`@oddshawk/oddshawk-sdk`); same auth headers; includes WebSocket client this Python repo lacks
- **cn-127** — docs/SDK refresh that landed this catalog surface, packaging, and guides (this branch)
