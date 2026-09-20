# Retire four skills — sketchbook

Conductor's record for removing Drive, Lorg, Interrogate and Pair from the plugin.
View: [scope.html](scope.html) (proposed, drawn 2026-09-19 with diagram-design).

## Where this stands

**Both releases done on 2026-09-19: 0.141.0 removed the four skills, 0.142.0 retired the ladder and the risk ledger.** It began at Shape that evening, proposed. Anthony chose this work at Switch
In (the picker's "Yes — remove the four retired skills"); that chose the work and approved none of
its operations.

## Settled

- Rulings: Drive dropped for Conductor (Anthony, 2026-09-18); Lorg, Interrogate and Pair
  cut (Anthony, 2026-09-19). Cases in `docs/decisions.md`.
- Saved scope from the last sitting, proposed: one breaking release; Claude builds and
  releases; Codex reviews before push; stops at a reviewed release; nothing else rides
  along.

## Found at Shape (one trace, tested but not yet verified)

- The ruling tied Interrogate's removal to "the ladder and gate cleanup", read from the
  checks guide and not traced in code. Traced 2026-09-19 by search: the risk-ledger
  format is defined in `tools/gates/README.md` and `kit.py`; nothing under `tools/gates`,
  `hooks/`, `tests/` or `.github/` names Interrogate. Four old diagram generators do.
  Not yet confirmed by a test run with the skill folder gone.
- Each of the four is a single `SKILL.md`. Pair also owns `hooks/pair.sh`, its
  `hooks.json` entry, three cases in `tests/hooks_test.sh` and Tend's hygiene check.
- Drive is named in `tools/gates/README.md` (frame question set), a `kit.py` comment,
  Conductor's SKILL.md, `test_step_check.py`, the README and the playbook. The Backlog
  row asks that anything Drive does that Conductor lacks (frame-gate intake) be named
  before removal.
- `test_visual_default.py:54` asserts at least twelve skill entry points.
- Living mentions to correct: `CLAUDE.md`, both manifests' capability lists,
  `docs/playbook.md`, `docs/state-contract.md`, `docs/machine-setup.md`,
  `docs/guide/reference.md`, `skills/kivna/SKILL.md`, `skills/lorg` cross-reference.

## Proposed by Conductor, awaiting Anthony

- Interrogate leaves without a ladder or gate cleanup; the checks, ladder and ledger
  format stay exactly as they are.
- Version 0.141.0, following how earlier cuts shipped (trim 0.87.0, mode 0.75.0), though
  `CLAUDE.md` says MAJOR for a breaking change.

## Ruling, Anthony, 2026-09-19 18:48

Asked who other than him wants a machine to refuse their work, Anthony answered that
nobody wants it (paraphrased, his meaning kept): what is wanted is a sketchbook that
becomes a spec and a score used to check the work during the build, and risks recorded
so they are kept in view; this level of risk ledger is not needed; remove it.

Settles: the machine-refusal ladder and the tiered risk ledger go. Kept, in his words:
a sketchbook that becomes a spec and a score used to check work during the build, and
risks recorded to be aware of. Not yet settled: what "remove" covers beyond the ledger
and ladder checks (the CI release rules are a different thing), and whether it rides in
the same release as the four skills.

## Sequencing, 2026-09-19 18:48

Conductor proposed two releases (the four skills first, the ladder and ledger second);
Anthony said he did not mind and left it to Conductor. Delegated to Conductor, decided: two releases, in that
order. This delegates the order only; it approves no build, commit or push.

## Agreement, 2026-09-19 18:49

Asked "Shall I build release 1 and push 0.141.0 to `main` once Codex's review is clear?",
Anthony: yes. Agreed: build the removal of the four skills, run
the tests and CI rules locally, Codex reviews the whole change before push, commit and
push 0.141.0 to `main` if the review is clear or its findings are plain fixes. Stop and
bring one decision if a test shows a missed dependency or Codex raises something that is
his call. Not included: the ladder, ledger and checks (release 2).

Baseline for the change read: `main` at the 2026-09-19 session-close commit, tree clean
apart from the three local-only paths.

## Build, 2026-09-19 18:51–19:0x (uncommitted on `main`)

Done: four skill folders and `hooks/pair.sh` removed; `hooks.json`, `tests/hooks_test.sh`,
three skill-count assertions (one in `test_visual_default.py`, two in
`test_question_form.py`, the two missed by the Shape search and caught by the test run),
both capability lists, versions to 0.141.0, `CLAUDE.md`, the getting-started guide,
playbook, machine-setup, Tend, state-contract, README and CHANGELOG notes.
Readings: baseline 758 unit + 21 hook tests green; after the change 758 unit green on
the two repaired modules' rerun (full rerun owed), 16 hook tests green; `gate.py release`
clean, selftests clean.

**Stopped, as agreed, on a missed dependency.** `gate.py audit` refuses: two recorded
work items (`docs/product/gate-reachability.md`, `docs/product/question-set-derivation.md`)
list `skills/drive/SKILL.md` under `## Grounding`, and the audit resolves every grounding
bullet against the filesystem. `progress.py stale` also refuses. Both were clean at the
baseline (checked in a throwaway worktree). Trialled and reverted: rewording the bullet
still refuses; deleting the two bullets clears the audit; the board still needs a
re-render. Not left untracked: `docs/lorg-report.md` still exists with no owner.

## Go-ahead for the two grounding lines, 2026-09-19 19:35

Asked "May I delete those two dead grounding lines and re-render the board so release 1
passes CI?", Anthony: yes. Done; `gate.py audit` clean, board current. Honest
consequence on the board: `funnel-driver` went from 2 missing needs to 4, because its
ledger cited the removed Drive skill file.

## Review, Codex (before-push), 2026-09-19

First reply: not clear to push. Two blockers, both in `docs/machine-setup.md` (a setup
step still said `/kerd:pair on`; the hook-test count still said 21). Both fixed. A third
point concerned `docs/guide/reference-from-readme.md`, which is local only by ruling and
not in the commit; Codex agreed on re-read. It found no other live invocation, and the
release note accurate. Re-read verdict: clear to push. Codex did not run the tests or a
fresh install.

Readings on the final tree: 758 unit tests and 16 hook tests green; every CI step clean
locally. Not checked by anyone: a fresh install of 0.141.0.

## Left for release 2 (the ladder and ledger removal)

`tools/gates` still names Drive; Conductor's "Do not invoke Drive" line and its pinning
test; `docs/lorg-report.md`, now without an owner; the old diagram generators;
`docs/requirements/` mentions; a plain place in Conductor for risks to keep in view.

## Release 2, Shape, 2026-09-19 21:51

Anthony asked to do release 2. View: [scope-release-2.html](scope-release-2.html),
proposed. Terrain, traced by search: the ladder tools are called only by CI, Conductor's
step check and its test; the release rules check lives inside `tools/gates/kit.py`
(`release_audit` and its helpers) and must be lifted out before the tools go; the site
(`site/docs.html`), the checks guide and its picture, the README, `CLAUDE.md`, playbook,
machine-setup, Slainte and one example name the ladder; `docs/pictures` is not generated
by `tools/diagram`; the test runner covers skills only; Conductor has no place for risks
today.

Proposed by Conductor, awaiting Anthony: remove the machinery (`tools/gates`,
`tools/reqview`, `tools/design`, `tools/diagram`, the handoff fidelity check), Conductor's
step check, eight CI steps and the public promises; keep the release rules check in its
own file, the skill tests and hook tests; add a short "risks to keep in view" list to the
sketchbook; leave every old record in place as history; version 0.142.0; same flow, built
with players, Codex review before push, stops at a reviewed release.

## Agreement for release 2, 2026-09-19 21:53

Asked "Shall I build release 2 in that shape and push 0.142.0 once Codex's review is
clear?", Anthony: yes. Score: [score-release-2.md](score-release-2.md), every step written
by Conductor. Concert batch 1: P1–P4 to native players in parallel, disjoint files; K1 kept.
Change-read baseline taken before dispatch: the 0.141.0 commit plus uncommitted edits under
this folder only.

## Concert, release 2, 2026-09-19 21:55–22:2x

Batch 1, four native players in parallel on disjoint files, every one observed on the
model and effort requested (P1 Sonnet medium, P2 Opus high, P3 Sonnet high, P4 Sonnet
medium); no dispatch without a named model. Each return was read against the baseline.
- P1: `tools/release_check.py`, standalone. Conductor re-ran it: clean tree, selftest,
  a version drift and a capability drift each refused with exit 1. By Conductor's score it
  does not port the old tool's refusal to run outside a project.
- P2: step check removed from Conductor, the risks rule added as scored, `work-record.md`
  gains `## Risks to keep in view`, `test_risks_in_view.py` added, `test_step_check.py` gone.
- P3: checks guide and picture deleted, site row removed, README and three guides reworded.
  Conductor corrected one player phrase in three places ("before a push goes out"; the
  check runs on a push).
- P4: `CLAUDE.md`, playbook, machine setup, Slainte. Slainte no longer claims CI audits gate
  records or treats an acceptance record as a release trigger.
K1 (Conductor): four tool folders and `docs/lorg-report.md` deleted, CI cut to three steps,
capability lists and versions, release notes.

Goal check against the score: (1) no living instruction needs a removed tool; (2) release
check refuses version and capability drift, shown; (3) 757 unit and 16 hook tests green,
CI after push; (4) Conductor carries the risks rule and no step check; (5) no link to a
deleted file; (6) no change under the history paths. All met before review.

Review, Codex (before-push): clear to push, no findings; it compared the old and new
release functions and found their syntax trees identical. It did not run the suite, CI, a
fresh install, or the risks rule in a real sitting.

## Risks to keep in view

- The risks rule is wording and a wording test; whether Conductor actually reads the list
  back before Ready is unobserved. Watch it in the next real piece of work. Named 2026-09-19.
- `TODO.md` and `CONTEXT.md` still describe the ladder as live (launch sequence, most of the
  Backlog). Reconcile at the next session close, with verdicts. Named 2026-09-19.
- Nobody has done a fresh install of 0.141.0 or 0.142.0. Named 2026-09-19.

## Pending question

None.
