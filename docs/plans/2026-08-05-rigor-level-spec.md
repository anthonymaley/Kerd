---
route: new
stage: contracted
---

# Rigor level — slice 1 build spec (v0.81.0)

Contract for the rigor-level slice-1 build. One parser, two call sites,
six new fixtures, an honest retrofit in the same commit. All paths are
relative to `/Users/anthonymaley/Kerd` (call it `$BASE`). Scratchpad:
`/private/tmp/claude-501/-Users-anthonymaley-Kerd/c19f6a52-9cdc-4c01-bc26-a5a72a7f8b5e/scratchpad`
(call it `$SCRATCH`). Every command below runs with absolute paths;
subagent cwd resets between calls.

Fixture-asserted strings — these appear VERBATIM in code and in this
spec; any paraphrase is a build failure:

- `docs/product/<S>.md — Rigor level line outside Release slice`
- `docs/product/<S>.md — Release slice missing 'Rigor level: <spike|mvp|production-v1>' line`
- `docs/product/<S>.md — duplicate Rigor level lines (want exactly one)`
- `docs/product/<S>.md — illegal rigor level '<v>' (legal: spike, mvp, production-v1)`
- gate need row: `need: docs/product/<S>.md — Release slice declares a legal rigor level (Rigor level: spike|mvp|production-v1)`

Out of scope: the rigor catalog, disposition tables, any change to
`.github/workflows/gate.yml` (CI stays seven steps), slices 2/3, any
route/stage front-matter schema change. `tools/gates/gate.py` is NOT
touched — it renders kit dicts and enumerates no rules.

## Pieces

- [x] Step 1 — Capture before-route baselines
- [x] Step 2 — kit.py: RIGOR_LEVELS + rigor_problems + AU6 + design-rung need row
- [x] Step 3 — kit.py: fixture amendment + six new cases (18 → 24)
- [x] Step 4 — Diff-review kit.py (blast radius)
- [x] Step 5 — Retrofit `Rigor level: mvp` into four product docs
- [x] Step 6 — Route byte-compare (before vs after)
- [x] Step 7 — tools/gates/README.md: gate row, AU6 row, Rigor level section
- [x] Step 8 — Version bump to 0.81.0 (three fields)
- [x] Step 9 — Full local suite
- [x] Step 10 — Work commit (one commit, with trailer)
- [x] Step 11 — Both-ways demo (strip → red verbatim; restore → clean)
- [x] Step 12 — Progress refresh, render commit, stale check, single push

### Step 1 — Capture before-route baselines

`[keep]` — ordering-critical and trivial; must run before ANY edit.

For each slug `push-wiring`, `grounding-was-read`, `progress-html`:

    python3 /Users/anthonymaley/Kerd/tools/gates/gate.py route <slug> > $SCRATCH/route-<slug>-before.txt

WHY: the constraint is that these three done journeys' `route` output is
byte-identical before/after the whole build (the retrofit must exactly
compensate the new check). The baseline must predate every edit or the
comparison proves nothing.

**Verify:** `wc -l $SCRATCH/route-push-wiring-before.txt $SCRATCH/route-grounding-was-read-before.txt $SCRATCH/route-progress-html-before.txt` — each file ≥ 9 lines (8 rung lines + `enters at:`), none empty.

### Step 2 — kit.py: RIGOR_LEVELS + rigor_problems + AU6 + design-rung need row

`[delegate, model: sonnet, effort: medium]` — file: `/Users/anthonymaley/Kerd/tools/gates/kit.py`.

Four edits, exact text:

**(a)** Immediately after the `LEGAL_STATES = { ... }` closing brace
(after the line containing only `}` that ends the set, before the
`GATE_RECORD_RE` block), insert:

```python
# The legal rigor levels (AU6, design rung). A '## Release slice' section
# declares how rigorously the slice is measured — one 'Rigor level:' line;
# the legal set lives here and only here.
RIGOR_LEVELS = ["spike", "mvp", "production-v1"]
```

**(b)** In the regex block, immediately after the line
`SEPARATOR_ROW_RE = re.compile(r'^[\s|:-]+$')`, insert:

```python
RIGOR_LINE_RE = re.compile(r'^Rigor level:(.*)$')
RIGOR_SECTION_HEADING_RE = re.compile(r'^## Release slice[ \t]*$')
```

**(c)** Immediately after the `find_section` function (after its final
`return text[start:end].strip()` line and before the
`# ── the risk ledger` banner), insert:

```python
# ── rigor level (AU6, design rung) ──────────────────────────────────────────

def rigor_problems(text):
    """Judge one product doc's 'Rigor level:' declaration. Single-parser
    rule: AU6 and the design rung both call THIS function — the law is
    written once. The law: exactly one legal 'Rigor level: <value>' line
    INSIDE the '## Release slice' section; a 'Rigor level:' line anywhere
    else in the doc is a problem; a doc with no '## Release slice' section
    passes vacuously (the section's absence is already the design rung's
    own refusal — this rule does not double-refuse it). Returns problem
    strings WITHOUT the 'docs/product/<S>.md — ' prefix; callers prepend
    it. Emission order: the outside-line problem first, then exactly one
    of missing / duplicate / illegal."""
    inside = False
    section_seen = False
    inside_values = []
    outside_count = 0
    for line in text.splitlines():
        if RIGOR_SECTION_HEADING_RE.match(line):
            inside = True
            section_seen = True
            continue
        if line.startswith("## "):
            inside = False
            continue
        m = RIGOR_LINE_RE.match(line)
        if not m:
            continue
        if inside:
            inside_values.append(m.group(1).strip())
        else:
            outside_count += 1

    problems = []
    if outside_count:
        problems.append("Rigor level line outside Release slice")
    if section_seen:
        if not inside_values:
            problems.append(
                "Release slice missing 'Rigor level: <spike|mvp|production-v1>' line"
            )
        elif len(inside_values) > 1:
            problems.append("duplicate Rigor level lines (want exactly one)")
        elif inside_values[0] not in RIGOR_LEVELS:
            problems.append(
                f"illegal rigor level '{inside_values[0]}' (legal: spike, mvp, production-v1)"
            )
    return problems
```

WHY this shape: the line-walk (not `find_section`) is needed because the
rule must classify lines as inside/outside the section, which the
body-extracting `find_section` cannot express; the heading regex is the
per-line equivalent of `find_section`'s `^## <title>[ \t]*$` semantics.
Duplicate short-circuits the value check (one problem per category, so
each fixture asserts exactly one line). Value is `.strip()`-ed and
case-sensitive: `Rigor level: MVP` is illegal.

**(d)** In `check_rung`, the design block currently reads:

```python
    if idx >= RUNGS.index("design"):
        if not product_exists:
            need.append(f'{rel_product} — section "Release slice"')
        else:
            if find_section(product_text, "Release slice"):
                have.append(f'{rel_product} — section "Release slice"')
            else:
                need.append(f'{rel_product} — section "Release slice"')
```

Replace it with:

```python
    if idx >= RUNGS.index("design"):
        if not product_exists:
            need.append(f'{rel_product} — section "Release slice"')
        else:
            if find_section(product_text, "Release slice"):
                have.append(f'{rel_product} — section "Release slice"')
            else:
                need.append(f'{rel_product} — section "Release slice"')
            if rigor_problems(product_text):
                need.append(
                    f"{rel_product} — Release slice declares a legal rigor level "
                    "(Rigor level: spike|mvp|production-v1)"
                )
```

WHY: the gate emits ONE generic need row regardless of which violation
fired — the gate names the requirement, the audit names the violation.
No `have` row is added when clean: the intent grants the design rung
exactly one need row, and `route`'s text render prints only need counts,
which keeps the three done journeys' output stable by construction.

**(e)** Immediately after the `_audit_au5` function (before
`def audit(root):`), insert:

```python
def _audit_au6(root):
    """docs/product/*.md: the 'Rigor level:' law — see rigor_problems
    (single parser; the design rung is the second call site). Absent
    '## Release slice' section = vacuous pass."""
    problems = []
    d = os.path.join(root, "docs", "product")
    if not os.path.isdir(d):
        return problems
    for path in sorted(glob.glob(os.path.join(d, "*.md"))):
        rel = f"docs/product/{os.path.basename(path)}"
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for p in rigor_problems(text):
            problems.append(f"{rel} — {p}")
    return problems
```

**(f)** In `audit(root)`: change the docstring's `(AU1-AU5)` to
`(AU1-AU6)` and add `problems += _audit_au6(root)` immediately after
`problems += _audit_au5(root)`.

**Verify:** `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py selftest` exits 1 printing exactly `selftest: FAILED — T8a: expected design, got 'slice'` — the INTENDED intermediate red: it proves the new check grips (T8's fixture has a Release slice without a rigor line, so design now refuses it). Step 3 turns this green.

### Step 3 — kit.py: fixture amendment + six new cases (18 → 24)

`[delegate, model: sonnet, effort: medium]` — file: `/Users/anthonymaley/Kerd/tools/gates/kit.py`.

**(a)** In `_selftest_body`, T8a's fixture line currently reads:

```python
        _sw(product, ledger_good + "\n## Release slice\n\nShip the caching path first.\n")
```

Replace with:

```python
        _sw(product, ledger_good + "\n## Release slice\n\nRigor level: mvp\n\nShip the caching path first.\n")
```

WHY: T8's product doc persists through T9/T10, so this one amendment
carries the clean path through every downstream rung — and route
reaching `design` here is the proof the gate's second call site passes
when the declaration is legal.

**(b)** At the end of `_selftest_body`, after the entire T18
`with tempfile.TemporaryDirectory() as root_g4:` block, append (same
top-level indentation as T18):

```python
    # T19 — AU6: legal Rigor level line inside Release slice, audit clean.
    with tempfile.TemporaryDirectory() as root_v1:
        _sw(
            os.path.join(root_v1, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nRigor level: production-v1\n\nShip the smallest slice.\n",
        )
        problems = audit(root_v1)
        assert problems == [], f"T19: expected a clean audit, got {problems}"

    # T20 — AU6: Release slice without the line, named verbatim; the design
    # rung refuses with its one need row (second call site, same parser).
    with tempfile.TemporaryDirectory() as root_v2:
        _sw(
            os.path.join(root_v2, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nShip the smallest slice.\n",
        )
        problems = audit(root_v2)
        assert problems == [
            "docs/product/gamma.md — Release slice missing 'Rigor level: <spike|mvp|production-v1>' line"
        ], f"T20: expected the verbatim missing-line problem, got {problems}"
        cr = check_rung(root_v2, "gamma", "design")
        assert (
            "docs/product/gamma.md — Release slice declares a legal rigor level "
            "(Rigor level: spike|mvp|production-v1)"
        ) in cr["need"], f"T20: expected the rigor need row: {cr['need']}"

    # T21 — AU6: illegal value, named verbatim.
    with tempfile.TemporaryDirectory() as root_v3:
        _sw(
            os.path.join(root_v3, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nRigor level: prod\n\nShip it.\n",
        )
        problems = audit(root_v3)
        assert problems == [
            "docs/product/gamma.md — illegal rigor level 'prod' (legal: spike, mvp, production-v1)"
        ], f"T21: expected the verbatim illegal-value problem, got {problems}"

    # T22 — AU6: duplicate lines inside the section, named verbatim.
    with tempfile.TemporaryDirectory() as root_v4:
        _sw(
            os.path.join(root_v4, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Release slice\n\nRigor level: mvp\nRigor level: spike\n\nShip it.\n",
        )
        problems = audit(root_v4)
        assert problems == [
            "docs/product/gamma.md — duplicate Rigor level lines (want exactly one)"
        ], f"T22: expected the verbatim duplicate problem, got {problems}"

    # T23 — AU6: a line outside the section, named verbatim (the section's
    # own legal line keeps this the only problem).
    with tempfile.TemporaryDirectory() as root_v5:
        _sw(
            os.path.join(root_v5, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nRigor level: mvp\n\nWorth it.\n\n"
            "## Release slice\n\nRigor level: mvp\n\nShip it.\n",
        )
        problems = audit(root_v5)
        assert problems == [
            "docs/product/gamma.md — Rigor level line outside Release slice"
        ], f"T23: expected the verbatim misplaced problem, got {problems}"

    # T24 — AU6: no '## Release slice' section = vacuous pass (mirrors
    # T18's rule for AU5: the rule scopes to docs carrying the section).
    with tempfile.TemporaryDirectory() as root_v6:
        _sw(
            os.path.join(root_v6, "docs", "product", "gamma.md"),
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n",
        )
        problems = audit(root_v6)
        assert problems == [], f"T24: expected a vacuous pass, got {problems}"
```

**(c)** In `selftest()`: docstring `Run the 18 fixture-built cases` →
`Run the 24 fixture-built cases`; docstring `'selftest: 18 cases passed'`
→ `'selftest: 24 cases passed'`; the print
`print("selftest: 18 cases passed")` → `print("selftest: 24 cases passed")`.

**Verify:** `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py selftest` exits 0 printing exactly `selftest: 24 cases passed`.

### Step 4 — Diff-review kit.py (blast radius)

`[keep]` — review `git -C /Users/anthonymaley/Kerd diff tools/gates/kit.py`
and confirm NOTHING outside these symbols changed: `RIGOR_LEVELS`,
`RIGOR_LINE_RE`, `RIGOR_SECTION_HEADING_RE`, `rigor_problems`,
`_audit_au6`, `audit` (one wiring line + docstring token), `check_rung`
(design block only — the appended need row), `_selftest_body` (the T8a
fixture string; T19–T24 appended after T18), `selftest` (18→24, three
spots). The review must specifically catch: no edit to any existing
verbatim message, `LEGAL_STATES`, `parse_ledger`, the release functions,
or the order of any pre-existing have/need append; the four refusal
suffixes and the need row byte-match this spec's header list.

**Verify:** `git -C /Users/anthonymaley/Kerd diff --name-only` prints exactly `tools/gates/kit.py` (steps 5–8 have not run yet), and the review found no out-of-scope hunk.

### Step 5 — Retrofit `Rigor level: mvp` into four product docs

`[delegate, model: haiku, effort: low]` — insertion point is fixed:
the line `Rigor level: mvp` plus a blank line, inserted immediately
after the blank line that follows the `## Release slice` heading. Four
exact replacements (old → new), one per file:

`/Users/anthonymaley/Kerd/docs/product/push-wiring.md`:
`## Release slice\n\nSmallest valuable slice: **the staleness refuser**` →
`## Release slice\n\nRigor level: mvp\n\nSmallest valuable slice: **the staleness refuser**`

`/Users/anthonymaley/Kerd/docs/product/grounding-was-read.md`:
`## Release slice\n\nSmallest valuable slice — **slice 1: declarations + the reachability` →
`## Release slice\n\nRigor level: mvp\n\nSmallest valuable slice — **slice 1: declarations + the reachability`

`/Users/anthonymaley/Kerd/docs/product/progress-html.md`:
`## Release slice\n\nSmallest valuable slice: **one committed self-contained page**` →
`## Release slice\n\nRigor level: mvp\n\nSmallest valuable slice: **one committed self-contained page**`

`/Users/anthonymaley/Kerd/docs/product/rigor-level.md`:
`## Release slice\n\nSmallest valuable slice — **slice 1: the declared level + the refusal**` →
`## Release slice\n\nRigor level: mvp\n\nSmallest valuable slice — **slice 1: the declared level + the refusal**`

WHY: the value `mvp` for all four is the composer's fixed call (honest
retrofit — these are shipped/shipping tool slices, not spikes and not
production-v1); top-of-section placement makes the declaration the first
thing the section states, uniformly, so no player ever chooses a spot.
This is the move that keeps the three done journeys' route output
identical: the new design-rung check passes for them by construction.

