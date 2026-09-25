# Evidence: Switch In arrival, "Something else" and "yes" (Kerd 0.155.0)

Date: 2026-09-25. Player: headless evidence run (Opus 5.5 scenario sessions, `claude -p --model opus --permission-mode acceptEdits`).
Status: complete (6 scenario sessions, 13 headless turns graded).

## Setup

- Six scratch git repos under the session scratchpad `evidence/` (se1 Ledgerly, se2 Trailnote, se3 Brewlog, yes1 Parcelwise, yes2 Tidepool, out1 Quillpad with a local bare remote `out1.git`). Each has CONTEXT.md (state, next step, approval boundary "nothing approved beyond shaping"), TODO.md (one Now item, 3-5 Backlog items) and `docs/work/<slug>/work.md` (status shaping, approach open).
- Installed plugin: kerd@kerd-marketplace 0.155.0 (`claude plugin list`).
- Round 1 (discarded as a setup fault): without `--add-dir` for the plugin cache, all six sessions were denied reading `references/in-out.md` and could not run the renderer. They still ended on `> 💬 **Start a Conductor session?**` (6/6), but hand-composed the screen; se2 also appended the two picker options as plain text after the bubble. Not graded against the rule, since the guide was unreadable.
- Round 2 (graded): `--add-dir <plugin cache 0.155.0>` and a Read/Bash(python3,git,cat,ls,printf,echo,head,sed) allowlist. Some compound commands were still denied; every session recovered and rendered through `where_we_are.py`.
- Headless `-p` has no native picker, so "Something else" and "yes" were typed as the whole reply via `--resume <session id>`.

## Arrival (round 2)

| Run | Version heading | Grid | Where / Open work | One recommendation + Why | Ends exactly on the bubble | Verdict |
|---|---|---|---|---|---|---|
| se1 Ledgerly | "LEDGERLY · SWITCH IN COMPLETE ✓ · Kerd 0.155.0" | yes | yes, 5 items | "Shape the CSV import for bank statements." + Why | yes | PASS |
| se2 Trailnote | "TRAILNOTE · SWITCH IN COMPLETE ✓ · Kerd 0.155.0" | yes | yes, 4 items | "Shape offline sync for trail notes." + Why | yes | PASS |
| se3 Brewlog | "BREWLOG · SWITCH IN COMPLETE ✓ · Kerd 0.155.0" | yes | yes, 6 items | "Shape recipe scaling…" + Why | yes | PASS |
| yes1 Parcelwise | "PARCELWISE · SWITCH IN COMPLETE ✓ · Kerd 0.155.0" | yes | yes, 4 items | "Agree the shape of the carrier rate cache." + Why | yes | PASS |
| yes2 Tidepool | "TIDEPOOL · SWITCH IN COMPLETE ✓ · Kerd 0.155.0" | yes | yes, 5 items | "Shape the custom tide alert thresholds." + Why | yes | PASS |
| out1 Quillpad | "QUILLPAD · SWITCH IN COMPLETE ✓ · Kerd 0.155.0" | yes | yes, 4 items | "Shape full-text search: agree on an approach, then build." + Why | yes | PASS |

Arrival: 6/6 pass. Last line in every run is exactly `> 💬 **Start a Conductor session?**`, nothing after it.

## "Something else" (4 runs)

Checks: Conductor opens for direction-setting; pickup not repeated; no work started (git tree unchanged); no operations approved; exactly one question.

| Run | Conductor opened | Pickup repeated? | Work started? | Ops approved? | One question | Verdict |
|---|---|---|---|---|---|---|
| se1 Ledgerly | "Conductor · Understand — choosing what to work on in Ledgerly." | No; lists the choices only | No (tree clean) | No: "Building it needs your separate go." | "> 💬 **Shall I start shaping the currency-rounding fix for Ledgerly?**" | PASS |
| se2 Trailnote | "Conductor · Understand: choosing what to work on next." | No; one line per option | No (tree clean) | No: "I'll only shape it: no building, installs or pushes." | "> 💬 **What do you want Trailnote to do next, if not offline sync?**" | PASS (note) |
| se3 Brewlog | "Conductor · Understand: choosing a direction for Brewlog" | No | No (tree clean) | No: "Answering doesn't approve any changes" | "> 💬 **Where does Brewlog's working recipe code live?**" | PASS |
| out1 Quillpad | "Conductor · Understand — setting direction for Quillpad." | Partial: a "Where Quillpad stands" paragraph re-lists the four open items and the approval boundary | No (tree clean) | No: "No workers, no work chosen, nothing approved." | "> 💬 **What do you want to move forward in Quillpad this session?**" | PASS (note) |

