# Requirements catalog — the schema

What a requirement *is* in this project: which fields exist, which are
required, what a state means and what it owes, which links are legal, and which
fields each surface shows.

**Declared separately from the register on purpose.** Measured 2026-08-08:
StrictDoc's default `REQUIREMENT` node has eight fields and **none of them is
mandatory** — required-ness is a per-project declaration, not a vendor opinion,
and it lives in a grammar block that can be shared across documents. This file
is that grammar. Kerd ships it as a default; a consuming project copies it and
may extend it.

> **On this directory's name.** `docs/requirements/` was the output path of
> `capturerequirements`, the skill cut at v0.73.0 — cut partly *because* that
> path produced **dated snapshots**, which violated the date-split rule and
> re-created measured scatter. The standing rule is that dead solutions stay
> dead unless a named return condition fires. **The named condition: the defect
> that caused the cut is not reproduced here.** These are living files,
> overwritten in place, with no date in any filename. The path returns; the
> shape that killed it does not.

## Fields

| Field | Required | Type | Notes |
|---|---|---|---|
| ID | yes | `^[A-Z]{2,4}-\d{3}$` | The code must be one of the twenty below. Widened from `{3,4}`, which rejected `UX-001` — a shipped code and the frame's own worked example. |
| Category | yes | one of the twenty codes | Its disposition in `categories.md` must be `applies`. |
| State | yes | one of the five below | |
| Statement | yes | free text, may be multi-line | The producer's words, compressed but never paraphrased into the model's vocabulary. |
| Source | yes | free text | Where it came from, so the full wording stays reachable. |
| Approved | when `final` | `sha256:<12 hex>` | The statement as it read when keyed. See **State obligations**. |
| Title | no | free text | Currently the heading. Earns its own field when a statement outgrows one line. |

**Deferred, each with a return condition** — Priority (returns when a release
object exists to consume it), Owner (returns on the first register with two
writers), Acceptance Criteria and Verification Method (the forward trace, slice
2), Project Type (returns with the project-type work), Subtype (appears exactly
once in the whole repo with no legal set — must not be built until one exists).

## The twenty category codes

`BUS` `STA` `USR` `PRD` `FUN` `NFR` `UX` `TECH` `INT` `DATA` `SEC` `PRIV`
`CMP` `ANA` `OPS` `SUP` `TST` `REL` `DOC` `POST`

Supplied by the producer 2026-08-07 as a discipline-based taxonomy — *which
specialism owns the requirement* — which is why it travels to any project
rather than being fitted to one. Full definitions and the sub-types each covers
are in `docs/product/requirements-traceability.md`. A project may extend the
set; it never has to invent one.

`Category` maps to **`ReqIF.Category`**, a reserved enumeration in the ReqIF 1.2
interchange standard, so the taxonomy is portable by construction rather than
by translation.

## States, and what each one owes

A state is not a label. Measured 2026-08-08: Sphinx-Needs attaches obligations
to a state — *"a `fun` in status `final` must be `verified_by` at least one
`tst`"* was written and produced a real refusal. Kerd's five states owed
nothing, while the producer's own `G0`–`G8` gates state those obligations in
prose. This table is their machine form.

| State | Means | Owes |
|---|---|---|
| `proposed` | captured, not yet qualified — the holding state | nothing; this is the free-capture landing zone |
| `qualified` | judged durable, wording agreed, not yet signed | a `Source` |
| `final` | the producer's key is on it | a `Source` **and** an `Approved` hash matching the statement |
| `superseded` | replaced, and the replacement is named | a `superseded-by` link to a requirement that exists |
| `dropped` | deliberately abandoned | a reason in `Source` |

**The `final` obligation is the one that closes a real hole.** Doorstop's
`reviewed` is a sha256 fingerprint rather than a label; editing one line of a
requirement's text immediately reported *"unreviewed changes"*. Kerd's `final`
survived any later edit, so an approval could not be told from one whose
subject had changed underneath it. **The audit REFUSES on divergence and never
rewrites the state** — a red check is a question the producer answers; a silent
downgrade is a decision made for them.

## Link roles

A link is a typed object, never a column. ReqIF's `SpecRelation` makes `TYPE`,
`SOURCE` and `TARGET` all mandatory — a relation cannot be untyped. StrictDoc
requires a role to be **registered in the grammar** (`ROLE: Refines` was refused
until declared) and its `REVERSE_ROLE` gives both reading directions from one
declaration.

| Role | Reverse | Used for |
|---|---|---|
| `depends-on` | `required-by` | `TECH-006` — one requirement depends on another |
| `supersedes` | `superseded-by` | supersession as a typed edge, not a prose convention |
| `refines` | `refined-by` | a functional requirement under a product one |
| `satisfied-by` | `satisfies` | requirement → the contract piece that builds it *(slice 2)* |
| `verified-by` | `verifies` | requirement → the test that proves it *(slice 2)* |

A link naming an ID that does not exist is refused. An **origin** requirement —
`BUS`, `STA`, `USR` — may legitimately have no parent; without that allowance
every such row reads as a broken trace.

## Views

Named field subsets, stored as data. StrictDoc's `VISIBLE_FIELDS` idea, adopted
because it dissolves an argument this design had been having with itself: the
producer's fifteen-field row against `UX-006`'s *"avoid reading lots of text"*
was never fifteen fields against seven. It was **one model against one
rendering**, and shrinking the model was the wrong half to change.

| View | Shows | Surface |
|---|---|---|
| `card` | ID · Category · State · Statement | the board |
| `table` | + Source | a scan of the file |
| `full` | every declared field and every link | one record open |
| `release` | ID · Title · State · release | release planning *(needs the release artifact, which does not exist)* |
