# Entry gates — the router and the first refuser

Given a work slug, runs the eight gates in series and routes work to the
LOWEST rung whose declared inputs all exist on disk. It is mechanical only:
files, front-matter values, named sections, a qualified risk-ledger table,
a checked-box count. It has no opinion on whether a VALUE claim is
convincing, a risk well-argued, or a design sound — that judgment belongs
to whoever writes the artifact and whoever reviews it. `tools/gates/` is
the ladder's first refuser: the first check in the repo that fires from
outside the model, in CI, on every push.

## Usage

    python3 tools/gates/gate.py route <slug> [--json]        # where work enters — always exit 0
    python3 tools/gates/gate.py check <slug> <rung> [--json] # the refuser — exit 0 pass / 1 refusal
    python3 tools/gates/gate.py audit [--json]                # repo-wide mechanical sweep — exit 0 clean / 1 problems
    python3 tools/gates/gate.py release [--json]              # release rules — exit 0 clean / 1 problems
    python3 tools/gates/gate.py selftest                      # fixture suite in a temp tree — exit 0 / 1

Exit codes: `0` pass/bypass/report, `1` refusal or audit problems, `2` bad
argv (prints the module's usage docstring). `route` is a render and never
refuses — `check`, `audit`, and `release` are the only three subcommands that can exit 1.

`route` prints one line per rung (`<rung>  pass` or `<rung>  need <n>`),
then `enters at: <rung>`, then — when there is a next rung — `missing for
<next-rung>:` followed by that rung's need lines. `--json` on any
subcommand dumps the same structured dict via `json.dumps` instead of the
text render; it is the same data either way, not a second code path.

## The gate table

Inputs are cumulative: rung N requires everything rungs above it require,
plus its own new rows. "Section" means a `## <Title>` heading (exact,
case-sensitive) with non-whitespace body before the next `## ` heading or
EOF, for work slug `S`:

| Rung | New inputs (all mechanical) |
|---|---|
| `frame` | nothing — always enterable |
| `viability` | `docs/product/<S>.md` exists · front matter with legal `route` + `stage` · section `Value` (the declared VALUE, impact in units) |
| `slice` | section `Risk ledger`: a pipe table whose header row is exactly `Risk \| Killer? \| Impact \| Likelihood \| Evidence \| State \| Countermeasure \| Review trigger`, ≥1 data row, and per row: `Evidence` non-empty · `State` one of the five legal values below · `Countermeasure` non-empty when `State` begins `countermeasure` · `Review trigger` non-empty when `State` begins `accepted` · no row in state `FATAL` |
| `design` | section `Release slice` in `docs/product/<S>.md` · the doc's `Rigor level:` law holds: exactly one legal `Rigor level: <spike\|mvp\|production-v1>` line inside that section and none elsewhere in the file (see Rigor level, below) |
| `contract` | `docs/design/<S>.md` exists · ≥1 file matching `docs/gates/*-<S>-design.md` (the design GO record) |
| `build` | ≥1 file matching `docs/plans/*-<S>-spec.md` (latest by filename is THE contract) · that spec has section `Pieces` with ≥1 line matching `^- \[[ x]\] ` · every `^### Step ` heading in it is followed, before the next `###`, by a line starting `**Verify:**` — lines inside ``` fenced code blocks are invisible to this parse (a step may quote headings without splitting itself) |
| `goal` | zero unchecked boxes (`- [ ] `) in the contract's `Pieces` section |
| `loop` | ≥1 file matching `docs/gates/*-<S>-goal.md` containing section `Done condition` · `.github/workflows/gate.yml` exists (the live refusal instance) |

`goal` uses the contract's checklist as the "every piece landed" proxy —
declared simplification, not the real signal. Git-derived landing (a
landed piece is a pushed commit) belongs to the progress view and will
cross-check this later; a checked box is the mechanical stand-in for now.

Risk-ledger `State` cells are normalized before checking: lowercase,
em-dash and `--` collapsed to `-`, whitespace collapsed, stripped. The
five legal normalized values are `countermeasure - permanent`,
`countermeasure - temporary`, `accepted`, `accepted unknown`, `fatal`.
`fatal` is a structurally legal cell value — the row still parses — but
its presence is itself a refusal, named separately from a merely-illegal
`State` value: `FATAL risk '<risk>' — record in What we ruled out; cannot
pass`.

Routing runs the rungs top → bottom. `enters_at` is the DEEPEST rung whose
inputs all exist — a rung's inputs are the prerequisites to *perform* that
rung, and each rung's outputs become the next rung's inputs. Missing
inputs push work UP the ladder, never through it. `frame` requires
nothing, so routing always lands somewhere: the router never says "can't
proceed".

## Front-matter schema

The canonical write-down — this README, not the dated spec it came from,
is now the standard.

YAML front matter: the first line of the file is exactly `---`, closed by
a line `---` within 30 lines, containing `key: value` lines. A leading
`---` with no closing fence, or no `key: value` line inside it, is NOT
front matter — it parses to nothing, the same as if it weren't there.

| Key | Values | Meaning |
|---|---|---|
| `route` | `new` \| `problem` \| `spike` | triage class. QUESTION never becomes work — it has no route. `spike` is the one licensed ladder bypass. |
| `stage` | `framed` \| `viable` \| `sliced` \| `designed` \| `contracted` \| `building` \| `done` | last completed rung, past-tense. |

Both keys travel together: front matter carrying either key must carry
both, with legal values — one without the other is incomplete and fails
the check. Front matter is required on `docs/product/*.md` and
`docs/gates/*.md`, optional elsewhere, and validated wherever present
(that "wherever" is AU4, below — it validates this rule against every
markdown file in `docs/`, not just the two required directories).

The six system design docs in `docs/design/` are the system's own specs,
not work climbing the ladder — they do NOT get retrofitted front matter.

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

## Refusals

`check` is the refuser. Passing prints one line:

    PASS <rung> — <slug>: <n> inputs on disk

Refusing prints the full have/need render, then the verdict:

    gate: design — <slug>
    have: docs/product/<slug>.md — file exists
    have: docs/product/<slug>.md — front matter route=new stage=viable
    have: docs/product/<slug>.md — section "Value"
    have: docs/product/<slug>.md — section "Risk ledger" (3 rows, all qualified)
    need: docs/product/<slug>.md — section "Release slice"
    REFUSED at design — <slug>: 1 missing
    enters at: slice

`route` never refuses — it is a report, not a gate, and always exits 0.
That asymmetry is deliberate: a work slug can always be told where it
currently belongs on the ladder; only an explicit `check` against a
specific rung can say no.

Refusals ride the existing role ladder — the human or model that owns the
slug reads the need lines and fixes the artifact. The gate has no
escalation machinery of its own: no notification, no retry, no ticket. It
states what is missing, in the same vocabulary the ladder already uses
(files, sections, front matter), and stops there.

## The spike bypass

If `docs/product/<S>.md` carries `route: spike`, the ladder does not
apply. The gate checks exactly one thing: section `Kill-or-keep` (the
declared kill-or-keep question) is non-empty.

- Present → pass (exit 0), message `SPIKE — ladder bypassed; output
  re-enters through the gates`.
- Missing → refusal naming it.

No rung beyond this is evaluated for a spike — not `viability`, not
`slice`, nothing. A spike's output is expected to re-enter the ladder
normally once it exists; the bypass only covers the spike itself.

## Audit

The repo-wide mechanical sweep — `gate.py audit` — is the day-one live
refusal surface: the six rules below run against the real tree on every
push, not just against a named slug.

| # | Rule |
|---|---|
| AU1 | `docs/design/*.md` filenames must NOT start `YYYY-MM-DD-` — living docs are undated. Runs against ten real files today. |
| AU2 | `docs/product/*.md`: undated filename · front matter required and legal · stage-vs-sections within the file: `framed`+ requires `Value`, `viable`+ requires `Risk ledger`, `sliced`+ requires `Release slice` — a stage claiming more progress than the file's sections show is a named problem. |
| AU3 | `docs/gates/*.md` filenames MUST match `^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*-(frame\|viability\|slice\|design\|contract\|build\|goal\|loop)\.md$`. |
| AU4 | Any `docs/**/*.md` whose front matter carries `route` or `stage`: both keys present, both values legal — this validates the front-matter schema against every file that opts into it, including dated spec files like this piece's own contract. |
| AU5 | `docs/product/*.md` carrying a `## Grounding` section: every `- ` list line must parse as `- <ref> — <why>` (split on the FIRST ` — `, the em-dash separator) and `<ref>` — a path or glob relative to the repo root — must resolve to ≥1 match on disk. Absent section = vacuous pass: declaring grounding is opting in. |
| AU6 | `docs/product/*.md`: exactly one legal `Rigor level: <spike\|mvp\|production-v1>` line INSIDE the `## Release slice` section — a line outside the section, a missing line, duplicate lines, or an illegal value is a named problem. No `## Release slice` section = vacuous pass. Lines inside ``` fenced code blocks are invisible (a quoted example is content, not a declaration). |

Nonexistent directories pass vacuously — a repo that hasn't grown
`docs/gates/` yet is not thereby in violation of its naming rule.
`docs/plans/` legacy content is not name-audited (mixed dated docs,
`annotations/`, `.reviewed/`); only AU4 touches it, and only for files
that carry `route`/`stage` at all.

Output is `audit: clean` (exit 0) or one `problem:` line per finding
followed by `audit: <n> problems` (exit 1).

## Release rules

The release sweep — `gate.py release` — enforces versioning and documentation
consistency before a skill or mode is published.

| # | Rule |
|---|---|
| R1 | the three version fields must be identical: `plugin.json` `version` · `marketplace.json` `metadata.version` · `marketplace.json` `plugins[0].version` |
| R2 | `plugin.json` `description` must be byte-identical to `marketplace.json` `plugins[0].description`. `metadata.description` is NEVER checked — it is intentionally a different shape (the marketplace one-liner). |
| R3 | living files must write Kerd slash-command references as `/kerd:<name>`, never bare `/<name>`. Skill names derive from `skills/<name>/SKILL.md` directories — no hardcoded list. |

R3 runs against the allowlist: `skills/**`, `modes/**`, `docs/design/*.md`,
top-level `docs/*.md`, and `CLAUDE.md`. Excluded: immutable dated records
(`docs/plans/`, `docs/gates/`, `kivna/`) never retroactively fail CI, and
`README.md` is exempt because its shorthand exception is human-adjudicated
(CLAUDE.md rule 5).

Output is `release: clean` (exit 0) or one `problem:` line per finding
followed by `release: <n> problems` (exit 1).

## CI

`.github/workflows/gate.yml` runs on every `push` and `pull_request`:

    name: entry-gate
    on: [push, pull_request]
    jobs:
      gate:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
            with:
              fetch-depth: 0
          - name: Gate selftest
            run: python3 tools/gates/gate.py selftest
          - name: Repo audit
            run: python3 tools/gates/gate.py audit
          - name: Release rules
            run: python3 tools/gates/gate.py release
          - name: Progress selftest
            run: python3 tools/diagram/progress.py selftest
          - name: Matrix selftest
            run: python3 tools/design/matrix.py selftest
          - name: Matrix audit
            run: python3 tools/design/matrix.py audit
          - name: Progress render current
            run: python3 tools/diagram/progress.py stale

No `setup-python` step — `ubuntu-latest` ships python3 and these tools
have zero dependencies. Seven things can fail the build; this tool owns
the first three: the fixture suite (`selftest`, exercising the 26 cases
against a temp tree), the real repo (`audit`, exercising AU1–AU6 against
the actual `docs/` tree), and the release sweep (`release`, enforcing
R1–R3 on plugin metadata and living files). The other four belong to the
progress and matrix tools (see their own READMEs). A dated file dropped into `docs/design/`, a malformed `docs/gates/`
record name, a bare `/<name>` reference in a living file, or a broken
selftest fails CI — a refusal that fires from outside the model, on
GitHub's infrastructure, not inside a session.

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

## Rigor level

Every `## Release slice` section must declare how rigorously its slice
is measured — one line, machine-checked:

    Rigor level: mvp

Grammar: the line starts at column 0 with `Rigor level:`; the value is
the rest of the line, whitespace-stripped, case-sensitive. The legal
set is `spike` · `mvp` · `production-v1` — `RIGOR_LEVELS` in `kit.py`
is the value the checker tests against; the refusal messages, the
fixtures that pin them, and this standard repeat the set as literal
text, so amending it means editing all of them in one commit — nothing
machine-checks those literals against `RIGOR_LEVELS`, so the drift risk
is named here rather than refused. The law is written once
(`rigor_problems`) and enforced at two call sites:

- **AU6** (above) sweeps every `docs/product/*.md`: exactly one legal
  line inside the `## Release slice` section; a `Rigor level:` line
  anywhere else, a missing line, duplicates, or an illegal value is a
  named problem. Fenced code blocks are invisible to the parse — a
  quoted example line is content, not a declaration.
- **The design rung** refuses work whose product doc violates the law,
  with one need row: `need: docs/product/<S>.md — Release slice
  declares a legal rigor level (Rigor level: spike|mvp|production-v1)`.

A doc with no `## Release slice` section passes vacuously — the
section's absence is already the design rung's own refusal, and the
rigor rule does not double-refuse it. The declared level is data for
later slices (the rigor catalog and per-class disposition tables);
this slice enforces only that the level question is asked and answered
legally.

## Progress view

The gate is a seam, not a renderer: `--json` on `route`, `check`, and
`audit` dumps the same structured dict the text output is built from, and
every `kit.py` function takes `root` as a plain parameter so it can be
imported directly rather than shelled out to. That is the interface the
progress view is expected to consume — have/need lists, `enters_at`,
audit problem lines — but this tool draws no view of its own; rendering
that data as a UI is out of scope here and belongs to the progress-view
piece.
