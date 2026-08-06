---
route: new
stage: contracted
---

# Conductor-boundary — slice 1 build spec (v0.84.0)

Contract for the conductor-boundary slice-1 build: conductor's close-out
runs the boundary and names what's next. Authority:
`docs/design/conductor-boundary.md` (the 17-edit map and its six stage-1
measurements are binding); frame: `docs/product/conductor-boundary.md`;
GO record `docs/gates/2026-08-06-conductor-boundary-design.md`.
All paths relative to `/Users/anthonymaley/Kerd` (call it `$BASE`).
Subagent cwd resets between calls — every command uses absolute paths.
Fenced blocks below quote headings and checkboxes safely — the gate and
progress parsers are fence-aware since v0.83.1.

Fixture-asserted strings — these appear VERBATIM in the files and in
this spec; any paraphrase is a build failure:

- banner ritual line: `Free context: type /clear, then /kerd:switch in`
- principles bullet opener: `Conductor closes the session it conducted.`
- execute-phase phrase (stage-1 measurement 6 greps for it): `name what's next`

The single-definition law (the frame's killer risk, dissolved
structurally): conductor's text gains ONE instruction to invoke
`/kerd:switch out` via the Skill tool and ZERO descriptions of what the
boundary flow does. The boundary stays defined in exactly one place —
`skills/switch/SKILL.md`, Switch Out. Any conductor edit that
re-describes a switch-out step is a build refusal.

Standing terrain note, observed at contract time: `TODO.md` is modified
in the working tree (mid-session brief capture by the running conductor).
It is session state — the boundary's to commit, never this build's.
Tolerate ` M TODO.md` in every porcelain check below; never stage it,
never revert it.

Out of scope: any `/clear` automation; loops, hooks, scheduling;
light/low modifier changes and boundary auto-sizing; the stop-hook
over-prescription fix; every edit inside switch's `## Switch In` section;
both SKILL.md frontmatter `description` fields (considered by the
design-time sweep, left unchanged); `.github/workflows/`.

## Pieces

- [x] Step 1 — skills/conductor/SKILL.md: the 5-edit map (invoke is literal)
- [x] Step 2 — skills/switch/SKILL.md: 3 edits (single definition + banner ritual line)
- [x] Step 3 — Diff-review both SKILL.md files (blast radius)
- [x] Step 4 — docs/state-contract.md: 4 ownership-row edits
- [x] Step 5 — README.md: conductor + layers re-wordings (+ flagged day-to-day edit)
- [x] Step 6 — README.md: What's New v0.84.0, five-version cap
- [x] Step 7 — docs/playbook.md: switch role line, two-caller phrasing
- [x] Step 8 — Version bump 0.83.1 → 0.84.0 (three fields) + product-doc stage
- [x] Step 9 — Proof obligations: the six stage-1 measurements + collateral
- [x] Step 10 — Full local suite (six gate.yml commands; stale deferred)
- [x] Step 11 — Ship: work commit with boxes checked, render refresh, stale, one push

### Step 1 — skills/conductor/SKILL.md: the 5-edit map (invoke is literal)

`[delegate, model: sonnet, effort: medium]` — file:
`/Users/anthonymaley/Kerd/skills/conductor/SKILL.md`. Five edits, exact
old → new. Touch nothing else — no frontmatter change, no Mode Markers
change, nothing in Orient/Plan/Escalation.

**What:**

**(1) Close-out intro** (§4 first paragraph, after the marker line):

old:

```
Conductor closes the *work*, not the *session boundary*. By now each verified task is already committed and pushed (see [Work commits](#work-commits)); what remains for switch is the session-state commit — the session log and the CONTEXT.md/TODO.md updates below. Keep conductor's close-out short:
```

new:

```
Close-out settles the work, then runs the boundary itself — one act, no handoff ask. By now each verified task is already committed and pushed (see [Work commits](#work-commits)). Keep conductor's close-out short:
```

**(2) Close-out step 5 splits; new step 6 runs the boundary.** The
`[conductor: closed]` marker moves to after the boundary completes.

old (one line):

```
5. **Clear the conductor marker**: remove the conductor line from `kivna/.active-modes`. Output `[conductor: closed]` as the final marker. Never touch the mode line — mode owns its own state.
```

