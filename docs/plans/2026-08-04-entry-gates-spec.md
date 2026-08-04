---
route: new
stage: contracted
---

# Entry gates — build spec (the score)

Contract for the piece `entry-gates`: the router and the system's first
refuser. A runnable tool in `tools/gates/` that, given a work slug, runs
the eight gates in series and routes work to the LOWEST rung whose
declared inputs all exist on disk — plus the first refusal wiring: a
minimal GitHub Actions workflow that blocks from outside the model,
live from day one.

Design source: `docs/design/entry-gates.md`. Sibling constraints:
`docs/design/risk-ledger.md`, `docs/design/progress-view.md`,
`docs/design/conductor-role.md`, standing decisions in `CONTEXT.md`.

Out of scope: progress-view rendering (the gate exposes `--json` as the
seam the view will consume; it draws no view), wider CI, the unattended
loop, anything outside this repo.

---

## Part A — definitions this spec settles

These are first write-downs. Nothing else in the repo defines them; after
this piece lands they are the standard.

### A1. Front-matter schema (canonical)

YAML front matter: first line of the file is exactly `---`, closed by a
line `---` within 30 lines, containing `key: value` lines. A leading
`---` with no closing fence or no `key: value` line is NOT front matter.

| Key | Values | Meaning |
|---|---|---|
| `route` | `new` \| `problem` \| `spike` | triage class. QUESTION never becomes work (no route). `spike` is the one licensed ladder bypass. |
| `stage` | `framed` \| `viable` \| `sliced` \| `designed` \| `contracted` \| `building` \| `done` | last completed rung, past-tense. |

Both keys required together: a front matter carrying either must carry
both, with legal values. Required on `docs/product/*.md` and
`docs/gates/*.md`; optional elsewhere; validated wherever present.
The six system design docs in `docs/design/` are the system's own specs,
not work in the ladder — they do NOT get retrofitted front matter.

### A2. Rung slugs (canonical, in ladder order, top → bottom)

`frame`, `viability`, `slice`, `design`, `contract`, `build`, `goal`,
`loop`. Gate-record filenames use these:
`docs/gates/<YYYY-MM-DD>-<slug>-<rung>.md`.

### A3. The gate table — concrete on-disk inputs per rung, for work slug S

Inputs are cumulative: rung N requires everything above it plus its own
rows. "Section" means a `## <Title>` heading (exact, case-sensitive)
with non-whitespace body before the next `## ` or EOF.

| Rung | New inputs (all mechanical) |
|---|---|
| `frame` | nothing — always enterable |
| `viability` | `docs/product/<S>.md` exists · front matter with legal `route` + `stage` · section `Value` (the declared VALUE, impact in units) |
| `slice` | section `Risk ledger` in `docs/product/<S>.md`: a pipe table whose header row is exactly `Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger`, ≥1 data row, and per row: `Evidence` non-empty · `State` one of the five (see A4) · `Countermeasure` non-empty when State begins `countermeasure` · `Review trigger` non-empty when State begins `accepted` · NO row in state `FATAL` (a FATAL row is itself a refusal: `FATAL risk '<risk>' — record in What we ruled out; cannot pass`) |
| `design` | section `Release slice` in `docs/product/<S>.md` |
| `contract` | `docs/design/<S>.md` exists · ≥1 file matching `docs/gates/*-<S>-design.md` (the design GO record) |
| `build` | ≥1 file matching `docs/plans/*-<S>-spec.md` (latest by name is THE contract) · that spec has section `Pieces` with ≥1 line matching `^- \[[ x]\] ` · every `^### Step ` heading in it is followed, before the next `###`, by a line starting `**Verify:**` (a piece carrying its own check) |
| `goal` | zero unchecked boxes (`- [ ] `) in the contract's `Pieces` section |
| `loop` | ≥1 file matching `docs/gates/*-<S>-goal.md` containing section `Done condition` · `.github/workflows/gate.yml` exists (the live refusal instance — no CI, no loop) |

