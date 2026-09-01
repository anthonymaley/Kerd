# Requirements success measurement — the contract spec

Contract for `docs/product/requirements-success-measurement.md` (rigor: `mvp`).
Design: `docs/design/requirements-success-measurement.md` and the three views
sealed beside it — corrected, re-keyed and resealed 2026-09-01 under the
approval-fingerprint ruling (`condition-anatomy` `fp:67ff11391faf` ·
`condition-lifecycle` `fp:22651ad0d921` · `assurance-boundary`
`fp:544e73328c06`). GO record:
`docs/gates/2026-08-31-requirements-success-measurement-design.md` —
immutable, so its fingerprint table records the pre-ruling seals.

**What lands.** Four phases, in order. **Phase 1** builds the success-condition
model into the register machinery: a category disposition, the catalog's
recorded supersession executed verbatim, the condition's owned fields
(`Measure` · `Baseline` · `Target`), the versioned approval fingerprint —
`approval_fingerprint(category, fields)`, one category-aware mechanism whose
producer-gated landing preserves every existing hash byte-for-byte (ruled
2026-09-01) — the `measured-by` and `evidenced-by` roles with `verified-by`
re-sourced, the AU7/AU8 checks and their fixtures. The storage, link and
check pieces sit downstream of the four producer gates that key the
questions the design left open; the fingerprint is NOT among those
questions, and no gate re-asks it. **Phase 2** frames
the pilot work item `stage-route-consistency` through `/kerd:drive` and
declares its measurable success condition in the register BEFORE any design
artifact for it exists. **Phase 3** carries that condition through the pilot's
handoff (`CARRIED`) and loop (`TRACKED`). **Phase 4** takes the reading at the
pilot's acceptance, links the `Observed result`, and demonstrates the two
decisions ending in `PROVEN` or `NOT MET`.

