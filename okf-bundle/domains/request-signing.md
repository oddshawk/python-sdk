---
type: Reference
title: Request signing
description: The signature the OddsHawk API checks on a request, and what a caller can rely on.
tags: [okf, domains, request-signing, python-sdk]
timestamp: 2026-11-13T08:35:00Z
---

# Request signing

`src/oddshawk_sdk/hashing.py`: the file that defines the signature helper.

## Function

The proof the OddsHawk API checks on a request: that the caller held the account's key for the second
the value names.

## Guarantees

- The sibling JavaScript client at `github:oddshawk/node-js-sdk` produces the same value for a given
  key and second, and the API's security scheme accepts it.
- One key and one second always answer the same value.

## Place in the application

The signature is what a caller of the package root receives beside the client
([package-root.md](package-root.md)), and what every request the REST client makes carries
([rest-client.md](rest-client.md)).

The scheme that accepts the value is the API's, served by `github:oddshawk/rest-api`;
[README.md](../../README.md) § Quickstart states the wire construction in the form a reimplementation
follows.
