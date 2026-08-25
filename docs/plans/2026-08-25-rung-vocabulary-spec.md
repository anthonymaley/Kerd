# Rung vocabulary — slice 1, the ladder restructure, atomic

Contract for `docs/product/rung-vocabulary.md`, release slice 1 (rigor: mvp).
Design: `docs/design/rung-vocabulary.md`; GO record:
`docs/gates/2026-08-25-rung-vocabulary-design.md`.

**What lands.** `RUNGS` goes eight → seven: `frame, viability, scope, design,
handoff, loop, acceptance`. `slice → scope`, `contract → handoff`,
`build`+`goal` fold into `loop` as one route position (a container checked only
at its edges), and old `loop`'s human key becomes `acceptance`. `STAGES`
becomes `framed, viable, scoped, designed, handed-off, looping,
ready-to-release`. `## Release slice` is renamed `## Scope` and moves from the
design gate to the scope gate; the rigor law moves with it. Viability gains its
first content check: killer risks NAMED in the ledger (rows with `Killer?` =
yes — presence only, no qualification). `route()` gains a derived terminal:
`ready-to-release` when every rung's inputs exist *and* the acceptance record
is on disk. Retired names become read-only parser aliases forever; the writer
emits only live names. The sweep covers the board tooling, the journey
generator, the gates README (the canonical home), the skills that name the old
gate records, the root README, and the living design docs. The board is
re-rendered in the same push.

**What does not land.**
- Nothing under `docs/gates/` or `kivna/sessions/` is touched — ever. The
  parser adapts to them; no file on disk is renamed or rewritten.
- `docs/product` → `docs/work` — different item, out of scope.
- `CONTEXT.md` and `TODO.md` — switch owns them; CONTEXT.md is append-only
  between licensed prune events, and this build is not one.
- The dated renders under `docs/plans/` (`2026-08-0x-*.svg/.excalidraw`) are
  NOT regenerated — see D8, a declared divergence from the design's sweep
  table, raised at the approval gate.
- No new subcommand, no `gate.yml` change, no `skills/drive/` (does not exist).

**Version bump: YES — 0.98.0 → 0.99.0 (MINOR, changed behavior).** The sweep
genuinely requires skill text changes: `skills/conductor/SKILL.md`,
`skills/slainte/SKILL.md` (including its frontmatter trigger description) and
`skills/switch/SKILL.md` all name `docs/gates/*-goal.md` as the completion
trigger, which after this slice will never fire again — new records are
`*-acceptance.md`. Per CLAUDE.md's release checklist, the version is bumped in
all three locations: `.claude-plugin/plugin.json` → `version`,
`.claude-plugin/marketplace.json` → `metadata.version` AND
`plugins[0].version`. The capability-list descriptions do not change (their
one `handoff` is already qualified as "session and machine handoff"), so R2
stays clean without edits.

**Workflow / CI impact.** `.github/workflows/gate.yml` is unchanged. Every one
of its nine legs is re-anchored by this slice: `gate.py selftest` (rewritten
fixtures), `gate.py audit` (renamed sections, new AU2 clause, alias legality),
`gate.py release` (version sync after the bump), `progress.py selftest`
(board terminal fixture), `progress.py stale` (byte-compares the re-rendered
trio). **The tree is CI-red at every intermediate state** — kit.py without the
migrated work records fails AU2, and migrated records without kit.py fail
front-matter legality. This is the atomic-restructure case the ordering rule
anticipates: NO step commits alone. All work lands as ONE work commit carrying
every `Piece: rung-vocabulary/<n>` trailer, followed by ONE render commit for
the progress trio, pushed together (Step 10). CI runs only on the pushed head.

**Step headings are `### Step N — <name>`**, not `## Step`, because the loop
gate's checker (`STEP_HEADING_RE = ^### Step `) binds on `###`.

---

## Decisions the steps depend on

### D1 — the ladder's literals

```python
RUNGS  = ["frame", "viability", "scope", "design", "handoff", "loop", "acceptance"]
STAGES = ["framed", "viable", "scoped", "designed", "handed-off", "looping", "ready-to-release"]

# Retired names — READ-ONLY aliases, forever. The parser's legal set is the
# union of live names and retired aliases; the WRITER only ever emits live
# names. An alias that is still written is a synonym, which is the defect
# this item exists to remove. No file on disk is ever renamed or rewritten.
STAGE_ALIASES = {
    "sliced": "scoped",
    "contracted": "handed-off",
    "building": "looping",
    "done": "ready-to-release",
}

GATE_RECORD_RE = re.compile(
    r'^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*-'
    r'(frame|viability|slice|scope|design|contract|handoff|build|goal|loop|acceptance)\.md$'
)

RIGOR_SECTION_HEADING_RE = re.compile(r'^## Scope[ \t]*$')
```

`ROUTES`, `LEDGER_COLUMNS`, `LEGAL_STATES`, `RIGOR_LEVELS` are unchanged.
Two helpers, defined once next to `STAGES`:

```python
def legal_stage(v):
    return v in STAGES or v in STAGE_ALIASES

def stage_index(v):
    """Position on the live ladder; a retired value maps to its live name."""
    return STAGES.index(STAGE_ALIASES.get(v, v))
```

Every stage-legality test in kit.py (`check_rung`'s front-matter row,
`_audit_au2`, `_audit_au4`) uses `legal_stage`; every ordering comparison in
`_audit_au2` uses `stage_index`. Have/need/problem lines always print the
stage value AS WRITTEN in the file, never the mapped one.

**A named limit, stated not hidden:** AU3 validates filenames only, so it
cannot tell a NEW file written with a retired suffix from an old record — a
freshly written `-goal.md` would pass. The write discipline lives in the gates
README and the skills; the machine holds the read side only.

**The CLI surface:** `gate.py check <slug> <rung>` accepts LIVE rung names
only (`rung not in kit.RUNGS` → usage, exit 2, unchanged code). Retired names
are artifact aliases, not addressable gates. `ready-to-release` is a route
verdict, not a rung — `check` never takes it.

### D2 — the viability gate's new check: killer risks NAMED

