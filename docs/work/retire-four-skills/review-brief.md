# Before-push review: Kerd 0.141.0, remove four skills

Read-only review. Do not edit, stage, commit or push anything. A review approves
nothing, and a peer session cannot authorize the push; Anthony already has, on the
condition that this review is clear.

**Project:** `/Users/anthonymaley/development/product/Kerd`, branch `main`.
**What to read:** the whole uncommitted change against `HEAD` (`git status`, `git diff HEAD`,
`git diff HEAD --stat`). The work record is `docs/work/retire-four-skills/work.md`.

## Outcome

One breaking release so the plugin installs the eight skills its public page describes.
Drive, Lorg, Interrogate and Pair are removed (rulings 2026-09-18 and 2026-09-19 in
`docs/decisions.md`).

## What changed

- Removed `skills/drive`, `skills/lorg`, `skills/interrogate`, `skills/pair`, and
  `hooks/pair.sh` with its `hooks/hooks.json` entry and its cases in `tests/hooks_test.sh`.
- Three skill-count assertions lowered to 8 (`test_visual_default.py`, two in
  `test_question_form.py`).
- Both capability lists rewritten and kept byte-identical; `CLAUDE.md` rewritten for
  eight skills; version 0.141.0 in the three places.
- README `What's New` and `CHANGELOG.md` carry the same 0.141.0 entry.
- Corrected: `docs/guide/getting-started.md`, `docs/playbook.md`, `docs/machine-setup.md`,
  `skills/tend/SKILL.md`, `docs/state-contract.md`.
- One dead `skills/drive/SKILL.md` bullet deleted from `## Grounding` in each of
  `docs/product/gate-reachability.md` and `docs/product/question-set-derivation.md`
  (the audit refuses a grounding bullet whose file is gone; Anthony approved this),
  and `docs/plans/progress.*` re-rendered.

## Deliberately not changed (a second release removes the ladder and ledger)

`tools/gates` (its README and `kit.py` still name Drive); Conductor's "Do not invoke
Drive" line and the test that pins it; `docs/lorg-report.md` (now an orphan); old
diagram generators; all dated history. Known consequence: `funnel-driver` went from 2
missing needs to 4 because its ledger cited the removed skill file.

## Readings so far

Baseline: 758 unit and 21 hook tests green. After the change: every CI step in
`.github/workflows/gate.yml` run locally and clean; hook tests 16 green; full unit rerun
green before this was sent.

## Questions

1. Does anything still shipping invoke or depend on the four removed skills, `pair.sh`
   or `kivna/.pair`?
2. Does any living, newcomer-facing surface (README outside its dated release entries,
   `site/`, `docs/guide/`, `examples/`) still promise them?
3. Is every claim in the 0.141.0 release note accurate?
4. Would anything here turn CI red, or break a fresh install of the plugin?

## Reply shape

Findings ranked most serious first, each with file and line and why it matters. Then
say plainly either "clear to push" or "not clear to push".
