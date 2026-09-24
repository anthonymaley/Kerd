# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.151.0 on `main`.** The 2026-09-24 morning sitting (08:24–09:3x)
brought Codex to 0.150.0 and released 0.151.0: Conductor builds with its own host's workers
and the other provider reviews; a cross-provider builder is an exception the person asks for
or approves. The 2026-09-23 late sitting released 0.149.2 and 0.150.0.

**Both hosts name the Kerd version on arrival:** Claude Code's heading read "Kerd 0.150.0"
this morning; Codex was brought to 0.150.0 (read back 08:48) and Anthony reported its fresh
arrival working. Sketchbook `docs/work/codex-pickup/work.md` (local).

**The new job names are seen in real use:** with 0.149.0 installed, Anthony's running-job
list read `kerd:sonnet-high` (2026-09-23 17:28). Closed.

**Kerd has an accepted launch plan** (`docs/design/launch-plan.md`). Ready to launch when
someone other than Anthony carries a real piece of work, in their own repository, to its
agreed result, unaided. **Step 1 is under way in 3of3's own session**, which has used Kerd
since August; its next item is the TV-to-TV iCloud sync proof, his hands on the televisions,
**which Anthony said he is doing today (2026-09-24 09:29, "y").** Kerd hands nothing over. Step 1's evidence so far (read
2026-09-23 from 3of3's records) is in the local sketchbook `docs/work/launch-plan/work.md`:
Codex review caught four real defects there; the one failure that reached real devices was
a waived review while his Codex session was closed, which 0.149.0 answers.

**Two teams already use Kerd** (Anthony, 2026-09-22): SAM and Aubel.app. The note asking
which version they run, whether they finished work unaided and what broke
(`docs/work/launch-plan/team-note.md`) is going out: Anthony said "y" to sending it now
(2026-09-23 17:05); not yet confirmed sent. Replies go into the per-team lines in
`docs/work/launch-plan/work.md`. **Parked (Anthony, 2026-09-24 08:55): "delay any sam and
auble work for now";** don't raise it until he does.

**The 2026-09-13 hold is lifted (Anthony, 2026-09-23 18:19),** so launch step 2, inviting
three to five people he picks, is open. He was asked who (18:20) and parked it (21:13:
"skip lets skip that").

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **Conductor builds with its own host's workers and the other provider reviews; a
  cross-provider builder is an exception the person asks for or approves, with a reason,
  called a trial without a comparison (2026-09-24, 0.151.0).** No routing framework or
  provider quotas; spare capacity is a reason he gives, not a stored setting.
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
review and investigation** (cadence: checkpoints, before-push); on 2026-09-24 it built and
installed Kerd 0.150.0 for Codex on Anthony's direct go in its window, and reviewed 0.151.0
(four findings, fixed; then clear). Its install report went to Anthony's window, not to
Claude; Claude verified the install by read-back. A relayed "y" is not
enough for Codex to do a user-level install; the go must be his, in its window. No job is
running.

**Installed state:** Claude Code's install is 0.151.0 (`claude plugin list`, 2026-09-24
09:29), in force from the next session; this sitting ran 0.150.0. **Codex runs 0.150.0**
(`codex plugin list --marketplace kerd-core`, 2026-09-24 08:48); bring it along with the
next release. The next arrival's heading names the version
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
(2026-09-23); every file inside `docs/work/codex-pickup/` (2026-09-23 late); and every file inside
`docs/work/codex-players/` (2026-09-24). They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted at the 2026-09-24 08:24 arrival
against the saved designation; it designates its successor at this Out.

**Selected continuation, agreed (Anthony, 2026-09-24 09:29): after Anthony's TV-to-TV
iCloud sync sitting in 3of3, Claude reads 3of3's records (read-only; no question needed)
and adds one line of step 1 evidence to `docs/work/launch-plan/work.md`.** Owner: Anthony
runs the sitting in 3of3's own session; Kerd hands nothing over. **Stops at** the evidence
line; no writes in 3of3, no device actions. **Why:** step 1 is the only launch step under
way, and this proof is its next item. If the sitting hasn't happened, the arrival says so
and weighs the other open work. Then launch step 2, still parked: Anthony names three to
five people (ask again only if he picks it up). His too: the announcement and the output
style. SAM and Aubel.app are parked.

**Pickup reading set** (Switch Out, 2026-09-24 09:3x):
- this file complete: position, rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-24.md`, the late and morning sittings.
Deeper: `kivna/sessions/2026-09-23.md` (the day's three earlier sittings);
`docs/design/launch-plan.md`; local sketchbooks `docs/work/launch-plan/work.md`,
`docs/work/codex-players/work.md`, `docs/work/codex-pickup/work.md`.

The observed position before this save is the 0.151.0 release on `main`; the boundary
commit is this save itself. Ask `git log` for its ID.

**Measured** 2026-09-24 09:3x: about 19,900 bytes across the three sources, about 5,000
tokens estimated at four bytes each, within the 8,000 target. `read_args` for the next
pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-24.md",
 "--section", "TODO.md", "## Now"]
```
