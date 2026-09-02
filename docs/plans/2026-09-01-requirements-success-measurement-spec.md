# Requirements success measurement — the contract spec

Contract for `docs/product/requirements-success-measurement.md` (rigor: `mvp`).
Design: `docs/design/requirements-success-measurement.md` and the three views
sealed beside it — corrected, re-keyed and resealed on 2026-09-01, three times:
under the approval-fingerprint ruling, under the binding-direction amendment,
and under the taxonomy and `Taken` corrections at the combined eye. Current
seals, from the work record's concerns block (the authority — verify with
`gate.py check requirements-success-measurement design`, never from memory):
`condition-anatomy` `fp:a75179033850` · `condition-lifecycle` `fp:da2a068e7a94`
· `assurance-boundary` `fp:73ba8986c228`. GO record:
`docs/gates/2026-08-31-requirements-success-measurement-design.md` —
immutable, so its fingerprint table records the pre-ruling seals.

**This file was revised in place on 2026-09-01** — the composer hand-back the
Step 2 and Step 3 rulings obliged (D1). The first score carried an
`evidenced-by` link role and steps built around it; the binding-direction
ruling removed that role before it ever landed, and this revision removes it
from the score: the binding runs FROM the immutable observed-result entry TO
the `MSC`, never the reverse, and discovery is DERIVED by scanning acceptance
records, not by traversing an edge.

**What lands.** Four phases, in order. **Phase 1** builds the
success-condition model into the register and gate machinery, transcribing the
eight producer rulings of 2026-09-01: the `MSC` disposition under
`categories.md`'s split framing (twenty requirement categories · register
artifact extensions), the catalog's recorded supersession executed in its
CORRECTED wording, the condition's owned fields (`Measure` · `Baseline` ·
`Target`), the versioned approval fingerprint —
`approval_fingerprint(category, fields)`, one category-aware canonical payload
with two renderings (12-hex register stamps, 64-hex record entries), whose
producer-gated landing preserves every existing hash byte-for-byte — the
`measured-by` / `measures` pair stored as TWO reciprocal stamped edges with
`verified-by` re-sourced, the AU7/AU8 extensions, the observed-result entry
parser (AU11: the eight qualification checks, `Evidence-SHA256` recomputed
over raw bytes), and their fixtures. **Phase 2** frames the pilot work item
`stage-route-consistency` through `/kerd:drive` and declares its measurable
success condition in the register BEFORE any design artifact for it exists.
**Phase 3** carries that condition through the pilot's handoff (`CARRIED`) and
loop (`TRACKED`). **Phase 4** takes the reading at the pilot's acceptance,
snapshots and digests its evidence, records the observed-result entry in the
pilot's immutable acceptance record — bound inbound to the `MSC` by its exact
frozen fingerprint — and demonstrates the two decisions ending in `PROVEN` or
`NOT MET`.