new (two lines):

```
5. **Clear the conductor marker**: remove the conductor line from `kivna/.active-modes`. Never touch the mode line — mode owns its own state.
6. **Run the boundary**: invoke `/kerd:switch out` via the Skill tool — full mode, the standalone default. The flow is defined once, in `skills/switch/SKILL.md` Switch Out; do not re-describe its steps here or anywhere in this file. When it completes, output `[conductor: closed]` as the final marker.
```

**(3) Delete the hand-off paragraph whole** — the paragraph between the
numbered list and `## Principles`, plus one of its surrounding blank
lines so exactly one blank line separates the list from `## Principles`:

```
Then hand off: tell the user to run `/kerd:switch out` to write the session log and make the session-state commit. Conductor does not pull, does not write session logs, and does not call `/kerd:kivna save` — but its own work is already committed and pushed, task by task, so the boundary has only session state left to carry.
```

**(4) Work commits gains the next-pick paragraph.** Insert between the
"Why per-task" paragraph and the `#### No vault writes` heading:

old:

```
Why per-task rather than per-session: the collateral check (verification gate step 5) is only affordable when the diff is small. Three tasks' worth of interleaved change in one boundary commit hides exactly the drift that check exists to catch — a swallowed helper is obvious in one task's diff and invisible in a session's.

#### No vault writes
```

new:

```
Why per-task rather than per-session: the collateral check (verification gate step 5) is only affordable when the diff is small. Three tasks' worth of interleaved change in one boundary commit hides exactly the drift that check exists to catch — a swallowed helper is obvious in one task's diff and invisible in a session's.

**At each task's verified commit, name what's next in one line.** While the plan still has steps, that's the next plan step; when the plan is done, it's the top pick from TODO's `## Now` or `## Backlog`. Suggestion only — starting it stays a human reply; no loop, no hook, no auto-start.

