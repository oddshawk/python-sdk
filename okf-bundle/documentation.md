---
type: Reference
title: Documentation
description: This repository's additions to the OddsHawk documentation standard, including what its customer-facing documents may say.
tags: [okf, documentation, docblocks, python-sdk]
timestamp: 2026-11-12T23:53:00Z
---

# Documentation — python-sdk

The OddsHawk documentation standard `github:oddshawk/internal-documentation/okf-bundle/documentation.md` applies here. The additions below are all this repository makes to it.

## Additions

| Area | Addition |
|---|---|
| Generated reference | None is produced or published: no generator is configured and the package carries no generated artefact |
| Consumer-facing description | [../README.md](../README.md) is the document a customer reads; this bundle is the maintainer-facing one, starting at [index.md](index.md). § Consumer-facing documents states what that document and the shipped sources may say |
| Tests and documents | Document content is guarded by review, not by a test; what a suite may assert is [testing.md](testing.md) § Repo rules |

## Consumer-facing documents

[../README.md](../README.md) and the shipped sources are the two documents a customer reads. They name a provider only as an example in a sample call, never as a recommendation or a ranking, and they describe neither the feed's composition nor any per-provider branch of the API, which is maintainer-only material recorded in `github:oddshawk/rest-api/okf-bundle/application.md`. They carry no internal work reference.

They state the metered behaviour as live, with no reserved or forthcoming wording, as `github:oddshawk/rest-api` serves it: the `X-Data-Points-This-Hour`, `X-Data-Points-Limit` and `X-Hour-Resets-At` response headers on the metered routes, `GET /rest/account`'s throttle block, `403 {"error":"coverage_not_entitled"}` and `429 {"error":"throttled"}`. A code the API does not yet emit is described as planned.

## Adversarial review

The documentation standard's acceptance bar (`github:oddshawk/internal-documentation/okf-bundle/documentation.md` § 3) covers every pull request; in this repository the diff also goes to a review subagent (`bugbot`, or a fresh review-only agent) when it touches `src/oddshawk_sdk/`, when it changes authentication or hash generation, when it changes packaging or publish metadata, or when it changes more than five files in one handoff — with the branch, the changed files and [testing.md](testing.md) § Commands. A critical or high finding blocks the handoff until it is resolved. The author does not review the diff in the same context that wrote it.
