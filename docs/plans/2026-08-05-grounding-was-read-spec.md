---
route: new
stage: contracted
---

# Grounding-was-read slice 1 — contract spec (AU5: the reachability audit)

Contract for the build rung of `grounding-was-read`, slice 1. Upstream truth:
`docs/design/grounding-was-read.md` — every rule semantic and both problem
strings below are measured against it, byte-exact.

Boundaries (hard, from the approved design): no read-receipts, no
rung-scoping, no static per-rung table, no orphan report, no new CI step —
AU5 rides the existing `gate.py audit` step. No changes to `check_rung`,
`route`, or the release rules. Stdlib only. Deterministic: no randomness, no
timestamps; problem order follows sorted file order then line order.

**The em-dash separator is load-bearing:** every ` — ` in the grounding
grammar and in both problem strings is the literal three-character sequence
space, U+2014 EM DASH, space. Every code block in this spec already carries
the correct character — **copy the blocks, never retype them**. A hyphen or
en dash is a different feature.

## Pieces

- [x] `_audit_au5` in `tools/gates/kit.py`, wired into `audit()`
- [x] Four selftest fixture cases T15–T18 (suite grows 14 → 18)
- [x] Dogfood `## Grounding` section in `docs/product/grounding-was-read.md`
- [x] AU5 documented in `tools/gates/README.md` (rule row, section shape, counts, deferred section retired)
- [x] Version `0.80.0` in the three release locations

Piece trailers on the work commit: `Piece: grounding-was-read/<n>`, numbered
in list order (1–5). Steps 6–7 are review and ship — procedural, no piece.

## Steps

### Step 1: AU5 lands in kit.py
[delegate, model: sonnet, effort: low]

File: `/Users/anthonymaley/Kerd/tools/gates/kit.py`. Three edits, all in the
`── audit (A7) ──` region. Copy verbatim — the em dashes in the strings are
the feature.

**1a.** Insert this function immediately above `def audit(root):`, keeping
the standard two blank lines between functions:

```python
def _audit_au5(root):
    """docs/product/*.md carrying a '## Grounding' section: every list
    line ('- ...') must parse as '- <ref> — <why>' (split on the FIRST
    ' — ') and <ref> — a path or glob relative to the repo root — must
    resolve to at least one match on disk. Absent section = vacuous
    pass: declaring grounding is opting in, and the audit refuses only
    what was declared."""
    problems = []
    d = os.path.join(root, "docs", "product")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        fname = os.path.basename(path)
        rel = f"docs/product/{fname}"
        with open(path, encoding="utf-8") as f:
            text = f.read()
        body = find_section(text, "Grounding")
        if not body:
            continue
        for line in body.splitlines():
            if not line.startswith("- "):
                continue
            shown = line.rstrip()
            rest = shown[2:]
            if " — " not in rest:
                problems.append(
                    f"{rel} — grounding line malformed (want '- <ref> — <why>'): {shown}"
                )
                continue
            ref = rest.split(" — ", 1)[0].strip()
            if not glob.glob(os.path.join(root, ref)):
                problems.append(f"{rel} — grounding reference does not resolve: {ref}")
    return problems
```

**1b.** In `audit()`'s docstring, change `(AU1-AU4)` to `(AU1-AU5)`.

**1c.** In `audit()`'s body, this exact change (the two-line old string is
unique in the file):

old:
```python
    problems += _audit_au4(root)
    return problems
```
new:
```python
    problems += _audit_au4(root)
    problems += _audit_au5(root)
    return problems
```

Nothing else in kit.py changes in this step. No new imports — `glob`, `os`,
`find_section` are already in scope.

**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest && python3 - <<'EOF'
import os, sys, tempfile
sys.path.insert(0, "tools/gates")
import kit
with tempfile.TemporaryDirectory() as root:
    os.makedirs(os.path.join(root, "docs", "product"))
    with open(os.path.join(root, "docs", "product", "x.md"), "w", encoding="utf-8") as f:
        f.write("---\nroute: new\nstage: framed\n---\n\n## Value\n\nv\n\n"
                "## Grounding\n\n- nope.md — gone\n- bad line no separator\n")
    for p in kit.audit(root):
        print(p)
