# The rung vocabulary — design

The design package for the work item `rung-vocabulary`. The thing being changed
is the ladder itself: the names of its gates, what each gate checks, and what
state an item reaches when it comes out the far end.

The frame settled the ladder's shape and deliberately left three things for
design. This document settles them, and settles a fourth the frame did not know
it had.

## Grounding

- docs/product/rung-vocabulary.md — the frame, and the currency test across all eight rungs
- docs/design/rung-vocabulary/the-ladder.html — sealed view: why loop is a container and acceptance is the producer's last gate
- docs/design/rung-vocabulary/rungs-and-artifacts.html — sealed view: what each gate checks and what each renamed word costs
- tools/gates/kit.py — `RUNGS` (34), `STAGES` (35), `GATE_RECORD_RE` (93), `check_rung`, `route`, `stage_ahead`
- tools/gates/README.md — the canonical home of the rung vocabulary and the gate-record schema
- docs/design/funnel-driver.md — the six work types this vocabulary must read across
- CONTEXT.md — the currency rule, Law 4's supersession clause, the cross-cutting sweep obligation

External sources are cited inline below rather than listed here: `## Grounding`
resolves every reference against the filesystem, so a URL is always refused
(Backlog row filed 2026-08-23).

## Acceptance creates READY-TO-RELEASE — DECIDED 2026-08-25

The producer's ruling, and it is the spine of this document:

> acceptance means ready for release, not done. So the concept is settled, but
> the wording needs to stop implying finality. The producer is not declaring the
> work "done forever" or "released"; they're declaring it **fit to release**.

So, in his own enumeration:

| Thing | Value |
|---|---|
| What the gate is | the producer's **ready-for-release** gate |
| `stage:` value | `ready-to-release` |
| Gate record | `docs/gates/<date>-<slug>-acceptance.md` |
| Required section | `## Release condition` — **not** `## Done condition` |
| How prose and UI say it | *"accepted as ready for release"* — never *"done"* |

**`## Release condition` is chosen over `## Ready-for-release condition`** on
length alone; both were offered and they mean the same thing. It sits inside a
gate record named `-acceptance.md`, so the context is unambiguous and the shorter
form loses nothing.

**Why the wording matters enough to be a ruling rather than a preference.** Drive
moves content plans, business plans, documents and repairs as well as software.
For none of those does the work stop at the gate — a released document gets
revised, a shipped business plan gets re-forecast, a completed repair gets
inspected. `done` asserts an ending that the ladder's own loop contradicts, and
it asserts it in the one record that outlives everything else. The state the
producer is actually creating is *fit to release*, which is a property of the
work, not a verdict on its future.

## The three things the frame left open

### 1. The `stage:` values — SETTLED

`STAGES` goes from seven values across eight rungs to seven across seven, one per
gate:

| Rung | `stage:` value | Was |
|---|---|---|
| `frame` | `framed` | `framed` |
| `viability` | `viable` | `viable` |
| `scope` | `scoped` | `sliced` |
| `design` | `designed` | `designed` |
| `handoff` | `handed-off` | `contracted` |
| `loop` | `looping` | `building` |
| `acceptance` | `ready-to-release` | `done` |

Four values change. **Two of the four touch nothing on disk**: `contracted` and
`building` are legal values no work record has ever used (`grep -rl '^stage:
contracted' docs/product/` returns nothing, same for `building`). The migration
is `sliced` in 2 files and `done` in 6 — eight files, not twenty-one.

`handed-off` and `looping` are hyphenated and gerund respectively because the
`stage:` field states *what has been reached*, and both read naturally that way.
`ready-to-release` is hyphenated for the same reason every other value is one
token: it is a parser value, and a space would make it ambiguous against prose.

### 2. `loop` or `learn` — SETTLED AS `loop`

The producer's call, 2026-08-25. No evidence arrived either way since the frame
raised it, and the frame's own rule applies: changing a name that passes the
currency test on a hunch is precisely the failure this item exists to prevent.

`learn` also mis-describes the container. What runs inside is build, verify and
adjust — learning may happen, but it is not what the loop is *for*, and a name
that describes a hoped-for side effect rather than the mechanism is the class of
name the currency rule was written against.

### 3. What marks an item ready to release — SETTLED, AND IT CLOSES A BREAK IN THE IRON RULE

The frame recorded this as an accepted unknown: *"today the last rung is `loop`,
so a finished item reports `enters at: loop` forever; with `acceptance` last the
same ambiguity moves rather than resolving."*

**Checking the code found the problem is worse than the frame described, and the
fix is better.** `STAGES` already ends in `done` and six work records declare
`stage: done` today — but `route()` never reads `stage:` at all. It walks
artifacts. So **doneness is declared by a human editing front matter and derived
from nothing**, at the one position where the derived-from-disk rule matters
most: the board's own definition of finished.

