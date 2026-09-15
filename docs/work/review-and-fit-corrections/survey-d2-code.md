# Score step D2 — survey pairing storage and display in code

Author: Conductor (Claude), 2026-09-14 23:12 EDT. Defects return to Conductor.
Player: native subagent, Sonnet 5 requested. Read-only; return a report, write nothing.

## Intended result

A precise map of how Agent stores, validates, carries forward, reads and displays a
partner's `partner_role`, so Conductor can design a sibling review-cadence field
(set at pairing, changeable, carried across session succession, readable by
Conductor, shown where useful) without breaking existing behaviour or tests.

## Terrain (project root `/Users/anthonymaley/development/product/Kerd`)

- `skills/agent/scripts/agent.py` (1,233 lines): `pair`, `start`, `adopt`/succession
  (around lines 600–620), `arrival` (around 650–760), `sessions`, argparse setup.
- `skills/agent/scripts/tests/test_agent.py`, `test_arrival.py`.
- `skills/switch/scripts/where_we_are.py` (TEAM rendering) and its tests under
  `skills/switch/scripts/tests/` if present.
- `tests/hooks_test.sh` only if it touches Agent bindings.
- `tools/gates/gate.py` only for checks that would fail on a new binding field or
  new skill text (search for `partner`).

## What to report

1. Binding schema: every key written to `kerd-agent/partners/<alias>.json`, where
   each is written (function, line), and validation rules for `partner_role`.
2. CLI: argparse definitions for `pair` and `start` (flags, help text, lines), and
   how `--partner-role` flows to storage.
3. Carry-forward: every place a binding is replaced or copied (succession, adopt,
   recovery, replacement) and which keys survive; cite lines. Note any allowlist of
   copied keys a new field would need to join.
4. Readers: every reader of `partner_role` (arrival team, sessions listing, notices),
   and what each outputs.
5. Display: how TEAM is rendered from the team array in `where_we_are.py`, and
   whether extra keys are ignored safely.
6. Tests: tests that assert the binding shape, role storage, carry-forward or TEAM
   display, with names and lines, and whether they would fail if a new optional key
   appeared.
7. Any existing place a person-facing question is asked by Agent code (vs. by the
   model following SKILL.md), to tell whether a picker would be model-driven.

## Boundaries

Read-only: no edits, no test runs that write, no session contact, no `pair`/`ask`
invocations. Do not design the field; map what exists. Cite `file:line` throughout.

## Success and evidence

Success: all seven items answered with citations or "none found" plus the search.
Verification by Conductor: spot-check four citations with `sed -n`; expected match.
