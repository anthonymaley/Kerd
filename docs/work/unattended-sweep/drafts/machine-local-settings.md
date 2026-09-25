# Machine-local state: verdict proposal

Backlog row: "Machine-local state has an inventory but no refuser". Proposal only; nothing built, no settings file touched.

## What the machine shows today (2026-09-25, Mac Studio)

- **The doc's own hook grep fails on a healthy machine.** `grep -l kerd ~/.claude/settings.json` prints the file, but the only match is line 146, `"kerd@kerd-marketplace": true`, the enabled-plugin line that §5 step 7 requires. The `hooks` key holds ten events and none mention Kerd. So there is no duplicate hook today, and the check that should say so says the opposite. A check that always complains teaches the reader to ignore it, which is how silent drift survives.
- **Per-repo half is clean and already owned.** The loop over `~/development/product/*/.claude/settings.local.json` prints nothing. Tend's Category 9 already audits that file for stale Kerd hook entries.
- **§4 items:** `kivna/.active-modes` exists (gitignored). `kivna/.pair` exists, holds `on`, and nothing in skills, hooks, tools or tests reads it: the pair hook was removed in 0.141.0. `AGENTS.md` is absent. `~/eolas` is a symlink and `~/eolas/vault` resolves. The Backlog row names `kivna/.pair`; §4 of the doc does not. Both are stale in different directions.
- **The one incident** (session log 2026-08-27): a hand-wired pair hook in the user-global settings file injected old text beside the plugin's. That hook no longer exists in the plugin, so the specific duplicate cannot recur.

## Recommendation: a tiny tools/ script, not a tend category

Hypothesis: `tools/machine_check.py` (stdlib, about 40 lines) will catch the drift class that bit, with no false alarm, because it reads the `hooks` key as JSON instead of grepping the whole file.

It would check: no Kerd hook command in the user-global `hooks` key; no Kerd hook in any repo's `settings.local.json`; the plugin is enabled and its cache version matches the repo; `~/eolas/vault` resolves. It exits non-zero on any failure, and §3, §4 and step 8 of `docs/machine-setup.md` call it instead of the prose greps. It drops `kivna/.pair` from the inventory and flags the orphaned file.

Why not tend: tend runs in one repo's root and converges that repo. The user-global settings file belongs to no repo, and tend already covers the repo-local file. Adding machine config to tend blurs the one line that keeps tend's fixes safe: it only edits what the repo owns.

Why not drop the row: the documented check is broken right now, so "a person runs it" is not even true. Fixing the doc alone would leave a python one-liner in prose again.

Expected result: all green on this machine. A reported Kerd hook would mean the JSON read is wrong.

Cost: one small script, one test, a doc edit, a patch release.

What it does not do: refuse by itself. It runs at a move, when someone runs it. Whether that suffices depends on when drift appears.

> 💬 **Did the duplicate hook in your user settings arrive with the Studio move, or could you have added it by hand during normal use before the move?**
