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

**6 of 25 functions interviewed — PRODUCT RUNG COMPLETE, DESIGN RUNG COMPLETE (collapsed 4→1). 1 cut. 1 added. 3 folded.**

| Function | Interviewed | Flow drawn | Two-key approval |
|---|---|---|---|
| Frame the intent | yes — 2026-08-03 | `2026-08-03-frame-the-intent-flow.excalidraw` | machine: pass · human: pending |
| Test viability | yes — 2026-08-03 | `2026-08-03-test-viability-flow.excalidraw` | machine: pass · human: pending |
| Slice a release · Set the goal | yes — 2026-08-03 | `2026-08-03-slice-a-release-flow.excalidraw` | machine: pass · human: **reviewed** |
| Choose what matters next | yes — 2026-08-03 | `2026-08-03-choose-what-matters-view.excalidraw` | machine: pass · human: pending |
| What we ruled out, and why | **added 2026-08-03** (cross-cutting) | `2026-08-03-what-we-ruled-out-flow.excalidraw` | machine: pass · human: **reviewed** |
| Hold product truth | **CUT 2026-08-03** | — | — |
| Design the solution | yes — 2026-08-03 (was "Shape the solution" + 3 folded in) | `2026-08-03-design-the-solution-flow.excalidraw` | machine: pending · human: pending |
| *all others* | not yet | — | — |

### Settled on *Design the solution* (DESIGN rung collapsed 4→1)

- **The four-way DESIGN split was Claude's decomposition of the superpowers
  brainstorming checklist, never Tony's shape.** Tony: "i dont know what agree
  the shape is or shape the solution - they are the superpowers skill." His
  answers describe ONE conversation producing ONE package.
- **The package:** detailed specs, architecture plans, testing strategy, solution
  diagrams, flow diagrams, visualizations for as many aspects as we can.
- **Acceptance is two keys:** every aspect drawn and nothing left to annotate
  (human) · every stage-1 measurement has a NAMED ANSWER in the package
  (machine/trace). The measuring itself is post-build conformance.
- **Home (chosen A over folder-per-piece-of-work):** `docs/design/<slug>.md` +
  `.excalidraw`, living, undated, same slug as the product doc. GO writes a dated
  gate record `docs/gates/<date>-<slug>-design.md` and hands to CONTRACT — never
  to `writing-plans` (today the working half of brainstorming exits into the dead
  half: "The terminal state is invoking writing-plans", superpowers 5.0.6).
- **Grounding gained two entries from measured failures:** standing decisions
  (or settled ground gets re-litigated) and the living design docs of whatever
  the work touches — the exact class whose retrieval failed on 08-02. Second
  caller for reachability.
- **Diagnostic, from the installed skill text (5.0.6):** bundles five of our
  functions in one flow; prose sections with per-section approval (a sequence of
  clarifications); "multiple choice preferred"; dated-snapshot artifact in a
  third home (`docs/superpowers/specs/`). The 2-3-approaches capability is the
  part that earned its keep.

### Settled on *Slice a release · Set the goal*

- **A release is a GROUPING, not a time axis.** Time may be attached later, or
  never — ordering and scheduling are separable, and conflating them turns a
  grouping decision into a deadline argument. (Corrects the 2026-08-02 record.)
- Five factors decide a grouping, and they do not work alike: **dependency** is a
  hard constraint that forbids groupings outright; **how much a user can absorb at
  once** is a ceiling — a release can be too big even when everything in it is
  finished; **effort, risk and opportunity** are trade-offs that shape what is
  left. The ceiling is the unusual one: the bound comes from the receiving side,
  not from capacity, which is why "we shipped everything we had" is a real failure.
- **Risk arrives pre-qualified from Test viability and is not re-assessed.** A
  feature carrying a temporary countermeasure is a different slicing candidate
  from one carrying a permanent fix.
- **The DONE condition is ASSEMBLED, never authored.** Every item is a conformance
  check against something an upstream rung already declared. That dissolves the
  circular draft ("specific enough to terminate a loop") — it is specific enough
  exactly when every item points at a declaration that exists.
- **Nothing may be in DONE that nothing declared.** An unbacked item cannot be
  checked, so it passes by assertion — the unqualified-risk failure in another
  costume. This rule resolved two orphans without new functions: *user testing* is
  a proof layer declared by *Decide what proves it*, and *documentation complete*
  is derived rather than declared — every declaration covered.

### Added 2026-08-03 — *What we ruled out, and why* (cross-cutting)

Four functions independently demanded this output and none had a home for it:
gaps that could not be closed (function 1), accepted unknowns and blockers
(function 2), "work we discounted" in documentation (function 4), and "what was
deliberately not built" when *Hold product truth* was cut.

- **Its own artifact, reviewable in one pass.** Inside each solution doc, "what
  have we already ruled out?" cannot be answered without reading all of them.
- **A rejected approach and a failed fix are the same thing** — an option
  eliminated. One was eliminated by analysis, the other by a test, and those are
  the same kind of evidence differing in cost, as agreed at function 2. Splitting
  them was smuggling back a distinction already dissolved.
- **The unit is the CONCEPT, not the attempt, and not the code.** Concepts outlive
  codebases; a diff does not. Many failed attempts at one idea are one entry.
