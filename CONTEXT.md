# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0; being retired for Conductor, ruled 2026-09-18; **lorg, interrogate and pair also ruled cut 2026-09-19**, all four still shipping until a breaking release removes them), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.140.0 on `main`, 2026-09-19 evening.** Four commits this sitting:
the product package, two removals from it, and 0.140.0. CI green on the last.

**Kerd now has a public face.** A newcomer's README, a four-page website (`site/`),
guides (`docs/guide/`), fourteen pictures (`docs/pictures/`) and three real examples
(`examples/`). It tells one story: three things that go wrong when you work with an AI
(you lose your place; what you want never gets pinned down; done is whatever the AI
says) and what Kerd does about each. The ladder and gates are one deeper guide, not the
pitch. Six capabilities are shown: Switch, Conductor, Visuals, Agent, Tend and Slainte,
Kivna and Skriv.

**0.140.0: reports you can read at a glance.** Every report Conductor gives has one
shape, and the delegation grid says who does each job in plain words. Wording and a
wording test; **not yet seen in real use.**

**0.139.0 has now been used once, on real work.** The package was rehearsed in eight
exchanges and performed as a concert of three batches, twenty dispatches, with the goal
check reopening two failed goals. The account, with what went wrong, is
`kivna/sessions/2026-09-19.md`.

**Selected continuation, proposed not agreed: remove the four retired skills (Drive,
Lorg, Interrogate, Pair) from the plugin in one breaking release.** **Why:** the published
package no longer mentions them and the plugin still ships them, so the product and its
front page disagree. Owner: Claude builds and releases; Codex reviews before push. It
stops at a reviewed release. Terrain and traps are in `TODO.md` `## Now`.

**Rulings that govern the next work (2026-09-19; cases in `docs/decisions.md`):**
- **Lorg, Interrogate and Pair are cut.** Out of the package now; out of the plugin in a
  later breaking release with Drive. Interrogate's removal travels with the ladder and
  gate cleanup.
- **What is published is the product, not how it was made.** Working notes, review
  ledgers and the owner's raw typed words stay out of what a newcomer sees.
- **The release history stays in the README;** `CHANGELOG.md` carries a copy; each
  release updates both.
- **Every report has one shape, built into Conductor's formats, never a mode.** The
  grid with Fit lines is right, without the routing column.
- **At the end of a build, bring one decision,** never a review file or a list of choices.
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a
score and a goal; always be delivering; Conductor owns the sketchbook; rolling is per
batch; work capability and product first, protocol after.

**The finding that governs how rules are written here, now at six instances.** A new
rule needs a situation it can pass and one it can fail, and **what catches the defects is
an independent reader, never a static check.** On 2026-09-19 cold readers found what the
pages were missing, and Codex found what Claude had under-weighted; 752 green tests found
nothing. New this sitting: **players told not to grade their own work caught four
defects in Claude's briefs** by declining to write what they could not source.

**Found, unanswered: a concert cannot roll without publishing.** A roll is a Switch Out,
which commits and pushes. Details in `TODO.md` `## Now`.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push); it answered four
before-push reviews on 2026-09-19. Twenty native Claude agents were dispatched and all
returned; none is running.

**Installed state:** this session loaded 0.139.0; the tip is 0.140.0 and the cache does
not hold it yet. Resolve live numbers.

**Standing:** a peer session cannot authorize a push. Change the dispatch contract only
for demonstrated behaviour from real dispatches (0.140.0's grid change was that).

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every
save:** `kerd-laptop-result.patch` (2026-09-09); and from 2026-09-19, by Anthony's ruling
that working notes stay unpublished: `docs/work/product-package/` (the sketchbook, score,
story, reader findings, quotes ledger and two views), `docs/guide/reference-from-readme.md`
(the old README's text), and inside it `structured-route-work-with-observations.md` (the
observations of 0.139.0 in use; the tracked `docs/work/structured-route/work.md` was left
as committed). They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted by this session at its
2026-09-18 23:26 arrival, and designates its successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-19 evening):
- this file complete: position, the selected continuation and its reason, the rulings;
- `TODO.md` `## Now` with its child section, the designated active list;
- `kivna/sessions/2026-09-19.md`, the sitting's account.
Deeper, on this machine only: `docs/work/product-package/work.md`.

The observed position before this save is the 0.140.0 release commit; the boundary
commit is this save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-19 18:2x: about 17,600 bytes before this note, about 4,400 tokens
estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-19.md",
 "--section", "TODO.md", "## Now"]
```