The settled answer: **`ready-to-release` becomes a derived terminal position, not
a declared one.**

- `route()` gains one terminal case. When every rung's inputs exist — including
  the acceptance record with its `## Release condition` section — it reports
  `ready-to-release` rather than naming the last rung again.
- The evidence is the acceptance record on disk. A human can no more type an item
  into `ready-to-release` than they can type it into `designed`.
- `stage: ready-to-release` in front matter stays as the item's own declaration,
  and `stage_ahead` refuses it when the artifacts are not there — the same
  declaration-versus-evidence check every other stage already gets.

This is the smallest change that closes the break, and it is a change the frame
did not know was available because the frame had not read `route()`.

## The gates were holding the wrong things

Settled 2026-08-25 on the producer's correction — *"scope, that is not a risk
ledger. its where we lock in what we want, what features etc."* — and recorded in
full in the frame and CONTEXT.md. The design-level statement:

| Gate | Checks, after | Checks, before |
|---|---|---|
| `viability` | `## Value` exists · killer risks **named** in the ledger | `## Value` exists |
| `scope` | `## Scope` (in, out, rigor level) · **every** ledger row qualified | `## Risk ledger` qualified |
| `design` | one sealed view per declared concern | `## Release slice` + rigor + sealed views |

**`## Release slice` is renamed `## Scope` and moves up one gate.** It cannot keep
a retired word in its own name. 17 work records carry it.

**The risk ledger does not move.** One section, read at two depths: viability
wants killer risks named and accepts no sizing or evidence; scope wants every row
sized, evidenced, and in exactly one state. The reasoning, the refutation that
produced it, and the evidence tiers are in CONTEXT.md.

**A consequence the design must own: five work records go backwards on the board.**
`diagram-toolkit`, `requirements-project-type-templates`, `requirements-view`,
`standards-grounding` and one more carry `## Value` and no risk ledger. They
report `enters at: slice` today; with killer risks required at viability they
will report `enters at: viability`. That is more honest than what they say now —
none of them has ever had a risk named — but it is a visible regression and it is
declared here rather than discovered on the board.

## The alias rule extends from filenames to section names

The frame settled that a retired name is **an alias for reading, never for
writing**, on the producer's test: *"if the intent is to keep writing goal.md
forever, then `goal` is not really folded away."*

That rule was written about filenames. This design extends it to section names,
because the acceptance ruling retires one:

| Retired | Replacement | Read forever | Written from now |
|---|---|---|---|
| `docs/gates/*-goal.md` | `docs/gates/*-acceptance.md` | 7 records | acceptance only |
| `## Done condition` | `## Release condition` | those same 7 records | Release condition only |
| `slice` (rung) | `scope` | records, front matter | scope only |
| `contract` (rung) | `handoff` | no records exist | handoff only |
| `stage: done` | `stage: ready-to-release` | 6 work records | ready-to-release only |

All 7 existing goal records carry `## Done condition` (`grep -rl '^## Done
condition' docs/gates/` returns 7), so the reader must accept it forever or the
project's own immutable history becomes unparseable. **No file on disk is ever
renamed and no record is ever rewritten.**

**The rule that makes this a retirement rather than a synonym:** the parser's
legal set is a union of live names and retired aliases; the *writer* only ever
emits live names. Two live names for one thing is the defect this item exists to
remove, and an alias that is still written is a second live name.

## The sweep, measured

Done at design time per the standing cross-cutting rule (born at `vault-unhook`:
any slice touching system-wide behaviour owes a `grep -rn` sweep at design, not
at build). Immutable history — `docs/gates/`, `kivna/sessions/` — is excluded
throughout, because none of it is ever rewritten.

| Site | Count | Note |
|---|---|---|
| Parser keys per renamed rung | 3 each | `RUNGS` (kit.py:34), `STAGES` (kit.py:35), `GATE_RECORD_RE` (kit.py:93) |
| `## Release slice` → `## Scope` | 17 work records + 8 hits in `tools/` | the expensive one |
| `stage:` values changing | 8 files | `sliced` ×2, `done` ×6; `contracted` and `building` are unused |
| `## Done condition` → `## Release condition` | 4 in kit.py + 2 living docs | plus 7 gate records read-only forever |
| `contract` as a rung in generators | 5 files | `gen_flow_contract.py` (a filename), `gen_journey.py:57`, `gen_functions.py:47` and `:637`, `gen_flow_design.py:97`, `gen_flow_celtic_example.py:128` |
| `goal` as a rung in `skills/` + gates README | 5 hits | |
| Rendered artifacts with the words baked in | 23 `.excalidraw`/`.svg` under `docs/plans/` | regenerate from the generators, never hand-edit |