Placement: inside `check_rung`'s `idx >= RUNGS.index("viability")` block,
after the `Value` section check. Semantics: presence only. The ledger section
must exist and contain at least one data row whose `Killer?` cell, stripped
and lowercased, equals `"yes"`. NO qualification is applied here — empty
Evidence, illegal State, even a FATAL row do not refuse at viability (rows
still parse out of `parse_ledger` alongside its problems; the problems are
ignored at this gate). Full qualification stays at scope, unchanged.

Rows, verbatim (`R` = `docs/product/<slug>.md`):

| Case | Row |
|---|---|
| product file absent | need `R — section "Risk ledger" naming at least one killer risk (Killer? = yes)` (appended in the not-exists branch alongside the existing three) |
| section absent or empty | need `R — section "Risk ledger" naming at least one killer risk (Killer? = yes)` |
| section present, no yes-row | need `R — Risk ledger names no killer risk (no row with Killer? = yes)` |
| ≥1 yes-row | have `R — Risk ledger names {k} killer risk(s) (Killer? = yes)` |

Implementation sketch (product exists):

```python
ledger_body = find_section(product_text, "Risk ledger")
if not ledger_body:
    need.append(f'{rel_product} — section "Risk ledger" naming at least one killer risk (Killer? = yes)')
else:
    k_rows, _ = parse_ledger(ledger_body)
    killers = [r for r in k_rows if r["Killer?"].strip().lower() == "yes"]
    if killers:
        have.append(f'{rel_product} — Risk ledger names {len(killers)} killer risk(s) (Killer? = yes)')
    else:
        need.append(f'{rel_product} — Risk ledger names no killer risk (no row with Killer? = yes)')
```

**Declared consequence (correcting the design doc's numbers):** the design
declares "five work records go backwards from `enters at: slice` to
`enters at: viability`". Measured against the tree and the router's actual
semantics, the truth is: four records carry `## Value` and no ledger —
`diagram-toolkit`, `requirements-view`, `standards-grounding` (all three
`route: spike`, so the ladder bypasses them and nothing changes), and
`requirements-project-type-templates` (`route: new`), which today reports
`enters at: viability` and will report **`enters at: frame`**. Every other
ledger on disk already names ≥1 killer risk (measured 2026-08-25), so no
other slug regresses. The regression is declared here; NO exemption is added.

### D3 — the scope gate: what we commit to, plus the qualified ledger

`check_rung`'s `idx >= RUNGS.index("scope")` block (was `slice`) holds THREE
checks:

1. **The qualified ledger — unchanged.** Same `parse_ledger` call, same
   have/need texts (`section "Risk ledger" ({n} rows, all qualified)` etc.),
   FATAL refusal included.
2. **Section `Scope`** (moved from design, renamed from `Release slice`):
   have/need `R — section "Scope"`; when the product file is absent, need
   `R — section "Scope"` joins the not-exists branch.
3. **The rigor law** (moved from design): `rigor_problems(product_text)`
   non-empty → need
   `R — Scope declares a legal rigor level (Rigor level: spike|mvp|production-v1)`.

`rigor_problems` itself: `RIGOR_SECTION_HEADING_RE` becomes `^## Scope[ \t]*$`
and two problem strings change verbatim — `Rigor level line outside Release
slice` → `Rigor level line outside Scope`; `Release slice missing 'Rigor
level: <spike|mvp|production-v1>' line` → `Scope missing 'Rigor level:
<spike|mvp|production-v1>' line`. Duplicate/illegal texts unchanged. Its
docstring's "Release slice" mentions follow. AU6 inherits all of this through
the single parser.

The design gate (`idx >= RUNGS.index("design")`) keeps ONLY the concerns/views
block — `parse_concerns` + `view_rows`, texts unchanged. A work item declaring
no concerns passes design vacuously; that hole is the design doc's own open
question, owned elsewhere, not patched here.

`_audit_au2` changes: legality via `legal_stage`/`stage_index`; the
`sliced`-tier row becomes `stage_idx >= STAGES.index("scoped")` requiring
section `Scope` with problem text
`{rel} — stage {stage_v} ahead of its artifacts: missing section "Scope"`;
plus one NEW tier (D4 below). `framed`/`viable` tiers unchanged.

### D4 — loop is a container; acceptance is the producer's gate; ready-to-release is DERIVED

The machine checks only at the loop's edges. Rung-block mapping in
`check_rung`, with every have/need text kept character-for-character from the
old blocks:

| New block | Old block | Checks (unchanged texts) |
|---|---|---|
| `idx >= RUNGS.index("handoff")` | `contract` | `docs/design/<S>.md` exists · `docs/gates/*-<S>-design.md` design GO record |
| `idx >= RUNGS.index("loop")` | `build` | spec exists (`— contract spec`) · section `Pieces` with boxes · every `### Step ` carries `**Verify:**` — the loop's ENTRY |
| `idx >= RUNGS.index("acceptance")` | `goal` | zero unchecked boxes in Pieces (`— zero unchecked boxes in Pieces` / `— {n} unchecked boxes in Pieces`) — the loop's EXIT |

The old `loop` block (goal record + workflow) is DELETED from `check_rung` and
becomes the terminal's evidence:

```python
def acceptance_record(root, slug):
    """Basename of the first gate record proving producer acceptance, else
    None. Search order: sorted docs/gates/*-<slug>-acceptance.md, then sorted
    *-<slug>-goal.md (the read-only alias — 7 such records exist and are
    never rewritten). A file qualifies when it carries a non-empty
    'Release condition' OR 'Done condition' section (the section alias)."""

def terminal_check(root, slug):
    """{'have': [...], 'need': [...]} for the derived terminal."""
    # acceptance record:
    #   have: f"docs/gates/*-{slug}-acceptance.md — acceptance record ({basename})"
    #   need: f'docs/gates/*-{slug}-acceptance.md — acceptance record with section "Release condition"'
    # workflow (text unchanged from the old loop block):
    #   have/need: ".github/workflows/gate.yml — file exists"
```

`route()` gains the terminal case, after the walk, non-bypass only:

```python
if deepest_ok == RUNGS[-1]:                # every rung's inputs exist
    t = terminal_check(root, slug)
    if not t["need"]:
        enters_at, next_rung, missing = "ready-to-release", None, []
    else:
        enters_at, next_rung, missing = "acceptance", "ready-to-release", t["need"]
```

The result dict keeps its exact shape (`slug, enters_at, bypass, rungs,
missing_for_next, next`); `rungs` stays a 7-entry list keyed by `RUNGS` — the
terminal never appears as a rung row. `gate.py route`'s text render needs no
change: it prints `enters at: ready-to-release` and, when the record is
missing, `missing for ready-to-release:` followed by the terminal needs.

**The board** (`tools/diagram/progress_kit.py`, `board_for`): the one line
that would crash —

```python
e_idx = len(gates_kit.RUNGS) if route_result["enters_at"] == "ready-to-release" \
        else gates_kit.RUNGS.index(route_result["enters_at"])
```

— all seven rungs render `built`, no in-flight cell. Everything else in the
renderer is derived from `RUNGS` and adapts by itself.

**AU2's new tier** (the declaration-versus-evidence check the design calls
`stage_ahead`): with `slug = fname[:-3]`,

