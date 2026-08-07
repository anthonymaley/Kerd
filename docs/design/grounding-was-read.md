# Grounding-was-read — declarations + the reachability audit

Living design doc. Owner: the `grounding-was-read` work item
(`docs/product/grounding-was-read.md`), release slice 1. Parent:
`docs/design/entry-gates.md` (the audit this piece extends). Routed here
by `gate.py route` — enters at design on the frame's own artifacts.

## What it does

Makes a work item's background reading a **declared, machine-checkable
artifact**. A product doc may carry a `## Grounding` section — the
artifacts that must be read before this work produces anything — and the
repo-wide audit gains a fifth rule (AU5): every declared reference must
resolve on disk. A reference that stops resolving (the artifact moved,
was renamed, or never existed) turns the push red, naming the doc and
the broken reference. **"Lost" becomes a checkable state.**

Slice 1 checks *resolution only* — that the declared reading list is
real. Whether the reading happened (receipts) is slice 2, carrying the
retrieval-not-comprehension claim priced in the product ledger.

## The `## Grounding` section

Optional, per work item, in `docs/product/<slug>.md`. List lines, one
reference each:

```
## Grounding

- docs/design/entry-gates.md — the audit this work extends
- tools/gates/kit.py — the harness AU5 lands in
- docs/gates/*-grounding-was-read-design.md — the GO record, once it exists
- CONTEXT.md — standing decisions bind the design
```

- **Shape:** `- <ref> — <why>`. The reference is everything before the
  first ` — ` (em-dash separator, the repo's established list idiom);
  the why is prose for the human reader and never parsed.
- **Resolution:** the reference is a path relative to the repo root.
  Glob characters are allowed; a glob resolves when it matches ≥ 1
  file. An exact path resolves when the file exists.
- **Absent section = vacuous pass.** Declaring grounding is opting in;
  the audit refuses only what was declared. (Why not required: see the
  decision below.)

## AU5 — the reachability audit rule

Extends `kit.audit` (AU1–AU4 precedent), swept over every
`docs/product/*.md`:

1. Find the `## Grounding` section (exact heading, `find_section`).
   Absent → no problems for that file.
2. For each list line matching `- `: split on the first ` — `. No
   separator → problem:
   `docs/product/<S>.md — grounding line malformed (want '- <ref> — <why>'): <line>`
3. Resolve the reference against the repo root. No match → problem:
   `docs/product/<S>.md — grounding reference does not resolve: <ref>`

Runs wherever audit already runs — `gate.py audit`, CI step two. **CI
gains no step**; reachability rides the existing refusal
surface, and rot is caught at the push that causes it.

## The decision — where declarations live

The frame named the granularity question; grounding it against the
built kit settled it. The honest finding first: **A8's sketched landing
site does not exist** — `check_rung` is inline code per rung, there is
no `kit.GATES` data table to hold a `grounding` slot. Any static
per-rung home would have to be *invented*, not filled.

Marks (light tier — the options are not close, so no scored matrix;
`docs/design/design-instrument.md`: marks always, scores when close):

| Criterion | static per-rung table | per-item `## Grounding` | hybrid now |
|---|---|---|---|
| Can name what THIS work touches (M) | × | ○ | ○ |
| Adds checks beyond existing gate inputs (M) | × — duplicates existence checks already enforced | ○ | △ |
| No data structure invented ahead of its need | × | ○ | × |
| Authoring cost per work item | ○ none | △ a few lines; rot caught by AU5 itself | △ |

A static table dies on both M-criteria: the artifacts worth declaring
(the 6-July class — related living docs, standing decisions) vary per
work item, and the per-rung constants it *could* hold are already the
gate's existence-checked inputs. **Per-item wins.** The hybrid's static
floor is deferred to slice 2, where rung-scoped receipts may want it —
an extension point, not a debt.

**Why optional rather than required:** retrofitting twelve product docs
with invented reading lists would manufacture exactly the hollow
declarations the frame's killer risk names. Grounding grows organically
per new work; the audit enforces only honesty about what was declared.
Named residual (accepted, per the frame): an absent section means no
reachability guarantee for that work item.

## Testing strategy

Fixture cases extend `kit.selftest()` (temp-tree pattern, currently 14):

1. **Resolving grounding** — exact path + glob reference, both present
   → audit clean.
2. **Broken reference** — a declared path absent from the tree → audit
   names the doc and the reference verbatim.
3. **Malformed line** — a `- ` line with no ` — ` separator → audit
   names the line.
4. **Absent section** — product doc without `## Grounding` → vacuous
   pass (asserts the opt-in semantics).

At build, the refusal is demonstrated both ways on the real tree (the
0.70.0 pattern): a planted broken reference exits 1; removal returns
clean. **Dogfood:** `docs/product/grounding-was-read.md` gains its own
`## Grounding` section in the build — the feature's first citizen is
its own product doc.

## Named answers — the stage-1 measurement

| Measurement (product doc, Value) | Target | Named answer |
|---|---|---|
| Broken grounding references at a pushed tip | 0 | AU5 runs inside `gate.py audit` — CI step two — at every pushed tip; a reference that stops resolving goes red within the run, naming the doc and the reference. Measured by: the both-ways demonstration at ship + fixture 2's verbatim message assertion. |

## Out of scope, named

- **Read-receipts at gates** — slice 2, carrying the hollow-stamping
  ledger row and the retrieval-not-comprehension claim; its receipt
  shape rides the `mark_reviewed` precedent.
- **Rung-scoped grounding and any static per-rung floor** — slice 2's
  extension point, taken only if receipts need it.
- **An orphan report** (artifacts no grounding names — the inverse
  view) — unframed; reachability's slice-1 claim is about declared
  references resolving, not repo-wide coverage.
- **Any comprehension proof** — never, per the product ledger's third
  row.
