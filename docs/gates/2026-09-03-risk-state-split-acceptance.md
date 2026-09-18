---
route: new
stage: ready-to-release
---

# Acceptance record: risk-state-split, 2026-09-18

**THE PRODUCER'S KEY, given 2026-09-18 11:23 EDT.** Anthony answered **"y"** to
this question, asked with the proposal and its conditions immediately above it:

> Do you accept the risk-rating change with the measurement exception, once the
> missing citation test is added, and are the migration decisions yours?

That answer accepts the item with the product-measurement gap as an explicit
exception, makes the acceptance conditional on the missing fixture being added
first (it was: T68b, below), and confirms the worksheet's Severity and Treatment
keys as his. It is the first and only acceptance this record carries; the record
was drafted before the key and moved here only after it.

The filename carries the build date, 2026-09-03, as the launch plan names it;
the record was written on 2026-09-18.

**What shipped.** A risk ledger row used to carry one `State` field whose values
mixed two facts: `fatal` (how bad) and the treatments (what we do about it). The
build split it into **Severity** and **Treatment**, as one atomic commit, `e15a0f0`
(v0.106.0, 2026-09-03 23:10 EDT), followed by `6f988b2` (render refresh),
`7418657` (pieces boxed) and `f098ae5` (render refresh).

## Release condition

This record keeps three things apart, as the 2026-08-30 gate-visuals record did:
**conditions checked against declarations made before the build**, **one
condition that cannot be assessed because nothing was declared**, and **the
producer's decision**. Each claim says whether it was **observed** on
2026-09-18 or is **recorded** in a commit or log and not re-verified.

### Conformance: checked against what was promised before the build

- **Met the contract: 14 of 14 pieces present in the tree, with two
  qualifications.** Checked against files, not the checkboxes
  (`docs/plans/2026-09-03-risk-state-split-spec.md` `## Pieces`). Observed:
  - The checker carries ten columns (`tools/gates/kit.py:62`), the pre-split
    header kept for refusal (`:70`), and the acceptance proof demand (`:970–991`).
    Fixtures T64–T69 are at `:2944–3061`.
  - The progress tool's fixture ledgers use the new header, the old one zero
    times.
  - The prose surfaces use the new vocabulary: `tools/gates/README.md`,
    `skills/interrogate/SKILL.md` (`:104`, `:225`, trigger `:3`) and
    `docs/design/risk-ledger.md`.
  - The release metadata read 0.106.0 in all three places at `e15a0f0`, and the
    README carried its What's New (v0.106.0) entry and the rewritten interrogate
    section.
  - The review worksheet is committed:
    `docs/plans/2026-09-03-risk-state-split-migration-review.md`, 80 keys, none
    blank.

  **Qualification 1, piece 13 ("ONE push; CI green").** Not as written: three
  pushes, one red. The first carried `e15a0f0` with `6f988b2` and **passed**
  (run 33832272705), so the migration itself reached the remote green. The
  second, `7418657`, **failed** (run 33832297411) at `progress.py stale` because
  the render files were stale. The third, `f098ae5`, passed (run 33832310275).

  **Qualification 2, piece 11 (diff review).** A review activity; nothing in the
  files can show it happened. Recorded in the session log only.

- **Met the producer's atomic-migration rule.** *"Checker change, all existing
  ledger migrations, and tests land together so no committed tree contains
  mixed schemas."* Observed:
  - `e15a0f0` is one commit: 35 files, 12 `Piece:` trailers.
  - At `e15a0f0~1` the 21 ledger records carried the old header 21 times and the
    new one 0 times. At `e15a0f0` they carried the old header 0 times and the
    new one 21 times.
  - `git log -G` on the column list shows only its creation (`884d9c4`) and
    `e15a0f0`. No earlier commit changed the checker's demand.

