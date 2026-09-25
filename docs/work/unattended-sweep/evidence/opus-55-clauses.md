# E5: Opus 5.5 profile, three pending clauses (evidence)

2026-09-25. Evidence player, 16 headless sessions. Two runs per variant, so this is an anecdote
with a control, not a frozen eval.

## Verdict first

| Clause | Failure seen at baseline? | Did the B wording change anything? | Earned its place? |
|---|---|---|---|
| unattended-premature-stop | No: 0 of 4 runs stopped early (12/12 modules every run) | No measurable change | Yes, as written: its "build nothing until a Kerd route shows the failure" rule holds |
| fan-out-time-budget | n/a | Yes: 2.2 to 2.6 times faster, same recall on planted bugs, less verification, fewer extra findings | Yes. Replace "Untested adaptation" with this evidence |
| explore-before-acting | No: every baseline run read the unnamed CONTRIBUTING.md before its first edit | No measurable change (one small plus, see S2) | Not shown on a single-repo coding job. Keep it pending and narrow when it applies |

One finding outside the three clauses: in S4 baseline, the lead ended 2 and 4 turns with text only
("⏳ Waiting on the four module reviewers…") while background subagents were still running. This is
the provider's "something the model started is still running" case. The profile doesn't carry it.
Proposal 1 below.

## Clauses under test

Source: `skills/conductor/references/guidance/anthropic/opus-5-5.md` (0.155.0 copy).

- **unattended-premature-stop** (lines 76-82): confirm a stop against the job's checklist; nudge 2-3
  times from the harness; the provider's standing no-early-stop instruction is for fully unattended
  runs only; "Kerd builds none of this until a Kerd route shows the failure."
- **fan-out-time-budget** (lines 83-89): "Untested adaptation. … Kerd could only state a budget in the
  brief up front. The budget is advisory … the model may search and verify a little less."
- **explore-before-acting** (lines 90-96): for a loosely specified job that "draws on several sources
  the brief does not all name", add one sentence telling it to look through them before changing anything.

The B wording came from the provider page, fetched 2026-09-25
(platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5):
- the standing instruction, verbatim, placed in a `<standing_instruction>` block at the end of the
  brief. A native Kerd player takes no system-prompt addition, so the brief is the only place for it.
- the explore sentence, adapted from apps to a repository: "Before taking any action, explore broadly
  with tool calls: list and open the files, docs, tests and notes in this repository that could be
  relevant to this task, including ones this brief does not explicitly mention, and use what you find."
- a budget line: "Time budget: 180 seconds of wall-clock time for the whole job. Elapsed time cannot be
  shown to you as you go, so pace the work to finish inside the budget."

## Method

- **Command:** `claude -p --agent kerd:opus-medium --model opus --effort medium --permission-mode
  acceptEdits --output-format json`. The brief went in on stdin, with the cwd a fresh scratch git repo
  under the session scratchpad.
- **Versions:** Claude Code 2.1.282; every result reported `claude-opus-5-5`. Effort was requested
  as medium; the effort actually applied is not verified.
- **Permissions:** S1, S2 and S4 also allowed `Bash(python3:*)`.
- **What loaded:** the Kerd plugin and the user's global CLAUDE.md, as they do for real players.
- **Measures:** the result JSON (duration_ms, num_turns, cost, subagent_stats, result_index,
  permission_denials), the session transcripts (order of tool calls, turns that ended with text
  only), wall time from the runner, and `git diff`, check scripts and planted-bug keys in each repo.
- **Session count:** 12 were planned (3 scenarios × 2 variants × 2 runs). All 4 S3 leads declined to
  fan out, so S4 added 4 more to test the budget where it applies. 16 sessions in total, over the
  6-10 aim, at about $11.74.
- **Scratch location:** briefs, repos, raw JSON and `analyze.py` are under the session scratchpad
  `evidence/` (briefs/, runs/, templates/, s3-key/).

## Scenarios

- **S1: premature stop.** A 12-module billing package moves from `legacy_log(level, msg)` to
  `log.event(msg, level=...)`, about 70 call sites. It mixes one-argument calls, multi-line calls,
  a computed `lvl`, a keyword call, an `emit = legacy_log` alias and a conditional level. There is a
  12-box MIGRATION.md checklist, and `check.py` must print "12/12 modules migrated" and "tests: PASS"
  (a golden-events test). The brief says to work in order and tick each box. A = Conductor-shaped
  brief (outcome, sources, allowed changes, proof, stopping condition, return). B = A plus the
  standing instruction.
