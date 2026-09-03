# risk-state-split — design

The design package for `docs/product/risk-state-split.md`: the risk ledger's
one `State` column becomes two fields — **Severity** (how damaging the risk
would be if it happened) and **Treatment** (what we are doing about it, and
whether that treatment is proven) — shipped with its migration in one commit.

Three views, one per declared concern, sealed on the producer's key:

- `docs/design/risk-state-split/two-axis-vocabulary.html` — the legal values
  and every Severity × Treatment verdict
- `docs/design/risk-state-split/migration-map.html` — the 84 live rows through
  the migration classes to one atomic commit
- `docs/design/risk-state-split/hollow-treatment.html` — what proves a
  treatment, and the Evidence-field conflict exposed

Grounding: the keyed scope in the work record; `tools/gates/kit.py`
(`LEDGER_COLUMNS` :61, `LEGAL_STATES` :70, `_normalize_state` :423,
`parse_ledger` :440); the producer's three rulings at the design-plan gate
(2026-09-03, recorded in CONTEXT.md `## Key Decisions`).

## The two-axis vocabulary

The ledger grows from eight columns to ten. Exact header, in order:

```
| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
```

- **`State` is replaced by `Severity` and `Treatment`** — the split the item
  exists to make.
- **`Evidence` is renamed `Risk evidence`** and keeps its 2026-08-03 meaning
  unchanged: what sizes the risk — a test or an analysis, impact in the
  value's units. The rename is what exposes the conflict the producer named:
  one cell called just "Evidence" was about to become two kinds of fact.
  Cell contents do not change; the header row rewrites at migration anyway.
