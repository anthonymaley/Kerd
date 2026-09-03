---
route: new
stage: framed
---

# A risk's severity and its treatment are two facts, not one field

## Value

Tony's ruling, in his words (2026-09-03 morning, resolving the conflict opened
2026-09-02 at `gate-reachability`'s gate — option 2 of the two he had named):

> - Severity: how damaging the risk would be if it happened.
> - Treatment: what we are doing about it and whether that treatment is proven.
>
> For gate-reachability, that means:
>
> - Severity: fatal—the check could confidently judge the wrong project.
> - Treatment: permanent countermeasure—always pass the target repository
>   explicitly and verify both directions with fixtures.
>
> This avoids redefining "fatal" into something conditional or vague. The
> tradeoff is a real schema migration across 22 work records and the checker,
> so gate-reachability should remain blocked while that change is designed and
> implemented as its own work item.

**The defect this fixes, plainly.** A risk ledger row has one `State` field,
and its five legal values mix two different kinds of fact: `fatal` says *how
bad* (a severity), while `countermeasure - permanent | temporary` and
`accepted | accepted unknown` say *what we are doing about it* (a treatment).
So a risk that is genuinely fatal **and** genuinely treated cannot be stated
truthfully — whichever value the field carries is a lie about the other fact.
`gate-reachability`'s killer row is exactly that risk, marked `fatal` on the
producer's 2026-09-02 refusal to let a cheap fix soften the classification, and
its item sits correctly refused until this one ships. Same defect class as
`project type` before its 2026-08-23 split into three axes: one field doing
two jobs.

**Why the other option died.** Redefining `fatal` as *uncountermeasurable loss
of the declared value* would have been free of migration — and would make
severity depend on how good the treatment is, which is the exact dependence
the 2026-09-02 refusal forbade: *"the countermeasure being cheap and permanent
affects treatment, not impact classification."*

**Winning, in units:**

- Every ledger row can state both facts, and the checker refuses a row that is
  missing either.
- `gate-reachability`'s killer row reads Severity: fatal · Treatment: permanent
  countermeasure, with neither field lying about the other.
- No half-migrated moment: at the commit where the checker's demand changes,
  every record carrying a ledger parses clean — the board never goes red from
  the migration itself.

**The producer's boundaries at the frame, verbatim:** *"Name both risks, with
the half-migrated state as killer because it could disable every existing work
item simultaneously. Keep hollow treatment distinct: a treatment is not proven
merely because its field is populated."* And the task boundary: *"No checker,
migration, or skill changes in this task"* — those are this item's later rungs.

**The ledger below was qualified at viability, 2026-09-03** — both rows sized
on measured evidence, in today's five-state vocabulary: the split this item
proposes does not exist yet and is not pretended to. States and the scope below
keyed by the producer the same sitting.

## Grounding