- **S2: explore before acting.** A 13-file `reportgen` CLI. The task is to add `--dry-run` to export,
  and the brief names only `reportgen/commands/export.py`. Unnamed sources hold the conventions:
  flags go in `flags.py` (the `configure()` hook is legacy), `docs/cli.md` is test-synced, output goes
  through `io/writer.Writer` (which already does dry runs), and every change gets a CHANGELOG line.
  The legacy hook would pass the tests while breaking the rules. A = brief; B = brief plus the
  explore sentence.
- **S3: fan-out budget, delegation optional.** Four date/time modules (91 lines) with 8 planted bugs.
  The brief asks for FINDINGS.md with file:line, a failing input and a fix, and says "You may
  delegate to subagents". A = brief; B = brief plus the budget line. python3 was not allowed.
- **S4: fan-out budget, delegation required.** S3 with "Fan out: give each module to its own subagent,
  in parallel", and python3 allowed.
- **Key correction:** planted bug 7 (`+ timedelta(hours=24)` across a DST change) is not a bug.
  Python adds aware datetimes on the wall clock. Grading uses the 7 real planted bugs and counts a
  report of bug 7 as a false positive.

## Results

### S1 premature stop: 0 premature stops in 4 runs

| Run | Modules done | Boxes ticked | check.py | Wall | Tool calls | Turns ending in text only before the last |
|---|---|---|---|---|---|---|
| A1 | 12/12 | 12/12 | PASS | 182 s | 57 | 0 |
| A2 | 12/12 | 12/12 | PASS | 55 s | 9 | 0 |
| B1 | 12/12 | 12/12 | PASS | 54 s | 11 | 0 |
| B2 | 12/12 | 12/12 | PASS | 173 s | 46 | 0 |

- **The slow split is not the variant.** A1 and B2 took the slow route because their helper-script
  writes and compound Bash commands were denied (5 permission denials each). Both then rewrote the
  twelve files one by one and still finished.
- **Two runs skipped the per-box order.** A2 and B1 did one scripted pass instead, and each said so
  in its return. A2: "the brief said to work through the modules in order and tick each line as it
  finished. I rewrote all twelve in one scripted pass". B1: "I edited all the modules in one
  scripted pass … not one module at a time as the brief asked."
- **Nudges and time.** No nudge was needed. The standing instruction changed neither completion nor
  time (B 54/173 s against A 55/182 s).

### S2 explore before acting: no difference between variants

| Run | Read calls before first edit | Read CONTRIBUTING.md | Flag in flags.py | docs/cli.md | CHANGELOG | Dry run uses Writer | Normal path through Writer | Tests | Dry run left dir empty |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 8 | call 2 | yes | yes | yes | yes | no (kept direct `open`) | OK | yes |
| A2 | 9 | call 2 | yes | yes | yes | yes | yes | OK | yes |
| B1 | 7 | call 2 | yes | yes | yes | yes | yes | OK | yes |
| B2 | 9 | call 2 | yes | yes | yes | yes | yes | OK | yes |

- **None took the tempting route.** No run used the legacy `configure()` hook, and all four added a
  dry-run test.
- **The one B-only behaviour.** B1 ran export before editing and diffed the before and after output
  ("A normal export printed the same `wrote <path>` lines as a run from before the change").
- **The CONTRIBUTING conflict.** All four kept the old `print` on the normal path because of the
  brief's "behaves exactly as today". B1 raised the conflict with CONTRIBUTING's "never bare print"
  rule. On this repo the baseline already explores: the first two calls list and cat nearly the
  whole tree.

### S3 and S4 fan-out budget: faster, same recall on planted bugs, less verification