EOF` — expected output, verbatim (existing 14-case suite still green, then the probe's two problems in line order):
```
selftest: 14 cases passed
docs/product/x.md — grounding reference does not resolve: nope.md
docs/product/x.md — grounding line malformed (want '- <ref> — <why>'): - bad line no separator
```
The probe is spec-authored, not player-authored — it exercises the rule from
outside before the step-2 fixtures exist.

### Step 2: Fixture cases T15–T18 (14 → 18)
[delegate, model: sonnet, effort: low]

File: `/Users/anthonymaley/Kerd/tools/gates/kit.py`. Two edits.

**2a.** Append the four cases at the end of `_selftest_body()`, immediately
after the T14 block (anchor: the line
`assert problems == [], f"T14: expected a clean release audit, got {problems}"`
and its closing of the `with` block). Same indentation as T12–T14 (the
`with` statements at 4 spaces). Verbatim:

```python
    # T15 — AU5: resolving grounding (exact path + glob), audit clean.
    with tempfile.TemporaryDirectory() as root_g1:
        _sw(os.path.join(root_g1, "docs", "design", "beta.md"), "# Beta design\n\nHow it works.\n")
        _sw(
            os.path.join(root_g1, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Grounding\n\n"
            "- docs/design/beta.md — the design this work rides\n"
            "- docs/design/*.md — every living design doc\n",
        )
        problems = audit(root_g1)
        assert problems == [], f"T15: expected a clean audit, got {problems}"

    # T16 — AU5: broken reference, named verbatim.
    with tempfile.TemporaryDirectory() as root_g2:
        _sw(
            os.path.join(root_g2, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Grounding\n\n"
            "- docs/design/ghost.md — moved away and never fixed\n",
        )
        problems = audit(root_g2)
        assert problems == [
            "docs/product/beta.md — grounding reference does not resolve: docs/design/ghost.md"
        ], f"T16: expected the verbatim broken-ref problem, got {problems}"

    # T17 — AU5: malformed line (no ' — ' separator), named verbatim.
    with tempfile.TemporaryDirectory() as root_g3:
        _sw(
            os.path.join(root_g3, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Grounding\n\n"
            "- docs/design/beta.md the why, but no separator\n",
        )
        problems = audit(root_g3)
        assert problems == [
            "docs/product/beta.md — grounding line malformed (want '- <ref> — <why>'): "
            "- docs/design/beta.md the why, but no separator"
        ], f"T17: expected the verbatim malformed-line problem, got {problems}"

    # T18 — AU5: absent section = vacuous pass (opting in).
    with tempfile.TemporaryDirectory() as root_g4:
        _sw(
            os.path.join(root_g4, "docs", "product", "beta.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n",
        )
        problems = audit(root_g4)
        assert problems == [], f"T18: expected a vacuous pass, got {problems}"
```

**2b.** Update `selftest()` — the count appears twice in the docstring and
once in the print:

old:
```python
    """Run the 14 fixture-built cases in temporary trees. Prints
    'selftest: 14 cases passed' and returns 0 on success; on the first
```
new:
```python
    """Run the 18 fixture-built cases in temporary trees. Prints
    'selftest: 18 cases passed' and returns 0 on success; on the first
```

old: `    print("selftest: 14 cases passed")`
new: `    print("selftest: 18 cases passed")`

**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest` — expected output, verbatim: `selftest: 18 cases passed` (exit 0). Cross-step: these fixtures were written into the spec by the orchestrator and exercise step 1's code, applied by a different player.

### Step 3: Dogfood — the feature's first citizen is its own product doc
[delegate, model: haiku, effort: low]

File: `/Users/anthonymaley/Kerd/docs/product/grounding-was-read.md`. Append
this block at the end of the file (after the `## Release slice` section's
last line), separated by one blank line. Verbatim:

```markdown
## Grounding

- docs/design/grounding-was-read.md — the design this slice implements; AU5's semantics are measured against it
- tools/gates/kit.py — the harness AU5 lands in
- docs/gates/*-grounding-was-read-design.md — the design GO record that admitted this build
- CONTEXT.md — standing decisions bind the implementation
```

**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py audit` — expected output, verbatim: `audit: clean` (exit 0). Cross-step: the real-tree audit runs step 1's rule against step 3's declarations — all four refs must resolve on this tree, glob included. If this refuses instead, the ref it names is a real finding: hand it back to the orchestrator, do not delete the reference to get green.

### Step 4: README — AU5 row, section shape, counts, deferred section retired
[delegate, model: haiku, effort: low]

File: `/Users/anthonymaley/Kerd/tools/gates/README.md`. Four edits. The
dashes in `AU1–AU4` are en dashes (U+2013) and the grounding separators are
em dashes (U+2014) — copy from the blocks.

**4a.** In the `## Audit` intro paragraph — old: `the four rules below run` → new: `the five rules below run`.

**4b.** Append this row to the audit rules table, directly under the AU4 row:

```markdown
| AU5 | `docs/product/*.md` carrying a `## Grounding` section: every top-level list line must parse as `- <ref> — <why>` (split on the FIRST ` — `, the em-dash separator) and `<ref>` — a path or glob relative to the repo root — must resolve to ≥1 match on disk. Absent section = vacuous pass: declaring grounding is opting in. |
```

**4c.** In the `## CI` paragraph — old: `exercising the 14 cases` → new: `exercising the 18 cases`; old: `exercising AU1–AU4 against the actual` → new: `exercising AU1–AU5 against the actual`.

**4d.** Replace the entire `## Deferred: grounding-was-read` section — from
its heading up to (not including) `## Progress view` — with:

```markdown
## Grounding-was-read

Slice 1 is live. A product doc may declare its background reading — the
artifacts that must be read before the work produces anything — in an
optional `## Grounding` section of list lines:

    ## Grounding

    - docs/design/grounding-was-read.md — the design this slice implements
    - docs/gates/*-grounding-was-read-design.md — the GO record

Shape: `- <ref> — <why>`. The ref is everything before the FIRST ` — `
(space, em-dash, space); the why is prose for the human reader and never
parsed. The ref is a path or glob relative to the repo root; AU5 (above)
refuses any declared reference that stops resolving. Absent section =
vacuous pass — declaring grounding is opting in.

Slice 2 — read-receipts proving the reading *happened* (on the
`tools/diagram/mark_reviewed.py` precedent) and any rung-scoped grounding —
stays deferred. The earlier sketch of a `grounding` slot in a `kit.GATES`
table is dead: no such table exists, and the design
(`docs/design/grounding-was-read.md`) settled on per-item declarations over
a static per-rung home.
```

**Verify:** `cd /Users/anthonymaley/Kerd && grep -F "| AU5 |" tools/gates/README.md && grep -F "exercising the 18 cases" tools/gates/README.md && grep -cF "Deferred: grounding-was-read" tools/gates/README.md; true` — expected: the full AU5 table row printed, one line containing `exercising the 18 cases`, then `0` (the deferred heading is gone; grep -c prints 0 and the trailing `; true` absorbs its exit 1).

### Step 5: Version 0.80.0 in the three locations
[delegate, model: haiku, effort: low]

**5a.** `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` —
old: `  "version": "0.79.0",` → new: `  "version": "0.80.0",`

**5b.** `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json`, metadata
block — old:
```json
    "description": "Kerd: opinionated workflow skills for Claude Code",
    "version": "0.79.0"
```
new:
```json
    "description": "Kerd: opinionated workflow skills for Claude Code",
    "version": "0.80.0"
```

**5c.** Same file, plugins[0] block — old:
```json
      "version": "0.79.0",
      "strict": true
```
new:
```json
      "version": "0.80.0",
      "strict": true
```

No description fields change — this slice adds no skill capability.

**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py release && grep -F '"version": "0.80.0"' .claude-plugin/plugin.json .claude-plugin/marketplace.json` — expected output, verbatim:
```
release: clean
.claude-plugin/plugin.json:  "version": "0.80.0",
.claude-plugin/marketplace.json:    "version": "0.80.0"
.claude-plugin/marketplace.json:      "version": "0.80.0",
```
Cross-step: R1 (written long before this build) is the drift refuser
checking this step's three edits agree.

### Step 6: Diff review — blast radius
[keep]

kit.py is load-bearing: CI steps 1 and 2 (`selftest`, `audit`) both run
through it, and every product doc in the repo is now swept by AU5. Review
`git diff` in full before ship. Checklist:

- kit.py: AU5 is purely additive — `check_rung`, `route`, `release_audit`,
  and all existing `_audit_au*` functions byte-untouched; no new imports;
  no I/O beyond reading `docs/product/*.md`; `sorted()` on the glob keeps
  output deterministic.
- Both problem strings byte-match `docs/design/grounding-was-read.md`
  (section "AU5 — the reachability audit rule"), em dashes included.
- The dogfood section and README blocks carry em dashes (U+2014) in the
  separators, not hyphens or en dashes:
  `grep -c '—' docs/product/grounding-was-read.md` must be ≥ 4.
- No file outside the five below is touched; the spec file itself is the
  only untracked addition.

**Verify:** `cd /Users/anthonymaley/Kerd && git diff --name-only && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release` — expected output, verbatim:
```
.claude-plugin/marketplace.json
.claude-plugin/plugin.json
docs/product/grounding-was-read.md
tools/gates/README.md
tools/gates/kit.py
selftest: 18 cases passed
audit: clean
release: clean
```

### Step 7: Ship — refusal both ways, then the standing flow
[keep]

**7a — refusal proven (the 0.70.0 pattern), before committing.** Append this
line to the `## Grounding` section of `docs/product/grounding-was-read.md`
via Edit:

```
- docs/design/does-not-exist.md — planted broken reference for the both-ways demonstration
```

Run `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py audit; echo "exit=$?"` — expected output, verbatim:
```
problem: docs/product/grounding-was-read.md — grounding reference does not resolve: docs/design/does-not-exist.md
audit: 1 problems
exit=1
```

**7b — and back.** Remove exactly that planted line via Edit (do NOT
`git checkout` the file — the dogfood section is uncommitted). Re-run the
same command — expected output, verbatim:
```
audit: clean
exit=0
```

**7c — work commit** (the spec rides with its build):

```
git add docs/plans/2026-08-05-grounding-was-read-spec.md tools/gates/kit.py tools/gates/README.md docs/product/grounding-was-read.md .claude-plugin/plugin.json .claude-plugin/marketplace.json
```

Commit with this message (Pieces boxes in this spec checked first):

```
Grounding-was-read slice 1: AU5, the reachability audit (v0.80.0)

A product doc may declare its background reading in an optional
'## Grounding' section ('- <ref> — <why>' list lines); AU5 sweeps
every docs/product/*.md and refuses malformed lines and references
that do not resolve on the tree. Four new selftest fixtures (18
total), dogfood section on the feature's own product doc, README
rule row and section shape, v0.80.0.

Piece: grounding-was-read/1
Piece: grounding-was-read/2
Piece: grounding-was-read/3
Piece: grounding-was-read/4
Piece: grounding-was-read/5
Claude-Session: https://claude.ai/code/session_01SHPPRQJHn8tiaxhuLwBLHS
```

**7d — render refresh:** `python3 tools/diagram/progress.py`, then
`git status --porcelain` and stage exactly the render outputs it rewrote
(the render trio). Commit — no Piece trailer:

```
Refresh progress render

Claude-Session: https://claude.ai/code/session_01SHPPRQJHn8tiaxhuLwBLHS
```

**7e — ONE push:** `git push` (once, after both commits).

**Verify:** `cd /Users/anthonymaley/Kerd && git log --format='%s' -2 && git status -sb | head -1` — expected output, verbatim:
```
Refresh progress render
Grounding-was-read slice 1: AU5, the reachability audit (v0.80.0)
## main...origin/main
```
(no ahead/behind marker, clean tree — the push landed; CI reruns the same
three gates on GitHub's side).