Simplification, declared: `goal` uses the contract's checklist as the
"every piece landed" proxy. Git-derived landing (a landed piece is a
pushed commit) belongs to the progress view and will cross-check this
later; a checked box is the mechanical stand-in for now.

State normalization for the ledger `State` cell: lowercase, em-dash and
`--` → `-`, whitespace collapsed, stripped. Legal normalized values:
`countermeasure - permanent`, `countermeasure - temporary`, `accepted`,
`accepted unknown`, `fatal`.

### A4. The spike bypass

If `route: spike` in `docs/product/<S>.md`: the ladder does not apply.
The gate checks exactly one thing — section `Kill-or-keep` (the declared
kill-or-keep question) non-empty. Present → pass (exit 0) with message
`SPIKE — ladder bypassed; output re-enters through the gates`. Missing →
refusal naming it. No rung beyond this is evaluated for a spike.

### A5. Routing semantics

Run rungs top → bottom. `enters_at` = the DEEPEST rung whose inputs all
exist (inputs of rung N are the prerequisites to PERFORM rung N; each
rung's outputs are the next rung's inputs). Missing inputs push work UP
the ladder, never through. `frame` requires nothing, so routing always
lands somewhere — the router never says "can't proceed".

### A6. CLI shape

```
python3 tools/gates/gate.py route <slug> [--json]     # report: where work enters — always exit 0
python3 tools/gates/gate.py check <slug> <rung> [--json]  # the refuser — exit 0 pass / 1 refusal
python3 tools/gates/gate.py audit [--json]            # repo-wide mechanical sweep — exit 0 clean / 1 problems
python3 tools/gates/gate.py selftest                  # fixture suite in a temp tree — exit 0 / 1
```

Exit codes: 0 pass/bypass/report · 1 refusal or audit problems · 2 usage
(print module docstring). `route` is a render, never a refusal — `check`
and `audit` are the refusers.

Text output — line-based, never prose. `check` refusal:

```
gate: design — <slug>
have: docs/product/<slug>.md — file exists
have: docs/product/<slug>.md — front matter route=new stage=viable
have: docs/product/<slug>.md — section "Value"
have: docs/product/<slug>.md — section "Risk ledger" (3 rows, all qualified)
need: docs/product/<slug>.md — section "Release slice"
REFUSED at design — <slug>: 1 missing
enters at: slice
```

`check` pass: `PASS <rung> — <slug>: <n> inputs on disk`.
`route` output: one line per rung (`<rung>  pass` or `<rung>  need <n>`),
then `enters at: <rung>`, then `missing for <next-rung>:` followed by the
need lines for the next rung (the have/need render the progress view will
later consume). `--json` dumps the same structured dict via `json.dumps`.

### A7. Audit rules (the day-one live refusal surface)

| # | Rule |
|---|---|
| AU1 | `docs/design/*.md` filenames must NOT start `YYYY-MM-DD-` (living docs are undated) — runs against six real files today |
| AU2 | `docs/product/*.md`: undated filename · front matter required and legal · stage-vs-sections within-file: `framed`+ requires `Value`; `viable`+ requires `Risk ledger`; `sliced`+ requires `Release slice` (stage ahead of its artifacts is a named problem) |
| AU3 | `docs/gates/*.md` filenames MUST match `^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*-(frame|viability|slice|design|contract|build|goal|loop)\.md$` |
| AU4 | any `docs/**/*.md` whose front matter carries `route` or `stage`: both present, values legal (this validates this spec file itself) |

Nonexistent directories pass vacuously. `docs/plans/` legacy content is
not name-audited (mixed dated docs, `annotations/`, `.reviewed/`); only
AU4 touches it. Output: `audit: clean` or one `problem:` line each +
`audit: <n> problems`, exit 1.

### A8. Grounding-was-read — DEFERRED, explicitly

