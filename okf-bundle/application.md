---
type: Reference
title: Application
description: What the oddshawk-sdk Python client is, its function in the OddsHawk business, and how it relates to the organisation's other repositories.
tags: [okf, oddshawk, python-sdk, oddshawk-sdk]
timestamp: 2026-11-13T12:10:00Z
---

# Application

## What it is

`github:oddshawk/python-sdk`: the Python client library for the OddsHawk customer odds feed. Its
distribution name, as `pyproject.toml` declares it, is `oddshawk-sdk`. Its modules and the files that
define them are [domains/index.md](domains/index.md).

## Function in the business

OddsHawk collects odds from bookmakers and other sources, normalises them to canonical events,
markets and selections, and serves them over an authenticated REST API. This package is the Python
side of that contract: a customer's application reads the feed through it and is answered in
OddsHawk's own canonical terms, leaving authentication and request construction to the library.

## Relation to other repositories

`github:oddshawk/internal-documentation/okf-bundle/architecture.md` shows how the feed's components
join together; this section is only this repository's place in it. Repositories are named as their
organisation repository, which `github:oddshawk/internal-documentation/okf-bundle/repositories.md`
lists.

| Repository | Relation |
|---|---|
| `github:oddshawk/rest-api` | serves the authenticated REST API this client calls |
| `github:oddshawk/node-js-sdk` | the JavaScript client for the same REST API, with the same authentication wire format |
| `github:oddshawk/internal-documentation` | the organisation bundle this repository's documents point at |