```python
if stage_idx >= STAGES.index("ready-to-release") and acceptance_record(root, slug) is None:
    problems.append(
        f"{rel} — stage {stage_v} ahead of its artifacts: no acceptance record "
        f"(docs/gates/*-{slug}-acceptance.md, or a legacy *-{slug}-goal.md)"
    )
```

The six migrated `stage: ready-to-release` records all pass this via their
legacy goal records. A human can no more type an item into `ready-to-release`
than into `designed`.

### D5 — what the words mean after the fold (vocabulary the sweep must respect)

- **`contract spec` survives.** The rung `contract` is retired; the artifact
  `docs/plans/<date>-<slug>-spec.md` is still "the contract spec" and
  conductor's "Write the contract" phrase is still the act performed at the
  `handoff` rung. Need-line text `— contract spec` is unchanged.
- **`slice` as an increment-noun survives.** "Slice 1", "the smallest
  valuable slice", "spec slice" name portions of work, not the rung. Only the
  RUNG name and the SECTION name retire. The migration renames heading lines,
  never body prose.
- **Prose about the last gate says "accepted as ready for release", never
  "done"** — the producer's ruling.
- **Bare `handoff` is banned in living docs where ambiguity matters**: *session
  handoff* for switch's mechanism, *work handoff* for the rung. A quoted user
  trigger word (`'handoff'` in switch's trigger-phrase list) stays bare — it
  quotes what a user types, not what the doc asserts.

### D6 — the work-record migration (21 files in `docs/product/`)

Two mechanical rules, heading-line and front-matter-line only, body prose
untouched:

1. Every line exactly `## Release slice` → `## Scope` (17 files; the
   `Rigor level:` line stays where it is, now inside `## Scope`).
2. Front-matter line `stage: sliced` → `stage: scoped` (2 files:
   `hooks-autoload.md`, `model-effort-advisory.md`); `stage: done` →
   `stage: ready-to-release` (6 files: `conductor-boundary.md`,
   `grounding-was-read.md`, `release-closeout.md`, `rigor-level.md`,
   `time-awareness.md`, `vault-unhook.md`).

Nothing else in these files changes — concerns blocks, seals, grounding,
ledgers, `route:` values all stay byte-identical. `docs/product/*.md` are
LIVING records; this is why no read alias exists for `## Release slice` —
after this step, nothing the parser reads carries it.

### D7 — the prose sweep, enumerated

**Skills** (exact edits; line numbers as of HEAD `7176ffa`):

| File | Edit |
|---|---|
| `skills/conductor/SKILL.md:375` | "landed a goal record (a new `docs/gates/*-goal.md` — a feature closed as complete)" → "landed an acceptance record (a new `docs/gates/*-acceptance.md` — a feature accepted as ready for release)" |
| `skills/conductor/SKILL.md:165` | "the design and contract stages" → "the design and handoff stages"; "or a release slice" → "or a Scope section" |
| `skills/slainte/SKILL.md:3` (frontmatter description) | "at a version bump or a goal-record landing" → "at a version bump or an acceptance-record landing" |
| `skills/slainte/SKILL.md:18` | "or a goal-record landing (a new `docs/gates/*-goal.md` in the session's work commits: a feature closed as complete)" → "or an acceptance-record landing (a new `docs/gates/*-acceptance.md` in the session's work commits: a feature accepted as ready for release)" |
| `skills/switch/SKILL.md:30` | "a **goal record landing** (a new `docs/gates/*-goal.md` — a work item closed as complete)" → "an **acceptance record landing** (a new `docs/gates/*-acceptance.md` — a work item accepted as ready for release)" |
| `skills/switch/SKILL.md:68` | "a goal record landing this session (`docs/gates/*-goal.md`)" → "an acceptance record landing this session (`docs/gates/*-acceptance.md`)" |

**Handoff qualification rule** (mechanical): in `skills/**/SKILL.md`, every
occurrence of `handoff` NOT already part of "session handoff" or
"work handoff" gets qualified as **session handoff** (every incumbent use is
switch-altitude), with exactly two exceptions: the quoted trigger word
`'handoff'` in switch's description stays bare (it quotes user input), and
"cross-machine handoff" becomes "cross-machine session handoff". Known sites:
`switch/SKILL.md` lines 8, 64, 70, 196, 277, 286, 293, 295, 323, 336, 347;
`kivna/SKILL.md:151` ("for LLM handoff" → "for LLM session handoff");
re-grep `skills/` for any missed line at build time.

**Root `README.md`**: line 7's ladder sentence — "eight-rung ladder (frame →
viability → slice → design → contract → build → goal → loop)" → "seven-rung
ladder (frame → viability → scope → design → handoff → loop → acceptance)".
Sections describing CURRENT behavior update their vocabulary ("landed a
feature's goal record" → acceptance record; "the design and contract stages"
→ "the design and handoff stages"; "a release slice" as artifact → "a Scope
section"; "session handoff" phrasing is already qualified). Version-history
narration ("at v0.73.0…", "On 2026-08-07…") is NOT reworded beyond those
vocabulary swaps — README's shorthand latitude is human-adjudicated, and the
Step 9 review holds the line.

**Living design docs + playbook** (Step 8): `docs/design/funnel-driver.md`,
`docs/design/diagram-types-by-rung.md`, `docs/design/gate-visuals.md`,
`docs/design/push-wiring.md`, `docs/design/release-closeout.md`,
`docs/design/time-awareness.md`, `docs/playbook.md`. Rule: references to the
CURRENT ladder's rung names update (`slice`→`scope`, `contract`→`handoff` as
rungs; `goal record`/`*-goal.md` as the completion record → acceptance record,
noting `*-goal.md` stays readable as history); historical narration about what
a rung WAS, and quoted producer statements, stay verbatim.
`docs/design/rung-vocabulary.md` itself is NOT edited — its old-name tables
document the rename and are correct as written.