The gate's second job (check the function's declared grounding was READ)
is deferred to a later piece. Reason: it requires a machine-readable
grounding declaration per rung — which artifacts each function must have
read — and no artifact on disk carries that today (the function map's
grounding lives in the walk detail, not as data). Building it now would
invent the declaration shape ahead of its own design. Landing site
sketched for the later piece: a `grounding` field per rung in
`kit.GATES` (present, empty, commented) + dated read-receipt records on
the `tools/diagram/mark_reviewed.py` precedent (reading is an explicit
act, snapshotted). The README states this deferral.

---

## Part B — implementation shape

`tools/gates/` mirrors the `tools/diagram/` precedent: a `kit.py` with
the logic (importable — the progress view is the named future consumer),
thin CLI, README per tool dir. Stdlib only (`os, re, sys, json, glob,
tempfile`), python3, no pyyaml — the front-matter subset in A1 is parsed
by hand. Deterministic: no randomness, no timestamps in output. Repo
root: `ROOT = dirname(dirname(dirname(abspath(__file__))))`; every kit
function takes `root` as a parameter (selftest passes a temp tree, the
CLI passes `ROOT`).

### kit.py API (exact)

```python
RUNGS   = ["frame","viability","slice","design","contract","build","goal","loop"]
STAGES  = ["framed","viable","sliced","designed","contracted","building","done"]
ROUTES  = ["new","problem","spike"]
LEDGER_COLUMNS = ["Risk","Killer?","Impact","Likelihood","Evidence","State","Countermeasure","Review trigger"]

read_front_matter(path) -> dict | None    # A1 rules; None when absent/malformed-fence
find_section(text, title) -> str | None   # body under '## <title>'; None = heading absent; '' = empty body
parse_ledger(section_text) -> (rows, problems)  # rows: list of dicts keyed by LEDGER_COLUMNS; problems: strings per A3
check_rung(root, slug, rung) -> dict      # {"slug","rung","have":[str],"need":[str],"bypass":bool}
route(root, slug) -> dict                 # {"slug","enters_at","bypass","rungs":[{"rung","have","need"}],"missing_for_next":[str],"next":str|None}
audit(root) -> list[str]                  # problem lines, empty = clean
selftest() -> int                         # 0 all pass; prints "selftest: 12 cases passed"
```

`check_rung` evaluates the CUMULATIVE inputs (A3). Have/need item format:
`<relpath> — <what>` exactly as shown in A6.

### selftest — the 12 cases (fixtures built in a `tempfile.TemporaryDirectory`, slug `alpha`)

| # | Fixture state | Assert |
|---|---|---|
| T1 | empty tree | `route(...)["enters_at"] == "frame"` |
| T2 | empty tree | `check_rung(...,"viability")` need names `docs/product/alpha.md — file exists` |
| T3 | product doc, no front matter | viability need names front matter (route, stage) |
| T4 | front matter (`new`/`framed`) + `Value` section | enters_at == `viability` |
| T5 | + ledger, row 2 `Evidence` empty | check `slice` need contains `row 2` and `Evidence` |
| T6 | + ledger with a FATAL row | check `slice` need contains `FATAL` and the risk name |
| T7 | + qualified ledger (2 rows, no FATAL) | enters_at == `slice` |
| T8 | + `Release slice` → enters_at `design`; then + `docs/design/alpha.md` + `docs/gates/2026-01-01-alpha-design.md` → enters_at `contract` | both asserts |
| T9 | + `docs/plans/2026-01-02-alpha-spec.md` with `Pieces` (1 unchecked box) and `### Step 1` carrying `**Verify:**` → enters_at `build`; a variant spec whose Step lacks `**Verify:**` → check `build` refuses naming the step | both asserts |
| T10 | boxes all checked → enters_at `goal`; then + `docs/gates/2026-01-03-alpha-goal.md` with `Done condition` + `.github/workflows/gate.yml` → enters_at `loop` | both asserts |
| T11 | `route: spike`, no `Kill-or-keep` → refusal names it; with it → `bypass` True, need empty | both asserts |
| T12 | audit: dated file in `docs/design/` + bad `docs/gates/` filename + illegal `stage` value → exactly 3 problems; clean tree → 0 | both asserts |

