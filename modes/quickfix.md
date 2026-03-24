---
name: quickfix
description: "Bug fix or small change with minimal ceremony"
category: development
core_skills:
  - superpowers:systematic-debugging
  - superpowers:test-driven-development
  - superpowers:verification-before-completion
  - kerd:switch
discover_keywords:
  - "bug"
  - "fix"
  - "patch"
  - "debug"
  - "regression"
---

## Setup

- [ ] `/kerd:switch` in light -- open session with minimal context
- [ ] Identify the problem -- reproduce the bug, confirm expected vs actual behavior

## Fix

- [ ] `/superpowers:systematic-debugging` -- trace root cause methodically
- [ ] Write regression test -- TDD: failing test that proves the bug exists
- [ ] Implement fix -- minimal change to make the test pass
- [ ] `/superpowers:verification-before-completion` -- confirm fix works, no regressions

## Close

- [ ] `/kerd:switch` out light -- close session with brief summary
