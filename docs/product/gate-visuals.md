---
route: new
stage: ready-to-release
concerns:
  - concern: the life of a gate visual
    viewpoint: state
    view: docs/design/gate-visuals/visual-lifecycle.html
    approval: Tony, 2026-08-29 · fp:c4f3e8949191
  - concern: what the design gate refuses
    viewpoint: flowchart
    view: docs/design/gate-visuals/design-gate-check.html
    approval: Tony, 2026-08-29 · fp:d210312a9bec
---

# A visual at every gate, approved and locked

## Value

**Design is agreed in diagrams, and today a diagram costs a Python file.**
Measured 2026-08-22: 27 hand-written generators, 5,961 lines, one per drawing.
That is why *"design is agreed in diagrams, not prose"* keeps losing to prose —
the paragraph is free and the picture is a program.

The diagram-toolkit spike (`docs/design/diagram-toolkit-spike-findings.md`)
closed that: a drawing now costs a prompt and a lint pass.

**This item is what that unlocks.** Tony, 2026-08-22: *"EACH gate needs a
corresponding visual(s) that users can approve and lock in"* and *"we MUST have
visuals for the work that is in the design, so DB design needed, then we need to
show it, architecture needed, diagram must exist etc then we can compare design
with built."*

**Measured live during this item's own design, 2026-08-22.** The premise above
had never been measured; it has now, on the same producer in the same week:

| | Modality | Time to agreement |
|---|---|---|
| 39 requirements | text | ~a week — every block read, every reason written by hand, three rewrites of the wording before they were even readable |
| the visual lifecycle — 5 states, 7 transitions, an escalation rule | one drawing | **one exchange** — *"great diagram, love that… yes its correct"* |

His own remark on it: *"see how easy that was for me to agree."*

The drawing is not the simpler artifact. In prose that lifecycle is three
paragraphs the reader has to hold in their head to check. Drawn, the structure
**is** the argument, so checking it is looking at it. That is the whole of
*"design is agreed in diagrams, not prose"*, with a number attached for the
first time.

**Winning:** every gate has a picture the producer approved, the design is
declared truth rather than description, and a build that drifts from its own
design is detectable rather than discovered later.

## The prescription — Kerd is opinionated about the funnel

His constraint, 2026-08-22: *"kerd needs to be super onionated about what visuals
it shows for the funnel."* A menu means every session picks differently and the
funnel never looks like one thing twice.

**Opinionated means the vocabulary is closed, not that the count is one.**
Tony, 2026-08-22: *"gates can have MANY visuals, design and viablity and idea
etc."* A gate draws as many as the work needs — from its own declared set, and
from nowhere else.

| Gate | Its declared set | How many |
|---|---|---|
| **frame** | `it-state` the before picture · `fishbone` root cause · `journey` what a person does and feels · `venn` where two things overlap · `pyramid` what sits above what | as many as the idea needs — a frame with a legacy landscape *and* a root cause owes both |
| **viability** | `quadrant` impact against likelihood · `wardley` build, buy or outsource · `sankey` where the cost goes · `treemap` where the effort goes | one per question being answered. A build-versus-buy call and a cost question are two drawings, not one |
| **scope** | `story-map` release bands and the cut · `pyramid` when the cut is by rank · `treemap` when the cut is by size | usually one, more when the cut is argued on two grounds |
| **design** | `db-schema` · `er` · `architecture` · `deployment` · `sequence` · `state` · `flowchart` · `process` · `nested` · `dependency` · `swimlane` · `layers` · `tree` · `medallion` · `dp-integration` · `org-chart` | **one per concern the work declares.** The set is derived from the work, never chosen by whoever is drawing |
| **handoff** | `dependency` what lands before what · `org-chart` which role and model plays each piece · `swimlane` who owns which handoff · `dp-security-matrix` who may do what | as many as the work handoff needs |
| **loop** | the progress board | exactly one, and it is **the exception** — see below |
| **acceptance** | the design set **redrawn from what was built** · `bar` measured against target · `line` the trend · `scatter` the relationship · `timeline` what shipped · `loop` where the last step feeds the first · `fishbone` when the round-again was forced by something failing | one redraw per design drawing, plus whatever the measurement needs — and whatever explains a *round again* verdict |

