# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Position (2026-10-13):** Kerd 0.183.2 (overtone 0.10.0) is released on `main` (d6bfd6ae, CI 38405904537 green) and installed in Claude Code (0.183.2, loads on restart). 0.183.2: Slainte's trigger description and five guide/playbook/state-contract lines no longer say anything runs its release pass, nor name the retired acceptance-record trigger (`notes:homepage-redesign/work.md`). The public `codex` branch reads 0.183.1 (49cc7dab); his Codex is on 0.183.1 too, which is current for its package (Slainte is not in it) (its plugin cache holds only 0.183.1, written 2026-10-12 10:12, plugin enabled; seen 10:18, not checked inside a Codex turn). 0.183.1: a wait line's meanwhile clause is never replaced by "then <next step>", even on a re-wait (the same sentence was added to his global CLAUDE.md gate (b), backup `~/.claude/CLAUDE.md.bak-rewait-20261012`); `notes:wait-line-rewait/work.md`. Codex updates: `codex plugin marketplace upgrade kerd-core && codex plugin add kerd@kerd-core`; a running Codex thread picks an install up on its next turn. Codex users install the four-skill core with `codex plugin marketplace add anthonymaley/Kerd --ref codex` and `codex plugin add kerd@kerd-core`; the branch is built by `tools/codex_release.py` (`--publish` appends, never force). Record `notes:codex-public-package/work.md`.

**What the newest rules are doing in real use (scan 2026-10-12 09:0x, 11 sittings, `notes:watch-scan-1012/work.md`):** check questions (0.183.0) hold, 10 of 10; literal-path git (0.182.0) a second miss, both in alapah's long session; the global wait-line template slipped to 31 of 43, bare lines mostly one-line re-waits after a worker notification, no nudges or harm (global CLAUDE.md, not Kerd); CI-to-worker 12 of 12. Hand-read 2026-10-12 09:5x: ~37 of 48 hold; the 11 misses all put "Then <next step>" where meanwhile belongs, fixed in 0.183.1. Previous scan `notes:watch-scan-1011/work.md`. Detail per release and scan: `kivna/sessions/2026-10-09.md` to `2026-10-12.md`; release notes in README's What's New.