### gate.py

`mark_reviewed.py` shape: shebang, module docstring = usage text,
`sys.path.insert` for kit import, argv dispatch to the four subcommands,
`--json` handled by dumping the kit dict. No logic in gate.py beyond
argv parsing and text rendering per A6.

### .github/workflows/gate.yml (exact content)

```yaml
name: entry-gate
on: [push, pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Gate selftest
        run: python3 tools/gates/gate.py selftest
      - name: Repo audit
        run: python3 tools/gates/gate.py audit
```

No setup-python (ubuntu-latest ships python3; zero-dependency tool).
Live from day one: selftest exercises real fixtures on every push, and
AU1 checks six real files in `docs/design/` today. A dated file dropped
into `docs/design/`, a malformed `docs/gates/` name, or a broken gate
fails the build — a refusal that fires from outside the model.

### tools/gates/README.md — required headings

`# Entry gates — the router and the first refuser` · `## Usage` ·
`## The gate table` (A3 rendered concretely) · `## Front-matter schema`
(A1 — the canonical write-down) · `## Refusals` (format + the
never-"can't proceed" rule + refusals ride the role ladder, the gate has
no escalation machinery) · `## The spike bypass` (A4) · `## Audit`
(A7) · `## CI` (gate.yml, what refuses today) · `## Deferred:
grounding-was-read` (A8 verbatim in substance) · `## Progress view`
(one paragraph: `--json` is the seam; the gate never draws a view).

---

## Steps

### Step 1: tools/gates/kit.py [delegate, model: sonnet, effort: high]
**What:** Create `/Users/anthonymaley/Kerd/tools/gates/kit.py` implementing Part B's API exactly: constants, `read_front_matter`, `find_section`, `parse_ledger`, `check_rung`, `route`, `audit`, `selftest` with the 12 cases as specified. Cumulative gate inputs per A3, spike per A4, routing per A5, audit per A7, state normalization per A3. Stdlib only. Module docstring: one paragraph — mechanical checks only (files, front matter, sections), no judgment inside the gate.
**Why:** All non-obvious choices are settled above: `goal` uses the checklist proxy (A3 note), spikes short-circuit (A4), `route` never refuses (A5), grounding deferred with an empty commented `grounding` slot per rung in the GATES data (A8). Do not add checks beyond the tables — thinness is the design.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 -c "import sys; sys.path.insert(0,'tools/gates'); import kit; sys.exit(kit.selftest())"` → prints `selftest: 12 cases passed`, exit 0.

### Step 2: tools/gates/gate.py [delegate, model: sonnet, effort: medium]
**What:** Create `/Users/anthonymaley/Kerd/tools/gates/gate.py` per Part B: docstring usage, argv dispatch (`route`, `check`, `audit`, `selftest`, `--json`), text rendering exactly per A6, exit codes 0/1/2.
**Why:** gate.py is presentation only — every decision lives in kit.py so the progress view can import kit without the CLI.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py route entry-gates` → selftest passes, `audit: clean`, route ends `enters at: frame` with `missing for viability:` naming `docs/product/entry-gates.md — file exists`; then `python3 tools/gates/gate.py check entry-gates viability; echo "exit=$?"` → `REFUSED at viability — entry-gates: 3 missing` and `exit=1`.

### Step 3: diff review against the gate table [keep, model: fable, effort: medium]
**What:** Conductor reads the Step 1–2 diff against A1–A7 line by line: every rung's checks present and none added, refusal strings match A6, no judgment calls (no heuristics, no content interpretation beyond the named string checks), `root` parameterized everywhere, selftest touches only its temp tree.
**Why:** Blast-radius review is a separate step by rule — the risky edit was still delegated because it verifies by command; this step catches spec drift the commands can't.
**Verify:** Checklist above fully ticked; any miss → re-dispatch the step, never patch in review.