**What does not land.** No `rigor-level` slice 2 — no enforceable per-level
measurement floors are built or claimed; the control at `mvp` binds by
agreement at one gate and **Drive does not structurally guarantee compliance**
(the risk ledger's sentence, carried verbatim). No edit to `skills/conductor/`
— Drive may CALL conductor, never REQUIRE it to change; the measurement lives
in the work record and the gates, read by Drive. No skill-text change at all,
so **no version bump** (`gate.py release` checks version *sync*, not a bump —
it stays clean). No reciprocal stamping build and no machine-checked
comparison **unless a producer gate keys one in**, and then only through a
composer hand-back (D1). No `tools/reqview/` change — the register HTML's
rendering of the new fields waits on that spike's own verdict. No condition on
any requirement beyond the pilot's one: the proof is end-to-end depth on one,
not coverage across the register's blocks.

**No workflow change.** `.github/workflows/gate.yml` already runs
`gate.py selftest` and `gate.py audit` on every push; the new fixtures ride
`selftest` and the new AU behavior rides `audit`. Nothing in CI changes.

**The multi-session dependency, named.** Phases 2–4 depend on a DIFFERENT work
item — `stage-route-consistency`, today an unframed TODO row — walking four
rungs of the ladder (design → handoff → loop → acceptance) under its own
gates, its own producer keys, and its own contract spec. That spans multiple
sessions. This is correct, ruled by the producer: this item's declared value
IS the end-to-end proof ("one requirement with a measurable aspect going
through the whole lifecycle, with its measurements proven"), and closing it
earlier would weaken the scope after the fact. **This item's own acceptance
stays open until the pilot completes** — mechanically, the unchecked boxes in
`## Pieces` hold the acceptance rung shut, and no step below invents a way to
close it sooner. "The pilot completes" means: its acceptance gate has
evaluated the condition and recorded one of the three outcomes. `PROVEN` and
`NOT MET` both complete the demonstration — the capability's purpose includes
saying no and being heard. `NOT ASSESSABLE` does not: it would mean the
reading was never taken, the exact `gate-visuals` exception this item exists
to prevent, and it sends the work back to Step 17.

**Commits and the ship flow.** Each landing step commits with the trailer
`Piece: requirements-success-measurement/<n>` (n = the step number). Any
commit that moves a derived rung — including the commit that lands THIS spec,
and Steps 11, 12, 14 and 18 below — changes the board: the flow is work
commit → `python3 tools/diagram/progress.py` → render commit → ONE push.
Pushing a rung-moving commit without its render refresh leaves CI red
(measured 2026-08-31, red for two hours). Gate records written in any sitting
below carry a `**Clock:** YYYY-MM-DD HH:MM TZ` line directly under the title,
from a real `date` run in the same turn — never a remembered time.

**Reading the Verify lines.** Where a Verify expects `audit: clean`, a
parenthesised findings count and `finding:` lines are acceptable — findings
never turn the audit red; a `problem:` line is the failure. Where a Verify runs from the repo, the working
directory is the repo root, derived per command as `repo_root=$(git rev-parse
--show-toplevel)` and never assumed from the current directory, the
home directory, the checkout name or a worktree's location.

**`MSC` throughout Steps 5–18 means the code keyed at Step 1.** If that key is
not `MSC`, substitute the keyed code everywhere it appears in those steps —
and Step 1's contingency (the three sealed views redraw and reseal at this
item's own gate) must already have been scheduled before Step 5 executes.

**Step headings are `### Step N — <name>`**, because the loop rung's check
(`STEP_HEADING_RE = ^### Step `) binds on `###` and requires a `**Verify:**`
line before the next `###` heading. Lines inside ``` fences are invisible to
that parse, so the block examples below neither split a step nor satisfy one.

---

## Decisions the steps depend on

### D1 — four producer gates, how a key is recorded, and the hand-back rule

The design deliberately left four things open (its own `## What this design
does not settle`, restated in the GO record). **This spec settles none of
them.** Each gets a step (Steps 1–4) whose outcome is a producer key, framed
in terms the producer can answer without reading code. All four can be keyed
in one sitting; Step 2 before Step 4 in that sitting, because the comparison's
machine option is only feasible under one of Step 2's outcomes.

One thing that WAS open is open no longer: the approval fingerprint. Its
shape was ruled on 2026-09-01 (the design's `## The approval fingerprint —
ruled 2026-09-01`, the three views corrected and resealed with it), so the
design's does-not-settle list now carries a fifth bullet — the fingerprint's
BUILD — that is settled work, not a gate: D3 transcribes the ruling and
Step 7 is its producer-gated landing. No gate below re-asks any part of it.

**How a key is recorded.** The design doc is living
(`docs/design/*.md` — undated, maintained in place); the GO record is the
immutable history of what was open at GO. So: Step 1 appends a new section
`## Rulings after the GO` at the end of
`docs/design/requirements-success-measurement.md`, and each gate adds one
line to it:

```
- **RULED YYYY-MM-DD — <topic>:** <the producer's decision, in his words>
```

The four topic strings are fixed, verbatim, so greps stay mechanical:
`the category code` · `the Observed result's home` · `reciprocal stamping` ·
`the comparison`. Each gate also appends to the matching bullet under
`## What this design does not settle` the suffix
` — settled: see the ruling of YYYY-MM-DD below.` (the section's claim stays
true — the *design* did not settle it; a later ruling did).

**The hand-back rule.** When a ruling selects an outcome this spec carries no
steps for — reciprocal stamping built now (Step 3), a machine-checked
comparison built now (Step 4), an external evidence-artifact citation grammar
(Step 2 outcome b) — the conductor returns THIS spec to the composer with the
ruling attached, and the composer revises this file (same filename: the loop
gate reads the latest `*-requirements-success-measurement-spec.md` by
filename, so a second dated spec would displace this contract and is not the
hand-back mechanism). Players never improvise unwritten schema.

### D2 — the success-condition block: grammar, obligations, the method's home

A success condition is a register block in `docs/requirements/register.md`,
category `MSC`, written against `catalog.md`'s existing block grammar — no new
grammar, three new meta fields. The pilot's condition, shape exact (values are
the producer's agreed words from Step 12):

```
## MSC — Measurable Success Condition

### MSC-001 — <short title>

**Category**: MSC
**State**: proposed
**Source**: docs/product/stage-route-consistency.md — agreed at its scope gate, <date>
**Measure**: <the unit counted>
**Baseline**: <what it reads today>
**Target**: <the value that counts as met>

<Statement — what observable result counts as success, the producer's words>

**Links**
- verified-by → TST-006 (sha256:<TST-006's approval fingerprint — legacy statement-only payload, 12 hex>)
```

and on the requirement it measures:

```
**Links**
- measured-by → MSC-001 (sha256:<MSC-001's approval fingerprint — the MSC/v1 four-field payload, 12 hex>)
```

Obligations, enforced by Step 8's checks:

- **A condition owns all four**: statement, `Measure`, `Baseline`, `Target`.
  Any of the three fields missing on an `MSC` block is a refusal — `DECLARED`
  means all four written, register state `proposed` (the sealed lifecycle).
- **The requirement block gains no field.** `Measure`, `Baseline` or `Target`
  on any non-`MSC` block is a refusal, named as exactly that. This is the
  constraint the design says is most likely to erode under later convenience;
  the check is what stops the erosion.
- **Evidence is never a field.** No `Observed`/`Result`/`Evidence` field
  exists on any block; the reading arrives only as a linked `Observed result`
  (Step 17, home per Step 2's ruling).
- **The method's home**: `TST` owns Method — *how the reading is taken* — and
  existing `TST` blocks carry that as their **statement**. No `**Method**`
  field exists and none is added: the design assigns TST the method, and the
  statement already is the producer's words for it. The pilot's method block
  is `TST-006` (the register's TST section currently ends at `TST-005`).
- **Link stamps are the target's approval fingerprint**, one category-aware
  mechanism for every role (`approval_fingerprint`, D3 — ruled 2026-09-01):
  a requirement or test target keeps the legacy statement-only payload,
  byte-for-byte the stamp written today, while an `MSC` target's stamp is
  its full four-field fingerprint, so Measure, Baseline or Target moving
  makes every source pointing at it suspect. The stamp protects one
  direction only — edit the target and every source pointing at it is
  flagged; edit the source and nothing flags (the stamp check,
  `kit.py:1444–1450`, generalized by Step 7). Reciprocal stamping is
  Step 3's question, not assumed — a richer target fingerprint does not
  make protection bidirectional.

### D3 — the approval fingerprint: one versioned mechanism, category-aware payloads (RULED 2026-09-01)

The sealed lifecycle claims `KEYED` freezes the target. On the register's
shipped recipe it would not have: `req_statement_hash` (`kit.py:1191`) hashes
the **statement only**, so a keyed condition's `Measure`, `Baseline` and
`Target` could all be edited after the producer's key with nothing diverging
— and a statement-only link stamp would let the same three drift without
ever making the source link suspect. This spec's first draft raised that as
composer judgment and proposed a condition-only recipe; **the producer ruled
differently on 2026-09-01** — the design's `## The approval fingerprint —
ruled 2026-09-01` section, with the three views corrected and resealed to
match. What follows transcribes the ruling; it is settled, and no gate
re-asks it.

**One versioned mechanism, artifact-specific canonical payloads** —
`approval_fingerprint(category, fields)`. Explicitly rejected: widening the
existing requirement hash and re-keying the register's shipped `Approved`
records, and a second, unrelated hashing implementation. The canonical
payloads — field names, order, separators, normalization, version — are
fixed in ONE place, the table below, so an alternate implementation cannot
invent a different byte stream (the rule-9 lesson:
`tools/reqview/fingerprint.py` documents two rule-9 implementations tested
against each other by nothing; this mechanism must not repeat that).

```python
# The one versioned approval-fingerprint table (ruled 2026-09-01):
# category → (version, payload field order). A category absent here uses
# the LEGACY payload — the stripped Statement alone — byte-for-byte the
# recipe every existing 'Approved' hash and link stamp was computed with.
# Field names, order, separators, normalization and version are fixed HERE
# and nowhere else, so an alternate implementation cannot invent a
# different byte stream (the rule-9 lesson: two implementations tested
# against each other by nothing).
REQ_APPROVAL_PAYLOADS = {
    "MSC": ("v1", ("Statement", "Measure", "Baseline", "Target")),
}


def approval_fingerprint(category, fields):
    """sha256:<first 12 hex> of the category's canonical payload — the
    'Approved' recipe AND the link-stamp recipe (one mechanism, both uses,
    category-aware; ruled 2026-09-01). `fields` maps field names to values
    and must carry 'Statement'; keys outside the payload are ignored —
    `Method` and observed evidence stay outside because they belong to
    separate objects. Legacy payload (no table entry): the stripped
    Statement alone. A declared payload (MSC v1): the header line
    '<category>/<version>', then one '<Name>: <stripped value>' line per
    payload field in declared order, joined with single newlines. Editing
    ANY payload field after keying diverges the fingerprint."""
    spec = REQ_APPROVAL_PAYLOADS.get(category)
    if spec is None:
        payload = fields.get("Statement", "").strip()
    else:
        version, names = spec
        payload = "\n".join(
            [f"{category}/{version}"]
            + [f"{n}: {fields.get(n, '').strip()}" for n in names]
        )
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def req_statement_hash(statement):
    """The legacy statement-only payload under its historical name — kept
    for existing callers and fixtures; byte-for-byte approval_fingerprint()
    with no declared payload."""
    return approval_fingerprint(None, {"Statement": statement})
```

- **Legacy payload — every existing category.** The stripped Statement
  alone: byte-for-byte the recipe every shipped `Approved` hash and every
  live link stamp was computed with. **No existing hash changes; no record
  is re-keyed.** `req_statement_hash` keeps its name and signature for its
  callers and delegates; the legacy bytes are defined once.
- **`MSC` v1 — a canonical payload of exactly four fields**: Statement ·
  Measure · Baseline · Target. Changing ANY of the four after keying
  invalidates `Approved` (AU7 refuses; **the state is never rewritten** — a
  red check is a question the producer answers). The keyed freeze made
  true. `Method` and observed evidence stay OUTSIDE the payload: they
  belong to separate objects — the four-object model holding.
- **Link stamps are the target's approval fingerprint under the same
  mechanism.** A stamp targeting an `MSC` is the full four-field
  fingerprint, never `req_statement_hash(Statement)` — otherwise Measure,
  Baseline and Target could change without making the source link suspect.
  A stamp targeting a requirement keeps its current statement hash, the
  requirement payload being statement-only — every live stamp keeps
  matching, byte-for-byte.
- **What this does NOT buy, stated so nobody folds it in:** protection
  stays one-directional. A richer TARGET fingerprint still only flags the
  SOURCE when the target moves; edit the source and nothing flags.
  **Reciprocal stamping remains a separate owed mechanism — Step 3's gate,
  not this ruling — and is neither built nor marked solved here.**

**The producer-gated landing.** The producer requires the generalization to
land as its own gated piece: Step 7 builds exactly the code above,
generalizes the two call sites (`register_check`'s `Approved` comparison
and the link-stamp check), and commits only on the producer's key over the
preservation evidence. The payload is documented in the catalog by Step 6,
which names the fields and the version and points at
`approval_fingerprint` for the bytes rather than restating them.

### D4 — the edges: kit.py symbols, typing rules, and the catalog transcription

**kit.py constants** (Step 8). Beside `REQ_ORIGIN_CATEGORIES` — the standing
precedent that kit names the category codes whose SEMANTICS it enforces while
the LEGAL set stays per-project in `categories.md`:

```python
REQ_CONDITION_CATEGORIES = frozenset({"MSC"})
REQ_CONDITION_FIELDS = ("Measure", "Baseline", "Target")
```

`REQ_META_FIELDS` gains the three (append, preserving existing order):
`("Category", "Tags", "State", "Source", "Approved", "Measure", "Baseline",
"Target")`. `REQ_LINK_ROLES` gains two pairs:
`"measured-by": "measures"` and `"evidenced-by": "evidences"`.

**Problem strings, verbatim** (Steps 7–8 emit these — item 3 lands with
Step 7's generalized comparison, the rest with Step 8; Step 9's fixtures
assert them; every one carries the standard `docs/requirements/register.md — <ID>: `
prefix that `register_check`'s `prob()` adds):

1. `missing required field 'Measure' (a success condition owns Statement, Measure, Baseline, Target)` — same for `'Baseline'`, `'Target'`; fires on an `MSC` block missing the field.
2. `field 'Measure' is legal only on a success-condition block — the requirement block gains no field` — same for the other two; fires on any non-`MSC` block carrying one.
3. `'Approved' diverges from the condition's four owned fields (approved sha256:X, condition now sha256:Y) — refused; the state is never rewritten` — fires on a `final` `MSC` block whose `Approved` no longer matches its `MSC/v1` approval fingerprint.
4. Edge typing, in the links list: `link role 'measured-by' must point at a success-condition block; <ID> is '<cat>'` · `link role 'measured-by' may not ride a success-condition block; its source is the requirement` · `link role 'verified-by' rides the success condition (re-sourced by requirements-success-measurement); a '<cat>' block may not carry it` · `link role 'evidenced-by' rides the success condition; a '<cat>' block may not carry it`.

The `verified-by` source rule is safe against the live register: verified
2026-09-01, `docs/requirements/register.md` carries **zero** `verified-by`,
`satisfied-by`, `measured-by` or `evidenced-by` links today — the slice-2
roles were declared and never used, which is exactly why the re-source can be
enforced without breaking anything.

**The unparented-finding exemption.** AU8's aggregated finding names every
non-origin block with no `refines` parent. A condition's parentage is the
`measures` edge, not `refines` — an `MSC` block would sit in that finding
list forever, noise that never resolves. Step 8 adds
`REQ_CONDITION_CATEGORIES` to the exclusion alongside
`REQ_ORIGIN_CATEGORIES` in the `unparented` comprehension.

**The catalog transcription** (Step 6 — `docs/requirements/catalog.md`).
Three edits, nothing else in the file touched:

**(a) The recorded supersession, executed verbatim.** The design's
`## Proposed supersession` section is the recorded wording; the original text
is preserved verbatim inside the strike; the note sits adjacent, in the same
`## Fields` spot the claim lived. The deferred paragraph currently reads:

```
**Deferred, each with a return condition** — Priority (returns when a release
object exists to consume it), Owner (returns on the first register with two
writers), Acceptance Criteria and Verification Method (the forward trace, slice
2), Project Type (returns with the project-type work), Subtype (appears exactly
once in the whole repo with no legal set — must not be built until one exists).
```

It becomes, exactly:

```
**Deferred, each with a return condition** — Priority (returns when a release
object exists to consume it), Owner (returns on the first register with two
writers), Project Type (returns with the project-type work), Subtype (appears
exactly once in the whole repo with no legal set — must not be built until one
exists).

~~Acceptance Criteria and Verification Method (the forward trace, slice 2)~~
**Superseded** by the separate MSC artifact and typed links: the success
condition owns statement, measure, baseline, and target; TST owns the
verification method; observed results are linked evidence. See
`docs/design/requirements-success-measurement.md`.
```

Every recorded word verbatim; the struck span verbatim inside the strike. If
Step 1 keyed a code other than `MSC`, do NOT silently substitute inside the
recorded wording — the recorded text itself then needs the producer's re-key:
hand back (D1). *If a checker mistakes struck text for a live claim, teach
the checker to distinguish retired text; do not rewrite history to satisfy a
raw text scan* — the producer's standing rule, attached 2026-08-31.

**(b) The `## Link roles` table.** Two new rows appended, and the
`verified-by` row rewritten with its original wording preserved inside the
annotation (a live declared role changing meaning is called out, never
changed quietly — the design's own rule):

```
| `measured-by` | `measures` | requirement → the success condition that says how we will know *(requirements-success-measurement)* |
| `verified-by` | `verifies` | success condition → the test that proves it *(re-sourced 2026-09-01: was "requirement → the test that proves it *(slice 2)*" — a live role's source moved; see `docs/design/requirements-success-measurement.md`)* |
| `evidenced-by` | `evidences` | success condition → the observed result that supplies the reading *(requirements-success-measurement; target form per the Observed-result ruling)* |
```

The `satisfied-by` row stays exactly as it is — still slice 2, untouched.

**(c) The `## Fields` table** gains three rows (after `Tags`, before
`Title`), and `## States, and what each one owes` gains one paragraph:

```
| Measure | on success-condition blocks | free text | The unit counted. Legal only on a block whose Category is the success-condition code — the requirement block gains no field. |
| Baseline | on success-condition blocks | free text | What it reads today, before the work. |
| Target | on success-condition blocks | free text | The value that counts as met. Frozen by the keyed `Approved` fingerprint — see State obligations. |
```

The states paragraph, appended at the end of that section:

```
**On a success-condition block, `final` owes an `Approved` equal to the
block's approval fingerprint** — the versioned `MSC/v1` canonical payload
over its four owned fields: statement, `Measure`, `Baseline`, `Target` — so
the keyed target cannot drift unseen (the keyed-freeze claim in
`docs/design/requirements-success-measurement.md`, ruled 2026-09-01). On
every other block `Approved` remains the statement-only legacy payload,
byte-for-byte the shipped hashes; no record was re-keyed. Link stamps ride
the same category-aware mechanism, every role: a stamp is the TARGET's
approval fingerprint — the full four-field fingerprint when the target is a
success condition, the statement hash otherwise. The canonical payloads
(field names, order, separators, normalization, version) are fixed in one
place, `approval_fingerprint` in `tools/gates/kit.py`; no other surface may
restate the byte stream.
```

### D5 — the pilot's terrain: `stage-route-consistency`

Chosen by the producer: real, narrow software work; currently unframed, so
its measurement can be declared before design; naturally measurable —
fixtures must prove that BOTH a legal-but-OVERCLAIMED and a
legal-but-UNDERCLAIMED `stage:` value are refused; small enough to traverse
the full lifecycle without becoming a second large project. Its content,
condensed from the `TODO.md` row (## Backlog, High consequence, as of
2026-09-01 — the row on disk is longer; the sitting reads the full row there,
this condensation is not a substitute):

> A product doc's `stage:` is checked for LEGALITY only, never against the
> derived route — and it has already overclaimed. `kit.py` validates the field
> against `STAGES` and stops; nothing compares it to what `gate.py route`
> derives from disk. Measured on three items: `hooks-autoload` declares
> `stage: scoped` while route says it enters at `viability` — a two-rung
> overclaim; `model-effort-advisory` declares `scoped` against a derived
> `design`; `funnel-driver` declares `designed` against a derived
> `acceptance`. Candidate countermeasure: an AU rule refusing a `stage:` that
> disagrees with the derived rung — the `check_stage_schema()`/AU10 precedent.

One correction, verified 2026-09-01: the row's named precedent spans two
files. `check_stage_schema()` is real but lives at
`tools/diagram/gen_journey.py:385`, not in `kit.py` — it refuses when
`docs/design/funnel-steps.md` and the render's stage labels disagree, the
same two-sources-joined-by-a-refusal move. AU10 is `_audit_au10`
(`kit.py:1095`), which did that move for gate-record FRONT MATTER
(route/stage legality and the stage-to-suffix contract), not for filenames
as the row says — AU3 is what pins the filename.

**Known terrain the pilot's own gates must handle — named here, decided
there:** the moment its AU rule lands, the live tree carries one overclaim
(`hooks-autoload`) and two underclaims (`model-effort-advisory`,
`funnel-driver`, unless its acceptance gate has closed by then) — the rule
would turn `gate.py audit` red on the repo's own tree. Whether the pilot
corrects those `stage:` fields (note: `TODO.md` parks *walking* those items
on the ladder — correcting an overclaimed field to match the derived rung is
un-claiming, not walking, but that case is made to the producer explicitly,
not assumed), scopes the rule, or stages the fix, is the pilot's design
decision. A risk without a countermeasure is a blocker, not a row — its
viability sitting fills the ledger accordingly.

**Draft condition content** — a DRAFT for the producer to agree, reword or
replace at Step 12; his words rule, and what he agrees is what lands in
Step 13 (nothing below is paraphrased into the register without his key):

- **Statement**: A product doc's declared `stage:` that disagrees with the
  rung `gate.py route` derives from disk is refused by the audit, in both
  directions — overclaim and underclaim — and a stage that agrees passes
  clean.
- **Measure**: count of disagreement directions the audit refuses, proven by
  fixtures — one legal-but-overclaimed `stage:`, one legal-but-underclaimed —
  with the live tree passing clean.
- **Baseline**: 0 of 2 — measured 2026-08-31: three live items disagree with
  their derived rung and `gate.py audit` reports nothing.
- **Target**: 2 of 2 — both fixture directions refused with a named problem
  naming the file, the declared stage and the derived rung; `gate.py audit`
  on the live tree clean.

---

## Pieces

- [x] 1. Producer gate — the category code and its disposition (RULED line in the design doc)
- [ ] 2. Producer gate — the Observed result's home (RULED)
- [ ] 3. Producer gate — reciprocal stamping: build or owe (RULED)
- [ ] 4. Producer gate — the comparison: who performs it, what checks it (RULED)
- [ ] 5. categories.md — the condition category's disposition row and counts
- [ ] 6. catalog.md — the recorded strike executed verbatim; edges, fields, and the fingerprint transcribed
- [ ] 7. Producer-gated — kit.py: approval_fingerprint(category, fields), every existing hash byte-for-byte
- [ ] 8. tools/gates/kit.py — condition fields, new roles, edge typing, unparented exemption
- [ ] 9. tools/gates/kit.py — fixtures T52–T59 (and T60 under the register-home ruling)
- [ ] 10. Diff review of Phase 1 against D2–D4 and the four rulings
- [ ] 11. Pilot framed through /kerd:drive — question set 6 of 6, board entry live
- [ ] 12. Pilot viable and scoped — the condition agreed at scope in the producer's words
- [ ] 13. MSC-001 declared in the register, linked, before any pilot design artifact exists
- [ ] 14. MSC-001 keyed at the pilot's design gate — final, Approved = the MSC/v1 fingerprint
- [ ] 15. CARRIED — the pilot's spec names MSC-001 on every step whose work affects it
- [ ] 16. TRACKED — the pilot's loop closed; acceptance rung PASS; live tree clean
- [ ] 17. The reading taken and the Observed result linked, per ruling 2
- [ ] 18. Two decisions at the pilot's acceptance gate; Outcome: PROVEN or NOT MET recorded
- [ ] 19. Full local suite green; render current; zero unchecked boxes

---

## Phase 1 — the model, storage, links, checks, and comparison

### Step 1 — PRODUCER GATE: the category code and its disposition

[keep]

**The decision, in the producer's terms.** The register files success
conditions under a category code. The design proposes `MSC` — Measurable
Success Condition — a new code beside the shipped twenty, *"unless the
category vocabulary review finds a better existing term."* That review has
not happened; this gate is it. What to put in front of the producer:

- The twenty codes and their decision questions
  (`docs/requirements/categories.md`, `docs/requirements/catalog.md` — the
  twenty-category table). The two nearest neighbours, and why each fails:
  **TST** answers *how will we test this* — the producer's own rejection,
  2026-08-31: overloading it buys the register's machinery at the price of a
  semantic contradiction, one name carrying two meanings. **ANA** builds the
  instrument that counts and by its own definition *"says nothing about what
  anyone must do once they read it"* — a success condition exists precisely
  to bind acceptance.
- The question to key: **does any existing code already mean "what observable
  result counts as success" — or is the code `MSC`?** And, with the code:
  what its `categories.md` disposition row says (Step 5 executes it).
- **The contingency, priced in:** the three sealed views draw `MSC-nnn` by
  name. A different code makes them factually wrong about the schema being
  built, so it obliges redrawing and resealing all three at THIS item's own
  gate (the standing rule: a drawing is redrawn at its own gate, never from
  another slug's slice) — and the recorded supersession text names "MSC", so
  it too would need the producer's re-key (D4a). Neither is fatal; both are
  real costs the key should weigh.

Record the ruling per D1: open `## Rulings after the GO` at the end of
`docs/design/requirements-success-measurement.md`, add the
`- **RULED YYYY-MM-DD — the category code:** …` line in the producer's words,
and suffix the matching does-not-settle bullet. Commit
(`Piece: requirements-success-measurement/1`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — the category code" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
```

Expected: exactly one line printed, carrying a real date and the producer's
decision, then `audit: clean` (findings acceptable).

### Step 2 — PRODUCER GATE: where the Observed result lives

[keep]

**The decision, in the producer's terms.** When the pilot's reading is taken
at its acceptance, where is it written down? It is a fourth object either way
— never a field on the condition. The two homes the design left open:

- **(a) A register category.** The reading is a block with its own ID
  (`OBS-001`-shaped), and `evidenced-by → <ID> (sha256:…)` works exactly like
  every link today — no grammar change. Costs: the reading inherits the
  register's five states, which read oddly on an observation (what is a
  `proposed` reading?); and it owes its own code, its own `categories.md`
  row, keyed here as part of this ruling.
- **(b) An external evidence artifact.** The reading lives in a file — most
  naturally the pilot's acceptance record itself — and the register stays
  clean of evidence. Cost: the link grammar
  (`- <role> → <ID> (sha256:<12 hex>)`) cannot name a file today, so the
  `evidenced-by` citation form is new grammar this spec has no steps for —
  **composer hand-back (D1) before Steps 6, 8 and 9 execute their
  `evidenced-by` half.** This gate sits before the storage work precisely because this
  ruling changes the schema materially.

Record per D1 (topic `the Observed result's home`); if (a), the ruling names
the evidence category's code and disposition wording. Commit
(`Piece: requirements-success-measurement/2`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — the Observed result's home" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
```

Expected: exactly one RULED line with the decision, then `audit: clean`.

### Step 3 — PRODUCER GATE: reciprocal stamping — build or owe

[keep]

**The decision, in the producer's terms.** A link's stamp is the TARGET's
approval fingerprint stored on the SOURCE (the stamp check,
`kit.py:1444–1450`; category-aware per D3 — all four owned fields for a
condition target, the statement alone for a requirement target): edit the
keyed condition anywhere in its four fields and the requirement measuring it
is flagged for re-look; **edit the requirement's statement and nothing flags
the condition** — which may now be measuring words that no longer exist. The
2026-09-01 fingerprint ruling did not change this: a richer TARGET
fingerprint still protects one direction only. For this design the
unprotected direction is the dangerous one, and the design records reciprocal
stamped links as **owed, not assumed**. The question to key: **does this
slice build the symmetric check, or does the debt stay recorded with a named
return condition?**

- **Build now** → real mechanism design nobody has done: where the reverse
  stamp lives, who restamps, what refuses. **Composer hand-back (D1)** — a
  player does not improvise it, and Steps 8–9 wait for the revised spec.
- **Owe it** → the pilot's proof knowingly carries the hole already drawn in
  the sealed anatomy view; the ruling names the return condition in the
  producer's words (the design doc records it; the debt is already a named
  row in `TODO.md`).

Record per D1 (topic `reciprocal stamping`). Commit
(`Piece: requirements-success-measurement/3`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — reciprocal stamping" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
```

Expected: exactly one RULED line with the decision, then `audit: clean`.

### Step 4 — PRODUCER GATE: the comparison — who performs it, and what checks it

[keep]

**The decision, in the producer's terms.** At the pilot's acceptance,
decision two compares the reading against the target frozen at `KEYED`. The
design ships that comparison **unenforced** — among the resealed boundary's
thirteen assurance questions, the one added 2026-08-31 when the two-decision
model exposed it. The question to key: **for this
slice, is the comparison performed by you at the gate and recorded in the
acceptance record — the mvp posture the sealed drawing shows — or does a
machine check land now?**

- **Producer-performed** → Step 18 executes it visibly: the record quotes the
  frozen target and the reading side by side and states the outcome; nothing
  on disk refuses a wrong verdict — that limit stays drawn, not hidden.
- **Machine-checked now** → an AU rule could compare a register-resident
  reading against the frozen target — feasible only under Step 2's ruling
  (a); it needs a comparison grammar (what makes "2 of 2" satisfy "2 of 2")
  nobody has designed. **Composer hand-back (D1).**

This is the assurance line a machine could most plausibly own once the schema
exists; deferring it is not neglect, it is the recorded `mvp` boundary — but
the choice is the producer's, not this spec's. Record per D1 (topic
`the comparison`). Commit (`Piece: requirements-success-measurement/4`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — the comparison" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
```

Expected: exactly one RULED line with the decision, then `audit: clean`.

### Step 5 — categories.md: the condition category's disposition row

[delegate, model: haiku, effort: low]

**What.** Edit `$repo_root/docs/requirements/categories.md`,
three surgical changes, nothing else:

1. Append to the disposition table (after the `POST` row):

   ```
   | MSC | Measurable Success Condition | applies | introduced by `docs/design/requirements-success-measurement.md` — the register category for measurable success conditions; code and disposition keyed at the vocabulary-review gate (RULED <date from Step 1>) |
   ```

2. The file's opening sentence `Which of the twenty categories this project
   owes requirements in.` becomes:
   `Which categories this project owes requirements in — the twenty shipped
   defaults, plus the MSC extension introduced by
   docs/design/requirements-success-measurement.md.`

3. The closing count sentence's span
   `**Eleven of the eighteen \`applies\` categories are unfilled** — \`BUS\`, \`STA\`, \`USR\`, \`INT\`, \`DATA\`, \`SEC\`, \`PRIV\`, \`SUP\`, \`REL\`, \`DOC\` and \`POST\`,`
   becomes
   `**Twelve of the nineteen \`applies\` categories are unfilled** — \`BUS\`, \`STA\`, \`USR\`, \`INT\`, \`DATA\`, \`SEC\`, \`PRIV\`, \`SUP\`, \`REL\`, \`DOC\`, \`POST\` and \`MSC\`,`
   — the rest of that sentence untouched. (Step 13 flips this back to
   `Eleven of the nineteen` when `MSC` gains its first block.)

Two overrides on the templates above. Step 1's ruling keyed what the
disposition row actually says — where the ruling's recorded wording differs
from item 1's template, the ruling's words win. And if Step 2's ruling
created an evidence category (outcome a), add its row too, with the wording
that ruling recorded, and shift item 3's counts to match (two new `applies`
rows make it `Thirteen of the twenty`): the closing sentence states the
tree's actual counts; the template assumes the MSC row alone. **Why.**
Executes Step 1's key. The
legal category set is per-project and machine-read from this file
(`parse_category_table`) — this row is what makes an `MSC` block legal to
AU7. Commit (`Piece: requirements-success-measurement/5`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "^| MSC " docs/requirements/categories.md && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py selftest
```

Expected: the `| MSC | Measurable Success Condition | applies | …` row with
its line number, `audit: clean`, `selftest: 51 cases passed` (nothing else
changed yet).

### Step 6 — catalog.md: the recorded strike, the edges, the fields, the fingerprint

[delegate, model: sonnet, effort: medium]

**What.** Edit `$repo_root/docs/requirements/catalog.md`
exactly as D4's transcription specifies — the three edits (a), (b), (c),
copied from D4 verbatim, and NOTHING else in the file:

- (a) the deferred paragraph in `## Fields` split as shown, the struck span
  preserved verbatim inside `~~…~~`, the **Superseded** note adjacent — the
  design's recorded wording, executed;
- (b) the `## Link roles` table: `measured-by` and `evidenced-by` rows
  appended, the `verified-by` row rewritten with its original wording
  preserved inside the annotation, `satisfied-by` untouched;
- (c) the three field rows added to the `## Fields` table after `Tags`, and
  the keyed-freeze paragraph appended to `## States, and what each one owes`.

Never delete superseded text; the strike preserves it. **Why.** The catalog
is the declared grammar the register is validated against; a role must be
registered before anything writes it (the StrictDoc rule the catalog itself
cites), and the supersession's execution was recorded at the design gate as
belonging to exactly this schema implementation. Commit
(`Piece: requirements-success-measurement/6`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -c "~~Acceptance Criteria and Verification Method (the forward trace, slice" docs/requirements/catalog.md && grep -n "measured-by\|evidenced-by\|re-sourced 2026-09-01" docs/requirements/catalog.md && grep -n "four owned fields" docs/requirements/catalog.md && python3 tools/gates/gate.py audit
```

Expected: `1` (the struck span exists exactly once), the two new role rows
plus the re-sourced `verified-by` row printed with line numbers, the
keyed-freeze paragraph found, then `audit: clean`.

### Step 7 — PRODUCER-GATED: the approval fingerprint — one mechanism, two payloads

[keep]

**What.** Edit `$repo_root/tools/gates/kit.py`.
Stdlib only. This is the piece the producer required when he ruled the
fingerprint (2026-09-01): generalize the register's current recipe into ONE
category-aware implementation while preserving every existing requirement
hash byte-for-byte. Three edits, exactly D3's code:

1. **`REQ_APPROVAL_PAYLOADS`** beside the other `REQ_*` constants
   (~line 110) — the payload table, D3 verbatim, comment included. This is
   the central fixing of field names, order, separators, normalization and
   version; no other surface restates the byte stream.

2. **`approval_fingerprint(category, fields)`** at the current
   `req_statement_hash` site (~line 1191), D3 verbatim — and
   `req_statement_hash` becomes D3's delegation, its name and signature
   kept for every existing caller and fixture. After this edit exactly one
   place encodes a payload: grep the diff for a second `hashlib.sha256` in
   the register section and find none.

3. **The two call sites, generalized.** In `register_check`'s `final` arm,
   the `Approved` comparison becomes one category-aware call — the legacy
   problem string byte-identical to today's, the declared-payload branch
   emitting D4's item-3 string:

   ```python
            elif b["statement"]:
                want = approval_fingerprint(
                    cat, {**b["fields"], "Statement": b["statement"]}
                )
                if approved != want:
                    if cat in REQ_APPROVAL_PAYLOADS:
                        prob(
                            f"'Approved' diverges from the condition's four owned fields "
                            f"(approved {approved}, condition now {want}) — "
                            "refused; the state is never rewritten"
                        )
                    else:
                        prob(
                            f"'Approved' diverges from the statement (approved {approved}, "
                            f"statement now {want}) — "
                            "refused; the state is never rewritten"
                        )
   ```

   And in the link-stamp check (~line 1444), `current` becomes the
   TARGET's approval fingerprint — a byte-identical value for every
   existing link, the full four-field payload for a future `MSC` target:

   ```python
            elif ids[target]["statement"]:
                tgt = ids[target]
                current = approval_fingerprint(
                    tgt["fields"].get("Category", "").strip(),
                    {**tgt["fields"], "Statement": tgt["statement"]},
                )
   ```

   (the stale-stamp finding string below it is untouched.)

**The gate.** This piece touches the recipe standing under every shipped
`Approved` hash (47 in the live register) and every live link stamp, so it
lands only under the producer's key: put the diff and the verify output
below in front of him — the untouched 51-case selftest, the audit with its
findings line unchanged (no live `Approved` diverged, no live stamp gone
stale: the byte-for-byte claim measured on the whole register, not
asserted), and the four probe lines. Commit
(`Piece: requirements-success-measurement/7`) only on his key; the
completion note records it. This gate approves the LANDING of ruled work —
it re-opens nothing: the shape is settled in the design's `## The approval
fingerprint — ruled 2026-09-01` and transcribed in D3. With the landing, the
living design's owed-labels come true and are updated in the same commit:
the does-not-settle bullet "The approval fingerprint's BUILD" gains the
suffix ` — built YYYY-MM-DD (Step 7 of the contract spec).`, and the
lifecycle table's `KEYED` row drops "owed, not present" for "built
YYYY-MM-DD". The sealed views are NOT touched — the assurance drawing
already carries both tenses (its dual-marked design-gate line), which is why
it was drawn that way.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 - <<'EOF'
import sys; sys.path.insert(0, 'tools/gates'); import kit
s = "The audit refuses a stage that disagrees with the derived route."
print('legacy-identical', kit.approval_fingerprint('FUN', {'Statement': s}) == kit.req_statement_hash(s))
f = {'Statement': 'Both disagreement directions are refused by the audit.',
     'Measure': 'fixture directions refused', 'Baseline': '0 of 2', 'Target': '2 of 2'}
a = kit.approval_fingerprint('MSC', f)
print('four-field-payload', a != kit.req_statement_hash(f['Statement']))
print('target-moves-it', a != kit.approval_fingerprint('MSC', {**f, 'Target': '1 of 2'}))
print('method-outside-it', a == kit.approval_fingerprint('MSC', {**f, 'Method': 'run the fixtures and count'}))
EOF
```

Expected: `selftest: 51 cases passed` (untouched — the fixture half of the
byte-for-byte proof), `audit: clean` with the findings line unchanged from
the run before this edit (the live half: every shipped `Approved` and every
live stamp still matches), then exactly:

```
legacy-identical True
four-field-payload True
target-moves-it True
method-outside-it True
```

### Step 8 — kit.py: the schema — fields, roles, typing

[delegate, model: sonnet, effort: high]

**What.** Edit `$repo_root/tools/gates/kit.py`.
Stdlib only. No function signature changes. Four edits:

1. **Constants** (beside `REQ_ORIGIN_CATEGORIES`, ~line 110): add
   `REQ_CONDITION_CATEGORIES` and `REQ_CONDITION_FIELDS` per D4, with a
   comment citing the origin-categories precedent (kit names the codes whose
   semantics it enforces; the legal set stays per-project in categories.md).
   Extend `REQ_META_FIELDS` by appending `"Measure", "Baseline", "Target"`.
   Extend `REQ_LINK_ROLES` with `"measured-by": "measures"` and
   `"evidenced-by": "evidences"` (`REQ_LEGAL_ROLES` derives automatically).

2. **Field ownership**, in `register_check`'s per-block loop, immediately
   after the `if not b["statement"]: prob("missing statement")` check:

   ```python
        is_cond = cat in REQ_CONDITION_CATEGORIES
        for f in REQ_CONDITION_FIELDS:
            if is_cond and not b["fields"].get(f, "").strip():
                prob(
                    f"missing required field '{f}' (a success condition owns "
                    "Statement, Measure, Baseline, Target)"
                )
            if not is_cond and f in b["fields"]:
                prob(
                    f"field '{f}' is legal only on a success-condition block "
                    "— the requirement block gains no field"
                )
   ```

   (`cat` is already computed above in the loop.)

3. **Edge typing**, in the AU8 links loop after the existing role/target
   checks, emitting into the same `lp` list with the same
   `f"{reg_rel} — {rid}: …"` prefix — the four rules and exact strings of
   D4 item 4. Guard target-category checks with `target in ids`. Under
   Step 2's ruling (a), also require `evidenced-by` targets to be blocks of
   the evidence category (a `REQ_EVIDENCE_CATEGORIES` frozenset beside the
   condition one, exempted from the unparented finding the same way); under
   ruling (b) this sub-item is superseded by the hand-back's revision of
   this spec.

4. **The unparented-finding exemption**: in the `unparented` comprehension
   near the end of `register_check`, exclude condition categories alongside
   origin categories, with the comment
   `# a condition's parentage is the measures edge, not refines`.

**Why.** With the fingerprint mechanism already landed (Step 7), this is
the rest of the machine half: D2's obligations and D4's edges, each
refusing exactly what the design says must not happen — a field creeping
onto the requirement block, a role quietly keeping its old source. **No
fixtures in this step** — the existing 51 must still pass untouched, which
proves the new rules fire only on condition-category blocks and the new
roles (none of which exist in any current fixture or in the live register).
Commit (`Piece: requirements-success-measurement/8`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 - <<'EOF'
import re, sys, os, tempfile
sys.path.insert(0, 'tools/gates'); import kit
d = tempfile.mkdtemp()
os.makedirs(os.path.join(d, 'docs', 'requirements'))
open(os.path.join(d, 'docs', 'requirements', 'categories.md'), 'w', encoding='utf-8').write(
    "| FUN | Functional | applies |  |\n"
    "| MSC | Measurable Success Condition | applies |  |\n"
    "| TST | Testing / Validation | applies |  |\n")
s_req = "The audit refuses a stage that disagrees with the derived route."
s_msc = "Both disagreement directions are refused by the audit."
s_tst = "Run the two fixtures and the live audit; count refusals."
m, bl, tg = "fixture directions refused", "0 of 2", "2 of 2"
msc_fp = kit.approval_fingerprint('MSC', {'Statement': s_msc, 'Measure': m, 'Baseline': bl, 'Target': tg})
reg = (
    "# R\n\n## FUN — Functional\n\n"
    "### FUN-001 — r\n\n**Category**: FUN\n**State**: proposed\n**Source**: x\n\n"
    + s_req + "\n\n**Links**\n- measured-by → MSC-001 (" + msc_fp + ")\n\n"
    "## MSC — Measurable Success Condition\n\n"
    "### MSC-001 — c\n\n**Category**: MSC\n**State**: final\n**Source**: x\n"
    "**Measure**: " + m + "\n**Baseline**: " + bl + "\n**Target**: " + tg + "\n"
    "**Approved**: " + msc_fp + "\n\n"
    + s_msc + "\n\n**Links**\n- verified-by → TST-001 (" + kit.approval_fingerprint('TST', {'Statement': s_tst}) + ")\n\n"
    "## TST — Testing / Validation\n\n"
    "### TST-001 — t\n\n**Category**: TST\n**State**: proposed\n**Source**: x\n\n" + s_tst + "\n")
p = os.path.join(d, 'docs', 'requirements', 'register.md')
open(p, 'w', encoding='utf-8').write(reg)
rc = kit.register_check(d)
print('clean', rc['blocks'], rc['links'])
print('unparented-exempt', not any('MSC-001' in f for f in rc['findings']))
bad = reg.replace('**Target**: 2 of 2', '**Target**: 1 of 2').replace(
    '**State**: proposed\n**Source**: x\n\n' + s_req,
    '**State**: proposed\n**Source**: x\n**Measure**: sneaky\n\n' + s_req)
open(p, 'w', encoding='utf-8').write(bad)
rc = kit.register_check(d)
for pr in rc['blocks']:
    print(re.sub(r'sha256:[0-9a-f]{12}', 'sha256:*', pr))
print('stamp-stale', any('link stamp for MSC-001 is stale' in f for f in rc['findings']))
EOF
```

Expected, exactly (after `selftest: 51 cases passed` and `audit: clean`):

```
clean [] []
unparented-exempt True
docs/requirements/register.md — FUN-001: field 'Measure' is legal only on a success-condition block — the requirement block gains no field
docs/requirements/register.md — MSC-001: 'Approved' diverges from the condition's four owned fields (approved sha256:*, condition now sha256:*) — refused; the state is never rewritten
stamp-stale True
```

Note what the probe quietly demonstrates: ONE `Target` edit diverges the
`Approved` (AU7, repo-red) AND stales the `measured-by` stamp on `FUN-001`
(the finding — the source flagged for re-look), while the statement never
moved. Under the superseded statement-only stamp that link would have
stayed matched, Measure, Baseline and Target free to drift behind it. That
is the 2026-09-01 ruling working.

### Step 9 — fixtures T52–T59 (and T60 under the register-home ruling)

[delegate, model: sonnet, effort: medium]

**What.** In `$repo_root/tools/gates/kit.py`'s
`_selftest_body`, after T51, add eight cases in the house style (each a
comment `# T<n> — <what it pins>`, a temp tree via the existing helpers or
inline writes, exact-string asserts against the D4 strings):

- **T52** — the happy path: a `proposed` condition block with all four owned
  fields, `measured-by` into it from a requirement — stamped with the
  condition's FULL fingerprint (`approval_fingerprint('MSC', …)`) — and
  `verified-by` out of it to a TST block stamped with the TST's legacy
  fingerprint → `register_check` returns empty `blocks` and `links`, no
  stale-stamp finding, and the condition block's ID appears in NO finding
  (the unparented exemption).
- **T53** — the keyed freeze: the same condition at `final` with
  `Approved = approval_fingerprint('MSC', …)` → clean; then the `Target`
  edited → exactly the D4 item-3 divergence string (assert with the hashes
  normalized, e.g. `re.sub(r'sha256:[0-9a-f]{12}', 'sha256:*', p)`).
- **T54** — `**Measure**` on a `FUN` block → exactly the D4 item-2 string.
- **T55** — a condition block missing `Baseline` → exactly the D4 item-1
  string for `'Baseline'`.
- **T56** — `measured-by` pointing at a non-condition block, and a second
  `measured-by` riding a condition block → both D4 item-4 strings.
- **T57** — `verified-by` riding a requirement (`FUN`) block → the
  re-source string.
- **T58** — an MSC-targeting stamp uses the four-field fingerprint, proven
  both ways. (i) A correct full-fingerprint `measured-by` stamp, then the
  condition's `Target` alone edited (statement untouched) → the stale-stamp
  FINDING appears in `findings`, `blocks` and `links` stay empty — a
  finding, never a problem, and exactly the drift a statement-only stamp
  could not see. (ii) The same link stamped
  `req_statement_hash(<the condition's statement>)` — the superseded recipe
  — is stale from birth: the finding fires with no edit at all. Assert
  against the string the code actually emits — `link stamp for <ID> is
  stale (stamped sha256:…, target now sha256:…) — re-look, then restamp`
  (the stamp check, Step 7 edit 3) — NOT the catalog's paraphrase "flagged
  for re-look", which appears in no emitted string.
- **T59** — byte-for-byte preservation, pinned from outside the mechanism:
  `approval_fingerprint('FUN', {'Statement': s}) == req_statement_hash(s)`
  as equal strings; a `final` legacy-category block whose `Approved` is the
  statement hash passes the generalized comparison clean; a link targeting
  a legacy block, stamped with the statement hash, raises no finding.
  (T1–T51 passing untouched is the broader half of the same proof.)
- **T60** — only under Step 2's ruling (a): a legal `evidenced-by` from the
  condition to an evidence-category block passes — stamped with the
  evidence block's own approval fingerprint (legacy statement-only unless
  that ruling declared a payload); the same role riding a `FUN` block, and
  targeting a non-evidence block, both refuse with the D4 strings. Under
  ruling (b) this case belongs to the hand-back's revision.

Update the count literal in ALL THREE places it lives — the `selftest`
docstring's two mentions ("Run the 51 fixture-built cases" and
"'selftest: 51 cases passed'") and the printed line (`kit.py:2851`,
`kit.py:2852` and `kit.py:2859` as of this spec's writing; Steps 7–8 shift
them — grep for the literal) — to `59` (or `60` with T60). **Why.** The
fixtures are what make the schema refuse from outside the model, in CI, on
every push — the same rung the rest of the gate machinery stands on. Commit
(`Piece: requirements-success-measurement/9`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit
```

Expected: `root resolution: 7 cases passed` then `selftest: 59 cases passed`
(`60` if T60 landed), then `audit: clean`.

### Step 10 — diff review of Phase 1 against D2–D4 and the four rulings

[keep]

**What.** Read the full diff of Steps 5–9 (from the commit before Step 5 to
HEAD — find the base with `git log --oneline`, the commit preceding the
`Piece: requirements-success-measurement/5` trailer) with D2–D4 and the four
RULED lines open beside it. Hunt drift outside the named symbols:

- every existing hash byte-identical: `req_statement_hash(s)` returns the
  same string it did before Phase 1 for every input (delegation into
  `approval_fingerprint`, never a second byte-stream definition — grep the
  diff for a second `hashlib.sha256` in the register section and find
  none); `docs/requirements/register.md` ABSENT from the diff — no live
  `Approved` value or stamp moved; `tools/reqview/` untouched;
  `REQ_LINK_RE` untouched (unless Step 2's ruling (b) revised this spec —
  then per the revision);
- the catalog strike preserves every original word; nothing else in
  `catalog.md` reworded; `satisfied-by` untouched;
- no file under `skills/` touched — `git diff <base>..HEAD --stat` lists
  ONLY: `docs/requirements/categories.md`, `docs/requirements/catalog.md`,
  `tools/gates/kit.py`, `docs/design/requirements-success-measurement.md`
  (the rulings), this spec (ticked boxes), and progress-render outputs —
  plus, only if a session boundary fell inside Phase 1, the switch-owned
  state files (`CONTEXT.md`, `TODO.md`, `kivna/sessions/*`), which belong
  to `/kerd:switch` per `docs/state-contract.md`, not to any step here,
  and carry no schema;
- every problem string in the code matches D4 character-for-character (the
  fixtures assert most of this; the eye catches a string the fixtures and
  the code agree on that the SPEC does not);
- the sealed views' fingerprints unchanged: no `.html` under
  `docs/design/requirements-success-measurement/` in the diff.

A finding here is fixed by the step that owns the file, then this review
reruns.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release
```

Expected: the selftest count from Step 9, `audit: clean`, `release: clean` —
and the diff-stat inspection above recorded in the step's completion note
with any drift named.

---

## Phase 2 — the pilot framed, its condition declared before its design gate

### Step 11 — frame `stage-route-consistency` through /kerd:drive

[keep]

**What.** A producer sitting. Run `/kerd:drive stage-route-consistency` —
and Drive states the subject in plain language when it opens the frame gate,
never the slug alone (the 2026-08-28 hand-back: the producer could not tell
whether the questions were about the skill or the item). Work type
`software-change`, **declared by the producer, never inferred** — Drive
copies `docs/work/question-sets/software-change.md`'s six entries into the
work record's `## Question set`, and the producer answers them in his own
words. Source material for the conversation: the full `TODO.md` row that D5
condenses (read from `TODO.md` itself, not from D5's excerpt) and D5's
correction. The sitting produces `docs/product/stage-route-consistency.md` —
front matter `route: new`, `stage: framed` (written at the completed rung
only: this pilot exists because stage fields overclaim; it does not get to
overclaim its own), `work-type: software-change` above any concerns block,
`## Question set` answered 6 of 6, `## Value` in units. The measurable
framing should already be audible in the A3 answer — that is what Step 12
agrees into a condition. Commit (`Piece: requirements-success-measurement/11`),
then `python3 tools/diagram/progress.py`, render commit, ONE push — this
step puts a new item on the board.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py route stage-route-consistency && python3 tools/gates/gate.py audit
```

Expected: the route render's first rung line is `frame  pass`, the verdict
line is `enters at: viability` (or deeper if the sitting continued), no
`need:` line names the Question set, and `audit: clean`.

### Step 12 — pilot viability and scope: the condition agreed at scope

[keep]

**What.** The pilot's viability and scope sittings under Drive, producer in
the loop. Viability: `## Risk ledger` naming at least one killer risk — D5's
known terrain (the AU rule turns the live audit red on three items the
moment it lands) belongs in this conversation; a risk without a
countermeasure is a blocker, not a row. Scope: the qualified ledger, a
`## Scope` section, exactly one legal `Rigor level:` line inside it (the
level is the producer's declaration), and — **this item's countermeasure,
executed:** the producer agrees the smallest measurable success condition
proportionate to that rigor level, at scope, in his own words. Put D5's
draft condition in front of him as a draft; what he agrees is what Step 13
transcribes, and his wording overrides the draft wherever they differ. Write
the agreed condition into the pilot's `## Scope` so the agreement has a home
on disk before the register block exists. The same sitting also files the
requirement's register category — Step 13 item 1's two live candidates
(`TST` vs `DATA`) are argued to the producer here, and his filing is written
into `## Scope` beside the condition, so Step 13's transcriber inherits a
decision, not a question. Stage advances only as rungs
complete (`viable`, then `scoped`). Commit
(`Piece: requirements-success-measurement/12`), progress render, ONE push.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py route stage-route-consistency && python3 tools/gates/gate.py audit
```

Expected: `enters at: design`, and `audit: clean`.

### Step 13 — declare the condition in the register — before any design artifact exists

[delegate, model: sonnet, effort: medium]

**What.** Transcribe the Step 12 agreement into
`$repo_root/docs/requirements/register.md`
— three blocks and two links, D2's shapes exactly:

1. **The requirement** the condition measures — a new block carrying the
   producer's agreed statement of the rule itself. File it under the
   category the producer filed at Step 12's sitting, recorded in the
   pilot's `## Scope` (the two live candidates, argued either way in this
   repo's own terms: **TST** — the sentence rules on a check that produces
   a stopping verdict; **DATA** — it binds how faithfully a written record
   mirrors what it stands for. The producer's filing at Step 12 decides;
   this spec deliberately does not). State `proposed`, `Source` naming
   `docs/product/stage-route-consistency.md` and the date.
2. **`MSC-001`** — the condition block, D2's grammar, the four owned fields
   carrying the producer's agreed words, `State: proposed` (`DECLARED` —
   keying is Step 14's gate, not this step). Under a new
   `## MSC — Measurable Success Condition` section placed before
   `## Archive`.
3. **`TST-006`** — the method block: its statement is HOW the reading is
   taken (the commands run, what is counted), the producer's agreed method
   wording.
4. **Links**: on the requirement, `- measured-by → MSC-001 (sha256:…)`; on
   `MSC-001`, `- verified-by → TST-006 (sha256:…)`. Stamps are the targets'
   **approval fingerprints** (ruled 2026-09-01): the `MSC` target's is its
   full four-field fingerprint, never its statement hash — a statement-only
   stamp would let Measure, Baseline and Target drift behind the link; the
   `TST` target's is its legacy statement-only fingerprint. One mechanism
   decides both — compute them, never guess:

   ```
   python3 - <<'EOF'
   import sys; sys.path.insert(0, 'tools/gates'); import kit
   blocks, _ = kit.parse_register(open('docs/requirements/register.md', encoding='utf-8').read())
   for i in ('MSC-001', 'TST-006'):
       b = next(x for x in blocks if x['id'] == i)
       print(i, kit.approval_fingerprint(b['fields']['Category'],
                                         dict(b['fields'], Statement=b['statement'])))
   EOF
   ```

5. In `docs/requirements/categories.md`, the closing count sentence drops
   every category this step fills, so its numbers state the tree's actual
   counts. `MSC` always comes off the list (the tail returns to
   `\`DOC\` and \`POST\`,` and the count to
   `**Eleven of the nineteen \`applies\` categories are unfilled**` —
   nineteen becomes twenty if Step 5 added an evidence row); and if the
   requirement itself was filed under a previously unfilled category
   (`DATA` is the live candidate), drop that code and decrement once more
   (`Ten of the nineteen`). The numbers named here assume the MSC-only,
   TST-filed case; the rest of the sentence untouched.

**The ordering constraint is the step's whole point**: this lands while NO
design artifact for the pilot exists — no `docs/design/stage-route-consistency*`,
no `concerns:` block in its product doc. Declared BEFORE design, on disk,
provably. **Why.** This is the capability's first real use: the register
carries a success condition for a live work item ahead of its design, 0 → 1.
Commit (`Piece: requirements-success-measurement/13`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && (ls docs/design | grep stage-route-consistency || echo none) && (grep -n "^concerns:" docs/product/stage-route-consistency.md || echo no-concerns) && python3 - <<'EOF'
import sys; sys.path.insert(0, 'tools/gates'); import kit
blocks, _ = kit.parse_register(open('docs/requirements/register.md', encoding='utf-8').read())
msc = next(b for b in blocks if b['id'] == 'MSC-001')
print('MSC-001', msc['fields']['State'],
      all(msc['fields'].get(f, '').strip() for f in ('Measure', 'Baseline', 'Target')))
print('verified-by', [(r, t) for r, t, _ in msc['links']])
src = next(b for b in blocks if any(r == 'measured-by' for r, _, _ in b['links']))
print('measured-by from', src['id'])
fp = kit.approval_fingerprint(msc['fields']['Category'],
                              dict(msc['fields'], Statement=msc['statement']))
print('stamp is the four-field fingerprint',
      any(r == 'measured-by' and t == 'MSC-001' and f'sha256:{s}' == fp
          for r, t, s in src['links']))
EOF
python3 tools/gates/gate.py audit
```

Expected: `none` then `no-concerns` (no design artifact and no `concerns:`
block — both halves of the before-design claim, mechanical), then exactly
`MSC-001 proposed True`, `verified-by [('verified-by',
'TST-006')]`, `measured-by from <the requirement's ID>` (ID as filed at the
sitting), `stamp is the four-field fingerprint True` (a statement-only stamp
on the `MSC` target prints `False` — wrong even though the audit would show
it only as a stale-stamp finding), then `audit: clean` — the findings line may grow by the new
unparented non-origin blocks; `MSC-001` must NOT be among them.

### Step 14 — the pilot's design gate keys the condition

[keep]

**What.** The pilot's design sitting under Drive — its concerns, views and
design doc are its own business, sized by its own scope — and AT its design
gate, the producer's key does two things at once: approves the pilot's
design, and keys `MSC-001`. The keying edit, in the register: `State:
proposed` → `final`, and an `Approved` line added carrying the condition's
approval fingerprint — the `MSC/v1` four-field payload — computed same-turn,
never typed from memory:

```
python3 - <<'EOF'
import sys; sys.path.insert(0, 'tools/gates'); import kit
blocks, _ = kit.parse_register(open('docs/requirements/register.md', encoding='utf-8').read())
b = next(x for x in blocks if x['id'] == 'MSC-001')
print(kit.approval_fingerprint(b['fields']['Category'],
                               dict(b['fields'], Statement=b['statement'])))
EOF
```

`KEYED`: the target is frozen — from here it cannot move to meet the reading
without AU7 turning the tree red AND every `measured-by` stamp pointing at it
going stale. Keying edits `State` and `Approved` only; neither is in the
payload, so the stamps written at Step 13 stay matched. The pilot's design GO record
(`docs/gates/<date>-stage-route-consistency-design.md`, front matter, Clock
line from a real `date` run) is written by that sitting as its own gate
artifact. Commit (`Piece: requirements-success-measurement/14`), progress
render, ONE push — the pilot's rung moves.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 - <<'EOF'
import sys; sys.path.insert(0, 'tools/gates'); import kit
blocks, _ = kit.parse_register(open('docs/requirements/register.md', encoding='utf-8').read())
b = next(x for x in blocks if x['id'] == 'MSC-001')
f = b['fields']
print(f['State'], f['Approved'] == kit.approval_fingerprint(
    f['Category'], dict(f, Statement=b['statement'])))
EOF
python3 tools/gates/gate.py audit && python3 tools/gates/gate.py route stage-route-consistency
```

Expected: `final True`, `audit: clean`, and the route verdict
`enters at: handoff`.

---

## Phase 3 — carried through handoff and loop

### Step 15 — CARRIED: the pilot's spec names the condition

[keep]

**What.** The pilot's handoff runs its own composer, who writes
`docs/plans/<date>-stage-route-consistency-spec.md` under its own gates.
**The brief handed to that composer carries one requirement from this item:**
the spec must name `MSC-001` on every step whose work affects the condition,
and its fixture steps' expected outputs must be consistent with the frozen
Target's words (both directions refused; live tree clean — or whatever the
producer's agreed Target says). Then the CARRIED check, this step's own
work: read the pilot's spec cold and confirm the naming holds — every step
that builds or tests the refusal names the condition; a step that omits it
goes BACK to the pilot's composer for revision, never patched by hand here.
Record the reading's verdict in this step's completion note.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -l "MSC-001" docs/plans/*-stage-route-consistency-spec.md && python3 tools/gates/gate.py check stage-route-consistency loop
```

Expected: the pilot spec's path printed (it names the condition at least
once — the grep is the floor; the cold reading above is the actual check),
then `PASS loop — stage-route-consistency: <n> inputs on disk`.

### Step 16 — TRACKED: the pilot's loop lands aimed at the condition

[keep]

**What.** The pilot's loop executes ITS spec in its own sessions, with its
own `Piece: stage-route-consistency/<n>` trailers and its own render
refreshes — nothing here duplicates that. This step fires when the pilot's
boxes are all checked, and does the one thing the assurance boundary says
nothing enforces: confirms the work was actually aimed at the condition.
Run the tracked evidence end to end — the pilot's fixtures (both
directions) ride `selftest`; the live tree carries no stage/route
disagreement the audit tolerates (however its design resolved D5's three
live items — verify the resolution landed, not just that the rule exists).
If the evidence shows the build drifted from the condition, the finding goes
to the pilot's loop, not into a quiet pass here.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py check stage-route-consistency acceptance && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit
```

Expected: `PASS acceptance — stage-route-consistency: <n> inputs on disk`
(zero unchecked boxes in the pilot's spec — the loop's exit), the selftest
count including the pilot's fixtures, and `audit: clean` on the live tree.

---

## Phase 4 — the observed result and the demonstrated outcome

### Step 17 — take the reading; link the Observed result

[delegate, model: sonnet, effort: medium]

**What.** At the pilot's acceptance sitting, BEFORE the gate's decisions:
execute `TST-006`'s method exactly as its statement says — run the named
commands, at the current HEAD, and record what they actually print. The
reading is the verbatim result in the Measure's units (e.g. "2 of 2
directions refused; overclaim fixture problem: `<the exact line>`;
underclaim fixture problem: `<the exact line>`; live audit clean at
`<commit>`") — **taken, never asserted**; if a command fails, the reading
records the failure, and that too is a reading. Then write it into the home
Step 2 ruled and link it:

- **Ruling (a) — register category:** a new block in the evidence category
  (`<EVCODE>-001`), its statement carrying the reading verbatim with date
  and commit, `State: proposed`, `Source` naming the sitting; on `MSC-001`,
  `- evidenced-by → <EVCODE>-001 (sha256:…)` with the target's approval
  fingerprint (Step 13's stamp helper, adjusted to the ID — the evidence
  block's own category rules its payload: legacy statement-only unless
  Step 2's ruling declared one). The evidence category
  now holds its first block, so `categories.md`'s closing count drops
  `<EVCODE>` from the unfilled list and decrements — the same move as
  Step 13 item 5.
- **Ruling (b) — external artifact:** the reading lands in the artifact the
  ruling named (most naturally the pilot's acceptance record's evaluation
  section, written at Step 18), cited in the form the hand-back's revision
  of this spec defined — execute that revision, not this paragraph.

Evidence is a linked object, never a field: nothing on `MSC-001` mutates
except its `**Links**` list (ruling a). The frozen `Approved` must still
match after this edit — links are outside the four-field payload, so neither
the condition's fingerprint nor the `measured-by` stamp targeting it moves.
Commit (`Piece: requirements-success-measurement/17`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "evidenced-by" docs/requirements/register.md ; python3 tools/gates/gate.py audit
```

Expected under ruling (a): the `- evidenced-by → <EVCODE>-001 (sha256:…)`
line on `MSC-001` printed with its line number, then `audit: clean`. Under
ruling (b): the revised spec's verify replaces this one; the grep prints
nothing and the citation named by the revision exists.

### Step 18 — the two decisions at the pilot's acceptance gate

[keep]

**What.** The producer, at the pilot's acceptance gate. Two decisions, in
order, never collapsed into one:

1. **Is an Observed result linked?** Step 17 made yes true; confirm against
   disk, not memory. If the sitting finds no linked reading, the outcome is
   `NOT ASSESSABLE` — never a passed row, never grounds for authoring a
   target after the build — and this item's proof has failed its purpose:
   stop, return to Step 17. Do not close the pilot on a producer exception;
   preventing that exception is what this item is for.
2. **Does the reading satisfy the target frozen at `KEYED`?** First prove
   the freeze held — rerun Step 14's verify one-liner: `final True` means
   the target the reading is compared against is the target that was keyed.
   Then the comparison, per Step 4's ruling (producer-performed at `mvp`
   unless that gate keyed a machine check): target and reading side by
   side, in their own words. Satisfied → `PROVEN`. Missed → `NOT MET` — a
   real, reportable outcome, and the target does not move to meet the
   reading.

The pilot's acceptance record
(`docs/gates/<date>-stage-route-consistency-acceptance.md` — front matter
`route: new` / `stage: ready-to-release`, `**Clock:**` from a real `date`
run, non-empty `## Release condition`, prose saying "accepted as ready for
release", never "done") carries a section `## The success condition,
evaluated`: the condition ID, the frozen Target quoted, the reading quoted
with its date and commit, the two decisions in order, and one line
`**Outcome: PROVEN**` or `**Outcome: NOT MET**`. On decision 1's failure
path, write NO acceptance record at all: an acceptance-named gate record
with a non-empty `## Release condition` is exactly what derives the pilot's
`ready-to-release` terminal (`acceptance_record`, `kit.py:892`), so a record
carrying `NOT ASSESSABLE` would close the pilot mechanically while the
demonstration has failed — the `NOT ASSESSABLE` verdict goes in the
sitting's notes and the work returns to Step 17, per the preamble. On
`NOT MET`, whether the pilot
itself re-loops or is accepted with the miss recorded is the producer's key
on the PILOT — this item's demonstration is complete either way: the
capability measured, compared, and said what it found. Commit
(`Piece: requirements-success-measurement/18`), progress render, ONE push —
the pilot reaches the terminal.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -h "\*\*Outcome: " docs/gates/*-stage-route-consistency-acceptance.md && python3 tools/gates/gate.py route stage-route-consistency && python3 tools/gates/gate.py audit
```

Expected: exactly one `**Outcome: …**` line, reading `PROVEN` or `NOT MET`;
the route verdict `enters at: ready-to-release`; `audit: clean`.

### Step 19 — full suite, render, and the boxes

[delegate, model: sonnet, effort: low]

**What.** Close the contract: confirm every step's box in `## Pieces` above
is checked (each was ticked as its step verified — tick any verified
straggler, never an unverified one), run the full local CI surface, refresh
the render if stale, commit (`Piece: requirements-success-measurement/19`)
and push. This item's own acceptance GATE — the producer's key, its dated
acceptance record with `## Release condition` and Clock line, the value
restated in units (requirements carrying a measurable success condition:
0 of 52 measured 2026-08-23 → the first one, end to end, with the outcome
decided and recorded) — happens AFTER this spec, in a Drive sitting, on the
evidence this contract leaves on disk. This step only makes that evidence
complete and green.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest && python3 tools/diagram/progress.py stale && python3 tools/design/matrix.py selftest && python3 tools/design/matrix.py audit && python3 tools/diagram/gen_journey.py check && python3 tools/gates/fidelity.py && spec="$repo_root/docs/plans/2026-09-01-requirements-success-measurement-spec.md" && unchecked=$(awk '/^- \[ \]/{n++} END{print n+0}' "$spec") && echo "unchecked: $unchecked" && test "$unchecked" -eq 0
```

Expected: every suite line clean (`selftest` at the Step 9 count plus the
pilot's cases, `audit: clean`, `release: clean`, progress selftest pass,
`render current`, matrix selftest and audit clean, `stage schema: clean
(…)`, `fidelity: clean` — the full CI surface of
`.github/workflows/gate.yml`), and the final grep
prints `0` — zero unchecked boxes (grep exits 1 at zero matches; that exit
code is the pass here, so run it last or with `|| true`).
