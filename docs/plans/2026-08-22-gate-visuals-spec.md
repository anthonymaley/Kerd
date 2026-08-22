# Gate visuals — slice 1, the design rung counts its views

Contract for `docs/product/gate-visuals.md`, release slice 1 (rigor: mvp).
Design: `docs/design/gate-visuals.md`; GO record:
`docs/gates/2026-08-22-gate-visuals-design.md`.

**What lands.** A work item declares its agreed concern list in the front
matter of `docs/product/<slug>.md`. The design rung of `tools/gates/kit.py`
counts views against that list — every declared concern has a view on disk
or an `n/a — <reason>`; every view carries an approval sealed with a
fingerprint over the `.html`'s content, computed at approval and invalidated
by any content edit. A new `gate.py seal <slug>` subcommand completes a
hand-written approval with its fingerprint, exactly as reqview's `seal`
completes a requirement's approval line. Vocabulary is ISO/IEC/IEEE 42010
throughout: *concern* (what matters), *viewpoint* (the diagram type), *view*
(the drawing).

**What does not land.** No comparison against the built side (slice 2). No
new approval machinery beyond the writer. No progress-board or
evaluation-matrix change. No check that a drawing is a diagram rather than
a slide — the design's stated limit.

**No version bump.** The plugin's version bumps when skill text changes; no
`skills/*/SKILL.md` changes here. `gate.py release` checks version *sync*,
not a bump, so it stays clean.

**No workflow change.** `.github/workflows/gate.yml` runs
`gate.py selftest` and `gate.py audit` on every push. The new fixtures ride
`selftest`; the new repo-wide audit rule AU9 (Step 2) rides `audit`. Note
the premise correction: CI never runs `check <slug> <rung>` — so without
AU9 an edited approved drawing would only be refused when someone ran
`check` by hand. AU9 is what makes the invalidation fire from outside the
model.

**Step headings are `### Step N — <name>`**, not `## Step`, because the
build rung's own check (`STEP_HEADING_RE = ^### Step `) binds on `###` and
is vacuous on `##`. The brief's shape is otherwise followed exactly.

---

## Decisions the steps depend on

### D1 — the front-matter schema (`docs/product/<slug>.md`)

```
---
route: new
stage: designed
concerns:
  - concern: <what matters, free text>
    viewpoint: <the diagram type, free text — e.g. state, flowchart, sequence>
    view: <path relative to the repo root, must end .html>
    approval: <name>, <YYYY-MM-DD>                  # hand-written; seal completes it
  - concern: <another>
    view: n/a — <reason it owes no drawing>        # no viewpoint, no approval
---
```

Grammar, exact (all inside the front-matter fence):

| Line | Regex | Meaning |
|---|---|---|
| opener | `^concerns:\s*$` | bare key, opens the list. A value on this line is a parse problem. |
| entry | `^  - concern:\s*(.*)$` (two spaces, dash, space) | starts an entry; the capture is the concern name |
| field | `^    (viewpoint\|view\|approval):\s*(.*)$` (four spaces) | a field of the current entry |
| end | the closing `---`, or any line matching `FRONT_MATTER_KV_RE` (a top-level key) | closes the list |
| other | anything else inside the list, blank lines included | parse problem: `concerns: line <n> unreadable: '<line.strip()>'` (n = 1-based file line) |

Values are stripped; a matching pair of surrounding quotes is removed, the
same rule `read_front_matter` applies. Parse problems (each a `need` row,
prefixed `docs/product/<slug>.md — `):

- `concerns: line carries a value; it must be bare` — opener with text after the colon
- `concerns: declared with no entries`
- `concerns: line <n> field before any entry`
- `concerns: line <n> entry has no concern name`
- `concerns: entry "<c>" repeats <field>`
- `concerns: entry "<c>" is n/a and carries an approval — nothing to approve`
- `concerns: line <n> unreadable: '<text>'`