**Verify:** `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py audit` exits 0 printing exactly `audit: clean` (before this step it exits 1 with four missing-line problems — all four product docs carry a Release slice).

### Step 6 — Route byte-compare (before vs after)

`[keep]` — for each slug `push-wiring`, `grounding-was-read`,
`progress-html`: run
`python3 /Users/anthonymaley/Kerd/tools/gates/gate.py route <slug> > $SCRATCH/route-<slug>-after.txt`
then `cmp $SCRATCH/route-<slug>-before.txt $SCRATCH/route-<slug>-after.txt`.

WHY: this is the contract's proof obligation that detection-at-tip did
not falsify three done journeys — the retrofit guarantee, demonstrated,
not asserted.

**Verify:** all three `cmp` invocations exit 0 with no output (byte-identical before/after).

### Step 7 — tools/gates/README.md: gate row, AU6 row, Rigor level section

`[delegate, model: haiku, effort: low]` — file:
`/Users/anthonymaley/Kerd/tools/gates/README.md`. Four exact edits:

**(a)** Gate-table `design` row, old:

    | `design` | section `Release slice` in `docs/product/<S>.md` |

new:

    | `design` | section `Release slice` in `docs/product/<S>.md` · that section declares its rigor level: exactly one `Rigor level: <spike\|mvp\|production-v1>` line inside it (see Rigor level, below) |

