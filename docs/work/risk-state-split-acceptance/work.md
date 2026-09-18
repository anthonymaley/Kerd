# risk-state-split: the acceptance record

## Where this stands

**Accepted, 2026-09-18 11:23 EDT** — Anthony's "y" to: *"Do you accept the
risk-rating change with the measurement exception, once the missing citation test
is added, and are the migration decisions yours?"* The record is at
`docs/gates/2026-09-03-risk-state-split-acceptance.md`, stage ready-to-release;
`docs/product/risk-state-split.md` moved from `framed` to `ready-to-release`;
T68b added to `tools/gates/kit.py` (negative control failed as it should) as
0.136.1. Awaiting Anthony's yes to commit and push.

Also found, for later: TODO's launch step 2 wording (gate-reachability refuses at
scope, not viability); `stage:` never flags a lagging stage (11 records say
`framed`); the measurement countermeasure from 2026-08-29 is unbuilt.

## Agreement

- 10:42, shape proposed with `shape.html`: Claude gathers what shipped and drafts
  the record; a blind reviewer (Codex, or a fresh Claude) checks the claims and
  findings return to Claude; Anthony gives the expert pass and the key (accept,
  exception or reject); stop with the record saved.
- Paused 10:48 for 0.136.0 (the Switch In screen), released 11:06 as `59cbd49`.
- **11:12, Anthony: "y"** to "Shall I start drafting the risk-rating change
  acceptance record?"

Boundaries: no release or version bump; no commit or push without Anthony's yes;
gate-reachability and the four fatal rows stay with their own items. The product
outcome is stated as *not assessable* if no measurement was declared before the
build; no target is written after the fact (the 2026-09-02 ruling: cold eyes and
the expert-user pass, never mechanical cleanup).

## Why

It is the first of the five launch steps in `docs/design/launch-plan.md`, and
every later step waits on it. The gate ladder (checked 2026-09-18 10:42) passes
every rung through acceptance with 16 inputs on disk; only the record is missing.
