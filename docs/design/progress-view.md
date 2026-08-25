# The progress view — show where we are

Living design doc. Owner: **Show where we are** (cross-cutting function
21). Source: the walk (push + pull, liveness at piece granularity) and
post-walk ratification (grows from the diagram toolkit, not a new skill).

## What it does

Answers "where are we?" with a RENDER, never a paragraph — pushed without
being asked, pullable at any moment, and alive enough during a long run
that motion is visibly different from hang.

## The two clocks

| Clock | Cadence | What it shows |
|---|---|---|
| **Liveness** | every piece boundary | the piece strip: **landed · in flight · remaining** — the running answer to "is it actually moving, or is that a static 'working…' line" |
| **Position** | every stage close · end of task · on pull | **have / need / progress** for ONE rung and for the whole board |

## The iron rules

- **Derived from disk, never self-reported.** Pieces commit as they verify
  and declarations live in artifacts (the state-in-artifacts property), so
  the renderer reads git and the declared files — the working model never
  gets to describe its own progress. A hung model produces no commits, and
  the strip shows it.
- **The push is a REPORT, never an ask.** It carries no question, so it
  costs the human nothing and never violates the hear-nothing escalation
  contract.
- **Never prose.**
- **The gate-close copy is a dated RECORD** (`docs/gates/` shape, diffable
  against the next one); the any-time view is living. The date split's
  standing rule.

## Callers

- **The entry gate** renders its have/need through this view — it never
  draws a view of its own.
- **The human**, by pull, at any time.
- **Every stage close**, by push — the render doubles as part of the gate
  record.

## Implementation

Grows from `tools/diagram/` — the toolkit already renders the map
(movement 11 is this function's first instance); it gains progress state:

- **Sources**: the work order's piece checklist · git log (a landed piece
  is a pushed commit) · gate records in `docs/gates/` · the walk-state
  table pattern (a table whose rows carry verdicts is already a
  have/need/progress render).
- **Board view**: the function map coloured by state — agreed / built /
  in-flight / missing — one glance answers "have / need" per rung.
- **Piece view**: the work order strip — landed (green-lit by commit) · in
  flight (the current piece) · remaining (queued) — ticking at piece
  boundaries.
- No new skill. The renderer is an instrument any function calls.