#### No vault writes
```

**(5) Principles bullet** — full replacement (design wording binding):

old:

```
- **Conductor doesn't own the boundary — but it does own its work.** Two kinds of commit, two owners: *work commits* (code and its docs) are conductor's, made and pushed as each task verifies; the *session-state commit* (CONTEXT.md, TODO.md, session log) is switch's, made once at the boundary. No pull, no session log, no vault writes — the vault is on-demand via `/kerd:kivna save`, never part of the flow. Decisions accumulate in CONTEXT.md and flow into the session log when switch runs.
```

new:

```
- **Conductor closes the session it conducted.** Work commits per verified task, then close-out invokes the Switch Out flow (`/kerd:switch out`) as its final act — one definition of the boundary, two callers. Standalone switch out serves sessions without conductor. Conductor still never pulls (pull is switch-in's) and never writes session state by hand.
```

**Why:** the invoke replaces the handoff ask (2 boundary acts → 1); one
instruction to invoke, zero descriptions, so the two callers cannot drift.

**Verify:** from `$BASE`, all five:
`grep -c 'tell the user to run' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `0`;
`grep -c 'kerd:switch out' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `2`;
`grep -c "name what's next" /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1`;
`grep -c 'Conductor closes the session it conducted' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1`;
`grep -c "Conductor doesn't own the boundary" /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `0`.

### Step 2 — skills/switch/SKILL.md: 3 edits (single definition + banner ritual line)

`[delegate, model: sonnet, effort: low]` — file:
`/Users/anthonymaley/Kerd/skills/switch/SKILL.md`. Three edits, exact
old → new. Touch NOTHING inside `## Switch In (Picking Up a Session)`
(it ends at `## Fallback Behavior`) and nothing in Switch Out steps 1–6.

**What:**

**(1) Ownership paragraph** (the bold intro paragraph, line ~10) — full
replacement:

old:

```
**Switch owns `git pull` and the session-state commit.** Nothing else pulls. The session-state commit is CONTEXT.md, TODO.md, and the session log — written and committed once, here, at the boundary.
```

new:

```
**This file is the single definition of the boundary.** Switch-in owns `git pull` — nothing else pulls, ever. Switch Out makes the session-state commit and has two callers: standalone `/kerd:switch out`, and conductor's close-out invoking the same flow as its final act. Either way the steps below are the only definition — no caller re-describes them. The session-state commit is CONTEXT.md, TODO.md, and the session log — written and committed once, here, at the boundary.
```

**(2) Switch Out section intro** — one added line naming the second
caller. Insert after the section's opening paragraph and a blank line,
before `### 1. Update CONTEXT.md (state)`:

old:

```
Wrap up everything so the next session can pick up cold, whether that's a fresh session on this machine or another.

### 1. Update CONTEXT.md (state)
```

new:

```
Wrap up everything so the next session can pick up cold, whether that's a fresh session on this machine or another.

Two callers run this flow: standalone `/kerd:switch out`, and conductor's close-out invoking it as its final act. The steps below are identical either way — the flow cannot tell who called it, and doesn't need to.

### 1. Update CONTEXT.md (state)
```

**(3) Completion banner template** (step 7) — one added line beneath
`Next:`, inside the fenced template. The line overflows the box border;
that is the established shape (the ⚠ triage banner already overflows).
Full fence replacement:

old:

```
┌─────────────────────────────────────────────┐
│  ✓ Switch out complete                      │
│                                             │
│  Pushed: [hash] [message]                   │
│  → origin/[branch] ([N files])              │
│  Tree: clean                                │
│  Next: [what to pick up]                    │
└─────────────────────────────────────────────┘
```

new:

```
┌─────────────────────────────────────────────┐
│  ✓ Switch out complete                      │
│                                             │
│  Pushed: [hash] [message]                   │
│  → origin/[branch] ([N files])              │
│  Tree: clean                                │
│  Next: [what to pick up]                    │
│  Free context: type /clear, then /kerd:switch in  │
└─────────────────────────────────────────────┘
```

The low-mode one-liner is untouched.

**Why:** both callers get the ritual line from the one banner; the
boundary's definition gains its two-caller preamble in the only file
that defines it.

**Verify:** from `$BASE`:
`grep -c 'Free context: type /clear' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `1`;
`grep -c 'single definition' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `1`;
`grep -c 'callers' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `2`.

### Step 3 — Diff-review both SKILL.md files (blast radius)

`[keep]` — read `git -C /Users/anthonymaley/Kerd diff skills/` in full.
The characteristic blast-radius failure is mechanical — an edit range
that swallows a neighbour — and passes every step-level grep. The review
must specifically catch:

1. **Switch In byte-identical** (stage-1 measurement 4, run early so a
   miss dies here, not at Step 9):
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/switch/SKILL.md | sed -n '/^## Switch In (Picking Up a Session)$/,/^## Fallback Behavior$/p') <(sed -n '/^## Switch In (Picking Up a Session)$/,/^## Fallback Behavior$/p' /Users/anthonymaley/Kerd/skills/switch/SKILL.md)`
   — must exit 0 with no output. Any difference: revert the file,
   re-dispatch Step 2.
2. **Switch Out steps 1–6 byte-identical** (standalone flow intact —
   the edits sit before step 1 and inside step 7's fence only):
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/switch/SKILL.md | sed -n '/^### 1. Update CONTEXT.md (state)$/,/^### 7. Completion banner$/p') <(sed -n '/^### 1. Update CONTEXT.md (state)$/,/^### 7. Completion banner$/p' /Users/anthonymaley/Kerd/skills/switch/SKILL.md)`
   — must exit 0 with no output.
3. **Conductor untouched outside the three named regions**:
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/conductor/SKILL.md | sed -n '1,/^#### Work commits$/p') <(sed -n '1,/^#### Work commits$/p' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md)`
   and
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/conductor/SKILL.md | sed -n '/^#### No vault writes$/,/^### 4. Close Out$/p') <(sed -n '/^#### No vault writes$/,/^### 4. Close Out$/p' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md)`
   — both exit 0 with no output.
4. **Diff hunks land only where named**: conductor — close-out intro,
   step 5/6, the deleted hand-off paragraph, the Work-commits insert,
   the one Principles bullet; switch — ownership paragraph, Switch Out
   intro insert, banner fence. Any other hunk (in either file) is a
   refusal: revert, re-dispatch the offending step.
5. **No switch-out step re-described in conductor** — the single-definition
   law: the diff's added conductor lines contain no boundary-step
   description beyond the step-6 invoke instruction.

**Why:** a verify command tests presence of the intended change and is
silent about the absence of unintended ones; the byte-compares are the
proof the design demands.

**Verify:** all four diff commands exit 0 with no output; the hunk-scope
read (items 4–5) is affirmed in one line each.

### Step 4 — docs/state-contract.md: 4 ownership-row edits

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/docs/state-contract.md`. Five exact line
replacements (edits 9–12 of the design map; edit 11 has two sites).
This file is in the release sweep's namespace allowlist — no bare slash
skill references in any new text (none of the texts below contain one).

