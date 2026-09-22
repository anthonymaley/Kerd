# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.143.0 on `main`, 2026-09-21 afternoon.** Nothing released since; the
2026-09-21 evening sitting shipped prose only, under the no-bump ruling below.

**Kerd's front page, site and README now tell one story, and each says only what a run has
shown.** Anyone can install it (proved 2026-09-20); the front page's claims were checked and
four corrected (2026-09-21); on the evening of 2026-09-21 the six places where the live site
and the README contradicted each other were settled against what Kerd does, and the host line
now reads "Kerd runs inside Claude Code, and a four-skill core can be built for Codex", because
no Codex conversation through that core is on record. The site is live at
https://kerd-six.vercel.app/, checked byte-identical to the repo after each change.

**Jev was tried and is not worth a place in Kerd now** (`docs/work/jev-trial/work.md`). It
grades written evidence fast and cheaply, but Kerd's cost is in finding the evidence. Three
graded runs; backlog triage and review screening failed their pass lines.

**Selected continuation, proposed not agreed: draft a launch plan for the Kerd that exists
now, for Anthony to rule on.** **Why:** the product and its front page are ready for a reader;
what stands between Kerd and a launch is a plan that describes a route to one, and
`docs/design/launch-plan.md` was written around the retired ladder and a ladder pilot, so as
written it no longer does. Owner: Claude drafts through Conductor, starting at Shape; the
ruling is Anthony's; stops at a draft, nothing published. The detail is in `TODO.md` `## Now`.

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
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a score and
a goal; always be delivering; Conductor owns the sketchbook; rolling is per batch.

**Not yet ruled, and it is Anthony's:** the launch plan (the selected continuation drafts
toward that ruling; it does not make it).

**The finding that governs how work is checked here held again.** An independent reader
catches a wrong claim, and a re-read against the record catches one before it ships: the
evening's host-line draft said the Codex core "runs", and the record showed it had only been
built and installed. Codex cleared all four evening changes on first read.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert review
and investigation** (cadence: checkpoints, before-push); four reads on 2026-09-21 evening. No
job is running.

**Installed state:** the 2026-09-21 evening session ran 0.143.0 from the plugin cache, which
is the tip. Resolve live numbers.

**Standing:** a peer session cannot authorize a push. Change the dispatch contract only for
demonstrated behaviour from real dispatches. `.env` at the repo root holds Anthony's TypeSafe
key and is git-ignored (2026-09-22); never print or commit it.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); from 2026-09-19, by Anthony's ruling that working
notes stay unpublished: every file inside `docs/work/product-package/` (the helper takes
files, not folders) and `docs/guide/reference-from-readme.md`; from 2026-09-22,
`docs/work/jev-trial/review_results.json`, which carries role text from the local-only
review archive. They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` is held by the 2026-09-21 evening session,
adopted at its 18:23 arrival, and designates its successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-22 just after midnight):
- this file complete: position, the selected continuation and its reason, the rulings;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-22.md`, the evening sitting's account.
Deeper: `docs/design/launch-plan.md` (the plan the next work redrafts),
`docs/work/front-page-claims/work.md` and `docs/work/jev-trial/work.md`.

The observed position before this save is `9b763c2` (`.env` ignored); the boundary commit is
this save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-22 00:2x: about 16,400 bytes across the three sources, about 4,100
tokens estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-22.md",
 "--section", "TODO.md", "## Now"]
```