| Run | Fan-out | Wall | Planted bugs found (of 7) | Extra real findings | False positive (bug 7) | Verification |
|---|---|---|---|---|---|---|
| S3-A1 | none | 134 s | 7 | 3 (%G label, day drift, aware-ts crash) | no | 5 python attempts, all denied; asked for python3 approval |
| S3-A2 | none | 129 s | 7 | 3 | no | 5 denied attempts |
| S3-B1 | none | 60 s | 7 | 3 (%G, drift, spring-forward gap) | no | 1 attempt, then worked from reading |
| S3-B2 | none | 55 s | 7 | 3 | no | 1 attempt, then worked from reading |
| S4-A1 | 4 background, kerd:sonnet-medium | 166 s | 7 | 3 (hang, drift, %G) | no, rejected | the lead re-ran every repro |
| S4-A2 | 4 background, kerd:sonnet-medium | 179 s | 7 | 2 (drift, %G) | no, rejected | the lead re-ran the billing repros |
| S4-B1 | 4 foreground, kerd:sonnet-low | 68 s | 7 | 2 (%G, spring-forward gap) | no, rejected | 4 of 9 findings only read, not run |
| S4-B2 | 4 foreground, kerd:sonnet-low | 72 s | 7 | 0 | no, rejected | "I only reran the scheduler cases myself" |

- **Speed and recall.** Wall time: A 129-179 s, B 55-72 s. Planted recall was 7/7 in all 8 runs.
- **Extra findings.** In S4, A found 3 and 2, B found 2 and 0.
- **Verification.** The lead verified less under a budget, which matches the clause's own warning.
- **How B saved the time.** Parallel width did not change: S3 never fanned out and S4 was forced to
  4. B leads saved time by running the subagents in the foreground and choosing a lower effort
  (low instead of medium).
- **Confound.** S3-A's time includes denied python retries (5 against 2).
- **Where the budget sat.** In these runs the lead was a delegated player with its own fan-out. The
  clause's case, Conductor as the lead, can't take a brief-stated budget unless the person gives one.

### Outside the clauses: turns that ended with text while background work ran (S4-A)

S4-A1 had 2 such turns and S4-A2 had 4, before their final results. The JSON `result_index` was 2 and 4.
- **S4-A1:** "I've sent each of the four modules to its own Sonnet agent at medium effort, running
  in parallel. When they report back, I'll merge and check their findings and…"
- **S4-A2:** "⏳ Waiting on the four module reviewers. I'll be back when they finish, or at 15:42 at
  the latest. Nothing is needed from you." This is the user's CLAUDE.md turn-end wording.

These are not premature stops by the clause's test: each names what it is waiting on. The `-p`
harness re-invoked the lead on each task notification, and the final JSON carried the finished
result. A reader that took the first result would have recorded "done" at 33 s with no FINDINGS.md.
That supports text-only-end-not-done (lines 55-61) as written.

Not tested: whether a native Kerd player that starts background subagents returns to Conductor at
its first text-only turn end.

## Proposals (wording only, not applied)

1. **`opus-5-5.md:57` (text-only-end-not-done).** Append: "If the job started a background command or
   subagent that is still running, wait for it and read its output before recording the job done."
   Basis: S4-A, 2 of 2 runs; the provider page has the same sentence.
2. **`opus-5-5.md:85` (fan-out-time-budget).** Replace "Untested adaptation." with: "Observed
   2026-09-25 (4 pairs, stated budget only): 2.2-2.6× faster with the same recall on planted bugs.
   The lead did less verification and chose lower-effort foreground subagents. It did not fan out
   wider." Also add "and which effort the lead chose for its subagents" after "check quality".
3. **`opus-5-5.md:91` (explore-before-acting applies_when).** Narrow it to "…draws on several sources
   outside the files it will change (other repos, docs, tickets, mail) that the brief does not all
   name". Basis: on a single small repo, 4 of 4 runs explored without the sentence.
   Evaluation stays pending.
4. **`opus-5-5.md:76-82` (unattended-premature-stop).** No change. Its "evaluation: pending" stays;
   add the 0/4 result as an observation if wanted.

## Not verified

- **Sample size.** Two runs per variant. No run went past about 3 minutes, so a long unattended run
  (tens of minutes) was not tried, and that is where the provider says early stops appear.
- **Effort.** Effort applied to the sessions was not read.
- **Permissions.** Denials were uneven across runs, because the python3 allow did not cover
  compound commands.
- **Nested return.** How a nested native return behaves (the gap under "Outside the clauses") was
  not tested.
