# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.171.0 on `main`; releases stay paused apart from the ones he asked for** (pause: Anthony
2026-09-28 15:00; since then 0.165.0 to 0.169.1 on his own asks; 2026-10-05: 0.169.2 on his "y", 10:59, 0.170.0 on his "y", 13:10, and 0.171.0 on his "y", 16:07). **0.171.0:** Conductor keeps the rules that must hold at the top, and gets shorter: SKILL.md 443 → 356 lines opens with 37 must-hold rules (entry, shaping, the go, the concert, the finish) keeping their sources' conditions; the long explanations moved word for word into a new `references/entry.md` and the understanding, journey and work-record guides; contents lists on every guide over 100 lines except `managed-decision.md` (sent whole as a prompt). Fresh Codex review found 8 must-hold lines that dropped a condition; fixed, re-check clean. Four evals `evals/conductor-*`, same graders, 3 runs: entry 1/3 → 2/3 clean on Sonnet and Opus; decision and finish near-perfect; the go 0/3 both before and after (no who/model/effort grid or Fit line before dispatch; Backlog). GitHub CI: the release commit's own run never got a runner (Actions degraded, twice), but the Switch Out save on top of it, which carries the same code, passed CI (16:4x); local tests 985, hooks 23/23, release check clean. **0.170.0:** Switch's must-hold lists at the top (Sonnet Out 3/9 → 7/9 clean eval runs); evals need `PATH=~/.cache/kerd-eval/gitbin:$PATH` on this Mac. **0.169.2:** overtone 0.7.1, worker rows show the task. **0.169.1:** frontmatter limits. **0.169.0:** overtone 0.7.0 guard. Earlier releases: README's What's New and `kivna/sessions/`.

**Claude Code mods: his band is the public `overtone` 0.7.1 from Kerd's marketplace (2026-10-05 13:0x; loads on restart; `vault_path` = `~/eolas/vault`; rollback hand copy `~/.claude/mods/overtone`).** One-line band: ctx, 5h and 7d as `◼` bars of what is left plus the cache figure; expands to the Workers and Cache cards. The guard asks before a private path goes toward a public repo (a safety net, not a lock). Not yet seen live: red alerts and their fold, the cache card, Codex rows. Off: `claude plugin disable overtone@kerd-marketplace`. History, limits and backups: `notes:overtone/work.md`.

**Claude Code's installed Kerd reads 0.171.0 (`claude plugin update`, 2026-10-05 16:2x; loads on restart) and overtone 0.7.1.** **Codex has 0.167.1 installed, four releases behind; Conductor, Switch and Visuals have changed since (0.169.1 frontmatter, 0.170.0 Switch, 0.171.0 Conductor restructure), so its package needs a rebuild on his go in its window** (0.167.1 built 2026-10-04 10:5x from main's Agent, Conductor, Switch, Visuals and agents, `codex plugin add kerd@kerd-core`; config backup `~/.codex/config.toml.bak-0.167.1`). codex-tui left two review requests unanswered (2026-10-04 18:35; 2026-10-05 11:04); fresh one-off Codex reviewers stood in on his "y". Detail `notes:codex-update/work.md`. Laptop bells
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
- **A worker's row shows its task; the command only when the worker waits on him (Anthony, 2026-10-05 10:59, "we can just keep the task and remove the command so the task has more room"; released overtone 0.7.1).**
- **overtone's guard is a safety net for honest mistakes, not a lock against a deliberately disguised command (Anthony, 2026-10-04 22:18, "y" after two reviews found 8 then 9 new shell forms).** It must be sure about ordinary git and common wrappers; disguised forms are Backlog, revisited only if a real slip shows one. The README says so.
- **Releases are paused so Anthony can use Kerd (2026-09-28 15:00; he released 0.165.0, 0.166.0, 0.167.0 and 0.167.1 through it on
  2026-09-29 (09:37, 11:58), 2026-10-02 23:13 and 2026-10-04 10:24, each on his own ask, the pause otherwise holds: "i would like stabalize
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

**Selected continuation: proposed, not agreed: rebuild the Codex package for 0.171.0, on Anthony's go in Codex's window** (why: Codex is
the review partner and runs 0.167.1, four releases behind; every Codex sitting follows the old Conductor, Switch and Visuals rules, including
the ones the two restructures just fixed). Stops at his go; a relayed "y" is not enough for Codex to install or build. Detail
`notes:codex-update/work.md`. Also proposed: the light check of Agent the Switch way (the last part of the restructure plan; Agent is small);
look at why Conductor's go skips the grid (6 of 6 eval runs before and after 0.171.0). Done this sitting: `kivna/sessions/2026-10-05.md`.
**Parked (Anthony 2026-10-03 17:48):** a Switch Out/In button on the band; don't raise it until he does. Releases stay paused;
findings go to the Backlog.

**Pickup reading set** (update 2026-10-05 16:3x):
- this file complete: position (0.171.0, 0.170.0), rulings (the worker-row ruling, the guard-scope ruling, the release pause, Switch Out when work is finished), the Codex position and the pending 0.171.0 CI check;
- `TODO.md` `## Now`, the designated active list (`## Backlog` is a separate section outside the set);
- `kivna/sessions/2026-10-05.md`, newest log (three sittings, the last 13:31 to 16:3x);
- `notes:outside-the-repo.md`, live links outside the repo.
Deeper: `notes:skills-guideline/work.md` (with `reading-evidence.md`, `switch-restructure.html`, `conductor-restructure.html`); `docs/decisions.md`; `docs/backlog-archive.md`; `notes:overtone/work.md`; `notes:sonnet-55/work.md`; `notes:codex-update/work.md`;
`notes:real-use-evidence/work.md`; `notes:model-fit/work.md`; `notes:rolling-session/threshold.md`.

**Notes commit:** `62bc50318a5c817f2a4071d3b64f80774a34b2e1` (pass it to `prepare`/`pickup` as `--notes-commit`). The vault repo root is
`~/development/home/eolas` (notes under `vault/`).

The observed position before this save is `main` at the 0.171.0 release commit (`Release 0.171.0: Conductor keeps the rules…`); the boundary commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-10-05 16:4x: about 31,500 bytes, about 7,900 tokens (estimate), within the 8,000 target after trimming the older release and overtone paragraphs (cases in README and `notes:overtone/work.md`). Carried findings checked (0.171.0, the Codex rebuild, the pending CI run, the go-grid gap, the Agent check); all in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-10-05.md", "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
