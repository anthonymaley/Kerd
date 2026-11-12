# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Position (2026-11-12 08:4x):** Kerd 0.192.0 is released on `main` (aa297be8, CI 43228928753 green) and published on the public `codex` branch (20a92da8); Claude Code here still has 0.191.0 installed and runs Claude Code 2.1.319; his Codex is on 0.188.1 until he updates it in its window. 0.192.0: a Fable 5.2 prompt profile for Conductor (`anthropic/fable-5-2.md`, 17 clauses from Anthropic's 5.2 pages, none tried on Kerd work) and model choice listing Fable 5.2 in place of 5.1; Claude Code's `fable` alias is Fable 5.2 only from 2.1.321 (5.1 from 2.1.257), so `kerd:fable-*` runs Fable 5.1 here until `claude update`; Fable 5.2 was released 2026-11-09, the day the catalogue run opened no PR (`notes:fable-5-2/work.md`). 0.191.0 (from work-anthony, where `codex-scribe` stalled 2026-11-05 and 142 hand-typed `codex exec` runs stood in, unseen from Codex): Switch In lists looking at a Codex window whose Kerd requests have waited since an earlier day as his own Open work line; Conductor names that partner as a gap at Ready and the go on it covers fresh reviewers through Agent; a grid row naming `codex exec` is not a valid plan; wording only, unseen live (`notes:codex-exec-reviews/work.md`). 0.190.0: Conductor reads model profiles from the public `catalogue` branch (saved copy fresh for seven days, last saved copy on a failed fetch, shipped profiles only with none); Tend names a project still on the old vault Codex bridge (`.agents/bin/ask-codex`) and offers pairing its recorded thread through Agent, then removing the bridge piece by piece (from apple-music's weekly review, `notes:codex-reply-prompt/work.md`). The weekly catalogue task runs Mondays 12:00 UTC (env `kerd-catalogue`). Its 2026-11-09 run succeeded and said "quiet week" after reading only the three index pages in 26 s; by its own reading they still listed Fable 5.1 at 12:08 UTC (found 2026-11-12). Since then the catalogue's stale `model-choice.md` has hidden 0.192.0's Fable 5.2 row from Conductor. On his "yy" 2026-11-12 10:34, the job's step 4 now requires listing every page it re-read before saying "quiet week" (live from 2026-11-16). **PR #3** (https://github.com/anthonymaley/Kerd/pull/3) brings 0.192.0's Fable 5.2 profile, model-choice and README onto `catalogue`. A fresh Codex reviewer's three findings were checked: the PR description is fixed, and the two problems already on `catalogue` are in the Backlog. **The merge is his.** The GitHub Codex connector has never acted on Kerd (his repo-access step unconfirmed). 0.189.0 (Anthropic staff habits: gaps at Ready, the narrower stop rule, Found / Needs you / Unsure, weekly review) not yet seen in real use (`notes:anthropic-habits/work.md`). 0.188.2's Intersect rules not yet seen in a drawing (`notes:chuck-theme/work.md`). Release history: README's What's New (copy in `CHANGELOG.md`) and `kivna/sessions/`.
Codex users install with `codex plugin marketplace add anthonymaley/Kerd --ref codex` and `codex plugin add kerd@kerd-core`; update with `codex plugin marketplace upgrade kerd-core && codex plugin add kerd@kerd-core` (a running thread picks it up next turn). The branch is built by `tools/codex_release.py` (`--publish` appends, never force).

**Real use of the newest rules:** last scan 2026-10-12 (`notes:watch-scan-1012/work.md`); per-row verdicts live in TODO.md's Now.

