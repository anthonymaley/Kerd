# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

Older positions, selections and pickup sections: `docs/context-archive/index.md` (moved verbatim 2026-11-26; read the entry when this file lacks something an open item needs).

**Newest (2026-11-26 14:1x): Kerd 0.204.0 is released: start points stay small, and nothing is lost.** From his chief of staff's report (cosplay-32, 11:46, `~/development/product/cosplay/docs/work/for-kerd/2026-11-26-switch-in-friction.md`: CONTEXT.md files of 239-484 KB; 3of3's Switch In failed at the 256 KB read limit). Chosen at Switch In ("y" 11:46), plan approved ("y" ~11:59), release on his 14:07 "gi" (read as go). Switch Out copies anything it removes or rewrites, in any file it trims, verbatim into an append-only `docs/context-archive/` with an index line per write; `measure`/`prepare`/`pickup` flag every source over 32 KB; `prepare`/`pickup` default `--branch`; `--project` either side (differing repeats refused); in.md split into a core and `in-detail.md`. Five fresh Codex reviews (Hold 3, 3, 3, 1, then Safe); suite 1,701; ship exit 0 (main d95d1bd4, CI 45881304294, plugin 52f4064a, codex 9690fc3a; loads on restart). One-time migrations (originals byte-identical in each project's `docs/context-archive/CONTEXT-2026-11-26.md`): Seinn (27 KB), 3of3 (31 KB; its CONTEXT was stale since 10-15, TODO `## Now` ~500 KB left out of read_args) and Apple Music (24 KB, in the vault) fast-forwarded in their checked-out branches, unpushed; Krutho NOT merged (live CONTEXT.md had unsaved edits): branch `kerd/lean-start-point`, worktree `~/development/work/work-anthony-lean`, for its own session. Chief of staff (now `cosplay-fb`) told. Kerd's own CONTEXT.md archived the same way this Out. Side finding: weekly reviews exist only in Kerd, Krutho, 3of3 and Apple Music; never in Seinn, Leru, Bree, Klar, Toyota Sensei, Dinner Tonight, Cosplay. Sketchbook `notes:start-point-size/work.md`.

Phase: 0.204.0 shipped (lean start points); next, why weekly reviews don't run in most projects; the portal-links paper waits beside it; then the invited round, whose who and when are his.

Codex users install with `codex plugin marketplace add anthonymaley/Kerd --ref codex` and `codex plugin add kerd@kerd-core`; update with `codex plugin marketplace upgrade kerd-core && codex plugin add kerd@kerd-core` (a running thread picks it up next turn). The branch is built by `tools/codex_release.py` (`--publish` appends, never force).

**Real use of the newest rules:** last scan 2026-10-12 (`notes:watch-scan-1012/work.md`); per-row verdicts live in TODO.md's Now.

**Release boundary: 0.203.1 shipped (2026-11-23 22:0x, on his 21:53 "y"; release commit c2d0f978, `plugin` 398e6813, `codex` 3d8aa7ae), before it 0.203.0 (2026-11-21 14:58, on his 14:49 "y"; main 52c6c479, `plugin` 081c7414, `codex` 1fd8388f), before it 0.202.0 (2026-11-21 11:29, on his 11:20 "y"; main 0cc9c445, `plugin` f2f13a1a, `codex` d2390573), before it 0.201.0 (2026-11-20 23:00, on his 22:57 "yy"; main 363b3ea6, `plugin` 420769c5, `codex` bd091403, installed here at 420769c5), before it 0.200.1 (2026-11-20 14:16, on his 14:13 "y"; main 05769806, `plugin` 4713ac2a, `codex` d0ff8a6b, installed here at 4713ac2a), before it 0.200.0 (12:1x, his 12:14 "y"; main cc66024a, `plugin` 0604285b) and 0.199.0 (2026-11-14 17:31, on his 17:06 "y"; main 6224b5ed, `plugin` 04c5dbc8, `codex` d3edb66f, installed here at 04c5dbc8), before it 0.198.0 (14:59, on his 14:58 "y"; main 29fb7aab, `codex` 9c3816fc); releases stay paused apart from the ones he asks for** (ruling below; the releases he lifted it for are in that ruling's case in `docs/decisions.md`). Unreleased on main since 0.175.1: Switch's eval graders read tool output in the trace (`notes:switch-eval-graders/work.md`).

**Parked, on trial or dropped, each with its own condition:** the guard false alarm is parked (2026-10-11 09:55, his "n" to fixing it; apple-music tag pushes go by hand with `!` when it fires; Backlog row); guard work stopped (2026-10-07 20:31; branch `fix/guard-unreadable-working-vault` 3dbcc28 local, unpushed): the next guard change waits for a real slip; rolling by hand at ~200k is on trial, the 200k plan parked (2026-09-27: "i want more data first"): don't build the plan until he asks (he rolls by hand at a break, status line `~/.claude/statusline-command.sh`; Kerd's chat roll stays at 50%; three hand rolls, no loss; `notes:rolling-session/threshold.md`); SAM and Aubel.app work is parked (2026-09-24: "delay any sam and auble work for now"): don't raise it until he does (the team note had his "y" 2026-09-23, not confirmed sent); launch step 2 is dropped (2026-09-25: "i dont. drop this"): don't raise or recommend it unless he does.

**Claude Code mods:** his band is the public `overtone` from Kerd's marketplace (`vault_path` = `~/eolas/vault`; rollback `~/.claude/mods/overtone`; off: `claude plugin disable overtone@kerd-marketplace`; `notes:overtone/work.md`, `notes:overtone-savvy/work.md`). Laptop bells on (backups `*.bak-bell`).

**Tend's stale-hook check worked once** (0.151.1, one headless run; not verified).

**Launch:** accepted plan `docs/design/launch-plan.md`; ready when someone other than Anthony carries real work in their own repo to its agreed result, unaided. Step 1: 3of3 uses Kerd in its own sessions; evidence read from them when he asks (`notes:launch-plan/work.md`). 3of3's own work is never Kerd's open work (2026-09-25: "we are mixing work"). Two teams already use Kerd: SAM and Aubel.app (2026-09-22).

**Site:** the orchestra look, live since 2026-10-12 (https://kerd-six.vercel.app/site/index.html): homepage hall plan, Capabilities, Examples, Docs; no version in the footer; every push deploys through Vercel's GitHub integration (one deploy arrived ~40 min late, 2026-10-14). Sketchbook `notes:homepage-redesign/work.md`.

**Rulings that govern the next work** (one line each; quotes and cases in `docs/decisions.md`, except the 2026-09-23 read-only-reads ruling and the 2026-11-26 no-deletion ruling, which have no case there yet):
- Kerd never compacts or deletes context: trimmed material moves verbatim to a reachable archive (2026-11-26 12:07: "we cannot have context compacting though or deletion of context"; 0.204.0).
- `measure` refuses a source outside `--scope` and `retire` refuses a binding under an hour old with an unconfirmed launch; both stay as shipped (2026-11-14, his "y" 11:51; weekly review #5).
- Reviews go to a fresh, record-briefed reviewer from the other provider by default; standing Codex partners only for multi-turn Codex work or when he names one (2026-11-12, his "y" 10:47; built and released 0.193.0 on his 14:46 go; case `notes:review-routing/work.md`).
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

**Team:** Claude owns build and release. Since 0.193.0 reviews go to fresh reviewers from the other provider through Agent, not to a standing partner; four fresh Codex rounds reviewed 0.193.0 (Hold 4, 4, 2, then Safe). On his yes 2026-11-14 11:55-11:56, all 12 stale bindings (`codex-tui` among them) and the test leftovers `route-test-1112` and `stall-test-1112c` were retired (set aside in `.git/kerd-agent/partners-retired/`, recoverable); only `codex-review-1108` (a one-off review) remains. Fresh reviewers are one-off workers (`review-0198-r1`…`r9`; `cos-design-review-1120`, `-r2`), not bindings. Anthony's chief of staff, Cosplay's Claude session (`cosplay-b1` on 2026-11-20; names change), sends requests and relays his decisions by cross-session message; a relayed approval covers what he said, never a push or release by itself. A relayed "y" is not enough for Codex to install or build; the go must be his, in its window. Routing: no role designation saved; `kerd-b5-review` still carries an unadopted 2026-09-25 handoff.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds Anthony's TypeSafe key and is git-ignored; never print or commit it, and never serve the repository root over the network (previews serve `site/` only).

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); `docs/guide/reference-from-readme.md` (2026-09-19);
`docs/work/jev-trial/review_results.json` (2026-09-22). They exist on the Mac Studio only.

**Working notes live in the private vault:** `notes:<work>/work.md` under `~/eolas/vault/kerd/work/` (private repo `anthonymaley/eolas`); history of the move in `docs/decisions.md`.

**His to delete:** 72 sealed `/private/tmp/e-*` eval folders from 2026-10-07 (`~/.cache/kerd-eval/gitbin` kept).

**Selected continuation (2026-11-26 14:1x, proposed): find out why weekly reviews don't run in most projects, then propose a fix.** Claude reads, read-only, the newest Switch In screens in Seinn, Leru, Bree and Klar (their session transcripts or logs) to see whether the "weekly review" Open work line appeared and whether anyone picked it; compares with in.md's three lookups; writes the finding and one proposed change (e.g. recommend it when 14+ days overdue, or let the chief of staff schedule it) into `notes:start-point-size/work.md` "Side finding", for his decision. Stops at the proposal; nothing built. Why: he raised it today (11:4x, "weekly reviews not running on most projects or not being offered perhaps"), and the review is how Kerd learns from real sittings.
Beside it (proposed): the portal-links and paper-template paper (TODO Now); Kerd's own weekly review (last 2026-11-13).

**Branch:** `main` (0.204.0, shipped 2026-11-26; `concert/start-point-size` merged fast-forward and kept, worktree removed). Before it: `main` (0.199.0, shipped). The public `plugin` branch is generated by `ship`; never commit to it by hand. `concert/round5-fixes` (worktree `~/development/product/Kerd-round5`) is merged into main (fast-forward) and kept. `concert/batch-1114` (worktree `~/development/product/Kerd-batch-1114`) and `concert/overnight-1113` are merged into main (fast-forward) and kept; so are `concert/review-routing`, `concert/route-repair`, `concert/openai-advice`, `concert/readme-guides`, `concert/prepare-scope` and `concert/pickup-recheck`.
Session logs: `kivna/sessions/` (newest `2026-11-26.md`).
Chief of staff: now `cosplay-fb` (was cosplay-32 earlier 2026-11-26, cosplay-a8 before).

## For Kerd's next pickup (you can ignore this)

**Pickup reading set** (2026-11-26 14:2x): this file complete (position, continuation, rulings, team); `TODO.md` `## Now` (active list, Queue and Asks tables); `kivna/sessions/2026-11-26.md` (newest log); `notes:outside-the-repo.md` (live links outside the repo); `notes:start-point-size/work.md` (the sketchbook the next step writes into). Deeper: `docs/context-archive/index.md`, `docs/decisions.md`, `docs/backlog-archive.md`.

**Notes commit:** `1d6de2a98707d5266ef9437e6b5dd6f401ce744c` (pass as `--notes-commit`; vault repo root `~/development/home/eolas`, notes under `vault/`). That vault push also carried Apple Music's lean start point (95d27d1) to the eolas remote: Apple Music's records live in the vault, so its migration is pushed, unlike Seinn's and 3of3's.

**Measured** 2026-11-26 14:2x: 51,761 bytes, about 12,941 tokens (estimate), over the 8,000 target; CONTEXT.md is now 16 KB (was 38.8 KB), TODO `## Now` 22 KB is the largest part. Carried phrases all in the set. `read_args`:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-11-26.md",
 "--file", "notes:outside-the-repo.md", "--file", "notes:start-point-size/work.md",
 "--section", "TODO.md", "## Now"]
```