**(b)** Audit intro: `the five rules below` → `the six rules below`.
Then add to the audit table, directly after the AU5 row:

    | AU6 | `docs/product/*.md`: exactly one legal `Rigor level: <spike\|mvp\|production-v1>` line INSIDE the `## Release slice` section — a line outside the section, a missing line, duplicate lines, or an illegal value is a named problem. No `## Release slice` section = vacuous pass. |

**(c)** CI prose (the paragraph after the workflow snippet):
`exercising the 18 cases` → `exercising the 24 cases`, and
`exercising AU1–AU5` → `exercising AU1–AU6`. Touch nothing else in the
CI section — the workflow file itself is out of scope.

**(d)** Insert a new section between `## Grounding-was-read` and
`## Progress view`:

```markdown
## Rigor level

Every `## Release slice` section must declare how rigorously its slice
is measured — one line, machine-checked:

    Rigor level: mvp

Grammar: the line starts at column 0 with `Rigor level:`; the value is
the rest of the line, whitespace-stripped, case-sensitive. The legal
set is `spike` · `mvp` · `production-v1`, living in exactly one place —
`RIGOR_LEVELS` in `kit.py`. The law is written once (`rigor_problems`)
and enforced at two call sites:

- **AU6** (above) sweeps every `docs/product/*.md`: exactly one legal
  line inside the `## Release slice` section; a `Rigor level:` line
  anywhere else, a missing line, duplicates, or an illegal value is a
  named problem.
- **The design rung** refuses work whose product doc violates the law,
  with one need row: `need: docs/product/<S>.md — Release slice
  declares a legal rigor level (Rigor level: spike|mvp|production-v1)`.

