---
route: new
stage: contracted
---

# CI refusal — release rules — contract spec

**Scope:** widen CI refusal inside Kerd with a new `release` subcommand on the
existing gate tool, enforcing the three mechanically checkable release rules:
(R1) version sync across the three version fields, (R2) capability-list
byte-identity between plugin.json and marketplace plugins[0], (R3) `kerd:`
prefix on slash-command references to Kerd skills in living files. Prompt-layer
only; CI only; no pre-commit hooks; no new skill.

**Acceptance bar:** first CI run green on the real tree; refusal demonstrated
locally BEFORE push (plant a violation → exit 1 → remove → clean), on the
entry-gates canary precedent.

**Boundaries (restated from the intent — do not wander):** no 3of3; no
grounding-was-read; no CHANGELOG revival; no change to the existing AU1–AU4
audit rules; CI only; no new skill; `metadata.description` in marketplace.json
is NEVER checked for identity — it is intentionally a different shape.

## Decision: sibling subcommand, not a wider audit

The three release rules ride a NEW `gate.py release` subcommand backed by
`kit.release_audit(root)`, mirroring `audit`'s exact shape (empty list = clean,
exit 0/1, `--json` dumps the same list). Why not extend `audit`: AU1–AU4 are
the doc-schema sweep and the boundary forbids changing them; mixing release
rules into the same problems list would blur the refusal vocabulary (a version
drift is not a doc-schema problem), and a separate named CI step ("Release
rules") makes the failing domain legible in the GitHub UI without reading logs.
Cost: one extra step in gate.yml — accepted.

## The R3 scope: allowlist, not exclude-list

R3 scans ONLY these living locations (paths relative to repo root):

- `skills/**/*.md` (recursive)
- `modes/**/*.md` (recursive)
- `docs/design/*.md`
- `docs/*.md` (top level ONLY — non-recursive; this is where playbook.md lives)
- `CLAUDE.md`

Everything else is out by construction — notably `docs/plans/`, `docs/gates/`,
`docs/interrogations/`, `kivna/`, `tools/`, and `README.md`.

**Rationale (encode this in the gates README too):**

1. *Immutable dated records never retroactively fail CI.* The real tree
   carries ~90 bare references inside `docs/plans/` dated records (top
   offenders: 2026-03-15-vault-redesign-plan.md ×21,
   2026-02-27-kerd-implementation-plan.md ×20,
   2026-04-04-hooks-and-kif-design.md ×15). Those are history, not living
   guidance. An allowlist is the right failure direction: a NEW dated-record
   directory is automatically excluded; a NEW living directory must be added
   to the gate deliberately.
2. *README.md is excluded entirely.* CLAUDE.md's rule 5 grants README examples
   a shorthand exception ("may omit the prefix for readability"). A machine
   cannot adjudicate which README lines are "examples showing shorthand
   usage", so a mechanical check there would refuse legitimate text. The
   README half of rule 5 stays human-enforced. (Raise-at-gate item — this is a
   deliberate narrowing of rule 5's mechanical coverage.)
3. This spec file itself lives in `docs/plans/` and quotes bare forms below;
   the exclusion protects it and every future spec from self-refusal.

## Refusal-demo protocol (run at Step 9, BEFORE push)

```
python3 tools/gates/gate.py release        # release: clean, exit 0
# plant 1: set .claude-plugin/plugin.json "version" to "0.70.1" (Edit tool)
python3 tools/gates/gate.py release        # problem: version drift … / exit 1
# revert plant 1: Edit "version" back to "0.70.0"
# plant 2: append to CLAUDE.md the line:  Run /tend before commits.
python3 tools/gates/gate.py release        # problem: CLAUDE.md:<n> — bare '/tend' … / exit 1
# revert plant 2: remove that line (Edit tool)
python3 tools/gates/gate.py release        # release: clean, exit 0
```

**TRAP — revert by Edit, never by `git checkout --`.** At demo time the tree
holds the UNCOMMITTED 0.70.0 bump and the uncommitted CLAUDE.md line;
`git checkout -- <file>` would silently destroy them (plugin.json back to
0.69.0). Both plants are reverted by editing the value back, and Step 9's
verify closes with a `git diff` inspection to prove no demo residue.

## Pieces

- [x] Step 1: kit.py — release rules R1–R3 + selftest T13/T14
- [x] Step 2: gate.py — `release` subcommand
- [x] Step 3: gate.yml — Release rules CI step
- [x] Step 4: fix the live bare references (checker-driven; two mention-not-use hits reworded to `/<skill>` placeholder by conductor decision per the R3 false-positive rule)
- [x] Step 5: tools/gates/README.md — document the release sweep (one re-dispatch: CI-section "bare" phrase + R3 row gloss)
- [x] Step 6: CLAUDE.md — one enforcement line in the Release Checklist
- [x] Step 7: version bump 0.69.0 → 0.70.0 in the three fields
- [x] Step 8: full local gate — selftest + audit + release all clean
- [x] Step 9: refusal demo — plant → exit 1 → revert → clean (replayed inline after a player API death; tree checked clean first)
- [ ] Step 10: collateral diff review
- [ ] Step 11: commit staged by name, push, watch CI green

### Step 1: kit.py — release rules R1–R3 + selftest T13/T14 [delegate, model: sonnet, effort: high]

**What:** In `/Users/anthonymaley/Kerd/tools/gates/kit.py`:

1. Add `import json` to the imports (currently `glob`, `os`, `re`, `tempfile`).

2. Add a new section after the audit section (after `def audit(root)`, before
   the selftest section), header comment `# ── release rules (R1–R3) ──`, with
   exactly these functions:

   ```python
   def _release_files(root):
       """Load .claude-plugin/plugin.json and .claude-plugin/marketplace.json.
       Returns (plugin, marketplace, problems). When NEITHER file exists:
       (None, None, []) — vacuous pass, a tree without plugin metadata is not
       in violation. Otherwise each path that is absent or fails json.load
       contributes the problem '<relpath> — missing or invalid JSON' and
       loads as None."""
   ```
   Implementation: check both absolute paths with `os.path.isfile`; if both
   missing return `(None, None, [])`. Else for each of
   `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (always
   forward-slash relpaths in messages): try `json.load`; on missing file or
   `ValueError`, append the problem and carry `None`.

   ```python
   def _release_versions(plugin, marketplace):
       """R1 — the three version fields must be identical: plugin['version'],
       marketplace['metadata']['version'], marketplace['plugins'][0]['version'].
       A None document contributes nothing (its load problem is already
       reported). Missing/non-string field → one problem naming it. All three
       present but not all equal → ONE problem showing all three values."""
   ```
   Exact problem strings:
   - `.claude-plugin/plugin.json — 'version' missing`
   - `.claude-plugin/marketplace.json — 'metadata.version' missing`
   - `.claude-plugin/marketplace.json — 'plugins[0].version' missing`
   - `version drift — plugin.json='<a>' metadata.version='<b>' plugins[0].version='<c>' (all three must match)`
   Guard shapes defensively: `(marketplace.get("metadata") or {})`,
   `plugins[0]` only when `plugins` is a non-empty list of dicts. Emit the
   drift line only when all three values were found (`len(vals) == 3`).

   ```python
   def _release_capability(plugin, marketplace):
       """R2 — plugin['description'] must be byte-identical to
       marketplace['plugins'][0]['description']. metadata.description is
       NEVER read — it is intentionally a different shape (marketplace
       one-liner), and checking it would homogenize what CLAUDE.md says to
       keep distinct."""
   ```
   Exact problem strings:
   - `.claude-plugin/plugin.json — 'description' missing`
   - `.claude-plugin/marketplace.json — 'plugins[0].description' missing`
   - `capability-list drift — plugin.json description != plugins[0].description (first differs at char <i>; metadata.description is exempt by design)`
   where `<i>` is the first index at which the strings differ (the shorter
   length when one is a prefix of the other). Compare only when both are
   strings.

   ```python
   def _skill_names(root):
       """Sorted names of skills/<name>/ directories that contain SKILL.md.
       Derived from the tree, not hardcoded — a new skill extends R3
       automatically, with no list to drift."""
   ```

   ```python
   def _release_namespace(root):
       """R3 — scan the living-file allowlist for bare slash references to
       Kerd skills. The correct form is /kerd:<name>; a bare /<name> is a
       violation. Allowlist (see spec): skills/**/*.md, modes/**/*.md,
       docs/design/*.md, top-level docs/*.md, CLAUDE.md. docs/plans/,
       docs/gates/, kivna/, README.md are out by construction — immutable
       dated records never retroactively fail CI; README's shorthand
       exception is human-adjudicated."""
   ```
   Implementation (this is the load-bearing part — use exactly this pattern):
   ```python
   pat = re.compile(r'(?<![\w:/.\-])/' + re.escape(name) + r'\b')
   ```
   The lookbehind kills the false-positive classes on the real tree: file
   paths (`skills/tend/SKILL.md` — `/` preceded by a word char), double
   slashes, `kerd:`-prefixed forms (`/kerd:tend` contains no `/tend`
   substring), and relative paths (`./`, `../`). Collect targets:
   `glob.glob(os.path.join(root, d, "**", "*.md"), recursive=True)` for `d`
   in `("skills", "modes", os.path.join("docs", "design"))`, plus
   `glob.glob(os.path.join(root, "docs", "*.md"))` (non-recursive), plus
   `CLAUDE.md` if it exists. Read each file line by line
   (`enumerate(f, start=1)`); for each skill name whose pattern matches a
   line, append exactly:
   - `<relpath>:<lineno> — bare '/<name>' (write '/kerd:<name>')`
   (relpath via `os.path.relpath(path, root)`; one problem per (line, name),
   not per occurrence). If `_skill_names` returns empty, return `[]`.

   ```python
   def release_audit(root):
       """Release-rules sweep (R1–R3). Empty list = clean. R1/R2 skip
       vacuously when neither plugin file exists; R3 runs regardless (it
       depends only on the tree)."""
   ```
   Body: `plugin, marketplace, problems = _release_files(root)`; if any of
   the three is truthy/non-None, extend with `_release_versions` then
   `_release_capability`; always extend with `_release_namespace(root)`;
   return the list.

3. Extend the selftest with two cases appended at the end of
   `_selftest_body()` (after T12), each in its own temp tree:

   **T13 — planted release problems.** Write:
   - `.claude-plugin/plugin.json` = `{"name": "kerd", "version": "1.0.0", "description": "caps A"}`
   - `.claude-plugin/marketplace.json` = `{"metadata": {"description": "one-liner, different by design", "version": "1.0.1"}, "plugins": [{"version": "1.0.0", "description": "caps B"}]}`
   - `skills/tend/SKILL.md` = `"Run /tend to converge.\nThe path skills/tend/SKILL.md stays clean.\n"`
   Then `problems = release_audit(root)`; assert `len(problems) == 3` (the
   count is itself the metadata.description-exemption proof: it differs from
   both capability lists yet adds no fourth problem), and assert one problem
   contains `"version drift"`, one contains `"capability-list drift"`, one
   contains `"bare '/tend'"`.

   **T14 — clean tree with exclusion guards.** Write:
   - `.claude-plugin/plugin.json` = `{"name": "kerd", "version": "1.0.0", "description": "caps A"}`
   - `.claude-plugin/marketplace.json` = `{"metadata": {"description": "different one-liner", "version": "1.0.0"}, "plugins": [{"version": "1.0.0", "description": "caps A"}]}`
   - `skills/tend/SKILL.md` = `"Use /kerd:tend here.\nSee skills/tend/SKILL.md for the source.\n"`
   - `docs/plans/2026-01-01-old-plan.md` = `"Historic record: we ran /tend that day.\n"`
   - `kivna/sessions/2026-01-01-session.md` = `"session log: /tend output pasted\n"`
   Assert `release_audit(root) == []` — proving in one case: prefixed form
   passes, path text passes the lookbehind, and both excluded directories
   stay excluded.

4. Update the counts: `selftest()` docstring `"Run the 12 fixture-built
   cases"` → `14`, and the success print → `"selftest: 14 cases passed"`.

**Why:** every decision lives in kit.py with `root` as a parameter precisely so
fixtures can drive it in temp trees; the three rules become functions the same
way AU1–AU4 did, and the fixtures pin the exact message formats the demo and CI
will rely on.

**Verify:**
```
python3 /Users/anthonymaley/Kerd/tools/gates/gate.py selftest
```
Expected: `selftest: 14 cases passed`, exit 0. Then against the real tree:
```
cd /Users/anthonymaley/Kerd && python3 -c "import sys; sys.path.insert(0,'tools/gates'); import kit; [print(p) for p in kit.release_audit(kit.ROOT)]"
```
Expected: ONLY `bare '/<name>'` lines (versions are in sync at 0.69.0 and the
capability lists are byte-identical today), all from allowlist paths —
terrain evidence says ~5: skills/tend/SKILL.md ×3, skills/trim/SKILL.md ×1,
skills/slainte/SKILL.md ×1. The refined regex is authoritative and the count
MAY differ from the crude grep's 5; what must hold is: zero lines from
docs/plans/, docs/gates/, kivna/, or README.md.

### Step 2: gate.py — `release` subcommand [delegate, model: haiku, effort: low]

**What:** In `/Users/anthonymaley/Kerd/tools/gates/gate.py`:

1. Docstring: add the usage line after the `audit` line:
   `    python3 tools/gates/gate.py release [--json]`
   and extend the prose paragraph after "audit is the repo-wide mechanical
   sweep: exit 0 clean, 1 with problems." with: `release is the release-rules
   sweep (version sync, capability-list identity, kerd: namespace): exit 0
   clean, 1 with problems.`

2. Add `_cmd_release`, an exact structural mirror of `_cmd_audit` (same
   `--json` handling, same argv guard returning 2):
   ```python
   def _cmd_release(argv):
       as_json = "--json" in argv
       argv = [a for a in argv if a != "--json"]
       if argv:
           print(__doc__)
           return 2
       problems = kit.release_audit(kit.ROOT)
       if as_json:
           print(json.dumps(problems))
           return 0 if not problems else 1
       if not problems:
           print("release: clean")
           return 0
       for p in problems:
           print(f"problem: {p}")
       print(f"release: {len(problems)} problems")
       return 1
   ```

3. Register `"release": _cmd_release` in `COMMANDS` (after `"audit"`).

**Why:** gate.py only parses argv and renders kit's data — the new subcommand
adds zero decisions, keeping the render/decide seam intact for the progress
view's `--json` consumers.

**Verify:**
```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py release; echo "exit=$?"
```
Expected (live violations not yet fixed): one `problem: skills/...` line per
bare reference, then `release: <n> problems`, `exit=1`. And
`python3 tools/gates/gate.py release --json` prints a JSON array of the same
strings, exit 1.

### Step 3: gate.yml — Release rules CI step [delegate, model: haiku, effort: low]

**What:** In `/Users/anthonymaley/Kerd/.github/workflows/gate.yml`, append a
third step after `Repo audit`, same indentation:
```yaml
      - name: Release rules
        run: python3 tools/gates/gate.py release
```
No other changes — no setup-python (the tool stays zero-dependency on
ubuntu-latest's python3), no trigger changes.

**Why:** a separately named CI step makes a release-rule refusal legible from
the GitHub checks UI without opening logs — the failing domain is the step
name.

**Verify:**
```
python3 -c "import yaml,sys; d=yaml.safe_load(open('/Users/anthonymaley/Kerd/.github/workflows/gate.yml')); steps=d['jobs']['gate']['steps']; print([s.get('name') for s in steps])" 2>/dev/null || grep -c "gate.py" /Users/anthonymaley/Kerd/.github/workflows/gate.yml
```
Expected: `[None, 'Gate selftest', 'Repo audit', 'Release rules']` (or, on the
grep fallback if PyYAML is absent: `3`).

### Step 4: fix the live bare references (checker-driven) [delegate, model: sonnet, effort: medium]

**What:** Run `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py release`
and fix EVERY reported problem — the checker's output is the work list, not
the crude-grep counts (skills/tend ×3, skills/trim ×1, skills/slainte ×1 are
the expectation, not the contract). For each `<file>:<line> — bare '/<name>'`
hit:

1. Read the line in context. CONFIRM it is genuinely a slash-command reference
   to the Kerd skill `<name>` (the crude grep that found these was pattern
   `/<name>` — a hit could in principle be a path fragment or homonym the
   refined regex still matches).
2. If genuine: insert the prefix — `/tend` → `/kerd:tend` — changing nothing
   else on the line. This includes hits inside SKILL.md frontmatter
   `description` fields (e.g. trim's trigger listing `'/trim'` becomes
   `'/kerd:trim'`); keep any bare-word triggers (`'trim'`) untouched. That is
   a trigger-description touch under release-checklist item 4 with no
   behavior change.
3. If NOT genuine (a false positive the regex should not have matched): do
   NOT edit the file and do NOT edit the regex — STOP and hand the hit back
   to the conductor with the line quoted. A false positive at this step means
   the R3 pattern needs a decision, not a silent workaround.

**Why:** the first CI run must be green on the real tree, and these are living
files — fixing them is the point of the rule, not collateral. The
confirm-each discipline exists because the terrain grep was crude.

**Verify:**
```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py release; echo "exit=$?"
```
Expected: `release: clean`, `exit=0` (versions are in sync and capability
lists identical, so R3 was the only live failure class). Then
`git diff --stat` — only the files the checker named are modified, and
`git diff` shows every hunk is a pure `kerd:` insertion.

### Step 5: tools/gates/README.md — document the release sweep [delegate, model: haiku, effort: medium]

**What:** In `/Users/anthonymaley/Kerd/tools/gates/README.md`:

1. Usage block: add after the `audit` line, aligned with the existing comment
   column:
   `    python3 tools/gates/gate.py release [--json]              # release rules — exit 0 clean / 1 problems`
2. Exit-codes paragraph: change "`check` and `audit` are the only two
   subcommands that can exit 1" to "`check`, `audit`, and `release` are the
   only three subcommands that can exit 1".
3. New section `## Release rules` placed between `## Audit` and `## CI`,
   containing: a three-row table —
   | # | Rule |
   |---|---|
   | R1 | the three version fields must be identical: `plugin.json` `version` · `marketplace.json` `metadata.version` · `marketplace.json` `plugins[0].version` |
   | R2 | `plugin.json` `description` must be byte-identical to `marketplace.json` `plugins[0].description`. `metadata.description` is NEVER checked — it is intentionally a different shape (the marketplace one-liner). |
   | R3 | living files must write Kerd slash-command references as `/kerd:<name>`, never bare `/<name>`. Skill names derive from `skills/<name>/SKILL.md` directories — no hardcoded list. |
   — followed by the R3 allowlist (`skills/**`, `modes/**`, `docs/design/*.md`,
   top-level `docs/*.md`, `CLAUDE.md`) and the exclusion rationale, stated as
   in this spec: immutable dated records (`docs/plans/`, `docs/gates/`,
   `kivna/`) never retroactively fail CI, and `README.md` is exempt because
   its shorthand exception is human-adjudicated (CLAUDE.md rule 5).
4. CI section: update the quoted workflow YAML to include the third step
   (`- name: Release rules` / `run: python3 tools/gates/gate.py release`),
   change "the 12 cases" to "the 14 cases", and extend the "Two things can
   fail the build" sentence to three, naming the release sweep.

**Why:** this README is the canonical write-down of the gate tool ("this
README, not the dated spec it came from, is now the standard") — an
undocumented subcommand would violate the tool's own doctrine.

**Verify:**
```
grep -c "release" /Users/anthonymaley/Kerd/tools/gates/README.md
```
Expected: ≥ 8. And `grep -n "14 cases" /Users/anthonymaley/Kerd/tools/gates/README.md`
prints exactly one line; `grep -n "12 cases"` prints nothing.

### Step 6: CLAUDE.md — one enforcement line in the Release Checklist [delegate, model: haiku, effort: low]

**What:** In `/Users/anthonymaley/Kerd/CLAUDE.md`, add exactly ONE line at the
end of the `## Release Checklist` section (after item 5's paragraph, before
`## Version Strategy`), as its own paragraph:

`CI enforces the mechanical subset of this checklist on every push: \`python3 tools/gates/gate.py release\` refuses version drift (item 1), capability-list drift (item 3), and bare slash references (item 5).`

Note the mapping deliberately names checklist items 1, 3, 5 — NOT "items 1–3".
The three intent rules (version sync, capability identity, namespace) land on
those checklist numbers; items 2 (README) and 4 (trigger descriptions) remain
human-judgment and are not claimed.

**Why:** the checklist is where a human looks before committing; one line
tells them which items the machine now backstops — and claims exactly what is
enforced, no more.

**Verify:**
```
grep -c "gate.py release" /Users/anthonymaley/Kerd/CLAUDE.md
```
Expected: `1`. And the section still reads as one added line:
`git diff --stat CLAUDE.md` shows `1 insertion` (plus possibly 1 blank-line
context change, but no deletions).

### Step 7: version bump 0.69.0 → 0.70.0 in the three fields [delegate, model: haiku, effort: low]

**What:** MINOR bump (new enforced behavior in CI):
- `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` → `"version": "0.70.0"`
- `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` → `metadata.version`: `"0.70.0"`
- `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` → `plugins[0].version`: `"0.70.0"`
Do NOT touch either capability-list `description` (CI internals do not change
what Kerd does at a high level) and do NOT touch `metadata.description`.

**Why:** changed behavior → MINOR per the version strategy; bumping all three
together is precisely the invariant R1 now enforces — the bump and the check
must agree or Step 8 refuses.

**Verify:**
```
python3 -c "import json; p=json.load(open('/Users/anthonymaley/Kerd/.claude-plugin/plugin.json')); m=json.load(open('/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json')); print(p['version'], m['metadata']['version'], m['plugins'][0]['version'])"
```
Expected: `0.70.0 0.70.0 0.70.0`.

### Step 8: full local gate — selftest + audit + release all clean [delegate, model: haiku, effort: low]

**What:** Run the complete gate surface exactly as CI will:
```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && echo "ALL CLEAN"
```

**Why:** "first CI run green on the real tree" is verified locally before it
is claimed remotely — the same three commands, same order, as gate.yml.

**Verify:** the command above prints `selftest: 14 cases passed`,
`audit: clean`, `release: clean`, `ALL CLEAN`, exit 0. If audit reports
problems, STOP and hand back to the conductor — this spec changes no audit
rule, so an audit failure means pre-existing drift outside this contract.

### Step 9: refusal demo — plant → exit 1 → revert → clean [delegate, model: haiku, effort: medium]

**What:** Execute the refusal-demo protocol from the top of this spec,
verbatim, in this order:

1. `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py release; echo "exit=$?"` → `release: clean`, `exit=0`.
2. Edit `.claude-plugin/plugin.json`: `"version": "0.70.0"` → `"version": "0.70.1"`.
3. Run again → expect exactly one problem line starting `problem: version drift — plugin.json='0.70.1' metadata.version='0.70.0' plugins[0].version='0.70.0'`, then `release: 1 problems`, `exit=1`.
4. Edit the version BACK to `"0.70.0"` (Edit tool — NOT `git checkout`, which
   would destroy the uncommitted bump).
5. Append to `/Users/anthonymaley/Kerd/CLAUDE.md` the line: `Run /tend before commits.`
6. Run again → expect exactly one problem line matching `problem: CLAUDE.md:<lineno> — bare '/tend' (write '/kerd:tend')`, `release: 1 problems`, `exit=1`.
7. Remove that line (Edit tool — NOT `git checkout`).
8. Run again → `release: clean`, `exit=0`.

**Why:** the acceptance bar demands demonstrated refusal, not asserted
refusal — one plant per live rule class (the JSON pair and the tree scan),
run locally before push on the entry-gates canary precedent.

**Verify:** the four run outputs above, in order (clean / 1 problem exit 1 /
1 problem exit 1 / clean). Then prove zero demo residue:
```
cd /Users/anthonymaley/Kerd && git diff .claude-plugin/plugin.json CLAUDE.md | grep -E "^[+-]" | grep -vE "^(\+\+\+|---)"
```
Expected: only the intended changes remain — the 0.70.0 bump line pair in
plugin.json and the single Step-6 checklist line in CLAUDE.md; no `0.70.1`,
no `Run /tend`.

### Step 10: collateral diff review [keep]

**What:** Conductor reads `git status` and the full `git diff` before
anything is staged. Checklist:
- Modified set is exactly: `tools/gates/kit.py`, `tools/gates/gate.py`,
  `tools/gates/README.md`, `.github/workflows/gate.yml`, `CLAUDE.md`,
  `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, the
  living files Step 4 fixed (expected: `skills/tend/SKILL.md`,
  `skills/trim/SKILL.md`, `skills/slainte/SKILL.md`; authoritative list is
  Step 4's report), plus untracked
  `docs/plans/2026-08-04-ci-refusal-spec.md` (this spec).
- Every Step-4 hunk is a pure `kerd:` insertion — no rewording, no trigger
  phrases dropped.
- No demo residue (no `0.70.1`, no `Run /tend`), no capability-list or
  metadata.description edits in either JSON file, no AU1–AU4 logic touched
  in kit.py (the audit functions' diffs must be empty).
- Check this spec's own Pieces boxes for Steps 1–9 before committing it.

**Why:** the one seam where human/conductor judgment beats a command — scope
control on a multi-file change that edits the enforcement tool and the files
it enforces in the same commit.

**Verify:** conductor states the file list matches, hunk classes match, and
explicitly names anything unexpected (which routes back to the owning step,
not into the commit).

### Step 11: commit staged by name, push, watch CI green [keep]

**What:** Stage by name — never `git add -A`:
```
cd /Users/anthonymaley/Kerd && git add tools/gates/kit.py tools/gates/gate.py tools/gates/README.md .github/workflows/gate.yml CLAUDE.md .claude-plugin/plugin.json .claude-plugin/marketplace.json skills/tend/SKILL.md skills/trim/SKILL.md skills/slainte/SKILL.md docs/plans/2026-08-04-ci-refusal-spec.md
```
(adjust the skills/ list to Step 4's actual report). Commit with a message in
repo voice, e.g. `Release rules: the second refuser — version sync, capability
identity, kerd: namespace (0.70.0)`; the committing session's harness appends
its own session trailer. Then push (always push after committing), then watch
the run to conclusion:
```
cd /Users/anthonymaley/Kerd && git push && gh run watch $(gh run list --branch main --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status
```

**Why:** the ship gate — the acceptance bar closes only when GitHub's runner,
not the local shell, exits green on all three steps.

**Verify:** `gh run watch ... --exit-status` exits 0 with the `entry-gate`
workflow showing `Gate selftest`, `Repo audit`, and `Release rules` all
passing. If `Release rules` fails remotely after passing locally, STOP:
capture the log (`gh run view --log-failed`), hand back to the conductor — do
not hot-fix on main.