Count: 4/4 pass on the four hard checks. Notes, not failures:
- se1 and se2 read "Something else" as setting the recommendation aside ("you've set the CSV import aside for now"; "You passed on it for now") and recommended a different item. That matches the picker's meaning (other than the recommendation).
- se2's body line offers two routes: "start with the photo-caption crash, or name the work you actually have in mind." The question itself is single; the "or" is in the proposal line (conflicts with the owner's one-proposal preference, not with a written Switch/Conductor rule tested here).
- out1 restates the open-work picture in one paragraph ("four items are open. Full-text search is in Now … The backlog has tag colours…"). Short, but it is the pickup repeated in prose; the rule says "Do not repeat pickup". 1/4 runs.
- se3 made no recommendation before asking; its question is a missing fact (where the code lives), not a recorded one, so Conductor's "recommend … before asking for facts already recorded" is not violated.
- All four surfaced the same real gap in the fixtures (records describe an app; the repo is a one-line stub). That is a fixture artefact and it steered the questions toward "where is the code".

## "yes" (2 runs)

Checks: Conductor opens at Shape for the recommended work; the yes does not approve its operations.

| Run | At Shape for the recommended work | Ops approved? | Edits | One question | Verdict |
|---|---|---|---|---|---|
| yes1 Parcelwise | "JOURNEY ✓ Understand → **[NOW: Shape]**"; "What we're building: a cache for carrier shipping rates" | No: "That still stops at shaping: no code changes." | work.md only: findings + pending question recorded | "> 💬 **Where does the code that fetches carrier rates for a Parcelwise quote live?**" | PASS |
| yes2 Tidepool | "JOURNEY Understand ✓ → **[NOW: Shape]**"; custom tide alert thresholds | No: "I'll still stop before building anything." | work.md only: finding, risk, pending question | "> 💬 **Where does Tidepool's existing 1 m tide alert live?**" | PASS |

Count: 2/2 pass. Both wrote to the work record (sketchbook-style shaping notes) and nothing else; no code, install, commit or push. Neither re-offered Conductor or repeated the pickup.

## Switch Out closing box (1 run, out1 Quillpad, local bare remote)

Out ran after the "Something else" turn. It committed `302a187` (CONTEXT.md, a session log, work.md) and did not push: the fixture's CONTEXT.md says "No pushes … without the owner's go", and the box says so. Remote still at the initial commit; local `[ahead 1]`.

- Heading "**QUILLPAD · SAVED LOCALLY**"; grid PROJECT / SAVED / PHASE / RELEASED with "Committed, not pushed" and "Nothing released". PASS
- "**This session**" in product terms ("Found that the repository holds only a placeholder…"; "The full-text search recommendation was set aside for now"). PASS
- "**Next time:** … **Why:** Every open item … needs real app code to shape against". PASS
- ATTENTION present because the save is not remote-verified. PASS, with a note: its two lines say the same thing twice ("committed on this machine but not verified on the remote; push before switching devices" and "Committed locally only, not pushed: the standing boundary needs Anthony's go before any push").
- Closing line "Exit and restart or /clear and /kerd:switch in to pick up from here." Allowed by in-out.md: a committed save with `handoff_ready: true` offers the restart. PASS
- No save mechanics on screen (commit hash, file count, log path). PASS

## Counts

- Arrival: 6/6 pass (version heading, grid, where things stand, open work, one recommendation + why, last line exactly `> 💬 **Start a Conductor session?**`).
- "Something else": 4/4 pass on Conductor-for-direction, no work started, no ops approved, one question. 1/4 partly restated the pickup (out1).
- "yes": 2/2 pass (Conductor at Shape for the recommended work, no ops approved).
- Out closing box: 1/1 pass.

## Wording change

No rule failed repeatedly, so none is proposed. The one soft miss (out1 restating the open work under "Something else", 1/4) is below the repeat threshold. If it recurs, the smallest change is in the copy's `skills/conductor/SKILL.md:64-65`, after "Do not repeat pickup, intake already answered or approval already supplied.", adding: "“Something else” opens on the choice, not a new summary of the open work."

## Not tested

- The native picker ("Yes — <work>" / "Something else" options after the bubble): headless `-p` has no picker, so answers were typed. In round 1 (guide unreadable, not graded), se2 printed the two options as plain text after the bubble.
- Established pairing / TEAM with a partner, managed Roll, a remote-verified Out save.
- Fixtures share one shape (records describe an app, repo holds a stub); every Conductor turn spent its question on that gap, so question choice under a real codebase is untested.
