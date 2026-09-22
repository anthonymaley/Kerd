# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.146.0 on `main`, 2026-09-22 evening.** Six releases this day:
0.144.0 (a concert performs on its own branch), 0.144.1 (the pictures stay readable on a
laptop), 0.145.0 (a correction leads a report; a finish names the next item), 0.145.1 (the
picture-by-path route has Claude evidence), 0.146.0 (a turn never ends idle), plus the
launch plan, a CI check on the release history, the Codex core guide and the site's
musical story.

**Kerd has a launch plan, accepted.** `docs/design/launch-plan.md`. Kerd is ready to
launch when someone other than Anthony carries a real piece of work, in their own
repository, to its agreed result, unaided — his 2026-09-02 definition, reworded without
the ladder and confirmed 2026-09-22. The route: prove it at home (3of3's iCloud sync,
kept light), invite three to five people he picks, they install and carry their own work
through a first sitting and a second, then the open launch. Each invited person is
recorded against five checks: own repository, unaided, finished to their goals, came back
unasked, what broke.

**Two teams already use Kerd** (Anthony, 2026-09-22 17:11): the SAM product team and the
Aubel.app team. The record backs Aubel — a user's 378 kb `TODO.md` there drove v0.41.0 in
June. What nobody has asked them: which version they run, whether they finished work
unaided, and what broke. A note asking exactly that is drafted and approved, for Anthony
to send: `docs/work/launch-plan/team-note.md`. Their answers may show the launch
definition is already met.

**The site now tells the musical story.** Rehearsal and the concert are named in the hero,
defined in their own band before the pieces use them, and defined again on the
capabilities page for a reader arriving from the nav. The README opening matches. Live and
byte-identical, checked after each push.

**What today's releases changed about how Kerd behaves:** a concert runs on
`concert/<work>` and merges back only on the person's go; a report that retracts an
earlier claim leads with it rather than burying it; a finish names the next item instead
of ending on "no action needed"; and a turn ends either carrying on or stopped on a
question answerable cold — never idle with nothing asked, in rehearsal as much as in the
concert. All are wording rules: whether they hold shows in the next sittings, not in
tests.

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **Kerd's readers are on desktops and laptops, not phones (2026-09-21).** Measure pages and
  pictures there first; a narrower laptop window is the edge case.
- **A correction to what the page says ships without a version bump when the installed
  plugin is byte-identical (2026-09-21).** Bounds the next ruling.
- **A defect that changes what installs gets its own version and a release note
  (2026-09-20).** A change to skill text is a release (0.143.0).
- **The Kerd look (`site/DESIGN.md`) is the only diagram theme on this machine; Krutho is
  retired (2026-09-21).** It lives in this machine's diagram tool as the `kerd` profile, not
  in `kerd:visuals`, because Kerd ships to anyone.
- **The site is published on Vercel from the repository root (2026-09-21).** Anthony owns
  the Vercel project; the repository owns `vercel.json`.
- **The ladder and the tiered risk ledger are retired (2026-09-19).** Do not rebuild gates,
  rungs or a ledger.
- **What is published is the product, not how it was made.** Working notes, review ledgers
  and a third party's material stay out of what a newcomer sees.
- **The release history stays in the README;** `CHANGELOG.md` carries a copy; each release
  updates both.
- **Every report has one shape**, built into Conductor's formats. **At the end of a build,
  bring one decision.**
- **Keep moving; never sit idle (2026-09-22).** A session either carries on towards the
  goal, or stops on a reason he can engage with when he gets back. He should never have to
  ask what is going on or what is next. Built into Conductor in 0.146.0, and it covers
  rehearsal's own tasks, not only the concert.
- **A launch plan exists and is accepted (2026-09-22).** `docs/design/launch-plan.md` is
  the route; its open decisions are named there and are his.
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a score and
a goal; always be delivering; Conductor owns the sketchbook; rolling is per batch.

**Not yet ruled, and it is Anthony's:** whether the 2026-09-13 hold is lifted (rows 3 and
5 of that day's verification list are unclosed), who the invited few are, where and when
the open launch is announced, and whether the explanatory output style stays on for this
machine.

**The finding that governs how work is checked here held again, hard.** Codex blocked four
pushes today, each time correctly: it caught a report that read Anthony's "go" as
authorizing a push he had not approved; a claim that nothing writes `.active-modes` when
Skriv still does; a history check that would have accepted a truncated release note, and
then the same check fooled by a `#` comment inside a fenced block; and site copy claiming a
concert never comes back to ask. Claude's own misses today: a trimmed test output that hid
a failure and turned CI red, and two JSON files truncated by opening them for writing
before reading.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert review
and investigation** (cadence: checkpoints, before-push); eleven reads on 2026-09-22, four of
them blocking. No job is running.

**Installed state:** this sitting ran 0.143.0 from the plugin cache throughout, while the
tip moved to 0.146.0. None of today's rules were in force in the session that wrote them;
the cache updates only on `claude plugin update kerd@kerd-marketplace` and a restart.
Resolve live numbers.

**Standing:** a peer session cannot authorize a push. Change the dispatch contract only for
demonstrated behaviour from real dispatches. `.env` at the repo root holds Anthony's TypeSafe
key and is git-ignored (2026-09-22); never print or commit it.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); from 2026-09-19, by Anthony's ruling that working
notes stay unpublished: every file inside `docs/work/product-package/` (the helper takes
files, not folders) and `docs/guide/reference-from-readme.md`; from 2026-09-22,
`docs/work/jev-trial/review_results.json`, which carries role text from the local-only
review archive; and from 2026-09-22 the sitting's own sketchbooks, every file inside
`docs/work/launch-plan/`, `docs/work/roll-on-branch/`, `docs/work/waiting-on-you/`,
`docs/work/no-idle-sessions/` and `docs/work/site-musical/`. They exist on the Mac Studio
only.

**Routing:** the Claude role `kerd-b5-review` was adopted by this sitting at its 08:13
arrival, against the 2026-09-22 designation and unchanged `CONTEXT.md` bytes; the recovery
receipt retires the previous ID. It designates its successor at the next Out.

**Selected continuation, proposed not agreed: watch the four rules shipped today in a real
sitting, and start the first Conductor build on its own branch.** **Why:** five releases
today changed how Kerd behaves — the concert branch, corrections leading a report, a finish
naming the next item, and a turn never ending idle — and not one has been seen in force,
because this sitting ran the 0.143.0 cache while writing them. Owner: Claude, in ordinary
work; nothing to install but `claude plugin update kerd@kerd-marketplace` and a restart,
which is Anthony's to run. **Anthony's own next steps, which no session can do for him:**
send the drafted note to the SAM and Aubel.app teams
(`docs/work/launch-plan/team-note.md`), and take 3of3's iCloud sync through Kerd as the
launch plan's step 1.

**Pickup reading set** (Switch Out, 2026-09-22 evening):
- this file complete: position, the accepted launch plan, the rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-22.md`, both of the day's accounts.
Deeper: `docs/design/launch-plan.md` (the route and its open decisions), and the
local-only sketchbooks `docs/work/launch-plan/`, `docs/work/no-idle-sessions/work.md` and
`docs/work/site-musical/work.md`.

The observed position before this save is `4e5d4bc` (the capabilities page); the boundary
commit is this save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-22 evening: 23,923 bytes across the three sources, about 5,981 tokens
estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-22.md",
 "--section", "TODO.md", "## Now"]
```