**Release boundary: 0.192.0 on `main`; releases stay paused apart from the ones he asks for** (ruling below; the releases he lifted it for are in that ruling's case in `docs/decisions.md`). Unreleased on main since 0.175.1: Switch's eval graders read tool output in the trace (`notes:switch-eval-graders/work.md`).

**Parked, on trial or dropped, each with its own condition:** the guard false alarm is parked (2026-10-11 09:55, his "n" to fixing it; apple-music tag pushes go by hand with `!` when it fires; Backlog row); guard work stopped (2026-10-07 20:31; branch `fix/guard-unreadable-working-vault` 3dbcc28 local, unpushed): the next guard change waits for a real slip; rolling by hand at ~200k is on trial, the 200k plan parked (2026-09-27: "i want more data first"): don't build the plan until he asks (he rolls by hand at a break, status line `~/.claude/statusline-command.sh`; Kerd's chat roll stays at 50%; three hand rolls, no loss; `notes:rolling-session/threshold.md`); SAM and Aubel.app work is parked (2026-09-24: "delay any sam and auble work for now"): don't raise it until he does (the team note had his "y" 2026-09-23, not confirmed sent); launch step 2 is dropped (2026-09-25: "i dont. drop this"): don't raise or recommend it unless he does.

**Claude Code mods:** his band is the public `overtone` from Kerd's marketplace (`vault_path` = `~/eolas/vault`; rollback `~/.claude/mods/overtone`; off: `claude plugin disable overtone@kerd-marketplace`; `notes:overtone/work.md`, `notes:overtone-savvy/work.md`). Laptop bells on (backups `*.bak-bell`).

**Tend's stale-hook check worked once** (0.151.1, one headless run; not verified).

**Launch:** accepted plan `docs/design/launch-plan.md`; ready when someone other than Anthony carries real work in their own repo to its agreed result, unaided. Step 1: 3of3 uses Kerd in its own sessions; evidence read from them when he asks (`notes:launch-plan/work.md`). 3of3's own work is never Kerd's open work (2026-09-25: "we are mixing work"). Two teams already use Kerd: SAM and Aubel.app (2026-09-22).

