# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.154.1 on `main`** (2026-09-25 08:4x). The sitting of 2026-09-24 21:00 to
2026-09-25 08:46 released 0.153.3 (finished Roll records retire under the owner lock, with
`roll_retire.py`), 0.154.0 (Conductor rolls its own Claude chat in tmux) and 0.154.1 (that roll
works for sessions started `Claude --dangerously-skip-permissions`). Two real rolls worked
(08:04 plain `claude`; 08:44 with the skip flag): the pane restarted on the same model, effort
and permission mode and the new session did its saved next step. Before that, 2026-09-24:
0.153.0 to 0.153.2 (the context hook and its wording), 0.152.0, 0.151.x.

**Both hosts run 0.154.1:** Claude Code (`claude plugin update`, 2026-09-25 08:4x) and Codex
(built and installed by `codex-tui` on Anthony's go in its window, read back by Claude
2026-09-25 09:41). The chat roll itself is Claude-only.

**Rolling by hand at ~200k tokens is on trial (Anthony, 2026-09-25 10:26 to 10:30).** He found
the built alternative (a 200k trigger, a thrash guard and a backstop, checked by a composer and
Codex) too complex, and chose instead: the Studio status line
(`~/.claude/statusline-command.sh`, not Kerd) shows tokens used and a coloured state, green
`keep working` (under 200k and under 60% used), yellow `switch at a break` (200k+ or 60%+), red
`switch now` (80%+); he rolls by hand at a break. Kerd's automatic chat roll stays at 50%. The
test, his ask: track Switch Out across sittings to see whether the numbers and the benefit hold.
`notes:rolling-session/measure.py` prints per-sitting calls, start, peak, average
tokens re-sent per call and the size at Switch Out; baseline since 2026-09-21: averages 116k to
286k per call, peaks up to 459k, Outs at 133k to 433k. This sitting (2026-09-25 08:49 to 10:3x)
is the first rolled at the mark (~207k). Estimate, not proof: rolling near 200k should keep the
average near 190k; the model and both checks are in `notes:rolling-session/threshold.md`.

**Tend's stale-hook check works in one real run** (0.151.1, 12:58): a headless Tend in a
scratch repo flagged a settings entry with the literal placeholder, kept an unrelated hook and
changed nothing. One observation, not verified.

**Kerd has an accepted launch plan** (`docs/design/launch-plan.md`). Ready to launch when
someone other than Anthony carries a real piece of work, in their own repository, to its
agreed result, unaided. **Step 1: 3of3 is using Kerd in its own sessions; Kerd evidence is
read from those sittings when Anthony asks for it.** 3of3's work (its iCloud sync, its devices)
is 3of3's, never Kerd's open work or next step (Anthony, 2026-09-25 10:49: "we are mixing work";
he had said the same 2026-09-23). Evidence so far: local sketchbook `notes:launch-plan/work.md`.