**THIS COMPOSES WITH `docs/design/talk-formats.md`; IT DOES NOT REPLACE IT.**
Tony, 2026-08-22: *"we have the sensei story flows too for problems and
stories."* An earlier draft of this frame was rebuilding structure that already
exists, which is the thing Law 4 exists to stop.

The division is clean:

| | Owns |
|---|---|
| **talk-formats.md** | **the narrative** — which sections a communication owes, in what order, and which system moment triggers which format |
| **this item** | **the rendering** — how each of those sections is drawn, and which type it is drawn in |

They meet at a section. The format says *"you owe a Current Situation"*; the
aspect table below says a current situation about a database is drawn as
`db-schema` and one about a process is drawn as `process`.

**Two things this frame was reinventing, now pointed at instead:**

- **As-is and to-be** is **format 2, Compare & Contrast** — *Current Situation →
  New Situation*. Already specified, already mapped to *"say it in the user's
  terms"*.
- **Problem solving** is **format 8, Problem Solving A3**, whose sections already
  are *Happy path → As-is (GAP, measured) → Point of cause (TARGET) → Root cause
  (5 whys / fishbone) → Countermeasure & plan → Check / Monitor / Prevent /
  Share*. The as-is/to-be pair and the fishbone are both in it. This item does
  not restate them; it says how each section is drawn.

**And talk-formats already anticipated this work**, which is why it is a
continuation rather than a new idea: *"The diagram toolkit grows layout helpers
per format — a build item, not a precondition; until then formats are drawn by
convention."* The spike changes the mechanism — the third-party toolkit is
prompt-driven and has no generator, so it cannot be a layout helper inside
`kit.py` — but the need is the one already recorded there.

**One collision to settle at design, named here rather than discovered later.**
talk-formats' rendering rules say *colour marks cost (red), the human's input
(green), deltas (blue)*. The toolkit's central rule caps its accent at two
elements and says colour is editorial rather than a flag. Tony's ruling,
2026-08-22: *"color also we can give a little on, where we really need it is the
eval."* So funnel visuals yield on colour; the evaluation matrix, which is ours
and not drawn with this toolkit, keeps the grammar in full.

**THE WORK ITEM DICTATES THE VISUALS — they are derived, not chosen.**
Tony, 2026-08-22: *"work items dictate the need for visuals, DB design needs
schema, process needs …. architecture needs …. UI needs… etc etc."*

So a work item declares what it touches, and the required drawings fall out of
that declaration. Nobody picks. This is what makes the design gate countable
from outside the model rather than a judgement about whether enough was drawn:
**the gate counts drawings against declared concerns.**

| The work touches… | It owes… |
|---|---|
| a database | `db-schema` — real tables, types, constraints, foreign keys |
| a domain or data model | `er` — entities and cardinality |
| a business process | `process` — ordered steps with actors and the data between them |
| a process crossing teams | `swimlane` — because the handoff is the load-bearing part |
| system architecture | `architecture` |
| where it runs | `deployment` — hosts, environments, network boundaries |
| an API or an exchange between actors | `sequence` |
| a lifecycle or status | `state` |
| decision logic | `flowchart` |
| scope, trust or blast radius | `nested` |
| coupling between modules or services | `dependency` — including cycles a tree cannot show |
| tiered storage | `medallion` |
| an integration surface | `dp-integration` |
| roles and permissions | `dp-security-matrix` |
| team or agent ownership | `org-chart` |
| layered abstraction | `layers` |
| **a user interface** | **NOTHING — see the gap below** |

### The gap: there is no UI type, and UI is not a rare work item

**None of the 39 types draws a screen.** `journey` draws what a person does and
how they feel across stages; `flowchart` draws branching; `story-map` draws
release scope. **No wireframe, no screen layout, no navigation map, no
component hierarchy.**