**Site:** the orchestra look, live since 2026-10-12 (https://kerd-six.vercel.app/site/index.html): homepage hall plan, Capabilities, Examples, Docs; no version in the footer; every push deploys through Vercel's GitHub integration (one deploy arrived ~40 min late, 2026-10-14). Sketchbook `notes:homepage-redesign/work.md`.

**Rulings that govern the next work** (one line each; quotes and cases in `docs/decisions.md`, except the 2026-09-23 read-only-reads ruling, which has no case there yet):
- Reviews go to a fresh, record-briefed Codex reviewer by default; standing Codex partners only for multi-turn Codex work (2026-11-12, his "y" 10:47; case `notes:review-routing/work.md`; not yet built).
- Sonnet 5.5 grading or scanning readers run at medium when Conductor checks every finding; high where completeness is the result (2026-10-08; 0.179.0).
- When listed options are chosen among, the bubble asks about the recommendation; a missing fact, pick-several, the arrival question and a chosen work's outcome keep their own (2026-10-06; 0.174.0).
- Every question carries the options in hand, listed above it with one recommendation; bare only when none (2026-10-06; 0.173.0).
- A worker's row shows its task; the command only when it waits on him (2026-10-05; overtone 0.7.1).
- overtone's guard is a safety net for honest mistakes, not a lock against disguised commands; disguised forms go to the Backlog (2026-10-04).
- Releases are paused so he can use Kerd: findings to the Backlog, fixes come back for his release decision, he lifts it (2026-09-28).
- Switch Out previews what Switch In will offer; Switch In offers Conductor with up to four options; a plain yes means the recommendation and approves nothing (2026-10-02; 0.167.0).
- The one-line band is colour, not text; figures in the expanded band (2026-10-03; overtone 0.5.0).
- A mod shows only figures that drive a decision; nothing repeats what is on screen (2026-10-03).
- Nothing is built to show him what he can already see, nothing counted for its own sake; mod UI quiet when fine, loud when he is needed (2026-10-02).
- Mods are Claude Code only for now; Codex separately (2026-10-02).
- Batch the work: under a fan-out grant, several tasks per approval, release on the standing go, back only for his decisions (2026-09-25/26).
- A question never loads its answer: a consequential question follows a decision block and ends "— approve?" or one genuine question (2026-09-25; 0.159.0).
- A public repo's working notes live in the private vault; Kerd sets `work_notes: "vault"`, sketchbooks are `notes:<work>/`, commits staged by name only (2026-09-25; 0.157.0).
- Conductor rolls its own Claude chat in tmux, never the person; nothing typed into Claude, no Stop hook (2026-09-24/25; 0.154.0–1).
- When agreed work is finished with nothing outstanding, Claude runs Switch Out itself; never asks "Run Switch Out now?" (2026-10-03).
- Claude sees its own context token count every session; when to Switch Out is otherwise his call (2026-09-24; 0.153.0, narrowed above).
- Conductor runs on Opus 5.5 at medium by default; Kerd advises session setup, never changes it (2026-09-24; 0.152.0).
- The explanatory and learning output styles are off on this machine (2026-09-24).
- Conductor builds with its own host's workers and the other provider reviews; a cross-provider builder is an approved exception, called a trial (2026-09-24; 0.151.0).
- The "prove Kerd first" hold is lifted; lifting it invites nobody and announces nothing (2026-09-23).
- A review the partner leaves unanswered gets a fresh one-off reviewer on his yes, never a recommended waiver (2026-09-23).
- Dispatch agents are named for the model and the effort (2026-09-23).
- Read-only reads of his own projects need no question; writes, builds, installs, pushes and device actions need their go (2026-09-23).
- Keep moving; never sit idle (2026-09-22).
- A launch plan exists and is accepted; its open decisions are his (2026-09-22).
- Kerd's readers are on desktops and laptops (2026-09-21).
- A page correction ships without a bump when the installed plugin is byte-identical; a change to what installs gets its own version and note (2026-09-21, 2026-09-20).
- Intersect is this machine's diagram default, on white paper for every Kerd user; the Kerd look stays saved as the site's look; after a diagram-design update, reload `intersect.md` (2026-10-15, 2026-10-16; 0.186.0).
- The site is published on Vercel from the repository root (2026-09-21).
- The ladder and the tiered risk ledger are retired (2026-09-19).
- What is published is the product, not how it was made; sketchbooks stay local (2026-09-19).
- The release history stays in the README; `CHANGELOG.md` carries a copy (2026-09-19).
- Every report has one shape; at the end of a build, bring one decision (2026-09-19).
- Claude Code's Agent view stays on: `/exit` detaches, he quits with Ctrl-C there (2026-09-25; 0.160.0).
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a score and a goal; always be delivering; Conductor owns the sketchbook; rolling is per batch.

**Not yet ruled, and it is Anthony's:** where and when to announce.

**Team:** Claude owns build and release. Codex `codex-tui` is the partner for expert review and investigation (cadence: checkpoints, before-push); the bound thread is the one to keep (his confirmation 2026-10-05 22:14); since 0.184.0 Agent's status says when its queue stalls (`notes:codex-queue-stall/work.md`). A relayed "y" is not enough for Codex to install or build; the go must be his, in its window. **codex-tui's bound thread looks closed** (2026-11-08: request 7fb71445 queued over an hour, never delivered); a one-off `codex-review-1108` (his open "Connect Kerd Claude session" window) reviewed 0.190.0; re-pairing codex-tui is his decision; 0.191.0 and 0.192.0 were each reviewed by fresh Codex reviewers started through Agent (five rounds each, 2026-11-10 and 2026-11-12). Routing: no role designation saved; the old `kerd-b5-review` binding still carries an unadopted 2026-09-25 handoff.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds Anthony's TypeSafe key and is git-ignored; never print or commit it, and never serve the repository root over the network (previews serve `site/` only).

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); `docs/guide/reference-from-readme.md` (2026-09-19);
`docs/work/jev-trial/review_results.json` (2026-09-22). They exist on the Mac Studio only.

**Working notes live in the private vault:** `notes:<work>/work.md` under `~/eolas/vault/kerd/work/` (private repo `anthonymaley/eolas`); history of the move in `docs/decisions.md`.

