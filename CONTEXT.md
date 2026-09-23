# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.149.1 on `main`, 2026-09-23 evening.** One release this sitting:
0.149.1, the getting-started guide (the first page an invited user reads) now says a concert
runs on its own branch and nothing reaches `main` without the person's go, and names no
current version that can go stale. Found by a read-only Sonnet/high check; Codex clear.
Earlier the same day: 0.147.0 (job list names the model), 0.148.0 (model guide), 0.149.0
(an unanswered review gets a fresh reader, not a waiver).

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

**Rulings that govern the next work (cases in `docs/decisions.md`):**
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

**Not yet ruled, and it is Anthony's:** whether the 2026-09-13 hold is lifted (rows 3 and
5 checked 2026-09-23 17:29, both still open; see the continuation below), who the invited few are, where and when to announce, and whether the
explanatory output style stays on for this machine.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push); this sitting one
before-push read (0.149.1, clear) and one closeout account ("No outstanding delta"). No
job is running.

**Installed state:** this sitting ran 0.149.0 from the plugin cache; the tip is 0.149.1
(guide wording only), in force after `claude plugin update kerd@kerd-marketplace` and a new
session. Codex's installed Kerd: 0.133.0, reported by Codex 2026-09-23 17:31 (read-only,
not verified here). Resolve live numbers.

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
2026-09-23 16:52 arrival against the saved designation; it designates its successor at
this Out.

**Selected continuation, delegated by Anthony ("your call", 2026-09-23 17:30): observe
row 3 of the 2026-09-13 hold at this Switch In.** Row 3 ("Coordinated Out lost a
contributor", `docs/work/switch-coordinated-closeout/work.md:56`) still owes "the fresh In
recovering both accounts without either old conversation". This Out collected both: Claude
(owner: 0.149.1, the two checks, the job-name sighting) and Codex (one before-push review,
clear; closeout account "No outstanding delta"). **The step:** at this In, check that the
account in `kivna/sessions/2026-09-23.md` ("Evening sitting") and this file carry both
contributions without asking either old session; write the verdict for row 3 (closed, or
open with the missing piece) into `docs/work/launch-plan/work.md` under "The 2026-09-13
hold". **Stops at** that verdict: it does not lift the hold, which stays Anthony's. **Why:**
the hold blocks launch step 2 (inviting a few), and row 3 costs nothing beyond the In
itself. After it: row 5, which needs a current Codex build installed at user level (his go)
and a fresh Codex session loading it. **Anthony's own:** the TV proof in 3of3, confirming
the team note went and passing on replies, the hold, the invited few, the announcement.

**Pickup reading set** (Switch Out, 2026-09-23 evening):
- this file complete: position, rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-23.md`, both of the day's sittings (the evening one last).
Deeper: `docs/design/launch-plan.md`; local sketchbooks `docs/work/launch-plan/work.md`,
`docs/work/job-label/work.md`, `docs/work/partner-closed/work.md`.


The observed position before this save is `7464e89` (0.149.1); the boundary commit is this
save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-23 evening: about 19,000 bytes across the three sources, about 4,750
tokens estimated at four bytes each, within the 8,000 target. `read_args` for the next
pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-23.md",
 "--section", "TODO.md", "## Now"]
```
