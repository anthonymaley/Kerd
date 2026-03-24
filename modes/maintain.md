---
name: maintain
description: "Health loop: structural, content, skill, and writing audits"
category: maintenance
core_skills:
  - kerd:tend
  - kerd:slainte
  - kerd:lorg
  - kerd:skriv
  - kerd:switch
discover_keywords:
  - "health"
  - "audit"
  - "drift"
  - "staleness"
  - "cleanup"
---

## Setup

- [ ] `/kerd:switch` in light -- open session with minimal context

## Audit

- [ ] `/kerd:tend` -- run structural health checks on project layout
- [ ] `/kerd:slainte` all -- run content consistency checks across all skills and docs
- [ ] `/kerd:lorg` -- scan for skill gaps or undiscoverable workflows
- [ ] `/kerd:skriv` audit on README and key docs -- check writing quality and voice

## Fix

- [ ] Address high-severity findings -- fix critical issues surfaced by audits
- [ ] Re-run checks -- confirm fixes resolved the flagged issues

## Close

- [ ] `/kerd:switch` out light -- close session with brief summary
