# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.149.1 on `main`, unchanged.** The 2026-09-23 night sitting released
nothing; it closed the last two rows of the 2026-09-13 hold and Anthony lifted it. Earlier
that day: 0.147.0 (job list names the model), 0.148.0 (model guide), 0.149.0 (an unanswered
review gets a fresh reader, not a waiver), 0.149.1 (getting-started guide and the concert).

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
"skip lets skip that"). The Codex pickup in a work project the hold deferred is unblocked.

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
announce, which work project gets the Codex pickup, and whether the explanatory output
style stays on for this machine.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push); this sitting it built and
installed Kerd 0.149.1 for Codex on Anthony's direct go in its window. A relayed "y" is not
enough for Codex to do a user-level install; the go must be his, in its window. No job is
running.

**Installed state:** Claude ran 0.149.0 from the plugin cache this sitting; the tip is
0.149.1 (guide wording only), in force after `claude plugin update kerd@kerd-marketplace`
and a new session. **Codex runs 0.149.1** (`codex plugin list`, read by Claude 2026-09-23
18:16; a fresh Codex session reported loading it). Resolve live numbers.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds
Anthony's TypeSafe key and is git-ignored; never print or commit it.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); every file inside `docs/work/product-package/` and
`docs/guide/reference-from-readme.md` (2026-09-19); `docs/work/jev-trial/review_results.json`
and every file inside `docs/work/launch-plan/`, `docs/work/roll-on-branch/`,
`docs/work/waiting-on-you/`, `docs/work/no-idle-sessions/` and `docs/work/site-musical/`
(2026-09-22); and every file inside `docs/work/job-label/` and `docs/work/partner-closed/`
(2026-09-23). They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted by this sitting at its
2026-09-23 17:36 arrival against the saved designation; it designates its successor at
this Out.

**Selected continuation, proposed (not agreed): launch step 2, inviting a few.** Owner:
Anthony names three to five people (the plan proposes at least one non-developer); then
Claude drafts one invitation each, pointing to `docs/guide/getting-started.md` and asking
them to bring their own real work. **Stops at** the drafts: sending is his. **Pending
question:** who they are (parked 2026-09-23 21:13; ask again only if he picks it up).
**Why:** it is the next step to launch, and the only one now unblocked on Kerd's side.
Alongside, his: the TV proof in 3of3 (step 1), confirming the team note to SAM and
Aubel.app went and passing on replies, the announcement, the Codex pickup's project.

**Pickup reading set** (Switch Out, 2026-09-23 night):
- this file complete: position, rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-23.md`, the day's three sittings (the night one last).
Deeper: `docs/design/launch-plan.md`; local sketchbooks `docs/work/launch-plan/work.md`,
`docs/work/job-label/work.md`, `docs/work/partner-closed/work.md`.


The observed position before this save is `5222815` (the evening close, 0.149.1); the boundary commit is this
save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-23 night: about 21,300 bytes across the three sources, about 5,300
tokens estimated at four bytes each, within the 8,000 target. `read_args` for the next
pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-23.md",
 "--section", "TODO.md", "## Now"]
```
