---
route: new
stage: contracted
---

# Time-awareness — slice 1 build spec (honest actuals)

Contract for the time-awareness slice-1 build: the machine consults a clock,
and effort becomes data. Six edits plus a stage flip. Authority:
`docs/design/time-awareness.md` (its edit map and its six stage-1
measurements are binding); frame: `docs/product/time-awareness.md`;
GO record `docs/gates/2026-08-06-time-awareness-design.md`.

All paths relative to `/Users/anthonymaley/Kerd` (call it `$BASE`). Subagent
cwd resets between calls — **every command below uses absolute paths**.
Fenced blocks quote headings, checkboxes and declarations safely: the gate
and progress parsers have been fence-aware since v0.83.1.

**Byte fidelity is load-bearing.** Three non-ASCII characters appear in the
new text and a paraphrase is a build failure:

- `·` U+00B7 MIDDLE DOT — the statusline separator and the per-task line separator
- `–` U+2013 EN DASH — the time range `HH:MM–HH:MM TZ`
- `—` U+2014 EM DASH — prose dashes and the per-task line's leading dash

Every step's `git diff --numstat` expectation was computed against the live
tree at contract time by applying that step's exact text. A numstat that does
not match means the text drifted or something else was touched — treat it as
a step failure, not a rounding error.

**The single-definition law (v0.84.0's, applied to time).** The same-turn
rule gets exactly ONE definition, in `docs/state-contract.md`. Conductor and
switch carry one-line *pointers* at their write moments and zero restatements.
Any edit that re-defines the rule inside a skill file is a build refusal.

Out of scope — a hunk in any of these is a refusal:

- **Retrofits of any `docs/gates/*` record.** A backfilled time is
  manufactured history. `git diff --stat docs/gates/` stays empty (measurement 5).
- **AU/CI rule changes.** The Clock line is documented and deliberately
  unvalidated; graduating it is held by the accepted risk's review trigger
  in `docs/product/time-awareness.md`.
- **Estimates or derived duration views.** Slice 1 builds the actuals base only.
- **Per-step spec timestamps.** Excluded by the frame; per-task is the unit.
- **`hooks/hooks.template.json`.** The statusline is not a hook event — it is
  registered under `statusLine`, never under `hooks`. Confirmed at contract
  time: the template's four events (UserPromptSubmit, Stop, SessionStart,
  PostToolUse) stay exactly as they are.
- **`tests/hooks_test.sh`.** Checked at contract time: its shellcheck test
  names the four hook scripts explicitly (line 380) rather than globbing
  `hooks/*.sh`, and its stop-hook fixture writes its own `conductor: orient`
  line — so a fifth script in `hooks/` and a stamped marker format both leave
  the harness green with no edit. Step 10 runs it to prove that.
- **`skills/tend/SKILL.md`.** Checked at contract time: tend's category-9
  hook hygiene merges entries *from* `hooks/hooks.template.json`; a script
  absent from the template is invisible to it.
- **The three version-field bump and the README What's New entry.** The
  conductor owns both at close-out, not this build.

## Pieces

