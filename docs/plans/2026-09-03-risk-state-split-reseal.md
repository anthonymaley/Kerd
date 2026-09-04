# Reseal record — risk-state-split, migration-map view, 2026-09-03

**Clock:** 2026-09-03 23:08 EDT

`docs/design/risk-state-split/migration-map.html`
**fp:aef214c7ae05 → fp:3b7b1c17243a**, on the producer's key.

## What was superseded, and by what

The view, and two sentences of `docs/design/risk-state-split.md`, predicted
that **`gate-reachability` unblocks at the migration commit**. That
prediction was **true when it was sealed** and was superseded hours later
by the producer's own severity key on that item's row 2 — a ruling that
postdates the design gate.

His row-2 ruling, verbatim (2026-09-03, at the severity review):

> gate-reachability row 2: fatal. If the canonical invocation cannot work
> without a manually supplied path, the acceptance criterion is inverted.
> Its narrow measurement must resolve this before the item advances.

Keyed `fatal` against an `accepted unknown` treatment, that row refuses on
the very matrix this design ships — a fatal risk cannot be accepted by name
(the 2026-08-03 rule) — and its `Treatment evidence` is empty. So the item
does not advance, exactly as he intended.

## The corrected truth, as it now reads on every living surface

- `gate-reachability` **remains at viability**.
- Row 1 parses cleanly — `fatal` severity, `countermeasure - permanent`
  treatment, planned evidence — which is the two-axis mechanism this item
  exists to deliver, working on real data.
- Row 2 **refuses independently**: fatal severity with an
  `accepted unknown` treatment, and an empty `Treatment evidence` cell.
- **The migration clarifies the blocker; it does not unblock the item.**

## What was corrected, and what was deliberately not

Corrected — living surfaces, which may not stay factually false:

- `docs/design/risk-state-split/migration-map.html` — the outcome panel and
  the `<desc>`; downgraded, corrected, re-rendered, reviewed by the
  producer, resealed **from final content** in that order (the 2026-08-25
  procedure; the seal is written on the key, never before it — 2026-08-28).
- `docs/design/risk-state-split.md` — both sentences struck in place with
  the original text preserved inside the strike and the replacement named
  (the Law 4 supersession rule).
- `docs/plans/2026-09-03-risk-state-split-spec.md` — Step 10's expectation.
  Its assertion of **zero** `FATAL risk` lines was **removed rather than
  re-expected**: one such line is now the correct output. Declared in the
  spec as the conductor's correction, the composer being rate-limited.

Not corrected, deliberately:

- `docs/gates/2026-09-03-risk-state-split-design.md` — the dated GO record
  **stands untouched**. It records what was believed at the design gate on
  the date it was written, and a dated record is never rewritten (the
  2026-08-25 living-versus-dated rule). This record is where the
  supersession lives instead.

## The class, recorded because it recurs

A sealed drawing that was **accurate when sealed** and later invalidated by
a producer ruling — the third distinct failure mode named on 2026-09-01,
when `condition-anatomy` met the same fate. The rule that governs it: a
ruling that changes a mechanism invalidates every view describing it, not
only the view that was wrong. Here the mechanism did not change — only a
prediction about one item's board position did, and one view carried it.

**Home note:** this record lives in `docs/plans/` rather than
`docs/gates/`, because AU3 refuses any filename under `docs/gates/` that is
not a dated, rung-suffixed gate record — and a reseal is not a rung.
