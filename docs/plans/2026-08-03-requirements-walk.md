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

`(?)` in the MUST text = drafted by Claude, not read from evidence. 1 remains (Design the solution: machine-checkable interface values).

## Interview state

**THE WALK IS COMPLETE — all 25 functions accounted for (2026-08-04). 15 walked/agreed, 1 cut, 5 folded, 3 dissolved, 1 added. Every rung: PRODUCT, DESIGN (4→1), CONTRACT, BUILD (4→2 + property), SESSION (4→1 + property), CROSS-CUTTING (5 + the reachable clause). Two properties promoted system-wide: the ROLE LADDER and STATE-IN-DECLARED-ARTIFACTS; the refusal property carries from BUILD.**

| Function | Interviewed | Flow drawn | Two-key approval |
|---|---|---|---|
| Frame the intent | yes — 2026-08-03 | `2026-08-03-frame-the-intent-flow.excalidraw` | machine: pass · human: pending |
| Test viability | yes — 2026-08-03 | `2026-08-03-test-viability-flow.excalidraw` | machine: pass · human: pending |
| Slice a release · Set the goal | yes — 2026-08-03 | `2026-08-03-slice-a-release-flow.excalidraw` | machine: pass · human: **reviewed** |
| Choose what matters next | yes — 2026-08-03 | `2026-08-03-choose-what-matters-view.excalidraw` | machine: pass · human: pending |
| What we ruled out, and why | **added 2026-08-03** (cross-cutting) | `2026-08-03-what-we-ruled-out-flow.excalidraw` | machine: pass · human: **reviewed** |
| Hold product truth | **CUT 2026-08-03** | — | — |
| Design the solution | yes — 2026-08-03 (was "Shape the solution" + 3 folded in) | `2026-08-03-design-the-solution-flow.excalidraw` | machine: pass · human: **reviewed** |
| Write the contract · Size and assign | yes — 2026-08-03 | `2026-08-03-write-the-contract-flow.excalidraw` | machine: pass · human: **reviewed** |
| Build a piece · Prove it + Prove the whole · Goal gate | yes — 2026-08-03 (BUILD rung, one flow) | `2026-08-03-build-flow.excalidraw` | machine: pass · human: **reviewed** |
| Drive to done (SESSION rung, one flow — 15/16/18 dissolved into it) | yes — 2026-08-04 | `2026-08-04-session-flow.excalidraw` | machine: pass · human: **reviewed** |
| *all others* | not yet | — | — |

### Settled on CROSS-CUTTING (2026-08-04) — the walk is COMPLETE

