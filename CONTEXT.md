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

**Claude Code mods (shipped 2.1.287, 2026-10-01): `overtone` 0.5.0 is live and his only usage display (2026-10-03 23:1x on Anthony's "y"; backup `~/.claude/mods-work/overtone-live-pre-0.5.0`; codex-tui three rounds, cleared; 270/270 against live; not yet seen in his terminal).** The one-line band is three colour bars of what is left (ctx, 5h, 7d) plus the cache figure; firing alerts fold to a red "⚠ N" when narrow; click or `ctrl+x b` expands it to the Workers, Context, 5-hour, Weekly and (when it fires) Cache cards. Claude gets the figures on every prompt (`usage:` line); nothing is written to disk. Claude Code draws its own `[-]` at the right of the band's first line; clicking it hides the band until `claude --resume`. The guard asks before a private path is staged, committed or pushed toward a public repo: public only when GitHub says so (`gh`; a private answer re-checked after 5 min; no answer in 5 s asks, and now says GitHub did not answer), the notes-folder rule only where `kivna/vault.json` sets vault notes, push-path reads fail closed. Not yet seen live: the bars in his terminal, red alerts and their fold, the cache card, Codex rows on real data. Old status line retired 2026-10-03 13:39 (scorched-earth's wrapper keeps only its burn light; backups `~/.claude/mods-work/statusline-retire-2026-10-03/`). Turn the mod off by deleting the `CLAUDE_CODE_PLUGIN_DIRS` line in `~/.claude/settings.json`. The mods API is early. History, pictures, accepted limits and backups: `notes:overtone/work.md`.

**Claude Code's installed Kerd reads 0.167.0 (installed_plugins.json, 2026-10-03 12:40).** **Codex has 0.167.0 installed** (2026-10-03 14:03, on Anthony's
"y" here, built and installed by Claude after his line never reached the Codex window: `output/kerd-codex-0.167.0`, `kerd-core`
repointed, `codex plugin list` reads 0.167.0; config backup `~/.codex/config.toml.bak-kerd-0.164.0`). The open codex-tui window
loads it only after he restarts it (`codex resume`); not yet seen loaded. Laptop bells
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
- **The one-line band is colour, not text: ctx, 5h and 7d as bars of what is left, coloured by the existing rules; figures live in the expanded band and Claude's usage line; cache stays a figure (Anthony, 2026-10-03 18:07: "we dont need the text, the color is enough"; live 0.5.0, 23:1x).**
- **A mod shows only figures that drive a decision for him or Claude (Anthony, 2026-10-03 11:53, "yeah agree"); nothing repeats
  what is already on screen (2026-10-03 10:55: "kinda pointless, already have this is status line below").**
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
- **When the agreed work is finished with nothing outstanding for Claude, Claude runs Switch Out itself, at any token count; never
  ask "Run Switch Out now?" (Anthony 2026-10-03 17:08 "y" past 200k; widened 17:49: "i thought you where going to do the switch
  outs?").** Narrows the next ruling.
- **Claude sees its own context token count, in every session; when to Switch Out stays his
  call (2026-09-24, 0.153.0; narrowed 2026-10-03, above).** Partly supersedes the 2026-09-15 context-pressure ruling.
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

**Selected continuation: none selected; proposed: Anthony looks at overtone 0.5.0's bars in a fresh session** (why: live since
23:1x but never seen in his terminal; an open session keeps the old band until it restarts; his reaction decides whether the bars
stay). Also proposed: Anthony restarts the codex-tui window (`codex resume`) so it loads Kerd 0.167.0 (why: installed 14:03, load
not confirmed); Anthony decides whether Sonnet readers move to medium (why: medium matched high at ~7% fewer tokens once; a release,
his call under the pause). Done this sitting (17:54 to 23:1x): the guard's 17:51 stop on the private vault was GitHub not answering in
time, not a misjudgement (same command passed 2.5 min later); fixed so a slow `gh` is not tried twice and the question says GitHub did
not answer; and the band became bars on his ask; both live as overtone 0.5.0. Detail `notes:overtone/work.md`. **Parked (Anthony
17:48):** a Switch Out/In button on the band; don't raise it until he does. Releases stay paused; findings go to the Backlog.

**Pickup reading set** (update 2026-10-03 23:2x):
- this file complete: position, rulings (the release pause first, then Switch Out when work is finished, then the band-as-bars ruling), the overtone and Codex positions;
- `TODO.md` `## Now`, the designated active list (`## Backlog` is a separate section outside the set);
- `kivna/sessions/2026-10-03.md`, newest log (four sittings);
- `notes:outside-the-repo.md`, live links outside the repo.
Deeper: `docs/decisions.md`; `docs/backlog-archive.md` (the pruned rows, verbatim); `notes:overtone/work.md`; `notes:sonnet-55/work.md`;
`notes:real-use-evidence/work.md`; `notes:model-fit/work.md`; `notes:rolling-session/threshold.md`.

**Notes commit:** `1be8c39f240049f7f3cc30b086123ece45baf008` (pass it to `prepare`/`pickup` as `--notes-commit`). The vault repo root is
`~/development/home/eolas` (notes under `vault/`).

The observed position before this save is `main` at the prune commit; the boundary commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-10-03 23:2x: 32,884 bytes, about 8,221 tokens (estimate), 221 over the 8,000 target: the newest log holds five sittings (10.3k bytes) and the overtone paragraph was cut by a third this sitting; kept rather than drop active context. All five carried findings are in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-10-03.md", "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