### D8 — renders: living surfaces regenerate; dated records stand

The design's sweep table says the ~23 rendered artifacts under `docs/plans/`
are "regenerated from the generators, never hand-edited". This spec applies
the never-hand-edit half everywhere and the regeneration half ONLY to living
(undated) surfaces: the progress trio (`progress.excalidraw/svg/html` —
CI-enforced by `stale`), the journey pages (`journey-shared-memory.html`,
`journey-switch-fidelity.html`, `journey-time-awareness.html`), and any
undated output of an edited generator (e.g. `project-types.svg`). The DATED
renders (`2026-08-0x-*.svg/.excalidraw`) are point-in-time drawings of the
old ladder — regenerating them would rewrite dated records to say something
they did not say on their date. Generator SOURCE files (living code) are
updated regardless. **This is a deliberate divergence from the design's sweep
row, raised at the approval gate — if the producer wants the dated renders
regenerated instead, only Step 5's regeneration list changes.**

### D9 — the version bump

`0.98.0` → `0.99.0` in all three locations, byte-identical:
`.claude-plugin/plugin.json` `version`; `.claude-plugin/marketplace.json`
`metadata.version`; `.claude-plugin/marketplace.json` `plugins[0].version`.
No description field changes.

---

## Pieces

- [ ] 1. `tools/gates/kit.py` — the seven-rung ladder, aliases, killer check, terminal, fixtures (45 cases)
- [ ] 2. `docs/product/*.md` — heading and stage migration, audit clean
- [ ] 3. `tools/diagram/progress_kit.py` — board terminal + fixtures (15 ok)
- [ ] 4. `tools/diagram/gen_journey.py` — seven-rung table, PLAIN map, three pages regenerated
- [ ] 5. Remaining generators — retired rung words out of living code
- [ ] 6. `tools/gates/README.md` — the canonical write-down, rewritten
- [ ] 7. Skills sweep + root README + version bump to 0.99.0
- [ ] 8. Living design docs + playbook sweep
- [ ] 9. Diff review of pieces 1–8 against D1–D9; board-delta review
- [ ] 10. Full local suite, renders, two-commit assembly, push

---

### Step 1 — kit.py: the seven-rung ladder, aliases, terminal, and the fixture suite

[delegate, model: sonnet, effort: high]

**What.** Edit `/Users/anthonymaley/Kerd/tools/gates/kit.py` only. Stdlib
only. Apply D1–D4 exactly:

1. **Constants** (lines 34–35, 91–93, 110): `RUNGS`, `STAGES`,
   `STAGE_ALIASES`, `GATE_RECORD_RE`, `RIGOR_SECTION_HEADING_RE` per D1, with
   D1's alias comment kept verbatim. Add `legal_stage` and `stage_index`
   directly below.
2. **`rigor_problems`**: the two message changes and heading regex per D3;
   docstring's "Release slice" mentions become "Scope".
3. **`check_rung`**: front-matter legality via `legal_stage` (have-line
   prints the stage as written); viability block gains the killer check (D2,
   including the product-absent need row); `slice` block becomes `scope` and
   gains the `Scope` section row and the rigor need row (D3); `design` block
   drops the Release-slice and rigor rows, keeps concerns/views untouched;
   `contract` → `handoff` (same checks); `build` → `loop` (same checks);
   `goal` → `acceptance` (same checks); the old `loop` block is deleted.
   Update the module docstring / block comments where they name the old rungs.
4. **`acceptance_record` + `terminal_check`** per D4, placed after
   `check_rung`; **`route`** gains the terminal case per D4 — result shape
   unchanged, `rungs` stays 7 entries.
5. **`_audit_au2`**: `legal_stage`/`stage_index`; `sliced` tier →
   `scoped`-requires-`Scope` (D3 text); the new `ready-to-release` tier (D4
   text). **`_audit_au4`**: legality via `legal_stage`.