- **The producer's five required tests exist and pass, one only in part.**
  `python3 tools/gates/gate.py selftest` → 57 cases passed (observed).

  | Required test, the producer's words | Fixture | Result |
  |---|---|---|
  | old-only schema refused | T64 | passes |
  | mixed schema refused | T65 | passes |
  | fully migrated schema accepted | T66 | passes |
  | fatal severity with permanent treatment representable | T67 | passes |
  | populated-but-unproven treatment refused | T68 | passes, **partly covered** |

  **T68 covers half of what the design promised for it.** The design
  (`docs/design/risk-state-split.md`, fixture 5) says a fatal row carrying
  `planned — …` **or a non-resolving citation** at acceptance is refused. T68
  tests the `planned` case only. **No fixture tests a citation that points at
  nothing.** Two further limits were declared by the design, not missed by the
  build: the check confirms that a citation resolves (a path or a commit hash),
  not that it proves the treatment (the producer's keyed decision 5); and
  Treatment evidence is optional at non-fatal rows
  (`docs/design/risk-state-split.md:211`). T69 (fatal with a temporary countermeasure and no Review trigger)
  was added by the model and is not on the producer's list.

- **The migration boundary: evidenced by the product, not by the worksheet.**
  The producer's ruling at the scope key: *"Every ambiguous Severity or
  Treatment value requires explicit producer review; the migration must not
  infer it merely to complete the schema."*
  - Observed: the worksheet has every Key cell filled (50 `non-fatal`, 29
    `fatal`, 1 `accepted`). It has a Treatment-evidence section ruled
    "2026-09-03 (option 2)", with 11 `empty` rulings plus citations.
  - Recorded, not re-verified: the commit message says "79 severities and 1
    treatment keyed by the producer record by record", and
    `kivna/sessions/2026-09-03.md:304–311` says fourteen rows were flagged
    ambiguous and ruled one by one.
  - **Not evidenced in the file:** which fourteen rows were ambiguous, and who
    typed each key. The keys carry no initials or date. Only the producer can
    confirm that the keys are his.

- **The declared value, "Winning, in units", holds.** Observed:
  - *"Every ledger row can state both facts, and the checker refuses a row
    that is missing either."* All 21 records in `docs/product` carry the
    ten-column header, 84 rows in total. T64/T65 refuse the old and mixed
    shapes.
  - *"`gate-reachability`'s killer row reads Severity: fatal · Treatment:
    permanent countermeasure, with neither field lying about the other."* Its
    row 1 reads Severity `fatal`, Treatment `countermeasure - permanent`, with
    Treatment evidence `planned — --root fixtures in both directions … built in
    gate-reachability's loop`.
  - *"No half-migrated moment."* Shown above: one commit, 21 → 21.
  - The scope's *"First action after this ships"*, gate-reachability's killer
    row re-qualifying under the new shape, was planned "in its own item". It
    happened inside `e15a0f0` instead (`docs/product/gate-reachability.md`,
    12 lines), which design decision 6 allowed.

- **Proof layers pass at HEAD, 2026-09-18.** Each was run, not assumed:
  `gate.py selftest` (57) · `gate.py audit` (clean, 1 finding about
  requirement parents, unrelated) · `gate.py release` (clean) ·
  `gate.py check risk-state-split acceptance` → PASS, 16 inputs on disk ·
  `progress.py selftest` (15 ok) · `progress.py stale` (render current).

### Not assessable: no antecedent exists

- **Product outcome: not assessable.** No measurable product outcome was
  declared before the build, so this gate cannot say whether the item achieved
  one. A search of the product record, design, design gate record, spec and
  `docs/requirements/` found no stage-1 measurement, target or baseline.
  "Winning, in units" is three pass/fail conditions, checked above as
  conformance. No target is written now: writing one two weeks after the build
  would check the build against a number chosen to fit it.

- **This is the second time, and the countermeasure for the first is unbuilt.**
  gate-visuals was accepted on 2026-08-30 with the same gap, as an exception
  bounded by a filed countermeasure, ruled 2026-08-29: *"future work must
  declare measurable outcomes upstream — or explicitly declare them
  **inapplicable with a reason** — before it can reach acceptance."* It was
  filed toward `requirements-success-measurement` (the record says "likely
  home"), which on 2026-09-18 still enters at **viability**, refused at scope
  on its own fatal row. risk-state-split was framed on 2026-09-03, after that
  ruling, and declared neither a measure nor
  its inapplicability. The exception has repeated because what was meant to
  prevent it does not exist yet.

### Found at this gate, outside this item's own surfaces

- **`stage:` does not set the rung.** `docs/product/risk-state-split.md` says
  `stage: framed` while the gate routes the item to acceptance. The route is
  derived from the files on disk (`kit.py:1056`). `stage` is checked only for
  legality and for claiming too much progress (`:1151–1160`); a stage that lags
  is never flagged. 11 records in `docs/product` say `framed`.
- **The launch plan's step 2 is imprecise in `TODO.md`.** It says
  gate-reachability is "still refusing at viability, on row 2". The item does
  stay at viability (`route` → enters at viability), but the viability check
  passes; the refusal comes at **scope** (row 2: fatal, Treatment `accepted
  unknown`, empty Treatment evidence; no Scope section). The README's viability
  row explains why: full qualification is scope's business.

### The producer's decision

- **Accepted with the measurement gap named as an exception, 2026-09-18 11:23
  EDT** (the key above). No target is authored after the build, and nothing in
  this record implies a product measurement was met.
- **Repaired before acceptance, not filed:** the missing half of fixture 5.
  **T68b** (`tools/gates/kit.py`, released in 0.136.1) refuses a fatal row whose
  Treatment evidence cites a path that does not exist at acceptance. Negative
  control: with the check changed to treat an unresolved citation as verified,
  the selftest fails on T68b; restored, 57 cases pass.
- **Key authorship confirmed** by the producer: the worksheet's 80 keys are his.
- **Accepted as written:** the three pushes where the spec said one (the
  migration commit's own push was green), and piece 11's diff review, which
  files cannot show.
- **The second measurement exception is not bounded by a built countermeasure.**
  The 2026-08-29 countermeasure is still unbuilt, so this exception carries the
  same unmet bound as the first. Recorded plainly, not resolved here.

## Cold eyes

One blind reviewer (fresh Claude, opus · high), 2026-09-18, re-derived every claim
against the tree, CI and git history. **One blocking finding**: the draft had two
pushes where there were three, missing `6f988b2`, whose green run shows the
migration reached the remote clean. **Six non-blocking**: a precedent quote not
verbatim, a countermeasure "home" stated firmer than its source, "misdescribed"
too strong for the TODO line, two design-declared limits presented as shortfalls,
the scope's first action unrecorded, and README release metadata unstated. All
seven were corrected in this draft. It confirmed every line reference, count,
commit, quote and gate outcome otherwise. Not verifiable from files: who typed
the worksheet keys.