- **The filter is: was it ever a candidate?** Did someone believe it, for a
  reason? A slip is not an option.
- **It is read in GROUNDING by every function that proposes anything** — which is
  what stops a dead option being re-proposed, and makes it an input rather than a
  graveyard. It is also a second caller for grounding, and partly answers the
  still-open reachability clause: it gets read because a rung cannot start
  without it.
- **Capture must be a byproduct of work already happening.** A failed verify IS
  the record. Running the maintenance risk through function 2's own machinery:
  impact high (a stale "already tried" list is worse than none — the argument
  that killed *Hold product truth*), likelihood high, countermeasure none —
  which by Tony's rule is a dead project, so byproduct capture is not an
  optimisation but the condition of it existing at all.
- Each entry carries the **condition that would bring it back**. Third thing today
  with a return condition, which suggests a general rule rather than three
  coincidences.

### Settled on *Choose what matters next*

- **The failure is not bad ranking — it is items that cannot be weighed.** Three
  things missing, and only one is about order: no diagram, no clear structure
  (same shape per item), no clear ask. "Too much noise" is not volume; a list of
  prose titles gives you nothing to compare, however short.
- **Two constant axes, both about OUTCOME: consequence × value.** Consequence is
  what it costs us not to do it; value is what we gain. Value is already declared
  by *Frame the intent* and already used by *Test viability* — third caller for
  the same number rather than a new measure.
- **Effort is not an axis.** An input measure beside two outcome measures makes
  the grid incoherent, and it systematically flatters cheap work. Tested live:
  under effort×consequence, "repin the three repos" rose as a cheap win; under
  value it fell correctly to pure hygiene — high consequence, no value. "The
  SPIKE" rose for the mirror reason. Effort survives as a tiebreaker inside a
  cell and as one of the five slicing factors at *Slice a release*.
- **Each item names WHAT WE LOSE by not choosing it** — v0.68's rule applied to
  work. A ranked list shows what you picked and never what you gave up.
- **Blocked items are separated, not ranked.** A dependency is a hard constraint,
  so they are not candidates at any consequence.
- Kerd's own switch-in pick-list is an instance of this gap: a numbered menu
  ordered by position in TODO.md, title-only, no consequence, no value, no loss.

### Cut 2026-08-03 — *Hold product truth*

Cut on its own test. Asked whether any question had ever needed answering that
**the code could not answer**, the answer was no.

The argument for cutting is stronger than the argument that built it:

- The code is the truth for mechanism and sequencing. Tony's own examples —
  *"how do we ingest data from x or y?"*, *"do we check authentication at this
  step or before?"* — are all answerable from the running system. A parallel
  document is a second source that drifts, and a drifted document answers
  confidently and wrongly.
- The one measured failure behind this function was **retrieval, not absence**.
  The 6 July design doc that held 1 August's answer *existed*. Another document
  cannot fix a retrieval problem.
- What is genuinely not in the code — why a step sits where it does, what was
  deliberately not built, what the thing is worth — is **already produced by
  Frame the intent**.

What survives, relocated:

- **Retrieval** → the still-open `reachable` clause of *Where the work is
  written down*.
- **Intent and value** → `Frame the intent`, which already writes them.
- **The QUESTION exit** from function 1 keeps its value and changes its
  destination: answered *from the code*, still never framed as new work.

**Return condition:** a question arises that the code cannot answer. This is a
temporary countermeasure with a named trigger, not a permanent deletion — the
same discipline agreed for risks in function 2, applied to a design decision.

### Settled on *Frame the intent*

- **Triage is a branch inside one function, not a fork between two.** Three exits:
  NEW, PROBLEM, and QUESTION — which leaves the stage entirely and is answered
  **from the code** (revised 2026-08-03 when *Hold product truth* was cut).
  Framing a question as a feature is how invented work gets started.
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
| 1 | PRODUCT | Frame the intent | 1 | 0 | **walked** |
| 2 | PRODUCT | Test viability | 6 | 0 | **walked** |
| 3 | PRODUCT | Hold product truth | — | — | **CUT** |
| 4 | PRODUCT | Slice a release · Set the goal | 6 | 0 | **walked** |
| 5 | PRODUCT | Choose what matters next | 6 | 0 | **walked** |
| 6 | DESIGN | Design the solution | 6 | 1 | **walked** (folded 7–9 in) |
| 7 | DESIGN | ~~Agree the shape~~ | — | — | **folded into 6** (2026-08-03) |
| 8 | DESIGN | ~~Decide what proves it~~ | — | — | **folded into 6** (2026-08-03) |
| 9 | DESIGN | ~~Design the interface → approved~~ | — | — | **folded into 6** (2026-08-03) |
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
| 23 | CROSS-CUTTING | Where the work is written down | 5 | 1 | **agreed** (reachable still open) |
| 24 | CROSS-CUTTING | Stay in control of external tools | 1 | 0 | open |

| 25 | CROSS-CUTTING | What we ruled out, and why | 6 | 0 | **walked** (new) |

Verdicts: `open` · `agreed` · `reworded` (text changed, then agreed) · `split`
(became more than one requirement) · `dropped`.

When a row is agreed, edit the MUST text in `gen_functions.py`, drop its `(?)`,
regenerate, and set the verdict here. The diagram and this file move together —
neither is a snapshot of the other.
