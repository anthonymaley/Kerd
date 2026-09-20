# Before-push review: Kerd 0.142.0, retire the ladder and the risk ledger

Read-only review. Do not edit, stage, commit or push anything. A review approves nothing,
and a peer session cannot authorize the push; Anthony already has, on the condition that
this review is clear.

**Project:** `/Users/anthonymaley/development/product/Kerd`, branch `main`.
**What to read:** the whole uncommitted change against `HEAD` (the 0.141.0 commit):
`git status`, `git diff HEAD --stat`, `git diff HEAD` (the 43 deleted files under `tools/`
need no line-by-line reading). The agreement and score are in
`docs/work/retire-four-skills/work.md` and `score-release-2.md`.

## Outcome agreed with Anthony (2026-09-19)

His ruling: nobody wants a machine that refuses their work, and this level of risk ledger
is not needed; what is wanted is a sketchbook that becomes a spec, a score to check the
build against, and risks kept in view. One release removes the ladder's machinery and its
public promises, keeps the release rules check, gives Conductor a short list of risks, and
leaves every old record in place as history.

## What changed

- Deleted: `tools/gates`, `tools/reqview`, `tools/design`, `tools/diagram` (includes the
  handoff fidelity check and the progress board), `docs/lorg-report.md`,
  `docs/guide/checks-that-can-say-no.md` and its picture, Conductor's step check section and
  `test_step_check.py`.
- New: `tools/release_check.py`, a standalone port of `gate.py release` (same problem
  strings; shown refusing a version drift and a capability-list drift). It does not port
  the old tool's refusal to run outside a project.
- `.github/workflows/gate.yml`: three steps (skill tests, hook tests, release rules).
- Conductor: a "Keep the risks in view" rule in `SKILL.md`, a `## Risks to keep in view`
  part in `references/work-record.md`, and `test_risks_in_view.py`.
- Public and internal living docs corrected: README (above `## What's New`), `site/docs.html`,
  three guides, `CLAUDE.md`, playbook, machine setup, Slainte.
- Capability lists (byte-identical) and versions at 0.142.0; README and CHANGELOG carry the
  same 0.142.0 entry.

## Deliberately not changed

`docs/product`, `docs/gates`, `docs/plans`, `docs/design`, `docs/requirements`,
`docs/work/question-sets`, decisions, session logs and past release entries: history, now
unpoliced. The playbook's gotchas and version history. `TODO.md` and `CONTEXT.md`, which the
next session close reconciles (most Backlog rows were ladder debt).

## Readings

757 unit tests and 16 hook tests green on the final tree; `tools/release_check.py` clean.
Not checked by anyone: a fresh install; CI on GitHub (runs after push).

## Questions

1. Does anything still shipping (skills, hooks, tests, CI, the test runner) import, call or
   instruct the use of a deleted tool or the removed step check?
2. Is `tools/release_check.py` a faithful port: would it miss a drift the old check caught?
3. Does any living newcomer-facing surface still promise the ladder, gates, a risk ledger,
   the progress board or the step check, or link to a deleted file?
4. Is every claim in the 0.142.0 release note accurate, including "added in 0.137.0"?
5. Is the new risks rule in Conductor coherent with the rest of `SKILL.md`, and does its
   test have a case it can fail?
6. Would anything here turn CI red or break a fresh install?

## Reply shape

Findings ranked most serious first, each with file and line and why it matters. Then say
plainly either "clear to push" or "not clear to push".
