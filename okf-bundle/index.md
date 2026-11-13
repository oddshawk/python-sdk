---
type: Reference
title: OKF bundle index
description: Entry point for the python-sdk OKF docs.
tags: [okf, oddshawk, python-sdk]
timestamp: 2026-11-12T21:40:00Z
---

# OKF bundle — python-sdk

The standard this bundle follows is
`github:oddshawk/internal-documentation/okf-bundle/documentation.md`; the organisation's repositories,
including this one, are listed in
`github:oddshawk/internal-documentation/okf-bundle/repositories.md`.

| Document | Content |
|---|---|
| [application.md](application.md) | What this package is, its function in the OddsHawk business, and the repositories it relates to |
| [dependencies.md](dependencies.md) | The dependency classes, human pins, holds, cross-repo consumers and the commands that verify them |
| [developer-acceptance-environment.md](developer-acceptance-environment.md) | How a developer starts the package locally, and what a change is accepted against |
| [documentation.md](documentation.md) | This repository's additions to the documentation standard |
| [domains/index.md](domains/index.md) | Every module, the file that defines it, its function, and the document that describes it |
| [domains/package-root.md](domains/package-root.md) | The package root: what importing `oddshawk_sdk` gives a caller and what it guarantees |
| [domains/rest-client.md](domains/rest-client.md) | The REST client: the odds catalog and name resolution an application reads, and the guarantees a caller holds it to |
| [domains/request-signing.md](domains/request-signing.md) | Request signing: what the signature proves to the API and what it guarantees |
| [git.md](git.md) | How the organisation git standard applies in this repository |
| [regular-updates.md](regular-updates.md) | The log of when each dependency class was last checked and last updated |
| [testing.md](testing.md) | The kinds of test, the command for each, and what is measured |

Repo-root [AGENTS.md](../AGENTS.md) points here.
