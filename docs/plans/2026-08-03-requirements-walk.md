# Requirements walk — agreeing the board, one at a time

Source of truth is `tools/diagram/gen_functions.py`, rendered into
`docs/plans/2026-08-02-product-to-build.excalidraw`. Two structures hold it:

- `DETAIL` — the interview. Four fields per function, in execution order:
  **in · grounding · out · acceptance** (movement 6). A function appears here
  only once it has actually been walked.
- `REQUIREMENTS` — the compressed MUST text (movement 9).

The old `ACHIEVED/GAP` line was neither a requirement nor an acceptance test —
it says whether the function *runs at all*. It now has its own view, movement 11,
which is the first concrete instance of the **Show where we are** function.

This file is the **walk state**. Tick as we go.

`(?)` in the MUST text = drafted by Claude, not read from evidence. 12 of them.

## Interview state

**1 of 25 functions interviewed.**

| Function | Interviewed | Flow drawn | Two-key approval |
|---|---|---|---|
| Frame the intent | yes — 2026-08-03 | `2026-08-03-frame-the-intent-flow.excalidraw` | machine: pass · human: pending |
| *all others* | not yet | — | — |

### Settled on *Frame the intent*

- **Triage is a branch inside one function, not a fork between two.** Three exits:
  NEW, PROBLEM, and QUESTION — which leaves the stage entirely and is answered
  from *Hold product truth*. Framing a question as a feature is how invented work
  gets started.
- The routes **diverge at grounding (4)**, stay apart through **output (6)**, and
  **rejoin at acceptance (7)** — shared machinery, route-specific checklist.
- **Two documents, not one shape with optional sections**: an *idea brief* and a
  *problem statement*. Both are `.md` + diagram; the sections differ.
- **Sensei is a tool, not a MUST.** Invoked when its route matches — asserting a
  position, proving a gap with measurement, or a complex problem needing point of
  cause and 5 whys. Trigger: *a problem that survived a few attempts to fix it.*
  Same rule for superpowers and every external tool: it declares the route it
  serves and is invoked on match.
- **Both routes hand off to Test viability.** The killer assumption differs, the
  test does not. A problem statement going straight to design is the
  jump-to-countermeasure failure, and the risk is highest on that route.
- **Acceptance is two keys** — machine (sections, measurements, pattern
  conformance, next stage's inputs filled) and human (Tony approves). Neither
  alone passes.

### Debt left on this function

1. The route-specific acceptance checklists are named but not written.

## Agreed 2026-08-03 — *Where the work is written down* (cross-cutting)

**Date records of events. Never date living documents.** The test is one
question: *would rewriting this tomorrow be correct, or would it be falsifying
the record?* Correct → living, no date, git history is the archive. Falsifying →
a record, dated, never rewritten.

This is the split `switch` already runs — `CONTEXT.md` overwritten in place,
`kivna/sessions/` immutable and dated. Second caller for a working mechanism,
not a new invention.

| Path | Holds | Kind |
|---|---|---|
| `docs/product/<slug>.md` | idea brief / problem statement | living |
| `docs/product/<slug>.excalidraw` + `.svg` | its diagram, **same slug** | living |
| `docs/gates/<date>-<slug>-<rung>.md` | gate-close record | immutable |
| `kivna/sessions/<date>.md` | session history (already exists) | immutable |
| vault | human-read narrative, never duplicating git | living |

Same slug across the pair is what makes the name derivable. Front matter carries
`route: new \| problem` and the stage, so route-specific acceptance is
machine-checkable.

**Still open:** *reachable*. Naming solves findability, not reachability — the
6 Jul design doc that held 1 Aug's answer was perfectly well named and went
unread because nothing pointed at it.

**Not done, deliberately:** the repo's 30 files in `docs/plans/` all use the
dated shape, including living documents like the board (`2026-08-02-…`, rewritten
six times on 08-03). Renaming is a rip; nothing gets ripped until the design is
approved. Rule is forward-only for now.

| # | Rung | Requirement | MUSTs | (?) | Verdict |
|---|---|---|---|---|---|
| 1 | PRODUCT | Frame the intent | 1 | 0 | open |
| 2 | PRODUCT | Test viability | 1 | 0 | open |
| 3 | PRODUCT | Hold product truth | 2 | 0 | open |
| 4 | PRODUCT | Slice a release · Set the goal | 1 | 0 | open |
| 5 | PRODUCT | Choose what matters next | 2 | 0 | open |
| 6 | DESIGN | Shape the solution | 1 | 0 | open |
| 7 | DESIGN | Agree the shape | 1 | 0 | open |
| 8 | DESIGN | Decide what proves it | 1 | 0 | open |
| 9 | DESIGN | Design the interface → approved | 2 | 1 | open |
| 10 | CONTRACT | Write the contract · Size and assign | 1 | 0 | open |
| 11 | BUILD | Execute a unit · Prove it worked | 2 | 0 | open |
| 12 | BUILD | Review unanchored | 1 | 0 | open |
| 13 | BUILD | Refuse bad work | 1 | 0 | open |
| 14 | BUILD | Verify against what we said | 1 | 0 | open |
| 15 | SESSION | Open / close · Keep tempo · Hold state | 1 | 0 | open |
| 16 | SESSION | Route to the altitude | 1 | 0 | open |
| 17 | SESSION | Drive to done  (/goal + /loop) | 2 | 0 | open |
| 18 | SESSION | Keep context optimal (inside the loop) | 1 | 1 | open |
| 19 | CROSS-CUTTING | How we talk to each other | 4 | 4 | open |
| 20 | CROSS-CUTTING | Do we have what we need? (entry gate) | 3 | 0 | open |
| 21 | CROSS-CUTTING | Show where we are | 3 | 1 | open |
| 22 | CROSS-CUTTING | Size work to a model | 2 | 1 | open |
| 23 | CROSS-CUTTING | Where the work is written down | 5 | 4 | open |
| 24 | CROSS-CUTTING | Stay in control of external tools | 1 | 0 | open |

Verdicts: `open` · `agreed` · `reworded` (text changed, then agreed) · `split`
(became more than one requirement) · `dropped`.

When a row is agreed, edit the MUST text in `gen_functions.py`, drop its `(?)`,
regenerate, and set the verdict here. The diagram and this file move together —
neither is a snapshot of the other.