**Absent `concerns:` = the design rung behaves exactly as today.** Declaring
is opting in — the AU5 (`## Grounding`) precedent. The existing reader
already survives the block: `FRONT_MATTER_KV_RE` (`^([A-Za-z0-9_.-]+):`)
does not match indented lines, so `read_front_matter` returns
`{"route","stage","concerns": ""}` and AU2/AU4 only ever read `route` and
`stage`. **The one reader extension:** the closing-fence window grows from
30 lines to 120 (`min(len(lines), 31)` → `min(len(lines), 121)`), because
a real concern list (the frame's table had sixteen rows) overflows 30.
Fixture T33.

Two entries may share a concern name — that is two views of one concern.
The unit the gate counts is the entry.

### D2 — the fingerprint covers the `.html` only

The PNG is a render of the `.html`; a derived artifact is never approved
(the board rule). A `view:` path that does not end `.html` is refused.

**Bytes hashed.** Rule 9's recipe, with the file's content as the
Statement and the other three fields empty: read the file as UTF-8 text;
trim it and collapse every internal whitespace run to a single space; join
the four fields with single `\n` (so the hashed text is the collapsed
content followed by three newlines); SHA-256 over the UTF-8 bytes; first
twelve hex characters. Equivalent by hand:

```python
hashlib.sha256((" ".join(text.split()) + "\n\n\n").encode("utf-8")).hexdigest()[:12]
```

Collapsing whitespace is the recipe's own rule — a formatting-only edit
must not un-approve a drawing.

**Test vector (fixture T34 must reproduce all three):**

```python
FX = '<svg viewBox="0 0 8 8">\n  <rect x="0" y="0" width="4" height="4"/>\n</svg>\n'
view_fingerprint(FX)                                    == "2878c07db022"
view_fingerprint(FX + "   \n\n")                        == "2878c07db022"   # whitespace-only edit: same
view_fingerprint(FX.replace('height="4"', 'height="8"')) == "c938aa15c609"   # content edit: different
```

The two live drawings, at HEAD `2016134` on 2026-08-22:
`docs/design/gate-visuals/visual-lifecycle.html` → `3ef85a6441d5`;
`docs/design/gate-visuals/design-gate-check.html` → `ccbac6efdb93`.

### D3 — one implementation of the recipe: a shared module

**Choice:** move `fingerprint()` out of `tools/reqview/reqview.py` into a
new `tools/reqview/fingerprint.py` (the recipe and nothing else, plus
`view_fingerprint`). `reqview.py` imports it as a sibling (`from fingerprint
import fingerprint` — the script's own directory is `sys.path[0]`);
`kit.py` inserts `<its own dir>/../reqview` on `sys.path` (path-safe:
relative to `__file__`, never to the audited `root`, so a consuming project
without `tools/` still resolves it inside the plugin install) and imports
`view_fingerprint`.

**Reason, over importing `reqview` into `kit`:** rule 9 says every
implementation must share the recipe exactly; the way that is guaranteed is
one module whose only content is the recipe. A gate that runs in CI should
not depend on importing a 2,000-line, spike-labelled CLI whose module body
(register paths, output path, an HTML template) is about a different job —
and if that spike is ever killed, the gate must not die with it. The
reqview side of the change is two lines; `seal()` is untouched; reqview's
own `selftest()` (both published vectors) proves the recipe unchanged.
`editor.py` does not reference `fingerprint` — checked.

### D4 — the design rung's rows

Computed per entry, in entry order, first failing rule wins. `P` =
`docs/product/<slug>.md — `. Every row is a count on disk (R-0051).

| # | Rule | code | Row (verbatim) |
|---|---|---|---|
| a1 | entry has no `view` | `no-view` | need `P concern "<c>": no view and no n/a reason` |
| a2 | `view` starts `n/a` but does not match `^n/a\s+—\s+(\S.*)$` | `na-no-reason` | need `P concern "<c>": n/a without a reason` |
| a3 | `view` is `n/a — <reason>` | `na` | have `P concern "<c>": n/a — <reason>` |
| a4 | `viewpoint` absent or empty | `no-viewpoint` | need `P concern "<c>": view <path> has no viewpoint` |
| a5 | path does not end `.html` | `not-html` | need `P concern "<c>": view <path> is not .html — a render is never the view` |
| b | `os.path.isfile(os.path.join(root, path))` false | `missing` | need `P concern "<c>": view <path> not on disk` |
| c1 | no `approval` | `unapproved` | need `P concern "<c>": view <path> unapproved — no approval line` |
| c2 | approval matches `VIEW_SEALED_RE` and fp == computed | `ok` | have `P concern "<c>": <viewpoint> view <path> approved by <name>, <date> (fp:<fp>)` |
| c3 | approval matches `VIEW_SEALED_RE`, fp != computed | `mismatch` | need `P concern "<c>": view <path> fingerprint mismatch — approved at fp:<stored>, now fp:<computed>` |
| c4 | approval matches `VIEW_UNSEALED_RE` | `unsealed` | need `P concern "<c>": view <path> approved by hand, not sealed — no fp` |
| c5 | anything else | `unreadable` | need `P concern "<c>": view <path> approval line unreadable: '<text>'` |

```python
VIEW_SEALED_RE   = re.compile(r'^(.+?),\s*(\d{4}-\d{2}-\d{2})\s*·\s*fp:([0-9a-f]{12})\s*$')   # · is U+00B7, as reqview
VIEW_UNSEALED_RE = re.compile(r'^(.+?),\s*(\d{4}-\d{2}-\d{2})\s*$')
NA_VIEW_RE       = re.compile(r'^n/a\s+—\s+(\S.*)$')
```

A mismatch is refused, never rewritten — the requirement-register
precedent. The viewpoint is free text at mvp: no closed viewpoint list is
checked (the UI viewpoint is a named gap, not a vocabulary rule).

**AU9 (repo-wide audit).** For every `docs/product/*.md` whose front matter
declares `concerns:`: every parse problem, and every row whose code is not
in `{ok, na, unapproved, unsealed}`, is an audit problem with the same text.
Pending approvals are the rung's business; a declaration that is *wrong* —
unreadable, missing file, a render, a changed drawing — refuses on push.

---

## Pieces

- [ ] 1. `tools/reqview/fingerprint.py` — the shared recipe; reqview imports it
- [ ] 2. `tools/gates/kit.py` — reader window, `parse_concerns`, `view_rows`, design-rung rows, AU9
- [ ] 3. `tools/gates/kit.py` + `gate.py` — `seal_views` and the `seal` subcommand
- [ ] 4. `tools/gates/kit.py` — fixtures T33–T41 (`selftest: 41 cases passed`)
- [ ] 5. Diff review of pieces 1–4 against D1–D4
- [ ] 6. Dogfood: `docs/product/gate-visuals.md` declares its two views, refuses, seals, passes
- [ ] 7. `tools/gates/README.md` + `docs/design/gate-visuals.md` open question 2
- [ ] 8. Full local suite and the render refresh

---

### Step 1 — the shared recipe module

[delegate, model: sonnet, effort: medium]

**What.** Create `/Users/anthonymaley/Kerd/tools/reqview/fingerprint.py`
with exactly these two functions (the `fingerprint` body is a verbatim move
of `reqview.py` lines 114–119 — do not alter a character of its body):

```python
#!/usr/bin/env python3
"""Rule 9's fingerprint — the one implementation, shared.

docs/design/requirement-shape.md rule 9 says every implementation must share
the recipe exactly; the way to make that true is to have one. reqview.py
(the register's seal) and tools/gates/kit.py (the design gate's view lock)
both import this module, and nothing else computes a fingerprint.

Recipe: four fields in order — statement, why, traces, depends — each
trimmed with every internal whitespace run collapsed to one space; joined
with single newlines; SHA-256 over the UTF-8 bytes; first twelve hex
characters. A derived statement is prefixed `derived: ` so flipping the
flag un-approves.

A view (a drawing — docs/design/gate-visuals.md) uses the same recipe with
its file content as the statement and the other three fields empty, so the
hashed text is the collapsed content followed by three newlines.
"""
import hashlib


def fingerprint(statement, why, traces, depends, derived):
    """Rule 9. Labels are already stripped by the parser (whole, modifier included).
    A derived statement is prefixed `derived: ` so flipping the flag un-approves."""
    stmt = ("derived: " + statement) if derived else statement
    parts = [stmt, why, traces, depends]
    joined = "\n".join(" ".join(p.split()) for p in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def view_fingerprint(text):
    """A view's lock: the recipe over its file content as the statement,
    the other three fields empty. Whitespace-only edits do not change it."""
    return fingerprint(text, "", "", "", False)
```

In `/Users/anthonymaley/Kerd/tools/reqview/reqview.py`, replace the
`def fingerprint(...)` block (lines 114–119, the def and its six lines)
with this single line, keeping the three comment lines above it (110–112)
as they are:

```python
from fingerprint import fingerprint  # rule 9 — the one implementation, tools/reqview/fingerprint.py
```

Leave every other line of `reqview.py` alone, including `import hashlib`
and the whole of `seal()`. No `__init__.py`, no package.

**Why.** D3. A sibling import works because `python3 tools/reqview/reqview.py`
puts `tools/reqview` at `sys.path[0]`; the import sits where the def was so
the section comment still tells the truth.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 -c "
import sys; sys.path.insert(0,'tools/reqview'); import reqview, fingerprint
print(reqview.fingerprint is fingerprint.fingerprint)
print([ok for *_, ok in reqview.selftest()])
print(fingerprint.view_fingerprint(open('docs/design/gate-visuals/visual-lifecycle.html', encoding='utf-8').read()))
" && grep -c '^def fingerprint' tools/reqview/reqview.py tools/reqview/fingerprint.py
```

Expected, exactly:

```
True
[True, True]
3ef85a6441d5
tools/reqview/reqview.py:0
tools/reqview/fingerprint.py:1
```

---

### Step 2 — kit.py: the reader window, `parse_concerns`, `view_rows`, the design rows, AU9

[delegate, model: sonnet, effort: high]

**What.** Edit `/Users/anthonymaley/Kerd/tools/gates/kit.py`. Stdlib only.
Every function takes `root` where it touches disk.

1. **Imports.** Add `import sys` to the import block. After `ROOT = ...`
   add:

   ```python
   # Rule 9's recipe has one implementation — tools/reqview/fingerprint.py.
   # Resolved from THIS file's location, never from the audited root: a
   # consuming project has no tools/ of its own and the recipe ships here.
   sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "reqview"))
   from fingerprint import view_fingerprint
   ```

2. **Constants.** Next to `FRONT_MATTER_KV_RE` add:

   ```python
   CONCERNS_KEY_RE   = re.compile(r'^concerns:(.*)$')
   CONCERN_ENTRY_RE  = re.compile(r'^  - concern:\s*(.*)$')
   CONCERN_FIELD_RE  = re.compile(r'^    (viewpoint|view|approval):\s*(.*)$')
   NA_VIEW_RE        = re.compile(r'^n/a\s+—\s+(\S.*)$')
   VIEW_SEALED_RE    = re.compile(r'^(.+?),\s*(\d{4}-\d{2}-\d{2})\s*·\s*fp:([0-9a-f]{12})\s*$')
   VIEW_UNSEALED_RE  = re.compile(r'^(.+?),\s*(\d{4}-\d{2}-\d{2})\s*$')
   ```

3. **Reader window.** Factor the fence-finding out of `read_front_matter`
   into `_front_matter_block(path) -> (lines, close) | None` — `lines` is
   the whole file's `splitlines()`, `close` the index of the closing fence;
   `None` when the file is absent, line 0 is not `---`, or no closing `---`
   within **120** lines (`range(1, min(len(lines), 121))`). `read_front_matter`
   calls it and keeps its exact current behaviour otherwise (the A1
   docstring's "30 lines" becomes "120 lines").

4. **`parse_concerns(path) -> None | (entries, problems)`** — in the front
   matter section, after `read_front_matter`. `None` when there is no front
   matter or no line matching `CONCERNS_KEY_RE` inside it. Otherwise walks
   the lines after the opener up to the first closing fence or top-level
   `FRONT_MATTER_KV_RE` line, applying D1's grammar exactly. Each entry is
   `{"concern": str, "viewpoint": str|None, "view": str|None,
   "approval": str|None, "index": int, "approval_index": int|None}` where
   the indexes are 0-based positions in `lines` (the entry line; the
   approval line). Values stripped, matching surrounding quotes removed
   (same rule as `read_front_matter`). Problems are D1's seven strings,
   without the `docs/product/... — ` prefix (callers prefix).

5. **`view_rows(root, entries) -> list[dict]`** — a new section
   `# ── views (the design gate's lock) ──` placed immediately before
   `def check_rung`. One dict per entry, entry order, keys: `code` (D4's
   code), `concern`, `detail` (the text after `concern "<c>": `), `text`
   (`concern "<c>": <detail>`), and when a path exists `path`; when an
   approval parsed `name`, `date`; when a fingerprint was computed `fp_now`;
   on `ok`/`mismatch` `fp_stored`. Rules and texts are D4's table, first
   failing rule wins. The file is read `open(p, encoding="utf-8").read()`
   and hashed with `view_fingerprint`.