- tools/gates/kit.py — `LEGAL_STATES` (line 70), the five-value set where `fatal` sits beside the four treatments; `parse_ledger`'s State legality check and FATAL refusal (lines 486–489), the machine half this item restructures.
- tools/gates/README.md — the viability and scope gate rows (lines 43–44), the declared contract for the ledger's columns and the killer-risk floor.
- docs/product/gate-reachability.md — killer row 1, the risk that is both fatal and treated: the case that exposed the defect and the item this one unblocks by shipping.
- CONTEXT.md — the 2026-09-02 open question this ruling resolves; the 2026-08-23 `project type` split, the same defect class ruled once already; the 2026-08-31 `unqualified` ruling this frame's ledger discipline follows.
- TODO.md — the Backlog row that carried the conflict, with its sizing note: 22 work records carry ledgers, so a column change is a migration.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| A half-migrated vocabulary — the checker demanding the new shape while any record still carries the old, or the reverse — makes every work item's ledger fail to parse at once, disabling the whole board in a single commit | yes | Every item's route degrades at once: the parser refuses in both directions (exact-header match), the board cannot derive truthfully, CI goes red at the next push, and nothing advances until the tree converges. No data loss — the parsers only read | High without the countermeasure: "checker first, records later" produces a mixed tree by construction. Low with it | Measured 2026-09-03: 21 records carry `## Risk ledger`; exact-header refusal at `kit.py:457-459`; `parse_ledger` consumed at `:740`/`:795` inside the rung checks the board derives from (`:965`); CI runs the gates on every push | countermeasure - permanent | The producer's atomic-migration rule, verbatim: checker change, all existing ledger migrations, and tests land together so no committed tree contains mixed schemas. Enforced by fixtures landing in the same commit: old-only refused, mixed refused, fully-migrated accepted | Fires if any later vocabulary change is proposed outside a single commit carrying its paired record migration — the same class recurring |
| Hollow treatment — the new Treatment field reads as protection merely because it is populated, so an unproven fix wears the same clothes as a proven one; a treatment is not proven merely because its field is populated | no | The Treatment half of the declared value silently defeated for any affected row; worst case, a fatal-severity risk advances as treated. A false green, no data loss | High without a machine check — measured, not supposed: the 2026-09-02 classification incident and the hollow-waiving family are this repo's own record of the cheap-state pull | Today's machine checks content only for non-emptiness (`kit.py:492`) — it cannot distinguish a proven treatment from an asserted one; the 2026-09-02 incident is recorded in CONTEXT.md | countermeasure - temporary | The design must make "proven" checkable; the producer's required fixture binds it — a populated-but-unproven treatment is refused. Temporary because that machinery is unbuilt; the fixture obligation is carried in `## Scope` below | Fires at this item's design gate: a design shipping without the populated-but-unproven refusal fixture re-opens this row and the state cannot stand |

## Scope

The smallest valuable increment: the two-axis ledger vocabulary, shipped with
its migration in one commit.

In scope:

- The checker — `LEDGER_COLUMNS`, the legal-value sets, `parse_ledger` and its
  refusal messages — restructured so a row carries **Severity** (how damaging
  the risk would be if it happened) and **Treatment** (what we are doing about
  it, and whether that treatment is proven) as separate facts. Exact column
  names, legal values per axis, and each refusal's wording are design-rung
  decisions: scope commits to the split, not the spelling.
- **Atomic migration, the producer's definition verbatim:** checker change, all
  existing ledger migrations, and tests land together so no committed tree
  contains mixed schemas. Every work record carrying `## Risk ledger`
  (21 measured 2026-09-03; re-measured at migration time) migrates in that
  commit.
- **The migration boundary, the producer's ruling at the scope key:**

  > Existing rows are migrated mechanically only where today's data determines
  > both new fields without judgment. Every ambiguous Severity or Treatment
  > value requires explicit producer review; the migration must not infer it
  > merely to complete the schema.

- **Tests, all five required, the producer's list verbatim:** old-only schema
  refused · mixed schema refused · fully migrated schema accepted · fatal
  severity with permanent treatment representable · populated-but-unproven
  treatment refused.
- The prose surfaces stating today's contract sweep with the change:
  `tools/gates/README.md` (the legal-values rows) and
  `skills/interrogate/SKILL.md` (the five states and the eight-column
  template) — a skill change, so the full release checklist rides.
- Release metadata (version bump, README What's New).
- First action after this ships: `gate-reachability`'s killer row re-qualifies
  under the new shape, in its own item.

Deliberately excluded, with reasons:

- No new gates or rungs — the vocabulary changes, the ladder does not.
- No waiver or legacy-closure record changes — they carry no ledgers.
- Dated records and session logs keep their vocabulary forever — aliases read
  old records; only living work records migrate.
- No renderer or board changes beyond what re-derives automatically.

Named for design, not settled here: what Severity an existing non-fatal row
receives when today's vocabulary never recorded one — resolvable only under
the migration boundary above: deterministic from existing evidence, or
explicitly producer-reviewed.

Rigor level: mvp