**What:**

**(9) CONTEXT.md Owner row:**

old: `**Owner:** switch (writes at out), conductor (records decisions during execution)`
new: `**Owner:** the Switch Out flow (standalone, or invoked by conductor close-out), conductor (records decisions during execution)`

**(10) TODO.md Owner row:**

old:

```
**Owner:** conductor (writes session plan into `## Now`), switch (writes wrap-up, runs closure inference)
```

new:

```
**Owner:** conductor (writes session plan into `## Now`), the Switch Out flow (writes wrap-up, runs closure inference — standalone, or invoked by conductor close-out)
```

**(11a) Session-log Owner row:**

old: `**Owner:** switch (creates on out)`
new: `**Owner:** the Switch Out flow (creates on out — standalone, or invoked by conductor close-out)`

**(11b) Session-log sole-creator rule:**

old: `- Switch is the sole creator. Conductor records decisions in CONTEXT.md during execution; switch captures them in the session log at the boundary.`
new: `- The Switch Out flow is the sole creator (either caller). Conductor records decisions in CONTEXT.md during execution; the Switch Out flow captures them in the session log at the boundary.`

**(12) Workflow Ownership git row** — one row becomes three (the work-commits
half was stale since v0.67.0):

old:

```
| Git pull/push/commit | **switch** | No other skill touches git boundaries |
```

new:

```
| Git pull | **switch-in** | Nothing else pulls, ever — pulling mid-session changes files under in-flight work |
| Session-state commit + push | **the Switch Out flow** (standalone, or invoked by conductor close-out) | No other skill commits CONTEXT.md, TODO.md, or session logs |
| Work commits + push | **conductor** (per verified task, since v0.67.0) | Session-state files never ride along in a work commit |
```

**Why:** the ownership rows are the contract other skills route by; the
v0.83.0 goal block proved stale rows here route behaviour.

**Verify:** from `$BASE`:
`grep -c 'Switch Out flow' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `5`;
`grep -c 'Git pull/push/commit' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `0`;
`git -C /Users/anthonymaley/Kerd diff --numstat -- docs/state-contract.md` prints exactly `7	5	docs/state-contract.md`.

### Step 5 — README.md: conductor + layers re-wordings (+ flagged day-to-day edit)

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/README.md`. README shorthand (`/switch out`,
`/clear`) is sanctioned here — keep it. Three substring swaps.

**What:**

**(a) Conductor section, closing sentences (edit 13):**

old:

```
At close-out it updates TODO.md and hands off; switch then writes the session log and makes the session-state commit.
```

new:

```
At close-out it updates TODO.md, then runs the boundary itself — invoking switch out as its final act, one act instead of two — naming the next pick from TODO and offering `/clear` to free context. Standalone `/switch out` remains for conductor-less sessions.
```

**(b) Layers paragraph (edit 14):**

old:

```
**The layers:** Switch owns the session boundary — pull, and the session-state commit. Conductor owns session discipline, and commits its own work as it verifies.
```

new:

```
**The layers:** The session boundary is defined once, in switch — pull on switch-in, the session-state commit at switch out — and has two callers: standalone, or conductor's close-out invoking it. Conductor owns session discipline, commits its own work as it verifies, and closes the session it conducted.
```

**(c) Day-to-day paragraph — FLAGGED: beyond the design's 17-edit map.**
A contract-time terrain find: this sentence still narrates the manual
handoff and becomes false at v0.84.0. Same class as the two routing
documents the v0.83.0 edit map missed. The gate may strike this item
alone — no proof obligation depends on it.

old:

```
When the work is done, conductor's close-out updates TODO.md and hands the boundary back to switch. You run `/slainte docs` to check nothing drifted. Then `/switch out` updates CONTEXT.md and TODO.md (closing done TODO items against session evidence), writes the session log, commits, and pushes.
```

new:

```
When the work is done, conductor's close-out runs the boundary itself — the session log, the state commit, and the push happen as its final act, and the close names the suggested next pick from TODO and offers `/clear`. Run `/slainte docs` any time to check nothing drifted. A session without conductor still ends with `/switch out` directly.
```

**Why:** the public page must describe the one-act close, and the layers
line was the README's copy of the ownership claim this slice re-homes.

**Verify:** from `$BASE`:
`grep -c 'hands off; switch then writes' /Users/anthonymaley/Kerd/README.md` prints `0`;
`grep -c 'Switch owns the session boundary' /Users/anthonymaley/Kerd/README.md` prints `0`;
`grep -c 'hands the boundary back' /Users/anthonymaley/Kerd/README.md` prints `0`;
`grep -c 'closes the session it conducted' /Users/anthonymaley/Kerd/README.md` prints `1`.

### Step 6 — README.md: What's New v0.84.0, five-version cap

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/README.md`. Four exact edits.

**What:**

**(a) Heading:** `## What's New (v0.83.0)` → `## What's New (v0.84.0)`

**(b) Insert** this block immediately before the `### v0.83.0` line
(blank line after the block, so `### v0.83.0` keeps one blank line
above it):

```
### v0.84.0

**A conductor session now ends itself.** Before, conductor's close-out finished by asking you to run `/switch out` — one more prompt to answer, and the session sat quiet until you did. Now close-out runs the boundary as its final act: the session log, the state commit, and the push happen in the same motion, and the close names the suggested next pick from TODO instead of waiting to be told. The completion banner ends with the reset ritual — type `/clear`, then `/switch in` — so freeing context is two keystrokes, never a guess. The boundary flow itself stays defined in exactly one place (switch), so the two callers can't drift apart. Standalone `/switch out` still closes sessions that never ran conductor; switch-in is untouched.
```

**(c) Delete** the entire `### v0.79.0` block (heading + its one
paragraph), leaving exactly one blank line between the `### v0.80.0`
paragraph and the trailing italic line:

```
### v0.79.0

**The progress board becomes a page.** `tools/diagram/progress.py` renders the derived board — every work item's position on the ladder, computed from git log, gate routes, contract checklists, and gate records, never self-reported — as a committed trio: Excalidraw canvas, SVG, and a self-contained HTML page. One serializer writes all three, so converged trees compare equal byte-for-byte.
```

**(d) Trailing line:**

old:

```
*Release notes for v0.78.0 and earlier live in git history — `git log --follow README.md`.*
```

new:

```
*Release notes for v0.79.0 and earlier live in git history — `git log --follow README.md`.*
```

**Why:** release notes keep the last five versions here (v0.82.0
convention); the entry speaks Compare & Contrast — what you did before,
what happens now, what it means.

**Verify:** from `$BASE`:
`grep -c '### v0.84.0' /Users/anthonymaley/Kerd/README.md` prints `1`;
`grep -c '### v0.79.0' /Users/anthonymaley/Kerd/README.md` prints `0`;
`grep -c '^### v0\.' /Users/anthonymaley/Kerd/README.md` prints `5`;
`grep -c 'v0.79.0 and earlier' /Users/anthonymaley/Kerd/README.md` prints `1`.

