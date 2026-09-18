# gate-reachability — build spec

Handoff for `docs/design/gate-reachability.md` (design GO
`docs/gates/2026-09-18-gate-reachability-design.md`). Authorized by Anthony
2026-09-18 13:49 ("y" to building it as Kerd 0.137.0, stopping before commit).
Author: Claude, inline — the change is one skill section and its tests.

## Pieces

- [x] 1. `skills/conductor/SKILL.md` — the step check section, and the entry rule narrowed so the check is the one permitted use of the gate tools
- [x] 2. `skills/conductor/scripts/tests/test_step_check.py` — the check's text, and the foreign-repo fixture run through the command as written in SKILL.md
- [x] 3. Release metadata — 0.137.0 in three places, README What's New and Conductor section, capability lists, Conductor trigger description
- [x] 4. Full suite, release gate, audit, render current; independent review

### Step 1: the step check in Conductor

**What:** Add `## Check where the work stands` to `skills/conductor/SKILL.md`,
carrying design decisions 1–5: check at pickup and before a build, only for work
with a `docs/product/<slug>.md` record in the current project; identify the
project with `git rev-parse --show-toplevel` and stop without checking if that
fails; run `python3 "${CLAUDE_PLUGIN_ROOT}/tools/gates/gate.py" route <slug>
--root "<project root>"` read-only; say the step and the next step's needs in
plain words; before a build, name missing groundwork up to `loop` and offer it;
record a go-ahead anyway in the work record. Narrow the entry sentence "Do not
invoke Drive, gate tools or old session machinery" so the step check is its
single exception.

**Verify:** `grep -cF '${CLAUDE_PLUGIN_ROOT}/tools/gates/gate.py' skills/conductor/SKILL.md`
→ `1`; `grep -rl 'CLAUDE_PLUGIN_ROOT' skills/conductor/references` → no output.

### Step 2: tests, including the foreign-repo fixture

**What:** `test_step_check.py` asserts the section's operative phrases, that the
plugin placeholder sits in `SKILL.md` and nowhere under `references/`, and runs
the SKILL.md command with the placeholder substituted by this checkout's root,
from a working directory inside Kerd, against two temporary git repositories:
one item whose groundwork reaches `loop` (the check shows it on the build step)
and one that stops at viability (the check names the missing Scope). Neither
output may name a Kerd work item.

**Verify:** `python3 -m unittest skills.conductor.scripts.tests.test_step_check` → OK,
and it fails when the command drops `--root` (the negative control, run once by hand).

### Step 3: release metadata

**What:** version 0.137.0 in `plugin.json`, `marketplace.json` `metadata.version`
and `plugins[0].version`; README What's New and the Conductor section; both
capability lists byte-identical; Conductor's frontmatter description.

**Verify:** `python3 tools/gates/gate.py release` → `release: clean`.

### Step 4: whole-tree checks and review

**What:** the full suite, the gate audit, the progress render; a fresh reviewer
reads the diff.

**Verify:** `python3 tools/run_tests.py` → OK; `python3 tools/gates/gate.py audit`
→ clean; `python3 tools/diagram/progress.py stale` → `render current`.