6. **Design rung.** In `check_rung`, inside `if idx >= RUNGS.index("design")`
   and its `else` (product exists), after the rigor check, add:

   ```python
   cs = parse_concerns(abs_product)
   if cs is not None:
       entries, problems = cs
       for p in problems:
           need.append(f"{rel_product} — {p}")
       for r in view_rows(root, entries):
           (have if r["code"] in ("ok", "na") else need).append(f"{rel_product} — {r['text']}")
   ```

   Nothing else in `check_rung` changes. Absent `concerns:` → no new rows.

7. **AU9.** Add `_audit_au9(root)` after `_audit_au8`, docstring: *"Every
   docs/product/*.md declaring `concerns:`: the block parses and no view is
   in a wrong state — a render, a missing file, a changed drawing, an
   unreadable approval. Pending approvals (no line yet, or hand-written
   and not sealed) are the design rung's business, not the audit's."*
   For each product doc in sorted order: `parse_concerns`; skip `None`;
   every problem and every row with code not in
   `{"ok", "na", "unapproved", "unsealed"}` → `f"docs/product/{fname} — {text}"`.
   Append `problems += _audit_au9(root)` to `audit()` and change its
   docstring's `AU1-AU8` to `AU1-AU9`.

**Why.** D1, D4. `view_rows` returns codes rather than have/need so the
rung, the audit and `seal` (Step 3) all branch on the same classification
— one implementation of the rules, not three.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 - <<'EOF'
import sys, os, tempfile
sys.path.insert(0, 'tools/gates'); import kit
d = tempfile.mkdtemp(); p = os.path.join(d, 'docs', 'product', 'z.md'); os.makedirs(os.path.dirname(p))
open(p, 'w', encoding='utf-8').write(
    "---\nroute: new\nstage: framed\nconcerns:\n"
    "  - concern: a\n    viewpoint: state\n    view: docs/design/z/a.html\n    approval: Tony, 2026-01-05 · fp:2878c07db022\n"
    "  - concern: b\n    view: n/a — nothing to draw\n---\n\n## Value\n\nx\n")
e, pr = kit.parse_concerns(p); print(len(e), pr)
for r in kit.view_rows(d, e): print(r['code'], '|', r['text'])
print(kit.read_front_matter(p))
EOF
```

Expected: `selftest: 32 cases passed` (preceded by `root resolution: 7 cases passed`), `audit: clean` (a findings count in parentheses is fine), then exactly:

```
2 []
missing | concern "a": view docs/design/z/a.html not on disk
na | concern "b": n/a — nothing to draw
{'route': 'new', 'stage': 'framed', 'concerns': ''}
```

---

### Step 3 — `seal_views` and `gate.py seal`

[delegate, model: sonnet, effort: medium]

**What.**

1. In `/Users/anthonymaley/Kerd/tools/gates/kit.py`, in the views section,
   add `seal_views(root, slug) -> dict` with keys:
   `product` (`docs/product/<slug>.md`), `exists` (bool), `declared` (bool),
   `parse_problems` ([str]), `sealed` ([[concern, path, name, date, fp]]),
   `already` ([[concern, path, fp]]), `diverged` ([[concern, path, was, now]]),
   `unapproved` ([[concern, path]]), `refused` ([[concern, path, why]]),
   `unreadable` ([[concern, text]]), `written` (bool). Algorithm:
   - product file absent → `exists=False`, all lists empty, return.
   - `parse_concerns` is `None` → `declared=False`, return.
   - parse problems → fill `parse_problems`, `written=False`, return. Nothing written.
   - for each row of `view_rows(root, entries)`: `no-view`, `na`,
     `na-no-reason` → skip (nothing to seal); `no-viewpoint`, `not-html`,
     `missing` → `refused` with `why = detail`; `unapproved` → `unapproved`;
     `ok` → `already`; `mismatch` → `diverged` (stored, now); `unreadable` →
     `unreadable` (the approval text); `unsealed` → compute `fp_now`, and
     replace the approval line in place:
     ```python
     lines = text.splitlines(keepends=True)          # same count as splitlines()
     old = lines[entry["approval_index"]]
     ending = old[len(old.rstrip("\r\n")):]
     lines[entry["approval_index"]] = f"    approval: {name}, {date} · fp:{fp_now}" + ending
     ```
     and record `sealed`.
   - if `sealed` is non-empty, write `"".join(lines)` back (UTF-8) and set
     `written=True`; otherwise the file is not opened for writing.
   Divergence is reported and never rewritten; nothing is written when
   anything fails to parse.

2. In `/Users/anthonymaley/Kerd/tools/gates/gate.py` add `_cmd_seal(argv)`
   (`seal <slug> [--root PATH] [--json]`; wrong arity → usage, exit 2),
   register it in `COMMANDS` as `"seal"`, and add to the module docstring
   the usage line `python3 tools/gates/gate.py seal <slug> [--root PATH]
   [--json]` plus one sentence: *"seal completes every hand-written view
   approval in the slug's concerns block with its fingerprint: exit 0 when
   nothing was refused, diverged or unreadable, else 1. It never rewrites a
   divergence."* Also amend the docstring's list of refusers so `seal` is
   named with `check`, `audit` and `release`. Text render, verbatim:

   ```
   not exists   → print(f"seal — {product}: no such work item"); return 1
   not declared → print(f"seal — {product}: no concerns block; nothing to seal"); return 1
   parse_problems → print(f"REFUSED — {product}: the concerns block does not parse; nothing was sealed.")
                    then one line per problem, indented two spaces; return 1
   otherwise:
     print(f"seal — {product}")
     for c, p, n, d, fp in sealed:      print(f"  sealed     {c}  {p}  {n}, {d} · fp:{fp}")
     for c, p, fp in already:           print(f"  already    {c}  {p}  fp:{fp}")
     for c, p, was, now in diverged:    print(f"  DIVERGED   {c}  {p}  approved at fp:{was}, now fp:{now} — the drawing changed since it was agreed. Not rewritten.")
     for c, p, why in refused:          print(f"  REFUSED    {c}  {p}  {why}")
     for c, p in unapproved:            print(f"  unapproved {c}  {p}  no approval line — nothing to seal")
     for c, t in unreadable:            print(f"  UNREADABLE {c}  approval line {t!r} is neither `<name>, YYYY-MM-DD` nor a sealed approval. Nothing was assumed.")
     print(f"  {len(sealed)} sealed · {len(refused)} refused · {len(already)} already approved · {len(diverged)} diverged")
     return 1 if (refused or diverged or unreadable) else 0
   ```

   `--json` prints `json.dumps(result)` and returns the same exit code.

**Why.** The producer types `<name>, <date>` and never a hash — reqview's
`seal` contract, applied to a view. Editing by line index inside the front
matter is what makes the rewrite unique: two views approved on the same
day carry identical approval text, so a text search would find two and
have to refuse (reqview's `block_span` lesson).

**Verify:**

```
cd /Users/anthonymaley/Kerd && D=$(mktemp -d) && mkdir -p "$D/docs/product" "$D/docs/design/z" && printf '<svg viewBox="0 0 8 8">\n  <rect x="0" y="0" width="4" height="4"/>\n</svg>\n' > "$D/docs/design/z/a.html" && printf -- '---\nroute: new\nstage: framed\nconcerns:\n  - concern: a\n    viewpoint: state\n    view: docs/design/z/a.html\n    approval: Tony, 2026-01-05\n  - concern: b\n    viewpoint: state\n    view: docs/design/z/b.html\n    approval: Tony, 2026-01-05\n---\n\n## Value\n\nx\n' > "$D/docs/product/z.md" && python3 tools/gates/gate.py seal z --root "$D"; echo "exit=$?"; grep -n 'approval:' "$D/docs/product/z.md"; python3 tools/gates/gate.py seal z --root "$D"; echo "exit=$?"
```

Expected, exactly:

```
seal — docs/product/z.md
  sealed     a  docs/design/z/a.html  Tony, 2026-01-05 · fp:2878c07db022
  REFUSED    b  docs/design/z/b.html  view docs/design/z/b.html not on disk
  1 sealed · 1 refused · 0 already approved · 0 diverged
exit=1
8:    approval: Tony, 2026-01-05 · fp:2878c07db022
12:    approval: Tony, 2026-01-05
seal — docs/product/z.md
  already    a  docs/design/z/a.html  fp:2878c07db022
  REFUSED    b  docs/design/z/b.html  view docs/design/z/b.html not on disk
  0 sealed · 1 refused · 1 already approved · 0 diverged
exit=1
```

---

### Step 4 — fixtures T33–T41

[delegate, model: sonnet, effort: high]

**What.** Append nine cases to `_selftest_body()` in
`/Users/anthonymaley/Kerd/tools/gates/kit.py`, after T32, each in its own
`tempfile.TemporaryDirectory()` unless stated. Update `selftest()`'s
docstring and its print to `selftest: 41 cases passed`. Define at the top
of the new block:

```python
FX = '<svg viewBox="0 0 8 8">\n  <rect x="0" y="0" width="4" height="4"/>\n</svg>\n'
BODY = ("\n## Value\n\nSaves 10 hours/week.\n\n## Risk ledger\n\n"
        "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| Adoption risk | yes | high | medium | 3 interviews | accepted | | check Q2 |\n"
        "\n## Release slice\n\nRigor level: mvp\n\nShip it.\n")
P = "docs/product/alpha.md — "
```

| # | Fixture | Assert |
|---|---|---|
| T33 | (window) product = `"---\nroute: new\nstage: framed\n" + "".join(f"k{i}: v\n" for i in range(40)) + "---\n" + BODY` | `read_front_matter(product)["route"] == "new"`. Then product = `"---\nroute: new\n" + "k: v\n" * 130` (no closing fence) → `read_front_matter(product) is None` |
| T34 | (recipe) no tree needed | `view_fingerprint(FX) == "2878c07db022"`; `view_fingerprint(FX + "   \n\n") == "2878c07db022"`; `view_fingerprint(FX.replace('height="4"', 'height="8"')) == "c938aa15c609"`; `hashlib.sha256((" ".join(FX.split()) + "\n\n\n").encode("utf-8")).hexdigest()[:12] == "2878c07db022"`; and `import reqview` (same `sys.path` entry Step 2 inserted) → `all(ok for *_, ok in reqview.selftest())` |
| T35 | (opt-in) product = `"---\nroute: new\nstage: framed\n---\n" + BODY` (no `concerns:`) | `cr = check_rung(root, "alpha", "design")`; `cr["need"] == []` and `not any('concern "' in h for h in cr["have"])` |
| T36 | (the refusals) product = the T36 front matter below + BODY; write FX to `docs/design/alpha/{d,e,g,h}.html`; do **not** create `c.html` | `check_rung(root, "alpha", "design")["need"]` equals, in order, the seven T36 rows below; `P + 'concern "f": n/a — covered by the README table'` is in `have` |
| T37 | (seal) on T36's tree, `r = seal_views(root, "alpha")` | `r["sealed"] == [["e", "docs/design/alpha/e.html", "Tony", "2026-01-05", "2878c07db022"]]`; `r["diverged"] == [["g", "docs/design/alpha/g.html", "000000000000", "2878c07db022"]]`; `r["unapproved"] == [["d", "docs/design/alpha/d.html"]]`; `r["refused"] == [["c", "docs/design/alpha/c.html", "view docs/design/alpha/c.html not on disk"]]`; `r["unreadable"] == [["h", "approved!!"]]`; `r["written"] is True`; the file now differs from before in exactly one line, and that line is `    approval: Tony, 2026-01-05 · fp:2878c07db022`; a second `seal_views` → `sealed == []`, `already == [["e", "docs/design/alpha/e.html", "2878c07db022"]]`, `written is False`; `check_rung(...,"design")["have"]` contains `P + 'concern "e": state view docs/design/alpha/e.html approved by Tony, 2026-01-05 (fp:2878c07db022)'` |
| T38 | (edit invalidates) on T37's tree, overwrite `e.html` with `FX.replace('height="4"', 'height="8"')`; snapshot the product bytes | `check_rung(...,"design")["need"]` contains `P + 'concern "e": view docs/design/alpha/e.html fingerprint mismatch — approved at fp:2878c07db022, now fp:c938aa15c609'`; `seal_views` → `diverged` contains `["e", "docs/design/alpha/e.html", "2878c07db022", "c938aa15c609"]`, `written is False`, product bytes unchanged |
| T39 | (clean pass) product front matter: `route: new`, `stage: framed`, `concerns:` with `- concern: one` / `viewpoint: state` / `view: docs/design/alpha/one.html` / `approval: Tony, 2026-01-05 · fp:2878c07db022`, and `- concern: two` / `view: n/a — nothing to draw`; + BODY; FX written to `one.html` | `check_rung(root, "alpha", "design")["need"] == []`; `route(root, "alpha")["enters_at"] == "design"`; `audit(root) == []` |
| T40 | (parse problems) product = the T40 front matter below + BODY; write FX to `docs/design/alpha/y.png` | `need` contains `P + 'concerns: entry "x" is n/a and carries an approval — nothing to approve'`, `P + "concerns: line 11 unreadable: 'this line is junk'"` and `P + 'concern "y": view docs/design/alpha/y.png is not .html — a render is never the view'`; `seal_views` → `len(parse_problems) == 2`, `written is False`, product bytes unchanged |
| T41 | (AU9) T36's tree, untouched by seal | `audit(root)` equals exactly, in order: the T36 rows for `a`, `b`, `c`, `g`, `h` (five problems — `d` and `e` are pending, `f` is n/a) |

**T36 front matter** (then BODY):

```
---
route: new
stage: framed
concerns:
  - concern: a
  - concern: b
    view: n/a
  - concern: c
    viewpoint: state
    view: docs/design/alpha/c.html
  - concern: d
    viewpoint: flowchart
    view: docs/design/alpha/d.html
  - concern: e
    viewpoint: state
    view: docs/design/alpha/e.html
    approval: Tony, 2026-01-05
  - concern: f
    view: n/a — covered by the README table
  - concern: g
    viewpoint: sequence
    view: docs/design/alpha/g.html
    approval: Tony, 2026-01-05 · fp:000000000000
  - concern: h
    viewpoint: state
    view: docs/design/alpha/h.html
    approval: approved!!
---
```

**T36 rows** (each prefixed `P`):

```
concern "a": no view and no n/a reason
concern "b": n/a without a reason
concern "c": view docs/design/alpha/c.html not on disk
concern "d": view docs/design/alpha/d.html unapproved — no approval line
concern "e": view docs/design/alpha/e.html approved by hand, not sealed — no fp
concern "g": view docs/design/alpha/g.html fingerprint mismatch — approved at fp:000000000000, now fp:2878c07db022
concern "h": view docs/design/alpha/h.html approval line unreadable: 'approved!!'
```

**T40 front matter** (then BODY; the junk line is file line 11):

```
---
route: new
stage: framed
concerns:
  - concern: x
    view: n/a — nothing to draw
    approval: Tony, 2026-01-05
  - concern: y
    viewpoint: state
    view: docs/design/alpha/y.png
  this line is junk
---
```

**Why.** T34 pins the recipe three ways (shared module, by-hand hashlib,
reqview's two published vectors) so a drift in any one is caught in CI.
T36/T41 enumerate every refusal text verbatim — the text is the contract a
reader acts on, so a wording drift is a failure.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest; echo "exit=$?"
```

Expected: `root resolution: 7 cases passed`, `selftest: 41 cases passed`, `exit=0`.

---

### Step 5 — diff review of pieces 1–4

[keep]

**What.** Read `git diff -- tools/reqview/reqview.py tools/reqview/fingerprint.py tools/gates/kit.py tools/gates/gate.py` against D1–D4 line by line. It must catch:

- the `fingerprint` body in `fingerprint.py` is byte-identical to the one removed from `reqview.py`; `seal()` in reqview is untouched; no second `def fingerprint` anywhere (`grep -rn "def fingerprint" tools/` → one hit)
- `kit.py` resolves the `reqview` path from `__file__`, never from `root`
- every row text in `view_rows` matches D4's table character for character (the `—` is an em dash, the `·` is U+00B7)
- first-failing-rule order is a1 → a2 → a3 → a4 → a5 → b → c1–c5; `no-viewpoint` is checked before the file is opened
- `seal_views` opens the product for writing only when `sealed` is non-empty, and never on a parse problem; divergence is reported, never rewritten
- the design rung adds nothing when `concerns:` is absent; AU9 skips `unapproved` and `unsealed`
- the reader window is 120 and the A1 docstring says so; nothing else in `read_front_matter` changed
- no `git add -A`, no file outside the four named was touched (`git status --porcelain` lists exactly those four)

**Why.** The rung, the audit and the writer share one classification; a
wording or ordering slip in `view_rows` is invisible to any single command
but changes what three tools say. A miss is re-dispatched to its step,
never patched in review.

**Verify:** every line above ticked; `git status --porcelain` shows exactly
`M tools/gates/gate.py`, `M tools/gates/kit.py`, `M tools/reqview/reqview.py`,
`?? tools/reqview/fingerprint.py`.

---

### Step 6 — dogfood: gate-visuals declares its own two views

[delegate, model: haiku, effort: low]

**What.** Replace lines 1–4 of
`/Users/anthonymaley/Kerd/docs/product/gate-visuals.md` (the front matter,
currently `route: new` / `stage: designed`) with exactly:

```
---
route: new
stage: designed
concerns:
  - concern: the life of a gate visual
    viewpoint: state
    view: docs/design/gate-visuals/visual-lifecycle.html
    approval: Tony, 2026-08-22
  - concern: what the design gate refuses
    viewpoint: flowchart
    view: docs/design/gate-visuals/design-gate-check.html
    approval: Tony, 2026-08-22
---
```

Then run, in order: `python3 tools/gates/gate.py check gate-visuals design`
(expect a refusal — the live demonstration), `python3 tools/gates/gate.py seal gate-visuals`,
`python3 tools/gates/gate.py check gate-visuals design` (expect a pass).
Touch nothing else in the file. **If `seal` prints any fingerprint other
than the two below, stop and hand back** — it means a drawing changed after
the producer's word on 2026-08-22, and his approval is not to be assumed.

**Why.** Both drawings were approved by the producer in words on
2026-08-22 (*"great diagram, love that… yes its correct"*); the approval
line records that and `seal` locks it. The first `check` is the refusal
firing on a real file before it ever passes — the entry-gates spec's canary
rule.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py check gate-visuals design; echo "exit=$?"; python3 tools/gates/gate.py seal gate-visuals; echo "exit=$?"; python3 tools/gates/gate.py check gate-visuals design; echo "exit=$?"; grep -n 'fp:' docs/product/gate-visuals.md
```

Expected — the first `check` ends with these lines (the `have:` lines
above them are the existing five; the ledger row count is whatever the
doc has):

```
need: docs/product/gate-visuals.md — concern "the life of a gate visual": view docs/design/gate-visuals/visual-lifecycle.html approved by hand, not sealed — no fp
need: docs/product/gate-visuals.md — concern "what the design gate refuses": view docs/design/gate-visuals/design-gate-check.html approved by hand, not sealed — no fp
REFUSED at design — gate-visuals: 2 missing
enters at: slice
exit=1
seal — docs/product/gate-visuals.md
  sealed     the life of a gate visual  docs/design/gate-visuals/visual-lifecycle.html  Tony, 2026-08-22 · fp:3ef85a6441d5
  sealed     what the design gate refuses  docs/design/gate-visuals/design-gate-check.html  Tony, 2026-08-22 · fp:ccbac6efdb93
  2 sealed · 0 refused · 0 already approved · 0 diverged
exit=0
PASS design — gate-visuals: 7 inputs on disk
exit=0
8:    approval: Tony, 2026-08-22 · fp:3ef85a6441d5
12:    approval: Tony, 2026-08-22 · fp:ccbac6efdb93
```

---

### Step 7 — README and the design doc's open question 2

[delegate, model: sonnet, effort: medium]

**What.** Edit `/Users/anthonymaley/Kerd/tools/gates/README.md`:

1. `## Usage`: add, after the `release` line and aligned with it,
   `python3 tools/gates/gate.py seal <slug> [--json]         # complete hand-written view approvals with their fingerprint — exit 0 / 1`.
   Change the sentence *"`check`, `audit`, and `release` are the only three
   subcommands that can exit 1"* to *"`check`, `audit`, `release` and
   `seal` are the only four subcommands that can exit 1"*.
2. `## The gate table`, the `design` row: append
   ` · when the front matter declares `concerns:` (see Views, below): every entry has a view path or `n/a — <reason>` · every view path ends `.html` and resolves on disk · every view carries a sealed approval `<name>, <date> · fp:<12 hex>` whose fingerprint matches the file's current content`.
3. `## Front-matter schema`: change "within 30 lines" to "within 120
   lines" wherever it appears in the README; add a table row
   `| `concerns` | a list — see Views | the agreed concern list. Declaring it opts the design rung into the view count; absent, the rung behaves as before. |`.
4. `## Audit`: add an AU9 entry in the section's existing form, text:
   *"AU9 — every `docs/product/*.md` declaring `concerns:`: the block
   parses and no view is in a wrong state — a render (`.png`) named as the
   view, a path not on disk, an approved drawing whose fingerprint no longer
   matches, an unreadable approval line. Pending approvals (no line, or a
   hand-written line not yet sealed) are the design rung's business and do
   not fail the audit."*
5. New section `## Views — the design gate's lock`, placed after
   `## Rigor level` and before `## Progress view`, carrying: the 42010
   vocabulary in one sentence (concern / viewpoint / view); the D1 grammar
   block verbatim; the D4 row table verbatim; the D2 recipe paragraph and
   its test vector verbatim (`2878c07db022` / `c938aa15c609`); the `seal`
   command, its output lines, and the rule that a divergence is reported
   and never rewritten; the PNG rule (a render is never the view); the
   stated limit — the gate counts that a view exists, is approved and is
   unchanged, never that it was worth drawing.

Edit `/Users/anthonymaley/Kerd/docs/design/gate-visuals.md`, open question
2, replacing its two lines with:

```
2. ~~**Where the agreed aspect list is stored.**~~ **Answered at contract,
   2026-08-22: the product doc's front matter.** `docs/product/<slug>.md`
   carries a `concerns:` list — one entry per view: concern, viewpoint,
   view path or `n/a — <reason>`, approval — read by the design rung of
   `tools/gates/kit.py`; `gate.py seal <slug>` completes a hand-written
   approval with rule 9's fingerprint over the `.html`. Schema and rows:
   `tools/gates/README.md`, Views.
```

Living docs, undated filenames — both files keep their names.

**Why.** The README is the canonical write-down of the schema (its own
rule: "this README, not the dated spec it came from, is now the
standard"); this spec is dated and will not be read again.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 -c "
import sys; sys.path.insert(0,'tools/gates'); import kit
t = open('tools/gates/README.md', encoding='utf-8').read()
d = open('docs/design/gate-visuals.md', encoding='utf-8').read()
print('views section:', '\n## Views — the design gate' in t)
print('usage seal:', 'gate.py seal <slug>' in t, '| 120:', 'within 120 lines' in t, '| 30 gone:', 'within 30 lines' not in t)
print('AU9:', 'AU9' in t, '| vector:', '2878c07db022' in t and 'c938aa15c609' in t, '| concerns row:', '\`concerns\`' in t)
print('design q2 struck:', '~~**Where the agreed aspect list is stored.**~~' in d)
" && python3 tools/gates/gate.py audit
```

Expected: every printed flag `True`, then `audit: clean` (a findings count
in parentheses is fine).

---

### Step 8 — full local suite and the render refresh

[keep]

**What.** Run the nine `gate.yml` commands locally, in its order:
`python3 tools/gates/gate.py selftest`, `gate.py audit`, `gate.py release`,
`python3 tools/diagram/progress.py selftest`, `python3 tools/design/matrix.py selftest`,
`matrix.py audit`, `progress.py stale`, `python3 tools/gates/fidelity.py`.
Then the standing ship ritual before each commit of this build: tick the
piece's box in this spec's `## Pieces`, `python3 tools/diagram/progress.py`
(render refresh — it derives from `docs/plans/*-spec.md` checklists and git
log, so this spec's existence and every ticked box change it), then
`progress.py stale` → `render current`. Commits carry the
`Piece: gate-visuals/<n>` trailer; no `git add -A` — name the files.

**Why.** `stale` is a byte-compare refuser in CI; a pushed tree whose
render was not refreshed after a box was ticked fails the build for a
reason that has nothing to do with this slice. `fidelity.py` reads the
handoff files switch owns — if it names `tools/reqview/fingerprint.py` or
this spec as unreachable, that is the close-out's to fix, not a step here.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest && python3 tools/design/matrix.py selftest && python3 tools/design/matrix.py audit && python3 tools/diagram/progress.py >/dev/null && python3 tools/diagram/progress.py stale && echo ALL-GREEN
```

Expected: `selftest: 41 cases passed`, `audit: clean`, `release: clean`,
the two other selftests passing, `render current`, `ALL-GREEN`, exit 0.
