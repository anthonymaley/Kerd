# Playbook: Kerd

How to rebuild this project from scratch.

## Tech Stack

Markdown, JSON, and stdlib Python 3. No third-party dependencies, no build step, no package manager.

- **Claude Code plugin system**: skills (SKILL.md), plugin manifest (plugin.json/marketplace.json)
- **Markdown**: all skill definitions, docs, session logs, and the playbook itself
- **JSON**: plugin.json and marketplace.json in `.claude-plugin/`
- **Git**: version control and the distribution mechanism (plugins install from the git repo)
- **Python 3** (stdlib only, nothing to install): the entry gates (`tools/gates/`), the progress board and diagram generators (`tools/diagram/`), and the design-matrix checker (`tools/design/`) — every CI step is a `python3 tools/…` invocation

There is no package.json, no node_modules, no compiled output. The plugin is consumed directly by Claude Code from the repo.

## Setup

1. Clone the repo:
   ```
   git clone git@github.com:anthonymaley/Kerd.git
   cd Kerd
   ```

2. That's it. There's no install step. The project is markdown and JSON files consumed by Claude Code's plugin system.

3. To test locally, install the plugin in Claude Code:
   ```
   claude plugins install /path/to/Kerd
   ```

4. To install from the marketplace (published version):
   ```
   claude plugins add-marketplace anthonymaley/Kerd
   claude plugins install kerd
   ```

## Architecture

**Skills define behavior.** The plugin system loads them directly via the `kerd:` prefix (e.g., `/kerd:conductor`).

Each skill lives in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`) and the full protocol in markdown. The `description` field controls when Claude auto-invokes the skill.

The plugin manifest (`.claude-plugin/plugin.json`) declares the plugin name, version, and description. The marketplace manifest (`.claude-plugin/marketplace.json`) wraps that for the Claude Code marketplace.

**Directory layout:**
```
skills/           # SKILL.md per skill — nine skills, one folder each
hooks/            # opt-in hooks (hooks.template.json + shell scripts, registered via tend)
hooks/statusline.sh # the clock segment — not a hook; wired via statusLine by hand, never by tend
tests/            # hooks_test.sh
tools/gates/      # entry-gate router and refusers (gate.py, kit.py, fidelity.py)
tools/diagram/    # progress board, journey pages, and diagram generators
tools/design/     # the evaluation-matrix checker
docs/product/     # the funnel board — one <slug>.md per work item, written at the frame stage
docs/design/      # living design docs (undated filenames — CI-enforced)
docs/gates/       # dated gate records, immutable
docs/plans/       # dated contract specs and generated progress renders
docs/playbook.md  # this file
docs/state-contract.md # shared state ownership and format rules
docs/vault-spec.md # what belongs in the Obsidian vault
CONTEXT.md        # current state, overwritten each session
TODO.md           # open work (## Now + ## Backlog)
kivna/vault.json  # Obsidian vault config
kivna/sessions/   # session logs written by switch
kivna/.active-modes # ephemeral mode/skill state (gitignored)
.claude-plugin/   # plugin.json + marketplace.json
.github/workflows/gate.yml # the entry-gate workflow
```

This project keeps an optional Obsidian vault at `~/eolas/vault/kerd/`. It is opt-in and never on the session path (v0.83.0) — a human knowledge base of living files updated in place, not append-only dumps, and not a machine sync layer. Kivna reads and writes vault files (`Kerd Status.md`, plus optional domain files like Architecture Decisions) only when you run `/kerd:kivna save`. The vault spec at `docs/vault-spec.md` defines what belongs. The vault config is at `kivna/vault.json`. See `/kerd:kivna` for details.

**Nine skills, each with a single responsibility, plus four opt-in hooks:**
- **conductor**: session discipline (orient/plan/execute/close-out protocol)
- **interrogate**: risk qualification (tiered risk ledger; exhaustive co-signed interview at the large-bet tier)
- **lorg**: skill gap analysis (tiered subcommands: installed, available, explore, all, report)
- **switch**: the boundary's single definition (pull on arrive is switch-in's; the Switch Out flow makes the session-state commit for either caller — standalone, or conductor close-out invoking it). Not the only committer — conductor commits its own work per verified task.
- **kivna**: knowledge management (Obsidian vault: living Status.md, domain knowledge files, import/export)
- **slainte**: the release close-out pass (triggered by conductor at version bumps and goal-record landings; fixes doc drift under the gate) + on-demand health audits
- **skriv**: human writing voice enforcement (audit, fix, session mode, self-audit pass)
- **tend**: structural health check and convergence
- **pair**: partner-mode toggle (per-repo rapid conversational style, default off)

**Four opt-in hooks** (registered via `/kerd:tend`, stored in `.claude/settings.local.json`):
- **Stop**: reminds about uncommitted changes and active modes on session end
- **SessionStart**: surfaces stale state (remote drift, last session date, interrupted mode) on same-machine resume
- **PostToolUse (Skill)**: shows mode progress when the current step's skill completes (read-only)
- **UserPromptSubmit**: injects partner-mode reminder each prompt while pair is on (read-only)

## Integrations

No external services or APIs. Kerd operates entirely within the local filesystem and git.

The only integration point is the **Claude Code plugin system**. Kerd registers as a plugin and its skills become available as slash commands (`/kerd:conductor`, `/kerd:switch`, etc.).

Session logs written by switch go to `kivna/sessions/` and are committed to git, making them available across machines.

## Deployment

Kerd is distributed as a Claude Code marketplace plugin.

**To publish an update:**
1. Make changes to skills and docs
2. Bump the version in all three locations per the release checklist in CLAUDE.md:
   - `.claude-plugin/plugin.json` → `version`
   - `.claude-plugin/marketplace.json` → `metadata.version`
   - `.claude-plugin/marketplace.json` → `plugins[0].version`
3. Commit and push to `main`
4. Users get the update on next `claude plugins install kerd`

CI is an eight-step entry-gate workflow (`.github/workflows/gate.yml`) running on every push — selftests, repo audit, release rules, progress-render currency, and handoff fidelity. It refuses the push rather than producing anything: still no build artifacts and no environment variables.

## Gotchas

### `git init --bare` points HEAD at `master`, not at your branch

A fixture that works on `main` clones the bare repo into an **unborn `master`
with no upstream**, so `@{u}` fails and any behind-remote check silently reads
as "not behind". This was misdiagnosed in the Backlog for weeks as a sandbox
problem with `git fetch --dry-run` — which emits its `->` line perfectly well.
Fix: `git -C <bare> symbolic-ref HEAD refs/heads/main` (or `init -b main`, which
needs git ≥ 2.28).

### Locating a line by searching the whole file breaks on the second one

`reqview seal` matched `**Approval.** Tony, <date>` across the file. Approve two
requirements on the same day and that string appears twice, so the match is
ambiguous and the second refuses. **Scope to the block first, then edit** —
`reqview.block_span` exists for this and both tools import it.

### A placeholder guard must match every form the placeholder took

The approval guard tested for the exact phrase `"Not yet written"`. Four blocks
carried the migration's *other* boilerplate, `"Partly written — the migrated
source records provenance…"`, so the guard never fired and **Approve was live on
a Why nobody had written.**