**His to delete:** 72 sealed `/private/tmp/e-*` eval folders from 2026-10-07 (`~/.cache/kerd-eval/gitbin` kept).

**Selected continuation (2026-11-12 10:47, direction agreed, his "y"): make fresh, record-briefed Codex reviewers Kerd's default for reviews.** Standing Codex partners stay only for multi-turn Codex work (a Kerd-started partner), and his own window is used only while he is at it. Switch In stops greeting stale bindings and offers to retire them. Build it next session in Agent, Conductor's review planning and Switch In, with tests. **The release needs his separate go** (releases are paused). First test whether a Kerd-started Codex partner stalls like a TUI. Sketchbook `notes:review-routing/work.md`.
Why: in every repo, reviews routed to an unattended Codex terminal sit in its queue (stalls 2026-10-14, 11-05, 11-08). Fresh reviewers have returned every time since 11-08, and the context they need is in the records.
Beside it (proposed): correct `model-choice.md`'s "GPT-6 has no Terra tier" and its two links that break on the catalogue branch, on `main` then by catalogue PR (Backlog row; Conductor's OpenAI advice says Terra doesn't exist); bring the README's Switch and Conductor sections up to 0.191.0 and run the Slainte release pass; run the first weekly review.
His first: merge catalogue PR #3; on Monday 2026-11-16 the run's report should list the pages it re-read.
His, when he wants 0.192.0 in use: update Kerd in Claude Code and run `claude update` (2.1.321 or later puts `kerd:fable-*` on Fable 5.2); restart work-anthony's Claude Code; look at `codex-scribe`'s window there and say which of its 12 waiting requests still matter; update his own Codex. His to delete: the private probe repo `anthonymaley/kerd-catalogue-probe` and its disabled task. Held on his go: the vault's `ask-codex`/`pair`/`selftest` become a "retired, use /kerd:agent" stub after apple-music pairs through Agent.
**Branch:** `main`. `fix/stalled-partner-route` is merged into it.
Session logs: `kivna/sessions/` (newest `2026-11-12.md`).

**Pickup reading set** (update 2026-11-12 10:5x):
- this file complete: position (0.192.0 released; Fable agents on 5.1 here until `claude update`; catalogue PR #3 awaiting his merge), the continuation (fresh reviewers by default, direction agreed), rulings, the Codex position;
- `TODO.md` `## Now`, the designated active list (`## Backlog` is a separate section outside the set; its newest row is the Terra fix, carried in the continuation above; the rest are held, parked or out of scope);
- `kivna/sessions/2026-11-12.md`, newest log;
- `notes:outside-the-repo.md`, live links outside the repo;
- `notes:review-routing/work.md`, the selected work's sketchbook (agreement, evidence, shape);
Deeper: `notes:anthropic-habits/work.md` (catalogue), `notes:fable-5-2/work.md`, `notes:codex-exec-reviews/work.md`, `notes:deeper-reading.md`, `docs/decisions.md`, `docs/backlog-archive.md`, `kivna/sessions/2026-11-10.md`.

**Notes commit:** `24b44b701a00e859402bbcea54fefee6700a9730` (pass it to `prepare`/`pickup` as `--notes-commit`). The vault repo root is
`~/development/home/eolas` (notes under `vault/`). Out commits Kerd's vault files by name with plain git.

The observed position before this save is `main` at 620373dc (0.192.0 released; this sitting changed records only); the boundary commit is this save itself.

**Measured** 2026-11-12 10:5x, at this Out: 42,096 bytes, about 10,524 tokens (estimate), over the 8,000 target. Kept that size because the set now includes the selected work's sketchbook (`notes:review-routing/work.md`) and a two-sitting log; the next Out should trim TODO's watch rows. Carried phrases (fresh, record-briefed Codex reviewers; notes:review-routing/work.md; PR #3; GPT-6 has no Terra tier; Weekly review) are all in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-11-12.md",
 "--file", "notes:outside-the-repo.md", "--file", "notes:review-routing/work.md",
 "--section", "TODO.md", "## Now"]
```
