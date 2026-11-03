# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Position (2026-11-03 10:2x):** Kerd 0.189.0 is released on `main` (CI 41663341336 green) and installed in Claude Code (loads on restart); **the public `codex` branch reads 0.189.0** (e2baeb4d, appended, identical to the offline build); his Codex is still on 0.188.1 until he updates it in its window. 0.189.0, from Anthropic's research on how its staff use Claude (`notes:anthropic-habits/work.md`, plan sheet `notes:anthropic-habits/plan.png`): Ready lists every open gap at once with its default; a concert stops only for cost, the irreversible, the outward or what falls outside the agreement (an undoable in-scope gap takes its default and is reported under Unsure); every report opens Found / Needs you / Unsure and its question asks what Needs you says; "make this a skill" via skill-creator; pasted decisions in one list; a weekly review (Conductor route, `skills/conductor/references/weekly-review.md`) offered by Switch In after 7 days, with a decision ledger. None of it seen in real use yet. Still open from that work: C, the model-profile catalogue, **shaped and agreed 2026-11-03 12:09** after live probes: a weekly Claude Code scheduled task opens a PR into a `catalogue` branch and posts `@codex review`, Codex's GitHub review checks each clause against its source, **Anthony presses merge** (a cloud Claude cannot merge: refused three times as "Merge Without Review"), Conductor reads the branch with the shipped profiles as fallback. No exception to the release/push rulings any more. Findings and shape in `notes:anthropic-habits/work.md`. 0.188.2's Intersect rules not yet seen in a drawing (`notes:chuck-theme/work.md`). Release history: README's What's New (copy in `CHANGELOG.md`) and `kivna/sessions/`.
Codex users install with `codex plugin marketplace add anthonymaley/Kerd --ref codex` and `codex plugin add kerd@kerd-core`; update with `codex plugin marketplace upgrade kerd-core && codex plugin add kerd@kerd-core` (a running thread picks it up next turn). The branch is built by `tools/codex_release.py` (`--publish` appends, never force).

**Real use of the newest rules:** last scan 2026-10-12 (`notes:watch-scan-1012/work.md`); per-row verdicts live in TODO.md's Now.

**Release boundary: 0.189.0 on `main`; releases stay paused apart from the ones he asks for** (ruling below; the releases he lifted it for are in that ruling's case in `docs/decisions.md`). Unreleased on main since 0.175.1: Switch's eval graders read tool output in the trace (`notes:switch-eval-graders/work.md`).

**Parked, on trial or dropped, each with its own condition:** the guard false alarm is parked (2026-10-11 09:55, his "n" to fixing it; apple-music tag pushes go by hand with `!` when it fires; Backlog row); guard work stopped (2026-10-07 20:31; branch `fix/guard-unreadable-working-vault` 3dbcc28 local, unpushed): the next guard change waits for a real slip; rolling by hand at ~200k is on trial, the 200k plan parked (2026-09-27: "i want more data first"): don't build the plan until he asks (he rolls by hand at a break, status line `~/.claude/statusline-command.sh`; Kerd's chat roll stays at 50%; three hand rolls, no loss; `notes:rolling-session/threshold.md`); SAM and Aubel.app work is parked (2026-09-24: "delay any sam and auble work for now"): don't raise it until he does (the team note had his "y" 2026-09-23, not confirmed sent); launch step 2 is dropped (2026-09-25: "i dont. drop this"): don't raise or recommend it unless he does.

**Claude Code mods:** his band is the public `overtone` from Kerd's marketplace (`vault_path` = `~/eolas/vault`; rollback `~/.claude/mods/overtone`; off: `claude plugin disable overtone@kerd-marketplace`; `notes:overtone/work.md`, `notes:overtone-savvy/work.md`). Laptop bells on (backups `*.bak-bell`).

**Tend's stale-hook check worked once** (0.151.1, one headless run; not verified).

**Launch:** accepted plan `docs/design/launch-plan.md`; ready when someone other than Anthony carries real work in their own repo to its agreed result, unaided. Step 1: 3of3 uses Kerd in its own sessions; evidence read from them when he asks (`notes:launch-plan/work.md`). 3of3's own work is never Kerd's open work (2026-09-25: "we are mixing work"). Two teams already use Kerd: SAM and Aubel.app (2026-09-22).