- [ ] Step 1 — hooks/statusline.sh: new, chainable, stdin-forwarding
- [ ] Step 2 — docs/state-contract.md: the same-turn rule + stamped marker format
- [ ] Step 3 — skills/conductor/SKILL.md: stamped phase marker + close-out actuals
- [ ] Step 4 — skills/switch/SKILL.md: sitting-heading range, per-task lines, banner close time
- [ ] Step 5 — tools/gates/README.md: the Gate records section + optional Clock line
- [ ] Step 6 — README.md: the statusline wiring paragraph
- [ ] Step 7 — docs/product/time-awareness.md: stage sliced → building
- [ ] Step 8 — Diff-review all seven edits (blast radius)
- [ ] Step 9 — Proof obligations: the six stage-1 measurements
- [ ] Step 10 — Full local suite (CI's seven commands + the hook harness)
- [ ] Step 11 — Ship: boxes checked, render refresh, one work commit, one push

### Step 1 — hooks/statusline.sh: new, chainable, stdin-forwarding

`[delegate, model: haiku, effort: low]` — create the new file
`/Users/anthonymaley/Kerd/hooks/statusline.sh`. Nothing else in `hooks/`
changes.

**What** — write EXACTLY this content, then `chmod +x` the file:

```bash
#!/bin/bash
# Kerd statusline segment — the wall clock, composed not claimed.
# Prints HH:MM. Given an existing statusline command as $1, prints
# "HH:MM · <that command's output>", forwarding the context JSON that Claude
# Code puts on stdin, so an occupied statusLine slot keeps working.
# Machine-local, opt-in wiring — see README (Hooks). Not a hook event: it is
# registered under `statusLine`, never under `hooks`.
set -euo pipefail

# A statusline runs on every update. It must go quiet, never crash — the
# path-resolution failure class (v0.29.1) governs here exactly as in hooks.
now=$(date '+%H:%M' 2>/dev/null || true)
[ -n "$now" ] || exit 0

inner="${1:-}"
if [ -z "$inner" ]; then
  printf '%s\n' "$now"
  exit 0
fi

# Claude Code feeds statusline commands a context JSON envelope on stdin.
# Read it once, hand it to the wrapped command unchanged.
payload=$(cat 2>/dev/null || true)
rest=$(printf '%s' "$payload" | /bin/sh -c "$inner" 2>/dev/null || true)

if [ -n "$rest" ]; then
  printf '%s · %s\n' "$now" "$rest"
else
  printf '%s\n' "$now"
fi
```

**Why the shape is what it is** (do not "simplify" any of these — each one
was exercised at contract time):

- Stdin is read **only** when an inner command was passed. A bare
  `bash hooks/statusline.sh` with no pipe must not block, and this ordering
  is what prevents it.
- `/bin/sh -c "$inner"` rather than `eval` or `"$@"`: the argument arrives
  from a settings file as one command string that may carry its own
  arguments, and `sh -c` runs it the same way the harness would.
- Every failure path degrades to the bare clock: a missing inner command, a
  crashing inner command, or empty output all print `HH:MM` and exit 0. The
  statusline never becomes the reason a session looks broken.
- No truncation of the wrapped command's output. The script prefixes what it
  is given and makes no claim about how many lines a statusline may occupy.

**Verify:** from `$BASE`, all five (the first four were run against this exact
script at contract time and produced exactly these results):
`echo '{}' | bash /Users/anthonymaley/Kerd/hooks/statusline.sh | grep -cE '^[0-2][0-9]:[0-5][0-9]$'` prints `1`;
`printf '#!/bin/bash\ncat >/dev/null\necho STUB\n' > /tmp/kerd-stub.sh && chmod +x /tmp/kerd-stub.sh && echo '{}' | bash /Users/anthonymaley/Kerd/hooks/statusline.sh /tmp/kerd-stub.sh | grep -cE '^[0-2][0-9]:[0-5][0-9] · STUB$'` prints `1`;
`bash /Users/anthonymaley/Kerd/hooks/statusline.sh </dev/null; echo "rc=$?"` prints a bare `HH:MM` then `rc=0` (does not hang);
`echo '{}' | bash /Users/anthonymaley/Kerd/hooks/statusline.sh /no/such/cmd; echo "rc=$?"` prints a bare `HH:MM` then `rc=0`;
`shellcheck /Users/anthonymaley/Kerd/hooks/statusline.sh; echo "rc=$?"` prints `rc=0` with no findings;
`test -x /Users/anthonymaley/Kerd/hooks/statusline.sh && echo exec` prints `exec`.

### Step 2 — docs/state-contract.md: the same-turn rule + stamped marker format

`[delegate, model: sonnet, effort: low]` — file:
`/Users/anthonymaley/Kerd/docs/state-contract.md`. Three edits, nothing else
in the file changes. This file is in the release sweep's namespace allowlist
(R3) — the new text contains no bare `/<name>` slash reference. Verified at
contract time: the string `same-turn` appears **0 times** in this file today,
and 0 times anywhere in `skills/`.

**(a) The rule's single definition.** Insert the block below immediately
BEFORE the line `## CONTEXT.md` (currently line 7), keeping one blank line
between the inserted block and that heading:

````markdown
## The same-turn rule (time)

**One definition, here.** Every skill that writes a wall-clock time points at this section; nothing restates it.

A time is written into an artifact only when a machine produced it in the same turn as the write. Two sources, no third: `date` was run in this turn and its output read, or the time was copied from a machine-written record read in this turn — a `conductor: <phase> @ ...` marker stamp, a git commit timestamp. A time the model remembers, infers from the conversation, or estimates from how long the work felt is never written.

Formats: `YYYY-MM-DD HH:MM TZ` for a full stamp (marker lines, gate-record `**Clock:**` lines), `HH:MM TZ` where the date is already established (session-log headings, the switch-out banner), `HH:MM–HH:MM TZ` for a range. Produce them with `date '+%Y-%m-%d %H:%M %Z'` and `date '+%H:%M %Z'`.

**The machine layer checks presence and format only.** A grep can see that a stamp is there and well-shaped; nothing on disk distinguishes a real `date` output from a plausible invention. Time honesty is this frame's declared limit — the retrieval-not-comprehension class. It is held by the write discipline above, not by a checker, and a wrong time is a failure of the discipline rather than of a missing validator.
````

**(b) The `.active-modes` format fence** (in the `## kivna/.active-modes`
section). Old:

```
# One line per skill: <skill>: <state>
conductor: execute
skriv: active
```

New:

```
# One line per skill: <skill>: <state>
conductor: execute @ 2026-08-06 15:17 EDT
skriv: active
```

**(c) One new rule bullet** in the same section, inserted directly after the
existing bullet `- Hooks read this file but never write to it.`:

```
- Conductor's line carries an `@ YYYY-MM-DD HH:MM TZ` stamp (the same-turn rule above). All four readers are prefix-greps (`^conductor:`, `^mode:`), so the suffix is inert to them; `hooks/stop.sh` echoes the whole line, which is how the stamp reaches the human for free.
```

**Why (b) and (c) ride this step:** the state contract is the format
definition of record for `.active-modes`. Stamping conductor's marker in the
skill while leaving the contract's fence showing the unstamped shape is
exactly the doc drift the release pass exists to catch — and it would be
caught in the same session that created it.

**Verify:** from `$BASE`:
`grep -c '^## The same-turn rule (time)$' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `1` (the single definition block);
`grep -c 'same-turn' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `2` (the heading and the new bullet's back-reference — was 0);
`grep -c '^conductor: execute @ 2026-08-06 15:17 EDT$' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `1`;
`grep -c '^conductor: execute$' /Users/anthonymaley/Kerd/docs/state-contract.md` prints `0` (was 1);
`git -C /Users/anthonymaley/Kerd diff --numstat -- docs/state-contract.md` prints exactly `12	1	docs/state-contract.md`.

### Step 3 — skills/conductor/SKILL.md: stamped phase marker + close-out actuals

`[delegate, model: sonnet, effort: medium]` — file:
`/Users/anthonymaley/Kerd/skills/conductor/SKILL.md`. Two edits, nothing else
in the file changes. R3 applies (this file is in the allowlist): the new text
uses `docs/state-contract.md` as a path, and contains no bare slash command.

**(a) Mode Markers — the stamped format.** In the `## Mode Markers` section,
replace this block (fence, example sentence) — old:

````markdown
```
conductor: <phase>
```

Example: `conductor: execute`. Remove the line entirely when closing out (don't write `conductor: closed`). Never touch other skills' lines in this file.
````

new:

````markdown
```
conductor: <phase> @ YYYY-MM-DD HH:MM TZ
```

Example: `conductor: execute @ 2026-08-06 15:17 EDT`. Remove the line entirely when closing out (don't write `conductor: closed`). Never touch other skills' lines in this file.

**The stamp has to be real.** Run `date '+%Y-%m-%d %H:%M %Z'` in the same turn as the write and copy its output — the same-turn rule, defined once in `docs/state-contract.md`. Never write a remembered or inferred time. The `execute` marker's stamp is the first conducted task's start time, which is why it is worth a `date` call rather than a guess.
````

**(b) Close-out — capture the actuals.** In `### 4. Close Out`, insert the
block below immediately BEFORE the paragraph beginning `Close-out settles the
work, then runs the boundary itself` (leave that paragraph and the numbered
list 1–7 that follows it byte-identical — **do not renumber anything**):

````markdown
**Capture the actuals first.** Writing the close-out marker replaces the `execute` line, and that line's stamp is the first task's start time — read the line you are about to overwrite, before you overwrite it. Then, for each task this session committed, produce one line:

```
<task> — started HH:MM (marker) · landed HH:MM (work commit)
```

Start: the `execute` stamp for the first task, the previous task's work-commit time for each task after it. Landed: `git log -1 --format=%cd --date=format:'%H:%M' <sha>`. Both sources are machine-written, which is what makes copying them legal under the same-turn rule (defined once in `docs/state-contract.md`). Hand these lines to the boundary — the Switch Out flow writes them into the session log; conductor never writes the log itself.
````

**Why "read before you overwrite":** `kivna/.active-modes` holds one
conductor line, overwritten at each phase transition. The moment the
close-out marker is written the execute stamp is gone from disk, and no
honest reconstruction of it exists. Capturing it at the transition is the
whole mechanism — everything downstream (the session log's per-task lines,
the sitting heading's open time) reads from that one value.

**Why later tasks derive their start from git:** a session with three tasks
has one execute stamp, not three. Task 2 starts when task 1 landed, and
that instant is already exact in the work commit — so no new write is
needed, and no start time is ever estimated.

**Verify:** from `$BASE`:
`grep -c '^conductor: <phase> @ YYYY-MM-DD HH:MM TZ$' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1`;
`grep -c '^conductor: <phase>$' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `0` (was 1);
`grep -c 'same-turn' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `2` (was 0 — two pointers, zero definitions);
`grep -n 'same-turn' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md | grep -vc 'docs/state-contract.md'` prints `0` (every mention is a pointer at the single definition);
`grep -c 'started HH:MM (marker) · landed HH:MM (work commit)' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1`;
`grep -c '^7\. \*\*Run the boundary\*\*' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md` prints `1` (the numbered list was not renumbered);
`git -C /Users/anthonymaley/Kerd diff --numstat -- skills/conductor/SKILL.md` prints exactly `12	2	skills/conductor/SKILL.md`.

### Step 4 — skills/switch/SKILL.md: sitting-heading range, per-task lines, banner close time

`[delegate, model: sonnet, effort: medium]` — file:
`/Users/anthonymaley/Kerd/skills/switch/SKILL.md`. Four edits, nothing else
in the file changes. **This is the highest-blast-radius step in the build**
— edit (b) is a deliberate replace-all across two nearly identical template
fences. Read edit (b)'s note before touching it.

**(a) The heading rule and the per-task lines.** In `### 3. Write session log
(history)`, insert the two paragraphs below immediately AFTER the existing
line `If appending to an existing file for today (multiple sessions), add a
`---` separator and a new section with a time or sequence number.`:

````markdown
**The sitting heading carries a real time range** — all modes. Shape: `# Session YYYY-MM-DD (<sitting label>, HH:MM–HH:MM TZ)`. Close time: `date '+%H:%M %Z'`, run at the boundary, this turn. Open time: the session's earliest `conductor: <phase> @ ...` marker stamp. If the session had no marker — no conductor ran — there is no honest open time, so write `(<sitting label>, closed HH:MM TZ)` instead. Never estimate the open side; a heading labelled hours wrong is the exact failure this rule exists to remove. The same-turn rule governing every time written here is defined once in `docs/state-contract.md`.

**Per-task actuals.** When conductor conducted this session, its close-out hands over one line per task; put them in `## What Was Done` verbatim, shape `<task> — started HH:MM (marker) · landed HH:MM (work commit)`. Nothing was handed over, nothing is written — switch never reconstructs a start it was not given.
````

**(b) Both session-log templates.** The string `# Session YYYY-MM-DD` starts a
line in **exactly two places** in this file (the full/light template fence and
the low template fence — confirmed at contract time). Replace **both**, and
only those two lines. Old (each):

```
# Session YYYY-MM-DD
```

New (each):

```
# Session YYYY-MM-DD (<sitting label>, HH:MM–HH:MM TZ)
```

Do not touch `# Session — YYYY-MM-DD` shapes elsewhere in the repo, and do
not touch any real session log under `kivna/sessions/` — those are immutable
history and are not this file.

**(c) The banner's fresh reads.** In `### 7. Completion banner`, old:

```
Run `git status` and `git log --oneline -1` fresh. Read the output. Show a completion banner with evidence:
```

new:

```
Run `git status`, `git log --oneline -1`, and `date '+%H:%M %Z'` fresh. Read the output. Show a completion banner with evidence — the `Closed:` line is this turn's `date`, never a recalled time:
```

**(d) The banner body and the low one-liner.** In the same section, insert the
`Closed:` row between `Tree: clean` and `Next:` — the padded line below is 47
characters wide, matching the box art exactly. Old:

```
│  Tree: clean                                │
│  Next: [what to pick up]                    │
```

new:

```
│  Tree: clean                                │
│  Closed: [HH:MM TZ]                         │
│  Next: [what to pick up]                    │
```

And the low-mode one-liner at the end of the same section. Old:

```
Pushed: [commit-hash] → origin/[branch]. Next: [what to pick up]
```

new:

```
Pushed: [commit-hash] → origin/[branch]. Closed: [HH:MM TZ]. Next: [what to pick up]
```

**Why the heading rule spans all modes:** one `date` call is not a token cost
worth a row in the modifier progression table, and a low-mode handoff whose
heading lies about when the sitting ran is exactly as wrong as a full one's.
The modifier table is deliberately NOT edited.

**Verify:** from `$BASE`:
`grep -c '^# Session YYYY-MM-DD (<sitting label>, HH:MM–HH:MM TZ)$' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `2` (both templates);
`grep -c '^# Session YYYY-MM-DD$' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `0` (was 2);
`grep -c 'Closed: \[HH:MM TZ\]' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `2` (banner row + low one-liner);
`grep -c 'same-turn' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `1` (was 0 — one pointer, zero definitions);
`grep -n 'same-turn' /Users/anthonymaley/Kerd/skills/switch/SKILL.md | grep -vc 'docs/state-contract.md'` prints `0`;
`grep -c 'closed HH:MM TZ' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `1` (the honest-omission branch);
`awk '/^│  Closed: \[HH:MM TZ\]/{print length($0)}' /Users/anthonymaley/Kerd/skills/switch/SKILL.md` prints `47` (box art aligned);
`git -C /Users/anthonymaley/Kerd status --porcelain -- kivna/sessions/` prints nothing (no session log was touched);
`git -C /Users/anthonymaley/Kerd diff --numstat -- skills/switch/SKILL.md` prints exactly `9	4	skills/switch/SKILL.md`.

### Step 5 — tools/gates/README.md: the Gate records section + optional Clock line

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/tools/gates/README.md`. One pure insertion; no
existing line changes. **Read this first:** there is no gate-record schema
section in this README today (confirmed at contract time — the sections are
Usage, The gate table, Front-matter schema, Refusals, The spike bypass,
Audit, Release rules, CI, Grounding-was-read, Rigor level, Progress view).
This step creates it. Do not hunt for an existing section to amend.

**What** — insert the block below immediately BEFORE the line `## Refusals`
(currently line 94), keeping one blank line between the inserted block and
that heading:

````markdown
## Gate records

A gate record is a dated file in `docs/gates/` whose name AU3 pins:
`YYYY-MM-DD-<slug>-<rung>.md`. The body is prose for the human — the gate
reads exactly two things from it, both already in the table above: that
the file exists (the `contract` rung's design GO) and, for a goal record,
a `Done condition` section (the `loop` rung).

One optional line is standardized. Directly under the `# ` title:

    **Clock:** YYYY-MM-DD HH:MM TZ

when the record was written. Git already times the commits at both ends
of a rung exactly; the Clock line is the missing end that makes rung
*duration* derivable for new records. Write it under the same-turn rule
(`docs/state-contract.md`): a `date` run in the same turn as the record,
never a remembered time.

**Deliberately not validated.** No rule checks the line — not AU3, not a
rung input. Nothing retrofits it into an existing record either: a
backfilled time is manufactured history. Goal records adopt it first.
Graduating presence to a checked rule is held by the accepted risk's
review trigger in `docs/product/time-awareness.md` ("first observed
missing Clock line in a new record"), not by this README.
````

**Why the section is placed before `## Refusals`:** it sits directly after
`## Front-matter schema`, so the two artifact-shape write-downs (front
matter, then record body) read as one pair before the README turns to what
the gate does with them.

**Verify:** from `$BASE`:
`grep -c '^## Gate records$' /Users/anthonymaley/Kerd/tools/gates/README.md` prints `1`;
`grep -c '\*\*Clock:\*\* YYYY-MM-DD HH:MM TZ' /Users/anthonymaley/Kerd/tools/gates/README.md` prints `1` (was 0 — measurement 5's Clock row);
`grep -c 'Deliberately not validated' /Users/anthonymaley/Kerd/tools/gates/README.md` prints `1`;
`git -C /Users/anthonymaley/Kerd diff --numstat -- tools/gates/README.md` prints exactly `25	0	tools/gates/README.md` (pure insertion — a nonzero deletion count means an existing line was clobbered).

### Step 6 — README.md: the statusline wiring paragraph

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/README.md`. One pure insertion in the `## Hooks`
section; no existing line changes. README is exempt from release rule R3, so
the bare `/tend` in the new text is correct house style here.

**What** — insert the block below immediately BEFORE the line beginning `The
four hooks are covered by a bash test harness` (currently line 212), keeping
one blank line between the inserted block and that line:

`````markdown
**Statusline segment (`hooks/statusline.sh`):** not a hook — it sits beside them and wires into `statusLine`, never into `hooks`. It prints the wall-clock time as `HH:MM`, and it **composes rather than claims** the slot: hand it an existing statusline command as its single argument and it prints `HH:MM · <that command's output>`, forwarding the context JSON on stdin unchanged. Machine-local and opt-in — `/tend` does not register it.

Free slot — point `statusLine` at the script:

```json
"statusLine": {
  "type": "command",
  "command": "/absolute/path/to/Kerd/hooks/statusline.sh"
}
```

Slot already taken — pass the command that is there now as the argument, quoted:

```json
"statusLine": {
  "type": "command",
  "command": "/absolute/path/to/Kerd/hooks/statusline.sh '/absolute/path/to/existing/statusline.sh'"
}
```

Both paths must be absolute and already resolved: `${CLAUDE_PLUGIN_ROOT}` does not expand inside a settings file (the v0.29.1 hook-path gotcha).
`````

**Why the "four hooks" sentence above it does not change:** the statusline is
not a hook and the new paragraph says so in its first clause. The count stays
true.

**Verify:** from `$BASE`:
`grep -ci 'statusline' /Users/anthonymaley/Kerd/README.md` prints `6` (was 0);
`grep -c '^```json$' /Users/anthonymaley/Kerd/README.md` prints `2` (both wiring examples);
`grep -c 'Kerd ships four opt-in hooks' /Users/anthonymaley/Kerd/README.md` prints `1` (the hook count sentence is untouched);
`git -C /Users/anthonymaley/Kerd diff --numstat -- README.md` prints exactly `22	0	README.md` (pure insertion; a nonzero deletion count means an existing line was clobbered — What's New in particular must be untouched, it is the conductor's at close-out).

### Step 7 — docs/product/time-awareness.md: stage sliced → building

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/docs/product/time-awareness.md`. One line in the
front matter. Old:

```
stage: sliced
```

new:

```
stage: building
```

Nothing else in the file changes — the Value section, the risk ledger, the
Release slice, the Grounding list all stay byte-identical.

**Why it rides the first work commit:** the front-matter stage is the
declared rung and `building` is legal under the AU4 value set. Flipping it in
the same commit as the first edits is what keeps the declaration honest
between "the spec exists" and "the pieces landed".

**Verify:** from `$BASE`:
`grep -c '^stage: building$' /Users/anthonymaley/Kerd/docs/product/time-awareness.md` prints `1`;
`grep -c '^stage: sliced$' /Users/anthonymaley/Kerd/docs/product/time-awareness.md` prints `0` (was 1);
`git -C /Users/anthonymaley/Kerd diff --numstat -- docs/product/time-awareness.md` prints exactly `1	1	docs/product/time-awareness.md`;
`python3 /Users/anthonymaley/Kerd/tools/gates/gate.py audit` prints `audit: clean`.

### Step 8 — Diff-review all seven edits (blast radius)

`[keep]` — the conductor reads the full working diff before any proof command
is run. This is judgment: a verify command tests for the presence of the
intended change and is silent about the absence of unintended ones, and every
per-step numstat above can pass while something adjacent is still wrong.

**What** — run `git -C /Users/anthonymaley/Kerd diff` and
`git -C /Users/anthonymaley/Kerd status --porcelain`, read both in full, and
confirm each of the following. Any "no" stops the build and is reported, not
patched over:

- **The file set is exactly seven** — `hooks/statusline.sh` (untracked, new),
  `docs/state-contract.md`, `skills/conductor/SKILL.md`,
  `skills/switch/SKILL.md`, `tools/gates/README.md`, `README.md`,
  `docs/product/time-awareness.md`. Nothing under `docs/gates/`, nothing under
  `kivna/`, nothing in `hooks/hooks.template.json`, nothing in `tests/`,
  nothing in `.claude-plugin/`.
- **Switch's replace-all hit two lines and only two** — the two template
  fences. No other heading, no real session log, no `# Session — YYYY-MM-DD`
  shape elsewhere.
- **Conductor's numbered close-out list is intact 1–7**, unrenumbered, with
  step 7 still `**Run the boundary**`.
- **The same-turn rule is defined once and pointed at three times.** Read the
  three pointer sentences: each one names `docs/state-contract.md` and none
  of them restates what the rule *is*. A pointer that grew into a paraphrase
  is a single-definition-law violation even though every grep above passes.
- **The non-ASCII characters survived.** Read the actual diff bytes for `·`
  (statusline separator, per-task line), `–` (the range), `—` (per-task
  line). An editor that normalized one to ASCII passes several greps and
  breaks the format.
- **No line outside the named anchors moved.** In particular no reflow, no
  trailing-whitespace strip, no blank-line collapse in the long paragraphs of
  either SKILL.md.

**Verify:** from `$BASE`:
`git -C /Users/anthonymaley/Kerd status --porcelain` lists exactly the six tracked modifications plus `?? hooks/statusline.sh`, plus — only if the conductor has not yet committed them — this spec file and the three `docs/plans/progress.*` renders. Nothing else;
`git -C /Users/anthonymaley/Kerd diff --numstat` prints exactly these six rows (order may vary):
`22	0	README.md`, `12	1	docs/state-contract.md`, `1	1	docs/product/time-awareness.md`, `12	2	skills/conductor/SKILL.md`, `9	4	skills/switch/SKILL.md`, `25	0	tools/gates/README.md`;
and the conductor states in one line that it read the full diff and what it checked for — a review that produces no sentence about what it looked for did not happen.

### Step 9 — Proof obligations: the six stage-1 measurements

`[delegate, model: sonnet, effort: low]` — run the design doc's six stage-1
measurements against the built tree and report each one's actual output.
**Do not edit any file in this step.** If a measurement fails, report it and
stop; do not fix.

**Measurements 1 and 2** (statusline standalone and chained) were run in step
1's verify. Re-run them here as part of the set so the six-measurement report
is complete.

**Measurement 3 — the stamped marker, and all four hooks against it.** Build
a throwaway fixture rather than touching the live `kivna/.active-modes`: the
running conductor owns that file, and this build must not clobber its state.

```bash
d=$(mktemp -d)
mkdir -p "$d/kivna/sessions" "$d/.git"
printf 'mode: research (step 1 of 4)\nconductor: execute @ 2026-08-06 15:17 EDT\n' > "$d/kivna/.active-modes"
grep -c '^conductor: execute @ ' "$d/kivna/.active-modes"        # expect 1
for h in stop session-start skill-complete pair; do
  printf '{"tool_response":{"success":true},"tool_input":{"skill":"kerd:switch"}}' \
    | CLAUDE_PROJECT_DIR="$d" bash /Users/anthonymaley/Kerd/hooks/$h.sh >/dev/null 2>&1
  echo "$h rc=$?"                                                 # expect rc=0 for all four
done
printf '' | CLAUDE_PROJECT_DIR="$d" bash /Users/anthonymaley/Kerd/hooks/stop.sh   # expect the line echoed with its stamp
rm -rf "$d"
```

The last command's output must contain `conductor: execute @ 2026-08-06 15:17
EDT` — that is the "the stamp reaches the human for free" claim, and it is
the only evidence for it.

**Measurement 4 — single definition, pointers everywhere else:**

```bash
grep -c '^## The same-turn rule (time)$' /Users/anthonymaley/Kerd/docs/state-contract.md   # expect 1
grep -rn 'same-turn' /Users/anthonymaley/Kerd/skills/ | grep -vc 'docs/state-contract.md'  # expect 0
grep -rc 'same-turn' /Users/anthonymaley/Kerd/skills/conductor/SKILL.md                    # expect 2
grep -rc 'same-turn' /Users/anthonymaley/Kerd/skills/switch/SKILL.md                       # expect 1
```

**Measurement 5 — the Clock row, and no retrofits:**

```bash
grep -c '\*\*Clock:\*\* YYYY-MM-DD HH:MM TZ' /Users/anthonymaley/Kerd/tools/gates/README.md  # expect 1
git -C /Users/anthonymaley/Kerd diff --stat docs/gates/                                       # expect NO output
```

**Measurement 6 — the board's routing is unchanged.** The change adds no gate
inputs for any existing slug. `time-awareness` is excluded from this compare
by construction: its route legitimately advances the moment this spec file
exists on disk, which happened before the build started.

```bash
for s in conductor-boundary grounding-was-read progress-html push-wiring release-closeout rigor-level vault-unhook; do
  printf '%s: ' "$s"
  python3 /Users/anthonymaley/Kerd/tools/gates/gate.py route "$s" | grep '^enters at:'
done
```

Expected, byte-for-byte (captured from the live tree at contract time):

```
conductor-boundary: enters at: loop
grounding-was-read: enters at: loop
progress-html: enters at: goal
push-wiring: enters at: loop
release-closeout: enters at: loop
rigor-level: enters at: loop
vault-unhook: enters at: loop
```

**Verify:** from `$BASE`, all six measurement families produce the expected
output above — the statusline regexes match, `grep -c '^conductor: execute @ '`
on the fixture prints `1`, all four hooks print `rc=0`, stop.sh's output
contains the stamped line, the four measurement-4 counts print `1 / 0 / 2 / 1`,
the Clock grep prints `1`, `git diff --stat docs/gates/` prints nothing, and
the seven `enters at:` lines match the block above byte-for-byte. Report each
family's actual output, not a summary claim.

### Step 10 — Full local suite (CI's seven commands + the hook harness)

`[delegate, model: haiku, effort: low]` — run the suite and report each
command's exact final line. **Do not edit any file in this step.** If anything
fails, report it and stop.

```bash
cd /Users/anthonymaley/Kerd
python3 tools/gates/gate.py selftest
python3 tools/gates/gate.py audit
python3 tools/gates/gate.py release
python3 tools/design/matrix.py selftest
python3 tools/design/matrix.py audit
python3 tools/diagram/progress.py selftest
bash tests/hooks_test.sh
```

`python3 tools/diagram/progress.py stale` is deliberately NOT run here — the
board changes when this spec's boxes get checked, so its refresh belongs to
step 11 and running it now reports a stale board that step 11 is about to fix.

**Why `tests/hooks_test.sh` is in the set even though no hook changed:** the
`.active-modes` line contract spans four files (skill writes it, hook greps
it, test asserts it, switch reads it) and this build changed the first of
those four. The harness is the standing net for that contract — the playbook
gotcha names it by name.

**Verify:** from `$BASE`, each command's final line is, in order:
`gate.py selftest` → a `selftest:` line reporting all cases passed, exit 0;
`gate.py audit` → `audit: clean`;
`gate.py release` → `release: clean`;
`matrix.py selftest` → passing, exit 0;
`matrix.py audit` → clean, exit 0;
`progress.py selftest` → passing, exit 0;
`tests/hooks_test.sh` → its pass summary with zero failures, exit 0.
Any nonzero exit or any `problem:` line stops the build.

### Step 11 — Ship: boxes checked, render refresh, one work commit, one push

`[keep]` — the conductor's own act. Conductor commits and pushes its own work;
this is that commit.

**What**, in order:

1. **Check every box** in this spec's `## Pieces` section — `- [ ]` becomes
   `- [x]` for all eleven steps. The `goal` rung reads zero unchecked boxes as
   its "every piece landed" proxy, and the progress board derives landed
   counts from the same list.
2. **Refresh the board:** `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py`,
   then `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py stale` must
   print `render current`. The board changed because this spec's checklist
   changed — refreshing before the commit is what keeps CI's byte-compare green.
   **Standing note, measured at contract time:** the board went stale the
   moment this spec file appeared on disk, before any build step ran
   (`progress.py stale` named all three renders). So whichever commit first
   carries this spec — the conductor's plan-gate commit or this one — must
   carry a fresh render with it, or CI is red on that push.
3. **Stage by name.** The seven build files, this spec file, and the three
   rendered board files — nothing else. Never `git add -A`. Session state
   (`CONTEXT.md`, `TODO.md`, anything under `kivna/`) never rides a work
   commit; the boundary owns those.
4. **One commit, one push.** Message names the slice and the six edits.
5. **Do not** bump the three version fields and **do not** write a README
   What's New entry — both are the conductor's at close-out, deliberately
   outside this contract.

**Verify:** from `$BASE`:
`grep -c '^- \[ \] ' /Users/anthonymaley/Kerd/docs/plans/2026-08-06-time-awareness-spec.md` prints `0`;
`grep -c '^- \[x\] ' /Users/anthonymaley/Kerd/docs/plans/2026-08-06-time-awareness-spec.md` prints `11`;
`python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py stale` prints `render current`;
`python3 /Users/anthonymaley/Kerd/tools/gates/gate.py route time-awareness | grep '^enters at:'` prints `enters at: goal` (build rung satisfied, goal record not yet written — that is close-out's, not this build's);
`git -C /Users/anthonymaley/Kerd status --porcelain` prints nothing (or only session-state files the boundary owns);
`git -C /Users/anthonymaley/Kerd log --oneline -1` shows the new commit and `git -C /Users/anthonymaley/Kerd status -sb | head -1` shows the branch level with its upstream (pushed).