That is a real hole rather than an oversight on our side, and it is not a
marginal one — a project using Kerd to build anything with an interface hits it
immediately, and *"UI needs…"* was named in the same breath as database and
architecture.

Under Law 4 this is exactly the sequence's fourth and fifth steps: adopt what
fits, **design for the gaps, build for the gaps.** The toolkit is adopted for
everything above the line; the UI row is ours to answer.

**Not answered here.** Naming it is the honest end of a frame; deciding what a
Kerd UI visual is belongs to design, and it may turn out that a screen is better
served by something other than a diagram.

**AS-IS AND TO-BE ARE A PAIR, AND BOTH ARE OWED.** Tony, 2026-08-22:
*"peoblem solving, as is - to be all need visuals."* An earlier version of this
table carried `it-state` — the before picture — and nothing for the after, so
there was nothing to compare it against. That is half a proposal.

The pair is already the house grammar: the A3 shape is *current situation drawn ·
numbered pains · proposal drawn · targets in units*, and a change stated in the
user's terms is *current → new → what changes*.

Three rules govern it:

1. **Where a change is proposed, both states are drawn.** As-is at **frame**;
   to-be at **frame** in outline and at **design** in full.
2. **Both are drawn in the SAME type.** An as-is in `it-state` and a to-be in
   `architecture` cannot be laid side by side — the difference between them
   reads as a difference in notation. Same type, same layout, so the only thing
   that changes between the two pictures is the thing that actually changed.
3. **The delta is named, not left to the eye.** What moved, what died, what is
   new. The colour grammar already carries this: red is cost, blue is changed
   since the producer last reviewed.

**Problem-solving work owes its own pair.** `fishbone` for the causes, plus the
current condition and the target condition in the same type — which is the
sensei route this repo already declares for a problem that survived a few
attempts to fix it. A root cause with no target condition is an explanation, not
a proposal.

**Two rules make this opinionated rather than a menu:**

1. **The set is closed.** A gate draws from its own row and from nowhere else.
   Reaching outside it is a defect, not a judgement call. **The rule binds the
   gate rows in the table above — those are the closed sets.**

   **Every type the aspect table owes now appears in some gate row**, which was
   not true before 2026-08-29: `medallion`, `dp-integration` and `org-chart`
   were added to `design`, and `dp-security-matrix` to `handoff`, where
   `docs/design/diagram-types-by-rung.md:40` assigns it. That is the claim this
   rule makes, and it is checkable by reading the two tables against each other.

   **What this document does NOT claim, because it would not be true.** The
   aspect table has no rung column, so *which* gate owes a given row is not
   readable from that table — it is a judgement made against the type map. And
   the type map disagrees with itself in ways this item cannot fix: its status
   column marks `db-schema`, `dp-integration`, `medallion` and `high-level` as
   design while its own DESIGN table omits all four; it marks `org-chart`
   handoff while listing it under DESIGN; and it still carries retired
   `BUILD`/`GOAL` headings. **Reconciling that file is `rung-vocabulary`'s
   outstanding editorial merge, filed in TODO.** Fixing it from here would take
   work belonging to another item's gate — it carries no seal, so the hazard is
   ownership, not fingerprints.

   A type may sit in a row and be owed by no aspect: in the design row `tree`
   is the only one (checked — 16 types in the row, 16 owed by the aspect table,
   `tree` the single spare). Other gates' rows carry types the aspect table
   never mentions, because that table is design-oriented. Spare capacity is not
   a contradiction — the rule forbids reaching *outside* a row, never leaving
   part of one unused.

2. **`quadrant` at viability keeps its axes.** Its own examples are Impact ×
   Effort; ours are impact against likelihood, **recorded separately and never
   multiplied** — expected value is the wrong maths for a bet taken once — and
   fatal is a band (impact ≥ declared value at any likelihood), not a cell.

