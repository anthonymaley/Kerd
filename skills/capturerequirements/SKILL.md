---
name: capturerequirements
description: "Use when the user says 'capture requirements', 'capturerequirements', 'lock requirements', 'what do we actually need', or wants to pin down the must-haves for a piece of work before building. Interview-based and lightweight — separates MVP-now from later. Not the exhaustive viability sweep that /kerd:interrogate runs; this just gets you moving."
---

# Capture Requirements

A fast, interview-based way to lock the requirements you actually need before building — the front door of the JIT flow. The point is momentum: pin the MVP must-haves, defer everything else, start building. It is deliberately *not* `/kerd:interrogate` (which exhaustively stress-tests viability across every axis and produces a readiness document). This is lighter — enough to build the first slice, no more.

## Principle

Build the features you need, not the ones you think you need. Requirements you can't tie to the core outcome go to **Later**, not into the build. When in doubt, defer it — JIT will surface it again if it's real.

## How it works

Interview the user **one question at a time** (speech-bubble style — short, clear, one ask). Drill the question that most unblocks the build. Do not enumerate multiple-choice menus or bundle questions. After each answer, reflect it back in a line and ask the next.

Cover only what's needed to start:

1. **Outcome** — what does done look like? One sentence.
2. **Must-haves** — the smallest set of capabilities without which the outcome fails.
3. **Explicitly not now** — what's tempting but out of the MVP. Name it so it stops competing for attention.
4. **Constraints** — any hard limits (tech, time, must-not-break).
5. **First slice** — the smallest valuable thing we can build and show.

Stop as soon as the first slice is clear. Don't keep interviewing for completeness — that's interrogate's job. If a requirement is genuinely uncertain, write it as an open question rather than inventing an answer.

## Output

Write a short requirements note to `docs/requirements/YYYY-MM-DD-<topic>.md`:

```
# Requirements — <topic>

**Outcome:** <one sentence>

## MVP (now)
- <must-have>
- <must-have>

## Later (deferred)
- <deferred>

## Constraints
- <constraint>

## First slice
<the smallest valuable thing to build and show>

## Open questions
- <anything genuinely unresolved — don't invent answers>
```

Keep it short. This note is a starting point the JIT loop revises as you learn — not a contract. When a slice teaches you something, come back and update it.

## Relationship to other skills

- **vs `/kerd:interrogate`** — interrogate is exhaustive readiness across every viability axis, co-signed, for high-stakes plans. capturerequirements is the quick MVP lock to start moving. Use interrogate when the cost of being wrong is high; use this when the cost of *not starting* is high.
- **In `jit` mode** — this is the Reqs step. The thin spec and MVP build follow; the loop feeds learnings back here.
