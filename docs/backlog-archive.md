# Backlog archive

Backlog rows closed at Switch Out, each with its verdict, the evidence and the date; and
position paragraphs moved out of `CONTEXT.md` when they stopped being current. Nothing here
is edited after it lands. Started 2026-09-11 at the first run of the lean-start step (v0.111.0).

## Closed 2026-09-11

**Verdict: dead — the step it describes no longer exists.** Conductor has had no close-out
since 0.107.0 replaced it (`grep -rniE "close-out|closeout" skills/conductor` is empty; the
2026-09-11 Fable review, finding 1, and README's rewritten "How They Fit Together").

- **Close-out double-write** — conductor step 1 writes CONTEXT/TODO, step 6's
  invoked flow overwrites both.

**Verdict: superseded — the producer took option (c) on 2026-09-11** ("switch out should
clean up todos/backlogs/docs/etc and set next session start to make switch in faster/cheaper"),
before the row's own return condition fired (CONTEXT.md was 216 KB against the 250 KB
trigger). Built as Switch Out's lean-start step in v0.111.0: ruling in the loaded file, case
in `docs/decisions.md`. The row's measurements and its named risk (a reachable record can
sit unread) stand and are the reason the reading set is measured at every Out.

- **Switch-in costs ~17% of the context window — measured, diagnosed, and
  DEFERRED by the producer 2026-09-01.** *"Do nothing for now"* — this repo is
  complex, mid-planning, and losing context is the more expensive error. The
  measurement is recorded here so no later session re-derives it, and **the row
  as first filed blamed the wrong lever (pruning); that framing is superseded by
  what follows.**
  **Where the cost is:** the read set is 250KB — `CONTEXT.md` 177KB (70.7%, so
  **12 of the 17 points**) · the day's session log 37KB (2.5 pts) · `TODO.md`
  36KB (2.5 pts). `## Key Decisions` alone is **97.9%** of CONTEXT.md; every
  other section totals 3.8KB.
  **Growth is two multipliers, and pruning only reaches one.** Bullets went 17
  (2026-07-06) -> 48 -> 74 -> 101 -> **131** today, while the MEAN bullet went
  232B -> 676 -> 919 -> 1,239 -> **1,352B**. Count 7.7x, size 5.8x.
  **The decisive measurement: old bullets do not accrete.** Of the 48 standing on
  2026-08-04, **44 survive and grew 1.01x** (29,376B -> 29,593B) with 4 removed;
  the **87 added since average 1,696B — 2.5x the survivors' 672B — and are 147KB,
  83% of the whole section.** So deleting every pre-August decision recovers 29KB
  (16%) and touches none of the growth. **Pruning is aimed at the wrong
  variable**, which is why two licensed prune events both ended with the file
  bigger.
  **Rate: linear, not compounding.** ~30 new bullets per window, per-window mean
  1,297B -> 2,117B -> 1,695B (inflated once in mid-August, then plateaued). ~5.3
  KB/day, projecting ~250KB in two weeks (~22% of a pickup) and ~320KB in four
  (~26%).
  **Two options were priced and neither taken.** (a) A size budget per decision —
  **refused on the producer's own reasoning**, the argument that got to a ruling
  is the thing the boundary exists to preserve. (b) Tiered loading, his idea:
  deferring the whole Backlog buys **2.2 pts**, and rank-and-read-High-only buys
  **0.5 pts** because High is already 76% of the Backlog — both aimed at the
  2.5-point file. (c) Named but untested: split CONTEXT.md the way 2026-07-03
  split state/work/history, keeping the **ruling** in the loaded file and moving
  the **case** to a reachable record — a full read of a smaller file rather than
  a reduced mode, which `skills/switch/SKILL.md` forbids outright. **Its risk is
  the one this repo has already paid:** `docs/design/conductor-role.md` was
  reachable by name and sat unbuilt for three days, which is why `fidelity.py`
  exists.
  **Return condition:** CONTEXT.md passes **250KB**, or a pickup passes **25%**,
  or the per-window bullet mean resumes climbing — whichever comes first. Until
  one fires, this is an accepted cost, not an open task.

## Retained position, 2026-09-03

Moved verbatim from `CONTEXT.md` `## Where We Are` on 2026-09-11; it was a position
paragraph, not a decision, and TODO.md's "Earlier launch sequence" carries the live
version of the same items.

### Previous installed-Kerd position — retained, not freshly revalidated

**2026-09-03, three sittings (08:38–09:16 · 10:40–14:03 · 14:09–23:18 EDT) —
the schema migration SHIPPED.** Kerd at **v0.106.0**; CI green at the tip
(`f098ae5`).

- **`risk-state-split` is at ACCEPTANCE** — all 14 pieces landed. The whole
  ladder walked in one sitting: design package with three sealed views and a
  GO record (`1008a43`), a 14-step work specification, and the migration
  itself as **one atomic commit** (`e15a0f0`). The ledger's `State` column is
  now **Severity** (`fatal` | `non-fatal`) + **Treatment** (the four values);
  `Evidence` renamed `Risk evidence`; **`Treatment evidence`** is new, in
  three machine-distinguished forms — empty · `planned — <what will exist> ·
  <expected location>` · a resolving citation. 21 records, 84 rows migrated;
  selftest 51 → **57**. Next: the evidence-backed acceptance record.
- **`gate-reachability` still REFUSES at viability, on row 2** — and that is
  the intended outcome, not a regression. Row 1 parses clean (fatal +
  permanent + planned evidence): the new mechanism working on real data. Row 2
  is fatal with an `accepted unknown` treatment and empty evidence, so it
  refuses independently. **The migration clarified the blocker; it did not
  unblock the item.** Its narrow `${CLAUDE_PLUGIN_ROOT}` measurement must
  resolve before it advances.
- **Four fatal/accepted-family risks are newly VISIBLE and refusing** —
  `funnel-driver` row 4 · `gate-reachability` row 2 · `gate-visuals` row 1 ·
  `switch-fidelity` row 4. Each was carried as *accepted* while being fatal,
  a contradiction the one-column schema could not express. Remediation
  belongs to each owning item, never to the migration (the producer's ruling).
- **The migration-map view was RESEALED** (`fp:aef214c7ae05` →
  `fp:3b7b1c17243a`) after the producer's row-2 key superseded the
  design-time prediction that gate-reachability would unblock. Downgrade →
  correct → re-render → his eye → reseal, in that order; the dated GO record
  stands untouched and the supersession lives in
  `docs/plans/2026-09-03-risk-state-split-reseal.md`.
- **The launch plan is ON DISK** (`8b08ad1`) — five outcomes, the 8-step
  critical path, the binding rules. **Launch: 0 of 5 outcomes.**
- **v0.105.0 (morning): the Status Report talk format** — status speaks Work
  item · Stage · Issue · Resolution path, one final question.
