# Score — release 2: retire the ladder and the risk ledger (Kerd 0.142.0)

Author of every step: Conductor. A defect in a step returns to Conductor, not the player.
Project root: `/Users/anthonymaley/development/product/Kerd`, branch `main`. Baseline: the
0.141.0 release commit, plus uncommitted edits under `docs/work/retire-four-skills/` only.

## Agreement (Anthony, 2026-09-19 21:53, "yes")

Remove the ladder's machinery and its public promises; keep the release rules check in its
own small file, the skill tests and the hook tests; give Conductor a short "risks to keep in
view" list; leave every old record where it is as history; release as 0.142.0; Codex reviews
before push; push when its review is clear or its findings are plain fixes.

**Why:** his ruling the same evening: nobody wants a machine that refuses their work, and this
level of risk ledger is not needed. What is wanted is a sketchbook that becomes a spec, a score
to check the build against, and risks kept in view.

## Rules for every player

- Edit only the files your step owns. Other players are editing other files at the same time.
- Do not run `git add`, `git commit`, `git push`, `git stash`, `git checkout` or `git restore`.
- Never touch dated history: `kivna/sessions/`, `docs/gates/`, `docs/plans/`, `docs/decisions.md`,
  `docs/backlog-archive.md`, `CHANGELOG.md`, README entries under a `### vX.Y.Z` heading,
  `docs/product/`, `docs/requirements/`, `docs/design/`, `docs/work/` (other than your own outputs).
- Do not grade your own work. Report what you changed, the commands you ran and their output,
  and anything you could not source or were unsure of. If a step asks for something the files
  do not support, say so and leave it rather than inventing it.
- Plain product English in anything a newcomer reads. No em dashes in new prose.
- All slash commands keep the `kerd:` prefix.

---

## P1 — Lift the release rules check into its own file  `[delegate]`

**Result.** A new standalone `tools/release_check.py` (Python 3, standard library only, no import
of `kit` or `gate`) that performs exactly what `python3 tools/gates/gate.py release` performs today,
so the ladder tools can be deleted without losing it.

**Why.** The release check (version drift across the three manifest locations, capability-list
drift between the two manifests, bare slash-command references) protects every push. It lives in
`tools/gates/kit.py` as `release_audit(root)` with helpers `_release_files`, `_release_versions`,
`_release_capability`, `_release_namespace` (around lines 1638–1830) and is exposed by
`_cmd_release` in `tools/gates/gate.py` (around line 215). Read those, plus anything they call.

**Build.**
- Port those functions and every helper or constant they depend on, behaviour unchanged, same
  problem strings.
- CLI: `python3 tools/release_check.py [--root PATH] [--json]`. Root: `--root`, else the Git
  top level of the current directory, else the current directory. Output and exit codes identical
  to `gate.py release`: `release: clean` and 0; or one `problem: …` line each, then
  `release: N problem(s)` with the same pluralisation, and 1; `--json` prints the list.
- `python3 tools/release_check.py selftest`: port any release-specific selftest cases from
  `gate.py`/`kit.py`; if there are none, write three small ones using a temporary directory
  (clean tree passes; version drift refuses; capability drift refuses). Prints `selftest: N ok`.
- If the namespace scan enumerates paths under `tools/gates`, `tools/reqview`, `tools/design` or
  `tools/diagram`, it must not fail when those directories are absent.

**Owns.** `tools/release_check.py` only. Do not edit `kit.py`, `gate.py` or anything else.

**Proof.** Show: (1) both commands on the current tree, same output; (2) in a temporary copy of the
two manifests' tree (or a temp dir fixture), a version drift and a capability drift each reported
with the same problem text by both tools; (3) the selftest output; (4) `python3 -c "import ast,sys;
ast.parse(open('tools/release_check.py').read())"` and a grep showing no `import kit`/`import gate`.

---

## P2 — Conductor: remove the step check, add risks to keep in view  `[delegate]`