**Release boundary: 0.183.2 on `main`; releases stay paused apart from the ones he asks for** (ruling below; every release he lifted it for since 2026-09-28 is listed in that ruling's case in `docs/decisions.md`). Unreleased on main since 0.175.1: Switch's eval graders read tool output in the trace (`notes:switch-eval-graders/work.md`).

**Guard false alarm parked (2026-10-11 09:55, his "n" to "worth an hour to fix?"):** apple-music tag pushes go by hand with `!` when it fires. Backlog row.

**Claude Code mods: his band is the public `overtone` from Kerd's marketplace** (`vault_path` = `~/eolas/vault`; rollback hand copy `~/.claude/mods/overtone`). Off: `claude plugin disable overtone@kerd-marketplace`. History, limits and backups: `notes:overtone/work.md`, `notes:overtone-savvy/work.md`. Laptop bells are on for both (backups `*.bak-bell`).

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

**The whole site is in the orchestra look, live since 2026-10-12 16:4x** (https://kerd-six.vercel.app/site/index.html; `main` a16ee817,
CI 38305761648 green). Homepage (5ef56bee, 14:3x): the hall plan of nine seats, each with a Without it / With it card, one story through the
hall, install. Capabilities: the nine seats in detail, each "Played by" its skill. Examples: three real programmes, seats lit only where the
record shows them. Docs: the guides by seat, the hall plan as index. The footer on all four pages has no version number. Direction from his
reference-board pick (Tailscale) and his 11:09 brief ("showing the orchestra as the whole project ... a real concrete why you need this
edge"); shape agreed 15:05; published on his "like it!" 16:40 with no version bump (page only). codex-tui reviewed both passes ("Safe to
push"). The Capabilities plan opens centred on phones since 2026-10-14 10:1x (`site/assets/capabilities.js`, like docs.js; three engines at 390/1440; one-off Codex review; live, CI 38578538162); the guide's stale Slainte line was fixed in 0.183.2. Every push
deploys through Vercel's GitHub integration and GitHub holds each record (checked 2026-10-14 11:0x; 5ef56bee's arrived ~40 min late, which looked like none). Sketchbook `notes:homepage-redesign/work.md`.

**Two teams already use Kerd** (Anthony, 2026-09-22): SAM and Aubel.app. The team note
(`notes:launch-plan/team-note.md`) had his "y" to send (2026-09-23 17:05); not confirmed
sent. **Parked (Anthony, 2026-09-24 08:55): "delay any sam and auble work for now";** don't
raise it until he does.

**Launch step 2, inviting three to five people, is dropped (Anthony, 2026-09-25 11:16: "i dont.
drop this").** Don't raise it or recommend it again unless he does.

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **A Sonnet 5.5 reader that grades or scans against a brief, with Conductor checking every finding, runs at medium; high stays where completeness is the result (Anthony, 2026-10-08 14:49; released 0.179.0).**
- **When options are listed and the question chooses among them, the bubble asks about the recommendation; a missing fact, a pick-several choice, the arrival question and a chosen work's outcome keep their own question (Anthony, 2026-10-06 11:41; released 0.174.0).**
- **Every question carries the options in hand: list them above it with one recommendation, even an open question; ask bare only when none are in hand (Anthony, 2026-10-06 10:40, "we should always give options to user when we have them"; 10:41, "happens a lot in other repos too"; released 0.173.0).**
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

**Not yet ruled, and it is Anthony's:** where and when to announce.

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
handoff from 2026-09-25; not adopted. Anthony confirmed (2026-10-05 22:14) the bound codex-tui thread is the one to keep using; the session ID he first gave was a closed Codex voice session that Agent refused. Its process started 2026-10-05 22:13 and it follows each install on its next turn (checked 2026-10-06). It answers again since 2026-10-14 11:19 (test reply in 16 s at 11:24); an `exit` typed into its prompt on 2026-10-13 10:34 had left its queue undelivered until Anthony typed in it (`notes:codex-queue-stall/work.md`).

**Claude Code's Agent view stays on (Anthony, 2026-09-25 20:54):** `/exit` detaches into the
background-session list; he quits there with Ctrl-C. Switch Out's restart line says so (0.160.0).

**Eval leftovers:** cleared 2026-10-06 on his "y" (detail `kivna/sessions/2026-10-06.md`); 72 sealed `/private/tmp/e-*` folders from 2026-10-07's eval runs (Opus 18 and 6, Haiku 18, 18 and 6, Sonnet 6) are his to delete; `~/.cache/kerd-eval/gitbin` kept.

**Guard work stopped (Anthony 2026-10-07 20:31, "y"):** the unreadable-working-`vault.json` redesign is parked in the Backlog (branch `fix/guard-unreadable-working-vault` 3dbcc28 kept local, unpushed); the next guard change waits for a real slip, per the guard-scope ruling. Four of the day's nine sittings went to guard edges found by review rather than real use.

**Selected continuation (2026-10-14 11:2x): make Agent say when a Codex request is still sitting in Codex's queue, undelivered. Proposed, not agreed.**
Today codex-tui sat for ~2 h with three requests queued and Agent showed only "submitted-unconfirmed": an `exit` typed into its prompt on 2026-10-13 10:34 had interrupted the turn, and the TUI took nothing from its queue until Anthony typed in it at 11:19 (then all three drained, and a test request got a reply in 16 s). A dormant Codex partner from another project has 13 requests queued since 2026-10-09 the same way. Agent could read Codex's queue (`~/.codex/queue_1.sqlite`, version-sensitive) and say "queued, not delivered: the session needs someone to type in it". Shape first (read-only design, then a branch); releases are paused, so a release is his decision. Why first: Now holds only watches; every review before a push routes to codex-tui, and a silent queue cost two hours today with no signal.
Beside it (proposed): nothing else in Now or the Backlog is buildable; the Backlog rows are held, parked or wait on a real slip.
Session logs: `kivna/sessions/` (newest `2026-10-14.md`).

**Pickup reading set** (update 2026-10-14 11:2x, after the Vercel record and codex-tui checks):
- this file complete: position (0.183.2 released; overtone 0.10.0; Claude Code on 0.183.2, his Codex on 0.183.1, current for its package), the whole site live in the orchestra look and the continuation (Agent showing an undelivered Codex queue, proposed), rulings and the Codex position;
- `TODO.md` `## Now`, the designated active list, one line per row with its sketchbook link (`## Backlog` is a separate section outside the set; its top row is the continuation, the rest held or out of scope);
- `kivna/sessions/2026-10-14.md`, newest log (the Capabilities plan on phones; the Vercel record; codex-tui's stuck queue);
- `notes:outside-the-repo.md`, live links outside the repo;
Deeper: `kivna/sessions/2026-10-13.md` (0.183.2, the Slainte wording); `kivna/sessions/2026-10-12.md` (six sittings: the real-use scan, 0.183.1, the orchestra site); `notes:homepage-redesign/work.md` (the site sketchbook, finished, plus 0.183.2 at its end: his words and bans at each step, the cast, both passes, checks and reviews; where the guide finding and the phone plan came from); `notes:wait-line-rewait/work.md` (0.183.1: the 48 lines, the wording, the release); `notes:watch-scan-1012/work.md` (this scan: checked findings per watch item); `kivna/sessions/2026-10-11.md` (five sittings: the parked false alarm, the check-question rule, 0.183.0, both trims); `notes:now-trim/work.md` (the Now trim; `moved-rows.md` holds rows with no sketchbook); `notes:watch-scan-1011/work.md` (the 2026-10-11 scan: checked findings per watch item; its verdicts are in TODO.md's Now); `notes:watch-scan-1010/work.md` (the 2026-10-10 scan, the template decision, the parked guard false alarm); `notes:overtone-savvy/work.md` (the plan view: design, live trial, accepted limits; the Now watch row carries what to look for); `notes:release-0181/plan.html`; `kivna/sessions/2026-10-08.md` (ten sittings: question shape, 0.178.0 to 0.180.1, the plan view); `notes:overtone-savvy/mock.html`, `savvy-look.html`, `raster-proto-register.tsx` (the prototype); `notes:release-0179/work.md` (this sitting: 0.179.0, three review rounds, the `test_ask` race); `notes:bundle-1008/work.md` (notes save, step-list scan); `notes:sonnet-55/work.md` (medium vs high, three checks); `notes:question-shape/work.md` (recheck results, the Switch Out fix, its release); `kivna/sessions/2026-10-07.md` (twelve sittings); `notes:overtone-guard-gaps/work.md` (cut read, unreadable-working blocker, 0.8.3 refspec fix, 0.8.2, 0.8.1); `notes:codex-public-package/work.md` (0.177.2 Codex package, Codex's record); `notes:codex-update/work.md` (Codex 0.177.0 install); `notes:arrival-nothing-buildable/work.md` (0.177.0); `notes:haiku-switch/work.md` (0.176.0: diagnosis, probe, build); `notes:overtone-guard-gaps/work.md` (0.8.2 failed `cd`, and 0.8.1); `notes:opus-switch-evals/work.md` (Opus evals); `kivna/sessions/2026-10-06.md` (eight sittings: 0.172.1 to 0.175.1, the eval graders); `notes:boundary-slip/work.md` (0.175.2); `notes:switch-eval-graders/work.md`; `notes:overtone-guard-gaps/work.md`; `notes:chat-roll-window/work.md`; `notes:fixes-2026-10-06/work.md`; `notes:skills-guideline/work.md`; `docs/decisions.md`; `docs/backlog-archive.md`; `notes:overtone/work.md`; `notes:sonnet-55/work.md`; `notes:codex-update/work.md`;
`notes:real-use-evidence/work.md`; `notes:model-fit/work.md`; `notes:rolling-session/threshold.md`.

**Notes commit:** `ac1a573a98bf59578ba2f3acf59dcc14a241fa5d` (pass it to `prepare`/`pickup` as `--notes-commit`). The vault repo root is
`~/development/home/eolas` (notes under `vault/`). Out commits Kerd's vault files by name with plain git (2026-10-07: the vault tree also holds apple-music's unsaved notes, not Kerd's; Kerd commits only its own paths).

The observed position before this save is `main` at c5439598 (the 10:1x Switch Out); the boundary commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-10-14 11:3x, after the Vercel record and codex-tui checks: 34,844 bytes, about 8,711 tokens (estimate), 711 over the 8,000 target (CONTEXT.md carries most of it; trimming its rulings is not this sitting's work). Carried phrases (queued, not delivered; Proposed, not agreed; false alarm; codex-queue-stall; c5439598) are all in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-10-14.md",
 "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