6. **Fixtures** — rewrite in place and append; final count **45**
   (`selftest()` docstring and print → `selftest: 45 cases passed`):
   - T4: after the fm+Value write, `route` → `"frame"`, and
     `check_rung(root, slug, "viability")["need"]` contains
     `docs/product/alpha.md — section "Risk ledger" naming at least one killer risk (Killer? = yes)`.
     Then append a named-only ledger (header + one row
     `| No adoption | yes | high | medium |  | accepted unknown |  |  |`) →
     `route` → `"viability"`.
   - T5, T6: the `check_rung(..., "slice")` calls become `"scope"`;
     fixture bodies keep the T4b named-only viability floor satisfied (their
     row 1 already carries `Killer? = yes`); assertions unchanged.
   - T7: `ledger_good` → `route` → `"viability"` (scope now also wants
     `## Scope`; the old expectation `slice` is gone).
   - T8a: append `\n## Scope\n\nRigor level: mvp\n\nShip the caching path first.\n`
     → `route` → `"design"` (no concerns declared → design passes vacuously).
     T8b: + design doc + design GO record → `"handoff"`.
   - T9a: spec on disk → `"loop"`. T9b: the missing-Verify variant refuses at
     `check_rung(root_variant, slug, "loop")` naming Step 1 (was `"build"`).
   - T10a: boxes all checked → `"acceptance"`. T10b: +
     `docs/gates/2026-01-03-alpha-acceptance.md` containing
     `---\nroute: new\nstage: ready-to-release\n---\n\n## Release condition\n\nAll steps verified and merged.\n`
     + `.github/workflows/gate.yml` → `route` → `"ready-to-release"` and
     `result["next"] is None`.
   - T12: expectations unchanged (still exactly 3 problems).
   - T19–T24, T26: every `## Release slice` in fixture bodies → `## Scope`;
     expected problem strings verbatim per D3 (`Scope missing 'Rigor level:
     <spike|mvp|production-v1>' line`, `Rigor level line outside Scope`);
     T20's rung call becomes `check_rung(root_v2, "gamma", "scope")` with the
     need row `docs/product/gamma.md — Scope declares a legal rigor level
     (Rigor level: spike|mvp|production-v1)` (membership assert).
   - T25: `check_rung(root_f1, slug, "loop")` (was `"build"`).
   - `BODY` (the T33+ constant): `## Release slice` → `## Scope`. T35/T39
     expectations unchanged (`"design"`, clean audit — BODY's ledger row
     carries `Killer? = yes`).
   - **T42 (append)** — alias filenames and stage aliases: a tree whose
     `docs/gates/` holds `2026-01-01-x-slice.md`, `-contract.md`,
     `-build.md`, `-goal.md`, `-acceptance.md`, each
     `---\nroute: new\nstage: done\n---\n\nbody\n` → `audit(root) == []`.
     A second tree with `2026-01-01-x-bogus.md` (same front matter) →
     exactly one problem, naming the gate-record pattern.
   - **T43 (append)** — the legacy terminal: T10's tree but with
     `2026-01-03-alpha-goal.md` carrying `## Done condition` instead of the
     acceptance record → `route` → `"ready-to-release"`, and the terminal
     have-line names the `-goal.md` basename.
   - **T44 (append)** — AU2's new tier: a product doc complete through
     `## Scope` (with rigor line and a qualified killer ledger) declaring
     `stage: ready-to-release`, no gate records → `audit` contains
     `docs/product/beta.md — stage ready-to-release ahead of its artifacts: no acceptance record (docs/gates/*-beta-acceptance.md, or a legacy *-beta-goal.md)`;
     add `2026-01-03-beta-goal.md` with `## Done condition` → that problem is
     gone (membership asserts both ways).
   - **T45 (append)** — purity, no tree needed:
     `set(RUNGS) == {"frame","viability","scope","design","handoff","loop","acceptance"}`
     and none of `build`, `verify`, `adjust`, `goal`, `slice`, `contract` is
     in `RUNGS`; and on T10b's terminal tree `enters_at` was
     `"ready-to-release"` (asserted there) — restate here as
     `"goal" not in RUNGS and "build" not in RUNGS`.

Do NOT run `gate.py audit` against the real repo in this step — it is red by
design until Step 2 migrates the work records.