**The finding this sweep produced, and it reverses a claim the drawing made
twice:** `contract → handoff` was described as the cheap rename because no gate
record was ever written at that rung. That is true and it is not the cost. The
word is a **generator filename**, a rung key in three more generators, and baked
into rendered output — so the rename that writes no history still edits more code
than the one that does.

## Named answers — the stage-1 measurements

| Measurement (frame, `### Value, in units`) | Target | Named answer |
|---|---|---|
| Rung names readable across all six declared work types | 5 of 8 → 7 of 7 | **Not machine-measurable, and not claimed to be.** The evidence is the currency test recorded in the frame, run against two questions per rung and against fetched sources. Verified at build only in the weak sense that all seven names are the tested ones. Declared limit: no checker can read a name for cross-work legibility, and a later reader disagreeing is the real test. |
| Rung names with no term-of-art collision | 7 of 8 → 7 of 7 | **Met only under the qualification rule, stated rather than glossed.** `handoff` collides with switch's session handoff — 15 uses in `skills/switch/SKILL.md` alone. The producer ruled the collision a benefit if qualified consistently, so the target is met by *"session handoff"* / *"work handoff"* in living prose, not by the word being unique. Verified at build: `grep -rn '\bhandoff\b' skills/ docs/design/` returns zero bare uses in ambiguous position. |
| Rung names a newcomer can search and get this meaning | 5 of 8 → 7 of 7 | Same class as the first row — a judgment, not a count. The strongest available evidence is that `scope of work` is standard in construction, consulting and law, and `handoff` in construction, manufacturing, healthcare and journalism. No checker. |
| Route positions that blur machine work with producer approval | 2 → 0 | **Machine-verifiable.** The two were old `goal` (a pure machine test named like a producer's target) and old `loop` (a human key named like iteration). After the fold, every route position is either a machine check or a producer key and never both. Fixture: `route()` on a fully-built slug returns `ready-to-release`, and `enters_at` is never `goal`. |
| Execution mechanics exposed as producer-visible gates | 2 → 0 | **Machine-verifiable.** Fixture asserting `enters_at ∉ {build, verify, adjust}` for every slug, and that `RUNGS` contains none of those three. This is the check that keeps the loop a container rather than quietly re-flattening into rungs. |

Rows one and three are honestly unmeasurable by machine and are recorded that way
rather than given a number invented after the fact — the gap `gate-visuals` left
open at its goal gate, not repeated here.

## Open questions

- **The `design` gate can now check nothing.** With `## Scope` moved out, design's
  only check is one sealed view per *declared* concern, and the concerns block is
  optional. A work item declaring no concerns passes design with zero checks.
  This is true today too, but moving `## Scope` out makes design the only gate
  that can be empty. Not answered here; it is a question about whether declaring
  a concern should itself be mandatory, which is `gate-visuals`' territory.
- **`## Release condition` versus the release-planning artifact.** A release is a
  grouping, not a time axis (2026-08-03), and that artifact has never been built.
  When it is, `## Release condition` on a per-item gate record and a release as a
  set of items will both be using the word. Flagged now so it is a known
  collision rather than a discovered one.
- **Does re-agreeing a lapsed approval cost anything?** Carried from the frame,
  still untested. If coming back means re-walking the gate, early gates must not
  lock at all.

## What this design does NOT do

- **It does not build anything.** No `kit.py` edit, no rename, no migration. That
  is slice 1, and it needs a contract spec.
- **It does not touch `docs/product` → `docs/work`.** Measured at ~180 references
  in `funnel-driver` slice 3. Two cross-cutting renames in one commit make the
  collateral check unaffordable, which is the whole reason that check exists.
- **It does not rename the four rungs that pass.** `frame`, `viability`, `design`
  and `build` are current and cross-work.
- **It does not fix the `design`-gate hole or the viability thinness beyond risk.**
  Named above, owned elsewhere.

## The limit, stated

**This design changes what the gates are called and what they hold. It cannot
change whether anyone reads them.** Every check here is a file-existence or
section-existence test; none of them reads content for meaning. `## Scope` at the
scope gate proves a section is present, never that the scope is right. Killer
risks *named* at viability proves rows exist, never that the real killer is among
them. That is the same declared limit the register carries — a fingerprint proves
words have not changed since approval, never that they were the right words — and
this item does not narrow it.

**And one thing genuinely gets worse before it gets better:** the terminal state
becomes derived, which means an item can no longer be declared finished by hand.
That is the point, and it will surface work records whose `stage: done` was
optimistic. Six of them exist. Expect the board to look worse immediately after
slice 1 lands, and expect that to be the truth arriving rather than a regression.
