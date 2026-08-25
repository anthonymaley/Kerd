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
  NOT regenerated — see D8, settled by producer ruling (2026-08-25): living
  surfaces regenerate, dated records stand.
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

### D8 — renders: living surfaces regenerate; dated records stand — SETTLED by producer ruling, 2026-08-25

The design's sweep table said the ~23 rendered artifacts under `docs/plans/`
are "regenerated from the generators, never hand-edited". This spec applies
the never-hand-edit half everywhere and the regeneration half ONLY to living
(undated) surfaces: the progress trio (`progress.excalidraw/svg/html` —
CI-enforced by `stale`), the journey pages (`journey-shared-memory.html`,
`journey-switch-fidelity.html`, `journey-time-awareness.html`), and any
undated output of an edited generator (e.g. `project-types.svg`). The DATED
renders (`2026-08-0x-*.svg/.excalidraw`) are point-in-time drawings of the
old ladder — regenerating them would rewrite dated records to say something
they did not say on their date. Generator SOURCE files (living code) are
updated regardless.

**This divergence was raised at the approval gate and the producer ruled in
its favour** — recorded in `docs/design/rung-vocabulary.md`, section "A
living surface regenerates; a dated record stands — RULED 2026-08-25". His
rule, binding on this build: **old words inside dated records are not
drift** — they are the record being honest about its date; any current link
to a dated drawing labels it *historical / pre-rename* where ambiguity
matters; and **future generated records use the new vocabulary only**. The
orientation write-down for the six-month reader ("why does this old drawing
say `slice`?") lands in the canonical home — Step 6, item 8.

### D9 — the version bump

`0.98.0` → `0.99.0` in all three locations, byte-identical:
`.claude-plugin/plugin.json` `version`; `.claude-plugin/marketplace.json`
`metadata.version`; `.claude-plugin/marketplace.json` `plugins[0].version`.
No description field changes.

---

## Pieces

- [x] 1. `tools/gates/kit.py` — the seven-rung ladder, aliases, killer check, terminal, fixtures (45 cases)
- [x] 2. `docs/product/*.md` — heading and stage migration, audit clean
- [x] 3. `tools/diagram/progress_kit.py` — board terminal + fixtures (15 ok)
- [x] 4. `tools/diagram/gen_journey.py` — seven-rung table, PLAIN map, three pages regenerated
- [x] 5. Remaining generators — retired rung words out of living code
- [x] 6. `tools/gates/README.md` — the canonical write-down, rewritten
- [x] 7. Skills sweep + root README + version bump to 0.99.0
- [x] 8. Living design docs + playbook sweep
- [x] 9. Diff review of pieces 1–8 against D1–D9; board-delta review
- [x] 10. Full local suite, renders, two-commit assembly, push
- [x] 11. `tools/diagram/progress_kit.py` + two design docs — the board's GOAL labels become PIECES
- [x] 12. `gen_flow_celtic_example.py` + `gen_flow_handoff.py` — the split literal, and a purity check that can see one
- [x] 13. Root `README.md` — the current-architecture prose D7's enumeration missed
- [x] 14. Reseal `rungs-and-artifacts.html` — dead file path corrected, fingerprint retaken, PNG re-rendered
- [x] 15. The two deferrals recorded, not fixed — gate-visuals' view, diagram-types-by-rung, gen_flow_build
- [x] 16. Step 7's corrected check re-run; the assembly amended from ten pieces to sixteen

**Steps 11–16 were added by a callback on 2026-08-25**, after the build
surfaced sites this score did not assign. Every one of them sits on the FOLD
half of the rename (`build`+`goal` → `loop`+`acceptance`), never the
substitution half: D7's enumeration caught `slice → scope` and
`contract → handoff` exhaustively because they are one-for-one swaps, and
missed the fold because a fold has a DIRECTION that can be read backwards and
no closing grep outside `skills/` was ever written. **Run order: Steps 1–9,
then 11–16, then Step 10 last** — Step 10 is the assembly and must see every
edit. Step 16 carries the amendments Step 10 and Step 9 need and are not being
rewritten to hold.

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
8. **A new section `## Why dated plans still say slice, contract and goal`**
   — the orientation artifact the producer's D8 ruling asks for. It states:
   the ladder was renamed on 2026-08-25; living surfaces were regenerated and
   dated records under `docs/plans/` deliberately were not; a dated render
   shows the vocabulary current on its date; **old words in a dated record
   are not drift**; and any current link to a dated drawing should label it
   *historical / pre-rename* where ambiguity matters. Short — a six-month
   reader opening a dated plan must be able to answer "why does this old
   drawing say `slice`?" from this section alone, without re-deriving the
   ruling.
9. **Rigor level section**: `## Release slice` → `## Scope` throughout,
   including the refusal literals (they must match `rigor_problems`'s new
   strings character for character).
10. Sweep the rest of the file for the old rung names used as CURRENT names
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
  "dated-plans orientation": "## Why dated plans still say" in t,
  "rename dated": "2026-08-25" in t,
  "not drift": "are not drift" in t,
  "historical label": "historical / pre-rename" in t,
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
grep -rnE 'acceptance[ -]record' skills/conductor/SKILL.md skills/slainte/SKILL.md skills/switch/SKILL.md | wc -l && \
grep -n 'seven-rung ladder (frame → viability → scope → design → handoff → loop → acceptance)' README.md | wc -l && \
grep -rn '\bhandoff\b' skills/ | grep -v 'session handoff\|work handoff\|session-handoff\|'\''handoff'\''' | wc -l
```

Expected: `release: clean`, `1`, `2`, `0`, `5`, `1`, `0`.

**Corrected 2026-08-25 by callback (see Step 16).** This assertion previously
read `grep -rn 'acceptance record' …` and expected `≥5`. D7's table specifies
slainte's two edits in the HYPHENATED form `acceptance-record landing` —
correct English, a compound adjective, mirroring the `goal-record landing` it
replaces — so applying D7 verbatim yields 3 space-form matches and 2
hyphen-form matches, and the old one-form check would have refused correct
work. The regex now counts both forms; the expected value is exactly `5`.

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

---

### Step 11 — the board's last retired word: GOAL becomes PIECES

[delegate, model: sonnet, effort: medium]

**What.** Step 3 claimed "rung rows, glyphs, HTML all derive from `RUNGS`".
Two labels in `/Users/anthonymaley/Kerd/tools/diagram/progress_kit.py` do not —
they are hardcoded, and they say `GOAL`.

**The ruling, so no player has to guess it.** That section reports PIECES
COMPLETION: a strip of landed / in-flight / remaining boxes, one per numbered
piece, per slug. Under the seven-rung ladder that is the `acceptance` rung's
check, taken at the loop's exit. The visible label becomes **`PIECES`** — not
`ACCEPTANCE`, not `LOOP` — for three reasons: (i) the section counts pieces,
and the strip is per-piece, not per-rung; (ii) the board directly above it
already renders `loop` and `acceptance` as rung rows, so a section heading
reusing either word would name two different things on one page; (iii)
`Pieces` is already the live schema noun in three places the machine reads
(the `## Pieces` section, the `Piece: <slug>/<n>` commit trailer, and
`check_rung`'s `— section "Pieces"` texts), so it cannot go stale at the next
rename.

1. **The two visible labels.**
   - line 432 — `f"GOAL  {slug.ljust(slug_width)}  …"` becomes
     `f"PIECES  {slug.ljust(slug_width)}  …"`. The prefix field widens 4 → 6;
     the two-space separator is unchanged. Nothing shares a column with it —
     the BOARD grid above computes its own widths and the `SPIKE …` line has
     its own prefix — so no other line moves and no width needs preserving.
   - line 667 — `out.append("<h2>GOALS</h2>")` becomes
     `out.append("<h2>PIECES</h2>")`.
2. **The model key and the CSS classes change too, and the reason is not
   tidiness.** `render_html` inlines the whole model as
   `<script type="application/json" id="progress-data">`, and writes
   `class="goal"` into the same page. So `"goals"`, `.goal` and `.goal-head`
   are all EMITTED strings living in `docs/plans/progress.html`, a committed
   surface `progress.py stale` byte-compares on every push. D1's writer rule —
   *the WRITER only ever emits live names* — binds them exactly as it binds a
   stage value. They are not internals; "not user-visible" is false for them.
   - `model["goals"]` → `model["piece_strips"]`: `derive`'s return dict and
     docstring (line ~249), the `drift` loop over it, `render_table`,
     `render_svg`, `render_html`.
   - the CSS block (lines 581–592) and its emitters: `.goal` →
     `.piece-strip`, `.goal-head` → `.piece-strip-head`, `.goal .detail` →
     `.piece-strip .detail`, `.goal.open .detail` →
     `.piece-strip.open .detail`; `<div class="goal">` (line 670) and
     `<div class="goal-head">` (line 671) follow; `_JS`'s selector
     `'.goal-head'` → `'.piece-strip-head'`.
   - `goal_for(root, slug, evidence)` → `piece_strip_for(…)`, plus its call
     site in `derive`. This one IS a true internal and changes for a weaker,
     stated reason: a reader of this module should not have to learn a retired
     ladder word to follow it, and two vocabularies inside one file is the
     defect this item exists to remove. Keep the docstring's `A1` / `A5`
     section citations verbatim — only the word `goals` inside them changes.
   - fixture helpers: `_goal(model, slug=_ST_SLUG)` → `_piece_strip(…)` and
     every call site; `_piece(goal, n)`'s parameter `goal` → `strip`.
3. **Prose inside the file.** The docstrings and block comments saying "goal
   strip", "goals entry", "BOARD/GOAL" (lines ~154, ~249, ~337–340, ~447,
   ~524, ~599) become "piece strip" / "piece-strips entry" / "BOARD/PIECES".
   Any `goal` in a non-ladder sense stays.
