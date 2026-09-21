# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.143.0 on `main`, 2026-09-21 afternoon.** Reviewed by Codex before push,
CI green, and the live marketplace manifest reads 0.143.0 with its HTTPS source.

**Kerd's front page now says only what a run has shown, and the site is live.** Anyone can
install it (proved 2026-09-20). On 2026-09-21 the rest of the front page was checked the same
way: 55 claims read cold, the site opened in a real browser, and the two unrun commands run
in a throwaway profile. Four claims were wrong, the worst sending a reader who rolled back
into the exact install failure 0.142.1 had fixed; all four are corrected. The site had never
been published anywhere; it is now at https://kerd-six.vercel.app/, checked live. And 0.143.0
lets a person show their Codex partner a screenshot, the first fix to come from a Kerd user
other than Anthony.

**Selected continuation, proposed not agreed: fix the six places where the live site and the
README contradict each other.** **Why:** the site went live today, so these are now
contradictions a real reader lands on, and the reading pass already scoped them
(`docs/work/front-page-claims/work.md`, F4). Owner: Claude, through Conductor. Re-check each
against the live pages first, settle which wording matches what Kerd actually does, correct
both copies; Codex reviews before push; prose only, so no version bump unless an install
changes; the push is Anthony's. The detail is in `TODO.md` `## Now`.

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **Kerd's readers are on desktops and laptops, not phones (2026-09-21).** Measure pages and
  pictures there first; a narrower laptop window is the edge case.
- **A correction to what the page says ships without a version bump when the installed
  plugin is byte-identical (2026-09-21).** Bounds the next ruling.
- **A defect that changes what installs gets its own version and a release note
  (2026-09-20).** A change to skill text is a release (0.143.0).
- **The Kerd look (`site/DESIGN.md`) is the only diagram theme on this machine; Krutho is
  retired (2026-09-21).** It lives in this machine's diagram tool as the `kerd` profile, not
  in `kerd:visuals`, because Kerd ships to anyone. Supersedes in part the 2026-09-16 "neutral
  default skin" ruling.
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

**Not yet ruled, and it is Anthony's:** `docs/design/launch-plan.md` was written around the
ladder and a ladder pilot, so as written it no longer describes a route to launch.

**The finding that governs how work is checked here held twice more on 2026-09-21.** A real
run catches a wrong mechanism: the rollback fix drafted before running would have told
readers to set a variable that does nothing, and a cold test draw showed a fresh session
reading a different diagram-tool version than the one set up. An independent reader catches
a wrong claim: Codex blocked three overstatements in one paragraph across two rounds, and a
returned subagent finding was rejected on re-check. Neither substitutes for the other.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert review
and investigation** (cadence: checkpoints, before-push); seven reads this sitting, two
correct blocks. No job is running. Three native jobs were dispatched and returned (the
theme test ran three times); the first two were observed on the model and effort requested,
the theme test's settings were not read.

**Installed state:** this session ran 0.142.1 from the plugin cache; the tip is 0.143.0, so
the cache is one release behind. Resolve live numbers.

**Standing:** a peer session cannot authorize a push. Change the dispatch contract only for
demonstrated behaviour from real dispatches.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); and from 2026-09-19, by Anthony's ruling that
working notes stay unpublished: every file inside `docs/work/product-package/` (the helper
takes files, not folders) and `docs/guide/reference-from-readme.md`. They exist on the Mac
Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted by this session at its 2026-09-20
14:33 arrival from the prepared handoff, and designates its successor against this file
after this save.

**Pickup reading set** (Switch Out, 2026-09-21 afternoon):
- this file complete: position, the selected continuation and its reason, the rulings;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-21.md`, this sitting's account.
Deeper: `docs/work/front-page-claims/work.md` (F4 holds the six contradictions) and
`docs/work/partner-images/work.md`.

The observed position before this save is the 0.143.0 release commit; the boundary commit
is this save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-21 15:09: about 18,500 bytes across the three sources, about 4,600
tokens estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-21.md",
 "--section", "TODO.md", "## Now"]
```