**What does not land.** No `rigor-level` slice 2 — no enforceable per-level
measurement floors are built or claimed; the control at `mvp` binds by
agreement at one gate and **Drive does not structurally guarantee compliance**
(the risk ledger's sentence, carried verbatim). No edit to `skills/conductor/`
— Drive may CALL conductor, never REQUIRE it to change; the measurement lives
in the work record and the gates, read by Drive. No skill-text change at all,
so **no version bump** (`gate.py release` checks version *sync*, not a bump —
it stays clean). **No `evidenced-by` / `evidences` link role, anywhere** —
removed as a stored register link role by the binding-direction ruling
(2026-09-01) before it ever landed: the `Observed result` is not a register
block, so there is nothing for an ID-only role to point at, and the producer
refused both cheap paths — forcing the role through today's grammar, and
pretending the suspect-link stamp supports a file reference. The phrase "the
`MSC` is evidenced by the result" survives only as prose for a **derived**
relationship. **No `OBS` register category** — observed results do not live in
the register. **No machine-checked comparison** — ruled producer-performed in
this slice: the parser enforces structure, never semantics, and machine
comparison returns only *"when the `MSC` target grammar is explicitly typed
and at least one real condition requires a repeatable comparison that the
acceptance producer should not perform by judgment alone."* **No remote or
provider-native evidence** — a bare URL or a mutable CI-run location is
insufficient in this slice; evidence is captured as a stable local snapshot
with a recomputable digest, and the remote question stays with the existing
out-of-repo-artifacts problem. No retrofit of reciprocity onto existing
role pairs — the reciprocal build (which DOES land, Steps 8 and 10) is scoped
to the new Requirement ↔ `MSC` pair only; broader reciprocal enforcement
stays separate work. No `tools/reqview/` change — the register HTML's
rendering of the new fields waits on that spike's own verdict. No condition on
any requirement beyond the pilot's one: the proof is end-to-end depth on one,
not coverage across the register's blocks.

**No workflow change.** `.github/workflows/gate.yml` already runs
`gate.py selftest` and `gate.py audit` on every push; the new fixtures ride
`selftest` and the new AU behavior — the AU7/AU8 extensions and the new
AU11 — rides `audit`. Nothing in CI changes.

**The multi-session dependency, named.** Phases 2–4 depend on a DIFFERENT work
item — `stage-route-consistency`, today an unframed TODO row (re-verified
2026-09-01: the row stands in `TODO.md`'s High-consequence backlog, marked as
this item's pilot; no product doc, no design artifact, and `gate.py route`
still reports it entering at `frame` — invisible to every machine surface
until Step 12 frames it) — walking four rungs of the ladder (design → handoff
→ loop → acceptance) under its own gates, its own producer keys, and its own
contract spec. That spans multiple sessions. This is correct, ruled by the
producer: this item's declared value IS the end-to-end proof ("one requirement
with a measurable aspect going through the whole lifecycle, with its
measurements proven"), and closing it earlier would weaken the scope after the
fact. **This item's own acceptance stays open until the pilot completes** —
mechanically, the unchecked boxes in `## Pieces` hold the acceptance rung
shut, and no step below invents a way to close it sooner. "The pilot
completes" means: its acceptance gate has evaluated the condition and recorded
one of the three outcomes. `PROVEN` and `NOT MET` both complete the
demonstration — the capability's purpose includes saying no and being heard.
`NOT ASSESSABLE` does not: it would mean the reading was never taken or never
qualified, the exact `gate-visuals` exception this item exists to prevent, and
it sends the work back to Step 18.

**Commits and the ship flow.** Each landing step commits with the trailer
`Piece: requirements-success-measurement/<n>` (n = the step number). Any
commit that moves a derived rung — including the commit that lands this
revision of the spec, and Steps 12, 13, 15 and 19 below — changes the board:
the flow is work commit → `python3 tools/diagram/progress.py` → render commit
→ ONE push. Pushing a rung-moving commit without its render refresh leaves CI
red (measured 2026-08-31, red for two hours). Gate records written in any
sitting below carry a `**Clock:** YYYY-MM-DD HH:MM TZ` line directly under the
title, from a real `date` run in the same turn — never a remembered time.

**Reading the Verify lines.** Where a Verify expects `audit: clean`, a
parenthesised findings count and `finding:` lines are acceptable — findings
never turn the audit red; a `problem:` line is the failure. Where a Verify
runs from the repo, the working directory is the repo root, derived per
command as `repo_root=$(git rev-parse --show-toplevel)` and never assumed from
the current directory, the home directory, the checkout name or a worktree's
location. Where a Verify asserts a count of ZERO, the count is taken
exit-safely — `awk` (or a `grep` inside `$( )`) feeding `test … -eq 0` —
never a bare `grep -c` in a `&&` chain, which exits 1 at zero matches and
aborts the chain exactly when the check should pass; every such command must
hold in both directions, green at zero and red at one.

**`MSC` is the keyed code.** Step 1's gate ruled it on 2026-09-01 — code
`MSC`, reader-facing name Measurable Success Condition, disposition `applies`
— so the contingency the first score priced (redrawing the sealed views under
a different code) died unexercised. `MSC` below is the code, not a
placeholder.

**Step headings are `### Step N — <name>`**, because the loop rung's check
(`STEP_HEADING_RE = ^### Step `) binds on `###` and requires a `**Verify:**`
line before the next `###` heading. Lines inside ``` fences are invisible to
that parse, so the block examples below neither split a step nor satisfy one.

---

## Decisions the steps depend on

### D1 — the four producer gates (all keyed), how a key was recorded, and the hand-back rule

The design deliberately left four things open at the GO (its own `## What this
design does not settle` as it then stood, restated in the GO record). **All
four are now keyed.** Steps 1–4 below are landed, and the design's
`## Rulings after the GO` carries the four RULED lines plus four more rulings
taken while the keys were being converted into schema — the binding direction,
the evidence digest, the comparison's assurance tense, and the taxonomy split.
This spec settles none of them; it transcribes all eight. The four gate
topics are fixed, verbatim, so greps stay mechanical: `the category code` ·
`the Observed result's home` · `reciprocal stamping` · `the comparison` —
grep each WITH its trailing colon, because a later ruling's topic (`the
comparison is producer-agreed, not unenforced`) begins with the same words.

One thing that WAS open never became a gate: the approval fingerprint. Its
shape was ruled on 2026-09-01 (the design's `## The approval fingerprint —
ruled 2026-09-01`), D3 transcribes it, and Step 7 is its producer-gated
landing. No step below re-asks any part of any ruling.

**How a key is recorded** — the mechanism, kept live for future gates. The
design doc is living (`docs/design/*.md` — undated, maintained in place); the
GO record is the immutable history of what was open at GO. Each gate appends
one line to `## Rulings after the GO` at the end of
`docs/design/requirements-success-measurement.md`:

```
- **RULED YYYY-MM-DD — <topic>:** <the producer's decision, in his words>
```

**The hand-back rule — and it has already fired once.** When a ruling selects
an outcome the current score carries no steps for, the conductor returns THIS
spec to the composer with the ruling attached, and the composer revises this
file — same filename: the loop gate reads the latest
`*-requirements-success-measurement-spec.md` by filename, so a second dated
spec would displace this contract and is not the hand-back mechanism. Players
never improvise unwritten schema. It fired on 2026-09-01: Step 2's key chose
a home neither drafted option described and refused both cheap link-grammar
paths, Step 3's key chose build-now, and this revision is that hand-back
executed — `evidenced-by` and every step and fixture written around it
removed, the observed-result entry contract (D6) and its parser (Step 9)
added, reciprocal stamping written into Steps 8 and 10. The rule stays live
for what remains open, each named as a dependency rather than an assumed
outcome: **Step 7's landing key** — a refusal there invalidates Steps 8–11 as
written, every one of which leans on the landed mechanism — and the pilot's
own gates, whose outcomes Steps 12–19 carry as branches, never as settled
fact.

### D2 — the success-condition block: grammar, obligations, the method's home

A success condition is a register block in `docs/requirements/register.md`,
category `MSC`, written against `catalog.md`'s existing block grammar — no new
grammar, three new meta fields. The pilot's condition, shape exact (values are
the producer's agreed words from Step 13):

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
- measures → <REQ-ID> (sha256:<the requirement's approval fingerprint — legacy statement-only payload, 12 hex>)
- verified-by → TST-006 (sha256:<TST-006's approval fingerprint — legacy statement-only payload, 12 hex>)
```

and on the requirement it measures:

```
**Links**
- measured-by → MSC-001 (sha256:<MSC-001's approval fingerprint — the MSC/v1 four-field payload, 12 hex>)
```

**Both directions are stored and both are stamped** — the reciprocal-stamping
ruling (Step 3, executed at Steps 8 and 10). That is a recorded departure from
the catalog's one-declaration convention, because the two directions carry
different stamp payloads; Step 6 transcribes the departure into the catalog
rather than letting it happen quietly.

Obligations, enforced by Steps 7–8's checks:

- **A condition owns all four**: statement, `Measure`, `Baseline`, `Target`.
  Any of the three fields missing on an `MSC` block is a refusal — `DECLARED`
  means all four written, register state `proposed` (the sealed lifecycle).
- **The requirement block gains no field.** `Measure`, `Baseline` or `Target`
  on any non-`MSC` block is a refusal, named as exactly that. This is the
  constraint the design says is most likely to erode under later convenience;
  the check is what stops the erosion.
- **Evidence is never a field, and never a link.** No
  `Observed`/`Result`/`Evidence` field exists on any block, and no evidence
  link role exists in the grammar. The reading is an ENTRY in the pilot's
  immutable acceptance record (D6, Steps 18–19), bound inbound to the
  condition by its frozen fingerprint; discovery is derived by scanning
  acceptance records, never by traversing an edge. The register never
  carries evidence, and an `MSC` gains no outbound file reference and no
  post-key mutation.
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
  makes every source pointing at it suspect. A single stamp protects one
  direction only — edit the target and every source pointing at it is
  flagged; edit the source and that stamp says nothing (the stamp check,
  `kit.py:1444–1450`, generalized by Step 7). **The second stored edge is
  what covers the dangerous direction**: with `measures` stamped on the
  condition, editing the requirement's statement stales THAT stamp — a
  finding, at the existing suspect-link severity, never a refusal in this
  slice (the Step 3 ruling, verbatim: *"Do not inflate it into a refusal in
  this slice."*).

### D3 — the approval fingerprint: one versioned mechanism, category-aware payloads (RULED 2026-09-01)

The sealed lifecycle claims `KEYED` freezes the target. On the register's
shipped recipe it would not have: `req_statement_hash` (`kit.py:1191`) hashes
the **statement only**, so a keyed condition's `Measure`, `Baseline` and
`Target` could all be edited after the producer's key with nothing diverging
— and a statement-only link stamp would let the same three drift without
ever making the source link suspect. This spec's first draft raised that as
composer judgment and proposed a condition-only recipe; **the producer ruled
differently on 2026-09-01** — the design's `## The approval fingerprint —
ruled 2026-09-01` section. What follows transcribes the ruling; it is
settled, and no step re-asks it.

**One versioned mechanism, artifact-specific canonical payloads** —
`approval_fingerprint(category, fields)`. Explicitly rejected: widening the
existing requirement hash and re-keying the register's shipped `Approved`
records, and a second, unrelated hashing implementation. The canonical
payloads — field names, order, separators, normalization, version — are
fixed in ONE place, the table below, so an alternate implementation cannot
invent a different byte stream (the rule-9 lesson:
`tools/reqview/fingerprint.py` documents two rule-9 implementations tested
against each other by nothing; this mechanism must not repeat that).

**One payload, two renderings.** The register grammar (`REQ_APPROVED_RE`,
`REQ_LINK_RE`) fixes `sha256:<12 hex>`; the immutable observed-result entry
(D6, per the design's entry shape) stores `fingerprint:<64 lowercase hex>`.
Both renderings come from the SAME canonical payload, digested in the one
function below — the 64-hex sibling was added by the 2026-09-01 revision to
serve D6, and defines no second byte stream.

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


def _approval_digest(category, fields):
    """Full 64-hex sha256 of the category's canonical payload — the ONE
    place the payload becomes bytes. Legacy payload (no table entry): the
    stripped Statement alone. A declared payload (MSC v1): the header line
    '<category>/<version>', then one '<Name>: <stripped value>' line per
    payload field in declared order, joined with single newlines. `fields`
    maps field names to values and must carry 'Statement'; keys outside
    the payload are ignored — `Method` and observed evidence stay outside
    because they belong to separate objects."""
    spec = REQ_APPROVAL_PAYLOADS.get(category)
    if spec is None:
        payload = fields.get("Statement", "").strip()
    else:
        version, names = spec
        payload = "\n".join(
            [f"{category}/{version}"]
            + [f"{n}: {fields.get(n, '').strip()}" for n in names]
        )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def approval_fingerprint(category, fields):
    """sha256:<first 12 hex> of the canonical payload — the register's
    rendering: the 'Approved' recipe AND the link-stamp recipe (one
    mechanism, both uses, category-aware; ruled 2026-09-01). Editing ANY
    payload field after keying diverges the fingerprint."""
    return "sha256:" + _approval_digest(category, fields)[:12]


def approval_fingerprint_full(category, fields):
    """The SAME canonical payload at full length — 64 lowercase hex, no
    prefix: the rendering the immutable observed-result entry stores
    ('Condition: <ID> (fingerprint:<64 hex>)', D6). One payload, two
    renderings, both from _approval_digest; no other surface may restate
    the byte stream."""
    return _approval_digest(category, fields)


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
- **What a richer TARGET fingerprint does NOT buy:** bidirectional
  protection. One stamp still only flags the SOURCE when the target moves.
  The reciprocal ruling closed that the other way — a SECOND stored edge,
  `measures`, stamped with the requirement's fingerprint (Step 8) — so the
  dangerous direction is covered by the same stamp check running over the
  back-edge, at finding severity.

**The producer-gated landing.** The producer requires the generalization to
land as its own gated piece: Step 7 builds exactly the code above,
generalizes the two call sites (`register_check`'s `Approved` comparison
and the link-stamp check), and commits only on the producer's key over the
preservation evidence. The payload is documented in the catalog by Step 6,
which names the fields and the version and points at
`approval_fingerprint` for the bytes rather than restating them.

### D4 — the edges: kit.py symbols, typing, reciprocity, and the catalog transcription

**kit.py constants** (Step 8). Beside `REQ_ORIGIN_CATEGORIES` — the standing
precedent that kit names the category codes whose SEMANTICS it enforces while
the LEGAL set stays per-project in `categories.md`:

```python
REQ_CONDITION_CATEGORIES = frozenset({"MSC"})
REQ_CONDITION_FIELDS = ("Measure", "Baseline", "Target")
```

`REQ_META_FIELDS` gains the three (append, preserving existing order):
`("Category", "Tags", "State", "Source", "Approved", "Measure", "Baseline",
"Target")`. `REQ_LINK_ROLES` gains ONE pair: `"measured-by": "measures"`
(`REQ_LEGAL_ROLES` derives automatically — and both directions were already
writable, kit's own comment at the roles table, which is what lets this pair
store both).

**Problem strings, verbatim** (Steps 7–8 emit these — item 3 lands with
Step 7's generalized comparison, the rest with Step 8; Step 10's fixtures
assert them; every one carries the standard `docs/requirements/register.md — <ID>: `
prefix that `register_check`'s `prob()` adds):

1. `missing required field 'Measure' (a success condition owns Statement, Measure, Baseline, Target)` — same for `'Baseline'`, `'Target'`; fires on an `MSC` block missing the field.
2. `field 'Measure' is legal only on a success-condition block — the requirement block gains no field` — same for the other two; fires on any non-`MSC` block carrying one.
3. `'Approved' diverges from the condition's four owned fields (approved sha256:X, condition now sha256:Y) — refused; the state is never rewritten` — fires on a `final` `MSC` block whose `Approved` no longer matches its `MSC/v1` approval fingerprint.
4. Edge typing, in the links list — five strings: `link role 'measured-by' must point at a success-condition block; <ID> is '<cat>'` · `link role 'measured-by' may not ride a success-condition block; its source is the requirement` · `link role 'measures' must ride a success-condition block; a '<cat>' block may not carry it` · `link role 'measures' may not point at a success-condition block; its target is the requirement it measures` · `link role 'verified-by' rides the success condition (re-sourced by requirements-success-measurement); a '<cat>' block may not carry it`.
5. Reciprocal presence — **FINDINGS, never problems** (into the same
   `findings` list the stale-stamp check feeds, with the standard
   `docs/requirements/register.md — <ID>: ` prefix; the named block is the
   one that OWES the missing edge):
   `reciprocal link missing — <REQ> carries measured-by → <MSC> but <MSC> carries no measures → <REQ> (the pair is stored as two edges; requirements-success-measurement)`
   · and the mirror,
   `reciprocal link missing — <MSC> carries measures → <REQ> but <REQ> carries no measured-by → <MSC> (the pair is stored as two edges; requirements-success-measurement)`.
   The ruling, verbatim: *"Do not inflate it into a refusal in this
   slice."* Staleness of either direction's stamp needs NO new code — once
   both edges are stored, Step 7's generalized stamp check covers each
   against its own target's current fingerprint.

The `verified-by` source rule is safe against the live register: verified
2026-09-01, `docs/requirements/register.md` carries **zero** `verified-by`,
`satisfied-by` or `measured-by` links today — the slice-2 roles were declared
and never used, which is exactly why the re-source can be enforced without
breaking anything.

**The unparented-finding exemption.** AU8's aggregated finding names every
non-origin block with no `refines` parent. A condition's parentage is the
`measures` edge, not `refines` — an `MSC` block would sit in that finding
list forever, noise that never resolves. Step 8 adds
`REQ_CONDITION_CATEGORIES` to the exclusion alongside
`REQ_ORIGIN_CATEGORIES` in the `unparented` comprehension.

**The catalog transcription** (Step 6 — `docs/requirements/catalog.md`).
Three edits, nothing else in the file touched:

**(a) The recorded supersession, executed in its CORRECTED wording.** The
design's `## Proposed supersession` section is the recorded wording — and it
was corrected on 2026-09-01, the binding-direction ruling having falsified
the earlier phrase "observed results are linked evidence". The corrected
recorded text is what lands; the original text is preserved verbatim inside
the strike; the note sits adjacent, in the same `## Fields` spot the claim
lived. The deferred paragraph currently reads:

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
verification method; observed results are entries in the immutable acceptance
record, bound to the condition by its frozen fingerprint. See
`docs/design/requirements-success-measurement.md`.
```

Every recorded word verbatim; the struck span verbatim inside the strike.
*If a checker mistakes struck text for a live claim, teach the checker to
distinguish retired text; do not rewrite history to satisfy a raw text scan*
— the producer's standing rule, attached 2026-08-31.

**(b) The `## Link roles` table.** One new row appended, and the
`verified-by` row rewritten with its original wording preserved inside the
annotation (a live declared role changing meaning is called out, never
changed quietly — the design's own rule):

```
| `measured-by` | `measures` | requirement → the success condition that says how we will know *(requirements-success-measurement; stored as TWO edges — see the note below this table)* |
| `verified-by` | `verifies` | success condition → the test that proves it *(re-sourced 2026-09-01: was "requirement → the test that proves it *(slice 2)*" — a live role's source moved; see `docs/design/requirements-success-measurement.md`)* |
```

The `satisfied-by` row stays exactly as it is — still slice 2, untouched.
And directly below the table, the departure note, so the two-edge storage is
declared grammar rather than a quiet exception:

```
**`measured-by` / `measures` is stored as TWO edges — a recorded departure
from the one-declaration convention above, not an application of it.** The
two directions carry different stamp payloads: `measured-by` stores the
success condition's full four-field approval fingerprint; `measures` stores
the requirement's legacy statement-only fingerprint. The audit requires both
directions for this role pair; a missing reciprocal edge or a stale stamp is
a finding at the suspect-link severity, deliberately not a refusal in this
slice. Every other role pair is unchanged — one declaration, both reading
directions. There is no evidence link role: an observed result is an entry
in the immutable acceptance record, bound to the condition by its frozen
fingerprint (see `docs/design/requirements-success-measurement.md`), not a
register link.
```

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
replace at Step 13; his words rule, and what he agrees is what lands in
Step 14 (nothing below is paraphrased into the register without his key):

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

### D6 — the observed-result entry: the record shape, the eight checks, and the parser (AU11)

The ruled home (Step 2) and the ruled direction: the `Observed result` is an
ENTRY in the immutable acceptance record, and **the binding runs from the
record entry TO the condition, never the reverse** — *"the record binds
itself to the exact predeclared condition; the condition does not reach
forward into history."* No link grammar changes; `REQ_LINK_RE` is untouched.
Discovery is derived: scan the acceptance records for entries naming the
`MSC` ID — the same files `acceptance_record` (`kit.py:892`) already globs.

**The canonical entry.** Inside an acceptance record
(`docs/gates/*-acceptance.md`, or the read-only `*-goal.md` alias — the scan
covers exactly what `acceptance_record` reads), an observed-result entry is a
run of consecutive `Name: value` lines opened by a `Condition:` line. Fenced
or bare — the parser reads RAW lines, fences included (an entry usually sits
in a fence to hold its alignment; a fence hides lines from the loop's STEP
parse, not from this scan). Shape, exact — the design's
`## The observed-result entry`:

```
Condition:       MSC-001 (fingerprint:<64 lowercase hex>)
Observed:        <value> <unit>
Method:          TST-006
Taken:           YYYY-MM-DD
Evidence:        <repo-relative path>
Evidence-SHA256: <64 lowercase hex>
Outcome:         PROVEN | NOT MET
```

**Seven fields, nine required facts, eight qualification checks** — the
`Condition` line carries two facts (the ID and the frozen fingerprint) and
`Observed` carries two (the value and its unit). The `fingerprint:` value is
the FULL 64-hex rendering of the same `MSC/v1` canonical payload the
register's 12-hex `sha256:` stamps truncate — `approval_fingerprint_full`
(D3): one payload, two renderings, one byte-stream definition. The design's
entry shape fixes 64 hex here while the register grammar fixes 12; this spec
reconciles the two lengths through the shared `_approval_digest`, and no
other surface may restate either.

**The opener, and the guard against sloppy records.**
`^Condition:\s+([A-Z]{2,4}-\d{3}) \(fingerprint:([0-9a-f]{64})\)$` opens an
entry; following lines matching `^([A-Za-z][A-Za-z0-9-]*):\s+(.*\S)\s*$`
belong to it, until the first blank or non-matching line. A line matching
`^Condition:` that fails the opener is REFUSED — a malformed entry must not
evade the parser and stand as prose claiming an outcome. (Verified
2026-09-01: zero `^Condition:` lines exist in live gate records, so the
guard refuses nothing retroactively.) Shape refusals: a missing, duplicate,
or unknown field.

**The eight checks — an entry QUALIFIES only when every one holds, and the
parser checks all of them** (*"a required fact the parser does not check is
not a requirement; it is a comment"*):

1. `Condition` names a success-condition block (`REQ_CONDITION_CATEGORIES`)
   that exists in the register.
2. Its stored fingerprint matches the condition — `approval_fingerprint_full`
   recomputed over the register block's CURRENT four fields equals the
   entry's 64 hex. AU7 separately guards that a keyed condition has not
   moved, so a match here on a green tree is a match against the target
   frozen at `KEYED` — *"the exact frozen four-field fingerprint, not
   `req_statement_hash`."*
3. `Evidence` resolves to a repo-relative regular file inside the tree — an
   absolute path or a `..` escape does not resolve.
4. `Evidence-SHA256` RECOMPUTES over that file's raw bytes — a plain sha256,
   full 64 hex. This is the second digest and the second `hashlib.sha256`
   call site, and deliberately so: *"the digest protects evidence identity;
   the stored MSC fingerprint protects target identity"* — bytes versus
   fields, two digests, two jobs, never merged.
5. `Observed` carries both a value and a unit — at least two
   whitespace-separated tokens.
6. `Method` names a `TST` that exists in the register — BOTH halves
   checked, each with its own refusal so the failure is diagnosable: the
   shape `TST-\d{3}`, AND resolution to a register block whose `Category`
   is `TST`. Symmetric with check 1, and RULED so on 2026-09-01 —
   correcting this spec's earlier shape-only reading of the design's
   asymmetric wording. The producer's words: *"'Method names a TST' means
   the referenced ID resolves to an existing TST block in the register,
   not merely that its text matches ^TST-[0-9]+$. A phantom method would
   make the observed result unverifiable and therefore NOT ASSESSABLE."*
   **The reference is NOT version-pinned** — no method fingerprint, no
   stamp on the reference, no `Method-SHA256`: the sealed design requires
   a method REFERENCE, not a frozen method version. Whether historical
   evidence must bind to the exact keyed `TST` version is a follow-up
   integrity question the producer is filing separately; it must not be
   silently added to this contract.
7. `Taken` is a real calendar date in `YYYY-MM-DD` form
   (`datetime.date.fromisoformat` — `2026-13-40` fails, not just malformed
   shapes).
8. `Outcome` is exactly `PROVEN` or `NOT MET`.

**Problem strings, verbatim** (Step 9 emits, Step 10's T62 asserts; each
prefixed `docs/gates/<file> — `):

- `malformed observed-result Condition line at line <n> — expected "Condition: <ID> (fingerprint:<64 lowercase hex>)"`
- `observed-result entry (<ID>) is missing field '<Name>'` · `observed-result entry (<ID>) duplicates field '<Name>'` · `observed-result entry (<ID>) carries unknown field '<Name>'`
- check 1: `observed-result entry names '<ID>', which is not a success-condition block in the register`
- check 2: `observed-result entry (<ID>): fingerprint does not match the condition's current four-field payload (entry <first 12 hex>…, condition now <first 12 hex>…) — the record binds to the exact frozen condition`
- check 3: `observed-result entry (<ID>): Evidence does not resolve to a file in the repo: '<path>'`
- check 4: `observed-result entry (<ID>): Evidence-SHA256 does not recompute over '<path>' (recorded <first 12 hex>…, file now <first 12 hex>…) — the artifact judged is not the artifact on disk`
- check 5: `observed-result entry (<ID>): Observed must carry a value and a unit: '<value>'`
- check 6, syntax: `observed-result entry (<ID>): Method must name a TST (TST-nnn): '<value>'`
- check 6, resolution: `observed-result entry (<ID>): Method '<value>' does not resolve to a TST block in the register`
- check 7: `observed-result entry (<ID>): Taken must be a real date in YYYY-MM-DD form: '<value>'`
- check 8: `observed-result entry (<ID>): Outcome must be exactly PROVEN or NOT MET: '<value>'`

**`NOT ASSESSABLE` — two derivation paths, both preserved, both mechanical.**
(1) No entry names the `MSC` — the ID is simply absent from the parser's
qualifying entries. (2) An entry exists but does not qualify — it is refused
into `problems` AND excluded from the qualifying entries, never silently
dropped, never `PROVEN`, never `NOT MET`. *"An unverifiable reading is not a
bad reading; it is not a reading."* The refusal (AU11, machine-refused — the
assurance boundary's designed tense for its parser and digest lines) is what
keeps a non-qualifying entry from standing on a green tree; the semantic
outcome for the condition is `NOT ASSESSABLE`, concluded by the producer at
the gate (Step 19) and NEVER written into an acceptance record — a record
naming acceptance with a non-empty `## Release condition` closes the pilot
mechanically (`acceptance_record`, `kit.py:892`), which is exactly what must
not happen when the demonstration has failed.

**The parser's symbols** (Step 9). `observed_results(root)` returns
`{"entries": {<MSC-ID>: [{"fields": {…}, "file": <basename>, "line": <n>}]},
"problems": […]}` — **qualifying entries only** under `"entries"`.
`_audit_au11(root)` returns the problems and registers in `audit()` after
`_audit_au10`. The comparison itself — does the reading satisfy the frozen
target — belongs to NO symbol here: it is the producer's, per the Step 4
ruling, and the parser *"should enforce structure, not invent semantics."*

---

## Pieces

- [x] 1. Producer gate — the category code and its disposition (RULED line in the design doc)
- [x] 2. Producer gate — the Observed result's home (RULED)
- [x] 3. Producer gate — reciprocal stamping: build or owe (RULED)
- [x] 4. Producer gate — the comparison: who performs it, what checks it (RULED)
- [ ] 5. categories.md — the split framing: twenty requirement categories, register artifact extensions, the MSC row
- [ ] 6. catalog.md — the corrected strike executed verbatim; the two-edge role pair, fields, and the fingerprint transcribed
- [ ] 7. Producer-gated — kit.py: approval_fingerprint(category, fields), one payload with two renderings, every existing hash byte-for-byte
- [ ] 8. tools/gates/kit.py — condition fields, the measured-by/measures pair as two stored edges, typing, reciprocal findings, unparented exemption
- [ ] 9. tools/gates/kit.py — the observed-result entry parser: AU11, the eight checks, Evidence-SHA256 recomputation
- [ ] 10. tools/gates/kit.py — fixtures T52–T63; selftest count to 63
- [ ] 11. Diff review of Phase 1 against D2–D4, D6 and the eight rulings
- [ ] 12. Pilot framed through /kerd:drive — question set 6 of 6, board entry live
- [ ] 13. Pilot viable and scoped — the condition agreed at scope in the producer's words
- [ ] 14. MSC-001 declared in the register, both edges stamped, before any pilot design artifact exists
- [ ] 15. MSC-001 keyed at the pilot's design gate — final, Approved = the MSC/v1 fingerprint
- [ ] 16. CARRIED — the pilot's spec names MSC-001 on every step whose work affects it
- [ ] 17. TRACKED — the pilot's loop closed; acceptance rung PASS; live tree clean
- [ ] 18. The reading taken; the evidence snapshotted and digested
- [ ] 19. Two decisions at the pilot's acceptance gate; the qualifying entry recorded; Outcome: PROVEN or NOT MET
- [ ] 20. Full local suite green; render current; zero unchecked boxes

---

## Phase 1 — the model, storage, links, checks, and the record parser

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

**Keyed 2026-09-01 — the code is `MSC`,** reader-facing name Measurable
Success Condition, disposition `applies`; the contingency above died
unexercised and the sealed views stand. The ruling attached a binding
consequence for the disposition's execution: `categories.md`'s framing must
split — twenty shipped requirement categories, and register artifact
extensions, currently `MSC` — because *"it must not quietly describe MSC as
another requirement category."* Step 5 executes exactly that.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — the category code:" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
```

Expected: exactly one line printed, carrying a real date and the producer's
decision, then `audit: clean` (findings acceptable).

### Step 2 — PRODUCER GATE: where the Observed result lives

[keep]

**The decision, in the producer's terms.** When the pilot's reading is taken
at its acceptance, where is it written down? It is a fourth object either way
— never a field on the condition. The two homes the design left open:

- **(a) A register category.** The reading is a block with its own ID
  (`OBS-001`-shaped), and an evidence link works exactly like every link
  today — no grammar change. Costs: the reading inherits the register's five
  states, which read oddly on an observation (what is a `proposed` reading?);
  and it owes its own code, its own `categories.md` row, keyed here as part
  of this ruling.
- **(b) An external evidence artifact.** The reading lives in a file — most
  naturally the pilot's acceptance record itself — and the register stays
  clean of evidence. Cost: the link grammar
  (`- <role> → <ID> (sha256:<12 hex>)`) cannot name a file today, so an
  evidence citation form would be new grammar the original score had no
  steps for — **composer hand-back (D1)**. This gate sits before the
  storage work precisely because this ruling changes the schema materially.

Record per D1 (topic `the Observed result's home`); if (a), the ruling names
the evidence category's code and disposition wording. Commit
(`Piece: requirements-success-measurement/2`).

**Keyed 2026-09-01 — neither home as drafted.** The Observed result lives in
the **immutable acceptance record** — not a register block (*"a reading is an
event: changing it tomorrow would falsify the record"* — no `OBS` code), and
not a stored link: the producer refused forcing `evidenced-by` through the
ID-only grammar AND pretending the suspect-link stamp supports a file
reference. The hand-back this obliged surfaced a conflict inside the ruling
itself — an outbound `MSC` reference versus inbound identity fields on the
entry — and a further ruling settled it: **the binding runs from the record
entry TO the condition** (inbound wins), the entry carries the `MSC` ID and
its exact frozen fingerprint plus a mandatory evidence digest, and discovery
is derived by scanning the records. This revision is that hand-back executed:
D6 is the entry contract; Steps 9, 10, 18 and 19 are its steps; `evidenced-by`
appears in no schema surface.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — the Observed result's home:" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
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
  player does not improvise it, and Steps 8–10 wait for the revised spec.
- **Owe it** → the pilot's proof knowingly carries the hole already drawn in
  the sealed anatomy view; the ruling names the return condition in the
  producer's words (the design doc records it; the debt is already a named
  row in `TODO.md`).

Record per D1 (topic `reciprocal stamping`). Commit
(`Piece: requirements-success-measurement/3`).

**Keyed 2026-09-01 — build now, scoped narrowly to the new Requirement ↔
`MSC` relationship.** His reason: *"If the requirement can change during
ordinary refinement while the MSC silently measures the old wording, the
smallest proof does not establish that alignment."* Required behaviour, his
list: `measured-by` stores the `MSC`'s full four-field fingerprint ·
`measures` stores the requirement's legacy statement fingerprint · the audit
requires BOTH directions for this role pair · a missing reciprocal edge or a
stale stamp is a **finding** at the existing suspect-link severity — *"Do not
inflate it into a refusal in this slice."* Existing role pairs are NOT
retrofitted. This requires TWO stored edges where the incumbent grammar
stores one — a departure the catalog transcription declares (D4b) rather
than hides. The hand-back this obliged is executed by this revision: the
mechanism is D2/D4, the build is Step 8, the fixtures are Step 10.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — reciprocal stamping:" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
```

Expected: exactly one RULED line with the decision, then `audit: clean`.

### Step 4 — PRODUCER GATE: the comparison — who performs it, and what checks it

[keep]

**The decision, in the producer's terms.** At the pilot's acceptance,
decision two compares the reading against the target frozen at `KEYED`. At
the GO the drawing shipped that comparison **unenforced** — the assurance
question added 2026-08-31 when the two-decision model exposed it. The
question to key: **for this slice, is the comparison performed by you at the
gate and recorded in the acceptance record — the mvp posture the sealed
drawing shows — or does a machine check land now?**

- **Producer-performed** → Step 19 executes it visibly: the record quotes the
  frozen target and the reading side by side and states the outcome; nothing
  on disk refuses a wrong verdict — that limit stays drawn, not hidden.
- **Machine-checked now** → an AU rule could compare a recorded reading
  against the frozen target — it needs a comparison grammar (what makes
  "2 of 2" satisfy "2 of 2") nobody has designed. **Composer hand-back
  (D1).**

This is the assurance line a machine could most plausibly own once the schema
exists; deferring it is not neglect, it is the recorded `mvp` boundary — but
the choice is the producer's, not this spec's. Record per D1 (topic
`the comparison`). Commit (`Piece: requirements-success-measurement/4`).

**Keyed 2026-09-01 — producer-performed in this slice.** The parser *"should
enforce structure, not invent semantics"*: confirm the entry exists when an
assessable outcome is claimed · names the `MSC` with its exact frozen
fingerprint · value and unit present · a legal outcome · `NOT ASSESSABLE`
preserved when no valid reading exists · the producer's key recorded as the
authority for whether the reading satisfies the target. Return condition, his
words: *"Revisit machine comparison when the `MSC` target grammar is
explicitly typed and at least one real condition requires a repeatable
comparison that the acceptance producer should not perform by judgment
alone."* Two later rulings resealed the boundary around this key: the
comparison row moved from `none` to **producer-agreed** (*"the comparison is
not assured by nothing… what remains absent is machine recomputation of that
semantic comparison"*), and the taxonomy split four ways — **machine-refused
· machine-detected · producer-agreed · no enforcement** — because a check
that FINDS is not a check that REFUSES. The resealed boundary counts
**fifteen** assurance questions by tense, four dual-marked, reciprocal
stamping the one machine-detected line; every total re-derived from the
drawing's rows, never adjusted arithmetically. Executed at Steps 9, 10
and 19.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "RULED .* — the comparison:" docs/design/requirements-success-measurement.md && python3 tools/gates/gate.py audit
```

Expected: exactly one RULED line with the decision, then `audit: clean`.
(The colon in the grep is load-bearing: a later ruling's topic — `the
comparison is producer-agreed, not unenforced` — begins with the same
words, and this check must match only the gate's own line.)

### Step 5 — categories.md: the split framing and the extension row

[delegate, model: sonnet, effort: low]

**What.** Edit `$repo_root/docs/requirements/categories.md`, two surgical
changes, nothing else:

1. The file's opening sentence
   `Which of the twenty categories this project owes requirements in.`
   becomes:
   `Which of the twenty requirement categories this project owes
   requirements in — plus, under `## Register artifact extensions` at the
   end of the file, the filing codes for register artifacts that are NOT
   requirements (currently `MSC`).`

2. Append at the end of the file:

   ```
   ## Register artifact extensions

   Filing codes the register carries for artifacts that are not
   requirements. They share the block grammar, the five states and the
   filing machinery; they are not categories this project owes requirements
   in, and no count above includes them. Introduced by
   `docs/design/requirements-success-measurement.md` — code and disposition
   keyed at the vocabulary-review gate (RULED 2026-09-01).

   | Code | Category | Disposition | Reason |
   |---|---|---|---|
   | MSC | Measurable Success Condition | applies | Kerd needs a first-class artifact for the predeclared threshold against which an observed result is judged. It is neither a requirement category such as NFR nor a check or method such as TST: the requirement states what must hold, MSC states the measure, baseline and target that count as met, and TST states how the reading is taken. Its distinct field obligations require a distinct filing key. |
   ```

   The Reason cell is the producer's keyed row, verbatim from the Step 1
   ruling — his words, not a template.

3. **Deliberate non-edits, and they are the point:** the twenty-row
   requirement table is untouched, and the closing count sentence
   (`**Eleven of the eighteen `applies` categories are unfilled** — …`)
   is untouched — `MSC` is NOT a requirement category, so the split framing
   is precisely what keeps those counts true. Do not add `MSC` to the
   requirement table, its counts, or its unfilled list.

**Why.** Executes Step 1's key under its attached constraint (*"it must not
quietly describe MSC as another requirement category"*) and the Step 2
ruling's `categories.md` consequence (the framing splits in two). The legal
category set is machine-read from this file by `parse_category_table`
(`kit.py:1293`), which scans EVERY `| CODE | … |` row in the file — any
table, headings ignored, fences excluded; verified 2026-09-01 — so the
extension row makes an `MSC` block legal to AU7 without joining the
requirement table. Commit (`Piece: requirements-success-measurement/5`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -n "^## Register artifact extensions" docs/requirements/categories.md && grep -n "^| MSC " docs/requirements/categories.md && grep -n "Eleven of the eighteen" docs/requirements/categories.md && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py selftest
```

Expected: the extension heading with its line number; exactly one
`| MSC | Measurable Success Condition | applies | …` row whose line number is
GREATER than the heading's (the row sits in the extension table, not the
requirement table); the untouched closing count (`Eleven of the eighteen`);
`audit: clean`; `selftest: 51 cases passed` (nothing else changed yet).

### Step 6 — catalog.md: the corrected strike, the two-edge pair, the fields, the fingerprint

[delegate, model: sonnet, effort: medium]

**What.** Edit `$repo_root/docs/requirements/catalog.md`
exactly as D4's transcription specifies — the three edits (a), (b), (c),
copied from D4 verbatim, and NOTHING else in the file:

- (a) the deferred paragraph in `## Fields` split as shown, the struck span
  preserved verbatim inside `~~…~~`, the **Superseded** note adjacent — the
  design's CORRECTED recorded wording, executed ("entries in the immutable
  acceptance record, bound to the condition by its frozen fingerprint" —
  never the pre-ruling "linked evidence");
- (b) the `## Link roles` table: the `measured-by` row appended, the
  `verified-by` row rewritten with its original wording preserved inside the
  annotation, the two-edge departure note added directly below the table,
  `satisfied-by` untouched — and NO `evidenced-by` row, the role having been
  removed by the binding-direction ruling before it ever landed;
- (c) the three field rows added to the `## Fields` table after `Tags`, and
  the keyed-freeze paragraph appended to `## States, and what each one owes`.

Never delete superseded text; the strike preserves it. **Why.** The catalog
is the declared grammar the register is validated against; a role must be
registered before anything writes it (the StrictDoc rule the catalog itself
cites), a role pair departing from the one-declaration convention must be
declared as departing, and the supersession's execution was recorded at the
design gate as belonging to exactly this schema implementation. Commit
(`Piece: requirements-success-measurement/6`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -c "~~Acceptance Criteria and Verification Method (the forward trace, slice" docs/requirements/catalog.md && grep -n "measured-by\|re-sourced 2026-09-01\|stored as TWO edges" docs/requirements/catalog.md && grep -n "four owned fields" docs/requirements/catalog.md && test "$(awk '/evidenced-by/{n++} END{print n+0}' docs/requirements/catalog.md)" -eq 0 && echo "no-evidenced-by" && python3 tools/gates/gate.py audit
```

Expected: `1` (the struck span exists exactly once — this `grep -c` expects a
NONZERO count, so its exit code correctly reddens the chain if the strike is
missing), the new role row, the re-sourced `verified-by` row and the
departure note printed with line numbers, the keyed-freeze paragraph found,
then `no-evidenced-by` (the zero-count taken with `awk` and asserted with
`test`, exit-safe in both directions), then `audit: clean`.

### Step 7 — PRODUCER-GATED: the approval fingerprint — one mechanism, one payload, two renderings

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

2. **`_approval_digest` / `approval_fingerprint` /
   `approval_fingerprint_full`** at the current `req_statement_hash` site
   (~line 1191), D3 verbatim — and `req_statement_hash` becomes D3's
   delegation, its name and signature kept for every existing caller and
   fixture. `approval_fingerprint_full` is dormant until Step 9's parser
   consumes it — landing it here keeps the byte stream defined once. After
   this edit exactly ONE `hashlib.sha256` call encodes an approval payload —
   `_approval_digest`; grep the diff and find no other in the register
   machinery. (Step 9 later adds the one OTHER sha256 site — evidence bytes
   — deliberately separate: two digests, two jobs.)

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
asserted), and the five probe lines. Commit
(`Piece: requirements-success-measurement/7`) only on his key; the
completion note records it. This gate approves the LANDING of ruled work —
it re-opens nothing: the shape is settled in the design's `## The approval
fingerprint — ruled 2026-09-01` and transcribed in D3. **A refusal here is a
hand-back (D1), and it invalidates Steps 8–11 as written — every one leans
on the landed mechanism.** With the landing, the living design's owed-label
comes true for ONE of its four owed mechanisms and is updated in the same
commit: in the first bullet of `## What this design does not settle`,
annotate the versioned approval fingerprint with
` (built YYYY-MM-DD — Step 7 of the contract spec)`, and the lifecycle
table's `KEYED` row drops "owed, not present" for "built YYYY-MM-DD". The
other three mechanisms stay labeled owed until Steps 8–10 land theirs. The
sealed views are NOT touched — the assurance drawing already carries both
tenses (its dual-marked lines), which is why it was drawn that way.

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
full = kit.approval_fingerprint_full('MSC', f)
print('one-payload-two-renderings', a == 'sha256:' + full[:12] and len(full) == 64)
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
one-payload-two-renderings True
```

### Step 8 — kit.py: the schema — fields, the two-edge pair, typing, reciprocity

[delegate, model: sonnet, effort: high]

**What.** Edit `$repo_root/tools/gates/kit.py`.
Stdlib only. No function signature changes. Five edits:

1. **Constants** (beside `REQ_ORIGIN_CATEGORIES`, ~line 110): add
   `REQ_CONDITION_CATEGORIES` and `REQ_CONDITION_FIELDS` per D4, with a
   comment citing the origin-categories precedent (kit names the codes whose
   semantics it enforces; the legal set stays per-project in categories.md).
   Extend `REQ_META_FIELDS` by appending `"Measure", "Baseline", "Target"`.
   Extend `REQ_LINK_ROLES` with `"measured-by": "measures"`
   (`REQ_LEGAL_ROLES` derives automatically).

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
   `f"{reg_rel} — {rid}: …"` prefix — the five rules and exact strings of
   D4 item 4. Guard target-category checks with `target in ids`.

4. **Reciprocal presence** — the Step 3 ruling executed. After the per-link
   loop, compare the set of stored `measured-by` edges (requirement → `MSC`)
   with the set of stored `measures` back-edges (`MSC` → requirement); each
   direction present without its reciprocal appends the D4 item-5 FINDING to
   the `findings` list (never a problem — *"Do not inflate it into a refusal
   in this slice"*), attributed to the block that owes the missing edge, and
   only where both named IDs exist (a nonexistent target is already a
   problem from the base checks). **Staleness needs NO new code here**:
   Step 7's generalized stamp check already compares EVERY stored edge's
   stamp against its own target's current approval fingerprint, so once both
   edges are stored, editing the requirement's statement stales the
   `measures` stamp on the condition — the dangerous direction the design
   named ("edit the source and nothing flags") closed by the second stored
   edge riding existing machinery.

5. **The unparented-finding exemption**: in the `unparented` comprehension
   near the end of `register_check`, exclude condition categories alongside
   origin categories, with the comment
   `# a condition's parentage is the measures edge, not refines`.

**Why.** With the fingerprint mechanism already landed (Step 7), this is
the register half of the machine work: D2's obligations and D4's edges, each
refusing exactly what the design says must not happen — a field creeping
onto the requirement block, a role quietly keeping its old source — and the
two-edge reciprocal contract at exactly the ruled severity. **No fixtures in
this step** — the existing 51 must still pass untouched, which proves the
new rules fire only on condition-category blocks and the new roles (none of
which exist in any current fixture or in the live register — verified
2026-09-01). With the landing, annotate the design's owed-label for
reciprocal stamping in the same commit:
` (built YYYY-MM-DD — Step 8, fixtures Step 10)`. Also update
`tools/gates/README.md`'s AU8 row: the stamp is now the target's
category-aware approval fingerprint, and the reciprocal-presence finding
joins the row's finding list (the AU9 precedent: the README row and the
docstring must stay in step). Commit
(`Piece: requirements-success-measurement/8`).

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
req_fp = kit.req_statement_hash(s_req)
reg = (
    "# R\n\n## FUN — Functional\n\n"
    "### FUN-001 — r\n\n**Category**: FUN\n**State**: proposed\n**Source**: x\n\n"
    + s_req + "\n\n**Links**\n- measured-by → MSC-001 (" + msc_fp + ")\n\n"
    "## MSC — Measurable Success Condition\n\n"
    "### MSC-001 — c\n\n**Category**: MSC\n**State**: final\n**Source**: x\n"
    "**Measure**: " + m + "\n**Baseline**: " + bl + "\n**Target**: " + tg + "\n"
    "**Approved**: " + msc_fp + "\n\n"
    + s_msc + "\n\n**Links**\n- measures → FUN-001 (" + req_fp + ")\n- verified-by → TST-001 (" + kit.approval_fingerprint('TST', {'Statement': s_tst}) + ")\n\n"
    "## TST — Testing / Validation\n\n"
    "### TST-001 — t\n\n**Category**: TST\n**State**: proposed\n**Source**: x\n\n" + s_tst + "\n")
p = os.path.join(d, 'docs', 'requirements', 'register.md')
open(p, 'w', encoding='utf-8').write(reg)
rc = kit.register_check(d)
print('clean', rc['blocks'], rc['links'], [f for f in rc['findings'] if 'reciprocal' in f])
print('unparented-exempt', not any('MSC-001' in f for f in rc['findings']))
open(p, 'w', encoding='utf-8').write(reg.replace(s_req, s_req + " Now reworded."))
rc = kit.register_check(d)
print('requirement-moved-flags-the-measures-edge',
      any('MSC-001: link stamp for FUN-001 is stale' in f for f in rc['findings']),
      rc['blocks'] == [] and rc['links'] == [])
bad = reg.replace('**Target**: 2 of 2', '**Target**: 1 of 2').replace(
    '**State**: proposed\n**Source**: x\n\n' + s_req,
    '**State**: proposed\n**Source**: x\n**Measure**: sneaky\n\n' + s_req).replace(
    '- measures → FUN-001 (' + req_fp + ')\n', '')
open(p, 'w', encoding='utf-8').write(bad)
rc = kit.register_check(d)
for pr in rc['blocks']:
    print(re.sub(r'sha256:[0-9a-f]{12}', 'sha256:*', pr))
print('stamp-stale', any('link stamp for MSC-001 is stale' in f for f in rc['findings']))
print('reciprocal-missing', any('reciprocal link missing' in f and 'MSC-001' in f for f in rc['findings']))
EOF
```

Expected, exactly (after `selftest: 51 cases passed` and `audit: clean`):

```
clean [] [] []
unparented-exempt True
requirement-moved-flags-the-measures-edge True True
docs/requirements/register.md — FUN-001: field 'Measure' is legal only on a success-condition block — the requirement block gains no field
docs/requirements/register.md — MSC-001: 'Approved' diverges from the condition's four owned fields (approved sha256:*, condition now sha256:*) — refused; the state is never rewritten
stamp-stale True
reciprocal-missing True
```

Note what the probe quietly demonstrates, in both directions. ONE `Target`
edit diverges the `Approved` (AU7, repo-red) AND stales the `measured-by`
stamp on `FUN-001` (the finding — the source flagged for re-look), while the
statement never moved: the 2026-09-01 fingerprint ruling working. And ONE
statement edit on the REQUIREMENT — the direction the shipped mechanism
could not see at all — stales the `measures` stamp on `MSC-001`, a finding
and only a finding: the reciprocal ruling working at exactly its ruled
severity.

### Step 9 — kit.py: the observed-result entry parser — AU11, the eight checks, the digest

[delegate, model: sonnet, effort: high]

**What.** Edit `$repo_root/tools/gates/kit.py` (and one row in
`$repo_root/tools/gates/README.md`). Stdlib only. This is the machine half
of the acceptance rulings — the parser *"should enforce structure, not
invent semantics"*. Four edits:

1. **Constants** beside the other `REQ_*` constants:

   ```python
   # The observed-result entry (requirements-success-measurement, spec D6):
   # an immutable acceptance-record entry binding a reading to the exact
   # frozen condition. Seven fields, nine required facts, eight
   # qualification checks — a required fact the parser does not check is
   # not a requirement.
   OBS_ENTRY_FIELDS = (
       "Condition", "Observed", "Method", "Taken",
       "Evidence", "Evidence-SHA256", "Outcome",
   )
   OBS_CONDITION_RE = re.compile(
       r"^Condition:\s+([A-Z]{2,4}-\d{3}) \(fingerprint:([0-9a-f]{64})\)$"
   )
   OBS_FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):\s+(.*\S)\s*$")
   OBS_METHOD_RE = re.compile(r"^TST-\d{3}$")
   ```

2. **`observed_results(root)`** — the derived-discovery scan the
   binding-direction ruling requires. Globs sorted
   `docs/gates/*-acceptance.md` then `*-goal.md` (exactly the files
   `acceptance_record` reads, `kit.py:892`), reads RAW lines — fences
   included — and applies D6: the opener regex, the malformed-line guard,
   the shape refusals (missing / duplicate / unknown field), then the EIGHT
   checks with D6's verbatim strings. The register is loaded once via
   `parse_register`, and BOTH resolution checks ride that one load —
   check 1's condition lookup and check 6's method lookup (an ID whose
   block is absent, or whose `Category` is not `TST`, is refused with the
   resolution string); the fingerprint recomputes via
   `approval_fingerprint_full`; the evidence digest recomputes via ONE
   `hashlib.sha256` over the referenced file's raw bytes — the second and
   last digest call site in this machinery, hashing bytes, never fields.
   Returns `{"entries": {<MSC-ID>: [{"fields": {…}, "file": <basename>,
   "line": <n>}]}, "problems": […]}` — **qualifying entries only** under
   `"entries"`; a non-qualifying entry lands in `"problems"` and nowhere
   else. That return shape is a contract Step 19's verify reads — keep it
   exact.

3. **`_audit_au11(root)`** returning `observed_results(root)["problems"]`,
   registered in `audit()` after `_audit_au10`; the `audit()` docstring's
   `AU1-AU10` becomes `AU1-AU11`.

4. **`tools/gates/README.md`**: an AU11 row in the AU table — the entry
   shape, the eight checks, the malformed-line guard, the two-digest split,
   and the severity (refusals: an acceptance record carrying a
   non-qualifying observed-result entry is a `problem`, red, because a
   record that claims an outcome must qualify or not stand) — and the
   file's `AU1–AU10` mentions updated (grep for the literal).

With the landing, annotate the design's owed-labels for the TWO mechanisms
this builds — the structural acceptance-record parser and `Evidence-SHA256`
recomputation — with ` (built YYYY-MM-DD — Step 9)` in the first bullet of
`## What this design does not settle`, same commit. After this step all four
owed mechanisms carry built annotations (Steps 7, 8, 9); Step 11's review
confirms the labels honest.

**Why.** Decision 1 of acceptance becomes entirely the machine's: *"the
machine proves the comparison is bound to the right frozen target and that
the evidence record is complete; the producer judges the result."* The
refusal is what keeps a non-qualifying entry from standing as `PROVEN` on a
green tree; the qualification verdict is what keeps `NOT ASSESSABLE`
derivable, never authored — both derivation paths mechanical (D6). The
assurance boundary's designed tense comes true for its parser and digest
lines (machine-refused), exactly as the resealed drawing dual-marked them.
**No fixtures in this step** — the live tree carries no entries (verified
2026-09-01: zero `^Condition:` lines under `docs/gates/`), so `audit` must
not change and the existing 51 cases must still pass untouched. Check 6's
resolution half is RULED (2026-09-01, correcting this spec's earlier
shape-only reading): a phantom method makes the result unverifiable and
therefore `NOT ASSESSABLE` — and the reference stays version-unpinned: no
method fingerprint, no stamp, no `Method-SHA256`; that follow-up integrity
question is the producer's separate filing, not this contract's. Commit
(`Piece: requirements-success-measurement/9`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 - <<'EOF'
import hashlib, os, sys, tempfile
sys.path.insert(0, 'tools/gates'); import kit
d = tempfile.mkdtemp()
for sub in (('docs', 'gates'), ('docs', 'requirements'), ('evidence',)):
    os.makedirs(os.path.join(d, *sub))
open(os.path.join(d, 'docs', 'requirements', 'categories.md'), 'w', encoding='utf-8').write(
    "| MSC | Measurable Success Condition | applies |  |\n"
    "| TST | Testing / Validation | applies |  |\n")
s_msc = "Both disagreement directions are refused by the audit."
m, bl, tg = "fixture directions refused", "0 of 2", "2 of 2"
f = {'Statement': s_msc, 'Measure': m, 'Baseline': bl, 'Target': tg}
open(os.path.join(d, 'docs', 'requirements', 'register.md'), 'w', encoding='utf-8').write(
    "# R\n\n## MSC — Measurable Success Condition\n\n"
    "### MSC-001 — c\n\n**Category**: MSC\n**State**: final\n**Source**: x\n"
    "**Measure**: " + m + "\n**Baseline**: " + bl + "\n**Target**: " + tg + "\n"
    "**Approved**: " + kit.approval_fingerprint('MSC', f) + "\n\n" + s_msc + "\n\n"
    "## TST — Testing / Validation\n\n"
    "### TST-006 — t\n\n**Category**: TST\n**State**: proposed\n**Source**: x\n\n"
    "Run the fixtures and count refusals.\n")
ev = os.path.join(d, 'evidence', 'reading.txt')
open(ev, 'w', encoding='utf-8').write("2 of 2 directions refused at abc1234\n")
entry = (
    "Condition: MSC-001 (fingerprint:" + kit.approval_fingerprint_full('MSC', f) + ")\n"
    "Observed: 2 of 2\n"
    "Method: TST-006\n"
    "Taken: 2026-09-01\n"
    "Evidence: evidence/reading.txt\n"
    "Evidence-SHA256: " + hashlib.sha256(open(ev, 'rb').read()).hexdigest() + "\n"
    "Outcome: PROVEN\n")
rec = ("---\nroute: new\nstage: ready-to-release\n---\n\n# A\n\n## Release condition\n\nok\n\n"
       "## The success condition, evaluated\n\n```\n" + entry + "```\n")
gp = os.path.join(d, 'docs', 'gates', '2026-09-01-x-acceptance.md')
open(gp, 'w', encoding='utf-8').write(rec)
res = kit.observed_results(d)
print('qualifies', res['problems'] == [], sorted(res['entries']), len(res['entries']['MSC-001']))
open(gp, 'w', encoding='utf-8').write(rec.replace('Method: TST-006', 'Method: TST-999'))
res = kit.observed_results(d)
print('method-unresolved', any("Method 'TST-999' does not resolve to a TST block" in p for p in res['problems']),
      res['entries'].get('MSC-001', []) == [])
open(gp, 'w', encoding='utf-8').write(rec)
open(ev, 'a', encoding='utf-8').write("tampered\n")
res = kit.observed_results(d)
print('digest-refused', any('Evidence-SHA256 does not recompute' in p for p in res['problems']),
      res['entries'].get('MSC-001', []) == [])
print('au11-rides-audit', any('Evidence-SHA256 does not recompute' in p for p in kit.audit(d)))
EOF
```

Expected (after `selftest: 51 cases passed` and `audit: clean` on the live
tree, its findings line unchanged), exactly:

```
qualifies True ['MSC-001'] 1
method-unresolved True True
digest-refused True True
au11-rides-audit True
```

The probe exercises both halves of the ruled check 6: `TST-006` resolves to
a real `TST` block and qualifies; `TST-999` parses perfectly and resolves to
nothing, so the SAME record is refused with the resolution string — a
phantom method is `NOT ASSESSABLE`, exactly like the missing evidence file
it is then proven alongside: one appended line of "tampering" flips the
restored record from qualifying to refused with no edit to the record
itself, the evidence digest doing the exact job the ruling gave it. No
method fingerprint and no version-pinning anywhere — the reference resolves,
it does not freeze.

### Step 10 — fixtures T52–T63

[delegate, model: sonnet, effort: medium]

**What.** In `$repo_root/tools/gates/kit.py`'s
`_selftest_body`, after T51, add twelve cases in the house style (each a
comment `# T<n> — <what it pins>`, a temp tree via the existing helpers or
inline writes, exact-string asserts against the D4 and D6 strings):

- **T52** — the happy path: a `proposed` condition block with all four owned
  fields; a requirement carrying `measured-by` into it stamped with the
  condition's FULL fingerprint (`approval_fingerprint('MSC', …)`); the
  condition carrying `measures` back, stamped with the requirement's legacy
  statement fingerprint, and `verified-by` out to a TST block stamped with
  the TST's legacy fingerprint → `register_check` returns empty `blocks`
  and `links`, NO stale-stamp finding, NO `reciprocal link missing` finding,
  and the condition block's ID appears in NO finding (the unparented
  exemption).
- **T53** — the keyed freeze: the same condition at `final` with
  `Approved = approval_fingerprint('MSC', …)` → clean; then the `Target`
  edited → exactly the D4 item-3 divergence string (assert with the hashes
  normalized, e.g. `re.sub(r'sha256:[0-9a-f]{12}', 'sha256:*', p)`).
- **T54** — `**Measure**` on a `FUN` block → exactly the D4 item-2 string.
- **T55** — a condition block missing `Baseline` → exactly the D4 item-1
  string for `'Baseline'`.
- **T56** — typing, all four ways: `measured-by` pointing at a non-condition
  block · `measured-by` riding a condition block · `measures` riding a
  non-condition block · `measures` pointing at a condition block → the four
  D4 item-4 strings (the fifth, `verified-by`, is T57's).
- **T57** — `verified-by` riding a requirement (`FUN`) block → the
  re-source string.
- **T58** — an MSC-targeting stamp uses the four-field fingerprint, proven
  both ways, on a `proposed` condition so the stamp is isolated from AU7's
  `Approved` check: (i) a correct full-fingerprint `measured-by` stamp, then
  the condition's `Target` alone edited (statement untouched) → the
  stale-stamp FINDING appears in `findings`, `blocks` and `links` stay empty
  — a finding, never a problem, and exactly the drift a statement-only stamp
  could not see. (ii) The same link stamped
  `req_statement_hash(<the condition's statement>)` — the superseded recipe
  — is stale from birth: the finding fires with no edit at all. Assert
  against the string the code actually emits — `link stamp for <ID> is
  stale (stamped sha256:…, target now sha256:…) — re-look, then restamp`
  (the stamp check, Step 7 edit 3) — NOT the catalog's paraphrase "flagged
  for re-look", which appears in no emitted string.
- **T59** — byte-for-byte preservation AND the two renderings, pinned from
  outside the mechanism:
  `approval_fingerprint('FUN', {'Statement': s}) == req_statement_hash(s)`
  as equal strings;
  `approval_fingerprint('MSC', f) == 'sha256:' + approval_fingerprint_full('MSC', f)[:12]`
  and `len(approval_fingerprint_full('MSC', f)) == 64`; a `final`
  legacy-category block whose `Approved` is the statement hash passes the
  generalized comparison clean; a link targeting a legacy block, stamped
  with the statement hash, raises no finding. (T1–T51 passing untouched is
  the broader half of the same proof.)
- **T60** — reciprocal presence, the ruled two-edge contract: `measured-by`
  with no `measures` back-edge → the D4 item-5 FINDING naming both blocks;
  `measures` with no `measured-by` back-edge → the mirror finding; both
  edges present and fresh → no reciprocal finding. Findings, never problems
  — `blocks` and `links` stay empty throughout, pinning the ruled severity
  so nobody later inflates it into a refusal without a producer key.
- **T61** — the dangerous direction covered: both edges present and fresh,
  then the REQUIREMENT's statement alone edited → the `measures` stamp on
  the condition goes stale (the stale-stamp finding), `blocks` and `links`
  stay empty. The hole the design named — "edit the source and nothing
  flags" — closed by the second stored edge.
- **T62** — the entry parser refuses each broken shape and check, exact D6
  strings, each proven excluded from `entries`: a malformed `Condition:`
  line · a missing field · an unknown `MSC` ID · a diverged fingerprint · a
  missing evidence file · a digest mismatch · a unit-less `Observed` · a
  syntactically invalid `Method` (not `TST-nnn` — the syntax string) · a
  well-formed `Method` naming a `TST` that resolves to nothing (`TST-999`)
  and a well-formed `Method` resolving to a block whose `Category` is not
  `TST` (both refused with the resolution string — a phantom method is
  `NOT ASSESSABLE`, ruled 2026-09-01; and neither case gains a fingerprint
  or version pin) · an unreal date (`2026-13-40`) · an illegal `Outcome`
  (`PASSED`).
- **T63** — `NOT ASSESSABLE` preserved, both derivation paths: a keyed
  condition with no entry anywhere → `observed_results` has no key for the
  ID (path one); a qualifying entry → present under the ID with its parsed
  fields and `_audit_au11` empty; a non-qualifying entry → absent from
  `entries` AND named in `problems`, never silently dropped (path two).

Update the count literal in ALL THREE places it lives — the `selftest`
docstring's two mentions ("Run the 51 fixture-built cases" and
"'selftest: 51 cases passed'") and the printed line (`kit.py:2851`,
`kit.py:2852` and `kit.py:2859` as of this spec's writing; Steps 7–9 shift
them — grep for the literal) — to `63`. **Why.** The fixtures are what make
the schema and the record parser refuse from outside the model, in CI, on
every push — the same rung the rest of the gate machinery stands on. Commit
(`Piece: requirements-success-measurement/10`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit
```

Expected: `root resolution: 7 cases passed` then `selftest: 63 cases passed`,
then `audit: clean`.

### Step 11 — diff review of Phase 1 against D2–D4, D6 and the eight rulings

[keep]

**What.** Read the full diff of Steps 5–10 (from the commit before Step 5 to
HEAD — find the base with `git log --oneline`, the commit preceding the
`Piece: requirements-success-measurement/5` trailer) with D2–D4, D6 and the
design's `## Rulings after the GO` open beside it. Hunt drift outside the
named symbols:

- every existing hash byte-identical: `req_statement_hash(s)` returns the
  same string it did before Phase 1 for every input (delegation into
  `approval_fingerprint`, never a second byte-stream definition); exactly
  TWO `hashlib.sha256` call sites in the register-and-record machinery —
  `_approval_digest` (canonical payloads: fields) and Step 9's evidence
  recomputation (raw bytes) — the two-digest split held, any third is
  drift; `docs/requirements/register.md` ABSENT from the diff — no live
  `Approved` value or stamp moved; `tools/reqview/` untouched;
  `REQ_LINK_RE` untouched — the binding-direction ruling required NO
  link-grammar change, which is part of why the removed edge was
  unnecessary as well as unbuildable;
- the catalog strike preserves every original word, and the Superseded note
  carries the CORRECTED recorded wording — "entries in the immutable
  acceptance record, bound to the condition by its frozen fingerprint",
  never the pre-ruling "linked evidence"; nothing else in `catalog.md`
  reworded; `satisfied-by` untouched;
- `evidenced-by` / `evidences` fully absent from every schema surface — the
  Verify below makes it mechanical;
- the design's owed-labels honest: all four mechanisms in the first
  does-not-settle bullet carry built annotations naming their steps, and no
  label claims more than its step landed;
- no file under `skills/` touched — `git diff <base>..HEAD --stat` lists
  ONLY: `docs/requirements/categories.md`, `docs/requirements/catalog.md`,
  `tools/gates/kit.py`, `tools/gates/README.md` (the AU rows),
  `docs/design/requirements-success-measurement.md` (the owed-label
  annotations), this spec (ticked boxes), and progress-render outputs —
  plus, only if a session boundary fell inside Phase 1, the switch-owned
  state files (`CONTEXT.md`, `TODO.md`, `kivna/sessions/*`), which belong
  to `/kerd:switch` per `docs/state-contract.md`, not to any step here,
  and carry no schema;
- every problem and finding string in the code matches D4 and D6
  character-for-character (the fixtures assert most of this; the eye
  catches a string the fixtures and the code agree on that the SPEC does
  not);
- the sealed views' fingerprints unchanged: no `.html` under
  `docs/design/requirements-success-measurement/` in the diff.

A finding here is fixed by the step that owns the file, then this review
reruns.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && test "$(grep -rE 'evidenced-by|"evidences"' docs/requirements tools/gates 2>/dev/null | awk 'END{print NR}')" -eq 0 && echo "role-fully-removed" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release
```

Expected: `role-fully-removed` — the zero-count is exit-safe in both
directions: the grep runs inside `$( )` where its no-match exit cannot abort
the chain, `awk` prints the line count (`0` at zero matches), and `test`
asserts it — so the chain goes red the moment any schema surface regrows the
role, and green means genuinely absent. Then the selftest count from
Step 10, `audit: clean`, `release: clean` — and the diff-stat inspection
above recorded in the step's completion note with any drift named.

---

## Phase 2 — the pilot framed, its condition declared before its design gate

### Step 12 — frame `stage-route-consistency` through /kerd:drive

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
framing should already be audible in the A3 answer — that is what Step 13
agrees into a condition. Commit (`Piece: requirements-success-measurement/12`),
then `python3 tools/diagram/progress.py`, render commit, ONE push — this
step puts a new item on the board.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py route stage-route-consistency && python3 tools/gates/gate.py audit
```

Expected: the route render's first rung line is `frame  pass`, the verdict
line is `enters at: viability` (or deeper if the sitting continued), no
`need:` line names the Question set, and `audit: clean`.

### Step 13 — pilot viability and scope: the condition agreed at scope

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
draft condition in front of him as a draft; what he agrees is what Step 14
transcribes, and his wording overrides the draft wherever they differ. Write
the agreed condition into the pilot's `## Scope` so the agreement has a home
on disk before the register block exists. The same sitting also files the
requirement's register category — Step 14 item 1's two live candidates
(`TST` vs `DATA`) are argued to the producer here, and his filing is written
into `## Scope` beside the condition, so Step 14's transcriber inherits a
decision, not a question. Stage advances only as rungs
complete (`viable`, then `scoped`). Commit
(`Piece: requirements-success-measurement/13`), progress render, ONE push.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py route stage-route-consistency && python3 tools/gates/gate.py audit
```

Expected: `enters at: design`, and `audit: clean`.

### Step 14 — declare the condition in the register — before any design artifact exists

[delegate, model: sonnet, effort: medium]

**What.** Transcribe the Step 13 agreement into
`$repo_root/docs/requirements/register.md`
— three blocks and three links, D2's shapes exactly:

1. **The requirement** the condition measures — a new block carrying the
   producer's agreed statement of the rule itself. File it under the
   category the producer filed at Step 13's sitting, recorded in the
   pilot's `## Scope` (the two live candidates, argued either way in this
   repo's own terms: **TST** — the sentence rules on a check that produces
   a stopping verdict; **DATA** — it binds how faithfully a written record
   mirrors what it stands for. The producer's filing at Step 13 decides;
   this spec deliberately does not). State `proposed`, `Source` naming
   `docs/product/stage-route-consistency.md` and the date.
2. **`MSC-001`** — the condition block, D2's grammar, the four owned fields
   carrying the producer's agreed words, `State: proposed` (`DECLARED` —
   keying is Step 15's gate, not this step). Under a new
   `## MSC — Measurable Success Condition` section placed before
   `## Archive`.
3. **`TST-006`** — the method block: its statement is HOW the reading is
   taken (the commands run, what is counted), the producer's agreed method
   wording.
4. **Links — both directions of the pair, plus the re-sourced role.** On
   the requirement, `- measured-by → MSC-001 (sha256:…)`; on `MSC-001`,
   `- measures → <REQ-ID> (sha256:…)` AND
   `- verified-by → TST-006 (sha256:…)`. Writing only one direction of the
   pair leaves a `reciprocal link missing` finding from birth — D4's audit
   clause. Stamps are the targets' **approval fingerprints** (ruled
   2026-09-01): the `MSC` target's is its full four-field fingerprint,
   never its statement hash; the requirement and `TST` targets' are their
   legacy statement-only fingerprints. One mechanism decides all three —
   compute them, never guess (run with the requirement's ID as filed):

   ```
   python3 - <<'EOF'
   import sys; sys.path.insert(0, 'tools/gates'); import kit
   blocks, _ = kit.parse_register(open('docs/requirements/register.md', encoding='utf-8').read())
   for i in ('MSC-001', 'TST-006', '<REQ-ID as filed>'):
       b = next(x for x in blocks if x['id'] == i)
       print(i, kit.approval_fingerprint(b['fields']['Category'],
                                         dict(b['fields'], Statement=b['statement'])))
   EOF
   ```

5. **`categories.md` needs NO edit for `MSC`** — under Step 5's split
   framing, `MSC` is an extension outside the requirement-category counts;
   that is the split working, not an omission. ONE branch, decided by the
   producer's Step 13 filing: if the requirement was filed under a
   previously unfilled requirement category (`DATA` is the live candidate;
   `TST` is already filled), the closing count sentence drops that code
   and decrements once (`Ten of the eighteen` in the DATA case) — the
   sentence states the tree's actual counts, and only the requirement's
   filing moves it.

**The ordering constraint is the step's whole point**: this lands while NO
design artifact for the pilot exists — no `docs/design/stage-route-consistency*`,
no `concerns:` block in its product doc. Declared BEFORE design, on disk,
provably. **Why.** This is the capability's first real use: the register
carries a success condition for a live work item ahead of its design, 0 → 1.
Commit (`Piece: requirements-success-measurement/14`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && (ls docs/design | grep stage-route-consistency || echo none) && (grep -n "^concerns:" docs/product/stage-route-consistency.md || echo no-concerns) && python3 - <<'EOF'
import sys; sys.path.insert(0, 'tools/gates'); import kit
blocks, _ = kit.parse_register(open('docs/requirements/register.md', encoding='utf-8').read())
msc = next(b for b in blocks if b['id'] == 'MSC-001')
print('MSC-001', msc['fields']['State'],
      all(msc['fields'].get(f, '').strip() for f in ('Measure', 'Baseline', 'Target')))
print('links', sorted((r, t) for r, t, _ in msc['links']))
src = next(b for b in blocks if any(r == 'measured-by' for r, _, _ in b['links']))
print('measured-by from', src['id'])
fp = kit.approval_fingerprint(msc['fields']['Category'],
                              dict(msc['fields'], Statement=msc['statement']))
print('stamp is the four-field fingerprint',
      any(r == 'measured-by' and t == 'MSC-001' and f'sha256:{s}' == fp
          for r, t, s in src['links']))
print('reverse stamp is the statement-only fingerprint',
      any(r == 'measures' and t == src['id'] and f'sha256:{s}' == kit.req_statement_hash(src['statement'])
          for r, t, s in msc['links']))
EOF
python3 tools/gates/gate.py audit
```

Expected: `none` then `no-concerns` (no design artifact and no `concerns:`
block — both halves of the before-design claim, mechanical; the `|| echo`
fallbacks keep the zero-match direction green, which is the direction this
step requires), then exactly `MSC-001 proposed True`,
`links [('measures', '<REQ-ID>'), ('verified-by', 'TST-006')]`,
`measured-by from <REQ-ID>` (the ID as filed at the sitting), both stamp
lines `True` (a statement-only stamp on the `MSC` target prints `False` —
wrong even though the audit would show it only as a stale-stamp finding),
then `audit: clean` — the findings line may grow by the new unparented
non-origin blocks; `MSC-001` must NOT be among them, and NO
`reciprocal link missing` finding may print.

### Step 15 — the pilot's design gate keys the condition

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
going stale. Keying edits `State` and `Approved` only; neither is in any
payload, so BOTH stamps written at Step 14 stay matched — the `measured-by`
stamp rides the four owned fields (untouched) and the `measures` stamp rides
the requirement's statement (untouched). The pilot's design GO record
(`docs/gates/<date>-stage-route-consistency-design.md`, front matter, Clock
line from a real `date` run) is written by that sitting as its own gate
artifact. Commit (`Piece: requirements-success-measurement/15`), progress
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

### Step 16 — CARRIED: the pilot's spec names the condition

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

### Step 17 — TRACKED: the pilot's loop lands aimed at the condition

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

### Step 18 — take the reading; snapshot and digest the evidence

[delegate, model: sonnet, effort: medium]

**What.** At the pilot's acceptance sitting, BEFORE the gate's decisions:
execute `TST-006`'s method exactly as its statement says — run the named
commands, at the current HEAD, and record what they actually print. The
reading is the verbatim result in the Measure's units (e.g. "2 of 2
directions refused; overclaim fixture problem: `<the exact line>`;
underclaim fixture problem: `<the exact line>`; live audit clean at
`<commit>`") — **taken, never asserted**; if a command fails, the reading
records the failure, and that too is a reading. Then make the reading a
hashable artifact — D6's evidence rules: a digest that cannot be recomputed
is decoration, so the evidence must be stable local bytes BEFORE acceptance:

1. **The snapshot.** Write the captured output verbatim — with the date,
   the commit, and the commands run — to a repo-relative file. Default
   home: `docs/gates/<date>-stage-route-consistency-acceptance-evidence.txt`
   — dated, immutable, beside the record that will cite it; AU3 globs only
   `*.md` (verified at `kit.py:1070`), so the `.txt` sits outside its
   filename contract. The producer may name a different repo-relative home
   at the sitting; the entry's `Evidence:` line carries whatever path was
   used. The snapshot is never edited after Step 19 cites it — an edit
   breaks the digest and AU11 refuses the record, which is the design
   working, not an inconvenience.
2. **The digest.** `Evidence-SHA256` over the file's raw bytes:

   ```
   python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <the evidence path>
   ```

3. **The entry, drafted six-sevenths.** Prepare the entry's first six lines
   in the step's completion note — `Condition` (the ID and
   `approval_fingerprint_full` computed same-turn, never typed from
   memory), `Observed` (value AND unit, in the Measure's units),
   `Method: TST-006`, `Taken` (from a real `date` run), `Evidence`,
   `Evidence-SHA256`. **`Outcome` is NOT drafted** — it is decision 2, the
   producer's judgment, keyed at Step 19; drafting it here would write the
   outcome of an open gate as settled fact.

Nothing in the register moves: the condition gains no field, no link and no
edit — the binding is inbound, from the record to the condition (*"the
record binds itself to the exact predeclared condition; the condition does
not reach forward into history"*). Commit the snapshot
(`Piece: requirements-success-measurement/18`).

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && ev=$(ls docs/gates/*-stage-route-consistency-acceptance-evidence.* 2>/dev/null | head -1) && echo "evidence: ${ev:-MISSING}" && test -n "$ev" && test -s "$ev" && python3 -c "import hashlib,sys; print('sha256', hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$ev" && python3 tools/gates/gate.py audit
```

Expected: the snapshot's path (under a producer-named home, substitute that
path — the check is existence, non-emptiness, and a recomputable digest), a
64-hex `sha256` line matching the drafted entry's `Evidence-SHA256`, then
`audit: clean`.

### Step 19 — the two decisions at the pilot's acceptance gate

[keep]

**What.** The producer, at the pilot's acceptance gate. Two decisions, in
order, never collapsed into one — the machine's, then the producer's:

1. **Is a QUALIFYING observed-result entry recordable?** The machine's half
   (the Step 4 ruling's structure list, D6): Step 18's six lines will face
   the eight checks the moment the record lands — the `MSC` exists, the
   fingerprint recomputes against the keyed condition, the evidence file
   resolves, `Evidence-SHA256` recomputes, value and unit present, method a
   `TST`, date real, outcome legal. If any fails — evidence missing, digest
   broken, fingerprint diverged — the condition is **`NOT ASSESSABLE`**:
   never a passed row, never grounds for authoring a target after the build
   (the `gate-visuals` precedent this item exists to prevent). **Write NO
   acceptance record at all on this path**: an acceptance-named record with
   a non-empty `## Release condition` is exactly what derives the pilot's
   terminal (`acceptance_record`, `kit.py:892`), so a record would close
   the pilot mechanically while the demonstration has failed — and a record
   carrying a non-qualifying entry turns the audit red (AU11) besides. The
   verdict goes in the sitting's notes; the work returns to Step 18, per
   the preamble.
2. **Does the reading satisfy the target frozen at `KEYED`?** First prove
   the freeze held — rerun Step 15's verify one-liner: `final True` means
   the target the reading is compared against is the target that was keyed.
   Then the comparison, per Step 4's ruling: **producer-performed** — the
   frozen Target and the reading side by side, in their own words; the
   machine never recomputes the semantic comparison in this slice (the
   return condition stands recorded in the design). Satisfied → `PROVEN`.
   Missed → **`NOT MET` — a real, reportable outcome**, and the target does
   not move to meet the reading.

Then the record, written once, complete: the pilot's acceptance record
(`docs/gates/<date>-stage-route-consistency-acceptance.md` — front matter
`route: new` / `stage: ready-to-release`, `**Clock:**` from a real `date`
run, non-empty `## Release condition`, prose saying "accepted as ready for
release", never "done") carries a section `## The success condition,
evaluated`: the condition ID, the frozen Target quoted, the reading quoted
with its date and commit, the two decisions in order — and the COMPLETE
seven-line observed-result entry, D6's exact shape: Step 18's six lines plus
the producer's keyed `Outcome:` line (fenced or bare; the parser reads
both). On `NOT MET`, whether the pilot itself re-loops or is accepted with
the miss recorded is the producer's key on the PILOT — this item's
demonstration is complete either way: the capability measured, compared, and
said what it found. Commit (`Piece: requirements-success-measurement/19`),
progress render, ONE push — the pilot reaches the terminal.

**Verify:**

```
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 - <<'EOF'
import sys; sys.path.insert(0, 'tools/gates'); import kit
res = kit.observed_results('.')
q = res['entries'].get('MSC-001', [])
print('qualifying entries', len(q))
print('outcome', q[0]['fields']['Outcome'] if q else 'NOT ASSESSABLE')
EOF
python3 tools/gates/gate.py route stage-route-consistency && python3 tools/gates/gate.py audit
```

Expected: `qualifying entries 1`, then `outcome PROVEN` or `outcome NOT MET`
— the PARSER, not a grep, is what reads the record here, so this passing IS
decision 1 confirmed by machine (an `outcome NOT ASSESSABLE` line means the
record should not exist — see decision 1's failure path); the route verdict
`enters at: ready-to-release`; `audit: clean` — AU11 now rechecks all eight
conditions on every push, permanently.

### Step 20 — full suite, render, and the boxes

[delegate, model: sonnet, effort: low]

**What.** Close the contract: confirm every step's box in `## Pieces` above
is checked (each was ticked as its step verified — tick any verified
straggler, never an unverified one), run the full local CI surface, refresh
the render if stale, commit (`Piece: requirements-success-measurement/20`)
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

Expected: every suite line clean (`selftest` at the Step 10 count — 63 —
plus the pilot's cases, `audit: clean`, `release: clean`, progress selftest
pass, `render current`, matrix selftest and audit clean, `stage schema:
clean (…)`, `fidelity: clean` — the full CI surface of
`.github/workflows/gate.yml`), then `unchecked: 0`. The box count is a
ZERO-expected check, so it is taken with `awk` (which exits 0 whether it
counts zero or fifty) and asserted with `test` — the preamble's exit-safe
rule applied to this file's own boxes.
