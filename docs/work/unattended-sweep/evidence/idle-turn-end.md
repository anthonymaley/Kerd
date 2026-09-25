# Evidence: a turn ends carrying on, or stopped on a reason

Kerd 0.155.0 (installed plugin, `installPath .../kerd/0.155.0`). Run on 2026-09-25 with fresh headless sessions:
`claude -p --model opus --permission-mode acceptEdits --output-format json`, and `--resume` for second turns.
Each run used its own scratch git repo under the session scratchpad
(`.../scratchpad/evidence/idle-s*`). None pointed at the Kerd repo.

The rule under test is from the read-only copy: `skills/conductor/references/journey.md:430-458`,
plus `skills/conductor/SKILL.md:203-207`. A Conductor turn must end in one of three ways:
- on one question the person can answer cold
- on a named wait: the job, how the session resumes, and when it should be back (or "return time unknown")
- by carrying on

It never ends idle with nothing asked. A partner's contribution still gets a line to the person.

## Scratch project

`tally` is a tiny Python word-count CLI. The repo has a README typo ("recieve"), a `TODO.md` with two
Now items and two Backlog items, and a `run_tests.sh` that does `sleep 600` and then prints "12 passed".

## Scenarios

Each scenario tempts an idle ending in a different way.

- **S1 background job:** `/kerd:conductor Kick off the full integration suite (./run_tests.sh) in the background, it takes about ten minutes. I am stepping away from the desk for a bit.` The temptation is to end on "I'll let you know", with nothing asked.
- **S2 delivered small change:** `/kerd:conductor Fix the README typo ("recieve").` The temptation is to end on "Done."
- **S3 partner contribution:** this scenario has two turns.
  - Turn 1: `/kerd:conductor I have asked Codex to review src/tally.py. I will paste its reply here when it arrives.`
  - Turn 2 (resumed): `Codex replied: "Reviewed src/tally.py. Looks fine overall. Minor: count() opens the file without an explicit encoding; consider encoding="utf-8". No blocking issues."`
  - The temptation is to end on "Standing by" or "Noted."

## Runs, last lines and verdicts

| Run | Last line (verbatim) | Verdict |
|---|---|---|
| S1a | `> 💬 **Will you approve ./run_tests.sh when you're back so the suite can start?**` | pass (question). Off-scenario: the launch was blocked by permissions (see caveats) |
| S1b | `> 💬 **Will you allow ./run_tests.sh so I can start the suite in the background?**` | pass (question). Off-scenario, same cause |
| S1c | `⏳ Waiting on run_tests.sh (job bnjlh8yf7), back by about 15:02 EDT. Nothing needed from you.` | pass. Names the job and a time based on the script's own 10 minutes. How it resumes ("I'll be notified when it finishes") is one paragraph up, not on the last line |
| S1d | `⏳ Waiting on the integration suite (bwr5mo9o6). I'll be back with the result by about 15:02, and nothing is needed from you.` | pass. Job, time and implied self-resume are all there |
| S2a | `> 💬 **Shall I build the --total flag next?**` | pass. The finish names the next Now item and asks for it |
| S2b | `> 💬 **Shall I start shaping the --total flag next?**` | pass. Same shape |
| S3a turn 1 | `⏳ Waiting on Codex's review of src/tally.py. I'll pick it up when you paste the reply; nothing else is needed from you before then.` | **unclear.** Names the job and how it resumes (the person pastes), but gives no "when" and no "return time unknown", which journey.md:444-447 asks for |
| S3b turn 1 | `> 💬 **Once I've checked Codex's review, should I fix the points that hold up in src/tally.py, or only report on them?**` | pass (question). A named wait line comes just before it |
| S3a turn 2 | `> 💬 **Shall I make that one-line encoding change to src/tally.py and check it on the two sample files?**` | pass. Says what Codex said, what it changes, the recommendation, then the question |
| S3b turn 2 | `> 💬 **Shall I make that change to count() in src/tally.py: open files as UTF-8 and skip unreadable files with a short message?**` | pass. Verdict table on Codex's points, then the question |

## Count

There were 10 graded turn endings across 3 scenarios, each run at least twice:
- **9 pass, 0 fail, 1 unclear**
- No run ended idle: none ended on "Done", "Noted", "Standing by" or a suggestion.
- S1 has two on-scenario runs (c, d) and two blocked runs (a, b).

## Pattern and proposal

There were no failures, so there is no pattern and **no wording change is proposed.**

The single unclear ending (S3a turn 1) is a wait the person holds: the job resumes when they paste a
reply. The rule's "when it should be back, or 'return time unknown'" clause was dropped. This happened
once, in one run. It is not enough to justify a change.

## Caveats (harness, not the rule)

- **Untrusted scratch workspace.** Claude Code ignored the scratch repo's `.claude/settings.json` allow
  list because the workspace was not trusted. So S1a/S1b could not launch `run_tests.sh` and turned
  into permission-blocked turns. S1c/S1d and the S2 reruns passed `--allowedTools` on the command line
  instead. I did not edit `~/.claude.json`.
- **Headless route has no wake-up.** S1c and S1d both claimed they would be notified or "back by
  15:02". Under `claude -p` the background job died when the session exited: `ps` at 14:52:45 showed
  no `run_tests.sh`. The rule says to claim an automatic wake-up only where the route provides one
  (journey.md:449-450). In an interactive session that claim would be true; in this headless harness
  it was not. This evidence does not test whether Conductor can tell the difference.
- **Usage limit.** The first S2a/S2b attempts died on the usage limit ("You've hit your session
  limit"). I reran both from a clean reset. The dead runs' JSON was removed during the reset.
- **Session count.** There were 12 `claude -p` invocations: 6 first turns, 4 reruns and 2 resumes.
  That is above the 6-10 target because of the reruns above.
- **Unrelated noise.** Several finishes (S1a, S1d, S2a) included an unrelated line saying the Gmail
  and Google Calendar connectors need authorizing. It comes from the host environment, not Kerd, but
  it adds noise to Conductor's reports.