**Result.** Conductor no longer asks a project which ladder step a work item is on, and its
sketchbook carries a short list of risks that it reads back before Ready and before the goal check.

**Owns.** Everything under `skills/conductor/` only.

**Remove the step check.**
- In `skills/conductor/SKILL.md`: the whole `## Check where the work stands` section; the
  sentence in the opening that makes the step check "the single exception" (rewrite that paragraph
  so it simply says Conductor does not invoke old gate or session machinery, with no mention of
  Drive, which no longer exists); the step-check clause in the frontmatter `description`
  ("For a work item recorded in the user's project, it checks where the work stands at pickup and
  before a build, names missing groundwork and offers it, and records a go-ahead anyway."); any
  in-file link to the removed section.
- Delete `skills/conductor/scripts/tests/test_step_check.py`.
- Search every file under `skills/conductor/` for `step check`, `gate.py`, `tools/gates`,
  `docs/product`, `ladder`, `rung`, `risk ledger` and remove or reword living instructions that
  depend on the ladder. Leave a mention alone where it is only an illustrative example of someone
  else's project and removing it would damage the example; list those in your report.
- If another test pins wording you change, update that test to the new wording and say so.

**Add risks to keep in view.** Use this wording, adjusting only for fit with the surrounding text:

In `SKILL.md`, in "Rehearsal, then the concert", directly after the **Keep a sketchbook** paragraph:

> **Keep the risks in view.** When the person or the work names something that could sink the
> work or hurt later, write it in the sketchbook's short risks list: the risk in one plain
> sentence, and what is being done about it or that it is accepted as it stands. No sizing,
> columns or tiers. Read the list back before saying Ready and before the goal check, and say
> which risks are still open. An empty list is fine; never invent risks to fill it.

In `references/work-record.md`: add a matching short part describing a `## Risks to keep in view`
section of the record (one line per risk: the risk, what is being done or "accepted", the date it
was named), in that file's existing voice, and state that it is not a ledger and gates nothing.

In the list of what rehearsal comes to hold ("the idea and why it matters, whether it can work
and is worth doing, the goals, the constraints, and the design"), add the risks worth keeping in
view.

**Test.** Add `skills/conductor/scripts/tests/test_risks_in_view.py` in the style of the sibling
wording tests: it passes when `SKILL.md` carries the rule's three obligations (write it down,
read it back before Ready and the goal check, never invent) and `work-record.md` describes the
section; it fails if any is absent. Also assert `SKILL.md` no longer contains
`Check where the work stands` or `gate.py`.

**Proof.** `python3 tools/run_tests.py` full output tail (count and OK/FAILED), and
`git status --short skills/conductor`.

---

## P3 — Public pages: take down the checks guide and every promise of the ladder  `[delegate]`

**Result.** Nothing a newcomer reads promises the ladder, gates, checks that refuse, a risk
ledger, a progress board or the step check.

**Owns.** `README.md` outside the `## What's New` section (do not touch that section or any
`### vX.Y.Z` entry; Conductor adds the release note later), `site/`, `docs/guide/` (tracked files
only; leave the untracked `docs/guide/reference-from-readme.md` alone), `docs/pictures/`,
`examples/`.

**Do.**
- Delete `docs/guide/checks-that-can-say-no.md` and `docs/pictures/guide-checks-that-can-say-no.svg`.
- Remove the entry for it in `site/docs.html` (around lines 79–82) and any other link to either
  deleted file anywhere you own; keep the page's layout sound (no empty list, no orphan heading).
- Search what you own for: `ladder`, `rung`, `gate`, `checks that can say no`, `risk ledger`,
  `step check`, `progress board`, `docs/product`, `refus`. For each living statement that
  promises the removed machinery, remove it or reword it to what Kerd does now: the sketchbook
  that becomes a spec, the score the build is checked against, the goal check at the end, an
  independent reviewer, and a short list of risks kept in view. The release rules check in CI
  still exists; a statement about CI checking releases may stay if it is accurate for
  version and capability-list drift only.
- `examples/` are accounts of real past work. Do not rewrite what happened. Only change a
  sentence there if it tells the reader Kerd offers the removed machinery today.
- Where the story named three problems and their answers, "done is whatever the AI says" is
  answered by the score, the goal check and the independent reviewer, not by gates.

**Proof.** The searches above re-run over what you own with each remaining hit explained in one
line; a link check: every relative link and image path in the files you touched resolves on disk
(show the command and its output); `git status --short` for your paths.

---

## P4 — Kerd's own living documents  `[delegate]`

**Result.** Kerd's internal living documents describe the repo as it will be after this release.
What will exist: `tools/run_tests.py`, `tools/release_check.py` (new; same behaviour as today's
`gate.py release`), `tests/hooks_test.sh`. What will be gone: `tools/gates/`, `tools/reqview/`,
`tools/design/`, `tools/diagram/`, the handoff fidelity check, Conductor's step check, and all CI
steps except skill unit tests, hook tests and the release rules. What stays as unpoliced history:
`docs/product/`, `docs/gates/`, `docs/plans/`, `docs/design/`, `docs/requirements/`,
`docs/work/question-sets/`.

**Owns.** `CLAUDE.md`, `docs/playbook.md`, `docs/machine-setup.md`, `docs/state-contract.md`,
`skills/slainte/`, `skills/tend/`, `skills/switch/`, `skills/kivna/`, `skills/skriv/`,
`skills/agent/`, `skills/visuals/`.

**Do.**
- `CLAUDE.md`: the sentence "CI enforces the mechanical subset…" now names
  `python3 tools/release_check.py`; the Project Structure block drops the removed tool folders,
  adds `tools/release_check.py` and `tools/run_tests.py`, and describes the kept record folders as
  history from the retired ladder; the opening description stays accurate.
- `docs/machine-setup.md`: the smoke tests become `python3 tools/release_check.py` (expects
  `release: clean`), `bash tests/hooks_test.sh` (expects `Passed: 16  Failed: 0`) and
  `python3 tools/run_tests.py`; remove other instructions that need the removed tools.
- `docs/playbook.md`: update the living parts (overview, structure, skills list, CI description,
  "Current Status" if it names the ladder as current). Leave gotchas, lessons and the version
  history as written; they are dated learning.
- Skills you own: search for `gate.py`, `tools/gates`, `kit.py`, `fidelity`, `progress.py`,
  `matrix.py`, `reqview`, `docs/product`, `ladder`, `rung`, `risk ledger`, `step check` and remove or
  reword living instructions that depend on removed machinery (Slainte is known to name it).
  If a wording test under that skill's `scripts/tests/` pins text you change, update the test and
  say so. Switch's arrival renderer uses "rung" and "ladder" for the PHASE cell as a generic
  project-stage idea; leave that unless it names Kerd's gate tools.

**Proof.** The search re-run over what you own with each remaining hit explained in one line;
`python3 tools/run_tests.py` tail; `git status --short` for your paths.

---

## K1 — Delete the machinery, cut CI, release  `[keep]`

Conductor, after P1–P4 return and are read: sequenced on all four and touches shared release
files. Delete `tools/gates`, `tools/reqview`, `tools/design`, `tools/diagram`, `docs/lorg-report.md`;
rewrite `.github/workflows/gate.yml` to three steps; capability lists (drop the step-check clause,
add risks kept in view) byte-identical; versions to 0.142.0; README What's New and CHANGELOG;
full tests, hook tests, `tools/release_check.py`; Codex before-push review; commit and push.

## Goal check (before leaving the loop)

1. `git grep` over living surfaces finds no instruction that needs a removed tool.
2. `tools/release_check.py` refuses a version drift and a capability drift (shown, not assumed).
3. Full tests and hook tests green; CI green after push.
4. Conductor's SKILL.md carries the risks rule and no step check.
5. No link on the site, README or guides points at a deleted file.
6. Every old record is still where it was (`git status` shows no change under the history paths).