### Step 4: tools/gates/README.md [delegate, model: sonnet, effort: medium]
**What:** Create `/Users/anthonymaley/Kerd/tools/gates/README.md` with the required headings and content named in Part B, in the `tools/diagram/README.md` register (what it does, usage, why the checks exist).
**Why:** This README is the canonical write-down of the front-matter schema and gate table — the first place the standard exists outside this dated spec.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 -c "import sys; sys.path.insert(0,'tools/gates'); import kit; t=open('tools/gates/README.md').read(); missing=[h for h in ['Usage','The gate table','Front-matter schema','Refusals','The spike bypass','Audit','CI','Deferred: grounding-was-read','Progress view'] if kit.find_section(t,h) in (None,'')]; print('missing:',missing); sys.exit(1 if missing else 0)"` → `missing: []`, exit 0.

### Step 5: .github/workflows/gate.yml [delegate, model: haiku, effort: low]
**What:** Create `/Users/anthonymaley/Kerd/.github/workflows/gate.yml` with the exact YAML in Part B, byte-for-byte.
**Why:** Minimal by design — wider CI is out of scope; this is the refusal instance only.
**Verify:** `cd /Users/anthonymaley/Kerd && python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && cat .github/workflows/gate.yml` → both commands exit 0, file matches the spec block. (The Actions run itself is confirmed at Step 8 — it cannot run pre-push.)

### Step 6: live-refusal demonstration [delegate, model: haiku, effort: low]
**What:** `cd /Users/anthonymaley/Kerd && touch docs/design/2099-01-01-canary.md && python3 tools/gates/gate.py audit; echo "exit=$?"; rm docs/design/2099-01-01-canary.md && python3 tools/gates/gate.py audit; echo "exit=$?"`
**Why:** A refusal that has never fired is not demonstrated. This proves the exact check CI will run refuses on this repo's real tree today.
**Verify:** Transcript shows a `problem:` line naming `2099-01-01-canary.md` with `exit=1`, then `audit: clean` with `exit=0`, and `git status` shows a clean tree afterward.

### Step 7: release checklist [delegate, model: sonnet, effort: low]
**What:** (a) Bump `0.68.0` → `0.69.0` in `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json` (`version`) and `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json` (`metadata.version` and `plugins[0].version`) — MINOR: new tool + CI. Do NOT touch the two capability-list `description` fields (repo-internal tooling, not a plugin capability). (b) Add a `## Entry gates (tools/gates/)` section to `/Users/anthonymaley/Kerd/README.md` after the existing tool/skill sections, matching their heading style: three short paragraphs — what it routes, the refusal property, the one-line usage block from A6. (c) Append to `/Users/anthonymaley/Kerd/docs/playbook.md` under its notes/gotchas area: `CI (entry-gate workflow) refuses dated filenames in docs/design/ and malformed docs/gates/ record names — the date split is now machine-enforced.`
**Why:** Release checklist precedes commit by standing rule; version in three places must stay in sync.
**Verify:** `cd /Users/anthonymaley/Kerd && grep -c '"0.69.0"' .claude-plugin/plugin.json .claude-plugin/marketplace.json && grep -n 'Entry gates' README.md docs/playbook.md` → counts 1 and 2, both greps hit.

### Step 8: commit, push, watch the first refusal go live [keep, model: fable, effort: low]
**What:** Single commit of all files, message `Entry gates: the router and the first refuser (tools/gates + CI)`, push to main, then `gh run watch` (or `gh run list --workflow=entry-gate`) until the first `entry-gate` run completes green.
**Why:** The workflow is only "added, not yet verified" until GitHub actually executes it — the first green run is the empirical retest that promotes the refusal instance to live.
**Verify:** `gh run list --workflow=entry-gate --limit 1` shows `completed` / `success` on the pushed SHA.