### Step 7 — docs/playbook.md: switch role line, two-caller phrasing

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/docs/playbook.md`. One line replacement (edit
16). This file is in the release sweep's namespace allowlist — the new
text contains no bare slash skill reference.

**What:**

old:

```
- **switch**: session boundary (pull on arrive; session-state commit+push on leave). Not the only committer — conductor commits its own work per verified task.
```

new:

```
- **switch**: the boundary's single definition (pull on arrive is switch-in's; the Switch Out flow makes the session-state commit for either caller — standalone, or conductor close-out invoking it). Not the only committer — conductor commits its own work per verified task.
```

**Why:** the playbook's architecture list is a routing document — the
v0.83.0 goal block caught exactly this class of line carrying stale
boundary claims.

**Verify:** from `$BASE`:
`grep -c 'either caller' /Users/anthonymaley/Kerd/docs/playbook.md` prints `1`;
`grep -c 'session-state commit+push on leave' /Users/anthonymaley/Kerd/docs/playbook.md` prints `0`;
`git -C /Users/anthonymaley/Kerd diff --numstat -- docs/playbook.md` prints exactly `1	1	docs/playbook.md`.

### Step 8 — Version bump 0.83.1 → 0.84.0 (three fields) + product-doc stage

`[delegate, model: haiku, effort: low]` — MINOR bump: changed behaviour.
Replace `"version": "0.83.1"` with `"version": "0.84.0"` in:

- `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` (one occurrence)
- `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` (BOTH
  occurrences: `metadata.version` and `plugins[0].version`)

All three `description` fields untouched — the capability lists stay
byte-identical ("session discipline, session and machine handoff" still
describes both skills; checked at design time, edit 17).

Plus one line in `/Users/anthonymaley/Kerd/docs/product/conductor-boundary.md`
frontmatter — **FLAGGED: beyond the 17-edit map**, stage-discipline
addition mirroring the vault-unhook goal-gate amendment (its product-doc
stage bump had to be amended in because the contract missed it; this
contract names it up front). The gate may strike it alone:

old: `stage: framed`
new: `stage: building`

**Why:** three synced version fields are release rule R1; the stage line
is what the vault-unhook amendment proved the map forgets.

**Verify:** from `$BASE`:
`grep -c '"version": "0.84.0"' /Users/anthonymaley/Kerd/.claude-plugin/plugin.json` prints `1`;
`grep -c '"version": "0.84.0"' /Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` prints `2`;
`git -C /Users/anthonymaley/Kerd diff -U0 -- .claude-plugin/ | grep -E '^[-+][^-+]' | grep -vc '"version"'` prints `0` (only version lines changed);
`grep -c 'stage: building' /Users/anthonymaley/Kerd/docs/product/conductor-boundary.md` prints `1`.

### Step 9 — Proof obligations: the six stage-1 measurements + collateral

`[keep]` — run the design doc's six stage-1 measurement commands
verbatim on the final tree, then the collateral check. Expected values
below are empirical (baselines measured at contract time), not predicted.
Note: `grep -c` exits 1 when it prints `0` — the printed count is the
check, not the exit code.

1. **Handoff ask 1 → 0:**
   `grep -c 'tell the user to run' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `0` (was `1`).
2. **Single definition:**
   `grep -c 'Update CONTEXT.md (state)\|Heal and self-migrate\|Completion banner' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `0`, and
   `grep -c 'invoke.*kerd:switch out\|invokes.*kerd:switch out' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `2` (design floor: ≥ 1 — the invoke step and the principles bullet).
3. **Both banner lines exist once, in switch:**
   `grep -c 'Free context: type /clear' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `1`, and
   `grep -c 'Free context: type /clear' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `0`.
4. **Pull untouched** — the Switch In byte-compare (Step 3 item 1, same
   command) exits 0 with no output.
5. **Standalone flow intact** — the Switch Out step-heading list is
   unchanged:
   `diff <(git -C /Users/anthonymaley/Kerd show HEAD:skills/switch/SKILL.md | awk '/^## Switch Out/,/^## Switch In/' | grep '^### ') <(awk '/^## Switch Out/,/^## Switch In/' /Users/anthonymaley/Kerd/skills/switch/SKILL.md | grep '^### ')`
   exits 0 with no output (eight headings, `### 1.` through `### 7.`
   with `### 2b.`, identical to parent).
6. **Next-pick naming present:**
   `grep -c 'name what.s next' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1` (design floor: ≥ 1).

Collateral: `git -C /Users/anthonymaley/Kerd status --porcelain` lists
EXACTLY these paths and nothing else (` M TODO.md` is the tolerated
bystander — present unless the boundary committed it meanwhile; its
absence is not a failure):

```
 M .claude-plugin/marketplace.json
 M .claude-plugin/plugin.json
 M README.md
 M TODO.md
 M docs/playbook.md
 M docs/product/conductor-boundary.md
 M docs/state-contract.md
 M skills/conductor/SKILL.md
 M skills/switch/SKILL.md
?? docs/plans/2026-08-06-conductor-boundary-spec.md
```

