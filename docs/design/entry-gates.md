# The entry gates — routing by construction

Living design doc. Owner: **Do we have what we need?** (cross-cutting
function 20), absorbing the dissolved *Route to the altitude* (function
16). The MVP keystone — three gaps stay unreachable without it.

## What it does

A thin gate at every rung that checks one mechanical thing — do the
declared inputs of this rung exist on disk? — and, run in series, does the
routing nobody else has to do: **work enters at the LOWEST rung whose
declared inputs all exist; missing inputs push work UP, never through.**

## The gate table — declared inputs per rung

| Gate | Requires on disk | Missing → |
|---|---|---|
| **Frame the intent** | nothing — the top of the ladder. Triage sorts NEW / PROBLEM / QUESTION (a QUESTION exits to the code, never becomes work) | — |
| **Test viability** | the framed intent with its declared VALUE (impact needs units) | frame first |
| **Slice a release** | framed, viability-tested candidates with QUALIFIED risks (pre-chewed) | back up the ladder |
| **Design the solution** | the intent document with measurements + the risk ledger | frame / qualify first |
| **Write the contract** | the GO'd design package + its gate record | design first |
| **Build a piece** | a work-order piece carrying its own check | contract first |
| **Goal gate** | every piece landed + everything declared upstream | keep building |
| **The loop (unattended)** | a cut release with its DONE condition — **and a live refusal instance**. No CI, no loop | build the refusal first |

## Mechanics

- **The check is mechanical**: files exist, front matter carries `route`
  and stage (per *Where the work is written down*), the named sections are
  present. No judgment call anywhere in the gate itself.
- **A refusal names exactly what is missing** — never "can't proceed."
- **The refusal rides the LADDER**: it is "a question the spec cannot
  answer" raised at the gate — closed by a role that can gather or adjust,
  or it waits for the human. The gate has no escalation machinery of its
  own.
- **The gate renders through the progress view** — have / need for the
  rung about to start; it never draws a view of its own.
- **Grounding is the gate's second job**: inputs arrive on their own;
  grounding is what gets skipped. The gate checks the function's declared
  grounding was READ (the reachability rule: an artifact is reachable
  because a gate makes some function read it).

  **Amended 2026-08-07:** as built this landed on the AUDIT, not the rung
  gate — AU5 (`gate.py audit`, v0.80.0) checks that a declared `## Grounding`
  reference RESOLVES; `check_rung` carries no grounding row and the
  `kit.GATES` landing site this assumed does not exist
  (`docs/design/grounding-was-read.md`). That the reading HAPPENED is
  receipts — slice 2, deliberately unqueued.

## The spike bypass

The ONE licensed way past the ladder: a **SPIKE**, declared as such up
front by the intent-holder — cheap, built to answer a kill-or-keep
question. Its output never ships: a spike that wants to become real work
re-enters through the gates with its evidence.

## Why this is the keystone — and the first refuser

The gate is the EASIEST refusal instance in the whole system: file
existence + front-matter fields + section presence are trivially CI-able.
Building it delivers the router and the refusal property's first working
instance in one piece — which is why it leads the MVP sequence.

**Amended 2026-08-07.** This paragraph used to end "until that lands, the gate
runs as convention inside the driving role (today: conductor's pre-flight
inventory, its only living instance)". That has been false since v0.69.0: the
gate landed, `tools/gates/gate.py` runs in CI on every push, and
`gate.py route <slug>` prints the exact missing-input list without asking a
human anything. Conductor's inventory is no longer the only living instance —
and as of v0.91.0 it has shed: the inventory runs `gate.py route` first and
asks the human only for what the gates cannot know (graduation row 1 of
`conductor-role.md`, gap 2 of `docs/product/funnel-driver.md`).