**Why.** D1–D4. The folded checks keep their exact tests and texts so every
slug's reported position changes label, not substance — the design's own
countermeasure for the router risk.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest; echo "exit=$?"
```

Expected: `root resolution: 7 cases passed`, `selftest: 45 cases passed`,
`exit=0`.

---

### Step 2 — the work-record migration

[delegate, model: haiku, effort: low]

**What.** Apply D6 to `/Users/anthonymaley/Kerd/docs/product/*.md`, exactly:
every line exactly `## Release slice` becomes `## Scope` (17 files); the
front-matter line `stage: sliced` becomes `stage: scoped` in
`hooks-autoload.md` and `model-effort-advisory.md`; `stage: done` becomes
`stage: ready-to-release` in `conductor-boundary.md`, `grounding-was-read.md`,
`release-closeout.md`, `rigor-level.md`, `time-awareness.md`,
`vault-unhook.md`. Touch no other line, no other directory — `docs/gates/` and
`kivna/sessions/` are immutable and stay byte-identical.

**Why.** D6. After this step nothing the parser reads carries the retired
section name, which is why it needs no read alias.

**Verify:**

```
cd /Users/anthonymaley/Kerd && \
grep -rln '^## Release slice' docs/product/ | wc -l && \
grep -rln '^stage: \(sliced\|done\|contracted\|building\)$' docs/product/ | wc -l && \
grep -c '^## Scope$' docs/product/rung-vocabulary.md && \
git diff --stat -- docs/gates kivna | wc -l && \
python3 tools/gates/gate.py audit && \
for s in vault-unhook requirements-project-type-templates funnel-driver gate-visuals rung-vocabulary; do \
  python3 tools/gates/gate.py route $s | grep '^enters at:'; done
```

Expected: `0`, `0`, `1`, `0`, `audit: clean` (a findings count in parentheses
is fine), then exactly:

```
enters at: ready-to-release
enters at: frame
enters at: handoff
enters at: acceptance
enters at: loop
```

---

### Step 3 — the board learns the terminal

[delegate, model: sonnet, effort: medium]

**What.** Edit `/Users/anthonymaley/Kerd/tools/diagram/progress_kit.py`:

1. `board_for`: the `e_idx` line per D4 —
   `len(gates_kit.RUNGS)` when `enters_at == "ready-to-release"`, else
   `RUNGS.index(...)`. Nothing else in the renderer changes (rung rows,
   glyphs, HTML all derive from `RUNGS`).
2. `_F8_PRODUCT`: append a named-but-unqualified killer ledger so the fixture
   still parks at viability —

   ```python
   _F8_PRODUCT = (
       "---\nroute: new\nstage: framed\n---\n\n"
       "## Value\n\nSaves 10 hours a week across the team.\n\n"
       "## Risk ledger\n\n"
       "| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |\n"
       "|---|---|---|---|---|---|---|---|\n"
       "| Adoption risk | yes | high | medium |  | accepted |  |  |\n"
   )
   ```

3. `_f8`: `by_rung["slice"]` → `by_rung["scope"]`; assertions otherwise
   unchanged (frame built, viability in-flight, scope missing with need ≥ 1).
4. **New `_f15`** — "board: ready-to-release terminal — all rungs built": a
   tree with a product doc carrying Value, a fully qualified killer ledger
   (reuse the gates suite's T7 `ledger_good` shape), `## Scope` with
   `Rigor level: mvp`, plus `docs/design/alpha.md`, a
   `2026-01-01-alpha-design.md` GO record, an all-checked spec with a
   Verify-carrying step, `2026-01-03-alpha-acceptance.md` with
   `## Release condition`, and `.github/workflows/gate.yml`; committed.
   Assert: `_board(model)["enters_at"] == "ready-to-release"`, every rung's
   `state == "built"`, no rung `in-flight`, and `render_table(model)` returns
   without raising. Register it in `cases`; final print `selftest: 15 ok`.

**Why.** `RUNGS.index("ready-to-release")` is the one crash this restructure
plants in the board, and seven real slugs hit it on the first re-render.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 tools/diagram/progress.py selftest; echo "exit=$?"
```

Expected: `ok 15 — board: ready-to-release terminal — all rungs built` among
the lines, `selftest: 15 ok`, `exit=0`.

---

### Step 4 — the journey generator

[delegate, model: sonnet, effort: high]

**What.** Edit `/Users/anthonymaley/Kerd/tools/diagram/gen_journey.py`. Read
the whole file first — it maps the gates' need-line vocabulary to plain
English and renders committed living pages.

1. The `STAGES` table (line 43) goes eight entries → seven, keys matching
   `kit.RUNGS`, keeping each entry's `expects` list where its rung survives:

   ```python
   ("frame",      "Idea",             "the problem named, and what winning would be", [ ...unchanged... ]),
   ("viability",  "Validated",        "the risks sized, the killer one answered", [ ...unchanged... ]),
   ("scope",      "Scoped",           "what is in, what is out, and how rigorously it is measured", []),
   ("design",     "Designed",         "the solution drawn and agreed", [ ...unchanged... ]),
   ("handoff",    "Handed off",       "each piece written down precisely enough to hand over", []),
   ("loop",       "Building",         "built, verified and adjusted until nothing is left unchecked", []),
   ("acceptance", "Ready to release", "the producer's key: accepted as ready for release, or back round the loop", []),
   ```

2. `if s == "build" and pieces:` → `if s == "loop" and pieces:` (line 503).
3. The `PLAIN` map: keep `— contract spec$` (D5 — the artifact keeps its
   name). Update/extend for the texts D2–D4 introduce or rename, at minimum:
   the two killer-risk need texts; `section "Scope"$`; `Scope declares a
   legal rigor level`; the old `goal record with section "Done condition"`
   entry becomes the acceptance-record texts (both the need text with
   `section "Release condition"` and the have text `acceptance record
   (<basename>)`); keep the `gate.yml` entry. Any old-text entry that can no
   longer match (`Release slice`, `goal record`) is updated, not duplicated.
4. Handle `enters_at == "ready-to-release"` wherever the script compares
   `enters_at` against stage keys (read the file; the board index trap from
   D4 applies here too if it indexes).
5. Regenerate the three committed pages:

   ```
   python3 tools/diagram/gen_journey.py shared-memory
   python3 tools/diagram/gen_journey.py switch-fidelity
   python3 tools/diagram/gen_journey.py time-awareness
   ```

**Why.** The journey pages are living committed surfaces that bake the rung
words in; an unmapped need-line renders raw on purpose — the vocabulary must
move with the gates in the same change.

**Verify:**

```
cd /Users/anthonymaley/Kerd && \
python3 tools/diagram/gen_journey.py shared-memory && \
python3 tools/diagram/gen_journey.py switch-fidelity && \
python3 tools/diagram/gen_journey.py time-awareness && \
grep -c '"slice"\|"contract"\|"goal"' tools/diagram/gen_journey.py; \
grep -l 'Handed off' docs/plans/journey-*.html | wc -l
```

Expected: three clean exits, `0` retired keys in the generator, `3` pages
carrying the new stage label.

---

### Step 5 — the remaining generators

[delegate, model: sonnet, effort: medium]

**What.** In `/Users/anthonymaley/Kerd/tools/diagram/`, apply D5's vocabulary
to living code (rung names change; "the contract" / "Write the contract" as
the artifact and act do NOT):

1. `git mv gen_flow_contract.py gen_flow_handoff.py` and
   `git mv gen_flow_slice.py gen_flow_scope.py` (retired rung words out of
   writer filenames). First `grep -rn 'gen_flow_contract\|gen_flow_slice' tools/ docs/design/`
   and update any importer or doc reference found (none expected — they are
   leaf scripts).
2. In `gen_flow_handoff.py`, `gen_flow_design.py` (line ~97),
   `gen_flow_celtic_example.py` (line ~128), `gen_functions.py` (lines ~47
   and ~637): where `CONTRACT` labels the RUNG/phase ("hands to CONTRACT",
   `("CONTRACT", [...]` section keys, "(CONTRACT)" step labels) → `HANDOFF`;
   the phrase "Write the contract" and every "the contract" artifact mention
   stay verbatim.
3. `gen_kerd_map.py`, `gen_rigor_level.py`, `gen_project_types.py`,
   `gen_journey_head.py`: `Release slice` (section name) → `Scope`; any
   retired rung word used AS a rung name → its live name (read each hit in
   context; increment-noun "slice" stays, per D5).
4. Regenerate ONLY undated committed outputs of the generators edited here
   (D8). Determine each edited generator's output path from its source;
   `docs/plans/project-types.svg` is known-undated — regenerate it if
   `gen_project_types.py` changed. Dated outputs (`2026-08-0x-*`) are NOT
   regenerated even though their generators changed.

**Why.** The design's sweep found `contract → handoff` writes no history yet
edits more code than the rename that does — the word is a generator filename
and a rung key in three more. Leaving a writer emitting a retired name would
make it a synonym, the defect this item removes.

**Verify:**

```
cd /Users/anthonymaley/Kerd && \
ls tools/diagram/gen_flow_handoff.py tools/diagram/gen_flow_scope.py && \
grep -rn 'Release slice' tools/diagram/ | wc -l && \
grep -rn 'hands to CONTRACT\|(CONTRACT)' tools/diagram/ | wc -l && \
git status --porcelain docs/plans/ | grep -v 'journey-\|progress\.' ; echo "dated-renders-check-exit=$?"
```

Expected: both renamed files listed, `0`, `0`, and the final `git status`
shows no modified dated render (only undated regenerations, if any —
`dated-renders-check` lists nothing matching `2026-`).

---

### Step 6 — the gates README, the canonical home

[delegate, model: sonnet, effort: high]

**What.** Rewrite `/Users/anthonymaley/Kerd/tools/gates/README.md` to
describe the seven-rung ladder. It is the canonical write-down; every schema
statement must match Step 1's code exactly.

1. **Intro**: "runs the eight gates" → "runs the seven gates".
2. **The gate table**: seven rows — `frame` (unchanged) · `viability` (adds
   the killer-named check, D2's wording: "≥1 ledger row with `Killer?` =
   yes — named only; no sizing, no evidence, no qualification") · `scope`
   (the full qualified-ledger cell moved from the old `slice` row, plus
   section `Scope` and the rigor law) · `design` (concerns/views only) ·
   `handoff` (the old `contract` cell) · `loop` (the old `build` cell,
   introduced as "the loop's entry — the machine checks at the container's
   edges, never inside it") · `acceptance` (the old `goal` cell, "the loop's
   exit: zero unchecked boxes; evidence ready for producer review").
3. **A new section `## Ready to release — the derived terminal`** directly
   under the gate table: `route` reports `ready-to-release` when every rung's
   inputs exist AND the acceptance evidence is on disk — a gate record
   matching `docs/gates/*-<S>-acceptance.md` with section `Release condition`
   (legacy `*-<S>-goal.md` with `Done condition` reads forever), plus
   `.github/workflows/gate.yml`. The terminal is derived, never declared:
   `stage: ready-to-release` without the record is an AU2 problem. `check`
   takes live rung names only; the terminal is `route`'s verdict.
4. **Front-matter schema**: the `stage` row lists the seven live values;
   a new paragraph + table **`## Retired names — read forever, written
   never`** with D1's alias sets (stage values `sliced`, `contracted`,
   `building`, `done`; filename suffixes `slice`, `contract`, `build`,
   `goal`; section `Done condition`) and the rule verbatim: the parser's
   legal set is a union of live names and retired aliases; the writer only
   ever emits live names; no file on disk is ever renamed and no record ever
   rewritten. Name AU3's limit (a filename check cannot tell a new file from
   an old one — write discipline is this README's and the skills').
5. **Gate records**: the last-gate record is
   `YYYY-MM-DD-<slug>-acceptance.md` with `## Release condition`; prose says
   "accepted as ready for release", never "done". AU3's regex updated
   verbatim to D1's.
6. **Refusals example**: `Release slice` → `Scope`, `enters at: slice` →
   `enters at: viability` (keep the example internally consistent).
7. **Audit table**: AU2 (adds the `scoped`→`Scope` wording and the
   ready-to-release/acceptance-record clause), AU3 (new regex), AU6
   (`## Scope`).
8. **Rigor level section**: `## Release slice` → `## Scope` throughout,
   including the refusal literals (they must match `rigor_problems`'s new
   strings character for character).
9. Sweep the rest of the file for the old rung names used as CURRENT names
   (`slice`, `contract`, `build`, `goal` rows/mentions); leave the Views,
   fingerprint, seal, release-rules and CI sections otherwise untouched.

**Why.** "This README, not the dated spec it came from, is now the standard"
— its own rule. This spec is dated and will not be read again.

**Verify:**

```
cd /Users/anthonymaley/Kerd && python3 - <<'EOF'
t = open('tools/gates/README.md', encoding='utf-8').read()
checks = {
  "seven gates": "seven gates" in t,
  "scope row": "| `scope` |" in t,
  "handoff row": "| `handoff` |" in t,
  "acceptance row": "| `acceptance` |" in t,
  "no slice row": "| `slice` |" not in t,
  "no contract row": "| `contract` |" not in t,
  "terminal section": "## Ready to release" in t,
  "retired names section": "## Retired names" in t,
  "release condition": "Release condition" in t,
  "regex updated": "slice|scope" in t and "goal|loop|acceptance" in t,
  "rigor in Scope": "Scope missing 'Rigor level:" in t,
  "old rigor gone": "Release slice missing" not in t,
}
for k, v in checks.items(): print(k, v)
assert all(checks.values())
EOF
```

Expected: every flag `True`, exit 0.

---

### Step 7 — skills, root README, version bump

[delegate, model: sonnet, effort: medium]

**What.**

1. Apply D7's skills table — the six enumerated edits, verbatim.
2. Apply D7's handoff qualification rule: the enumerated lines, then
   `grep -rn 'handoff' skills/` and qualify any remaining bare use under the
   same rule (session handoff everywhere; the quoted trigger word `'handoff'`
   in switch's description stays bare).
3. Apply D7's root `README.md` edits (line 7's ladder sentence; the
   current-behavior vocabulary swaps; nothing else reworded).
4. Bump the version per D9: `0.98.0` → `0.99.0` in the three locations. No
   description field changes.

**Why.** The three skills name a firing condition (`*-goal.md` landing) that
would otherwise never fire again; skill text changed → the release checklist
demands the bump, in the same atomic change.

**Verify:**

```
cd /Users/anthonymaley/Kerd && \
python3 tools/gates/gate.py release && \
grep -c '"version": "0.99.0"' .claude-plugin/plugin.json && \
grep -c '"version": "0.99.0"' .claude-plugin/marketplace.json && \
grep -rn 'docs/gates/\*-goal\.md' skills/ | wc -l && \
grep -rn 'acceptance record' skills/conductor/SKILL.md skills/slainte/SKILL.md skills/switch/SKILL.md | wc -l && \
grep -n 'seven-rung ladder (frame → viability → scope → design → handoff → loop → acceptance)' README.md | wc -l && \
grep -rn '\bhandoff\b' skills/ | grep -v 'session handoff\|work handoff\|session-handoff\|'\''handoff'\''' | wc -l
```

Expected: `release: clean`, `1`, `2`, `0`, `≥5`, `1`, `0`.

---

### Step 8 — living design docs and the playbook

[delegate, model: sonnet, effort: medium]

**What.** Apply D7's living-docs rule to `docs/design/funnel-driver.md`,
`docs/design/diagram-types-by-rung.md`, `docs/design/gate-visuals.md`,
`docs/design/push-wiring.md`, `docs/design/release-closeout.md`,
`docs/design/time-awareness.md`, and `docs/playbook.md`. Procedure: for each
file, `grep -n 'slice\|contract\|build\|goal\|loop\|handoff'`, then judge
each hit against D5/D7 — a CURRENT-ladder rung name or a `*-goal.md`
completion reference updates (`goal record` → `acceptance record
(docs/gates/*-acceptance.md; legacy *-goal.md records stay readable)`);
historical narration, quoted producer statements, artifact vocabulary
("contract spec", "slice 1", "spec slice", "the smallest valuable slice")
and non-ladder senses ("build" as a verb, "goal" as an aim) stay verbatim.
Do NOT edit `docs/design/rung-vocabulary.md`. Qualify any bare `handoff` in
these files per D5 (work handoff for the rung, session handoff for switch).

**Why.** Living docs are the write side of the vocabulary; a living doc
still teaching the old rung names is a second live name — the defect itself.

**Verify:**

```
cd /Users/anthonymaley/Kerd && \
grep -rn 'contract rung\|slice rung\|goal rung\|the goal gate' docs/design/ docs/playbook.md | grep -v 'rung-vocabulary.md' | wc -l && \
python3 tools/gates/gate.py release && python3 tools/gates/gate.py audit
```

Expected: `0`, `release: clean`, `audit: clean` (findings in parentheses
fine).

---

### Step 9 — diff review against the decisions, and the board delta

[keep]

**What.** Read the full working-tree diff (`git diff` + `git status
--porcelain`) against D1–D9, line by line. It must catch:

- **Immutability**: `git status --porcelain docs/gates kivna` is EMPTY.
  Nothing dated under `docs/plans/` modified except undated living renders.
- **kit.py**: every renamed/new have-need text matches D2–D4 character for
  character (em-dashes and quotes included); the folded blocks kept the old
  texts; `legal_stage`/`stage_index` are the only stage-legality paths; the
  writer side emits no retired name anywhere (`grep -n "'-goal" tools/gates/`
  finds only the read-side globs and aliases).
- **The board delta is exactly the declared one.** Run
  `for f in docs/product/*.md; do python3 tools/gates/gate.py route $(basename $f .md) | grep '^enters at:'; done`
  and check against this table — any other movement is drift to hand back:

  | enters at | slugs |
  |---|---|
  | `ready-to-release` | conductor-boundary, grounding-was-read, push-wiring, release-closeout, rigor-level, time-awareness, vault-unhook |
  | `acceptance` | gate-visuals, progress-html |
  | `loop` | rung-vocabulary (this spec is on disk with unchecked boxes) |
  | `handoff` | funnel-driver |
  | `design` | inline-composer, model-effort-advisory, requirements-traceability, shared-memory, switch-fidelity |
  | `viability` | hooks-autoload |
  | `frame` | requirements-project-type-templates (the declared regression), diagram-toolkit, requirements-view, standards-grounding (spikes — bypass) |

- **Skills/README/design docs**: no rewording beyond D7's rules; quoted
  producer statements untouched; the version bump is exactly three fields.
- A miss is re-dispatched to its step, never patched in review.

**Why.** Eight delegated steps share one vocabulary; a one-character drift in
a refusal text is invisible to any single Verify but changes what three tools
say. The board table is the only place the whole restructure is visible at
once.

**Verify:** every bullet ticked; the route loop's output matches the table
exactly; `git status --porcelain docs/gates kivna` prints nothing.

---

### Step 10 — full suite, renders, two-commit assembly, push

[keep]

**What.** The assembly that keeps CI green on an atomic restructure:

1. Tick all boxes 1–9 in this spec's `## Pieces` (piece 10 ticks with them —
   this step is the act), re-run `python3 tools/gates/gate.py route
   rung-vocabulary` → `enters at: acceptance` (all boxes checked, no
   acceptance record yet — correct: the producer's key is still to turn).
2. Run the full local suite, gate.yml's order:
   `gate.py selftest` · `gate.py audit` · `gate.py release` ·
   `progress.py selftest` · `matrix.py selftest` · `matrix.py audit`.
3. Regenerate the journey pages once more (they read the worktree, which now
   has every box ticked), then make the **work commit**: every changed file
   EXCEPT `docs/plans/progress.{excalidraw,svg,html}`, message body carrying
   all ten trailers `Piece: rung-vocabulary/1` … `Piece: rung-vocabulary/10`.
   No `git add -A` — name the files.
4. `python3 tools/diagram/progress.py` (the render now sees the work commit's
   trailers in `git log`), then `progress.py stale` → `render current`, then
   the **render commit**: exactly the three trio files.
5. `git push` — one push, two commits; CI evaluates the head only.
6. `python3 tools/gates/fidelity.py` — it skips itself unless a session log
   is in the commit; if it names anything, that is the close-out's to fix,
   not a step here.

**Why.** `stale` byte-compares a fresh derivation (which includes the work
commit's own trailers) against the committed trio — a trio rendered BEFORE
the work commit can never match AFTER it. Two commits, one push, is the only
ordering where the pushed head is self-consistent.

**Verify:**

```
cd /Users/anthonymaley/Kerd && \
python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && \
python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest && \
python3 tools/design/matrix.py selftest && python3 tools/design/matrix.py audit && \
python3 tools/diagram/progress.py stale && \
git log -2 --format='%s' && git status --porcelain | wc -l && echo ALL-GREEN
```

Expected: `selftest: 45 cases passed`, `audit: clean`, `release: clean`,
`selftest: 15 ok`, both matrix legs clean, `render current`, the two commit
subjects, `0` uncommitted files, `ALL-GREEN`, exit 0.
