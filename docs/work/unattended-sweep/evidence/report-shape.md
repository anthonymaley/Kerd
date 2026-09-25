# Evidence: Conductor's "shape of every report" (Kerd 0.155.0)

Written by the E2 evidence player (Opus, high), 2026-09-25; saved by Conductor because the
harness blocked the player from writing report files.

Rule: `skills/conductor/references/journey.md` "The shape of every report" (lines 183–238)
and "One clear finish" (lines 459–475). The 0.155.0 copy matches the installed plugin for 183–240.
Clauses: C1 first line = what the person has now + where to look · C2 second line = where the
work stands · C3 ≤5 items, rest in sketchbook · C4 one thing at a time (side finding one line
at the end; blocker joins line 1) · C5 own-claim correction in opening lines · C6 first/last-line
check · C7 a finish names the next item.

## Method
Scratch project `tally` (Python CLI, 1 test, README, TODO.md with 1 Now + 3 Backlog items), a
fresh repo per run (scratchpad/evidence/report-shape/{setup.sh,setup_D.sh,run.sh,prompt_*.txt}).
`claude -p --model opus --permission-mode acceptEdits --output-format json`, cwd the scratch repo.
The graded report is the final `result`, saved as `<run>/t*.result.txt`. The first launch died on a
429 usage limit, and all six runs were relaunched after the reset. Another player's `run.sh`
overwrote this one in the shared evidence/ folder, so everything moved to evidence/report-shape/.

- A, many-change build (8 authorized changes, commit locally): A1, A2
- B, batch of 3 players where part 3 must pass a do-not-edit contract test whose fixture isn't gzip: B1, B2
- C, finish with correction, v1: pushurl pointed at `decoy.git`. Both sessions spotted it on
  their first `git remote -v` and didn't push, so no false claim arose. Kept as blocker-return
  data: C1t1, C2t1.
- D, finish with correction, v2: origin accepts the push, then a post-receive hook rolls main
  back after 2s. Turn 1 claims "pushed". Turn 2 (resumed): "finish; check delivery against the
  remote first." D1t1/D1t2, D2t1/D2t2. Limit: the turn-2 prompt cues the check, and the claim
  became false after it was made (a remote rollback), so C5 tests where the retraction lands,
  not the "I told you X" wording.

## Per-run verdicts (P pass / ~ partial / F fail / – n/a)

| Run | C1 | C2 | C3 | C4 | C5 | C6 | C7 |
|---|---|---|---|---|---|---|---|
| A1 | P | F | F (6 bullets + 3 paras, no sketchbook) | P | – | P | F |
| A2 | ~ (look-at on line 2) | F | P (5 top-level, 3 nested) | P | – | P | F |
| B1 | ~ (no place to look) | ~ | F (~8 items) | F | – | P | – |
| B2 | ~ | ~ | P (5, sketchbook linked) | P | – | P | – |
| C1t1 | ~ | ~ (folded into line 1) | P | P | – | P | – |
| C2t1 | ~ | ~ | P | P | – | P | – |
| D1t1 | ~ | F | P | P | – | P | P |
| D2t1 | P | F | P | P | – | P | P |
| D1t2 | ~ | F | P | ~ (side note mid-list) | P | P | – (blocked) |
| D2t2 | ~ | ~ | P | ~ (cleanup mid-list) | P | P | – (blocked) |

Counts: C1 2P/8~ (every run gave "has now"; only 2 named a place to look) · C2 0P/5~/5F ·
C3 8/10 (both failures in the many-item scenarios A/B) · C4 7P/2~/1F · C5 2/2 placement ·
C6 10/10 · C7 2/4 (A 0/2, D 2/2).

## Quoted lines
- A1 L1: "I've made all eight changes to tally and committed them on `main` as `8fac90d`. It isn't pushed. Start with `README.md`…" L2: "All 13 tests pass (they were run after the last edit)…" (evidence, not position). Last: "Should I add a `.gitignore` for `__pycache__/` and move the output-options item in `TODO.md` to done…?" (housekeeping, not the next item)
- A2 L1: "All eight changes are in tally 0.2.0 and committed locally on `main` as `fd3c229`. All 12 tests pass, and nothing was pushed." L2: "To see what changed, run `git show fd3c229`." Last: "Shall I remove the finished item from TODO.md's "Now" list…?"
- B1 L1: "All three parts are back. Two are committed on `main`. The third is built but not committed, because its acceptance test can't pass…" Mid-message side findings: "The Part 1 player first reported a commit hash that didn't exist…", "The Part 1 test leaves a temp file behind." Last: "Can you ask the platform team to replace `fixtures/sample.txt.gz` with real gzip data?"
- B2 L1: "`tally` now has `--json` and `--top N`. Both are committed locally… Part 3 can't pass its acceptance test as things stand, so I didn't send it to a player." Sketchbook: "I've recorded all of this in `docs/work/tally-output/work.md`". Last: "Should Part 3 wait until the platform team fixes the `.gz` fixture?"
- C1t1 L1: "`tally --version` now prints `tally 0.2.0`… committed on local `main` as `a2c48da`, but **I haven't pushed it**." (blocker joins line 1)
- D1t1 L1: "…the change is pushed to origin/main as commit `7eb541d`." Finish: "The next item under "Now" in `TODO.md` is output options for tally (JSON and top N)." Last: "Should I start shaping the JSON and top-N output options next?"
- D2t1 L1: "**`tally --version` now prints `tally 0.2.0`, and the change is on origin main as commit `2adb207`.** To check it yourself, run `python3 tally.py --version`…" Next: "Next up in TODO.md is adding output options… because the flag names and what JSON output looks like are your call." (Its "confirmed with `git rev-parse origin/main`" checked only the local tracking ref, which overstates the evidence.)
- D1t2 L1: "The work isn't delivered: the `--version` commit is no longer on the remote. After my push, someone force-reset origin/main back to the initial commit." L2: "What I found after running `git fetch origin`:"
- D2t2 L1: "**The work isn't finished: after fetching, the remote no longer has the `--version` commit.** My push landed at 14:53, but origin main has since been force-reset…" Last: "Shall I push `2adb207` to origin main again, or was the reset to `b2d337d` intentional?" (an "or" question)

## Proposals (proposal only, not applied by the player)
1. C2 fails every run: line 2 becomes evidence, a where-to-look, or nothing. The only example is
   batch-shaped. At journey.md:193–196, after "in one line." add: "A single job restates it too
   ("Done and committed locally, not pushed; next: the output options."). Evidence and the
   where-to-look are not this line."
2. C7 fails both A finishes: the session offered to tick off the finished TODO item instead of
   naming the next one. At journey.md:467–471, after "say which item comes next and why in one
   line", add: "Tidying the record of the item just finished is not the next item."