### Rendering a diagram needs no Playwright — system Chrome does it

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars \
  --screenshot=out.png --window-size=1100,660 file://<abs-path>.html
```

Enough to look at a drawing before shipping it. **It will not catch the failure
that matters** — see below.

### No check can tell a diagram from a slide

A diagram of prose-in-rectangles passes the source linter, renders perfectly,
and is still worthless. *"Text on the screen with box that made no sense to the
subject."* **A box must mean something.** Pick a type, obey its layout rules,
do not freelance panels. The only reviewer for this is the producer — same
declared limit as reachability, which proves an artifact is there and never
that it was understood.

### `fidelity.py` counts files, not directories

Naming `docs/design/gate-visuals/` in TODO left all four files inside it
unreachable. Name each artifact.


- **A `## Risk ledger` section must be table-only** (2026-08-07): the parser in `tools/gates/kit.py` treats every non-blank line in the section as a data row, so a closing paragraph comes back as "rows 5-9: expected 8 columns, found 1". Same family as the v0.83.1 fence-awareness fix — a structural parser cannot tell commentary from content. Put prose in its own section after the table.
- **`unmitigated` is not a legal risk-ledger state** (2026-08-07): the closed set in `kit.py` `LEGAL_STATES` is `countermeasure - permanent`, `countermeasure - temporary`, `accepted`, `accepted unknown`, `fatal`. This is the machine enforcing the standing "a risk without a countermeasure is a BLOCKER" decision. An honestly-unresolved risk is `accepted unknown` with a non-empty Review trigger, never `unmitigated`.
- **Grounding references must resolve to an on-disk path** (2026-08-07, extended 2026-08-13): AU5 reports "grounding reference does not resolve" for `` `path/to/file.md` `` (backticks) even when the file exists, and also for a URL (`https://…`) — it only resolves local paths. Plain on-disk paths only, `- path — why`; put external-doc citations in prose or risk-ledger evidence, not as a grounding bullet.
- **The sitting's open time is not always the `execute` marker stamp** (2026-08-07): the v0.89.0 rule equates them, but a session that spends real time at frame/plan reaches execute much later. The 2026-08-07 morning sitting opened 08:28 and hit execute at 09:25 — using the execute stamp would have logged 105 minutes as 48. Both stamps are machine-written and same-turn, so the honest range uses the earliest marker written that sitting.
- **The conductor phase marker never advances in a conversational session** (2026-08-07): it goes `orient` → `plan` and stops, because the work flows out of planning with no discrete "now I start building" beat to trigger the restamp at Execute. The cost is the sitting's open time, which becomes unrecoverable — close-out forbids substituting another phase's stamp, so the log carries a close time alone. Framing and design sessions have no execute moment; the instruction assumes one.
- **`${CLAUDE_PLUGIN_ROOT}` expands only inside the plugin's own `hooks.json`** (2026-08-07): it is not an environment variable a skill-issued bash command can read. So "reuse the hooks' pattern" transfers only the *state* half (`$CLAUDE_PROJECT_DIR`, which hooks read at runtime); locating the *script* from a consuming repo needs the resolve-the-absolute-path-at-wiring-time approach `tend` already uses for hook registration.
- **`tac` does not exist on macOS** (2026-08-07): reverse a git log with `git log --reverse`, not by piping through `tac`. The failure is a bare "command not found" that reads like a broken pipeline rather than a missing tool.
- **A workflow joining findings to verdicts on a composite `location|issue` key will fail every row** (2026-08-07): verifier agents reword the issue string, so the key never matches, every finding silently loses its original fields, and a bucket that depends on one of them comes back empty — which reads as a result rather than a bug. Join on location alone, or carry an index through the schema.
- **A new product doc with `stage: framed` front matter turns `gate.py audit` red immediately** if it lacks `## Value` (2026-08-07). Correct behaviour and a useful refusal, but it means dropping a drafted frame into `docs/product/` breaks the push until the Value section is written.
- **SVG does not paste into Excalidraw as editable elements** (2026-08-07): it lands as a flat image and cannot be annotated. The repo's `tools/diagram/kit.py` → `to_svg.py` pipeline is the answer and predates this by weeks — hand-writing SVG bypasses it and produces a canvas nobody can mark up.
- **`progress.py --json` writes three files on every invocation** (2026-08-07), the `--json` path included, with no read-only flag. Anything polling position mid-build dirties the tree and contaminates the collateral diff read. Use `gate.py route`, which is read-only.
- **`html.escape` defaults to `quote=True`** (2026-08-07), which turns `Spec'd` into `Spec&#x27;d` inside a text node. Pass `quote=False` for text; keep the default only for attribute values.
- **The entry gates report requirements cumulatively** (2026-08-07): each stage's list contains every earlier stage's. Render them literally per stage and all eight stages read identically, which looks like a data bug and hides the real one. Show the delta.
- **A rename sweep must be ordered** (2026-08-07): `composer→producer` had to run before `orchestrator→composer`, or the second pass overwrites what the first just wrote. When two renames share a term, sequence them so no target is also a source still waiting its turn.

