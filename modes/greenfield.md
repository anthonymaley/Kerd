---
name: greenfield
description: "Build a new feature from scratch using spec-driven development"
category: development
core_skills:
  - gsd:new-project
  - gsd:discuss-phase
  - gsd:plan-phase
  - gsd:execute-phase
  - gsd:verify-work
  - superpowers:brainstorming
  - superpowers:test-driven-development
  - superpowers:verification-before-completion
  - superpowers:requesting-code-review
  - kerd:switch
  - kerd:slainte
discover_keywords:
  - "feature"
  - "implementation"
  - "testing"
  - "code review"
  - "deployment"
---

## Setup

- [ ] `/kerd:switch` in -- open session, set context
- [ ] Confirm what we're building -- agree on scope and success criteria

## Spec

- [ ] `/gsd:new-project` -- generate roadmap and phase breakdown
- [ ] Review roadmap -- verify phases, flag gaps before building

## Build (repeat per phase)

- [ ] `/gsd:discuss-phase N` -- clarify requirements and edge cases for this phase
- [ ] `/gsd:plan-phase N` -- produce implementation plan with tasks
- [ ] `/gsd:execute-phase N` -- build the phase, TDD where applicable
- [ ] `/gsd:verify-work N` -- run tests, confirm phase acceptance criteria met

## Close

- [ ] `/kerd:slainte` -- run docs and structural health checks
- [ ] `/kerd:switch` out -- close session, persist handoff context
