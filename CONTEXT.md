# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.167.0 on `main`; releases stay paused apart from three he asked for** (pause: Anthony
2026-09-28 15:00; 0.165.0 on his "lets just implement it", 2026-09-29 09:37; 0.166.0 on his "y", 11:58; 0.167.0 on his "y", 2026-10-02 23:13). **0.167.0:** Switch Out's closing box adds "Switch In will offer" (the recommended step plus up to two other open items, each with its reason, marked proposed), and Switch In's picker grows from exactly two choices to up to four with free text always open; a plain yes still means the recommendation and approves no operations; the bubble is unchanged. codex-tui reviewed the diff: consistent; its one finding (Switch description over 1,024 characters) fixed, now 997. 966 tests, hooks 23 of 23, release check clean. Not seen in a real sitting. **0.166.0:**
Claude Code's `sonnet` alias moved to Sonnet 5.5 on the Anthropic API (2026-09-28) and Kerd's Sonnet readers already
ran it (18 of 18 calls observed); new profile `anthropic/sonnet-5-5.md` (24 pending clauses: recalibrated effort,
medium default in Claude Code; early check-ins, unrequested files, self-started review rounds, done without a check),
a model-table row and per-provider alias note, and two lines in the five Sonnet agents (stop when done and checked; no
own review rounds or subagents unless asked). codex-tui two rounds, CLEAR. Sketchbook `notes:sonnet-55/work.md`.

**0.165.0:** Agent and Conductor say a Codex they start can't reach the network from its commands by default and offer
the person's own open `codex` session (Backlog row has the tests). Account: `kivna/sessions/2026-09-29.md`.

