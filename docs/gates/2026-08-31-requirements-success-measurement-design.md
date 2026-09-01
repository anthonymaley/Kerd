---
route: new
stage: designed
---

# Design GO — requirements-success-measurement, 2026-08-31

**Clock:** 2026-08-31 23:30 EDT

Design approved — the producer's key, 2026-08-31, three explicit per-concern
approvals given across one combined review. Package:
`docs/design/requirements-success-measurement.md` with three drawings beside it,
all sealed at this gate from final content:

| Concern | Viewpoint | View | Fingerprint |
|---|---|---|---|
| what the measurable condition contains and what artifact carries it | `nested` | `condition-anatomy.html` | `fp:fefa90380fe3` |
| how that condition travels from declaration to demonstrated proof | `state` | `condition-lifecycle.html` | `fp:0a91dbcac981` |
| where assurance comes from at each rung, and where it does not | `flowchart` | `assurance-boundary.html` | `fp:c9b8d06ebfb6` |

`gate.py check requirements-success-measurement design` → **PASS, 11 inputs on
disk.** Rigor level `mvp`, declared at scope.

## The gate passed on real checks because concerns were declared first

**The producer's entry condition, given before any view was drafted:** *declare
at least one `concerns:` entry BEFORE relying on the design gate.* Without one,
`parse_concerns` returns `None`, zero views are counted, and `design pass` is
evidence of nothing — the standing "the design gate can check nothing" defect.

Declaring three concerns **demoted the item from `design` to `scope`** on the
board with three named unmet needs. That demotion is the entry condition working.
This record is therefore the first design GO in the repo issued against a gate
that had something real to refuse.

## What the design settles

1. **A requirement and its measurable success condition are two artifacts,
   joined by typed edges.** The catalog held **two incompatible answers to one
   question under one `slice 2` return condition** — deferred `Acceptance
   Criteria`/`Verification Method` *fields* on the requirement block, and a
   `verified-by` *edge* to a separate object. Neither was ever built, which is
   why the contradiction went unnoticed. The producer ruled for the edge.
2. **Four objects.** Requirement (**gains no field**) → `measured-by` → Success
   condition `MSC-nnn` (Statement · Measure · Baseline · Target) → `verified-by`
   → Test/method `TST-nnn` (owns Method); and Success condition → `evidenced-by`
   → Observed result. **Evidence is a linked object, never a field that mutates
   inside an approved condition** — that is what keeps the predeclared target
   separable from its later proof.
3. **A new category `MSC`, not an overloaded `TST`.** `TST` answers *how will
   we test this*; a success condition answers *what observable result counts as
   success*. Reusing `TST` for its inherited machinery would buy a semantic
   contradiction. Pending a category vocabulary review.
4. **Acceptance is TWO decisions and THREE outcomes.** *Is a reading linked?* →
   no = `NOT ASSESSABLE`. Yes → *does it satisfy the target frozen at `KEYED`?*
   → yes = `PROVEN`, no = `NOT MET`. **A linked reading proves only that the
   condition was assessable, never that the target was met.** `NOT MET` is a
   real, reportable outcome: a design whose only outcomes are *proven* and
   *couldn't tell* is a design that cannot say no.
5. **The assurance boundary is drawn stark on purpose.** Fourteen lines: six
   machine-checked, two producer-agreed, six with no enforcement. **This slice
   adds no automated per-rigor floor**, and the drawing carries the risk
   ledger's sentence verbatim — *Drive does not structurally guarantee
   compliance*.

## What the producer's review caught, recorded because it is the gate's value

Four blocking findings across the combined eye, every one on a claim rather than
on the visual system:

- **A false trace claim, in a drawing already approved.** *"Edit either end and
  the other is flagged for re-look"* is wrong. Verified at `tools/gates/kit.py:1445`:
  the stamp is the **target's** hash stored on the **source**, so editing the
  target flags the source and editing the source flags nothing. **The unprotected
  direction is the dangerous one** — a requirement whose statement changes can
  leave its condition measuring words that no longer exist. Reciprocal stamping
  is now recorded as **owed**.
- **`NOT ASSESSABLE` branched out of `PROVEN`**, which is incoherent: `PROVEN`
  is *defined by* a linked result. The fork had to precede both outcomes.
- **The outcomes were two, and had to be three.** The catch that goes to the
  capability's purpose, and it exposed an omission in an already-approved view:
  nothing checks whether the reading *satisfies* the target. Added as the
  fourteenth assurance line, unenforced.
- **"`PROVEN` holds the later reading" contradicted the four-object model.**
  Corrected in prose and alt-text before sealing: *`KEYED` freezes the
  predeclared target; the `Observed result` holds the later reading; `PROVEN`
  records that the comparison satisfied the target.*

## Recorded, deliberately NOT executed

**The catalog is not edited by this session.** The supersession of its
merged-fields row belongs to the later schema implementation, struck in place
with the original preserved verbatim. **Standing rule attached by the producer:**
*if a checker mistakes struck text for a live claim, teach the checker to
distinguish retired text; do not rewrite history to satisfy a raw text scan.*
The record is authoritative and the checker adapts to it, never the reverse.

## What this GO does not cover

- **No build.** `MSC` owes a `categories.md` disposition and schema work.
- **Where the `Observed result` lives** — register category or external evidence
  artifact. A fourth object either way; the home is open.
- **Reciprocal link stamping**, owed for a symmetric suspect-link check.
- **`rigor-level` slice 2 is NOT absorbed.** It stays the return condition on
  risk row 1's `countermeasure - temporary`.
