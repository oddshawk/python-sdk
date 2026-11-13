---
type: Reference
title: Domains
description: Every module of python-sdk, the file that defines it, its function for the application, and the document that describes it.
tags: [okf, domains, modules, python-sdk]
timestamp: 2026-11-13T12:33:00Z
---

# Domains — python-sdk

The modules of `oddshawk-sdk`.

| Module | Defining file | Function | Document |
|---|---|---|---|
| Package root | `src/oddshawk_sdk/__init__.py` | What importing `oddshawk_sdk` gives an application: the client and the signature helper, which together are the package's whole public surface | [package-root.md](package-root.md) |
| REST client | `src/oddshawk_sdk/rest.py` | The odds catalog an application reads, and the matching that resolves a provider's own names to the OddsHawk canonical record, through one authenticated client | [rest-client.md](rest-client.md) |
| Request signing | `src/oddshawk_sdk/hashing.py` | The signature the API checks on every request, naming the second that request was made in | [request-signing.md](request-signing.md) |

[example.py](../../example.py) is the package's stand-in smoke program; [developer-acceptance-environment.md](../developer-acceptance-environment.md) § Running states what it prints.
