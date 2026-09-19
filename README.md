# OddsHawk Python SDK

Python client for the OddsHawk REST API — the public odds catalog plus the `/rest/match/*`
matching helpers.

Interactive API docs: https://odds.software/docs/

## Installation

```bash
pip install oddshawk-sdk
```

From a local checkout (editable):

```bash
pip install -e ".[dev]"
```

## Quickstart

```python
from oddshawk_sdk import Rest

client = Rest("your-username", "your-api-password")

# Optional: confirm credentials / API version
client.authenticate()
print(client.version())

# Catalog walk (same surface as the public OpenAPI paths)
sports = client.sports(from_now=True)
print(sports)

markets = client.markets(True, {"sport": "Football"})
competitions = client.competitions(True, {"sport": "Football"})
events = client.events(True, {"sport": "Football"})
providers = client.providers(True, {"sport": "Football"})

odds = client.odds({
    "sport": "Football",
    "provider": "Bet365",
    "limit": 10,
})
print(odds)
```

Auth on every request: `X-OH-User` + `X-OH-Hash` (SHA-256 of `password + unixSeconds`, hex digest, with unix seconds appended as lowercase hex). Same wire format as the JS SDK and OpenAPI security schemes.

Default base URL is `https://www.odds.software`. Override with `Rest(..., base_url="https://...")` if needed.

## Catalog methods

| Method | Path |
|--------|------|
| `authenticate()` | `GET /authenticate` |
| `version()` | `GET /rest` |
| `sports(from_now=True)` | `GET /rest/odds/sports` |
| `competitions(from_now, search_params)` | `GET /rest/odds/competitions` |
| `events(from_now, search_params)` | `GET /rest/odds/events` |
| `markets(from_now, search_params)` | `GET /rest/odds/markets` |
| `providers(from_now, search_params)` | `GET /rest/odds/providers` |
| `odds(search_params)` | `GET /rest/odds` |

Internal / admin routes are out of scope for this soft-launch package. The `/rest/match/*`
helpers are covered under [Matching](#matching).

## Matching

`/rest/match/*` resolves provider-supplied names to OddsHawk canonical entities. It is documented
in the OpenAPI `Matching` section and, like every other `/rest` endpoint — `/rest/odds` included —
it is available to any **authenticated** account (the same auth headers as every other call).

| Method | Path |
|--------|------|
| `match_event(provider, name, time, sport, init=False)` | `GET /rest/match/event` |
| `match_selection(provider, name, time, sport, event_name, init=False)` | `GET /rest/match/selection` |
| `match_team(provider, name, time, sport, init=False)` | `GET /rest/match/team` |
| `match_competition(provider, name, time, sport, init=False)` | `GET /rest/match/competition` |

```python
from oddshawk_sdk import Rest

client = Rest("your-username", "your-api-password")
match = client.match_event("Bet365", "Arsenal v Chelsea", 1734567890, "Football")
if not match:
    # no canonical match (also returned on any failure — mirrors the JS SDK)
    ...
```

- `name` is the name to resolve (a canonical name, provider spelling, or known alias); `time` is the
  event start in unix seconds; `sport` is required.
- `event_name` is required by `match_selection` and must be the **canonical** event name (e.g. the
  `event.name` returned by `/rest/match/event`) — it is used by the Betfair Exchange lookup.
- `init=True` registers an unresolved name for curation — the call that registers it still returns `False`.
- `provider="Betfair Exchange"` uses an exact stored-odds lookup instead of the canonical dictionary
  (except `match_team`, which has no Betfair Exchange branch).

Full guide: https://odds.software/guides/matching.md

## WebSocket

This package is **REST-first**. Live WebSocket subscribe/update (available in `@oddshawk/oddshawk-sdk`) is a follow-up — not included here.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Do not commit credentials. `example.py` is a manual smoke script only.

## Soft-launch notes

Entitlements / usage response headers and reserved error codes (`feed_down`, `catalog_dropped`, `payment_required`, etc.) are forthcoming with upstream API work — this SDK does not depend on them yet.

PyPI publish is Nathan-only (cn-123).
