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

**The ledger below is named, not qualified, and the empty cells are
deliberate.** The frame gate's floor is presence: a killer risk named, no
sizing, no evidence. Every row is refused at the scope gate until it carries
Evidence, a legal State and a countermeasure — left standing rather than filled
with a plausible disposition, per the 2026-08-31 ruling that workflow
incompleteness is not a durable risk state.

## Grounding

- tools/gates/kit.py — `LEGAL_STATES` (line 70), the five-value set where `fatal` sits beside the four treatments; `parse_ledger`'s State legality check and FATAL refusal (lines 486–489), the machine half this item restructures.
- tools/gates/README.md — the viability and scope gate rows (lines 43–44), the declared contract for the ledger's columns and the killer-risk floor.
- docs/product/gate-reachability.md — killer row 1, the risk that is both fatal and treated: the case that exposed the defect and the item this one unblocks by shipping.
- CONTEXT.md — the 2026-09-02 open question this ruling resolves; the 2026-08-23 `project type` split, the same defect class ruled once already; the 2026-08-31 `unqualified` ruling this frame's ledger discipline follows.
- TODO.md — the Backlog row that carried the conflict, with its sizing note: 22 work records carry ledgers, so a column change is a migration.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| A half-migrated vocabulary — the checker demanding the new shape while any record still carries the old, or the reverse — makes every work item's ledger fail to parse at once, disabling the whole board in a single commit | yes |  |  |  |  |  |  |
| Hollow treatment — the new Treatment field reads as protection merely because it is populated, so an unproven fix wears the same clothes as a proven one; a treatment is not proven merely because its field is populated | no |  |  |  |  |  |  |
