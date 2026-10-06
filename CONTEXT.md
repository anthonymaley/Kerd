# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.172.0 on `main`; releases stay paused apart from the ones he asked for** (pause: Anthony
2026-09-28 15:00; since then 0.165.0 to 0.169.1 on his own asks; 2026-10-05: 0.169.2 on his "y", 10:59, 0.170.0 on his "y", 13:10, and 0.171.0 on his "y", 16:07; 0.171.1 on his "y", 19:12; 0.172.0 on his "y", 22:54). **0.172.0:** Conductor's Ready decision block carries the who/model/effort grid with a Fit line per job, so the go approves staffing he has seen; the go dispatches as shown and a changed row is shown again first. New eval `evals/conductor-ready`: clean Opus 1/3 → 3/3 (shell and edits allowed); a fresh Codex review found 4 blockers (dropped controller row and repeated Fit line in the must-hold line; loose graders), fixed, re-run 3/3 grid; not re-reviewed after the fixes; Sonnet not measured cleanly; CI green, his install updated (loads on restart). Trial and review about $11. **0.171.1:** Agent keeps its rules that must hold at the top: the closing never-do paragraphs open a Must hold section word for word, the role-and-cadence question moved word for word to the user guide, contents lists on its three guides; SKILL.md 185 → 157 lines, line diff 0 missing, 985 tests, CI green (19:1x); no evals (no real-use failure behind it). The restructure plan (Switch, Conductor, Agent) is complete. **0.171.0:** Conductor's must-hold rules at the top, SKILL.md 443 → 356 lines, explanations moved word for word into guides; evals: entry 1/3 → 2/3 clean, the go 0/3 before and after (no grid or Fit line before dispatch; Backlog); CI passed on the save commit 6bce325 (the release commit's own runs never got a runner). **0.170.0:** Switch's must-hold lists at the top (Sonnet Out 3/9 → 7/9 clean eval runs); evals need `PATH=~/.cache/kerd-eval/gitbin:$PATH` on this Mac. **0.169.2:** overtone 0.7.1, worker rows show the task. **0.169.1:** frontmatter limits. **0.169.0:** overtone 0.7.0 guard. Earlier releases: README's What's New and `kivna/sessions/`.

**Claude Code mods: his band is the public `overtone` 0.7.1 from Kerd's marketplace (2026-10-05 13:0x; loads on restart; `vault_path` = `~/eolas/vault`; rollback hand copy `~/.claude/mods/overtone`).** One-line band: ctx, 5h and 7d as `◼` bars of what is left plus the cache figure; expands to the Workers and Cache cards. The guard asks before a private path goes toward a public repo (a safety net, not a lock). Not yet seen live: red alerts and their fold, the cache card, Codex rows. Off: `claude plugin disable overtone@kerd-marketplace`. History, limits and backups: `notes:overtone/work.md`.

**Claude Code's installed Kerd reads 0.172.0 (`claude plugin update`, 2026-10-05 23:0x; loads on restart) and overtone 0.7.1.** **Codex has 0.172.0 installed (2026-10-06 08:2x, on his "y": Claude built `output/kerd-codex-0.172.0` from the 0.171.1 package plus Conductor's two changed files, repointed `kerd-core`, `codex plugin add`; read back: `codex plugin list` 0.172.0, cache skills and agents identical to main; config backup `~/.codex/config.toml.bak-0.172.0`, 0.171.1 package kept for rollback). Both hosts on 0.172.0. The open codex-tui loads it only after Anthony restarts it (`codex resume`).** codex-tui left two review requests unanswered (2026-10-04 18:35; 2026-10-05 11:04); fresh one-off Codex reviewers stood in on his "y". Detail `notes:codex-update/work.md`. Laptop bells
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
handoff from 2026-09-25; not adopted. Anthony confirmed (2026-10-05 22:14) the bound codex-tui thread is the one to keep using; the session ID he first gave was a closed Codex voice session that Agent refused. That thread was last written 21:15, before the 21:3x install, so it probably still runs the older Kerd (inference, not checked).

**Claude Code's Agent view stays on (Anthony, 2026-09-25 20:54):** `/exit` detaches into the
background-session list; he quits there with Ctrl-C. Switch Out's restart line says so (0.160.0).

**Eval leftovers cleared (Anthony 2026-10-06 08:41, "y"):** 400 sealed `/private/tmp/e-*` folders (513 MB measured with `sudo du`; the earlier "26 GB" was all of /private/tmp, mostly Claude Code scratch and another project's `dd-*` builds) and the `Kerd-switch-baseline` worktree (its 119 untracked eval files byte-identical to main) removed; `~/.cache/kerd-eval/gitbin` kept for future evals. 

**Selected continuation: proposed, not agreed: Anthony restarts codex-tui** (`codex resume`) so the review partner loads 0.172.0 (why: it was resumed 2026-10-05 21:15, before the 0.171.1 and 0.172.0 installs, so the next review would likely run an older Kerd; inference from thread write time, not checked). His action; Claude does nothing until he says it is done; stops there. Also proposed: watching the Ready grid on the first real Conductor go (the only way to see whether the go dispatches as shown); the one-line fix so Switch Out ends on its box (Backlog; a release, so his decision while releases are paused).
Done this sitting: `kivna/sessions/2026-10-06.md`.
**Parked (Anthony 2026-10-03 17:48):** a Switch Out/In button on the band; don't raise it until he does. Releases stay paused;
findings go to the Backlog.

**Pickup reading set** (update 2026-10-06 09:1x):
- this file complete: position (0.172.0 on both hosts, 0.171.1, 0.171.0, 0.170.0), rulings (the worker-row ruling, the guard-scope ruling, the release pause, Switch Out when work is finished) and the Codex position;
- `TODO.md` `## Now`, the designated active list (`## Backlog` is a separate section outside the set);
- `kivna/sessions/2026-10-06.md`, newest log (two sittings, 08:16 to 09:1x);
- `notes:outside-the-repo.md`, live links outside the repo.
Deeper: `notes:skills-guideline/work.md` (with `ready-grid.html`, `reading-evidence.md`); `docs/decisions.md`; `docs/backlog-archive.md`; `notes:overtone/work.md`; `notes:sonnet-55/work.md`; `notes:codex-update/work.md`;
`notes:real-use-evidence/work.md`; `notes:model-fit/work.md`; `notes:rolling-session/threshold.md`.

**Notes commit:** `723ddff3969e157e32eda4dcb59e4119e3a70aa6` (pass it to `prepare`/`pickup` as `--notes-commit`). The vault repo root is
`~/development/home/eolas` (notes under `vault/`). The vault also holds apple-music's uncommitted notes from another project's sitting; they are not Kerd's and were not saved.

The observed position before this save is `main` at the eval-leftovers record commit; the boundary commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-10-06 09:1x: 27,855 bytes, about 6,964 tokens (estimate), within the 8,000 target. Carried findings checked (restarting codex-tui, the Ready grid watch, the release pause, the notes commit, the 513 MB correction); all in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-10-06.md", "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