**Three traps, excluded by name so nobody reaches for them:** `gantt` at scope
(a release is a grouping, not a time axis — a gantt makes time the definition);
`kanban` anywhere (a state census, which is the board, derived); `radar` at
viability (comparison between options is the evaluation matrix, ours, with 24
criteria and marks this has no equivalent for).

**Outside the funnel, nothing is prescribed.** A project using Kerd draws its own
system however it likes, with the full type set. Kerd is opinionated about its
own process and silent about your product.

**The design rung's gate is unchanged by this** — its two-key GO already says
*every aspect drawn and nothing left to annotate*. What changes is that the
aspect list is derived from what the work touches rather than chosen by whoever
is drawing.

## Approve and lock — reusing what already works

A visual becomes declared truth the same way a requirement does: **a fingerprint
over its content**, computed at approval, never typed. Change the drawing and the
approval invalidates, exactly as it does on a requirement today.

This is not new machinery. It is rule 9, `seal`, and invalidation, pointed at
pictures instead of blocks.

## Design against built

```
design gate   draw it · producer approves · fingerprint locks it
loop          the thing gets built
acceptance    redraw from what was built · fingerprint that · compare
```

**How checkable each aspect is, stated rather than promised:**

| Aspect | Built side derivable from | Strength |
|---|---|---|
| `db-schema` | migrations / DDL | strong |
| `dependency` | imports | strong |
| `deployment` | manifests / compose files | medium |
| `sequence` | traces, where they exist | weak |
| `architecture` | nothing — it is intent | eyeball only |

**Divergence is rare by design, and its frequency is the measurement.** Tony,
2026-08-22: *"if requirments are correct and visuals are approved then it
shouldnt happen and if it does it should be dealt with by conductor/composer."*
This is the same rule as the promotion beat (2026-08-07, *"really its a process
issue, that should only happen if we get requirements wrong?"*): a well-run item
never trips it, so an item that trips it often has a broken process upstream
rather than a noisy check.

**Who resolves it:** conductor or composer. The producer hears about it only when
neither can answer — the escalation contract already in the register.

## The one exception, kept visible rather than smoothed over

**The loop's visual is the progress board, which is derived from disk and
therefore cannot be approved or locked** — nobody authored it, so there is nothing to
fingerprint an agreement to. Every other gate's visual is authored, approved and
fingerprinted. That asymmetry is real. It is named here so nobody later "fixes"
it by making the board approvable, which would mean approving a fact.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
|---|---|---|---|---|---|---|---|---|---|
| A visual is approved without being read — the rubber-stamp failure, at picture speed | yes | an agreed drawing nobody looked at becomes declared truth, and every later comparison is against a fiction | medium | the register's own answer to false approval is presentational, named as an accepted residue on 2026-08-13 | fatal | accepted unknown | none yet — the producer's own ruling is that proper management plus strong pairing mitigates and does not cure |  | the first time a divergence traces back to an approved visual nobody had read |
| Prescribing one visual per gate makes a gate unpassable for work that genuinely has no such picture | no | a rung blocks on ceremony | medium | design already allows a declaration-driven set rather than a fixed one | non-fatal | countermeasure - permanent | the gate demands a visual **for each concern the work declares**; a work item declaring no such concern owes none, the same way `n/a` with a named reason works elsewhere |  |  |
| Redrawing from the built side is only strong for two aspects | no | the comparison is partial and could read as complete | high | measured in the table above | non-fatal | countermeasure - permanent | the strength column ships with the feature, so a weak comparison is labelled weak |  |  |
## Scope

Rigor level: mvp

**Slice 1 — the design rung only.** One gate, the declaration-driven set, approval and
fingerprint locking. No comparison yet.

**Slice 2** — the acceptance-gate redraw and comparison, starting with `db-schema` and
`dependency`, the two strong ones.

**Slice 3** — the remaining gates.

## Deliberately not in this item

- **The progress board.** Derived, byte-compared, not approvable — and the spike
  closed it to this toolkit permanently.
- **The evaluation matrix.** Ours already, machine-checked since v0.77.0.
- **Visuals outside the funnel.** A project's own domain drawings are free.
