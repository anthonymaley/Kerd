# Score step D1 — survey the docs for the four gaps

Author: Conductor (Claude), 2026-09-14 23:12 EDT. Defects return to Conductor.
Player: native subagent, Sonnet 5 requested. Read-only; return a report, write nothing.

## Intended result

A complete, cited inventory of every clause in Kerd's skill docs that governs or
would conflict with each of the four gaps in [work.md](work.md), so Conductor can
design the correction without missing a passage (0.126.0's survey found 9 conflicting
and 10 wording-update clauses the same way).

## Terrain (project root `/Users/anthonymaley/development/product/Kerd`)

- `skills/conductor/SKILL.md` and every file under `skills/conductor/references/`
  (including `guidance/model-choice.md`; skip `guidance/archive/`).
- `skills/agent/SKILL.md` and `skills/agent/references/*.md`.
- `skills/switch/SKILL.md` and `skills/switch/references/in-out.md` (TEAM display,
  Agent pairing restore, arrival), `skills/switch/references/to-roll.md` only for
  pairing or review clauses.
- `README.md` sections for Conductor, Agent and Switch.

## What to report, per gap

For each gap (1 review cadence and planning; 2 controller model/effort fit display;
3 player model suitability and model changes; 4 returned-edit diff reads including
new/untracked files), list every relevant clause as:

`file:line-range — short quote (≤25 words) — classification — note`

Classification is one of:
- **governs**: states the current rule;
- **conflicts**: would contradict the likely correction (say which correction);
- **update**: wording that must change or gain a clause for consistency;
- **display**: presentation (grid columns, startup view, TEAM, examples) affected.

Also report:
- every example grid or startup-view example that shows model/effort without a
  reason (gap 2/3), with line ranges;
- where "partner role" is explained to the person (setup questions, user guide help
  list), and any existing statement about what Agent asks at pairing;
- any clause saying verification or re-running checks can or cannot stand in for
  reading returned changes, and how untracked files are treated (or that none do).

## Boundaries

Read-only. No edits, no commands that write, no session contact. Do not propose the
design; classify and cite. If a gap has no clauses in a file, say "none" for that file.

## Success and evidence

Success: all four gaps covered across all listed files, each clause cited with a
line range. Verification by Conductor: spot-check five citations with
`sed -n '<a>,<b>p' <file>`; expected: each quote appears in that range.