**Claude Code mods (shipped 2.1.287, 2026-10-01): `overtone` 0.2.0 is copied live and not yet seen on his screen (2026-10-03 09:00).**
Anthony asked what mods could do for Kerd; research, six ideas and the agreed picture are in `notes:overtone/` (`work.md`,
`ui-brief.md`, `ui-direction.png`, `evidence/`). 0.1.0 passed its live check 22:09 ("yes it works": `/overtone`, the `ctx` band).
He then removed the turn-end check and its toast and count ("pointless though, i can see its an or question"; "seems like a
waste"): nothing graded by counts any more. He asked to "up the game in Mod Ui" and "learn from the best examples"; three readers
studied Anthropic's and community mods; he liked the picture ("looks good"). His "y" (23:13) built 0.2.0 at `~/.claude/mods/overtone`
(his "yes" 08:59 to copying it live before Codex's re-check): ONE composed band above the prompt (context row always, dim when calm;
requested vs observed model row; workers rows only while workers run; width tiers; tmux first) and a **guard** that asks before Claude
stages, commits or pushes a private path toward a public repo ("Don't run it" default; no answer in 30 s, or dismissal, refuses; a bug in
the guard's own detection fails open). 114 of 114 `claude plugin test`, validate clean. codex-tui round one: 3 blockers in the guard
(push target, un-cancellable ask after timeout, next() replay) plus shell-expansion paths, all fixed; **round two (request
`0193c64b`) is sent and unanswered.** Known, unfixed: `git add -f .` can still stage an ignored `.env`; a timed-out dialog may stay on
screen (late answer ignored); the never-run-twice tests also pass on the old guard. Idea 6 (one-button Switch Out): probe says
"fill the prompt, he presses Enter" is feasible, not built, one-press submit left out. To turn the mod off delete the
`CLAUDE_CODE_PLUGIN_DIRS` line in `~/.claude/settings.json` (backup `settings.json.bak-overtone`); pre-0.2 copy at
`~/.claude/mods-work/overtone-live-pre-0.2`. The mods API is early; it broke other authors within days.

**Claude Code's installed Kerd read 0.166.0 at this Out (2026-10-03 09:00; 0.167.0 is on `main`, installed copy not updated or checked).** **Codex runs 0.164.0**; its package
carries Agent, Conductor and Switch, so **installing 0.167.0 in Codex is owed, on Anthony's go in its window.** Laptop bells
are on for both (backups `*.bak-bell`).

**Rolling by hand at ~200k tokens is on trial (Anthony, 2026-09-25); the 200k plan is parked (2026-09-27 13:20:
"lets keep that plan but park for now. i want more data first.").** The Studio status line (`~/.claude/statusline-command.sh`,
not Kerd) shows green `keep working`, yellow `switch at a break` (200k+ or 60%+), red `switch now` (80%+); he rolls by
hand at a break; Kerd's automatic chat roll stays at 50%. Three hand rolls judged, none with loss reported (2026-09-28
20:53 "n"). Don't build the plan until he asks. Readings, model and history: `notes:rolling-session/threshold.md`,
`notes:rolling-session/measure.py`.

**Tend's stale-hook check worked once** (0.151.1, one headless run; not verified).

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
- **Releases are paused so Anthony can use Kerd (2026-09-28 15:00; he released 0.165.0, 0.166.0 and 0.167.0 through it on
  2026-09-29 (09:37, 11:58) and 2026-10-02 23:13, each on his own ask, the pause otherwise holds: "i would like stabalize
  releases for a while and use it"; "yes but only if there is nothing left to fix").** The pause starts at 0.164.1, which fixed the one
  defect the 2026-09-28 apple-music re-grade found. While it holds: grades, findings and ideas go to the Backlog, not
  into releases; any fix found comes back to him for the release decision; he lifts the pause.
- **Switch Out previews what Switch In will offer, and Switch In offers Conductor start with up to four options (Anthony,
  2026-10-02 20:18; built and released as 0.167.0 on his "y" 23:13).** It replaces the "exactly two picker options, one
  recommendation" wording; Switch In still re-weighs every open item and the saved choices stay candidates; a plain yes still
  means the recommendation and approves no operations. Needs no mod. Case in `docs/decisions.md`.
- **Nothing is built to show him what he can already see on screen, and nothing is counted for its own sake (Anthony, 2026-10-02
  22:1x: "pointless though, i can see its an or question"; "seems like a waste").** The overtone turn-end check, its toast and its
  tally were removed; nothing graded by counts any more. He wants the mod UI to be good ("up the game"): quiet when fine, loud
  only when something needs him.
- **Mods are Claude Code only for now; Codex is looked at separately (Anthony, 2026-10-02 20:18).**
- **Batch the work; fewer approvals (Anthony, 2026-09-25 23:01; 2026-09-26 08:17, 08:49):** under a
  grant like "we have tokens to use, lets build with subagents in fan out where we can unattended and
  get fable to review", take several tasks per approval, dispatch independent work instead of
  waiting on one job, release on the standing go, and come back only for his decisions.
- **A question never loads its answer (Anthony, 2026-09-25 21:47 to 22:50; released 0.159.0):** a
  consequential question comes after a decision block (Problem, Facts with evidence strength, Known
  options, Recommendation, Why, Cost, What we lose, Input) and ends on the Recommendation sentence
  ending "— approve?" (his words, 22:50), every operation included, or one genuine question. Small
  or factual questions stay one line; Switch In's arrival question is exempt.
- **A public repo's working notes live in the private vault, saved like any record** (Anthony,
  2026-09-25 16:18 to 16:26: "we should for every project no? or we need a folder that is not
  public somehow"; "yes"). Kerd sets `work_notes: "vault"`; sketchbooks are `notes:<work>/`.
  Stage Kerd commits by name only: two slips today put private notes toward the public repo.
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
review and investigation** (cadence: checkpoints, before-push). It was off for the 0.159.0/0.160.0
build; Fable (a Claude subagent) reviewed instead on Anthony's word, six rounds, all findings fixed.
Codex came back 2026-09-26 08:49 and runs Kerd 0.162.0 since 12:4x.
A relayed "y" is not enough for Codex to install or build; the go must be his, in its window.

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

**Routing:** no role designation saved. The old `kerd-b5-review` binding still carries a pre-12:51
handoff from 2026-09-25; not adopted.

**Claude Code's Agent view stays on (Anthony, 2026-09-25 20:54):** `/exit` detaches into the
background-session list; he quits there with Ctrl-C. Switch Out's restart line says so (0.160.0).

**Selected continuation: none selected; proposed: Anthony's first look at `overtone` 0.2.0 in a fresh session** (the dim context row,
the model row, workers rows while workers run; the guard's "Don't run it" dialog when a private path is staged toward a public repo;
if nothing draws, read the dim line the transcript names). **Pending job:** codex-tui's round-two review of the guard, request
`0193c64b-14e7-4e27-9206-d095ef4eb45b`, submitted 2026-10-03 08:59, unconfirmed; round one took until morning and the system does not wake
a turn when it lands, so check it with `agent.py status` at the next Switch In. Fix any blocker before leaning on the guard. **Also
proposed, open: Codex installs 0.167.0, on Anthony's go in its window** (so the Codex side carries the network notice, the Sonnet 5.5
guidance and the new picker; install, then read back its skills against `main`). Also proposed, open: the first real check of the Sonnet 5.5
profile, a Sonnet grader at medium vs high on one grading job. Releases stay paused; findings go to the Backlog and a fix comes back to
him. Idea 6 (one-button Switch Out) is not agreed to build: the probe says "fill the prompt, he presses Enter" is feasible. Unseen in real
use: the four-choice picker and the "Switch In will offer" preview, push-first, unanswered-review, chat-roll restart. Still Backlog,
unfixed until seen: the Kerd Agent reply-ID risk. Parked: the 200k roll plan, the announcement, SAM and Aubel.app, the homepage, the
thrash guard. Dropped: launch step 2. Backlog also: Skriv voice-profile wiring, blocked on his samples.

**Pickup reading set** (update 2026-10-03 09:0x):
- this file complete: position, rulings (the release pause first), the proposed Codex install of 0.167.0;
- `TODO.md` `## Now`, the designated active list (`## Backlog` is a separate section outside the set; its rows are
  carried in this file);
- `kivna/sessions/2026-10-02.md`, newest log (two sittings: the research and the overtone 0.1 build, then the 0.2 build and 0.167.0 release);
- `notes:outside-the-repo.md`, live links outside the repo.
Deeper: `docs/decisions.md`; `notes:overtone/work.md` (+ `ui-brief.md`, `ui-direction.png`, `evidence/`); `notes:real-use-evidence/work.md`; `notes:model-fit/work.md`;
`notes:rolling-session/threshold.md`.

**Notes commit:** `690e9395604554944e291f932802e84190c8ffb1` (pass it to `prepare`/`pickup` as `--notes-commit`).

The observed position before this save is 0.166.0 on `main`; the boundary commit is this save itself.
Ask `git log` for its ID.

**Measured** 2026-10-03 09:0x: 39,655 bytes, about 9,914 tokens (estimate), **1,914 over the 8,000 target**, kept on purpose: the
log carries two sittings and this file carries the 0.167.0 release and the live mod. Not pruned again: `TODO.md` `## Now` (14,826 bytes)
still holds old "watch" rows that are open, not done (age alone closes nothing); the next Out should give each a verdict and move the
closed ones to `docs/backlog-archive.md`. All four carried findings are in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-10-02.md", "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
