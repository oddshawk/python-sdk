---
type: Reference
title: Developer acceptance environment
description: How a developer runs this package locally and accepts a change by hand.
tags: [okf, acceptance, environment, python-sdk]
timestamp: 2026-11-13T00:20:00Z
---

# Developer acceptance environment — python-sdk

Additive to the OddsHawk developer acceptance environment standard `github:oddshawk/internal-documentation/okf-bundle/developer-acceptance-environment.md`.

## Prerequisites

| Need | Detail |
|---|---|
| Python | 3.10 or newer (`requires-python`); CI runs 3.12 |
| Packages | the package installed editable with its `dev` extra, in a fresh virtual environment |
| OddsHawk account | a username and its API password, exported to the shell as `OH_USER` and `OH_SECRET` |
| Reached service | the REST API at the client's base URL, `https://www.odds.software` by default |

## Start

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -e ".[dev]"`
3. `OH_USER=<username> OH_SECRET=<api-password> python example.py`

An `OH_USER` or `OH_SECRET` that is unset or empty ends the run before the first request, with `SystemExit("OH_USER and OH_SECRET must both be set")`.

## Running

Nothing is served: the package is a library and `example.py` is a stand-in program that runs in the calling process, so there is no address to open and no route to request. What a developer reads is the program's output on stdout.

For each sport it prints the sport's name, the `Available Markets:` label and that sport's markets payload; where the sport has a competition it goes on to print the first competition's name, and where that competition has an event it prints the event's name, its time and one odds record. The markets payload and the odds record are the API's response bodies as the client returns them, and the competition and the event appear by the name and time fields the API gives them. What is under acceptance is that walk: every step answers with the API's own records; a request the API rejects ends the run with `requests.HTTPError` carrying the API's status and body, and one that never reaches it ends the run with the `requests` transport exception (`requests.Timeout` or `requests.ConnectionError`).