Any extra path is unintended drift — a refusal, back to the offending
step.

**Why:** these six are the design's named answers; shipping without
them green is shipping an unmeasured contract.

**Verify:** all six measurements plus the collateral list pass exactly
as stated above.

### Step 10 — Full local suite (six gate.yml commands; stale deferred)

`[keep]` — run the `run:` lines from
`/Users/anthonymaley/Kerd/.github/workflows/gate.yml` locally from
`$BASE`, EXCEPT `python3 tools/diagram/progress.py stale` — stale's
natural green moment is after Step 11's render commit; it runs there.
The six, in gate.yml order, with expected outputs (measured at contract
time on the parent tree):

1. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py selftest` → exit 0, `selftest: 26 cases passed`
2. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py audit` → exit 0, `audit: clean`
3. `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py release` → exit 0, `release: clean` (R1: three synced version fields; R2: byte-identical capability lists; R3: no bare skill references in the allowlist sweep — Steps 4 and 7 wrote into swept files)
4. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py selftest` → exit 0, `selftest: 14 ok`
5. `python3 /Users/anthonymaley/Kerd/tools/design/matrix.py selftest` → exit 0, `selftest: 14 ok`
6. `python3 /Users/anthonymaley/Kerd/tools/design/matrix.py audit` → exit 0, `matrix audit: clean (0 matrices)`

**Why:** the local suite is CI run early — a red push is a refusal that
should have happened on this machine.

**Verify:** all six exit 0 with the named outputs.

### Step 11 — Ship: work commit with boxes checked, render refresh, stale, one push

`[keep]` — in order:

1. Set ALL eleven Pieces boxes in THIS spec to `[x]`. Boxes are checked
   IN THE WORK COMMIT, never the render commit — the progress board
   derives from contract checklists, so a box checked after the render
   moves the board the render just drew and the stale gate refuses the
   push (the standing stale-refuser gotcha).
2. Stage by name exactly these nine paths — `TODO.md` is session state
   and MUST NOT be staged:
   `.claude-plugin/marketplace.json` `.claude-plugin/plugin.json`
   `README.md` `docs/playbook.md` `docs/product/conductor-boundary.md`
   `docs/state-contract.md` `skills/conductor/SKILL.md`
   `skills/switch/SKILL.md`
   `docs/plans/2026-08-06-conductor-boundary-spec.md`
3. ONE work commit, message exactly:

```
conductor-boundary slice 1: close-out runs the boundary and names what's next — one definition, two callers (v0.84.0)

Claude-Session: https://claude.ai/code/session_01B7yNRTL9d6oJJQcpLVMaSq
```

4. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py` (the
   refresh).
5. `git -C /Users/anthonymaley/Kerd status --porcelain` — must list ONLY
   progress-render outputs (`docs/plans/progress.excalidraw`,
   `docs/plans/progress.svg`, `docs/plans/progress.html`), plus at most
   the tolerated ` M TODO.md`. Any other path is a refusal: a render
   commit that carries anything else moves the page it just rendered.
6. Stage the three render files by name, commit
   `Refresh progress render` — no trailer, render files only. If the
   refresh produced no render changes, skip this commit.
7. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py stale` →
   exit 0, `render current`.
8. `git -C /Users/anthonymaley/Kerd push` — ONE push carrying both
   commits.

**Why:** work and render stay separate commits so the board's derivation
is provable; one push keeps the boundary discipline.

**Verify:** `git -C /Users/anthonymaley/Kerd status --porcelain` prints
nothing except possibly ` M TODO.md`;
`git -C /Users/anthonymaley/Kerd rev-list origin/main..HEAD --count` prints `0`;
`git -C /Users/anthonymaley/Kerd log -2 --format=%s` shows
`Refresh progress render` above the work-commit subject (or only the
work commit if step 6 was skipped);
`grep -c '\- \[x\]' /Users/anthonymaley/Kerd/docs/plans/2026-08-06-conductor-boundary-spec.md` prints `11`;
the work commit's `git log --format=%B` ends with the `Claude-Session:` trailer.