- **A claim corrected in prose stays alive in the diagram that renders from code** (2026-08-06, release pass v0.88.0): cold eyes falsified a reader-count claim and it was fixed in the design doc — but the same sentence lived in `tools/diagram/gen_*.py`, so the rendered `.excalidraw`/`.svg` kept asserting it, invisible to every markdown grep. When a claim is retired, sweep the generators too, then regenerate; the canvas is downstream of code, not of prose.
- **Nothing machine-checks that the conductor's phase marker is current** (2026-08-06, time-awareness expert-user pass): the marker sat at `plan` from orient through close-out while phases advanced, and the model then reached for an `execute` stamp that never existed — inventing the exact value class the same-turn rule forbids. Write the marker at every phase transition with a real `date`, and never source a time from a marker you did not just read.
- **A build can falsify a doc line that was true at design time** (2026-08-06, cold eyes' sixth-run block): the concept sweep runs against the OLD tree, so a line describing behaviour the build is about to move reads as accurate and never enters the edit map (playbook's slainte-release line credited checks the same commit moved to CI). The design-time sweep needs a companion at goal time — which is exactly the release close-out pass shipped in v0.85.0, firing since its maiden run at the close that shipped it (and at feature closes too since v0.86.0).
- **The edit-map sweep must grep by concept, not by phrase** (2026-08-06, cold eyes' fifth-run block 1): README narrated the dead boundary-handoff in two sentences of the same section with different wording; the design-time cross-cutting sweep's phrase-grep caught one and missed its sibling. When retiring a claim, sweep with multiple phrasings/synonyms of the claim (ownership verbs, hand-off verbs, the old skill name), then read each surviving section WHOLE — a mapped edit's neighbour sentence is the likeliest stale survivor.
- **Composer grep-count predictions keep missing pre-existing terrain** (2026-08-06, three instances across two builds): spec verify steps that predict a count ("exactly three `step [0-9]` hits", "exactly 3 vault.json lines") keep undercounting lines that already existed in the parent tree. The work was correct every time; the contract was wrong. Countermeasure: the composer derives expected counts empirically at spec-write time — run the grep against the tree it just read, never predict from memory of it. (This role was called the orchestrator when the gotcha was recorded — renamed at v0.92.0.)
- **Background-task notifications outlive their session** (2026-08-06): CI watchers launched before a boundary deliver their completion notifications into whatever session is active next — the output-file path names the *originating* session's task directory, which is how to tell them apart. They can carry real signal (one surfaced a red tip), but never treat them as this session's work or as user input. Companion signature: a GitHub Actions outage cancellation shows `conclusion: cancelled` with zero steps run and an empty failure log — check job steps and githubstatus.com before rerunning repeatedly or hunting a gate failure that never executed. Deeper into the same incident the failures stop looking like failures at all: `The job was not acquired by Runner of type hosted`, and then no run object is created for a push whatsoever, so `gh run list --commit <sha>` returns empty rather than red. Absence of a run is not a green tip and not a bug in your workflow — confirm against githubstatus.com and say "unverified", never "passing".
- **Excalidraw paste — the mechanism that actually works** (2026-08-06): the Chrome extension's synthetic cmd+V lands at most once (fresh navigation, canvas focused); writing the scene into localStorage is silently clobbered by Excalidraw's own autosave on reload; the reliable path is in-page JS — `navigator.clipboard.readText()` then dispatch a synthetic `ClipboardEvent('paste', {clipboardData})`. And keep exactly ONE excalidraw.com tab open: two tabs share one saved scene, last writer wins, and the loser's paste vanishes without error.
- **Spec box-checks must not ride the render commit** (2026-08-06, stale refuser's fifth catch): the contract's Pieces checkboxes are part of the derived progress model, so checking boxes inside the "Refresh progress render" commit makes that commit move the very page it just rendered — `progress.py stale` refuses the push. Check boxes in the work commit, or budget a second, pure render commit to converge.
- **gate.py CLI pins root to kit.ROOT** (2026-08-06, cold-eyes trap): run from any other cwd it silently audits the Kerd repo, not your tree — a temp-dir probe can print `audit: clean` having tested nothing. For temp trees, import and call `kit.audit(<root>)` directly.
- **zsh does not word-split unquoted variables** (2026-08-05): a loop running `python3 $cmd` with `cmd="tools/gates/gate.py selftest"` passes ONE argument in zsh — python tries to open a file literally named `gate.py selftest` and every step spuriously FAILs. The tell: the error quotes the whole string as a filename. Fix: `eval` (or zsh's `${=cmd}`). This machine's shell is zsh; bash word-splitting habits lie.
- **`gh run list --limit 1` right after a push can return the PREVIOUS run** (2026-08-04): the new run hadn't registered yet; the stale run "completed" instantly and its step list was one short — nearly signed off the wrong SHA. Verify the run's `headSha` against the pushed SHA before `gh run watch`.
- **A file "already in context" can be a stale snapshot** (2026-08-04): a subagent quoted CLAUDE.md as it stood at its spawn baseline, not after the session's own committed edit to it — the spec it wrote carried a wrong old-string. Validate spec old-strings against disk at execution time; "it's in my context" is not "it's current".
- **`git rm -r` stages the deletion** (2026-08-04): a later ship step's `git add <deleted-path>` fails with "pathspec did not match" — the deletion is already in the index. Stage the *other* files by name; never re-add the deleted path.
- **A player can die mid-step with destructive edits pending** (2026-08-04): an API error killed a subagent between plant and revert during a refusal demo. The tree happened to be clean, but check it before re-dispatching any step that mutates uncommitted files — state-in-artifacts bounds the loss only if you verify the artifacts.
- **A player's verify mismatch can be the player's command retyping, not the work** (2026-08-05): a version-bump player STOPPED on grep output arriving in the wrong order — it had substituted a glob for the spec's explicit file arguments, and glob expansion is alphabetical. The edits were perfect; the spec's expected output was right. Before classifying a failure player-vs-score, the conductor re-runs the spec's verify command EXACTLY as written — the classification is only as good as the reproduction.

- **Canvas coordinates go stale the moment the human touches the camera** (2026-08-04): two band-select attempts in a row operated on a viewport from a previous screenshot — Tony had zoomed from 21% to 116%/128% while adding comments, so the drag landed on empty space (harmless) but could as easily have moved or deleted the wrong elements. Screen coordinates are only valid within the turn that captured them: screenshot immediately before any coordinate-based canvas action, and keep locate→act in one uninterrupted batch. For deletions, prefer clicking individual elements (a miss is a no-op) over rubber-band sweeps, and verify after with select-all → copy → text-diff against the generated files (MISSING catches collateral, EXTRA catches leftovers).
- **`navigator.clipboard.writeText` throws NotAllowedError whenever Chrome is not the OS-focused app** (2026-08-04): driving the canvas from the terminal means Chrome is *never* focused at execution time, so writing the paste payload via page JavaScript fails ("Document is not focused") even though the tab is active. Fix: write the payload to the OS clipboard with `pbcopy`, then send a trusted `cmd+v` through the extension — the paste event reads the system clipboard and needs no clipboard-API permission. Click the canvas first (the existing focus-swallow gotcha still applies to the paste itself).
- **Multiple open Excalidraw tabs silently clobber a paste — last writer wins** (2026-08-04): every excalidraw.com tab shares one localStorage scene; a paste driven into the session's tab vanished when one of Tony's other open Excalidraw tabs saved its older in-memory copy over it. No error anywhere — the package was simply gone from all tabs. Rule: ONE Excalidraw tab open while driving the canvas; have the human close the rest before pasting, and eyeball the scene after (the existing every-paste-needs-eyes rule catches it).
- **A status marker matched by substring means *mentioning* it asserts it** (2026-08-04): the `(?)` = "drafted, not read" marker is detected by `"(?)" in must` in the renderer and counted by grep, so writing "was (?), resolved" in a resolution note re-flagged three settled rows red and inflated the census. Notes about a marker must not quote the marker literally — say "was a guess, resolved". General rule: if a flag is detected by substring, any prose that quotes the flag *is* the flag.
- **Excalidraw reassigns every element id on paste**: any scheme that identifies "whose element is this" by id pattern fails on the first clipboard round trip — after one paste, 209 generated elements read back as foreign. Discovered 2026-08-02 when the round-trip test returned `mine: 0 | NOT mine: 214`; the proposed id-based preservation scheme would have destroyed hand-added annotations on the next regeneration.
- **…and `customData` does not fix it — CORRECTION to the entry above (2026-08-03)**: stamping `customData {gen: "kerd"}` was the fix adopted on 2026-08-02, and it is *also* unreliable, in the opposite direction. `customData` survives copy/paste as claimed, but Excalidraw **propagates it onto newly drawn elements**, so Tony's two hand-typed comments came back tagged `gen: kerd` — the round trip reported `total 91 | kerd 91 | tony 0` while two of them were plainly his. Ids under-claim (everything reads foreign), customData over-claims (everything reads ours). **Neither marker works.** What does: diff the clipboard against the generated file *by text* — anything whose string is not in the generated output is theirs. Better still, make annotations a short-lived queue (read → act → delete, disposition logged) so ownership only has to hold for one cycle.
- **A checker built on your own renderer is structurally blind to the target renderer's interpretation** (2026-08-03): the diagram toolkit renders a review SVG with its own code, and that SVG passed all three layout checks while native Excalidraw was drawing the same arrows as curved loops — `roundness: {"type": 2}` makes Excalidraw curve-fit an orthogonal path (down, across, down) into a blob. Three headless renders in a row missed it; pasting to the real canvas showed it instantly. Set `roundness: None` on lines and arrows. General rule: a mirror can only catch faults *your* code has. Anything the real target interprets differently needs a pass on the real target, so pasting to the canvas is part of the checking loop, not a nicety.
- **A dict keyed on display names silently drops entries when the display name wraps** (2026-08-03): `FUNCTIONS` names carry `\n` for box layout ("Slice a release ·\nSet the goal") while `DETAIL` keys are single-line, so `DETAIL.get(name)` missed and the board rendered a walked, *reviewed* function as never interviewed — no error, just absent detail that looked like "not yet walked" by design. Found only because a membership check ran before adding a new entry. Lookup now normalizes (`name.replace("\n", " ")` both sides, `_detail()`/`_walked()` in `gen_excalidraw.py`). General rule: never key a lookup on a string that also carries presentation (wrapping, casing, punctuation) — normalize at the boundary, and when a lookup's miss-path renders identically to a legitimate empty state, it needs a check that can tell them apart.
- **Two Excalidraw tabs fight over one saved scene — the idle tab clobbers your paste when it regains focus** (2026-08-03): excalidraw.com persists the scene to a single localStorage key per browser profile. Claude pasted the new flow in its own tab; Tony's already-open tab still held the *previous* diagram in memory and wrote it back over the paste the moment he focused it. He then reviewed last session's diagram believing it was the new one ("they look identical to previous ones" — it literally was), and his comments landed on the wrong artifact. No error anywhere — the same silent-failure family as the focus-swallowed paste. Fix: one Excalidraw tab at a time during a review cycle; after pasting, have Tony *refresh* his tab (loads the saved scene) rather than switch to an already-open one. Before any clear-and-paste, diff the canvas texts against the generated file to rescue uncaptured comments.
- **An Excalidraw paste silently does nothing when the canvas does not have keyboard focus** (2026-08-03): after `cmd+A` then `Delete`, focus leaves the canvas, so the following `cmd+V` is swallowed with no error. Worse, `shift+1` (zoom to fit) on an *empty* canvas leaves you at 10% zoom staring at blank space, so it looks exactly like a paste that worked and then vanished. Fix: click the canvas before pasting. **Correction to a claim made earlier the same day** — the first occurrence was attributed to colliding element `index` values, because the retry both re-indexed *and* clicked, and the re-indexing got the credit. Re-indexing is still required when *merging* two generated diagrams (both files start their fractional indices at `a0001`, and ids plus `containerId`/`boundElements` need remapping or bound labels detach), but it was not what unblocked that paste. This is the unqualified-risk pattern applied to a workflow: one observation, a plausible mechanism, written up as established.
- **A layout checker only catches the collision class it was written to imagine** (2026-08-03): `collision_report` compared free text against *rectangles*, so when a requirement row grew from two lines to nine and printed straight through the two rows below it, nothing flagged — the texts sat beside boxes, not on them. Added `text_overlap_report` (text vs text), which immediately found two real faults including one that had been sitting unnoticed. Same shape as the 2026-08-02 "generating visuals you cannot see" gotcha: the blind spot in the checker matched the blind spot in the workflow. When a check passes, ask what class of fault it *cannot* express.
- **zsh does not word-split unquoted variables**: `for x in $VAR` over a space-separated string iterates *once*, with the whole string as one item. Bash splits, zsh does not. This silently produced a "every skill is an orphan" result from a reference-graph script before it was caught (2026-08-02). Use a real array: `skills=(a b c); for s in $skills`.
- **`find ~ -name ...` with no depth limit will exceed the command timeout**: a home-directory-wide search for one filename ran past 120s and had to be backgrounded (2026-08-02). Always scope to specific directories and use `-maxdepth`.
- **Generating a visual artifact you cannot see is a defect, not a caveat**: two diagrams were generated, JSON-validated, and shipped before anyone looked at them. The first render immediately showed a caption sitting on top of a box — the validator only checked *bound* text against its container, so free-floating labels and box stacking were never checked at all. If you generate visuals, render them (headless Chrome on an SVG needs no dependencies) and look before sending. The blind spot in the checker matched the blind spot in the workflow exactly.
- **Focus mode makes mid-turn text invisible — gate messages must carry their content**: Claude Code's native focus mode shows the user only a turn's *final* text message; analysis written between tool calls is never seen. Combined with "don't bury the question under framing"-style brevity rules, a skill that ends a turn on an approval question can collapse to a content-free "execute the plan?" (observed live in ~/3of3, 2026-07-19). Any skill gate that asks for approval must include the findings/summary/plan in the same message as the ask — fixed in conductor v0.65.0 and clarified in the global CLAUDE.md question-formation gate ("findings are not framing").
- **Conductor/switch `## Now` updates must overwrite the whole section, not edit lines**: conductor close-out (and switch-out) are specced to *overwrite* TODO.md `## Now` to forward-only state. Doing it as a surgical line-edit instead leaves stale items behind — a 2026-07-07 close-out replaced the in-flight line but left a pre-existing duplicate below it, so `## Now` carried two near-identical items until the next switch-out's dedup caught it. When rewriting `## Now`, replace the entire section so nothing survives by omission.
- **Version sync**: the version must be identical in three places (plugin.json version, marketplace.json metadata.version, marketplace.json plugins[0].version). Easy to update one and forget the others. The release checklist in CLAUDE.md exists because this happened.
- **Cache busting**: after publishing, Claude Code may cache the old plugin version. Bumping a patch version forces a re-fetch. This is why you see "cache bust" commits in the history.
- **Namespace prefix**: skill SKILL.md frontmatter uses bare names (`name: conductor`), but all references in docs and skills must use `kerd:` prefix (`/kerd:conductor`). The plugin system adds the prefix automatically. README examples are exempt for readability.
- **Tend's hook-hygiene check must read the `"command"` fields, not the whole settings file**: grepping `.claude/settings.local.json` for a cache path (`kerd/<version>/hooks`) matches `permissions.allow` entries too — this repo holds two allow-entries for `sed` commands that re-wired *other* repos to `kerd/0.31.0/hooks`, a version long gone from cache. Read as hook wiring, that looks like three broken hooks; the actual `"command"` values point at `/Users/anthonymaley/Kerd/hooks/` and are correct. Grep the command fields, then confirm each script exists and is executable. Surfaced 2026-08-06 during a release-pass tend run.
- **Vault path convention**: default vault path is `~/eolas/vault/`. Kivna scaffold asks for the location if it doesn't exist. All vault.json files point here. If you rename or move the vault folder, update vault.json in every repo.
- **Vault spec**: the vault spec at `docs/vault-spec.md` defines what belongs in the vault. No symlinks, no append-only files, no generic filenames. When in doubt, check the spec.
- **Cross-cutting changes**: when modifying a pattern used across multiple skills (like vault file references), grep all skill files for the old pattern after implementation. The plan will miss files. The v0.10.0 vault redesign missed `lorg/SKILL.md` entirely, caught only by final code review searching for stale references.
- **Agent verification**: when using parallel agents for cross-file changes, always run a grep verification sweep afterward. Agents can make incorrect inferences (e.g., renaming `discover-sources.json` to `lorg-sources.json` when only the skill name changed, not the vault filename).
- **Verify collision claims**: before renaming a skill to avoid a collision, check the other plugin's actual skill list. The shakh rename was based on an assumed superpowers collision that never existed. A 2-minute scan of `~/.claude/plugins/cache/` would have prevented two unnecessary renames.
- **Vault files need the same rename sweep as repo files**: when renaming a skill, the vault has its own references (MOC, Status, Usage Guide, Architecture Decisions, Install Guide, Lorg Report). Easy to update the repo and forget the vault.
- **Renaming a per-repo state file silently disables the feature in every repo still carrying the old filename**: the `focus → pair` rename (v0.64.0) changed what the global UserPromptSubmit hook greps for (`kivna/.pair`); repos with the old `kivna/.focus` (e.g. 3of3) got partner mode silently switched off — no error anywhere, the hook's guard is just false. A state-file rename needs a migration sweep across every wired repo, same as a hook-path change.
- **Cached plugin version lags**: after pushing changes, the installed plugin still uses its cached version until `claude plugins install kerd` runs again. Skill templates loaded from cache will be old. This is why the switch template in this session loaded v0.21.0 even though the repo was at v0.23.0.
- **Renaming a skill whose docs talk *about* the rename**: a blind global find-replace corrupts the meta-text. When `dian`→`conductor` (v0.59.0), files saying "the dian skill, to be renamed conductor" became "conductor→conductor" nonsense. Split references into **plain** (bulk-replace) vs **meta** (text describing the rename — hand-edit), and docs into **living** (rename) vs **historical** (leave the old name as the record — release notes, CHANGELOG, session logs, superseded design docs). Use `perl -pe 's/\bX\b/Y/g'` for word boundaries — macOS/BSD `sed` has no `\b`. And `\bdian\b` also dodges "Obsidian" (no word boundary inside it).
- **The `.active-modes` line contract spans four files**: a skill's `.active-modes` line is written by the skill, grepped by the session hooks (`hooks/session-start.sh` and `hooks/skill-complete.sh` read `^mode:`), asserted by `tests/hooks_test.sh`, and read by switch. Renaming the line prefix (`dian:` → `conductor:`) must change all in one commit or the hook/test harness breaks quietly. The harness is the safety net — run it immediately after to confirm the contract held. (Before v0.96.0 `hooks/stop.sh` also grepped `^conductor:`; it was cut when hooks moved to plugin auto-load.)
- **Legacy user commands shadow plugin skills**: pre-plugin command files in `~/.claude/commands/` show as duplicate entries in the command picker. Delete them after migrating to the plugin. Common leftovers: `switch.md`, `kivna.md`, `sotu.md` (old slainte name), `human-draft.md` (old skriv), `rigour.md` (old conductor).
- **Hook paths break on plugin version updates** (historical, resolved v0.96.0): hooks wired in `settings.local.json` pointed to absolute cache paths (e.g., `/cache/kerd/0.30.0/hooks/`). When the plugin updated, the path changed and hooks broke. **Resolved by hooks-autoload (v0.96.0):** Kerd hooks now auto-load from the plugin's `hooks/hooks.json`, so there is no cache-pinned path in any repo to go stale — `${CLAUDE_PLUGIN_ROOT}` resolves at runtime. tend category 9 now *removes* leftover manual entries instead of re-wiring.
- **Cache GC breaks pinned hook paths even in repos you never touched** (surfaced 2026-07-11): the wired path doesn't only go stale when *you* update — Claude Code garbage-collects old cache versions, so a repo pinned to `.../kerd/0.41.0/hooks/stop.sh` breaks the moment `0.41.0` is pruned (the cache kept `0.41.1`, not `0.41.0`), and it then errors `Failed with non-blocking status code` on **every** Stop. `~/3of3` sat broken this way. The dev repo (Kerd itself) is immune because its hooks point at the versionless repo path `/Users/<name>/Kerd/hooks/`; only *installed*-plugin repos pin to a cache version. Fix: rewire the dead version to a live one (`sed -i '' 's|kerd/0.41.0/hooks|kerd/<current>/hooks|g' <repo>/.claude/settings.local.json`, verify the target scripts exist), or run `/kerd:tend` category 9. **Resolved v0.96.0 (hooks-autoload):** this entire class is closed — Kerd hooks auto-load from the plugin (`hooks/hooks.json`), so no repo pins a cache-version path any more. The backlogged "staleness check" is moot; tend category 9 now removes stale manual entries rather than re-pointing them. The narrative is kept as the record of why auto-load exists.
- **settings.json validation is all-or-nothing**: a single invalid field anywhere in `~/.claude/settings.json` causes the entire file to be skipped. All plugins, hooks, permissions, and config go with it. The error message ("Files with errors are skipped entirely") is easy to miss. If plugins suddenly stop loading across all repos, check settings.json first. The `"source": "local"` type for `extraKnownMarketplaces` is not valid — use `"github"` (with `repo`) or `"git"` (with `url`).
- **PostToolUse payload is a full envelope**: the stdin payload includes `session_id`, `tool_name`, `tool_input`, `tool_response`, `tool_use_id`, not just `tool_input`. Sed parsers must handle the nesting. Documented in `docs/state-contract.md`.
- **TODO.md / vault Status.md as point-in-time records, not live signals**: facts about *external* state in TODO Context blocks or vault Status (cache versions, install state, third-party system status, deployment status) are snapshots at the time the file was written, not current state. Citing them as live state is a recurring calibration risk — surfaced 2026-05-02 when "cache at 0.32.0" from yesterday's TODO was repeated as if current, when it had been 0.38.0 for days. Pattern fix: when a new session starts and citation of external state is needed, verify against the actual source (run `claude plugins list`, check the actual file mtime, hit the live API) rather than re-quoting the TODO/Status block. Internal-state facts (commits, file paths, code structure) are also snapshots but verifiable cheaply via git log / file reads — same gate applies.
- **Naive `grep '^## '` for verifying markdown section counts**: when a section embeds markdown examples inside a code fence (e.g., interrogate's canonical template embedding `## Scope`, `## Deferred`), naive `grep '^## '` counts code-fence content as headings. Implementation plans should write verifications that match exact heading text (e.g., `grep -n '^## Recitation Gate'`) rather than counting all `^## ` occurrences. Surfaced 2026-05-02 during the interrogate v0.39.0 implementation; no fix needed in repo (plan-design pattern only).
- **A pattern-detecting checker must declare its fence policy at birth**: the gate step parser and AU6 were both fence-blind, so the vault-unhook spec — legitimately quoting the very SKILL.md sections it edited inside code fences — derived `build need 2` over a verified, CI-green build, and the goal record was refused until the parsers went fence-aware (v0.83.1, `_fence_mask` in `tools/gates/kit.py`, fixtures T25/T26). The same class as the 2026-05-02 grep entry above, now at the machine layer with the fix in code. Standing habit: check `gate.py route <slug>` before writing any gate record — the board can honestly refuse a record the keys already earned; fix the machinery, then write the record. Surfaced 2026-08-06 at the vault-unhook goal rung.
- **An incomplete switch-out reads as a clean tree but isn't**: if a prior session did work but never committed, `git status` shows "up to date with origin" (nothing staged) while the working tree holds all the uncommitted work. The tell is the session log's `## Commits: (hash pending)`. Switch-in should treat a populated working tree with no matching commit as an aborted handoff, not a clean pickup. Surfaced 2026-06-16 (the 2026-06-10 v0.40.0 work was found uncommitted on switch-in).
- **TODO.md is forward-only — never demote-and-keep (v0.41.0)**: the Current Session block is overwritten each switch-out, not renamed to `## Previous Session` and kept. The completed record lives in `kivna/sessions/`. A user's TODO hit 378 kb from ~45 accumulated session blocks because the old "Update the Current Session block" wording was read as demote-and-keep. switch out now self-heals stray `## Previous Session`/`## Older Session` blocks into the session logs (rescue-before-delete).
- **Check "this is the status quo" claims against disk before building on them**: a design doc asserted a vault `sessions-of-record/` folder was "already the standard, written by switch." Ground truth: only 1 of 5 cited projects had it, and switch writes to repo-side `kivna/sessions/`. The phrase "formalizes existing behaviour" is exactly what to verify, not trust. Surfaced 2026-06-16 (project-spine spec review).
- **Editing a doc by replacing a heading to insert before it can silently drop the heading** if the `new_string` doesn't faithfully re-include it — and a one-char typo in `old_string` ("Tool" vs "Tony") fails the match outright. When inserting before a section, anchor on a unique line and re-verify the surrounding headers survive. Surfaced 2026-06-28 (self-caught twice that session); reached the playbook only on 2026-07-03 — the switch-out gotcha-mirror step was slipped, which is itself the next gotcha.
- **Switch-out step 5 (mirror gotchas to playbook) can silently slip**: the 2026-06-28 Edit-tool gotcha above lived only in the session log for five days; nothing verified the mirror happened. Older session logs are archives that switch-in stops reading after a session or two, so an unmirrored gotcha is effectively lost. Countermeasure (2026-07-03 context/history-split design): switch-out verifies this session's `## Gotchas` entries have playbook counterparts before committing.
- **`gh run list --commit <short-sha>` silently returns nothing** — the flag needs the full 40-char SHA; a short one matches no runs and errors nowhere. A CI poll loop that treats empty output as "not finished yet" spins forever on this (surfaced 2026-08-13: the first monitor of the v0.97.0 push never fired). Use the full SHA (`git rev-parse HEAD`), and make poll loops match every terminal state rather than only the happy one.
- **A risk-ledger State cell is an exact enum token** — the slice gate refused `accepted (evidence says the risk is empty)` outright; qualifiers and commentary belong in the Evidence column, the State cell carries only the legal token (`countermeasure - permanent` · `countermeasure - temporary` · `accepted` · `accepted unknown` · `fatal`). Surfaced 2026-08-13 when the gate refused the model-effort-advisory frame written by the machinery's own author.
- **A register statement must not OPEN with the meta-line shape** (`**Word**: ...` as its first line) — `parse_register` reads it as an unknown field and AU7 refuses the block. Ambiguity is refused, never guessed (the rule is in the parser's docstring, `tools/gates/kit.py`). Reword the statement's opening; bold mid-statement is fine, the trap is only the `**X**: ` shape as the first statement line.
- **`cd "$VAR" 2>/dev/null || exit 0` is a false safety net under `set -u`**: when `$VAR` (e.g. `CLAUDE_PROJECT_DIR`) is *unset*, the bare deref aborts the script with an `unbound variable` error during expansion — *before* the `2>/dev/null` or `|| exit 0` can fire — so the hook exits 1 with stderr noise instead of degrading silently. (Empty-string is worse-quiet: `cd ""` is a no-op success, so the hook runs in whatever cwd it inherited and reports the wrong repo.) Fix: guard existence before the deref — `[ -n "${VAR:-}" ] || exit 0`. This is the v0.29.1 path-resolution failure class at the script level; all three hooks were hardened + covered by `tests/hooks_test.sh` (v0.41.1). Surfaced 2026-06-25 by an empirical probe, not by shellcheck — shellcheck does not flag it.
- **Run characterization tests RED before fixing**: writing `tests/hooks_test.sh` against the *desired* behavior surfaced two assertions that mis-modeled the hooks' actual (correct) behavior — the report builder capitalizes the first/only message (`Mode interrupted`, not `mode interrupted`), and `next_skill` keeps its leading slash while `current_command` strips it. Running red first caught my wrong tests; had I only confirmed green after fixes, I'd have "fixed" correct code to match wrong tests. Characterization tests must match what the code does, not what you assume.
- **Cross-cutting changes need a final grep across ALL files — plans will miss consumers**: paid out on consecutive cross-cutting changes (dian→conductor rename v0.59.0; context/history split v0.60.0, where `hooks/session-start.sh` grepped `## Current Session` and appeared in no plan slice; **vault-unhook v0.83.0, where the design's four-file edit map missed conductor's close-out text and state-contract — the two documents routing the very behaviour being changed — caught by cold eyes running exactly this grep**). The final grep is the load-bearing step, not a formality — sweep skills/, docs/, hooks/, tests/, README, and the manifests before calling a shape change done. As of v0.83.0 this is a named design-rung obligation for any slice touching system-wide behaviour.
- **An inline `&&`-chain hook in settings.json errors every prompt when its guard is false**: a UserPromptSubmit hook written as `[ -f "$f" ] && grep -qi "^on" "$f" && echo "..."` returns the exit status of the *last command that ran*. When the guard fails (pair off/absent → `[ -f "$f" ]` is false), the `&&` short-circuits and the whole command exits non-zero, so Claude Code prints `hook error / Failed with non-blocking status code` on **every** prompt in that repo. The real `hooks/pair.sh` avoids this with `|| exit 0` guards; the bug appears only when the hook is *inlined* into `~/.claude/settings.json` and the inline copy drifts from the script (loses the guard). Fix: any inline gated hook must end with `; exit 0` (or `|| true`). Prefer pointing the hook at the script over re-inlining. Surfaced 2026-07-06 (pair banner erroring in every repo where pair was off; hook was named `focus.sh` until the v0.64.0 rename). Same care-with-inline-hooks class as the settings.json all-or-nothing and hook-path gotchas above; distinct from the `set -u` unbound-variable class (that's deref-time, this is `&&`-chain exit status).
- **The vault is a separate git repo that Kerd never commits**: `~/eolas/vault` is its own repo and drifts (~20 uncommitted files observed 2026-06-25). Historically switch-out wrote to it every boundary without committing it — superseded at v0.83.0: the boundary no longer writes the vault at all, `/kerd:kivna save` is the deliberate on-demand writer, and the old open question (should switch commit the vault repo?) is moot — switch neither writes nor commits it. Vault git sync remains manual and the vault's own business. Do not blanket-commit the vault from any Kerd flow — most uncommitted files there belong to other work.
- CI (entry-gate workflow) refuses dated filenames in docs/design/ and malformed docs/gates/ record names — the date split is now machine-enforced.
- **A file can be edited, verified, and still unshippable — check `git check-ignore` before speccing edits to it**: AGENTS.md is gitignored (machine-local by declaration), so the mode-cut spec's step edited and verified it, then the ship step's `git add AGENTS.md` would have refused an ignored path. "It's a real file on disk" is not the same claim as "it's tracked"; any spec that stages files by name needs the tracked/trackable check at scoping time. Surfaced 2026-08-04 by the step-9 diff read (the file appeared in no git output despite verified edits).
- **A player will self-judge PASS on a verify whose expected value its output contradicts** — expected values in a spec are load-bearing, and an execution agent under pressure to succeed treats them as advisory (observed 2026-08-04: expected "one hit", got two, reported PASS; the two was correct and the expectation wrong, but the player's job was to STOP). The spec's explicit stop-on-mismatch rule is the countermeasure; the conductor re-checking returned evidence against the spec's literal expected text is the backstop that caught it.

- **`## Criteria`, `## Options`, `## Evaluation matrix` and `## Countermeasures` are TABLE-ONLY.** Prose after a table parses as data rows; prose before one parses as the header. Same family as the risk-ledger gotcha — put commentary in the section above.
- **`tools/design/kit.py`'s row splitter is a naive `split("|")`.** `\|` is not honoured, so an escaped pipe inside a cell splits the row. Hit live 2026-08-08: a countermeasure row became eight columns. Avoid pipes in cell text, or use a block format.
- **`collision_report` calls a box under 420×120 "small" and flags free text overlapping it.** Bound text is exempt. To put a glyph inside a cell, BIND it to the rectangle — drawing it on top scores a fault. `tools/design/kit.py:_marked_box` exists for the case where border and text need different colours, which `Canvas.box` cannot express.
- **A block parser must stop at `## ` as well as `### `.** Otherwise the last block in each section absorbs the following heading into its body. Cost 2026-08-08: six false hash divergences on the register's first parse — the file was correct, the parser was not.
- **A subagent told "STRICTLY READ-ONLY, never modify anything under ROOT" can still write to the repo.** StrictDoc's cache landed in `output/` on 2026-08-08 despite the instruction. Prompt-layer instructions to subagents are guidance, not a sandbox — check `git status` after any workflow that installs or runs a third-party tool.
- **A fact stated in a subagent's brief is indistinguishable, from the outside, from the subagent having read the source.** Surfaced 2026-08-13: a composer was told "an existing register with 51 entries exists — do not read it", cited the number 51 in its output, and an adversarial reviewer then reported a contradiction between the file's clean-room isolation claim and its knowledge of the count. The finding was wrong; the reasoning was sound, because the reviewer could not see the brief. **Any document produced under an isolation constraint must state the provenance of every external fact it cites**, or its own isolation claim is unverifiable by anyone downstream.
- **An acceptance test must quote the SOURCE literal, not the rendered output.** `docs/product/hooks-autoload.md` states the verification as "a fresh session must show `📋 Last session: …`", but the literal in `hooks/session-start.sh:39` is lowercase `last session:` — capitalised at line 63 during message assembly. A grep for the documented string returns nothing and reads as "the hook never fired", which is the opposite of the truth. Surfaced 2026-08-13 while verifying auto-load (it worked).
- **`tac` does not exist on macOS.** Use `git log --reverse` rather than piping through it. The failure is a bare `command not found` that kills the pipeline mid-command (2026-08-13).
- **The conductor marker fails silently over a long conversational session.** `kivna/.active-modes` sat at `orient` for five hours of active work on 2026-08-13, was noticed only by accident, and had to be restamped — making the sitting's open time underivable from the marker. It is gitignored, so no CI step and no hook can refuse a wrong phase; the file is exactly as true as its last write. **When the marker is stale, take per-task times from commit timestamps** (machine-written, trustworthy) and say in the log that the marker failed, rather than writing a heading hours wrong.
- **Self-criticism cannot find omissions — it structurally audits only what made it in.** Measured 2026-08-13 on the requirements draft: the author's own straw-man found five real defects in what it had written and missed three things the producer had said that it had never written; an independent adversarial reviewer, prompted to run the source material *forward*, found all three. **A straw-man that only prunes is half a check** — pair it with an explicit omission pass (walk the source top to bottom, ask what each passage demands that nothing carries) and, for critical work, an independent reviewer.
- **A machine that sleeps kills a long-running subagent mid-write** (2026-08-14, twice in one session). The composer survived because its work had already landed on disk; the view spike lost everything because it was still composing. **For any long agent task, instruct it to write to disk early and often** — that is the difference between an interruption and a restart. Resuming via a message to the same agent preserves its context and is far cheaper than re-briefing.
- **`## Graveyard` appears in a register's prose as well as as its heading**, so splitting the file on that substring silently puts every requirement on the wrong side of the split. Split on the heading form (`\n## Graveyard`). Cost 2026-08-14: a verification that confidently reported 0 live requirements and 39 dead ones.
- **A subagent will invent an illegal front-matter value rather than leave a required field empty** — the view spike wrote `stage: findings`, which is not a legal stage, and it reached the audit unnoticed. Two lessons: a spike's *output* is not a rung and does not belong in the funnel directory at all; and any agent writing a file into a gate-checked directory needs the legal value set in its brief, not just the field name.
- **Writing and parsing are different tests of a file format, and passing one says nothing about the other** (2026-08-14). A requirement format was validated twice by having agents *write* in it and audited twice for fidelity; all four passes missed three defects that a parser found within an hour of existing. Prose inside a structured field is indistinguishable from structure to anything that reads mechanically, and **all three defects produced plausible wrong answers** — one fabricated four phantom dependencies that looked entirely genuine. **A plausible answer is believed where an error is seen**, which is why they survived review. If a format is meant to be machine-read, write the parser before declaring the format done.

## Current Status

**Current state is not kept here.** It lived here as a `**Version:**` line and
a long "Working:" list, and it was a duplicate of `CONTEXT.md` that drifted:
it last claimed v0.95.0, nine skills, four hooks and 26 tests while the repo
was at v0.98.0 with ten skills, three hooks and 22 tests. Two homes for one
fact is how that happens, so there is now one home.

- **What is true now** — `CONTEXT.md` (state, overwritten each session).
- **What is still to do** — `TODO.md` (`## Now` and `## Backlog`).
- **Where each work item sits on the ladder** — `python3 tools/diagram/progress.py`,
  derived from disk and CI-refused if stale.

What stays below is **history**, which is a different kind of fact and does not
go stale — it only stops.

## Release history — stopped 2026-04-25, kept as a record

**This is a changelog, and it is abandoned.** It runs from v0.15.0 to v0.38.0
and stops; every release since is in git and in `CONTEXT.md`. It is left intact
rather than deleted because the entries are real records of when things shipped
and why — that is history, and history is not rewritten.

**A finding worth one decision, not two:** `CHANGELOG.md` is the same artifact,
abandoned earlier (stale at v0.14.0), and the Backlog carries them as two
separate rows. They are one question — does this project keep a hand-written
changelog at all, given git and CONTEXT.md already answer "what shipped when"?
Whatever the answer, it should not be answered twice differently.

> **Editorial note on the v0.34.0-v0.38.0 sequence:** these releases responded to a calibration failure observed in real-world spike work. A subsequent sensei review of the underlying A3 caught that the shipped countermeasures (and the global CLAUDE.md Claim Discipline section) all live at the same granularity the original diagnosis identified as broken — text in markdown files read at turn-start. Honest framing: these releases ship **better text rules + measurement infrastructure** (genuine improvement at the existing granularity), not **a fix to the granularity problem itself**. The granularity gap remains open. See vault `Kerd Skill Lessons.md` for the full recursive-trap analysis.

- v0.38.0: Slainte and tend gain evidence-pointer discipline for audit findings. Each slainte finding requires an Evidence column citing the specific check (file:line, command + output, grep result). Each tend failing/warning finding's Why cell must reference the detecting check AND include a post-fix verification step. Same Claim Discipline shape applied to audit output. Switch was surveyed and considered already covered by v0.33.0 + global Claim Discipline.
- v0.37.0: Conductor gains five claim-discipline additions across all four phases (step-boundary markers within execute for higher-frequency reminders at the granularity where failures happen; pre-flight inventory in orient; plan-step prediction citations; strong-language gate during execute alongside the verification gate; close-out summary discipline). Global `~/.claude/CLAUDE.md` adds a Claim Discipline section with five gates at claim-formation, sourced from the parallel sensei A3.
- v0.36.0: Spike v1.2 — three additions imported from a parallel TPS-A3 investigation (sensei skill converged on the same fix shape from a different methodology). Strong-language gate gains an explicit downgrade vocabulary list. Tripwires fire mid-flow when "✓ verified" / strong language / architectural-from-2-obs are about to be written. Self-audit at close-out counts claims vs. citations against the 33-42% confident-wrong baseline from the 3of3 spike, so we can measure whether gates grip across sessions. Also see new vault file `Kerd Skill Lessons.md` for the full retro and synthesized principles.
- v0.35.0: Spike v1.1 — six structural additions after first real-world dogfood (3of3 tvOS deep-link spike). Setup adds pre-flight inventory and empirical-primitive-first. Try adds per-variant verify, provisional-decline zone (closure claims survive a config change or push-back round before promotion to canonical loss; each entry must enumerate "what would change my mind" and "what I haven't yet tried"), WebFetch-fail-3-alternates with "verified by [URL]" tags on external claims, and matrix trimming. All changes are structural (required artifacts/gates), not prose reminders — addressing the wallpaper-effect of high-frequency identical reminders losing their grip.
- v0.34.0: New `spike` mode for high-uncertainty exploration. Directional but exploratory — no plan, no decomposition. Captures both wins AND losses with evidence in a per-topic spec file. Batch-hard for hardware/long-loop tests (default N+1 variants). Commit graduation at close-out classifies each output as keep-as-is, extract-and-promote, or discard. Includes Removed-from-backlog log for disproven hypotheses.
- v0.33.0: Switch + kivna template refactor. Dropped bracketed fill-in prompts in favor of bare headers in template fences. Added three rules above the fence: anti-hallucination (omit empty optional sections; don't write "None" or "N/A"), okay-not-to-know ("I don't know" is a valid log entry, don't construct plausible explanations), match-vocabulary-to-work (covers code, writing, strategy, sales, research). Same vocabulary fix to kivna Weekly Achievements.
- v0.32.0: Switch auto-commit. Session files (TODO.md, session log, playbook) commit and push without confirmation. Only unexpected/unknown files trigger an INPUT REQUIRED banner. Steps 6-9 collapsed into 6-7.
- v0.31.0: Conductor task framing in plan phase. Decompose request into scoped tasks with acceptance criteria and verification before writing implementation plan. Default one task per session. Fresh-session retry when framing was wrong. Inspired by Backlog.md's spec-driven AI development pattern — borrowed the framing, not the tool.
- v0.30.0: Switch `low` modifier for minimum viable handoffs. Brief TODO (3-5 lines), skeleton session log (What Was Done + What's Next), skip vault/reflection/triage/trim, compressed narration. Switch-in low: pull, TODO current session, latest What's Next, active modes, no conductor offer.
- v0.29.1: Tend hook path resolution fix. ${CLAUDE_PLUGIN_ROOT} doesn't expand in settings.local.json.
- v0.29.0: Lorg dedupe across tiers and explanation quality rules. Mode resume/recovery protocol for stale or compacted context. Kivna do-not-save markers for private session content. State-contract workflow ownership table and conflict resolution rules.
- v0.28.0: Slainte cross-doc claim verification (README vs SKILL.md, playbook vs actual skills, state-contract ownership table, hook template currency). Trim added to maintain mode. CONTRIBUTING.md contributor quality gate. Mode-to-skill composition conventions in playbook.
- v0.27.0: Switch pre-commit summary (shows staged files before committing), untracked file triage (surfaces forgotten files), handoff contract verification on switch-in (flags partial handoffs), evidence-cited final confirmation (commit hash, push target, clean tree), conditional trim suggestion for completed plan docs.
- v0.26.0: Conductor execution discipline: hard verification gate (identify-run-read-confirm), bite-sized plan steps with concrete file paths and verification criteria, 3-fix escalation limit, hard stop on scope creep, critical review before plan approval. Kerd integration: mode-awareness in orient (reads .active-modes, surfaces mode instruction), mode-aware close-out (doesn't claim "done" mid-flow), fixed session-log ownership (conductor writes to TODO.md only, switch owns session logs).
- v0.25.0: Lorg tiered subcommands. Default runs Tier 1 only (installed but unused). Subcommands: installed, available, explore, all, report. Per-tier freshness dates. Incremental report saves.
- v0.24.0: Trim skill (community contribution from Kwanwoo Lee). Post-feature token cleanup: archives completed docs with forward-looking content rescue, prunes CLAUDE.md, cleans memory, trims TODO.md, safety-gated by haiku subagent.
- v0.23.1: Fixed hooks auto-loading bug (renamed hooks.json to hooks.template.json). Full lorg scan.
- v0.23.0: Switch: branch metadata in session logs, first-class Gotchas section, progressive session log loading on switch-in, stronger gotcha capture in reflection step.
- v0.22.0: Skriv: self-audit pass, synonym cycling rule, copula avoidance, chatbot residue cleanup.
- v0.21.0: Lorg ranking (scored results, recency-aware filtering, weak match cutoff). Shared state contract doc at docs/state-contract.md.
- v0.20.0: Kerd Interchange Format (KIF). `/kerd:kivna out` produces `.kif.toon` + `.kif.json`. Repo-grounded exports (TODO, session logs, playbook, vault first, conversation fills gaps). `/kerd:kivna in` parses `.kif.json` with per-section approval. Supports `--full` flag for all sections.
- v0.19.0: Hooks infrastructure (Stop, SessionStart, PostToolUse). Unified `.active-modes` schema. Structured mode steps format. Switch mode snapshot for cross-machine handoff. Tend category 9 (hook hygiene). Slainte release audit category.
- v0.17.1: Mode interactive phase selection (AskUserQuestion), session instructions.
- v0.17.0: Mode skill for workflow routing. 9 starter modes. Community-contributed via PR.
- v0.16.0: Switch `light` modifier for lower-token handoffs.
- v0.15.0: Lorg `report` subcommand.

**Next:**

See `TODO.md`. It is the forward-only work file and it is the only one.
