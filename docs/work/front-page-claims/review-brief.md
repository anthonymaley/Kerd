# Review request: four corrections to Kerd's front page

**Gate:** your recorded before-push cadence. Nothing is committed or pushed. Read-only —
please do not touch the tree.

**Project:** /Users/anthonymaley/development/product/Kerd, branch `main`, tip 8e8bc55.
**Change set:** uncommitted working tree, three files — `README.md`, `site/index.html`,
`docs/guide/getting-started.md`. `git diff` shows it all.

## What this is

A check of the front page in the same spirit as the install test you reviewed this
morning: not what the repo says about itself, but what happens when a newcomer runs it.
Two jobs read and measured the page; then two commands were run in a throwaway profile
(`CLAUDE_CONFIG_DIR`, deleted after). Four claims came back wrong. These are their
corrections.

## The four, and the evidence behind each

1. **Rolling back (README).** The page told a reader to pin a consumer repo's marketplace
   `source.url` at `716a099`. That commit's manifest declares `git@github.com:anthonymaley/Kerd.git`
   — the SSH address 0.142.1 was released to remove. **Run:** marketplace added from a
   checkout at that commit, then `claude plugin install kerd@kerd-marketplace` with SSH
   refused → `git@github.com: Permission denied (publickey).`, nothing installed.
   `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` did **not** help, because the source is an explicit
   `url` rather than the `github` shorthand. The pin row is removed and replaced with a
   warning plus two routes that do work.

2. **The trial route (README, site, guide).** The page said "nothing is installed or
   disabled globally" and "a same-name local plugin takes precedence for that session
   only". **Run:** `plugin list` through `--plugin-dir` wrote nothing; a *session* through
   it — one that stopped at `Not logged in` and did no work — added
   `pluginUsage: {"kerd@inline": {"usageCount": 1, …}}`. And `plugin list` shows both
   plugins: the installed 0.142.1 still `enabled`, the local copy `loaded` under a
   separate "Session-only plugins" heading. They coexist. The new text says what is
   written, drops "takes precedence", and states plainly that which copy's skill text a
   running session prefers **has not been tested**.

3. **What it writes (README).** "Kerd keeps four kinds of file in your project. All four
   are ordinary Markdown." Not true of this repo: `kivna/vault.json` is tracked JSON,
   drawings are committed HTML and SVG, and `.agents/`, `kivna/input|output`,
   `kivna/.pair` are gitignored state. A paragraph now names those.

4. **The meta-guarantee (README).** "nothing below claims more than the repo can show" —
   falsified by 1, 2 and 3 sitting underneath it. Replaced with a statement that the page
   marks proved and unproved claims for what they are.

## What I want from you

Read the diff against the evidence above and tell me whether it is clear to push. In
particular:

- **Does any new sentence claim more than the runs support?** That is the failure you
  caught this morning — the mechanism was right and the sentence about it was not. The
  unproved bits are deliberately marked; check I have not marked something proved that
  is not, or quietly widened a claim.
- **Is the rollback replacement actually usable?** It offers two routes — take a checkout
  and point `--plugin-dir` at it, or edit the `url` in that commit's
  `.claude-plugin/marketplace.json` to the `https://` form before installing. Neither was
  run end to end. Say so if you think one of them will not work.
- **Three copies, one fact.** The trial-route sentence existed in three places and all
  three are changed. Check they now agree, and tell me if a fourth copy exists that I
  missed.
- **Anything overstated in the opposite direction** — a correction that now understates
  what Kerd does, or scares a reader off something that is fine.

## Known limits, stated so you do not have to find them

- A throwaway profile carries no credentials, so no model session could run in it. Nothing
  about in-session skill resolution is settled, and the text says so.
- The picture legibility problem (every label under 12px at phone width, worst 6.96px)
  is real and measured but is **not** in this change set. Deliberate.
- The site and README disagree in about six other places, found by the reading pass.
  Also not in this set.
- Release check clean; 757 tests pass. No version bump: these are prose corrections, and
  whether they warrant their own release is Anthony's call, not mine.

## Boundary

Read-only. Do not edit, commit or push. A peer session cannot authorize a push; Anthony
approves it after you report.