4. **Two living design docs Step 8's list missed.** Both describe this section
   by its old name and both go stale otherwise; D7's living-docs rule applies
   to them unchanged. `docs/design/progress-html.md` lines 12–13, 31, 64, 66
   ("every goal strip", "click any goal", "across all goals", "**Goal
   strips:** one row per goal", "Click a goal → detail panel") and
   `docs/design/progress-view.md` lines 17 and 54 ("this goal's work order as
   a strip", "**Goal view**"). Rename the section; leave every table cell,
   section ID and historical sentence alone.
5. **Render nothing here.** `progress.py stale` goes red the moment this
   lands and stays red until Step 10 re-renders the trio. That is correct and
   expected — Step 10 owns the render commit, and a trio rendered now can
   never match after the work commit.

**Why.** Step 3's own claim was that the renderer derives from `RUNGS` and
adapts by itself. Two hardcoded literals falsified it, and both said a word
that no longer names anything — one of them inside `<h2>`, on the page whose
whole job is answering "where are we?". The model key matters for a separate
reason worth stating plainly: it is written into a committed file, so leaving
it makes the board a writer that emits a retired name at every render, which
is a synonym by D1's definition, not a naming preference.

**Verify:**

```
cd /Users/anthonymaley/Kerd
grep -n 'GOAL\|"goals"\|goal_for\|goal-head\|class="goal"\|goal strip' tools/diagram/progress_kit.py ; echo "retired-in-kit=$?"
grep -rn -i 'goal strip\|goal view\|any goal\|all goals\|one row per goal' docs/design/progress-html.md docs/design/progress-view.md ; echo "retired-in-docs=$?"
grep -c 'f"PIECES  {slug' tools/diagram/progress_kit.py
grep -c '<h2>PIECES</h2>' tools/diagram/progress_kit.py
python3 tools/diagram/progress.py selftest ; echo "selftest-exit=$?"
python3 -c 'import sys; sys.path.insert(0,"tools/diagram"); import progress_kit as pk; m=pk.derive(pk.REPO); h=pk.render_html(m); print("key-new",("piece_strips" in m),"key-old",("goals" in m)); print("h2",h.count("<h2>PIECES</h2>"),h.count("<h2>GOALS</h2>")); print("css",h.count("piece-strip-head"),h.count("goal-head"))'
```

Expected: `retired-in-kit=1` and `retired-in-docs=1` — **both greps print
nothing and exit 1, and exit 1 IS the passing case for a purity grep.** That
is why these lines are newline-separated and not `&&`-chained: an `&&` chain
truncates silently at the first passing purity check. Then `1`, `1`,
`selftest: 15 ok`, `selftest-exit=0`, then `key-new True key-old False`,
`h2 1 0`, and `css` with a first number ≥ 2 (the CSS rule, the JS selector,
one per slug) and a second number of exactly `0`.

---

### Step 12 — the split literal, and a check that can actually see one

[delegate, model: sonnet, effort: low]

**What.**

1. **`/Users/anthonymaley/Kerd/tools/diagram/gen_flow_celtic_example.py`,
   step 9** — the only step in the file still labelled with a retired rung.
   Steps 4, 7, 8 and 10 already read `SCOPE`, `HANDOFF`, `LOOP`, `SHIPPED`.
   - line 161, the step label: `"GOAL\nGATE"` → `"ACCEPTANCE\nGATE"`.
   - line 161, the step title: `"Prove the whole · Goal gate"` →
     `"Prove the whole · Acceptance gate"`.
   - line 160, the section comment `# ── 9 — goal gate ──…` →
     `# ── 9 — acceptance gate ──…`, keeping the rule's total line width.
2. **`/Users/anthonymaley/Kerd/tools/diagram/gen_flow_handoff.py:93`** — the
   step title `"→ Execute a unit  (BUILD)"` → `"→ Execute a unit  (LOOP)"`.
   Same class, one token: a parenthesised rung name in a step title, naming
   the rung that is now `loop`. Step 5 edited this file for
   `CONTRACT → HANDOFF` and left the fold half; this is that half.
3. **What deliberately does NOT change in these two files.** The narrative
   prose inside step bodies and artifact callouts — `"GOAL ACHIEVED"` (celtic
   line 168, handoff line 98), `"goal achieved"` (celtic line 171),
   `"CONTRACT governs everything downstream"` (handoff line 95) — is the
   WALK's own report vocabulary as agreed on 2026-08-03/04, the same latitude
   D5 grants `contract spec` and D8 grants a dated record. Only the RUNG-NAME
   positions move. A player that helpfully sweeps the prose has drifted, and
   Step 9's review hands it back.
4. **RUN NOTHING.** Both generators write DATED records —
   `docs/plans/2026-08-04-celtic-example-flow.excalidraw/.svg` and
   `docs/plans/2026-08-03-write-the-contract-flow.excalidraw/.svg`. Executing
   either overwrites a dated record, which D8 forbids; celtic's script
   additionally merges preserved annotations from
   `docs/plans/annotations/` and re-marks blue deltas, so a stray run also
   rewrites review state. Edit the source. Never execute it.
5. **The purity check that catches split literals**, below, added by this step
   and re-run by Step 10. Why it is needed: `"GOAL\nGATE"` is ONE string
   literal carrying an embedded newline, so `grep -rn 'GOAL GATE'` finds
   nothing, `grep -rn 'GOAL$'` finds nothing, and Step 9's purity bullet reads
   straight past it. The check unsplits `\n` and `\t` escapes back to spaces
   BEFORE matching, then looks only where a word IS a rung name: the
   `f.step(…)` label argument, an `("KEY", [` section key, and the
   `Flow("TITLE"` heading. It names its two deferred files out loud on every
   run, so the deferral can never go silent.

**Why.** The whole callback traces to one shape: the fold half of the rename
was enumerated by file and line and never closed by a grep, and the one site
that most needed a grep was the one no grep could reach. A purity check that
matches source text as written can only ever find the misses that were
already easy to find. Unsplitting the escapes first is the difference between
a check and a comfort.

**Verify:**

```
python3 - <<'EOF'
import glob, os, re, sys

RETIRED  = re.compile(r'\b(SLICE|CONTRACT|BUILD|GOAL)S?\b')
LABEL_RE = re.compile(r'f\.step\(\s*"[^"]*"\s*,\s*"([^"]*)"')
KEY_RE   = re.compile(r'^\s*\(\s*"([A-Z][A-Z0-9 +/&-]*)"\s*,\s*\[')
TITLE_RE = re.compile(r'Flow\(\s*"([^"]*)"')
# Deferred by producer ruling, 2026-08-25 — the editorial fold, not a
# one-for-one swap. Named here so the deferral can never go silent.
DEFERRED = {"gen_flow_build.py", "gen_functions.py"}

hits, deferred = [], []
for path in sorted(glob.glob("tools/diagram/*.py")):
    raw  = open(path, encoding="utf-8").read()
    flat = raw.replace("\\n", " ").replace("\\t", " ")   # unsplit the literals
    for i, line in enumerate(flat.splitlines(), 1):
        for rx in (LABEL_RE, KEY_RE, TITLE_RE):
            for m in rx.finditer(line):
                if RETIRED.search(m.group(1)):
                    row = f"{path}:{i}: {m.group(1)!r}"
                    (deferred if os.path.basename(path) in DEFERRED
                     else hits).append(row)

for d in deferred: print("deferred", d)
for h in hits:     print("HIT     ", h)
print(f"rung-name purity: {len(hits)} hit(s), {len(deferred)} deferred")
sys.exit(1 if hits else 0)
EOF
echo "purity-exit=$?"
grep -n '(BUILD)\|GOAL.nGATE\|Goal gate' tools/diagram/gen_flow_celtic_example.py tools/diagram/gen_flow_handoff.py ; echo "retired-labels=$?"
git status --porcelain docs/plans/ | grep '2026-' ; echo "dated-untouched=$?"
```

Expected: exactly four `deferred` lines —
`tools/diagram/gen_flow_build.py:18: 'BUILD — stage flow'`,
`gen_flow_build.py:36: 'BUILD + MEASURE'`, `gen_functions.py:54: 'BUILD'`,
`gen_functions.py:646: 'BUILD'` — **no `HIT` line at all**,
`rung-name purity: 0 hit(s), 4 deferred`, and `purity-exit=0`. Then
`retired-labels=1` and `dated-untouched=1`: both greps print nothing, and for
a purity grep exit 1 is the pass, which is why these are newline-separated
and never `&&`-chained. Measured before the edit, the same script prints
`HIT tools/diagram/gen_flow_celtic_example.py:161: 'GOAL GATE'` and exits 1 —
run it first if you want to watch it catch the literal no grep can find.

---

### Step 13 — the root README's current-architecture prose

[delegate, model: sonnet, effort: medium]

**What.** D7 named `README.md:7` and then said "sections describing CURRENT
behavior update their vocabulary" without enumerating them. Step 7 applied the
enumerated swaps; four sites remain where the project's front page asserts the
CURRENT architecture in retired words. None of these is version-history
narration and the README's shorthand latitude does not reach them: each one
states what the machine does today.

| Line | Now | Becomes |
|---|---|---|
| 62 | "…the contract and build rungs require them where they are" | "…the handoff and loop rungs require them where they are" |
| 268 | "a `## Release slice` without its `Rigor level:` line" | "a `## Scope` without its `Rigor level:` line" |
| 301 | "CONTEXT.md being pruned at goal landings" · "a shorter CONTEXT.md at the next goal landing" | "…pruned at acceptance-record landings" · "…at the next acceptance-record landing" |
| 303 | "every piece of work is a slug climbing frame → viability → slice → design → contract → build → goal → loop" | "every piece of work is a slug climbing frame → viability → scope → design → handoff → loop → acceptance" |

Two of these need their reasoning stated, because both sit inside history
entries and a careful player will hesitate:

- **Line 62** lives in the `### v0.87.0` entry, but its claim is present tense
  about machinery running today — it is the reason nothing archives specs, and
  a reader who greps `contract rung` finds no such rung. Version-history
  narration is a statement ABOUT a past release; this is a statement about the
  current gates that happens to live in a history entry. It swaps.
- **Line 301** sits in a paragraph that is genuinely history ("Until v0.90.0
  you could run…"), but both `goal landing` phrases name the licensed pruning
  event switch enforces RIGHT NOW, and Step 7 has already renamed that event
  inside `skills/switch/SKILL.md`. Leaving the README's name for it makes two
  living documents disagree about when pruning is allowed. Use the hyphenated
  compound-adjective form `acceptance-record landing`, matching what Step 7
  wrote into slainte.

**Then re-sweep the whole file, not just these four.** Run the closing grep in
the Verify block and read every remaining hit in context. The legitimate
survivors, all of which STAY: `contract` as the artifact ("a contract with
numbered pieces", "No contract, no trailer" — D5); `slice` as an increment
noun ("writing a slice well", "the smallest valuable slice", "This slice
captures honest actuals", "the next slice"); `build`/`building` as a verb;
`goal` as an aim ("The goal is prose that reads like a first draft…"); and the
counts "eight funnel stages" (past tense) and "eight CI steps" (unrelated).
Anything outside that list is a miss and is fixed here.

**Why.** Line 303 is the load-bearing one. It is the README's own definition
of the ladder, spelled out at full length, eight rungs long, under a heading
that says "The layers" — and it contradicts line 7 on the same page. A front
page that defines the ladder twice, differently, is the synonym defect at its
most public. D7 missed it because D7 enumerated the ladder sentence it knew
about; line 303 spells the same ladder with a different lead-in, which is
exactly the class of miss a closing grep exists to catch and D7 wrote no
closing grep outside `skills/`.

**Verify:**

```
cd /Users/anthonymaley/Kerd
grep -c 'frame → viability → scope → design → handoff → loop → acceptance' README.md
grep -nE 'slice → design|→ contract →|→ build → goal|eight-rung' README.md ; echo "old-ladder=$?"
grep -nE '## Release slice|contract and build rungs|goal landing' README.md ; echo "old-current-prose=$?"
grep -c 'acceptance-record landing' README.md
grep -nE '\b(sliced|contracted|building|Release slice|Done condition)\b' README.md ; echo "retired-stages=$?"
python3 tools/gates/gate.py release
```

Expected: `2` — line 7 and line 303 now spell the ladder identically, word for
word. Then `old-ladder=1` and `old-current-prose=1` (nothing printed; exit 1
is the pass for a purity grep, which is why every line here is
newline-separated rather than `&&`-chained). Then `2` for the two pruning-event
mentions on line 301, `retired-stages=1`, and `release: clean`.

---

### Step 14 — reseal the rung-vocabulary view whose file path went dead

[keep]

**What.** `docs/design/rung-vocabulary/rungs-and-artifacts.html:152` reads
`FILENAME (gen_flow_contract.py),`. Step 5 renamed that generator to
`gen_flow_handoff.py`, so a sealed, producer-approved view now makes a false
claim about a file that does not exist. Producer ruling, 2026-08-25, verbatim:

> A sealed view can remain visually approved, but it cannot remain factually
> false about a living file path after the slice lands. Step 9 should either
> require resealing that view or add an explicit correction annotation in the
> design doc that supersedes the dead-file claim. I'd prefer reseal, because
> it's a living design artifact for this item, not a dated historical record.

Reseal. In this exact order — the order is the countermeasure, and step 3 is
where this has already gone wrong once.

1. **Correct the one token.** Line 152 becomes
   `FILENAME (gen_flow_handoff.py),`. That is 31 characters against the
   original's 32, inside a 288px panel at 12.5px sans where a 34-character
   sibling (line 162, `drops "done" for ready-to-release.`) already fits — so
   no reflow, no re-layout, no other line moves. **Change nothing else in the
   file.** The `<desc>` on line 25 says "a generator FILENAME … and in a flow
   diagram" without naming the file and stays verbatim; lines 77, 100, 111,
   129, 138, 141, 143, 147, 156 and 160 are the panel's deliberate
   before/after annotations documenting the rename (`was slice`, `was
   contract`, `was build + goal`, `7 old -goal.md … read forever`) and are
   correct as written.
2. **Downgrade the seal to its hand-written form. Do not compute a hash.** In
   `docs/product/rung-vocabulary.md`, the FIRST concerns entry's approval line

   ```
       approval: Tony, 2026-08-25 · fp:8daab36a9d76
   ```

   becomes

   ```
       approval: Tony, 2026-08-25
   ```

   Leave the second entry (`the-ladder.html`, `fp:e2e788033798`) untouched —
   that view is unedited and its seal is still valid.
3. **Let the machine take the fingerprint.**

   ```
   python3 tools/gates/gate.py seal rung-vocabulary
   ```

   `seal_views` opens the view, reads its CONTENT, computes the value and
   writes it back into the approval line. **Never compute this by hand.**
   Measured 2026-08-25: `view_fingerprint` takes file CONTENT, not a path —
   handed the string `docs/design/rung-vocabulary/rungs-and-artifacts.html` it
   returns `3447c8ae6587`, a perfectly plausible twelve-hex value that is
   silently wrong, and the only thing that caught it was the gate refusing.
   There is one implementation, `tools/reqview/fingerprint.py`, and routing
   through `gate.py seal` makes the mistake structurally impossible because
   that command never accepts a path in that position. This is also why step 2
   exists: `seal_views` completes an UNSEALED approval and REFUSES to rewrite
   a diverged one, so the line must be downgraded first — `seal` will not
   overwrite `fp:8daab36a9d76` for you, by design.
4. **Re-render the PNG** at the dimensions the committed one already carries,
   1100 × 1140 (read with `python3 -c` off the PNG header, not guessed):

   ```
   shasum docs/design/rung-vocabulary/rungs-and-artifacts.png
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless --disable-gpu --hide-scrollbars \
     --screenshot=/Users/anthonymaley/Kerd/docs/design/rung-vocabulary/rungs-and-artifacts.png \
     --window-size=1100,1140 \
     file:///Users/anthonymaley/Kerd/docs/design/rung-vocabulary/rungs-and-artifacts.html
   shasum docs/design/rung-vocabulary/rungs-and-artifacts.png
   ```

5. **Prove the PNG actually changed before trusting anything you see in it.**
   Second measured gotcha, 2026-08-25: re-reading a PNG immediately after
   re-rendering can return the CACHED previous image, at an identical byte
   count. Compare the two `shasum` values from step 4 — a byte count is not
   evidence, and neither is a file size. If the hash is unchanged the render
   did not happen: re-run it, and do not proceed.
6. **Look at the corrected panel.** This is why the step is `[keep]`. What
   step 3 writes is a claim that Tony approved this content, and the machine
   cannot tell a one-token factual correction made under his standing ruling
   from a redrawn diagram. His ruling authorises the reseal of THIS
   correction; it does not authorise whatever else the render might show. Open
   the re-rendered PNG, confirm the bottom-middle panel reads
   `FILENAME (gen_flow_handoff.py),` with no reflow and nothing clipped, and
   confirm the rest of the drawing is unchanged in content from what he
   approved. If anything else moved, stop and hand it back. Do not reseal a
   drawing the producer has not seen.

**Why.** A fingerprint is not bookkeeping — it IS the approval, and it exists
precisely so that a changed drawing loses its key. That is the tension this
step lives inside, and it is worth naming rather than smoothing over: the
producer's ruling says correct the file, the machinery says a corrected file
is no longer approved, and both are right. The resolution is not to bypass the
machine but to route through it — downgrade, let `seal` recompute from
content, and put a human eye on the render before the key goes back on. AU9
holds the line either way: leave the seal stale and `gate.py audit` refuses the
whole push, which is the gate doing its job, not an obstacle to route around.

**Verify:**

```
cd /Users/anthonymaley/Kerd
grep -c 'gen_flow_contract' docs/design/rung-vocabulary/rungs-and-artifacts.html ; echo "dead-path=$?"
grep -c 'gen_flow_handoff.py' docs/design/rung-vocabulary/rungs-and-artifacts.html
grep -n 'approval: Tony' docs/product/rung-vocabulary.md
python3 -c 'import sys; sys.path.insert(0,"tools/reqview"); from fingerprint import view_fingerprint; print("live fp:", view_fingerprint(open("docs/design/rung-vocabulary/rungs-and-artifacts.html",encoding="utf-8").read()))'
python3 tools/gates/gate.py audit
python3 tools/gates/gate.py route rung-vocabulary | grep '^enters at:'
git status --porcelain docs/design/rung-vocabulary/ docs/product/rung-vocabulary.md
```

Expected: `0` printed with `dead-path=1` (a `grep -c` returning zero exits 1 —
the passing case, and the reason these lines are newline-separated); then `1`;
then two `approval: Tony, 2026-08-25 · fp:…` lines where the FIRST carries a
fingerprint that is **neither `8daab36a9d76` nor `3447c8ae6587`** and the
second is still `e2e788033798`; then a `live fp:` value EQUAL to the first
approval line's; then `audit: clean` — a mismatched seal is an AU9 problem, so
a clean audit is the proof the reseal took, not an incidental pass; then
`enters at: loop`, unchanged (the reseal must not move this item on the
board — the six new unchecked pieces keep it at the loop's entry); then
exactly three modified paths: `rungs-and-artifacts.html`,
`rungs-and-artifacts.png`, `docs/product/rung-vocabulary.md`.

---

### Step 15 — the deferrals, recorded and not fixed

[keep]

**What.** Three findings this callback surfaced are deliberately NOT repaired
in slice 1. This step's entire job is to prove they were left byte-identical
on purpose, and to hand their Backlog rows to the close-out.

**(a) `docs/design/gate-visuals/visual-lifecycle.html:28` — outside this
slice's authority.** Its `<desc>` says *"At the goal gate it is redrawn from
what was built"*, naming a rung that no longer exists. It is not repaired
here, for three reasons, and the third is the one that decides it.

1. **It belongs to another work item.** The file is a view of `gate-visuals`,
   sealed in `docs/product/gate-visuals.md` at `fp:3ef85a6441d5`, approved by
   Tony 2026-08-22. `gate-visuals` currently routes to
   `enters at: acceptance` — it is sitting at its own producer gate. Re-keying
   its concerns block now mutates the evidence its acceptance is about to be
   judged on, under a different slug's authority.
2. **The machinery forces the reseal, so "just fix the sentence" is not
   available.** Editing the HTML changes its fingerprint; a diverged seal is
   an AU9 problem; AU9 is part of `gate.py audit`; and `audit: clean` is
   asserted in Steps 2, 8 and 10. Editing without resealing turns the whole
   atomic push red. Editing WITH a reseal lands another item's producer
   approval inside a `Piece: rung-vocabulary/<n>` trailer.
3. **Its falsehood is a different kind, and the producer's ruling is scoped to
   the kind.** His words are "cannot remain factually false about a *living
   file path*". `gen_flow_contract.py` was a dangling reference — a path that
   resolves to nothing on disk. "At the goal gate" is stale VOCABULARY for a
   check that still exists and still runs, now at the rung named `acceptance`;
   and per D1 `goal` is a legal read alias forever, so nothing is broken by
   it. Stale vocabulary inside another item's sealed view is that item's
   business.

   **What it owes instead:** a Backlog row, carried into `gate-visuals`' own
   acceptance gate, where its producer key and its reseal both already live.

**(b) `docs/design/diagram-types-by-rung.md` — the EDITORIAL half is ruled out
of slice 1 by the producer, 2026-08-25.** Read the file's current state before
touching it: Step 8 has already applied the SUBSTITUTION half correctly —
every `slice` → `scope` and `contract` → `handoff` tag in the type table, and
the `### SLICE` and `### CONTRACT` section headings. What is deliberately left
is the FOLD half, and it is left in a visible half-state that this step must
NOT tidy:

- The three by-rung section headings `### BUILD — mostly nothing`,
  `### GOAL — did it meet what was declared` and `### LOOP — what we learned,
  and what comes next` are still separate. Merging them means merging two
  prose bodies and re-deciding heading order — editorial, ruled out.
- Six type tags now read `USE · acceptance` or `USE · loop, acceptance`
  (**bar**, **fishbone**, **line**, **loop**, **scatter**, **timeline**) while
  still sitting under the old headings, and **fishbone** and **loop** were
  mapped old-`loop` → `acceptance` on a wrong reading of D4. Every one of them
  uses a LIVE rung name, so no retired name ships and nothing is urgent — but
  the tags and the headings now disagree, and line 152's *"The rung's own
  name"* is true against its `### LOOP` heading and false against its
  `acceptance` tag. Resolving that is the same editorial pass.

Nothing further is edited here. The half-state is the record of what was
ruled out, and the Backlog row below is what closes it.

**(c) `tools/diagram/gen_flow_build.py`, and `gen_functions.py`'s two
`("BUILD", [` section keys** — the same editorial-fold shape as (b), not a
one-for-one swap: each `BUILD` section holds two entries ("Build a piece ·
Prove it" and "Prove the whole · Goal gate") that split across `loop`'s
interior and `acceptance` under the fold, and `gen_flow_build.py` is
additionally a whole file named for a retired rung. Step 12's purity check
prints both files as `deferred` on every run, so this deferral is re-announced
rather than forgotten.

**The three Backlog rows, verbatim, handed to the close-out — NOT written by
this step.** `TODO.md` is switch's file (this spec's "What does not land"), so
these do not go in the work commit; the conductor carries them into the
session-state commit at the boundary:

> - **`gate-visuals`' `visual-lifecycle.html` still says "At the goal gate".**
>   The sealed view (`fp:3ef85a6441d5`, Tony 2026-08-22) narrates a rung the
>   2026-08-25 rename folded into `loop` + `acceptance`. Correct the `<desc>`,
>   reseal and re-render the PNG at `gate-visuals`' own acceptance gate — not
>   from another slug's slice.
> - **`docs/design/diagram-types-by-rung.md` is still organised by the retired
>   rungs.** Slice 1 did the substitution half only. `### BUILD` and
>   `### GOAL` must merge into `### LOOP` with `### ACCEPTANCE` beside it,
>   heading order re-decided, line 152's quote "The rung's own name" re-checked
>   against the new names, and the six `USE · acceptance` type tags re-read
>   against their headings — **fishbone** and **loop** were mapped old-`loop` →
>   `acceptance`, which the fold makes wrong. Editorial; ruled out of
>   rung-vocabulary slice 1 on 2026-08-25.
> - **Two diagram generators still name the `build` rung.**
>   `tools/diagram/gen_flow_build.py` (filename, `Flow` title, step 2's label)
>   and `tools/diagram/gen_functions.py`'s two `("BUILD", [` section keys hold
>   entries that split across `loop` and `acceptance` under the fold — the
>   same editorial merge as the row above, not a swap. Step 12's purity check
>   prints both as `deferred` on every run.

**Why.** A deferral that is only a silence is indistinguishable from a miss,
and this whole callback exists because a fold was missed silently. Naming the
three, proving they are untouched by command, and re-announcing two of them
from inside a check that runs on every push is what turns "we did not do that"
into a record. The scope ruling on (a) matters beyond this slice: the
fingerprint mechanism draws work-item boundaries the way a lock draws a door,
and a slice that reaches through another item's seal because the fix looked
small is the failure that mechanism was built to prevent.

**Verify:**

```
cd /Users/anthonymaley/Kerd
git status --porcelain docs/design/gate-visuals/ tools/diagram/gen_flow_build.py | grep . ; echo "left-alone=$?"
grep -c 'At the goal gate' docs/design/gate-visuals/visual-lifecycle.html
grep -c 'fp:3ef85a6441d5' docs/product/gate-visuals.md
python3 tools/gates/gate.py route gate-visuals | grep '^enters at:'
grep -nE '^### (BUILD|GOAL|LOOP|ACCEPTANCE) ' docs/design/diagram-types-by-rung.md
grep -cE '\| \*\*(bar|fishbone|line|loop|scatter|timeline)\*\* \| USE · ' docs/design/diagram-types-by-rung.md
grep -nE '\b(slice|sliced|contracted|building)\b|USE · (slice|contract|goal)' docs/design/diagram-types-by-rung.md ; echo "no-retired-name-ships=$?"
grep -c '("BUILD", \[' tools/diagram/gen_functions.py
python3 tools/gates/gate.py audit
grep -cE 'visual-lifecycle|diagram-types-by-rung|gen_flow_build' TODO.md ; echo "rows-not-yet-written=$?"
```

Expected, line by line — note these are newline-separated and never
`&&`-chained, because three of them pass by printing nothing and exiting 1:

- `left-alone=1` — `git status` prints nothing for the gate-visuals view
  directory or `gen_flow_build.py`, and the pipe to `grep .` exits 1.
  **`docs/design/diagram-types-by-rung.md` and `tools/diagram/gen_functions.py`
  are NOT in this list, and that is deliberate**: both are legitimately
  modified, by Step 8 and Step 5 respectively, for the substitution half of
  the rename. Only the fold half is deferred in them, which the next four
  assertions check by content instead of by cleanliness.
- `1` — the false sentence is still in `visual-lifecycle.html`, on purpose.
- `1` — gate-visuals' seal untouched at `fp:3ef85a6441d5`.
- `enters at: acceptance` — gate-visuals unmoved on the board.
- exactly three heading lines: `### BUILD — mostly nothing`,
  `### GOAL — did it meet what was declared`, `### LOOP — what we learned, and
  what comes next`, and **no `### ACCEPTANCE`** — proof the editorial merge
  was not attempted.
- `6` — the six type tags carrying the fold's new names under the old
  headings, exactly as Step 8 left them.
- `no-retired-name-ships=1` — nothing printed: no retired STAGE value and no
  `USE · slice|contract|goal` tag survives. The deferral is a wrong reading in
  live words, never a retired word shipping.
- `2` — both `("BUILD", [` section keys still standing in `gen_functions.py`.
- `audit: clean` — the direct proof no other item's seal was disturbed.
- `0` with `rows-not-yet-written=1`. Note what is NOT asserted here: `TODO.md`
  is already modified in the working tree — the conductor tracks this build's
  dispatch waves in `## Now` — so "untouched" would be a false test. The
  assertion is that the three Backlog rows above have not been written YET.
  They belong to the session-state commit at the boundary, which switch owns,
  and Step 10's work commit names its files explicitly (`No git add -A`), so
  `TODO.md` cannot ride along into it.

---

### Step 16 — Step 7's check was wrong; re-run it corrected, and amend the assembly

[keep]

**What.**

1. **The defect, stated so it is not re-introduced.** Step 7's Verify
   asserted `grep -rn 'acceptance record' skills/conductor/SKILL.md
   skills/slainte/SKILL.md skills/switch/SKILL.md | wc -l` returning `≥5`. But
   D7's table specifies slainte's two edits in the HYPHENATED form
   `acceptance-record landing` — correct English, a compound adjective,
   mirroring the `goal-record landing` it replaces. Applying D7 verbatim
   therefore yields **3** space-form matches (`conductor/SKILL.md:375`,
   `switch/SKILL.md:30`, `switch/SKILL.md:68`) and **2** hyphen-form matches
   (`slainte/SKILL.md:3` frontmatter, `slainte/SKILL.md:18`) — measured
   2026-08-25. The one-form check would have refused correct work. **The work
   is right; the check was wrong.** Step 7's Verify block has been corrected
   in place by this callback: the grep now reads
   `grep -rnE 'acceptance[ -]record' …` and its expected value is exactly `5`,
   not `≥5`.
2. **Re-run Step 7's whole corrected Verify block against the landed tree**
   and confirm all seven assertions. Do NOT re-edit any skill file. If the
   corrected check fails, the defect is in the work and goes back to Step 7 —
   a check must never be adjusted twice to fit what is on disk, which is how a
   wrong check becomes a wrong standard.
3. **Amend the assembly for Step 10, which is not being rewritten.** Step 10
   was written when this spec had ten pieces; this callback makes it sixteen.
   When Step 10 runs: tick boxes **1–15** in `## Pieces` (piece 16 ticks with
   them — running Step 10 is the act), carry **sixteen** trailers
   `Piece: rung-vocabulary/1` … `Piece: rung-vocabulary/16` on the single work
   commit, and expect `route rung-vocabulary` → `enters at: acceptance`
   exactly as Step 10 says. Everything else in Step 10 — the suite order, the
   two-commit split, the single push, the `stale` reasoning — is unchanged.
4. **Amend Step 9's scope the same way.** Step 9 reviews the working-tree
   diff, so it must run AFTER Steps 11–16 and before Step 10, covering
   pieces 1–8 and 11–15. Its board-delta table is unchanged by this callback:
   none of Steps 11–16 edits a `docs/product/*.md` section or stage, and
   Step 14's reseal is asserted not to move `rung-vocabulary` off `loop`. Add
   two bullets to its immutability check: `git status --porcelain
   docs/design/gate-visuals/ docs/design/diagram-types-by-rung.md` is EMPTY,
   and the only modified files under `docs/design/rung-vocabulary/` are the
   one `.html` and its `.png`.

**Why.** A verify block is the only thing standing between a delegated step
and an unearned "done", so a wrong one is worse than a missing one: it fails
correct work, and the cheapest way out of a red check is to change the work
until the check goes green. Correcting it here — with the measurement written
down and the count pinned to exactly `5` rather than a floor — closes that
door. Items 3 and 4 exist because this callback changed the shape of an
assembly that two kept steps hardcode, and the honest place to say so is a new
passage rather than a quiet edit to a step the conductor has already read.

**Verify:**

```
cd /Users/anthonymaley/Kerd
grep -c 'acceptance record' skills/conductor/SKILL.md skills/slainte/SKILL.md skills/switch/SKILL.md
grep -c 'acceptance-record' skills/conductor/SKILL.md skills/slainte/SKILL.md skills/switch/SKILL.md
grep -rnE 'acceptance[ -]record' skills/conductor/SKILL.md skills/slainte/SKILL.md skills/switch/SKILL.md | wc -l
grep -c '^### Step ' docs/plans/2026-08-25-rung-vocabulary-spec.md
grep -c '^- \[ \] 1[1-6]\.' docs/plans/2026-08-25-rung-vocabulary-spec.md
python3 tools/gates/gate.py release
python3 tools/gates/gate.py route rung-vocabulary | grep '^enters at:'
```

Expected: first grep prints `skills/conductor/SKILL.md:1`,
`skills/slainte/SKILL.md:0`, `skills/switch/SKILL.md:2` (3 lines total);
second prints `skills/conductor/SKILL.md:0`, `skills/slainte/SKILL.md:2`,
`skills/switch/SKILL.md:0` (2 lines total); the combined regex prints `5`;
`16` step headings; `6` unchecked pieces numbered 11–16; `release: clean`; and
`enters at: loop` — still the loop's entry, because sixteen boxes are still
unticked and Step 10 has not run yet.
