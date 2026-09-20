# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.142.0 on `main`, 2026-09-19 late evening.** Two releases this
sitting, both reviewed by Codex before push, CI green on both.

**Kerd now installs what its front page says, and keeps work honest one way.** 0.141.0
removed Drive, Lorg, Interrogate and Pair, so the plugin ships the eight skills the README,
website and guides describe. 0.142.0 retired the ladder: the check tools, the requirements
register tools, the design matrix, the progress board, the diagram generators, the handoff
fidelity check, Conductor's step check and the "Checks that can say no" guide. What keeps
work honest now is the sketchbook that becomes a spec, the score the build is checked
against, the goal check, an independent reviewer, and **a short list of risks Conductor
keeps in view and reads back before Ready and the goal check (new, wording and a wording
test, not yet seen in real use).** The release rules check lives on as
`tools/release_check.py`; CI runs skill tests, hook tests and that check.

**The old records are history, unpoliced.** `docs/product/`, `docs/gates/`, `docs/plans/`,
`docs/design/`, `docs/requirements/` stay where they were. Nothing reads them.

**Selected continuation, proposed not agreed: install Kerd 0.142.0 from scratch, following
the README's own commands, and fix what breaks.** **Why:** three releases in one day changed
what installs, and nobody has ever run the published install commands; it is the first thing
a newcomer does. Owner: Claude runs it in a throwaway profile and reports; Codex reviews any
fix before push. It stops at a report and plain fixes. Installing on Anthony's own profile
needs his go. Terrain is in `TODO.md` `## Now`.

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **The ladder and the tiered risk ledger are retired (2026-09-19 18:48).** Nobody wants a
  machine that refuses their work. Wanted: a sketchbook that becomes a spec, a score to
  check the build against, risks kept in view. Do not rebuild gates, rungs or a ledger.
- **What is published is the product, not how it was made.** Working notes, review ledgers
  and the owner's raw typed words stay out of what a newcomer sees; committed work records
  paraphrase him rather than quote his typing.
- **The release history stays in the README;** `CHANGELOG.md` carries a copy; each release
  updates both.
- **Every report has one shape, built into Conductor's formats, never a mode.**
- **At the end of a build, bring one decision,** never a review file or a list of choices.
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a score
and a goal; always be delivering; Conductor owns the sketchbook; rolling is per batch; work
capability and product first, protocol after.

**Not yet ruled, and it is Anthony's:** `docs/design/launch-plan.md` was written around the
ladder and a ladder pilot. With the ladder retired it no longer describes a route to launch.

**The finding that governs how rules are written here, now at seven instances.** A new rule
needs a situation it can pass and one it can fail, and **what catches the defects is an
independent reader or a real run, never a static search.** This sitting: a search said
Interrogate had no dependents, and it was right; the same kind of search missed two test
assertions and the audit's grounding rule, and the test run and the audit found them.

**Found, unanswered: a concert cannot roll without publishing.** A roll is a Switch Out,
which commits and pushes. This sitting avoided it by keeping each build uncommitted until
reviewed. Details in `TODO.md` `## Now`.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push); it answered four requests
this sitting. Four native players were dispatched, all returned, all observed on the model
and effort requested; none is running.

**Installed state:** this session loaded 0.139.0 from the plugin cache; the tip is 0.142.0.
Until the cache refreshes, a session here still gets Pair's prompt line and the old step
check text. Resolve live numbers.

**Standing:** a peer session cannot authorize a push. Change the dispatch contract only for
demonstrated behaviour from real dispatches.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); and from 2026-09-19, by Anthony's ruling that
working notes stay unpublished: `docs/work/product-package/` and
`docs/guide/reference-from-readme.md`. They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted by this session at its 2026-09-19
18:12 arrival, and designates its successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-19 late evening):
- this file complete: position, the selected continuation and its reason, the rulings;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-19.md`, the day's two accounts.
Deeper: `docs/work/retire-four-skills/work.md`, the evening's sketchbook.

The observed position before this save is the 0.142.0 release commit; the boundary commit
is this save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-19 22:2x: about 21,600 bytes before this note, about 5,400 tokens
estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-19.md",
 "--section", "TODO.md", "## Now"]
```