A doc with no `## Release slice` section passes vacuously — the
section's absence is already the design rung's own refusal, and the
rigor rule does not double-refuse it. The declared level is data for
later slices (the rigor catalog and per-class disposition tables);
this slice enforces only that the level question is asked and answered
legally.
```

**Verify:** `grep -c 'AU6' /Users/anthonymaley/Kerd/tools/gates/README.md` prints ≥ 3, and `grep -n '24 cases\|six rules\|^## Rigor level' /Users/anthonymaley/Kerd/tools/gates/README.md` shows all three hits.

### Step 8 — Version bump to 0.81.0 (three fields)

`[delegate, model: haiku, effort: low]` — replace `"version": "0.80.0"`
with `"version": "0.81.0"` in:

- `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` (one occurrence)
- `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` (BOTH
  occurrences: `metadata.version` and `plugins[0].version`)

Descriptions untouched (behavior change is in tools, not skills — the
capability list is unaffected). MINOR bump: new feature.

**Verify:** `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py release` exits 0 printing exactly `release: clean`.

### Step 9 — Full local suite

`[keep]` — run every `run:` line from
`/Users/anthonymaley/Kerd/.github/workflows/gate.yml` locally (list them
with `grep 'run:' /Users/anthonymaley/Kerd/.github/workflows/gate.yml`),
from `$BASE`, EXCEPT the progress `stale` step — stale compares the
fresh render against the committed pair, whose natural green moment is
after Step 12's refresh commit; it runs there. Expected known outputs:
gate selftest `selftest: 24 cases passed`, gate audit `audit: clean`,
gate release `release: clean`; the progress and matrix selftest/audit
commands (exact paths per gate.yml — do not guess them) each exit 0.

**Verify:** every executed run line exits 0; `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py selftest` prints `selftest: 24 cases passed`.

### Step 10 — Work commit (one commit, with trailer)

`[keep]` — first re-review the full staged picture:
`git -C /Users/anthonymaley/Kerd status --porcelain` must list exactly
these modified files plus this spec:

    tools/gates/kit.py
    tools/gates/README.md
    docs/product/push-wiring.md
    docs/product/grounding-was-read.md
    docs/product/progress-html.md
    docs/product/rigor-level.md
    .claude-plugin/plugin.json
    .claude-plugin/marketplace.json
    docs/plans/2026-08-05-rigor-level-spec.md

Check the Pieces boxes for Steps 1–9 in this spec, stage all of the
above, and commit — ONE commit, message:

    rigor-level slice 1: Rigor level declared in every Release slice — AU6 + design-rung refusal (v0.81.0)

    Claude-Session: https://claude.ai/code/session_01B7yNRTL9d6oJJQcpLVMaSq

Do NOT push yet — the push is Step 12's, single, after the render commit.

**Verify:** `git -C /Users/anthonymaley/Kerd show --stat HEAD` lists exactly the nine files above, and `git -C /Users/anthonymaley/Kerd log -1 --format=%B` ends with the `Claude-Session:` trailer line.

### Step 11 — Both-ways demo (strip → red verbatim; restore → clean)

`[keep]` — runs AFTER the work commit so `git restore` is a safe
restore. Strip one retrofit line:

    python3 -c "p='/Users/anthonymaley/Kerd/docs/product/push-wiring.md'; t=open(p).read(); open(p,'w').write(t.replace('Rigor level: mvp\n\n','',1))"

Run `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py audit` —
expect exit 1 printing exactly:

    problem: docs/product/push-wiring.md — Release slice missing 'Rigor level: <spike|mvp|production-v1>' line
    audit: 1 problems

Restore: `git -C /Users/anthonymaley/Kerd restore docs/product/push-wiring.md`,
then audit again — expect exit 0, `audit: clean`.

WHY: proves the refusal both fires and names the file verbatim on the
REAL tree (not just fixtures), and that the shipped state is clean.

**Verify:** the stripped audit exits 1 with the two lines above verbatim; after restore, `python3 /Users/anthonymaley/Kerd/tools/gates/gate.py audit` exits 0 printing `audit: clean` and `git -C /Users/anthonymaley/Kerd status --porcelain` is empty.

### Step 12 — Progress refresh, render commit, stale check, single push

`[keep]` — in order:

1. Check the remaining Pieces boxes (Steps 10–12) in this spec.
2. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py` (the refresh).
3. `git -C /Users/anthonymaley/Kerd add -A` then
   `git -C /Users/anthonymaley/Kerd commit -m "Refresh progress render"`
   — NO trailer (render-only commits never carry one; that is the
   depth-1 convergence rule from push-wiring). If the refresh produced
   no diff beyond the box-checks, the commit still lands with the same
   message.
4. `python3 /Users/anthonymaley/Kerd/tools/diagram/progress.py stale` — expect exit 0.
5. `git -C /Users/anthonymaley/Kerd push` — ONE push carrying both commits.

**Verify:** `git -C /Users/anthonymaley/Kerd status --porcelain` prints nothing and `git -C /Users/anthonymaley/Kerd rev-list origin/main..HEAD --count` prints `0`.
