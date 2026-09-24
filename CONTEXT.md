# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.150.0 on `main`.** The 2026-09-23 late sitting (to 2026-09-24
08:10) released 0.149.2 (the getting-started walkthrough says what to type in Codex) and
0.150.0 (the Switch In heading names the Kerd version that drew it). Earlier on 09-23:
0.147.0, 0.148.0, 0.149.0, 0.149.1.

**The Codex pickup in a work project passed (2026-09-23 22:13, Seinn):** a fresh Codex
session on 0.149.1 restored Seinn's place, caught a stale claim, wrote nothing and stopped
at its question. Both its findings shipped as 0.149.2 and 0.150.0. Sketchbook
`docs/work/codex-pickup/work.md` (local).

**The new job names are seen in real use:** with 0.149.0 installed, Anthony's running-job
list read `kerd:sonnet-high` (2026-09-23 17:28). Closed.

**Kerd has an accepted launch plan** (`docs/design/launch-plan.md`). Ready to launch when
someone other than Anthony carries a real piece of work, in their own repository, to its
agreed result, unaided. **Step 1 is under way in 3of3's own session**, which has used Kerd
since August and is switched in now; its next item is the TV-to-TV iCloud sync proof, his
hands on the televisions. Kerd hands nothing over. Step 1's evidence so far (read
2026-09-23 from 3of3's records) is in the local sketchbook `docs/work/launch-plan/work.md`:
Codex review caught four real defects there; the one failure that reached real devices was
a waived review while his Codex session was closed, which 0.149.0 answers.

**Two teams already use Kerd** (Anthony, 2026-09-22): SAM and Aubel.app. The note asking
which version they run, whether they finished work unaided and what broke
(`docs/work/launch-plan/team-note.md`) is going out: Anthony said "y" to sending it now
(2026-09-23 17:05); not yet confirmed sent. Replies go into the per-team lines in
`docs/work/launch-plan/work.md`.

**The 2026-09-13 hold is lifted (Anthony, 2026-09-23 18:19),** so launch step 2, inviting
three to five people he picks, is open. He was asked who (18:20) and parked it (21:13:
"skip lets skip that").

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **The 2026-09-13 "prove Kerd first" hold is lifted (2026-09-23);** lifting it invites
  nobody and announces nothing.
- **A review the partner leaves unanswered gets a fresh one-off reviewer on his yes, never
  a recommended waiver (2026-09-23).**
- **Dispatch agents are named for the model and the effort (2026-09-23);** the call still
  names the same model. Bounds the 2026-09-16 countermeasure ruling.
- **Read-only reads of his own projects need no question first (2026-09-23,** "you can read
  anytime"). Writes, builds, installs, pushes and device actions still need their go.
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

**Not yet ruled, and it is Anthony's:** who the invited few are, where and when to
announce, and whether the explanatory output
style stays on for this machine.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push); on 2026-09-23 it built and
installed Kerd 0.149.1 for Codex on Anthony's direct go in its window, and reviewed
0.149.2 and 0.150.0 (one blocking finding, fixed). A relayed "y" is not
enough for Codex to do a user-level install; the go must be his, in its window. No job is
running.

**Installed state:** Claude Code's install is 0.150.0 (`claude plugin list`, 2026-09-24
08:02), in force from the next session; this sitting ran 0.149.1. **Codex runs 0.149.1**
(`codex plugin list`, read 2026-09-23 21:52). The next arrival's heading names the version
it loaded; resolve other live numbers.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds
Anthony's TypeSafe key and is git-ignored; never print or commit it.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); every file inside `docs/work/product-package/` and
`docs/guide/reference-from-readme.md` (2026-09-19); `docs/work/jev-trial/review_results.json`
and every file inside `docs/work/launch-plan/`, `docs/work/roll-on-branch/`,
`docs/work/waiting-on-you/`, `docs/work/no-idle-sessions/` and `docs/work/site-musical/`
(2026-09-22); every file inside `docs/work/job-label/` and `docs/work/partner-closed/`
(2026-09-23); and every file inside `docs/work/codex-pickup/` (2026-09-23 late). They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted at the 2026-09-23 21:36 arrival
against the saved designation; it designates its successor at this Out.

**Selected continuation, proposed (not agreed): bring Codex to Kerd 0.150.0.** Owner:
Anthony gives the go in Codex's own window (a relayed "y" is not enough for a user-level
install); Codex builds `output/kerd-codex-0.150.0` and reinstalls only `kerd-core`; Claude
reads back `codex plugin list` and, in a fresh Codex session, the arrival heading's
version. **Stops at** that read-back; no project work. **Why:** both hosts then show which
Kerd drew an arrival before anyone is invited, so a report from an invitee names its
build. Alongside, the first Claude arrival on 0.150.0 is its own check: its heading should
read "Kerd 0.150.0". Then launch step 2, still parked: Anthony names three to five people
(asked 2026-09-23 18:20, parked 21:13; ask again only if he picks it up). His too: the TV
proof in 3of3, confirming the team note to SAM and Aubel.app went, the announcement.

**Pickup reading set** (Switch Out, 2026-09-24 morning):
- this file complete: position, rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-24.md`, the late sitting.
Deeper: `kivna/sessions/2026-09-23.md` (the day's three earlier sittings);
`docs/design/launch-plan.md`; local sketchbooks `docs/work/codex-pickup/work.md`,
`docs/work/launch-plan/work.md`.

The observed position before this save is the 0.150.0 release on `main`; the boundary
commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-09-24 08:1x: about 16,100 bytes across the three sources, about 4,000
tokens estimated at four bytes each, within the 8,000 target. `read_args` for the next
pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-24.md",
 "--section", "TODO.md", "## Now"]
```
