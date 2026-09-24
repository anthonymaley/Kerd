# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.153.0 on `main`.** The 2026-09-24 afternoon sitting (15:08–16:18)
released 0.153.0: a Kerd hook tells Claude its context token count at every prompt and during
long turns, read from the session's transcript. The day sitting released 0.151.1 and 0.152.0;
the morning, 0.151.0.

**Claude Code runs 0.153.0** (`claude plugin update`, 16:07), in force from its next session;
the hook has not yet delivered live. **Codex stays on 0.152.0,** correctly: its four skills did
not change. Hand check before release: hook 170,532 tokens, his status line "83%" free (15:34).

**Tend's stale-hook check works in one real run** (0.151.1, 12:58): a headless Tend in a
scratch repo flagged a settings entry with the literal placeholder, kept an unrelated hook and
changed nothing. One observation, not verified.

**Kerd has an accepted launch plan** (`docs/design/launch-plan.md`). Ready to launch when
someone other than Anthony carries a real piece of work, in their own repository, to its
agreed result, unaided. **Step 1 is under way in 3of3's own session**; its next item is the
TV-to-TV iCloud sync proof, his hands on the televisions. Anthony said he is doing it today
(09:29) and will say here when it is done (09:49). At 14:58, 3of3 had no commits today and
uncommitted work in its player and Jellyfin code; no sign of the sync proof. Kerd hands
nothing over. Evidence so far: local sketchbook `docs/work/launch-plan/work.md`.

**The homepage redesign was tried and dropped (Anthony, 12:56: "nah dont like it - lets drop
it"; "will revisit").** Codex built three passes on his direct ask; his reactions and the
dropped pass are in the local sketchbook `docs/work/homepage-redesign/work.md`. `site/` is
unchanged. When revisited, start from what would make it feel serious rather than AI-made to
him, not from another pick of direction.

**Two teams already use Kerd** (Anthony, 2026-09-22): SAM and Aubel.app. The team note
(`docs/work/launch-plan/team-note.md`) had his "y" to send (2026-09-23 17:05); not confirmed
sent. **Parked (Anthony, 2026-09-24 08:55): "delay any sam and auble work for now";** don't
raise it until he does.

**The 2026-09-13 hold is lifted (2026-09-23),** so launch step 2, inviting three to five people
he picks, is open. He parked choosing them (2026-09-23 21:13: "skip lets skip that").

**Rulings that govern the next work (cases in `docs/decisions.md`):**
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

**Not yet ruled, and it is Anthony's:** who the invited few are, where and when to announce,
and what would make the homepage feel serious to him.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push). Today it built and installed
0.151.0 and 0.152.0 for Codex on Anthony's direct go in its window, reviewed 0.151.1 (clear)
and 0.152.0 (checkpoint: four findings; before-push: two minor; all applied), and built the
homepage passes. A relayed "y" is not enough for Codex to install or build; the go must be
his, in its window. No job is running.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds
Anthony's TypeSafe key and is git-ignored; never print or commit it, and never serve the
repository root over the network (a preview briefly did on 2026-09-24 11:21; its log shows no
request for `.env`; previews now serve `site/` only).

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); every file inside `docs/work/product-package/` and
`docs/guide/reference-from-readme.md` (2026-09-19); `docs/work/jev-trial/review_results.json`
and every file inside `docs/work/launch-plan/`, `docs/work/roll-on-branch/`,
`docs/work/waiting-on-you/`, `docs/work/no-idle-sessions/` and `docs/work/site-musical/`
(2026-09-22); every file inside `docs/work/job-label/` and `docs/work/partner-closed/`
(2026-09-23); every file inside `docs/work/codex-pickup/` (2026-09-23 late); every file inside
`docs/work/codex-players/` (2026-09-24); and every file inside `docs/work/homepage-redesign/`
and `docs/work/opus-55/` (2026-09-24 day). They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted at the 2026-09-24 15:08 arrival
against the saved designation; it designates its successor at this Out.

**First, at the next arrival:** look for the context-reading line at the first prompt; its
absence means the hook isn't loading, which comes before anything else.

**Selected continuation, agreed (Anthony, 2026-09-24 09:29 and 09:49): after Anthony's
TV-to-TV iCloud sync sitting in 3of3, Claude reads 3of3's records (read-only; no question
needed) and adds one line of step 1 evidence to `docs/work/launch-plan/work.md`.** Owner:
Anthony runs the sitting in 3of3's own session and says when it is done. **Stops at** the
evidence line; no writes in 3of3, no device actions. **Why:** step 1 is the only launch step
under way, and this proof is its next item. If the sitting hasn't happened, the arrival says so
and weighs the other open work. The context-window item shipped as 0.153.0's context-reading hook. Parked: step 2, the
announcement, SAM and Aubel.app, the homepage.

**Pickup reading set** (Switch Out, 2026-09-24 16:18):
- this file complete: position, rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-24.md`, today's four sittings.
Deeper: `docs/decisions.md` (the two new rulings' cases); `docs/design/launch-plan.md`; local
sketchbooks `docs/work/launch-plan/work.md`, `docs/work/opus-55/work.md`,
`docs/work/homepage-redesign/work.md`, `docs/work/codex-pickup/work.md`.

The observed position before this save is the 0.153.0 release on `main`; the boundary
commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-09-24 16:18: 28,317 bytes across the three sources, about 7,080 tokens
estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-24.md",
 "--section", "TODO.md", "## Now"]
```
