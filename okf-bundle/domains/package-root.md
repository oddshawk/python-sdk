---
type: Reference
title: Package root
description: What importing oddshawk_sdk gives a caller, and what that surface guarantees.
tags: [okf, domains, package-root, oddshawk-sdk]
timestamp: 2026-11-13T12:33:00Z
---

# Package root

`src/oddshawk_sdk/__init__.py`: the file that defines the surface a caller imports the package by.

## Function

One import yields the package's whole public surface: the REST client ([rest-client.md](rest-client.md)) and the signature helper ([request-signing.md](request-signing.md)).

## Guarantees

- One account credential covers both: the key an application gives the client is the key the signature helper takes.

## Place in the application

A customer's application begins at the package root: the odds feed this package serves is reached through the client and the signature it yields. [application.md](../application.md) is the business the package serves, and `github:oddshawk/rest-api` is the API the client calls.
