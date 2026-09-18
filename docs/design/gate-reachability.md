# Conductor's step check, in the user's own project

Design for `gate-reachability`, launch step 2. Keyed by Anthony 2026-09-18 13:39
("yes") against the view `docs/work/gate-reachability/design.html`. Scope:
`docs/product/gate-reachability.md` `## Scope`.

## What the user gets

Conductor, working in the user's own repository, knows which step a piece of work
is on and does not move past missing groundwork silently. It reads that
project's records, never Kerd's, and the user types no path.

## Decisions

1. **When it checks.** At two moments: when Conductor picks up a piece of work
   that has a work-item record in the project, and before it starts a build on
   it. Small standalone fixes, and work with no work-item record, get no check
   and no reminder.
2. **What the user sees.** One plain line: the step the work is on and what the
   next step needs, translated from the check's own findings into the item's
   plain name, not its slug. When something is missing, Conductor offers to do
   that groundwork now.
3. **Going ahead anyway.** Always the person's call, never refused. Conductor
   writes a line into the work record: the date, the step skipped, what was
   missing and the person's words. The next pickup shows it.
4. **Never the wrong project.** The check always names the user's repository
   explicitly. If Conductor cannot establish which project it is in, it says so
   and does not check or guess (risk row 1, the killer risk).
5. **How it finds the checks.** The plugin's install path is written in
   Conductor's main instructions (`SKILL.md`), where Claude Code fills it in;
   never in a reference file or as a shell variable, where it does not resolve
   (risk row 2, measured 2026-09-18).

## Proof at loop

A fixture from a repository that is not Kerd: one item with its groundwork
present (Conductor carries on) and one with a gap (Conductor names it), neither
reading Kerd's own files. Built at
`skills/conductor/scripts/tests/test_step_check.py` (the risk rows first
planned it in `tools/gates/kit.py`; moved beside the skill it tests).

## Not decided here

Removing the Drive skill (its own release); the progress board and the
session-fidelity check (excluded at scope).
