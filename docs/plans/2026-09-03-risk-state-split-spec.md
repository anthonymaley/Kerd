# Risk state split — the contract spec

Contract for `docs/product/risk-state-split.md` (rigor: `mvp`). Design:
`docs/design/risk-state-split.md` and the three views sealed on the
producer's key, 2026-09-03 — `two-axis-vocabulary` (matrix,
fp:065cb1c38dd7) · `migration-map` (flowchart, fp:aef214c7ae05) ·
`hollow-treatment` (flowchart, fp:c2a0be490625). GO record:
`docs/gates/2026-09-03-risk-state-split-design.md`. The seals' authority is
the work record's concerns block — verify with
`gate.py check risk-state-split design`, never from memory.

**What lands.** The risk ledger's one `State` column becomes two fields —
`Severity` (fatal / non-fatal) and `Treatment` (the four) — `Evidence`
renames to `Risk evidence`, and a new `Treatment evidence` column carries
what proves a treatment in three machine-distinguishable forms (empty ·
`planned — …` · a resolving citation). The checker restructures
(`LEDGER_COLUMNS`, the legal sets, `parse_ledger`, the refusal strings,
plus the acceptance rung's new verified-demand); ALL work records carrying
`## Risk ledger` (21 measured 2026-09-03, re-measured by Step 1) migrate in
the SAME commit as the checker and the fixtures; ~79 severities and 1
ambiguous treatment are keyed by the producer in a generated review
worksheet BEFORE that commit and the keyed worksheet commits WITH it as a
dated record; six selftest fixtures land in the same commit; the prose
surfaces and the release checklist ride.

**The atomic commit is the killer-risk countermeasure.** The work record's
killer row names the half-migrated tree as the risk that disables every
work item at once, and its countermeasure — the producer's rule, verbatim —
is: *checker change, all existing ledger migrations, and tests land
together so no committed tree contains mixed schemas.* This spec makes an
early commit structurally impossible:

- **No step before Step 12 runs `git commit`, `git add`, or `git push` —
  none.** Steps 1–11 change only the working tree. The only git commands
  permitted before Step 12 are read-only (`git rev-parse`, `git status`,
  `git diff`, `git log`, `git grep` — nothing that writes the index or
  the history).
- Step 12 is THE one work commit. It stages an explicit path list (D6) —
  never `git add -A`, never `git add .` — and carries one `Piece:
  risk-state-split/<n>` trailer line per landed piece.
- The ship flow after it: work commit → `python3 tools/diagram/progress.py`
  → render commit (no Piece trailer) → ONE push. Pushing a rung-moving
  commit without its render refresh leaves CI red (measured 2026-08-31).
- Pieces boxes for Steps 1–12 are checked inside Step 12, as part of the
  same staging — the commit carries trailers 1–12, so it checks boxes 1–12;
  a box is never committed ahead of the tree it describes.

**The producer gate.** Step 8 is a HARD PRODUCER GATE: the producer keys
every blank `Key` cell in the review worksheet, in batches by record. Steps
9–14 are DEPENDENT on those keys and say so; nothing below Step 8 states a
post-migration board position as settled fact — every such claim is written
as a branch on what the keys turn out to be. The severity of 79 legacy rows
is his judgment, not this spec's: an old ledger passing without `fatal`
does not prove its severity was non-fatal (the design-gate sharpening,
2026-09-03 — the old cell could not represent fatal-plus-treated, so its
silence is the defect, not a classification).

**Boundaries carried from scope and design, restated so no step drifts:**

- Dated records and session logs NEVER migrate — `docs/gates/`,
  `docs/plans/` (other than the two files this spec itself creates and
  edits), `docs/interrogations/`, `kivna/sessions/` are untouched. Only
  living work records under `docs/product/` migrate. The three dated plans
  that quote the old header (`2026-08-04-risk-ledger-spec.md`,
  `2026-08-22-gate-visuals-spec.md`, `2026-08-25-rung-vocabulary-spec.md`)
  keep it forever.
- No new gates, no new rungs, no new AU rule. `RUNGS` does not change.
- No renderer change beyond what re-derives: `tools/diagram/progress_kit.py`
  changes ONLY its two embedded fixture ledgers (Step 3). The board's new
  truth arrives through the gates kit it already loads by path.
- Deliberately left, named so restraint is visible: the prose mentions of
  "eight-column" / "five legal states" inside
  `docs/product/shared-memory.md` (body prose, rows 222–224 and 401–402 as
  of this writing) and `docs/design/shared-memory.md:79` — body prose of
  other work items, not ledger schema; slainte's judgment layer owns them.
  `CONTEXT.md` and `TODO.md` belong to switch/conductor, not this spec.

**No workflow change.** `.github/workflows/gate.yml` already runs every
check this spec relies on: `gate.py selftest` · `gate.py audit` ·
`gate.py release` · `progress.py selftest` · `matrix.py selftest` ·
`matrix.py audit` · `gen_journey.py check` · `progress.py stale` ·
`fidelity.py`. Nothing in CI changes; CI green on the one push is the live
proof of fixture 3 (fully-migrated tree accepted).

**Reading the Verify lines.** Every command runs from the repo root,
derived per command as `repo_root=$(git rev-parse --show-toplevel)` — never
assumed from the current directory, the home directory, or a worktree's
location; no absolute path appears anywhere in this spec. Where a Verify
asserts a count of ZERO, the count is taken exit-safely — a `grep` inside
`$( )` piped to `wc -l`, or `awk`, feeding `test … -eq 0` — never a bare
`grep -c` in a `&&` chain, which exits 1 at zero matches and aborts the
chain exactly when the check should pass; every such command holds in both
directions, green at zero and red at one. Where a Verify expects
`audit: clean`, `finding:` lines are acceptable — findings never turn the
audit red; a `problem:` line is the failure.

**Step headings are `### Step N — <name>`** because the loop rung's check
binds on `###` and requires a `**Verify:**` line before the next `###`
heading. Lines inside ``` fences are invisible to that parse, so the code
and example blocks below neither split a step nor satisfy one.

**Fixture numbering.** The in-flight requirements-success-measurement spec
reserves T52–T63 on paper (its Step 10 has not landed — the live count is
51). The six fixtures here are **T64–T69**, and the selftest count goes
**51 → 57**. When the requirements spec's fixtures land later they keep
their reserved numbers and lift the count from wherever it then stands.

---

## Decisions the steps depend on

### D1 — the ten-column schema and the legal sets

The exact header, in order (the design's, keyed 2026-09-03):

```
| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
```

- `State` is replaced by `Severity` and `Treatment`.
- `Evidence` renames to `Risk evidence`; its meaning (what sizes the risk)
  is unchanged, and existing cell contents do not change.
- `Treatment evidence` is new: what proves the treatment (D3).

Legal values, after `_normalize_state` normalization (lowercase, em-dash
and `--` to `-`, whitespace collapsed, stripped — unchanged, applied to
both new fields):

- **Severity**: `fatal` (impact >= declared value, at any likelihood — the
  2026-08-03 definition, unchanged) · `non-fatal` (impact < declared
  value). Empty = named, not yet qualified — refused at parse, never a
  legal durable value.
- **Treatment**: `countermeasure - permanent` · `countermeasure -
  temporary` · `accepted` · `accepted unknown`. Empty = named, not yet
  qualified — refused at parse. `fatal` leaves this set: it was never a
  treatment.

Kit constants (Step 2): `LEDGER_COLUMNS` becomes the ten names above;
`LEGAL_STATES` is deleted and replaced by `LEGAL_SEVERITIES = {"fatal",
"non-fatal"}` and `LEGAL_TREATMENTS` = the four treatment values; a new
read-only constant `LEDGER_COLUMNS_PRE_SPLIT` holds the old eight names,
recognized ONLY to name the migration in the header refusal.

### D2 — the refusal strings, verbatim

Parse-level — emitted by `parse_ledger`, so they bind at every gate that
reads the ledger (rungs accumulate their inputs):

- `row N: Risk evidence empty` — the 2026-08-03 empty-evidence check
  carried over under the renamed column (composer decision, flagged at the
  plan gate: the design's refusal list is silent on it and its living doc
  says "Empty evidence = unqualified = cannot pass the gate", so it
  survives the rename rather than silently dying).
- `row N: Severity empty — named, not yet qualified; qualify at viability`
- `row N: Treatment empty — named, not yet qualified; qualify at viability`
- `row N: Severity '<raw>' not a legal value (legal: fatal, non-fatal)`
- `row N: Treatment '<raw>' not a legal value (legal: countermeasure - permanent, countermeasure - temporary, accepted, accepted unknown)`
- `FATAL risk '<risk>' with no countermeasure — record in What we ruled out; cannot pass`
  — fires ONLY on Severity `fatal` + Treatment `accepted` /
  `accepted unknown` / empty. Never on a fatal risk carrying a real
  countermeasure: that combination is what this item exists to make
  representable.
- `row N: Countermeasure empty (required when Treatment is countermeasure)`
- `row N: Review trigger empty (required when Treatment is accepted)`
- `row N: Review trigger empty (required when Severity is fatal and Treatment is countermeasure - temporary — a lapsing protection on a fatal risk must name its return condition)`
- `row N: Treatment evidence empty (required when Severity is fatal) — declare the planned proof ('planned — <what will exist> · <expected location>') or cite the verified one`
- `row N: Treatment evidence is neither 'planned — <what will exist> · <expected location>' nor a resolving citation`

The header refusal, when the found header is exactly the pre-split eight:

- `Risk ledger header row must be exactly: Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger — this record carries the pre-split schema; migrate State to Severity + Treatment`

Any other wrong header gets the same sentence WITHOUT the migration tail.

Acceptance-level — the acceptance rung check's addition and only its, one
string, `<relpath> — ` prefixed like every need row:

- `fatal risk '<risk>': treatment still planned, not verified — acceptance requires resolving Treatment evidence`

### D3 — Treatment evidence: one grammar, three forms, the resolution limit

The cell has exactly three legal states, distinguished by form:

1. **empty** — legal only while Severity is not `fatal` (a non-fatal row's
   cell is optional at every gate, always).
2. **planned** — the exact grammar, one grammar, no editorial variants:
   `planned — <what will exist> · <expected repo-relative location>`.
   Machine contract: the cell is planned-form when its normalized text
   begins `planned -`; well-formed when the RAW cell splits on ` · ` into
   exactly two segments, the second non-empty and not starting with `/`
   (repo-relative). Every placeholder rendering, in every surface, reads
   `planned — <what will exist> · <expected location>`.
3. **verified** — a resolving citation, AU5's family: take the text before
   the first ` — ` (or the whole cell when none); it resolves when it
   glob-matches at least one path under the repo root, or is a 7–40 hex
   commit hash `git cat-file -e` confirms.

A non-empty cell that is neither well-formed planned nor a resolving
citation refuses at parse (the "neither" string). The fatal row's demand is
a LIFECYCLE: planned (or verified) carries viability → loop; the acceptance
rung check demands verified — `planned` there refuses with the
acceptance-level string. The declared limit, the producer's words, kept in
the kit comment: *the machine verifies that a citation resolves; the
producer decides whether it supports the treatment* — retrieval, not
comprehension.

### D4 — the migration boundary and the four streams

The producer's ruling verbatim (scope key): mechanical only where today's
data determines both fields without judgment; every ambiguous value gets
explicit producer review; the migration must not infer to complete the
schema.

Measured 2026-09-03 and re-measured by Step 1: 21 records, 84 rows, old
`State` distribution 78 legal (46 `countermeasure - permanent` · 15
`accepted` · 11 `accepted unknown` · 6 `countermeasure - temporary`) + 4
empty + 1 `fatal` + 1 `accepted (named loss)`.

| Stream | Rule |
|---|---|
| Header | all 21 records rewrite to the D1 header, mechanically |
| Treatment | a legal old `State` cell copies VERBATIM (raw cell text, not normalized) into `Treatment` · the 4 empty-State rows (all in `question-set-staleness.md`) stay empty in BOTH new fields · `gate-reachability.md` row 1 takes `countermeasure - permanent` from the recorded ruling · `hooks-autoload.md` row 3 (`accepted (named loss)`, illegal today) goes to producer review |
| Severity | `gate-reachability.md` row 1 takes `fatal` from the recorded ruling · the 4 empty rows stay empty · EVERY other row (79 by the 2026-09-03 measure) goes to producer review — the migration never infers |
| Treatment evidence | `gate-reachability.md` row 1 carries the planned form transcribed from the 2026-09-02 treatment ruling, byte-exact: `planned — --root fixtures in both directions, per the 2026-09-02 treatment ruling, built in gate-reachability's loop · tools/gates/kit.py` · a fatal-keyed row takes the producer's keyed evidence ruling from the worksheet's second table (a citation lands verbatim; `empty` stays empty and the item refuses honestly — the extension ruling, 2026-09-03) · every other row gets an empty cell |

All other cells (`Risk`, `Killer?`, `Impact`, `Likelihood`, the old
`Evidence` → `Risk evidence`, `Countermeasure`, `Review trigger`) copy
byte-verbatim. Nothing outside the `## Risk ledger` table lines of the 21
records changes.

### D5 — the review worksheet contract

Path: `docs/plans/2026-09-03-risk-state-split-migration-review.md`. It
stays UNCOMMITTED in the working tree until Step 12 commits it with the
migration — the archaeology rule: every reviewed value permanently
traceable to the producer's key, a reviewed value distinguishable from a
stated one.

Shape: a title, a provenance preamble (generated when, from what measure,
key legend), then one `## <record>.md` section per record holding
unresolved values, each with the table:

```
| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
```

One data row per unresolved value: the ledger row number (1-based data-row
index), the field (`Severity` or `Treatment`), and the row's `Risk`,
`Impact` and old-`Evidence` cells quoted verbatim (the design names Impact
and Risk evidence as what severity derives from; the Risk cell rides for
orientation). `Key` is EMPTY at generation. Expected population per the
2026-09-03 measure: 79 `Severity` rows + 1 `Treatment` row
(`hooks-autoload.md` row 3, which therefore appears twice — once per
unresolved field). A different count at generation time is a STOP: the tree
moved since the measure; hand back to the conductor, do not proceed.

Keying legality (checked by Step 8's verify): `Severity` keys normalize to
`fatal` or `non-fatal`; `Treatment` keys normalize to one of the four
legal treatments. No cell may remain empty at the gate's exit.

The extension (the producer's ruling, 2026-09-03): a second table,
`## Treatment evidence review — fatal rows` — Record · Row · the
composer's proposed citation (verified to resolve) or EMPTY-with-reason ·
a blank producer `Key`. Legal keys: `empty`, or the final
Treatment-evidence text whose citation segment resolves against the tree.
Keyed before the gate exits; the worksheet still commits with the
migration, unchanged.

### D6 — the atomic commit: the stage list and the trailers

Step 12 stages EXACTLY these paths, by name (relative to the repo root):

- the 21 migrated records, each named by exact path in Step 12's stage
  command — an explicit manifest, never a directory add: the atomicity
  review cannot protect against unrelated files appearing between review
  and staging
- `tools/gates/kit.py`
- `tools/diagram/progress_kit.py`
- `tools/gates/README.md`
- `skills/interrogate/SKILL.md`
- `docs/design/risk-ledger.md`
- `README.md`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `docs/plans/2026-09-03-risk-state-split-migration-review.md` (the keyed
  worksheet — new file)
- `docs/plans/2026-09-03-risk-state-split-spec.md` (this spec, with boxes
  1–12 checked)

Nothing else. If `git status --porcelain` shows any other modified or
staged path at commit time, STOP and hand back. The commit message carries
one trailer line per landed piece — `Piece: risk-state-split/1` through
`Piece: risk-state-split/12` — plus the session's own standard trailers.

---

## Pieces

- [x] 1. Review worksheet generated — one row per unresolved value, batched by record, Key cells empty, uncommitted
- [x] 2. tools/gates/kit.py — ten-column checker, D2 refusal strings, D3 evidence forms, acceptance verified-demand, embedded fixture ledgers migrated, fixtures T64–T69, selftest 57
- [x] 3. tools/diagram/progress_kit.py — its two fixture ledgers migrated; progress selftest green
- [x] 4. tools/gates/README.md — gate-table rows, normalization block, acceptance row on the new vocabulary
- [x] 5. skills/interrogate/SKILL.md — ledger reference, template, states tables, qualification check, sign-off line, trigger description
- [x] 6. docs/design/risk-ledger.md — columns table and states tables on the new vocabulary
- [x] 7. Release metadata — 0.106.0 in three locations, README What's New entry, README interrogate section
- [x] 8. PRODUCER GATE — every worksheet Key cell keyed by the producer, legal, none blank
- [x] 9. The 21 records migrated from the keyed worksheet — headers, streams, byte-verbatim carry-over
- [x] 10. Full local suite green; board truths hold under the keys as branches, not assumptions
- [x] 11. Diff review — blast radius is exactly the D6 stage list; boundaries held
- [x] 12. THE atomic commit — one commit, twelve trailers, no committed tree with mixed schemas
- [x] 13. Render refresh, render commit, ONE push; CI green — fixture 3's live proof
- [x] 14. Remaining boxes checked, final render current, zero unchecked

---

## Phase A — everything that does not need the producer's keys

No step in this phase runs any git command that writes. The EDITS of
Steps 1–7 are independent of each other and of Step 8; the VERIFIES are
not all so — Step 3's verify runs the renderer's selftest, which loads
`tools/gates/kit.py` from the working tree at runtime, so it depends on
Step 2 being applied first (its own step names the dependency). Step 1
first is deliberate — it lets the producer key batches while Steps 2–7
build.

### Step 1 — generate the review worksheet

[delegate, model: sonnet, effort: medium]

**What.** From the repo root, run exactly this program (heredoc — the spec
is the tool, so the migration's mechanics are themselves a committed
record):

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 - <<'EOF'
import glob, os, re

OLD = ["Risk", "Killer?", "Impact", "Likelihood", "Evidence",
       "State", "Countermeasure", "Review trigger"]
LEGAL = {"countermeasure - permanent", "countermeasure - temporary",
         "accepted", "accepted unknown"}

def norm(s):
    s = s.lower().replace("—", "-").replace("--", "-")
    return re.sub(r"\s+", " ", s).strip()

def rows_of(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"^## Risk ledger[ \t]*$\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    if not m:
        return None
    table = [l for l in m.group(1).splitlines() if l.strip().startswith("|")]
    hdr = [c.strip() for c in table[0].strip().strip("|").split("|")]
    assert hdr == OLD, f"{path}: header is not the pre-split schema"
    out = []
    for i, line in enumerate(table[2:], start=1):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(cells) == 8, f"{path} row {i}: {len(cells)} columns"
        out.append((i, cells))
    return out

entries = {}   # record -> list of (row, field, risk, impact, evidence)
n_rows = n_recs = 0
for p in sorted(glob.glob(os.path.join("docs", "product", "*.md"))):
    rows = rows_of(p)
    if rows is None:
        continue
    rec = os.path.basename(p)
    n_recs += 1
    for i, c in rows:
        n_rows += 1
        st = norm(c[5])
        if rec == "gate-reachability.md" and i == 1:
            continue          # both fields ruled 2026-09-02/03 — mechanical
        if st == "":
            continue          # stays empty in both new fields — mechanical
        entries.setdefault(rec, []).append((i, "Severity", c[0], c[2], c[4]))
        if st not in LEGAL:
            entries.setdefault(rec, []).append((i, "Treatment", c[0], c[2], c[4]))

sev = sum(1 for v in entries.values() for e in v if e[1] == "Severity")
tre = sum(1 for v in entries.values() for e in v if e[1] == "Treatment")
print(f"records={n_recs} rows={n_rows} severity={sev} treatment={tre}")
assert (n_recs, n_rows, sev, tre) == (21, 84, 79, 1), \
    "measure moved since 2026-09-03 — STOP, hand back to the conductor"

out = ["# Risk state split — migration review worksheet", "",
       f"Generated 2026-09-03 by the risk-state-split contract spec, Step 1, "
       f"from the live tree: {n_recs} records, {n_rows} rows; {sev} unrecorded "
       f"severities and {tre} ambiguous treatment for producer review.", "",
       "The producer keys every empty `Key` cell, in batches by record. "
       "Legal keys — Severity: `fatal` | `non-fatal`; Treatment: "
       "`countermeasure - permanent` | `countermeasure - temporary` | "
       "`accepted` | `accepted unknown`. This file commits WITH the "
       "migration (the archaeology rule: a reviewed value stays "
       "distinguishable from a stated one, forever).", ""]
for rec in sorted(entries):
    out += [f"## {rec}", "",
            "| Row | Field | Risk | Impact | Risk evidence | Key |",
            "|---|---|---|---|---|---|"]
    for i, field, risk, impact, ev in entries[rec]:
        out.append(f"| {i} | {field} | {risk} | {impact} | {ev} |  |")
    out.append("")
open(os.path.join("docs", "plans",
     "2026-09-03-risk-state-split-migration-review.md"),
     "w", encoding="utf-8").write("\n".join(out) + "\n")
print("worksheet written")
EOF
```

**Why.** The design's review worksheet (D5): the migration must not infer,
so every value judgment is extracted into one keyable artifact before any
record changes. The program's own asserts are the re-measure the scope
demands; a moved tree stops the step instead of silently proceeding. Do
NOT commit the file.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && ws=docs/plans/2026-09-03-risk-state-split-migration-review.md && test -f "$ws" && test "$(grep -c '^| [0-9]* | Severity |' "$ws")" -eq 79 && test "$(grep -c '^| [0-9]* | Treatment |' "$ws")" -eq 1 && test "$(grep -E '^\| [0-9]+ \|' "$ws" | grep -vc '|  |$' | awk '{print}')" -eq 0 && test "$(git status --porcelain "$ws" | grep -c '^??')" -eq 1
```

Expected: 79 Severity rows, exactly 1 Treatment row
(`hooks-autoload.md`, ledger row 3), every data row ending with an empty
`Key` cell (the zero-count is exit-safe: `grep -vc` inside `$( )`), and the
file untracked — generated, not committed.

### Step 2 — kit.py: the ten-column checker, the six fixtures, selftest 57

[delegate, model: sonnet, effort: high]

**What.** Every change to `tools/gates/kit.py`, in one pass. The file's
regions named below are located by content, not by line number — the line
references (from the 2026-09-03 read) are orientation only.

**2a — imports and constants** (top of file, near `LEDGER_COLUMNS` ~:61):
add `import subprocess` to the imports; replace `LEDGER_COLUMNS` and delete
`LEGAL_STATES`, installing the D1 constants:

```python
LEDGER_COLUMNS = [
    "Risk", "Killer?", "Impact", "Likelihood", "Risk evidence",
    "Severity", "Treatment", "Countermeasure", "Treatment evidence",
    "Review trigger",
]
# The pre-split eight-column schema (retired 2026-09-03, risk-state-split).
# Read-only, forever: recognized ONLY so the header refusal can name the
# migration instead of leaving the reader to diff two headers by eye.
LEDGER_COLUMNS_PRE_SPLIT = [
    "Risk", "Killer?", "Impact", "Likelihood", "Evidence",
    "State", "Countermeasure", "Review trigger",
]
# Severity: set by impact alone, against the declared value (A3, unchanged
# definition of fatal). Empty is workflow incompleteness, refused at parse —
# never a legal durable value (the producer's ruling, 2026-09-03).
LEGAL_SEVERITIES = {"fatal", "non-fatal"}
# Treatment: today's four, unchanged. `fatal` leaves the set — it was never
# a treatment. Empty refused at parse, same ground as Severity.
LEGAL_TREATMENTS = {
    "countermeasure - permanent",
    "countermeasure - temporary",
    "accepted",
    "accepted unknown",
}
```

**2b — the evidence-form helper** (beside `_normalize_state`, ~:423): add
D3's classifier. The docstring carries the producer's declared limit
verbatim.

```python
def _treatment_evidence_form(root, cell):
    """Classify a Treatment evidence cell: 'empty' | 'planned' |
    'planned-malformed' | 'verified' | 'unresolved'.

    planned: normalized text begins 'planned -'; well-formed when the RAW
    cell splits on ' · ' into exactly two segments, the second non-empty
    and repo-relative (no leading '/'). verified: a resolving citation,
    AU5's family — the text before the first ' — ' (or the whole cell)
    glob-resolves under root, or is a 7-40 hex commit hash git confirms.
    The declared limit, the producer's words: the machine verifies that a
    citation resolves; the producer decides whether it supports the
    treatment. Retrieval, not comprehension."""
    raw = cell.strip()
    if not raw:
        return "empty"
    if _normalize_state(raw).startswith("planned -"):
        segs = raw.split(" · ")
        if len(segs) == 2 and segs[1].strip() and not segs[1].strip().startswith("/"):
            return "planned"
        return "planned-malformed"
    ref = raw.split(" — ", 1)[0].strip()
    if re.fullmatch(r"[0-9a-f]{7,40}", ref):
        try:
            ok = subprocess.run(
                ["git", "-C", root, "cat-file", "-e", ref],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            ).returncode == 0
        except OSError:
            ok = False
        return "verified" if ok else "unresolved"
    if glob.glob(os.path.join(root, ref)):
        return "verified"
    return "unresolved"
```

**2c — `parse_ledger`** (~:441): the signature becomes
`parse_ledger(section_text, root)` (root now required — the citation check
resolves against the filesystem). Update the docstring to the new schema
and D2's refusal inventory. The header check appends the migration tail
exactly when the found header is the pre-split schema:

```python
    header_cells = _split_row(lines[0])
    if header_cells != LEDGER_COLUMNS:
        msg = "Risk ledger header row must be exactly: " + " | ".join(LEDGER_COLUMNS)
        if header_cells == LEDGER_COLUMNS_PRE_SPLIT:
            msg += (" — this record carries the pre-split schema; "
                    "migrate State to Severity + Treatment")
        problems.append(msg)
        return rows, problems
```

The per-row block replaces the old Evidence/State/Countermeasure/Review
checks with, in this order (strings byte-exact per D2):

```python
        if not row["Risk evidence"]:
            problems.append(f"row {i}: Risk evidence empty")

        sev = _normalize_state(row["Severity"])
        tre = _normalize_state(row["Treatment"])
        if sev == "":
            problems.append(f"row {i}: Severity empty — named, not yet qualified; qualify at viability")
        elif sev not in LEGAL_SEVERITIES:
            problems.append(f"row {i}: Severity '{row['Severity']}' not a legal value (legal: fatal, non-fatal)")
        if tre == "":
            problems.append(f"row {i}: Treatment empty — named, not yet qualified; qualify at viability")
        elif tre not in LEGAL_TREATMENTS:
            problems.append(
                f"row {i}: Treatment '{row['Treatment']}' not a legal value "
                "(legal: countermeasure - permanent, countermeasure - temporary, accepted, accepted unknown)"
            )
        # The FATAL refusal narrows twice (risk-state-split): it fires only
        # on fatal + accepted / accepted unknown / empty treatment — never
        # on a fatal risk carrying a real countermeasure, which is the
        # combination this item exists to make representable.
        if sev == "fatal" and tre in ("", "accepted", "accepted unknown"):
            problems.append(
                f"FATAL risk '{row['Risk']}' with no countermeasure — record in What we ruled out; cannot pass"
            )
        if tre.startswith("countermeasure") and not row["Countermeasure"]:
            problems.append(f"row {i}: Countermeasure empty (required when Treatment is countermeasure)")
        if tre.startswith("accepted") and not row["Review trigger"]:
            problems.append(f"row {i}: Review trigger empty (required when Treatment is accepted)")
        if sev == "fatal" and tre == "countermeasure - temporary" and not row["Review trigger"]:
            problems.append(
                f"row {i}: Review trigger empty (required when Severity is fatal and Treatment is "
                "countermeasure - temporary — a lapsing protection on a fatal risk must name its return condition)"
            )
        form = _treatment_evidence_form(root, row["Treatment evidence"])
        if sev == "fatal" and form == "empty":
            problems.append(
                f"row {i}: Treatment evidence empty (required when Severity is fatal) — declare the "
                "planned proof ('planned — <what will exist> · <expected location>') or cite the verified one"
            )
        if form in ("planned-malformed", "unresolved"):
            problems.append(
                f"row {i}: Treatment evidence is neither "
                "'planned — <what will exist> · <expected location>' nor a resolving citation"
            )
```

**2d — call sites**: both existing `parse_ledger(ledger_body)` calls inside
`check_rung` (the viability killer-floor parse and the scope qualification
parse) become `parse_ledger(ledger_body, root)`. There are exactly two;
verify with a search before editing.

**2e — the acceptance verified-demand** (inside `check_rung`'s
`idx >= RUNGS.index("acceptance")` block, after the unchecked-boxes
handling): the acceptance rung — and only it — demands a fatal row's
evidence resolve:

```python
        # The verified-demand (risk-state-split): a fatal row advances the
        # pre-acceptance rungs on a *planned* treatment — requiring proof
        # earlier would block the item that must build it (the circular
        # dependency the producer refused). Acceptance is where the
        # citation must resolve; the producer's key judges whether the
        # resolved evidence proves anything.
        if product_exists and product_text is not None:
            a_body = find_section(product_text, "Risk ledger")
            if a_body:
                a_rows, _ = parse_ledger(a_body, root)
                for a_row in a_rows:
                    if _normalize_state(a_row["Severity"]) != "fatal":
                        continue
                    if _treatment_evidence_form(root, a_row["Treatment evidence"]) == "verified":
                        have.append(
                            f"{rel_product} — fatal risk '{a_row['Risk']}': Treatment evidence resolves (verified)"
                        )
                    else:
                        need.append(
                            f"{rel_product} — fatal risk '{a_row['Risk']}': treatment still planned, "
                            "not verified — acceptance requires resolving Treatment evidence"
                        )
```

**2f — the embedded fixture ledgers migrate** (the atomic rule applies to
fixtures too). Replace the ledger literals in `_selftest_body` with these,
byte-exact — each preserves its case's intent (T4/T50/T51: named-only
killer floor; T5: empty Risk evidence in row 2; T6: fatal, untreated; T7+:
fully qualified):

`ledger_named_only` data rows:

```python
            "| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| No adoption | yes | high | medium |  |  | accepted unknown |  |  |  |\n"
```

`ledger_bad_evidence` data rows (same new header and separator as above):

```python
            "| Adoption risk | yes | high | medium | 3 interviews | non-fatal | accepted |  |  | check Q2 |\n"
            "| Perf risk | no | medium | low |  | non-fatal | accepted unknown |  |  | monitor |\n"
```

`ledger_fatal` data row (new header): `| No market | yes | high | high | 0
signups in beta | fatal |  |  |  |  |` — Severity fatal, everything after
empty; T6's assertions (the FATAL string, the risk name) hold because
fatal + empty treatment still fires the FATAL refusal.

`ledger_good` data rows (new header):

```python
            "| Adoption risk | yes | high | medium | 3 interviews | non-fatal | accepted |  |  | check Q2 |\n"
            "| Perf risk | no | medium | low | benchmark done | non-fatal | countermeasure - permanent | caching added |  |  |\n"
```

The `BODY` constant (the concerns-tests scaffold, ~:2331) and the T44
`beta.md` fixture (~:2617) each carry the single row
`| Adoption risk | yes | high | medium | 3 interviews | non-fatal | accepted |  |  | check Q2 |`
under the new header and ten-dash separator.

**2g — the six fixtures, T64–T69**, appended inside `_selftest_body` after
the T51 block (before the trailing T45 purity block). Each in its own
temporary tree; `slug = "alpha"` is already in scope. The producer's five,
plus the design's added sixth:

```python
    # T64 — fixture 1 (risk-state-split): an old-only record refuses with
    # the migration named in the message.
    with tempfile.TemporaryDirectory() as root_t64:
        old_ledger = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| Adoption risk | yes | high | medium | 3 interviews | accepted | | check Q2 |\n"
        )
        _sw(os.path.join(root_t64, "docs", "product", f"{slug}.md"), old_ledger)
        cr = check_rung(root_t64, slug, "scope")
        assert any("pre-split schema; migrate State to Severity + Treatment" in n for n in cr["need"]), \
            f"T64: expected the migration-naming refusal, got {cr['need']}"

    # T65 — fixture 2: a mixed tree refuses the unmigrated record and the
    # route degrades loudly — it does not crash, and the migrated record
    # is untouched by its neighbour's schema.
    with tempfile.TemporaryDirectory() as root_t65:
        new_ledger = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| Adoption risk | yes | high | medium | 3 interviews | non-fatal | accepted |  |  | check Q2 |\n"
            "\n## Scope\n\nRigor level: mvp\n\nShip it.\n"
        )
        old_ledger = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nWorth it.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| Perf risk | yes | high | low | benchmark | accepted | | monitor |\n"
        )
        _sw(os.path.join(root_t65, "docs", "product", "alpha.md"), new_ledger)
        _sw(os.path.join(root_t65, "docs", "product", "beta.md"), old_ledger)
        r_new = route(root_t65, "alpha")
        r_old = route(root_t65, "beta")   # must not raise
        assert r_new["enters_at"] == "design", f"T65: migrated record held back: {r_new['enters_at']!r}"
        assert r_old["enters_at"] == "frame", f"T65: expected loud degradation to frame, got {r_old['enters_at']!r}"
        cr = check_rung(root_t65, "beta", "scope")
        assert any("pre-split schema" in n for n in cr["need"]), f"T65: {cr['need']}"

    # T66 — fixture 3: a fully migrated tree is accepted — rows parse,
    # zero ledger problems, the scope have-line counts them qualified.
    with tempfile.TemporaryDirectory() as root_t66:
        _sw(os.path.join(root_t66, "docs", "product", f"{slug}.md"), new_ledger)
        cr = check_rung(root_t66, slug, "scope")
        assert f'docs/product/{slug}.md — section "Risk ledger" (1 rows, all qualified)' in cr["have"], \
            f"T66: expected the all-qualified have row, got {cr['have']}"

    # T67/T68 — fixtures 4 and 5: fatal + permanent + planned passes the
    # viability/scope parse (the combination this item exists to make
    # representable); the SAME row still planned at the acceptance check
    # refuses (T68); with a resolving citation it passes (T67's second
    # half). One tree, the cell swapped between assertions.
    with tempfile.TemporaryDirectory() as root_t67:
        planned_cell = "planned — --root fixtures in both directions · tools/gates/kit.py"
        fatal_treated = (
            "---\nroute: new\nstage: framed\n---\n\n"
            "## Value\n\nSaves 10 hours/week.\n\n"
            "## Risk ledger\n\n"
            "| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            f"| Wrong repo | yes | a gate that lies | medium | measured 2026-09-02 | fatal | countermeasure - permanent | --root everywhere | {planned_cell} | re-qualify when seal is wired |\n"
            "\n## Scope\n\nRigor level: mvp\n\nShip it.\n"
        )
        p67 = os.path.join(root_t67, "docs", "product", f"{slug}.md")
        _sw(p67, fatal_treated)
        cr = check_rung(root_t67, slug, "scope")
        assert not any("FATAL" in n for n in cr["need"]), \
            f"T67: fatal+permanent must not fire the FATAL refusal, got {cr['need']}"
        assert f'docs/product/{slug}.md — section "Risk ledger" (1 rows, all qualified)' in cr["have"], \
            f"T67: expected the planned row to parse qualified, got {cr['have']}"

        # the full tree, so only the acceptance-level demand separates the
        # two forms:
        _sw(os.path.join(root_t67, "docs", "design", f"{slug}.md"), "# Alpha design\n\nHow.\n")
        _sw(os.path.join(root_t67, "docs", "gates", "2026-01-01-alpha-design.md"),
            "---\nroute: new\nstage: designed\n---\n\n## GO\n\nApproved.\n")
        _sw(os.path.join(root_t67, "docs", "plans", "2026-01-02-alpha-spec.md"),
            "# Alpha — build spec\n\n## Pieces\n\n- [x] Step 1\n\n"
            "### Step 1: do the thing\n**What:** do it.\n**Verify:** `true`\n")
        cr = check_rung(root_t67, slug, "acceptance")
        assert any("treatment still planned, not verified" in n for n in cr["need"]), \
            f"T68: still-planned at acceptance must refuse, got {cr['need']}"

        _sw(p67, fatal_treated.replace(planned_cell, "docs/product/alpha.md"))
        cr = check_rung(root_t67, slug, "acceptance")
        assert not any("treatment still planned" in n for n in cr["need"]), \
            f"T67: a resolving citation must pass the acceptance check, got {cr['need']}"
        assert any("Treatment evidence resolves (verified)" in h for h in cr["have"]), \
            f"T67: expected the verified have row, got {cr['have']}"

    # T69 — fixture 6 (the design's added case): fatal + temporary with an
    # empty Review trigger refuses with the lapsing-protection string; the
    # same row with its return condition named passes.
    with tempfile.TemporaryDirectory() as root_t69:
        def t69_doc(trigger):
            return (
                "---\nroute: new\nstage: framed\n---\n\n"
                "## Value\n\nSaves 10 hours/week.\n\n"
                "## Risk ledger\n\n"
                "| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |\n"
                "|---|---|---|---|---|---|---|---|---|---|\n"
                f"| Silent regression | yes | a false green | high | measured | fatal | countermeasure - temporary | fixture blocks it | planned — the fixture · tools/gates/kit.py | {trigger} |\n"
            )
        p69 = os.path.join(root_t69, "docs", "product", f"{slug}.md")
        _sw(p69, t69_doc(""))
        _, probs = parse_ledger(find_section(open(p69, encoding="utf-8").read(), "Risk ledger"), root_t69)
        assert any("a lapsing protection on a fatal risk must name its return condition" in p for p in probs), \
            f"T69: expected the fatal+temporary trigger refusal, got {probs}"
        _sw(p69, t69_doc("fires if the fixture is removed"))
        _, probs = parse_ledger(find_section(open(p69, encoding="utf-8").read(), "Risk ledger"), root_t69)
        assert probs == [], f"T69: named return condition must pass, got {probs}"
```

**2h — counts and docstrings**: `selftest()`'s docstring and printed line
go 51 → 57 (both occurrences of the number). Update the module-level A3
comment above `_normalize_state` (it now normalizes both new fields) and
`parse_ledger`'s docstring to the D2 inventory. No other function changes —
`RUNGS`, `STAGES`, the register machinery, concerns, AU rules all stay
byte-identical.

**2i — T5's assertion follows the rename**: the pre-existing second
assertion in the T5 block checks the capitalized substring `"Evidence"`,
which no longer appears in the D2 string (`row 2: Risk evidence empty`
carries a lowercase e), so it fails against the very refusal 2c installs.
The line

```python
        assert any("Evidence" in n for n in cr["need"]), f"T5: expected 'Evidence' in need: {cr['need']}"
```

becomes, byte-exact — asserting the full refusal string, which cannot
drift on case:

```python
        assert any("row 2: Risk evidence empty" in n for n in cr["need"]), \
            f"T5: expected the Risk-evidence-empty refusal: {cr['need']}"
```

The first T5 assertion (`"row 2"`) stands unchanged.

**Why.** The checker half of the atomic pair, with the fixtures that prove
the refusal in both directions living in the same file — so Step 12's one
commit carries the demand and its proof together. The old fixtures migrate
because the atomic rule has no fixture exemption: a committed tree with an
old-schema fixture is a committed tree asserting the old schema still
parses.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('k', 'tools/gates/kit.py')
k = importlib.util.module_from_spec(spec); spec.loader.exec_module(k)
assert len(k.LEDGER_COLUMNS) == 10 and k.LEDGER_COLUMNS[4] == 'Risk evidence'
assert not hasattr(k, 'LEGAL_STATES')
assert k.LEGAL_SEVERITIES == {'fatal', 'non-fatal'} and len(k.LEGAL_TREATMENTS) == 4
assert k.RUNGS == ['frame', 'viability', 'scope', 'design', 'handoff', 'loop', 'acceptance']
print('constants ok')" && test "$(grep -c 'parse_ledger(ledger_body, root)' tools/gates/kit.py)" -ge 2
```

Expected: `selftest: 57 cases passed`; the constants probe prints
`constants ok` (ten columns, `LEGAL_STATES` gone, the ladder untouched);
both rung-check call sites pass `root`.

### Step 3 — progress_kit.py: the two fixture ledgers re-derive

[delegate, model: sonnet, effort: low]

**What.** In `tools/diagram/progress_kit.py`, exactly two edits — the
renderer changes nothing else (it loads the gates kit by path, so the new
truth arrives on its own):

1. `_F8_PRODUCT` (~:903): the ledger becomes the new header, ten-dash
   separator, and the named-but-unqualified row
   `| Adoption risk | yes | high | medium |  |  | accepted |  |  |  |`
   — its docstring's intent holds: the killer-presence check passes on the
   named row, scope's full qualification does not.
2. `_f15`'s `ledger_good` (~:1037): the new header, ten-dash separator, and
   the two fully-qualified rows exactly as Step 2f's `ledger_good` — so the
   full tree still derives `ready-to-release` (no fatal row, so the new
   acceptance demand stays vacuous).

**Why.** These two literals are the only old-schema text in the renderer;
after Step 2 they would refuse under the kit the renderer itself loads.
Migrating them IS "what re-derives" — anything more is out of bounds.

**Depends on:** Step 2 applied to the working tree — the verify's selftest
loads the gates kit by path at runtime, and with the old checker still
present the migrated fixture ledgers cannot parse (measured: ok 8 fails
with `expected enters_at viability, got 'frame'`). The edits above may land
in any order; this verify may not run before Step 2's.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/diagram/progress.py selftest && test "$(grep -c 'Risk evidence | Severity | Treatment' tools/diagram/progress_kit.py)" -eq 2 && test "$(grep -n '| Evidence | State |' tools/diagram/progress_kit.py | wc -l)" -eq 0
```

Expected: the progress selftest green; two new-header literals; zero
old-header literals (the zero-count exit-safe via `wc -l`).

### Step 4 — tools/gates/README.md: the contract prose

[delegate, model: sonnet, effort: medium]

**What.** Four regions of `tools/gates/README.md`, located by their current
text:

1. **The gate table, `viability` row** — the sentence "A FATAL row, an
   illegal `State`, or empty `Evidence` do not refuse here — full
   qualification is the `scope` rung's business." becomes: "An untreated
   fatal row, an illegal `Severity` or `Treatment`, or an empty
   `Risk evidence` cell do not refuse here — full qualification is the
   `scope` rung's business."
2. **The gate table, `scope` row** — the header spelling and the per-row
   rules rewrite to: a pipe table whose header row is exactly
   `Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger`
   (with the `\|` escapes the row already uses), ≥1 data row, and per row:
   `Risk evidence` non-empty · `Severity` one of `fatal`/`non-fatal` ·
   `Treatment` one of the four · `Countermeasure` non-empty when
   `Treatment` begins `countermeasure` · `Review trigger` non-empty when
   `Treatment` begins `accepted`, and also when `Severity` is `fatal` with
   `Treatment` `countermeasure - temporary` · `Treatment evidence`
   non-empty when `Severity` is `fatal`, and when non-empty either the
   planned form `planned — <what will exist> · <expected location>` or a
   resolving citation · no fatal row whose `Treatment` is `accepted`,
   `accepted unknown` or empty. The trailing `section Scope` and
   `Rigor level` clauses stay as they are.
3. **The gate table, `acceptance` row** — after "zero unchecked boxes …
   evidence ready for producer review." add: "Plus the verified-demand:
   every fatal-severity ledger row's `Treatment evidence` must be a
   resolving citation — a `planned — …` declaration refuses here (still
   planned, not verified), though it carries every earlier rung."
4. **The normalization block** (currently "Risk-ledger `State` cells are
   normalized …" through the FATAL-refusal sentence) — rewrite to: both
   `Severity` and `Treatment` cells normalize the same way (lowercase,
   em-dash and `--` collapsed to `-`, whitespace collapsed, stripped);
   legal `Severity` values `fatal`, `non-fatal`; legal `Treatment` values
   the four; empty cells in either are refused as named-not-yet-qualified;
   the FATAL refusal fires only on `fatal` + `accepted` /
   `accepted unknown` / empty treatment, verbatim string
   `FATAL risk '<risk>' with no countermeasure — record in What we ruled
   out; cannot pass`; a pre-split eight-column header is refused with the
   migration named in the message; and the `Treatment evidence` lifecycle
   in one sentence — planned (`planned — <what will exist> · <expected
   location>`) carries viability through loop, acceptance demands a
   resolving citation, and the machine verifies that a citation resolves
   while the producer decides whether it supports the treatment.

**Why.** The README is the declared contract the checker enforces; item 5
of the release checklist and the scope key both name these rows as the
prose surface that sweeps with the change.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -q 'Severity' tools/gates/README.md && grep -qF 'planned — <what will exist> · <expected location>' tools/gates/README.md && grep -qF "FATAL risk '<risk>' with no countermeasure" tools/gates/README.md && test "$(grep -cF 'Evidence \| State' tools/gates/README.md || true)" -eq 0 && test "$(grep -n 'five legal normalized values' tools/gates/README.md | wc -l)" -eq 0
```

Expected: the new vocabulary present with the exact planned-form
placeholder and narrowed FATAL string; the old escaped header spelling and
the five-value sentence both at zero (exit-safe counts).

### Step 5 — skills/interrogate/SKILL.md: the skill surface and its trigger

[delegate, model: sonnet, effort: medium]

**What.** Every schema-bearing spot in `skills/interrogate/SKILL.md`, an
enumerated sweep — nothing else in the file changes:

1. **Frontmatter `description`** (the trigger — release checklist item 4):
   the phrase "sized, evidenced, and left in exactly one state" becomes
   "sized, evidenced, with Severity and Treatment each stated". The rest of
   the description stands.
2. **The opening paragraph**: the same phrase, the same replacement.
3. **Tiering, the Everyday paragraph**: "same eight columns, same five
   states" becomes "same ten columns, same Severity and Treatment
   vocabulary"; "FATAL discipline" stays.
4. **Done gate 6(a), the row-qualification bullet**: "**State** exactly one
   of the five · **Countermeasure** named … when State begins
   *Countermeasure* … **Review trigger** non-empty when State begins
   *Accepted*" becomes "**Severity** `fatal` or `non-fatal` ·
   **Treatment** exactly one of the four · **Countermeasure** named with a
   confidence statement when Treatment begins *Countermeasure* (plus a
   return condition when TEMPORARY) · **Treatment evidence** for a fatal
   row: the planned form `planned — <what will exist> · <expected
   location>` or a resolving citation — never empty · **Review trigger**
   non-empty when Treatment begins *Accepted*, and when Severity is fatal
   with a temporary countermeasure".
5. **Done gate 6(a), the FATAL bullet**: "no row in **FATAL** — a FATAL row
   blocks recitation" becomes "no fatal-severity row whose Treatment is
   accepted, accepted unknown, or empty — an untreated fatal row blocks
   recitation"; the kill-or-reshape consequence sentence stays.
6. **The Ledger columns table**: `Evidence` row renames to
   `Risk evidence` (rule text unchanged); `State` row becomes two rows —
   `Severity` ("`fatal` or `non-fatal` — set by impact against the
   declared value, at any likelihood") and `Treatment` ("exactly one of
   the four below"); after `Countermeasure` add a `Treatment evidence` row
   ("what proves the treatment — empty only at non-fatal; `planned — <what
   will exist> · <expected location>` before the proof exists; a resolving
   citation once it does").
7. **The exact-header block** (the fenced one "downstream mechanical
   checks match it byte-for-byte") becomes the D1 ten-column header.
8. **"The five states" table** becomes two tables: **Severity** (`fatal`:
   impact ≥ the declared value, at ANY likelihood; `non-fatal`: impact
   below it) and **Treatment** (the four rows, meanings carried over from
   today's table; FATAL's row leaves — it was never a treatment).
9. **The rules bullets**: "FATAL is set by impact alone" stays (it defines
   Severity now); "It cannot be accepted by name" gains the precision "a
   fatal-severity risk cannot carry Treatment accepted or accepted
   unknown"; add one bullet: "A treatment is not proven merely because its
   field is populated — `planned — …` is the honest declaration, and only
   a resolving citation is called verified (demanded at acceptance)."
10. **Document Structure → Risk ledger**: "The eight-column table" becomes
    "The ten-column table".
11. **The canonical template**: the ledger header and placeholder row take
    the ten-column shape (placeholder cells `<fatal/non-fatal>`,
    `<one of the four treatments>`, `<empty · planned — … · citation>`).
12. **Recitation, step 2**: "Impact, Likelihood, State, and the
    countermeasure or acceptance gist" becomes "Impact, Likelihood,
    Severity, Treatment, and the countermeasure or acceptance gist".
13. **Sign-off ritual step 5 and the paragraph after it**: `FATAL rows: 0`
    becomes `untreated fatal rows: 0` in both places.

**Why.** The skill is the human-facing statement of the same contract the
checker enforces; a skill change, so the trigger description is checked
against the new vocabulary (item 4 of the release checklist) — the trigger
changes because "exactly one state" no longer describes the artifact.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -q 'with Severity and Treatment each stated' skills/interrogate/SKILL.md && grep -qF '| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |' skills/interrogate/SKILL.md && grep -q 'untreated fatal rows: 0' skills/interrogate/SKILL.md && test "$(grep -n 'left in exactly one state' skills/interrogate/SKILL.md | wc -l)" -eq 0 && test "$(grep -nF '| Likelihood | Evidence | State |' skills/interrogate/SKILL.md | wc -l)" -eq 0 && test "$(grep -c 'five states' skills/interrogate/SKILL.md || true)" -eq 0
```

Expected: new trigger phrase, the ten-column header verbatim, the renamed
sign-off line; zero hits for the old phrase, the old header fragment, and
"five states" — all zero-counts taken exit-safely.

### Step 6 — docs/design/risk-ledger.md: the living ledger doc

[delegate, model: haiku, effort: low]

**What.** `docs/design/risk-ledger.md` is the ledger's own living design
doc and still teaches the pre-split schema; a living doc describing a
retired schema is drift the moment Step 12 lands. Composer addition to the
named prose surfaces, raised at the plan gate — remove this step if the
producer rules it out. Three edits:

1. The columns table: `Evidence` → `Risk evidence` (rule unchanged);
   `State` row → `Severity` ("`fatal` or `non-fatal` — set by impact
   alone") and `Treatment` ("exactly one of the four below") rows; add
   `Treatment evidence` row ("what proves the treatment — `planned — <what
   will exist> · <expected location>` until the proof exists, a resolving
   citation once it does; required at fatal, optional at non-fatal").
2. "## The five states" → "## Severity and Treatment", the same two tables
   as Step 5 item 8.
3. The rules bullets: keep all five, tighten the third to "high impact +
   high likelihood + no countermeasure = dead project. A fatal-severity
   risk cannot carry an accepted treatment — it cannot be accepted by
   name."; add "A treatment is not proven merely because its field is
   populated: acceptance demands the citation resolve."

**Why.** Undated files in `docs/design/` are living by CI-enforced
convention; leaving this one on the old vocabulary contradicts the checker
in the same tree.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && grep -q 'Severity and Treatment' docs/design/risk-ledger.md && grep -q 'Risk evidence' docs/design/risk-ledger.md && test "$(grep -n 'The five states' docs/design/risk-ledger.md | wc -l)" -eq 0
```

Expected: the new section heading and column name present; the old heading
at zero, exit-safe.

### Step 7 — release metadata: 0.106.0 and the README story

[delegate, model: haiku, effort: low]

**What.** The release checklist's mechanical items, MINOR bump (changed
behavior — new schema, new refusals):

1. `.claude-plugin/plugin.json` → `version`: `0.105.0` → `0.106.0`.
2. `.claude-plugin/marketplace.json` → `metadata.version` AND
   `plugins[0].version`: both `0.105.0` → `0.106.0`.
3. The two capability-list descriptions are NOT touched — checked, not
   assumed: "risk qualification" still names this capability accurately,
   and the byte-identical rule makes an unnecessary edit a two-file edit.
4. `README.md`: the heading `## What's New (v0.105.0)` becomes
   `## What's New (v0.106.0)`, and this entry lands directly under it,
   above `### v0.105.0`:

   > ### v0.106.0
   >
   > **A risk's severity and its treatment are two facts, not one field.**
   > The ledger's one `State` column mixed how bad with what we are doing
   > about it, so a risk that was genuinely fatal and genuinely treated
   > could not be stated truthfully — whichever value the cell carried lied
   > about the other fact. Now a row carries `Severity` (fatal /
   > non-fatal) and `Treatment` (the four), `Evidence` renames to
   > `Risk evidence`, and a new `Treatment evidence` column holds what
   > proves the treatment: the honest `planned — <what will exist> ·
   > <expected location>` declaration before the proof can exist, a
   > resolving citation once it does. A fatal risk advances from viability
   > on a planned treatment; acceptance is where the citation must
   > resolve. All 21 work records migrated in the same commit as the
   > checker and its fixtures — no committed tree ever held mixed schemas
   > — and every severity the old vocabulary never recorded was keyed by
   > hand in a review worksheet committed with the migration, so a
   > reviewed value stays distinguishable from a stated one. **What it
   > means:** a fatal, treated risk no longer forces the ledger to lie,
   > and a treatment is never called proven merely because its field is
   > populated. **The limit, stated:** the machine verifies that a
   > citation resolves; the producer decides whether it supports the
   > treatment.

5. `README.md`, the interrogate section: "until every one is sized,
   evidenced, and left in exactly one state" → "until every one is sized,
   evidenced, with Severity and Treatment each stated"; the sentence
   "eight columns (Risk / Killer? / Impact / Likelihood / Evidence / State
   / Countermeasure / Review trigger), five states (…), killer assumption
   first, always." → "ten columns (Risk / Killer? / Impact / Likelihood /
   Risk evidence / Severity / Treatment / Countermeasure / Treatment
   evidence / Review trigger), Severity fatal or non-fatal, Treatment one
   of four with its evidence carried from `planned — …` to a resolving
   citation, killer assumption first, always."; and in the following
   paragraph "FATAL means impact ≥ that value" → "fatal severity means
   impact ≥ that value".

**Why.** Items 1–3 of the release checklist, before the commit — CI's
`gate.py release` refuses drift in exactly these fields.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py release && test "$(grep -c '"version": "0.106.0"' .claude-plugin/plugin.json)" -eq 1 && test "$(grep -c '"version": "0.106.0"' .claude-plugin/marketplace.json)" -eq 2 && grep -q '## What'"'"'s New (v0.106.0)' README.md && grep -q '### v0.106.0' README.md && grep -q 'with Severity and Treatment each stated' README.md
```

Expected: release rules clean (version sync across all three, capability
lists untouched and identical); the heading, the entry, and the interrogate
rewrite present.

---

## Phase B — the gate

### Step 8 — PRODUCER GATE: the severity and treatment keys

[keep]

**What.** HARD STOP. The producer opens
`docs/plans/2026-09-03-risk-state-split-migration-review.md` and keys every
empty `Key` cell, in batches by record, at his pace — 79 severities and 1
treatment per the Step 1 measure. His keys are the judgment the migration
is forbidden to infer: for each legacy row, `fatal` or `non-fatal` against
the record's declared value; for `hooks-autoload.md` row 3, which of the
four treatments `accepted (named loss)` actually meant. A row whose own
cells state the classification in the ledger's terms may be keyed straight
from them — his key is still what lands. The worksheet stays uncommitted.

**What this gate unlocks — nothing below runs before it exits:** Step 9
(the migration application reads the keys), Step 10 (board truths depend on
which rows he keyed fatal), Steps 11–14 (review, the atomic commit, the
ship). Until the gate exits, no statement about post-migration rung
positions is a fact anywhere — including in conversation.

**The evidence-review clause (the producer's extension ruling,
2026-09-03):** the worksheet's second table — `## Treatment evidence
review — fatal rows` — carries one composer-proposed `Treatment evidence`
value per fatal-keyed row (`gate-reachability.md` row 1 excluded, its
planned form already ruled), each proposed citation verified to resolve
against the live tree, and EMPTY-with-reason where no direct evidence
exists. The gate now ALSO exits only when the producer has keyed every
proposal row: `empty` (the cell stays empty — that item refuses honestly
at its scope parse with the fatal-evidence demand until re-qualified in
its own item, a real gap kept visible), or the final citation text
verbatim as it should land (accepting or editing the proposal — his key
is what lands). His ruling, verbatim: *"Ship only the evidence the
callback can cite directly; leave any unsupported cell empty so its item
still refuses honestly."* The point is distinguishing genuinely unproven
countermeasures from built ones whose citations were merely absent — a
board where nearly everything refuses solely on migration-omitted
evidence would hide the few real gaps inside noise.

**Correction, 2026-09-03, written by the CONDUCTOR, not the composer**
(the composer is rate-limited; this is declared rather than passed off as
its work): the evidence-key resolution check originally globbed the text
before the first ` — `, which refuses a legal **planned-form** key
outright — the producer keyed two of them. It now calls
`kit._treatment_evidence_form`, the same classifier the migrated cell
faces at every later gate, so the gate and the checker cannot disagree.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 - <<'EOF'
import glob, re, sys
ws = "docs/plans/2026-09-03-risk-state-split-migration-review.md"

def norm(s):
    s = s.lower().replace("—", "-").replace("--", "-")
    return re.sub(r"\s+", " ", s).strip()

SEV = {"fatal", "non-fatal"}
TRE = {"countermeasure - permanent", "countermeasure - temporary",
       "accepted", "accepted unknown"}
blank, bad, n_sev, n_tre = [], [], 0, 0
for line in open(ws, encoding="utf-8"):
    m = re.match(r"^\| (\d+) \| (Severity|Treatment) \|", line)
    if not m:
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    key = norm(cells[-1])
    if not key:
        blank.append(line.strip()[:60])
    elif cells[1] == "Severity":
        n_sev += 1
        if key not in SEV:
            bad.append(line.strip()[:60])
    else:
        n_tre += 1
        if key not in TRE:
            bad.append(line.strip()[:60])
ev_blank, ev_bad, n_ev = [], [], 0
for line in open(ws, encoding="utf-8"):
    m = re.match(r"^\| (\S+\.md) \| (\d+) \|", line)
    if not m:
        continue
    n_ev += 1
    key = [c.strip() for c in line.strip().strip("|").split("|")][-1]
    if not key:
        ev_blank.append(line.strip()[:60])
    elif key.lower() != "empty":
        # One implementation, not two (the rule-9 lesson): the gate asks the
        # SAME classifier the migrated cell will face — kit._treatment_evidence_form
        # — so a key that exits this gate cannot fail the ledger check later.
        # A planned-form key is legal here (its location is a future path and is
        # deliberately not resolved); a citation must resolve today.
        sys.path.insert(0, "tools/gates")
        import kit
        form = kit._treatment_evidence_form(".", key)
        if form not in ("planned", "verified"):
            ev_bad.append(f"{form}: {key[:48]}")
if n_ev != 29:
    print(f"GATE NOT EXITED: expected 29 evidence rulings, found {n_ev}")
    sys.exit(1)
if blank or bad or ev_blank or ev_bad:
    print(f"GATE NOT EXITED: {len(blank)} unkeyed, {len(bad)} illegal, "
          f"{len(ev_blank)} evidence rulings unkeyed, {len(ev_bad)} citations unresolved")
    for x in (blank + bad + ev_blank + ev_bad)[:6]:
        print("  ", x)
    sys.exit(1)
print(f"gate exited: {n_sev} severities + {n_tre} treatments keyed, all legal; "
      f"{n_ev} evidence rulings keyed, every kept citation resolves")
EOF
```

Expected: `gate exited: 79 severities + 1 treatments keyed, all legal; 29
evidence rulings keyed, every kept citation resolves`. Any unkeyed or
illegal cell — severity, treatment, or evidence ruling — fails the step;
the step repeats after the next keying batch. The gate is exited only by
the producer's keys, never by a player's edit to the worksheet.

---

## Phase C — dependent on the keyed worksheet

Every step below DEPENDS on Step 8's exit. Board-position statements in
this phase are branches on the keys, not facts of this spec.

### Step 9 — apply the migration from the keyed worksheet

**Corrections, 2026-09-03, written by the CONDUCTOR (the composer is
rate-limited; declared rather than passed off as its work).** A closing
sweep after Step 9's verify failed — because fixing the site a failure
names and not its neighbours is this repo's own measured defect — found
four sites, of which three had not yet fired:

- **Step 9's verify** globbed the text before the first ` — `, refusing a
  legal planned-form key. It now calls `kit._treatment_evidence_form`,
  as Step 8's already does.
- **Steps 11, 12 and 13's clean-tree assertions** counted `CONTEXT.md`
  and `TODO.md` as work left uncommitted. They are session state: switch
  owns them at the boundary and they never ride a work commit (standing
  decision, v0.67.0). All three assertions now exclude them by name, so
  they assert what they meant to assert.


[delegate, model: sonnet, effort: medium]

**Depends on:** Step 8's keyed worksheet — refuse to run while its verify
fails.

**What.** From the repo root, run exactly this program. It is deliberately
double-run-safe (it asserts the pre-split header before touching a record)
and infers nothing: every non-mechanical value comes from the keys.

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 - <<'EOF'
import glob, os, re

OLD = ["Risk", "Killer?", "Impact", "Likelihood", "Evidence",
       "State", "Countermeasure", "Review trigger"]
NEW_HEADER = ("| Risk | Killer? | Impact | Likelihood | Risk evidence | "
              "Severity | Treatment | Countermeasure | Treatment evidence | "
              "Review trigger |")
NEW_SEP = "|" + "---|" * 10
LEGAL = {"countermeasure - permanent", "countermeasure - temporary",
         "accepted", "accepted unknown"}
PLANNED = ("planned — --root fixtures in both directions, per the "
           "2026-09-02 treatment ruling, built in gate-reachability's loop "
           "· tools/gates/kit.py")

def norm(s):
    s = s.lower().replace("—", "-").replace("--", "-")
    return re.sub(r"\s+", " ", s).strip()

keys = {}
evkeys = {}
ws = "docs/plans/2026-09-03-risk-state-split-migration-review.md"
rec = None
for line in open(ws, encoding="utf-8"):
    h = re.match(r"^## (\S+\.md)\s*$", line)
    if h:
        rec = h.group(1)
    m = re.match(r"^\| (\d+) \| (Severity|Treatment) \|", line)
    if m:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        key = norm(cells[-1])
        assert key, f"unkeyed worksheet row: {rec} {cells[0]} {cells[1]}"
        keys[(rec, int(cells[0]), cells[1])] = key
    e = re.match(r"^\| (\S+\.md) \| (\d+) \|", line)
    if e:
        ecells = [c.strip() for c in line.strip().strip("|").split("|")]
        ekey = ecells[-1]
        assert ekey, f"unkeyed evidence ruling: {ecells[0]} row {ecells[1]}"
        if ekey.lower() != "empty":
            evkeys[(e.group(1), int(e.group(2)))] = ekey
assert len(evkeys) + sum(1 for l in open(ws, encoding="utf-8")
                     if re.match(r"^\| \S+\.md \| \d+ \|", l) and
                     [c.strip() for c in l.strip().strip("|").split("|")][-1].lower() == "empty") == 29

migrated = rows_out = 0
for p in sorted(glob.glob(os.path.join("docs", "product", "*.md"))):
    t = open(p, encoding="utf-8").read()
    m = re.search(r"^## Risk ledger[ \t]*$\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    if not m:
        continue
    rec = os.path.basename(p)
    body = m.group(1)
    lines = body.splitlines()
    tbl = [j for j, l in enumerate(lines) if l.strip().startswith("|")]
    hdr = [c.strip() for c in lines[tbl[0]].strip().strip("|").split("|")]
    assert hdr == OLD, f"{rec}: not the pre-split header — already migrated?"
    out = list(lines)
    out[tbl[0]] = NEW_HEADER
    out[tbl[1]] = NEW_SEP
    for i, j in enumerate(tbl[2:], start=1):
        c = [x.strip() for x in lines[j].strip().strip("|").split("|")]
        assert len(c) == 8, f"{rec} row {i}"
        risk, killer, impact, lik, ev, state, cm, rt = c
        st = norm(state)
        if rec == "gate-reachability.md" and i == 1:
            sev, tre, tev = "fatal", "countermeasure - permanent", PLANNED
        elif st == "":
            sev, tre, tev = "", "", ""
        else:
            sev = keys[(rec, i, "Severity")]
            tre = state if st in LEGAL else keys[(rec, i, "Treatment")]
            tev = evkeys.get((rec, i), "")
        out[j] = "| " + " | ".join(
            [risk, killer, impact, lik, ev, sev, tre, cm, tev, rt]) + " |"
        rows_out += 1
    new_body = "\n".join(out)
    if body.endswith("\n") and not new_body.endswith("\n"):
        new_body += "\n"
    open(p, "w", encoding="utf-8").write(t[:m.start(1)] + new_body + t[m.end(1):])
    migrated += 1
print(f"migrated {migrated} records, {rows_out} rows, "
      f"{len(evkeys)} keyed evidence citations written")
assert migrated == 21 and rows_out == 84, "measure moved — STOP, hand back"
EOF
```

Mechanics the program encodes, from D4: a legal old `State` cell copies
verbatim into `Treatment` (raw text, original dashes and case); the 4
empty-State rows take empty in both fields and skip the worksheet;
`gate-reachability.md` row 1 takes the ruled pair and the byte-exact
planned form; everything else takes its keyed values; `Treatment evidence`
takes the producer's keyed evidence ruling where one exists (the
worksheet's second table — a citation lands verbatim, `empty` stays
empty) and is empty everywhere else; all other cells copy byte-verbatim;
only table lines inside `## Risk ledger` sections change.

**Why.** The record half of the atomic pair — in the working tree only,
alongside the checker from Step 2, committed together by Step 12.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && test "$(grep -rl '| Likelihood | Evidence | State |' docs/product/ | wc -l)" -eq 0 && test "$(grep -rlF '| Risk evidence | Severity | Treatment |' docs/product/ | wc -l)" -eq 21 && grep -qF "planned — --root fixtures in both directions, per the 2026-09-02 treatment ruling, built in gate-reachability's loop · tools/gates/kit.py" docs/product/gate-reachability.md && test "$(git diff --name-only -- docs/product/ | wc -l)" -eq 21 && test "$(git diff -U0 -- docs/product/ | grep -E '^[+-][^+-]' | grep -vcE '^[+-]\|')" -eq 0 && python3 - <<'EOF'
import re
t = open("docs/product/question-set-staleness.md", encoding="utf-8").read()
m = re.search(r"^## Risk ledger[ \t]*$\n(.*?)(?=^## |\Z)", t, re.M | re.S)
rows = [l for l in m.group(1).splitlines() if l.strip().startswith("|")][2:]
for l in rows:
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    assert len(c) == 10 and c[5] == "" and c[6] == "", c
print("question-set-staleness: 4 rows, both fields empty — carried forward honestly")
EOF
python3 - <<'EOF'
import glob, os, re
ws = "docs/plans/2026-09-03-risk-state-split-migration-review.md"
rulings = {}
for line in open(ws, encoding="utf-8"):
    e = re.match(r"^\| (\S+\.md) \| (\d+) \|", line)
    if e:
        key = [c.strip() for c in line.strip().strip("|").split("|")][-1]
        rulings[(e.group(1), int(e.group(2)))] = key
assert len(rulings) == 29, f"expected 29 evidence rulings, found {len(rulings)}"
NEWC = 10
written = 0
for (rec, row), key in sorted(rulings.items()):
    tt = open(os.path.join("docs", "product", rec), encoding="utf-8").read()
    m = re.search(r"^## Risk ledger[ \t]*$\n(.*?)(?=^## |\Z)", tt, re.M | re.S)
    lines = [l for l in m.group(1).splitlines() if l.strip().startswith("|")]
    cells = [c.strip() for c in lines[2 + row - 1].strip().strip("|").split("|")]
    assert len(cells) == NEWC, (rec, row)
    want = "" if key.lower() == "empty" else key
    assert cells[8] == want, f"{rec} row {row}: evidence cell != ruling"
    if want:
        written += 1
        # CONDUCTOR CORRECTION 2026-09-03 (composer rate-limited; declared as
        # the conductor's, not passed off as the composer's): this globbed the
        # text before the first ' — ', which refuses a legal planned-form key —
        # the same defect Step 8's verify carried. It now asks the SAME
        # classifier the migrated cell faces, so gate, verify and checker
        # cannot disagree (one implementation, not three — the rule-9 lesson).
        sys.path.insert(0, "tools/gates")
        import kit
        form = kit._treatment_evidence_form(".", want)
        assert form in ("planned", "verified"), \
            f"{rec} row {row}: evidence cell is {form}: {want[:48]}"
print(f"evidence rulings landed: {written} citations verbatim (each resolving), "
      f"{29 - written} ruled empty — refusing honestly")
EOF
```

Expected: zero old headers under `docs/product/` and exactly 21 new ones
(both counts exit-safe); the ruled planned form byte-exact in
`gate-reachability.md`; the diff touches exactly 21 files and EVERY
changed line is a table line (the `grep -vcE '^[+-]\|'` zero-count is
exit-safe inside `$( )`); the four empty rows stayed empty in both new
fields.

### Step 10 — the full local suite, and the board truths as branches

[delegate, model: sonnet, effort: low]

**Depends on:** Steps 2, 3, 9 — the working tree holds checker + records +
fixtures together (the same shape the commit will freeze).

**What.** Run CI's exact battery locally, then check the design's
predicted truths — phrased as what they are: two predictions independent
of the keys, and one branch on them.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest && python3 tools/design/matrix.py selftest && python3 tools/design/matrix.py audit && python3 tools/diagram/gen_journey.py check && python3 tools/gates/fidelity.py && python3 tools/gates/gate.py route gate-reachability && python3 tools/gates/gate.py route question-set-staleness && python3 tools/gates/gate.py route risk-state-split
```

Expected: `selftest: 57 cases passed`; audit clean (findings acceptable,
problems not); release clean; the progress, matrix, journey and fidelity
checks green (`fidelity: skipped` is green — no boundary commit yet).
Then the truths:

- **SUPERSEDED 2026-09-03 by the producer's row-2 severity ruling, which
  postdates the design's seal** (conductor correction; the composer is
  rate-limited): the design-time prediction that `gate-reachability`
  unblocks is void. Its route DOES still carry one `FATAL risk` line, and
  that is correct — row 2 is fatal with an `accepted unknown` treatment and
  empty evidence, refusing independently of row 1. **Expected instead:**
  `gate-reachability` **remains at viability**; row 1 parses clean (fatal +
  permanent + planned evidence — the mechanism working); the migration
  clarifies the blocker rather than removing it. The zero-count assertion
  on `FATAL risk` is therefore REMOVED from this step, not merely
  re-expected. `question-set-staleness`
  still enters at `viability`, its scope needs naming the empty
  Severity/Treatment cells — today's honest state carried forward.
- **Branch on the keys and the evidence rulings:** each remaining route
  position follows from the producer's keys. A fatal-keyed row whose
  evidence ruling is a resolving citation parses qualified — its item's
  route is undisturbed by the split; a fatal-keyed row ruled `empty`
  refuses at scope with the fatal-evidence demand — the real gaps,
  visible outside migration-created noise, which is the extension
  ruling's point. Positions are READ from this output and reported to the
  conductor, never corrected by a player. A player who finds a route
  position surprising STOPS and reports; it does not edit ledgers or the
  worksheet.

### Step 11 — diff review: the blast radius against the design

[keep]

**Depends on:** Steps 1–10 all green; the producer's keys final.

**What.** The conductor reads the whole working tree before the one
commit. The checklist, each item against the diff (`git status
--porcelain` and `git diff`, plus the untracked worksheet read in full):

1. The changed-file set is EXACTLY D6's stage list, nothing more — any
   stray path is a stop.
2. `tools/gates/kit.py` against D1–D3: constants, refusal strings
   byte-exact, the FATAL narrowing, the acceptance block, the six
   fixtures matching the design's intents verbatim (old-only refused ·
   mixed refused · fully-migrated accepted · fatal+permanent+planned
   passes viability parse and verified passes acceptance ·
   still-planned-at-acceptance refused · fatal+temporary empty-trigger
   refused / named passes).
3. The 21 record diffs: only table lines; spot-check `gate-reachability.md`
   row 1 (the ruled triple and the planned form ending
   `· tools/gates/kit.py`), `hooks-autoload.md` row 3 (the producer's
   keyed treatment, his keyed severity), two records keyed in different
   batches (values match the worksheet).
4. The worksheet: every Key the producer's, none edited by a player
   (compare a sample against what he keyed at Step 8).
5. Boundaries held: `RUNGS` untouched; `docs/gates/`, `kivna/`,
   `docs/interrogations/` and every dated plan other than this spec and
   the worksheet untouched; `progress_kit.py`'s diff confined to the two
   fixture literals.
6. Prose surfaces read once, aloud-in-the-head, for a claim that outruns
   the machinery (the What's New entry claims only what Steps 2–9 built).

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && git status --porcelain && test "$(git status --porcelain | grep -vE '^(.M|M.|\?\?) (docs/product/|tools/gates/kit\.py|tools/diagram/progress_kit\.py|tools/gates/README\.md|skills/interrogate/SKILL\.md|docs/design/risk-ledger\.md|docs/design/risk-state-split\.md|docs/design/risk-state-split/|README\.md|\.claude-plugin/plugin\.json|\.claude-plugin/marketplace\.json|docs/plans/2026-09-03-risk-state-split-migration-review\.md|docs/plans/2026-09-03-risk-state-split-reseal\.md|docs/plans/2026-09-03-risk-state-split-spec\.md|CONTEXT\.md|TODO\.md)' | wc -l)" -eq 0 && test "$(git diff -- docs/gates/ kivna/ | wc -l)" -eq 0
```

Expected: the porcelain listing printed for the reviewer's eyes; zero
paths outside the stage-list pattern (exit-safe); zero diff lines in the
never-migrate directories. The judgment items (2–6) are the conductor's
reading, recorded in the session log — the command proves only the radius.

### Step 12 — THE atomic commit

**Conductor correction, 2026-09-03 (composer rate-limited, declared as
mine).** Caught by Step 11's own review: the producer's reseal of
`migration-map.html` corrected three files — the design doc, the view
source, and its render — that this manifest did not name. Committing
without them would have landed `docs/product/risk-state-split.md` carrying
the NEW fingerprint `fp:3b7b1c17243a` while the committed view still held
the pre-correction content, so `gate.py check design` would have found a
**diverged seal on the committed tree** and refused. All three now ride
the same atomic commit, which is what the atomicity rule means here: the
seal and the content it fingerprints cannot land in different commits.


[delegate, model: sonnet, effort: low]

**Depends on:** Step 11's review recorded. This is the FIRST git-writing
command in the entire spec.

**What.** Three actions, one commit:

1. In THIS spec file
   (`docs/plans/2026-09-03-risk-state-split-spec.md`), check Pieces boxes
   1 through 12 (`- [ ]` → `- [x]`), leaving 13–14 unchecked — the commit
   carries trailers 1–12, so it checks the twelve boxes it lands.
2. Stage EXACTLY the D6 list:

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && git add docs/product/conductor-boundary.md docs/product/funnel-driver.md docs/product/gate-reachability.md docs/product/gate-visuals.md docs/product/grounding-was-read.md docs/product/hooks-autoload.md docs/product/inline-composer.md docs/product/model-effort-advisory.md docs/product/progress-html.md docs/product/push-wiring.md docs/product/question-set-staleness.md docs/product/release-closeout.md docs/product/requirements-success-measurement.md docs/product/requirements-traceability.md docs/product/rigor-level.md docs/product/risk-state-split.md docs/product/rung-vocabulary.md docs/product/shared-memory.md docs/product/switch-fidelity.md docs/product/time-awareness.md docs/product/vault-unhook.md tools/gates/kit.py tools/diagram/progress_kit.py tools/gates/README.md skills/interrogate/SKILL.md docs/design/risk-ledger.md docs/design/risk-state-split.md docs/design/risk-state-split/migration-map.html docs/design/risk-state-split/migration-map.png README.md .claude-plugin/plugin.json .claude-plugin/marketplace.json docs/plans/2026-09-03-risk-state-split-migration-review.md docs/plans/2026-09-03-risk-state-split-reseal.md docs/plans/2026-09-03-risk-state-split-spec.md
```

3. Commit with a message whose subject names the split and whose body
   carries the twelve trailers (plus the session's standard trailers):

```
risk-state-split: one State becomes Severity + Treatment — checker, 21 records, keyed worksheet, six fixtures, prose, release, one tree

The atomic migration the killer row demanded: no committed tree before or
after this commit contains mixed ledger schemas. 84 rows; 79 severities and
1 treatment keyed by the producer in the committed review worksheet;
gate-reachability's row from the 2026-09-02 ruling; the four empty rows
carried forward empty. Fixtures T64-T69 prove the refusal in both
directions in this same commit. v0.106.0.

Piece: risk-state-split/1
Piece: risk-state-split/2
Piece: risk-state-split/3
Piece: risk-state-split/4
Piece: risk-state-split/5
Piece: risk-state-split/6
Piece: risk-state-split/7
Piece: risk-state-split/8
Piece: risk-state-split/9
Piece: risk-state-split/10
Piece: risk-state-split/11
Piece: risk-state-split/12
```

Do NOT push — the render is not refreshed yet (Step 13 owns the ship).

**Why.** The countermeasure itself: checker + records + worksheet +
fixtures + prose + release metadata become one tree state. Fixtures T64 and
T65 prove the refusal in both directions AT this commit; CI on Step 13's
push is fixture 3's live proof.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && test "$(git grep -l '| Likelihood | Evidence | State |' HEAD -- docs/product/ | wc -l)" -eq 0 && test "$(git grep -lF '| Risk evidence | Severity | Treatment |' HEAD -- docs/product/ | wc -l)" -eq 21 && git grep -qF 'LEDGER_COLUMNS_PRE_SPLIT' HEAD -- tools/gates/kit.py && git cat-file -e HEAD:docs/plans/2026-09-03-risk-state-split-migration-review.md && test "$(git log -1 --format=%B | grep -c '^Piece: risk-state-split/')" -eq 12 && test "$(git status --porcelain | grep -vE '^\?\?' | grep -vE ' (CONTEXT|TODO)\.md$' | wc -l)" -eq 0
```

Expected: the COMMITTED tree (HEAD, not the working tree) holds zero old
headers and all 21 new ones — the no-mixed-tree invariant proven where it
binds; the checker and worksheet are in the commit; twelve Piece trailers;
nothing tracked left uncommitted (untracked leftovers, if any, are the
conductor's to triage — none are this spec's).

### Step 13 — the ship: render, render commit, ONE push, CI

[delegate, model: sonnet, effort: low]

**Depends on:** Step 12's commit at HEAD.

**What.** The commit moved derived rungs (at minimum `risk-state-split`
itself; others per the producer's keys), so the ship flow applies: refresh
the render, commit it WITHOUT a Piece trailer, push once — the work commit
and the render commit travel in the same push.

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/diagram/progress.py && python3 tools/diagram/progress.py stale && git add docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html && git commit -m "Refresh the progress render — the board reports the post-split truth" && git push
```

The render after this commit is what reports the true post-migration board
— the design's own words: positions were not claimable until the keys, and
the render is what reports them now. If `gh` is available, watch the run
(`gh run watch`, or `gh run list --limit 1` until green) and report the
result; if not, report that CI's verdict is pending on the remote — do not
claim green unwatched.

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/diagram/progress.py stale && test "$(git status --porcelain | grep -vE '^\?\?' | grep -vE ' (CONTEXT|TODO)\.md$' | wc -l)" -eq 0 && git log origin/main -2 --oneline | head -2 && test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: the render current; the tracked tree clean; HEAD equals
`origin/main` — both commits pushed in the one push. CI green on that push
is fixture 3's live proof; report its actual observed state, never an
assumed one.

### Step 14 — close the boxes

[delegate, model: haiku, effort: low]

**Depends on:** Step 13 pushed and CI's verdict reported.

**What.** In this spec file, check boxes 13 and 14. That takes Pieces
to zero unchecked, which moves the item's derived rung — so the same ship
flow rides: refresh the render, commit spec + render together (no Piece
trailer — box-keeping, not new work), one push.

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && python3 tools/diagram/progress.py && git add docs/plans/2026-09-03-risk-state-split-spec.md docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html && git commit -m "risk-state-split: all pieces boxed; render current" && git push
```

**Verify:**

```bash
repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root" && test "$(grep -c '^- \[ \] ' docs/plans/2026-09-03-risk-state-split-spec.md)" -eq 0 && python3 tools/diagram/progress.py stale && python3 tools/gates/gate.py route risk-state-split && test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: zero unchecked boxes (exit-safe would be needed at zero — and
zero IS expected, so the count runs inside `$( )` where a no-match exits
clean through `test`); the render current; the route printout showing
`risk-state-split` at the loop's exit — `enters at: acceptance` — with the
producer's acceptance gate as the next and last human key; HEAD pushed.
Acceptance itself (the gate record, the producer's key) is DRIVE's
business at its own sitting, not this spec's — this spec ends with the
evidence ready for his review.
