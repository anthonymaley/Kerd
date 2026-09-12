# Fable review of the candidate skills at 0.110.0 — 2026-09-11

Read-only review by a Fable subagent dispatched from the Kerd session, brief:
Conductor, Switch, Visuals and Agent as shipped at `ea4778f`, with particular
care for the 0.110.0 Switch In change (Conductor opens after the dashboard and
stops on one approval line) and the prior Agent dispositions at
[the Agent work record](../../agent-connection/work.md). Findings are the
reviewer's, verbatim; dispositions are recorded below the report when made.

## Test suites, as run by the reviewer

| Suite | Result |
|---|---|
| Switch (`skills/switch/scripts`) | 276 tests, OK |
| Conductor (`skills/conductor/scripts`) | 37 tests, OK |
| Agent (`skills/agent/scripts`) | 110 tests, OK |
| Release gate | clean |

## Findings, most severe first

1. **CONTRADICTION** — `README.md:540,544` "How They Fit Together" still describes the pre-0.107 In loop: three fixed files, "offers to start a conductor session", Conductor close-out running the boundary and offering `/clear`. Conductor has no close-out (grep). Minimal change: rewrite the two paragraphs to the 0.110.0 flow.
2. **OVERCLAIM** — `README.md:407` says Conductor's close-out fires Slainte at a version bump or acceptance record; nothing in `skills/conductor/` names slainte. Product decision: document on-demand, or add the pass to `execution.md` "Finish the outcome".
3. **CONTRADICTION** — shipped Conductor and Switch still call themselves "development candidate" and say "Do not invoke installed Conductor/Switch" (`conductor/SKILL.md:6,20-22,226`; `switch/SKILL.md:6,9-10`; `visuals/references/sources.md:34-37`), while `in-out.md:102-103` loads the installed Conductor. Drop the candidate/trial wording.
4. **STALE REFERENCE** — `conductor/references/execution.md:39`, `model-jobs.md:16,87` link `../../../guidance/…`, absent from the checkout and every cached version. Material lives at `docs/work/model-ready-work/guidance/`; only Agent knows that. Repoint or move under `skills/conductor/references/`.
5. **CONTRADICTION** — In stop: "X is the saved next action or the first NOW item" vs "if no task is selected, say so rather than choosing one" (`conductor/SKILL.md:36-40`, `in-out.md:68-69,115-119`). Kerd's own TODO is task-null with NOW bullets. State precedence once.
6. **CONTRADICTION** — the "new window grants no new authority" reason for the In stop (`conductor/SKILL.md:40-42`, README:53-55) conflicts with "don't require a second yes" (`conductor/SKILL.md:146-148`, `execution.md:5-6`, `journey.md:22,201`). Give the real reason (a check-in on arrival) and name the one exception in those places.
7. **STALE REFERENCE / CONTRACT GAP** — `conductor/SKILL.md:70-71` looks for `docs/work/SESSION.md`, which Switch never writes. Replace with the project's current-context pointer.
8. **REPRODUCED DEFECT** — `where_we_are.py:527`: a string `now` renders one bullet per character. Wrap a string as a one-item list; add a test.
9. **STALE REFERENCE** — `switch/SKILL.md:59-60` lists four dashboard blocks; the guide has five. Add "Now".
10. **CONTRADICTION** — three names for the closing link: "Open work" (README:61,356), "View tasks and details" (`in-out.md:138`), "Tasks" (example). Pick one.
11. **REPRODUCED DEFECT** — `agent.py status/wait <unknown id>` creates an empty `.lock` in `.git/kerd-agent/requests/` before checking the record exists (`agent.py:119-120,692`); error reads as errno. Check existence first; add a test.
12. **REPRODUCED DEFECT (low)** — `handoff.py prepare --section` on a heading with trailing spaces says "must occur exactly once" (`handoff.py:202,211` strip only `\r\n`). `rstrip()` or fix the message.
13. **STALE REFERENCE** — Agent's discovery scope text predates 0.109.0 (`agent.py:480`, `user-guide.md:152-153`); the store scan is live. Also `docs/work/agent-connection/work.md:275-293` "## Now" still says "hand the integrated 0.108.0 release".
14. **OVERCLAIM (minor)** — `README.md:47-49` says 0.108.0 left you to ask for Conductor; 0.108.0 loaded it. Say "ask for the work".
15. **CLARITY** — the In rule lives in four places with drift (`switch/SKILL.md:63-69`, `in-out.md:100-122`, `conductor/SKILL.md:31-43`, `journey.md:29-37`). Keep the full rule in Conductor's SKILL.md; the others refer to it.

Nothing to report: bare slash references, dead links other than finding 4, `codex queue --cd` (verified against codex-cli 0.154.0), the Visuals 900px claim.

Coverage gaps: string `now` (8); store untouched after failed lookup (11); the In → Conductor handover itself is prose-only and no real 0.110.0 pickup is recorded — "added but not yet verified".

Prior Agent dispositions: none looked wrong against the code.

## What the reviewer did not review

Roll/managed-To helpers and `ask.py` beyond their suites (live runs cost paid work); Agent `start`/`ask`/`pair` success paths; the Visuals asset's rendered appearance; the other eight skills except where README claims intersected. Noted in passing: `CONTEXT.md:5` still says "ten workflow skills".

## Dispositions — 0.110.1, same day

All fifteen acted on in the 0.110.1 release; the branch and record name the
boundary, `git log` supplies the commit.

- 1, 14: README "How They Fit Together" and the 0.110.0 note rewritten to the
  current flow. **Fixed.**
- 2: corrected, not built — README now says `/kerd:slainte release` runs on
  demand and Conductor does not trigger it. The hook remains an open product
  choice, recorded as a named loss in the 0.110.1 note. **Corrected.**
- 3: "development candidate" headers, "do not invoke installed Conductor/Switch",
  "this trial" and the Visuals sources note removed across Conductor, Switch,
  Visuals and their references. **Fixed.**
- 4: `guidance/` moved to `skills/conductor/references/guidance/` (git mv, ten
  files) so it ships; Conductor and Agent links repointed. Dated session logs
  keep the old path as history. **Fixed.**
- 5: precedence stated once in Conductor's SKILL.md: saved next action, then
  first NOW item, then "no task selected". **Fixed.**
- 6: reason restated as a deliberate check-in on arrival; the one-exception
  clause added at `conductor/SKILL.md` (second yes), `execution.md` (ask once),
  `journey.md` (no extra continue; never a reason to end the turn). **Fixed.**
- 7: `docs/work/SESSION.md` replaced by the project's current-context pointer.
  **Fixed.**
- 8: string `now` wrapped as one item; test added. **Fixed, tested.**
- 9: "Now" added to Switch's block list. **Fixed.**
- 10: label is *Open work* in README, the guide and the example. **Fixed.**
- 11: `status` checks the record exists before taking the lock and says
  "No request <id> in this project"; test asserts the store is untouched.
  `wait` goes through `status`, so it is covered. **Fixed, tested.**
- 12: heading match ignores trailing whitespace; test added. **Fixed, tested.**
- 13: scope text in `agent.py`, the user guide and the Agent work record's
  `## Now` updated. **Fixed.**
- 15: full In rule lives in Conductor's SKILL.md; Switch SKILL.md, in-out.md
  and journey.md refer to it. **Fixed.**
- Aside: `CONTEXT.md:5` now says twelve skills.

Suites after the fixes: Switch 278, Conductor 37, Agent 111, all OK; release
gate clean; every relative link in `skills/` and README resolves (scripted
check). The In → Conductor handover itself is still prose-only and unproven in
a real pickup on this release.