**The homepage redesign was tried and dropped (Anthony, 12:56: "nah dont like it - lets drop
it"; "will revisit").** Codex built three passes on his direct ask; his reactions and the
dropped pass are in the local sketchbook `notes:homepage-redesign/work.md`. `site/` is
unchanged. When revisited, start from what would make it feel serious rather than AI-made to
him, not from another pick of direction.

**Two teams already use Kerd** (Anthony, 2026-09-22): SAM and Aubel.app. The team note
(`notes:launch-plan/team-note.md`) had his "y" to send (2026-09-23 17:05); not confirmed
sent. **Parked (Anthony, 2026-09-24 08:55): "delay any sam and auble work for now";** don't
raise it until he does.

**Launch step 2, inviting three to five people, is dropped (Anthony, 2026-09-25 11:16: "i dont.
drop this").** Don't raise it or recommend it again unless he does.

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **Conductor rolls its own Claude chat in tmux, never the person (2026-09-24/25, 0.154.0–1):**
  past 50% of the declared window at a safe boundary it saves, tmux restarts its pane into a
  fresh `claude` on the same model, effort and permission mode, and `/kerd:switch roll in`
  picks up. Nothing is typed into Claude; no Stop hook; outside tmux, one line to run.
- **Claude sees its own context token count, in every session; when to Switch Out stays his
  call (2026-09-24, 0.153.0).** Partly supersedes the 2026-09-15 context-pressure ruling.
- **Conductor runs on Opus 5.5, at medium by default, set up from Anthropic's guidance
  (2026-09-24, 0.152.0);** Kerd advises the session setup, never changes the session itself.
- **The explanatory and learning output styles are off on this machine (2026-09-24).**
- **Conductor builds with its own host's workers and the other provider reviews; a
  cross-provider builder is an exception the person asks for or approves, with a reason,
  called a trial without a comparison (2026-09-24, 0.151.0).** Codex building the homepage
  on Anthony's direct ask was his change of ownership, not a Conductor dispatch.
- **The 2026-09-13 "prove Kerd first" hold is lifted (2026-09-23);** lifting it invites
  nobody and announces nothing.
- **A review the partner leaves unanswered gets a fresh one-off reviewer on his yes, never
  a recommended waiver (2026-09-23).**
- **Dispatch agents are named for the model and the effort (2026-09-23).**
- **Read-only reads of his own projects need no question first (2026-09-23).** Writes,
  builds, installs, pushes and device actions still need their go.
- **Keep moving; never sit idle (2026-09-22).** Carry on towards the goal, or stop on a
  reason he can engage with.
- **A launch plan exists and is accepted (2026-09-22);** its open decisions are his.
- **Kerd's readers are on desktops and laptops (2026-09-21).**
- **A page correction ships without a bump when the installed plugin is byte-identical
  (2026-09-21);** a change to what installs gets its own version and note (2026-09-20).
- **The Kerd look (`site/DESIGN.md`) is the only diagram theme on this machine (2026-09-21).**
- **The site is published on Vercel from the repository root (2026-09-21).**
- **The ladder and the tiered risk ledger are retired (2026-09-19).**
- **What is published is the product, not how it was made.** Sketchbooks stay local.
- **The release history stays in the README;** `CHANGELOG.md` carries a copy.
- **Every report has one shape. At the end of a build, bring one decision.**
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a score
and a goal; always be delivering; Conductor owns the sketchbook; rolling is per batch.

**Not yet ruled, and it is Anthony's:** where and when to announce, and what would make the
homepage feel serious to him.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push). This sitting it reviewed the
chat-roll spec and the build over five rounds plus 0.154.1 twice (every finding fixed; last:
clear). A Claude session in the Codex window ran terminal probes on Anthony's ask (tmux and
iTerm2, synthetic); two empty iTerm2 test windows it opened may still be on the Studio's display.
A relayed "y" is not enough for Codex to install or build; the go must be
his, in its window. No job is running.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds
Anthony's TypeSafe key and is git-ignored; never print or commit it, and never serve the
repository root over the network (a preview briefly did on 2026-09-24 11:21; its log shows no
request for `.env`; previews now serve `site/` only).

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); `docs/guide/reference-from-readme.md` (2026-09-19);
`docs/work/jev-trial/review_results.json` (2026-09-22). They exist on the Mac Studio only.

**Working notes live in the private vault** (0.157.0, 2026-09-25): `kivna/vault.json` sets
`"work_notes": "vault"`, so sketchbooks are `notes:<work>/work.md` under
`~/eolas/vault/kerd/work/` (private repo `anthonymaley/eolas`). The 18 folders that were
local-only here moved there on 2026-09-25 (vault commit `b64d50a`). `notes:backlog-sweep/` and
`notes:unattended-sweep/` were pushed to this public repo by mistake in 0.155.0/0.156.0 and
untracked the same day; the old commits still hold them.

**Routing:** the Claude role `kerd-b5-review` was adopted at the 2026-09-25 08:5x arrival
against the saved designation; it designates its successor at this Out.

**Selected continuation: none saved.** The 3of3 sync evidence line was withdrawn as Kerd's
next step (Anthony, 2026-09-25 10:49). Dropped: step 2 (11:16). Parked: the announcement, SAM and Aubel.app,
the homepage.

**Pickup reading set** (Switch Out, 2026-09-25 10:3x):
- this file complete: position, rulings, the continuation, the roll trial;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-25.md`, both of today's sittings (releases to 08:5x; then Codex,
  audits, tests and the roll trial to 10:3x).
Deeper: `docs/decisions.md` (the chat-roll case); `docs/design/launch-plan.md`; local
sketchbooks `notes:rolling-session/threshold.md` (the roll trial, cost model, both checks),
`notes:rolling-session/work.md` (the chat roll), `notes:launch-plan/work.md`.
At the next In, run `python3 ~/eolas/vault/kerd/work/rolling-session/measure.py --since 2026-09-25` to add the
sitting that just ended to the trial's evidence.

The observed position before this save is 0.154.1 on `main`; the boundary commit is this save
itself. Ask `git log` for its ID.

**Measured** 2026-09-25 10:3x: 28,626 bytes across the three sources, about 7,157 tokens
estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-25.md",
 "--section", "TODO.md", "## Now"]
```
