# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.142.1 on `main`, 2026-09-20 midday.** Reviewed by Codex before push,
CI green.

**Kerd can now actually be installed by someone who is not Anthony.** It could not be, from
the day the package shipped until 2026-09-20. Kerd's own marketplace manifest declared the
plugin's source as an SSH address, `git@github.com:anthonymaley/Kerd.git`. Adding the
marketplace survived that, because the CLI's GitHub shorthand probes SSH and falls back to
HTTPS; installing did not, because it clones the declared address literally. So the second
of the two commands on the front page failed for anyone without a GitHub key, leaving no
plugin and none of the eight skills. 0.142.1 publishes
`https://github.com/anthonymaley/Kerd.git` instead. **Proved, not argued:** a keyless
throwaway profile installed 0.142.1 from the live marketplace and got all eight skills.

**Three releases went out over that defect and nothing in the repo could have caught it.**
Not the release check, not 757 tests, not two Codex reviews — because every one of them
inspects what Kerd says about itself. Only running the command as a stranger did.

**Selected continuation, proposed not agreed: check the rest of the front page the way the
install was checked.** **Why:** the install commands were the first front-page claim anyone
ever ran and they were broken; two claims on the same page are still unrun. The website has
never been opened in a real browser, and the `claude --plugin-dir` trial route has never
been used — and that one is already known to overstate itself, writing a `pluginUsage` row
to `~/.claude.json`, so "nothing is installed or disabled globally" is true of plugins and
marketplaces but not of every trace. Owner: Claude runs both in throwaway profiles and
reports; Codex reviews any fix before push; nothing touches Anthony's own profile without
his word. Terrain is in `TODO.md` `## Now`.

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **A defect that changes what installs gets its own version and a release note, not a
  quiet repair of what the existing tag points at (2026-09-20 11:42).** Proposed by
  Conductor, agreed by Anthony. Scope: packaging defects that change what a newcomer
  receives; not every repair is a release.
- **The ladder and the tiered risk ledger are retired (2026-09-19 18:48).** Nobody wants a
  machine that refuses their work. Wanted: a sketchbook that becomes a spec, a score to
  check the build against, risks kept in view. Do not rebuild gates, rungs or a ledger.
- **What is published is the product, not how it was made.** Working notes, review ledgers
  and the owner's raw typed words stay out of what a newcomer sees.
- **The release history stays in the README;** `CHANGELOG.md` carries a copy; each release
  updates both.
- **Every report has one shape, built into Conductor's formats, never a mode.**
- **At the end of a build, bring one decision,** never a review file or a list of choices.
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a score
and a goal; always be delivering; Conductor owns the sketchbook; rolling is per batch.

**Not yet ruled, and it is Anthony's:** `docs/design/launch-plan.md` was written around the
ladder and a ladder pilot. With the ladder retired it no longer describes a route to launch.

**The finding that governs how work is checked here, now at eight instances, and it split
in two on 2026-09-20.** **A real run catches a wrong mechanism:** reading the CLI's code
said a GitHub-shorthand source would inherit the SSH fallback, a fix was built on that, and
the run showed it does not — the shorthand prefers SSH when installing unless an
environment variable no newcomer sets is present. **An independent reader catches a wrong
claim:** every check that ran was of the mechanism and the mechanism was right, while the
sentence written *about* it overstated the blast radius, saying only the author could
install. Codex refused the push over it. No test could have caught that, because the error
was in the prose. Neither substitutes for the other.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push); it reviewed twice this
sitting, returned "not clear to push" first, and was right. Two native players were
dispatched, both returned, both observed on the model and effort requested; neither is
running. Both had their central claim re-checked rather than accepted, and one of the two
proposed an integrity check that was wrong.

**Installed state:** this session loaded 0.142.0 from the plugin cache, the first sitting
to run current text; the tip is now 0.142.1, so the cache is behind again by one release.
Resolve live numbers.

**Standing:** a peer session cannot authorize a push. Change the dispatch contract only for
demonstrated behaviour from real dispatches.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); and from 2026-09-19, by Anthony's ruling that
working notes stay unpublished: `docs/work/product-package/` and
`docs/guide/reference-from-readme.md`. They exist on the Mac Studio only.

**Routing:** the Claude role `kerd-b5-review` was adopted by this session at its 2026-09-19
22:16 arrival from the prepared handoff, and designates its successor against this file
after this save.

**Pickup reading set** (Switch Out, 2026-09-20 midday):
- this file complete: position, the selected continuation and its reason, the rulings;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-20.md`, this sitting's account.
Deeper: `docs/work/first-install/work.md`, the install test's sketchbook, with its view
beside it.

The observed position before this save is the 0.142.1 release commit; the boundary commit
is this save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-20 13:4x: 17,182 bytes across the three sources, about 4,300 tokens
estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-20.md",
 "--section", "TODO.md", "## Now"]
```
