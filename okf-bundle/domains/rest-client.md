---
type: Reference
title: REST client
description: The module an application reads the odds catalog through and resolves a provider's names with, and the answers a caller can rely on.
tags: [okf, domains, rest-client, oddshawk-sdk]
timestamp: 2026-11-13T12:33:00Z
---

# REST client

`src/oddshawk_sdk/rest.py`: the file that defines the client an application reads the odds catalog and resolves a provider's own names through.

## Function

One client gives an application the odds catalog, and the resolution of a provider's own spelling of an event, a selection, a team or a competition to the OddsHawk canonical record.

## Guarantees

- Every read is an authenticated `GET` under the base URL the client was given ([request-signing.md](request-signing.md)).
- A catalog read answers the body the API returned, parsed as JSON; a read the API rejects raises, carrying the API's own status and error.
- A match helper answers the canonical match, or `False` when nothing resolves or the read fails.
- Every search key a caller passes with a value reaches the endpoint; the keys a catalog read honours are enumerated in the docblock of the read that takes them.

## Place in the application

The client is where an application reads the feed from: the package root yields it alongside the signature helper ([package-root.md](package-root.md), [request-signing.md](request-signing.md)).

The endpoints, the query surface and the matching contract are the API's, served by `github:oddshawk/rest-api`. `github:oddshawk/internal-documentation/okf-bundle/architecture.md` shows where that API sits in the feed, and [application.md](../application.md) is the business this package serves.