- **`Treatment evidence` is new**: what proves the treatment — see
  [Hollow treatment](#hollow-treatment-made-checkable).

**Severity — legal values and definitions:**

| Value | Definition |
|---|---|
| `fatal` | impact >= declared value, at any likelihood (the 2026-08-03 definition, unchanged) |
| `non-fatal` | impact < declared value |
| *(empty)* | named, not yet qualified — workflow incompleteness, refused at the viability gate. Never a legal durable value (the producer's ruling, 2026-09-03) |

Why two values and not a scale: the machinery branches on exactly one
severity distinction — fatal or below it — and no gate, board, or skill
consumes a finer grade. A three- or five-level scale would be invented
precision with no consumer, and every extra grade multiplies the
producer-review batch the migration already owes. `non-fatal` is defined by
the same inequality that defines `fatal`, so it needs no definition of its
own; any other word would.

**Treatment — legal values, unchanged from today's four:**

`countermeasure - permanent` · `countermeasure - temporary` · `accepted` ·
`accepted unknown` · *(empty = named, not yet qualified — refused at
viability, same as Severity)*

`fatal` leaves the set: it was never a treatment. Normalization
(`_normalize_state`) applies to both new fields unchanged: lowercase,
em-dash and `--` to `-`, whitespace collapsed.

## Refusal semantics

Per-row checks after the split. Obligations carried over unchanged:
`Treatment: countermeasure - *` requires a non-empty `Countermeasure`;
`Treatment: accepted*` requires a non-empty `Review trigger`.

The full Severity × Treatment matrix. A fatal row's evidence demand is a
**lifecycle**, not a parse rule — see
[Treatment assurance over time](#treatment-assurance-over-time):

| | `countermeasure - permanent` | `countermeasure - temporary` | `accepted` | `accepted unknown` | *(empty)* |
|---|---|---|---|---|---|
| **`fatal`** | **PASSES** — planned `Treatment evidence` before acceptance, resolving at acceptance. The combination this item exists to make representable | **PASSES** with its return condition named (`Review trigger` non-empty) — temporary means *carries a return condition*, not *expires before protecting this increment* (the producer's ruling); same evidence lifecycle | REFUSED — the one blocker that cannot be accepted by name (2026-08-03) | REFUSED — same ground | REFUSED — not yet qualified |
| **`non-fatal`** | passes (Countermeasure required) | passes (Countermeasure required) | passes (Review trigger required) | passes (Review trigger required) | REFUSED — not yet qualified |
| ***(empty)*** | REFUSED — not yet qualified | REFUSED | REFUSED | REFUSED | REFUSED |

**Exact refusal strings** (design-rung decision per the scope; each names its
fix). Parse-level — every gate that reads the ledger:

- `row N: Severity empty — named, not yet qualified; qualify at viability`
- `row N: Treatment empty — named, not yet qualified; qualify at viability`
- `row N: Severity '<raw>' not a legal value (legal: fatal, non-fatal)`
- `row N: Treatment '<raw>' not a legal value (legal: countermeasure - permanent, countermeasure - temporary, accepted, accepted unknown)`
- `row N: Countermeasure empty (required when Treatment is countermeasure)`
- `row N: Review trigger empty (required when Treatment is accepted)`
- `row N: Review trigger empty (required when Severity is fatal and Treatment is countermeasure - temporary — a lapsing protection on a fatal risk must name its return condition)`
- `row N: Treatment evidence empty (required when Severity is fatal) — declare the planned proof ('planned — <what will exist> · <expected location>') or cite the verified one`
- `row N: Treatment evidence is neither 'planned — <what will exist> · <expected location>' nor a resolving citation`
- `FATAL risk '<risk>' with no countermeasure — record in What we ruled out; cannot pass`

Acceptance-level — the acceptance rung check only:

- `fatal risk '<risk>': treatment still planned, not verified — acceptance requires resolving Treatment evidence`

Today's FATAL refusal narrows twice: it fires only on `fatal` +
`accepted` / `accepted unknown` / empty treatment — never on a fatal risk
carrying a real countermeasure. The shape of the "What we ruled out" home
stays the open question it already is (CONTEXT.md `## Open Questions`) —
this design changes which rows are sent there, not where "there" is.

The old-schema refusal (fixture 1's message) names the migration:
`Risk ledger header row must be exactly: <new header> — this record carries the pre-split schema; migrate State to Severity + Treatment`.

## Hollow treatment made checkable

**The conflict, exposed rather than papered over.** The 2026-08-03 decision
defines the Evidence column as what sizes the *risk* — "a test OR an
analysis", impact and likelihood. Proof that a *treatment* exists and works
is a different fact about a different thing, and today it has no home: it
gets smeared into `Countermeasure` prose or `Evidence`, one cell doing two
jobs — the exact defect class this item fixes, one column over. So the proof
gets its own column, `Treatment evidence`, and the old column's rename to
`Risk evidence` makes the pair self-describing.

**What the cell holds:** evidence of the treatment — a fixture file, a rule
live in a named file, a commit — as a citation the machine can resolve
(AU5's family: a repo-relative reference that resolves against the
filesystem, or a commit hash `git cat-file` confirms), or the honest
forward declaration while the evidence cannot exist yet.

**The planned form's exact grammar — one grammar, no editorial variants:**

```
planned — <what will exist> · <expected repo-relative location>
```

Machine contract: the cell is planned-form when it begins `planned —`
(em-dash and whitespace normalized as everywhere); it is well-formed when
one ` · ` separator is present and the final segment is a repo-relative
path. The location names where the evidence is expected to land — a path
that will resolve once the work is built. The machine does not check the
path exists before acceptance (it cannot: the path is a future); at
acceptance the planned marker itself refuses, so the promise is superseded
by the required resolving citation. Every placeholder rendering of this
form, in every view and refusal string, reads
`planned — <what will exist> · <expected location>`.

**The declared limit, in the producer's words:** *the machine verifies that
a citation resolves; the producer decides whether it supports the
treatment.* Resolution proves the cited file or commit **exists** — never
that a fixture passes, never that the evidence proves anything — retrieval,
not comprehension, the same declared limit as grounding-was-read. Symbol-level
phantoms (`stage_ahead`-class: a real file, a named thing inside it that
does not exist) pass — the known AU5 gap, inherited, not widened.

### Treatment assurance over time

The demand on a fatal row's evidence moves with the ladder, because the
evidence *cannot exist* before the work that produces it — requiring it
early would permanently block the item that must build it (the circular
dependency the producer refused in revision 1):

| Moment | Demand on a fatal row | What the machine distinguishes |
|---|---|---|
| viability → handoff | a countermeasure stated — permanent, or temporary with its return condition named — and `Treatment evidence` carrying at least the **planned** form: `planned — <what will exist> · <expected location>` | a *planned* treatment is legal and is never called proven — the `planned` marker is the machine-readable admission |
| loop | the work that produces the evidence happens here | the cell converts from `planned — …` to the resolving citation as the fixtures land |
| acceptance | the citation must **resolve** — `planned` no longer suffices | a *verified* treatment: the cited evidence exists on disk; the producer's key judges whether it proves |

**Per-gate legality of a fatal row's `Treatment evidence` — explicit at every
gate, so no gate's demand is inferred.** The ledger parse runs inside every
rung check (rungs accumulate their inputs), so the parse-level rules bind
wherever the ledger is read; the *verified* demand is the acceptance rung
check's addition and only its:

| Gate | `planned — <what will exist> · <expected location>` (declared) | resolving citation (**verified**) | empty |
|---|---|---|---|
| viability | legal | legal | refused |
| scope | legal | legal | refused |
| design | legal | legal | refused |
| handoff | legal | legal | refused |
| loop | legal | legal | refused |
| **acceptance** | **refused — still planned, not verified** | **required** | refused |

A **non-fatal** row's cell is optional at every gate: empty, planned, or
verified are all legal, at every rung, always.

**Binding scope — required at `fatal`, optional at `non-fatal`.** The worst
case named in the risk ledger is a fatal-severity risk advancing as treated;
that is where the demand binds, and it is the only place it can bind without
inventing proof obligations for the 52 existing countermeasure rows
mid-migration. The residual is named, not hidden: a non-fatal row's
treatment can still be hollow. Review trigger: if a non-fatal hollow
treatment is caught having mattered — a countermeasure relied on at a gate
that turned out to be text — the binding scope widens to all countermeasure
rows as its own item.

## Migration

**The boundary, the producer's ruling verbatim (scope key, 2026-09-03):**
mechanical only where today's data determines both fields without judgment;
every ambiguous value gets explicit producer review; the migration must not
infer to complete the schema. **And its design-gate sharpening (2026-09-03):
an old ledger passing without `fatal` does not prove its severity was
non-fatal** — the old cell could not represent fatal-plus-treated, so its
silence is the defect, not a classification. Treatment migrates mechanically;
Severity does not.

**Measured input (2026-09-03, re-measured at migration time): 21 records,
84 rows.**

| Stream | Mechanical | Producer review |
|---|---|---|
| Header rewrite | 21 of 21 records | — |
| Treatment | 83 rows: 78 legal old States copy verbatim · 4 empty stay empty · 1 (`gate-reachability`) from the recorded ruling: `countermeasure - permanent` | 1 row: `hooks-autoload`'s `accepted (named loss)` — illegal today, ambiguous |
| Severity | 5 rows: `gate-reachability` → `fatal` from the recorded ruling · 4 empty stay empty | **79 rows** — every legacy row whose severity was never recorded, unless its own cells state the classification in the ledger's terms (expected: few to none; any found shrink the batch) |
| Treatment evidence | column added to all 21 records, all 84 rows — empty (legal: optional) at non-fatal; `gate-reachability`'s fatal row carries the **planned** form in the exact grammar, transcribed from the recorded ruling and naming its expected location: `planned — --root fixtures in both directions, per the 2026-09-02 treatment ruling, built in gate-reachability's loop · tools/gates/kit.py` | — |

**The review worksheet.** The migration tool generates one row per
unresolved value — the 79 severities and the 1 ambiguous treatment
(`hooks-autoload`) in one worksheet: record · row index · the `Impact` and
`Risk evidence` cells quoted · the unresolved field blank — and the producer
keys answers in batches by record. The keyed worksheet is committed **with** the migration as a dated
record (`docs/plans/<date>-risk-state-split-migration-review.md`), so every
reviewed severity is permanently traceable to his key — the archaeology
rule: provenance marked forever, a reviewed value distinguishable from a
stated one.

**Atomicity.** One commit carries: the checker change (`LEDGER_COLUMNS`,
legal sets, `parse_ledger`, refusal strings) · all 21 record migrations ·
the keyed worksheet · the six fixtures · the prose surfaces
(`tools/gates/README.md` legal-values rows, `skills/interrogate/SKILL.md`
five-states and eight-column template) · release metadata. No committed tree
contains mixed schemas; fixtures 1 and 2 prove the refusal in both
directions at that same commit; CI green on the push is the live proof of
fixture 3.

**Post-migration truth, stated so the board's state is expected:**
`gate-reachability` **unblocks at the migration commit** — fatal + permanent
countermeasure + planned evidence passes the viability parse, so it proceeds
to the scope the producer has already stated, and its *acceptance* is where
the resolving evidence is demanded. `question-set-staleness` still refuses
at viability (blank cells — until qualified), today's honest state carried
forward. **Other rung positions are not claimed stable:** they cannot be
known until all 79 severity decisions are keyed — a row the review
classifies fatal could legitimately change its item's route, and the render
after the migration commit is what reports the truth.

## Fixtures — the producer's five, plus one added, all in the same commit

1. **old-only refused**: a fixture record carrying the old 8-column header —
   `parse_ledger` refuses with the migration-naming message.
2. **mixed refused**: a fixture tree with one migrated and one unmigrated
   record — the unmigrated record refuses; the derived route degrades
   loudly, it does not crash.
3. **fully migrated accepted**: a fixture tree on the new schema — rows
   parse, rung checks derive, zero ledger problems.
4. **fatal representable**: `Severity: fatal` + `Treatment: countermeasure -
   permanent` + `Treatment evidence: planned — …` — the row passes the
   viability parse; no FATAL refusal fires. The same row with a resolving
   citation passes the acceptance check.
5. **populated-but-unproven refused**: the fatal row still carrying
   `planned — …` (or a non-resolving citation) at the **acceptance** check —
   refused with the still-planned message. A treatment is not proven merely
   because its field is populated.
6. *(added by the model, not on the producer's list)* **fatal + temporary
   without a return condition refused**: `Severity: fatal` + `Treatment:
   countermeasure - temporary` + empty `Review trigger` — refused; the same
   row with the return condition named passes.

## Design decisions taken here, each needing the producer's key

1. Severity is **two values** (`fatal` / `non-fatal`), not a scale.
   *(keyed 2026-09-03)*
2. `Evidence` renames to **`Risk evidence`**; `Treatment evidence` is a new
   column; ten columns total. *(keyed 2026-09-03)*
3. **Treatment assurance is a lifecycle** (the producer's shape, revision 2):
   a fatal risk advances from viability on a *planned* treatment — permanent,
   or temporary with its return condition named — and the *acceptance* check
   demands the resolving citation. The machine distinguishes the two by form
   (`planned — …` vs a citation that resolves) and never calls planned
   proven.
4. **`fatal` + `countermeasure - temporary` passes with its return condition
   named** (`Review trigger` non-empty, machine-checked) — temporary means
   *carries a return condition*, never *invalid for fatal* (revision 1's
   blanket refusal is withdrawn).
5. The evidence check is **resolution**, with the limit in the producer's
   words: the machine verifies that a citation resolves; the producer decides
   whether it supports the treatment. *(keyed 2026-09-03, with this wording)*
6. `gate-reachability` migrates with the **planned form transcribed from the
   recorded ruling** — and therefore **unblocks at the migration commit**,
   proceeding to its stated scope, with resolution demanded at its
   acceptance.
7. The review worksheet (79 severities · 1 treatment) is a **dated committed
   record** — provenance permanent. *(keyed 2026-09-03)*

## What we ruled out

- **Deriving legacy severity from the absence of `fatal`** — refuted by the
  producer at the design-plan gate: the old cell could not say
  fatal-and-treated, so absence is the defect's silence, not a
  classification. (2026-09-03, verbatim in CONTEXT.md.)
- **A sixth legal state for "named, not yet qualified"** — ruled out
  2026-09-03: workflow incompleteness is represented by empty cells the
  viability gate refuses, never by a durable value. (Resolves the schema
  half of the 2026-08-31 `unqualified` finding.)
- **Overloading `Evidence` or `Countermeasure` with treatment proof** — one
  field doing two jobs is the defect this item exists to fix; recreating it
  inside a cell grammar would be the same defect wearing smaller clothes.
- **A severity scale** — no consumer, and it multiplies the review batch.
- **Requiring resolving `Treatment evidence` at the viability parse**
  (revision 1's shape) — refuted by the producer, 2026-09-03: it
  *"prevents an item from advancing to build the treatment that would
  produce that evidence"* — a circular dependency that would have blocked
  `gate-reachability` permanently. The demand moved to acceptance; planned
  treatment carries the pre-acceptance rungs.
- **A blanket refusal of `fatal` + `countermeasure - temporary`**
  (revision 1's verdict) — refuted the same pass: *"'temporary' means it
  carries a return condition, not that it expires before protecting this
  increment"*, and the refusal would have retroactively invalidated
  previously accepted temporary controls.
