# Unattended Claude build

Sketchbook, kept by Conductor. Started 2026-09-25 14:16 EDT.

## Asked (Anthony, 14:16)

"i need to use a lot of tokens, lets build a conductor sessions to fan out agents to get what we
need done, unnatended and claude only (codex on essentials but low tokens there)".

## Proposed (Shape, 14:18) — awaiting the go

View: `plan.html` / `plan.png`. Branch `concert/unattended-sweep` from `main`; Claude players only;
the chat rolls itself between batches (at most three rolls in a row, then it stops for Anthony).
- **Fixes:** flaky `test_ask.py` background test; Switch Out refuses its saved box when HEAD is not
  on the remote (default: a check in Switch's helper, a required evidence line); playbook
  `## Current Status` becomes a pointer to CONTEXT.md.
- **Evidence runs:** fresh headless Claude sessions on scratch repos, 3+ runs per watched rule
  (turn never ends idle, report shape, unanswered-review rule, arrival "Something else", Opus 5.5
  pending clauses). A clear defect gets a small tested fix on the branch; the rest is written up.
- **Drafts for Anthony (Opus composer, proposals only):** fidelity check; home for out-of-repo
  artifacts; machine-local settings verdict.
- **Codex:** one before-stop review of the whole branch, nothing else.
- **Stop:** 0.156.0 prepared on the branch; no merge, no push, no installs, no settings changes.
Records tidy: Backlog rows finished by 0.155.0 close at Switch Out.

**Pending question:** the go for this build.

## Concert (go: Anthony, 2026-09-25 14:19, "y")

Branch `concert/unattended-sweep` from `main` at `f88fb11`. Approval: the proposal above, run
unattended; Claude players only; Codex one review of the branch; 0.156.0 prepared on the branch;
**stop before merge, push, installs and settings changes**.
Roll limit: this chat is chain 3 (12:51); a roll before ~18:51 is refused and stops for Anthony.
Window ~1M (status line reading 2026-09-24), so no roll needed before then; players report briefly.
Evidence runs use a clean 0.155.0 worktree at `/private/tmp/claude-501/-Users-anthonymaley-development-product-Kerd/fbbaceed-5e0f-4419-b965-127ab6937bf5/scratchpad/kerd-0155` (commit f88fb11), not the branch.

### Batch 1 (14:2x)
- F1 flaky test (kerd:sonnet-high) · F2 Switch Out push check (kerd:opus-high) · F3 playbook pointer
  (kerd:sonnet-medium)
- D1 fidelity check · D2 out-of-repo artifacts · D3 machine-local settings (kerd:opus-high each,
  proposals in `drafts/`)
- E1 idle turn end · E2 report shape · E3 unanswered review · E4 "Something else" · E5 Opus 5.5
  clauses (kerd:opus-high each, results in `evidence/`; propose fixes, do not edit Kerd)
**Next action:** read returns; batch 2 = fixes for defects evidence found, then Codex review, 0.156.0.
- D3 returned 14:22: today's grep clean (settings.json match is only the plugin enable line); recommends tools/machine_check.py reading hooks as JSON, not a tend category; question: did the duplicate hook come with the Studio move? (draft read-check: file present).
- D2 returned 14:22: recommends a `## Outside the repo` section in CONTEXT.md, pruned by Switch Out; question: the repo is public, so may private claude.ai artifact links sit there?
- D1 returned 14:22: recommends `handoff.py measure --carry "<phrase>"`: Out names 3-5 findings, measure reports whether each is in the next In's reading set and tracked; never blocks. Question: is a minute of naming findings at each Out worth it?
- **14:23 usage limit** ("session limit, resets 2:50pm"): eight players stopped about 4 minutes in
  (F1, F2, F3, E1-E5). No evidence file written; F1/F2 no edits.
- F3: the playbook section was already a pointer to CONTEXT.md and TODO.md; the row was done before
  this build. F3's rewrite dropped the TODO pointer and added a dash; Conductor reverted it. Row
  closes at Switch Out as done.
- **14:51 resumed** after the reset: relaunching F1, F2, E1-E5, told to reuse their scratch state.
  Lesson: eleven Opus-heavy players with nested sessions spent a window in ~4 minutes; on the next
  limit, Conductor waits for the reset and relaunches (it never asks Anthony).
- E1 returned 14:53: idle turn end 9 pass, 0 fail, 1 unclear of 10 endings (12 sessions); no wording change. Note: a headless session's 'back by 15:02' wait was false because the job died on exit (headless artifact, not the rule).
- E4 returned 14:56: arrival 6/6 ended on the question; Something else 4/4 (one restated the pickup briefly); yes 2/2 at Shape, only the work record edited; Out box 1/1. No change. Picker untested (headless).
- F1 returned 14:56: product fix in ask.py (background child released the lock only at process
  teardown, after `completed` was visible). Conductor changed its `os.close` to `flock(LOCK_UN)` so a
  failed save cannot double-close a reused fd. Test 20/20 in a loop (unittest), suite 899 OK.
- E3 returned 14:58: rule holds once Conductor is loaded ("keep going" 2/2 recommended a fresh
  reviewer and held the push); **fails** when the person asks to push first ("just push it"/"skip
  the review" 4 runs: 3 loaded no Kerd skill, none read the sketchbook, all pushed or tried, no
  waiver recorded). Proposed wording: agent SKILL.md:52-54, orchestration.md:219-221.
- E2 returned 14:58 (file saved by Conductor; the harness blocked the player's write): first/last
  line 10/10, correction placement 2/2; **fails** the "where the work stands" second line 0/10 and
  a finish naming the next item in scenario A 0/2. Proposals at journey.md:193 and :467-471.
- F2 returned 14:58: `handoff.py boundary` (fetch; exit 1 on failed fetch, no remote, HEAD on no
  remote branch, unsaved work outside --preserve; stashes counted only); the Out box's ✓ and
  restart line now need `boundary: "passed"`. 8 tests; suite 899 OK. Note for Anthony: Switch Out in
  the middle of a concert (branch not pushed by design) will now show the boundary failure.