- **Function 20 (Do we have what we need?) is a thin gate riding the ladder.**
  Its residue: check the DECLARED inputs of the rung about to start
  (mechanical — declarations exist on disk or they don't), name exactly what
  is missing, render via *Show where we are*, honour a declared SPIKE as the
  one licensed bypass. The push-back is NOT its own mechanism — a refusal is
  "a question the spec cannot answer" raised at the gate ("that is probably a
  subagent telling conductor and we go into that problem loop to get answers
  or provide info or make adjustments and if not it waits for me").
- **SYSTEM-WIDE PROPERTY — the role ladder.** Three callers emerged
  independently: the contract's escalation, the loop's questions, the gate's
  refusals. By the three-callers heuristic it is a property of the whole
  system, not a feature of any function: **every blocker, question, and
  refusal anywhere rides ONE ladder — answered at the lowest role with the
  knowledge and the authority, escalated only on genuine inability; the human
  is the last rung.**

- **Function 21 (Show where we are): push AND pull.** Pushed at every stage
  close and end of task ("it should be pushed at each stage or end of a task
  but if not i can ask for it or go pull it myself"); pull available at any
  time. The push is a REPORT, never an ask — it carries no question, so it
  does not violate the hear-nothing escalation contract (the ladder governs
  asks; the render is ambient visibility). The gate-close copy is a dated
  RECORD (`docs/gates/` shape) while the any-time view is living — third
  caller for the date-records-of-events split, resolving the `(?)`. Machine
  callers: the entry gate (renders through this, never its own view);
  movement 11 is the first instance.
- **21 addendum — LIVENESS during a long task is vital** ("if i can see where
  we are at then i can work on other things without wondering if the long
  task is actually moving and not just a static line on claude code
  'working...'"). The view must distinguish motion from hang at PIECE
  granularity: pieces landed · in flight · remaining, updated at every piece
  boundary. Free by construction — pieces commit as they verify, so the
  render derives from disk, no self-reporting by the working model.
- **Function 22 (Size work to a model): the declaration that makes the ladder
  computable.** Every dispatching function declares tier + effort + why,
  sized AFTER the work is written, never the top tier for difficulty alone —
  the `(?)` resolves to a requirement. Wrong sizes surface to NO human ("i
  dont need to see it"): a too-small model is caught by the piece's own
  failing check, re-sized and re-dispatched by the roles; it reaches Tony
  only as a role-unanswerable blocker on the ladder. His window stays
  liveness, "confirmation of activity not hang".
- **Function 24 (Stay in control of external tools): a tool is staffed like a
  player.** The driving role DECIDES which tools are needed ("conductor needs
  to decide what tools are needed and have control over them"); every
  invocation carries a bounded contract — do this, don't do that, return in
  this shape, to the caller ("do this but dont do that and return with x or
  y to me"); the caller holds KILL authority over a rogue task — control
  from outside the tool. The tool never names the next step: brainstorming's
  never-came-back failure is the class this forbids. Standing rules absorbed:
  route declared, invoked on match never obligation; what is NOT adopted
  named before invocation; Kerd's contract wins conflicts.
- **Function 19 (How we talk to each other) — three requirements from Tony,
  2026-08-04.** (1) A question to him is clear, visual, obvious — no
  rambling, no ambiguity, no noise; speech bubble + border marks a question
  needing his answer; a DECISION question carries five things in the
  simplest terms: what it is · why it matters · what the gap is · what we
  win · what we lose. Non-simple questions and issues use the TPS/A3
  storylines; a diagram on the whiteboard is a legitimate question form
  ("we can even just pop a diagram on excalidraw for me to whiteboard with
  you"). (2) GROUND BEFORE ASKING: no assumptions or inferences before the
  source is read — "if there is a problem GO TO THE CODE or documents first,
  or session history… THEN ask." (3) NEVER assume his position — unsure
  means ask. (2)+(3) are one rule, the ladder applied to questions: **facts
  are never asked, positions are never guessed** — a fact question dies at a
  lower rung (code/docs/history); a position question has exactly one
  source, him. Three of the four `(?)` dropped by evidence (diagrams,
  round-trip, story format all proven since drafting); the fourth —
  the enforcement point — stays, resolved BY the refusal property: a talk
  rule that cannot bind from outside the model is advisory (the one rule
  that holds today is held by a hook firing on every prompt).
  (4) STRAW-MAN YOURSELF FIRST: before raising a question or problem, ask
  "is that really true or accurate?" — self-review before spending anyone
  else's attention. A question or problem must survive its own refutation
  attempt before it travels the ladder; a raised issue that dies on first
  contact with its own evidence was noise, not signal.
- **The `reachable` clause CLOSED (2026-08-04)** — the walk answered it
  twice before naming it: reachability = **named in at least one function's
  declared grounding, enforced by the entry gate.** Not a property of the
  artifact but of the ladder's declared reads. Lost becomes a CHECKABLE
  state: an artifact in no grounding list is lost by declaration, and a
  machine can say so. The 6 Jul doc went unread because nothing's grounding
  pointed at it; the cost of the fix is discipline — every new artifact
  home is written into some function's grounding or it doesn't exist.

### Settled on the SESSION rung (4→1 + a rung-wide property)

- **Function 15 (Open / close · Keep tempo · Hold state) dissolves into a
  property: state lives in the declared artifacts, never in the session;
  anything worth keeping is written the moment it exists.** A session may die
  at any instant and the loss is bounded to the in-flight piece, redone from
  its spec. Sessions end *between* pieces by construction — the cut-point is
  chosen, not suffered ("why would sessions end mid flight"). Open/close has
  no job left (opening = read the work order); tempo (commit as it verifies)
  already belongs to BUILD. Third caller for byproduct capture (after failed
  verifies and mid-session decision recording), which by the three-callers
  heuristic makes it a property, not a coincidence.
- **Finding against current tooling:** today's boundary machinery defers some
  capture to close-out (gotchas, reflections written at switch-out) — exactly
  the loss window the property forbids. Logged for the post-walk skill-change
  definition, not fixed now.
- **Function 16 (Route to the altitude) dissolves into the entry gates in
  series.** Work enters at the LOWEST rung whose declared inputs all exist —
  a resumed build passes straight in because its declarations are on disk; a
  bare idea is pushed up rung by rung to *Frame the intent*, whose triage
  sorts idea / problem / question. No dispatcher decides anything. What
  survives as requirement: nothing passes THROUGH a gate on assertion —
  missing inputs push work up, never through. **The one licensed bypass is a
  SPIKE**: declared up front, cheap, built to generate evidence for a
  kill-or-keep decision; "just build it" is the anti-pattern for MVP work
  ("mvp needs measurable results and a spec that can be reliably built
  against, risks recorded"). A spike that wants to become real work re-enters
  at the top with its evidence. The "sherpa is an orphan" gap is answered
  structurally: gates route; nothing needs to reference a dispatcher.
- **Function 17 (Drive to done) is the rung's one surviving function.** The
  loop: next unblocked item → build and prove → goal check → repeat,
  unattended. Own requirements (the rest it consumes from upstream): runs
  unattended ONLY where every gate can block from outside the model; every
  question answered at the lowest role with the knowledge AND authority to
  answer it, escalating only on genuine inability, human last ("the conductor
  role will answer the questions based on spec… if not then it truly
  something only i can answer… we pause and wait for me"); while a question
  waits on the human, nothing may be built that the pending answer could
  invalidate — park-vs-stop is the driving role's call ("the conductor can
  decide that"); stops at goal achieved or a human-level blocker; cuts and
  resumes fresh between pieces whenever conditions degrade. Fills the
  escalation contract's missing middle: the ladder of roles that must fail
  before Tony hears anything.
- **Function 18 (Keep context optimal) DISSOLVES structurally.** The draft's
  `(?)` was honest — quality-degradation has no signal. It stays unneeded:
  two-tier access means each piece runs on exactly its slice; the session
  property means the driver restarts between pieces at zero cost. When
  cutting costs nothing, no degradation detector is needed — cut liberally,
  even per piece. The `(?)` dissolves by making the missing signal
  unnecessary, not by finding it.
- **Rung shape: 4 → 1 + a rung-wide property** — the same collapse DESIGN
  (4→1) and BUILD (4→2+property) took. The property: state lives in the
  declared artifacts, never in the session.

### Settled on the BUILD rung (4→2 + a rung-wide property)

- **Build a piece · Prove it:** done = measured against ALL RELEVANT specs and
  measurements — the piece's own criteria plus everything its change touches,
  relevance scoped by the overseer — and tests match the acceptance criteria /
  goal. "Relevant" is what covers collateral: the swallowed-helpers class shows
  up because neighbouring terrain is relevant by construction. No human key per
  piece.
- **Prove the whole · Goal gate** (absorbs *Review unanchored* and *Verify
  against what we said*): cold eyes on the whole change — work order + change
  only, verdict can BLOCK — once per goal and on demand for risky pieces, never
  routinely per piece. The flaw class cold eyes catch is a gap in the DECLARED
  TRUTH itself, and those live at assembly. Then per-layer conformance (code,
  logic, architecture, pixel vs design, product measurements — never one
  verdict), then the human key: **the expert-user pass** — Tony uses the output
  itself ("im checking it as the expert user"). This is the GOAL ACHIEVED
  report of the escalation contract.
- **Refuse bad work is not a function — it is the rung-wide property:** every
  gate on this rung must be able to block from OUTSIDE the model. Advisory
  output is not a check. (Today: 0 CI workflows, 0 pre-commit hooks, every
  repo.) The CI build item stays in the MVP sequence as this property's first
  concrete instance.

### Settled on *Write the contract · Size and assign* (CONTRACT rung complete)

- **The design package arrives INTACT** — full specs, documents, diagrams,
  measurements, plans, UX design, systems. The contract is written from
  upstream truth, never from a digest.
- **Two-tier access, by role:** the overseer holds all upstream truth; a
  builder gets the exact spec for their piece plus access to related
  materials, and no more.
- **No human gate at contract time** — provided every piece is measurable
  against an upstream declaration. Tony: *"i dont need to approve contract if
  we can measure it meets output of other stages."* A piece nothing declared
  is a push-back to design, not a silent pass — DONE-assembled applied to the
  contract itself. (This removes today's per-spec user approval when the
  machine key holds.)
- **Escalation contract:** the human hears only of a gap no agent role can
  answer that is a blocker; otherwise the next report is goal achieved.
  (Stricter than today's behaviour of surfacing score-corrections before
  making them.)
- **Carried from v0.66, now requirement-level:** implementable by a builder
  who never saw the reasoning; every piece carries its own check; sized and
  assigned after the piece is written.

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
| 10 | CONTRACT | Write the contract · Size and assign | 6 | 0 | **walked** |
| 11 | BUILD | Build a piece · Prove it (was Execute a unit) | 4 | 0 | **walked** |
| 12 | BUILD | ~~Review unanchored~~ | — | — | **folded into 14** (2026-08-03) |
| 13 | BUILD | ~~Refuse bad work~~ | — | — | **became the BUILD rung-wide property** (2026-08-03) |
| 14 | BUILD | Prove the whole · Goal gate (was Verify against what we said) | 8 | 0 | **walked** |
| 15 | SESSION | ~~Open / close · Keep tempo · Hold state~~ | — | — | **became the SESSION rung-wide property** (2026-08-04) |
| 16 | SESSION | ~~Route to the altitude~~ | — | — | **dissolved into the entry gates** (2026-08-04) |
| 17 | SESSION | Drive to done  (/goal + /loop) | 3 | 0 | **walked** |
| 18 | SESSION | ~~Keep context optimal (inside the loop)~~ | — | — | **dissolved by construction** (2026-08-04) |
| 19 | CROSS-CUTTING | How we talk to each other | 4 | 0 | **walked** (four rules 2026-08-04) |
| 20 | CROSS-CUTTING | Do we have what we need? (entry gate) | 3 | 0 | **walked** (thin gate riding the ladder) |
| 21 | CROSS-CUTTING | Show where we are | 4 | 0 | **walked** (push+pull, liveness) |
| 22 | CROSS-CUTTING | Size work to a model | 2 | 0 | **walked** (makes the ladder computable) |
| 23 | CROSS-CUTTING | Where the work is written down | 5 | 0 | **agreed** (reachable CLOSED 2026-08-04) |
| 24 | CROSS-CUTTING | Stay in control of external tools | 3 | 0 | **walked** (a tool is staffed like a player) |

| 25 | CROSS-CUTTING | What we ruled out, and why | 6 | 0 | **walked** (new) |

Verdicts: `open` · `agreed` · `reworded` (text changed, then agreed) · `split`
(became more than one requirement) · `dropped`.

When a row is agreed, edit the MUST text in `gen_functions.py`, drop its `(?)`,
regenerate, and set the verdict here. The diagram and this file move together —
neither is a snapshot of the other.