**Site:** the orchestra look, live since 2026-10-12 (https://kerd-six.vercel.app/site/index.html): homepage hall plan, Capabilities, Examples, Docs; no version in the footer; every push deploys through Vercel's GitHub integration (one deploy arrived ~40 min late, 2026-10-14). Sketchbook `notes:homepage-redesign/work.md`.

**Rulings that govern the next work** (one line each; quotes and cases in `docs/decisions.md`, except the 2026-09-23 read-only-reads ruling, which has no case there yet):
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

**Team:** Claude owns build and release. Codex `codex-tui` is the partner for expert review and investigation (cadence: checkpoints, before-push); the bound thread is the one to keep (his confirmation 2026-10-05 22:14); since 0.184.0 Agent's status says when its queue stalls (`notes:codex-queue-stall/work.md`). A relayed "y" is not enough for Codex to install or build; the go must be his, in its window. Routing: no role designation saved; the old `kerd-b5-review` binding still carries an unadopted 2026-09-25 handoff.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds Anthony's TypeSafe key and is git-ignored; never print or commit it, and never serve the repository root over the network (previews serve `site/` only).

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); `docs/guide/reference-from-readme.md` (2026-09-19);
`docs/work/jev-trial/review_results.json` (2026-09-22). They exist on the Mac Studio only.

**Working notes live in the private vault:** `notes:<work>/work.md` under `~/eolas/vault/kerd/work/` (private repo `anthonymaley/eolas`); history of the move in `docs/decisions.md`.

**His to delete:** 72 sealed `/private/tmp/e-*` eval folders from 2026-10-07 (`~/.cache/kerd-eval/gitbin` kept).

**Selected continuation (2026-11-03 12:1x): Ready for the model-catalogue build. Bring the agreed shape (`notes:anthropic-habits/work.md`, "C shape revised and agreed") to Ready: every open gap with its default (catalogue home: a `catalogue` branch of the public Kerd repo; network Custom allowlist; cadence; the Conductor reader shipped as a normal release on his decision), the staffing grid and the build go as one decision block. Proposed, awaiting his go; nothing built, no scheduled task created for Kerd, no release.**
Why: it is the one agreed direction from the habits work not yet built, and the only part that takes him out of keeping model profiles by hand; every fact it needed is now known from live runs.
Beside it (proposed): run the first weekly review on Kerd (0.189.0's new route; Switch In shows "Weekly review: never run"), the first real use of the new rules; trim TODO.md's Now (its watch rows are the largest part of the pickup read), moving each row's history to its sketchbook.
His to delete: the private probe repo `anthonymaley/kerd-catalogue-probe` (the CLI lacks the delete_repo scope) and its disabled scheduled task (claude.ai routines page); both in `notes:outside-the-repo.md`.
Session logs: `kivna/sessions/` (newest `2026-11-03.md`).

**Pickup reading set** (update 2026-11-03 12:1x):
- this file complete: position (0.189.0 released; Claude Code and the public codex branch on 0.189.0; his Codex on 0.188.1), the continuation (Ready for the model-catalogue build, proposed), rulings and the Codex position;
- `TODO.md` `## Now`, the designated active list, one line per row with its sketchbook link (`## Backlog` is a separate section outside the set; its rows are held, parked or out of scope);
- `kivna/sessions/2026-11-03.md`, newest log (morning: Anthropic's staff habits, 0.189.0 released; late morning: catalogue research, live probes, shape agreed);
- `notes:outside-the-repo.md`, live links outside the repo;
Deeper: `notes:deeper-reading.md` (older session logs and sketchbooks, newest first; open an entry only when a gap needs it), plus `docs/decisions.md` and `docs/backlog-archive.md`.

**Notes commit:** `3ec2b419945d3efbc6c238fb7b7dd1b674433e94` (pass it to `prepare`/`pickup` as `--notes-commit`). The vault repo root is
`~/development/home/eolas` (notes under `vault/`). Out commits Kerd's vault files by name with plain git (2026-10-07: the vault tree also holds apple-music's unsaved notes, not Kerd's; Kerd commits only its own paths).

The observed position before this save is `main` at ee9d826d (0.188.2); the boundary commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-11-03 12:1x, at this Out: 33,356 bytes, about 8,339 tokens (estimate), **339 over the 8,000 target**: today's log holds two sittings (dated history, not trimmed) and TODO.md's Now is the largest part; trimming Now is the offered fix. Carried phrases (Merge Without Review; Anthony presses merge; Ready for the model-catalogue build; kerd-catalogue-probe; Weekly review) are all in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-11-03.md",
 "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
