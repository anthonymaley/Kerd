# Entry gates — the router and the first refuser

Given a work slug, runs the seven gates in series and routes work to the
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
    python3 tools/gates/gate.py seal <slug> [--json]         # complete hand-written view approvals with their fingerprint — exit 0 / 1
    python3 tools/gates/gate.py selftest                      # fixture suite in a temp tree — exit 0 / 1

Exit codes: `0` pass/bypass/report, `1` refusal or audit problems, `2` bad
argv (prints the module's usage docstring). `route` is a render and never
refuses — `check`, `audit`, `release` and `seal` are the only four subcommands that can exit 1.

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
| `viability` | `docs/product/<S>.md` exists · front matter with legal `route` + `stage` · section `Value` (the declared VALUE, impact in units) · section `Risk ledger` naming at least one killer risk (≥1 row with `Killer?` = yes, stripped and lowercased) — named only; no sizing, no evidence, no qualification. A FATAL row, an illegal `State`, or empty `Evidence` do not refuse here — full qualification is the `scope` rung's business. |
| `scope` | the qualified risk ledger: section `Risk ledger`: a pipe table whose header row is exactly `Risk \| Killer? \| Impact \| Likelihood \| Evidence \| State \| Countermeasure \| Review trigger`, ≥1 data row, and per row: `Evidence` non-empty · `State` one of the five legal values below · `Countermeasure` non-empty when `State` begins `countermeasure` · `Review trigger` non-empty when `State` begins `accepted` · no row in state `FATAL` · section `Scope` in `docs/product/<S>.md` · the doc's `Rigor level:` law holds: exactly one legal `Rigor level: <spike\|mvp\|production-v1>` line inside that section and none elsewhere in the file (see Rigor level, below) |
| `design` | when the front matter declares `concerns:` (see Views, below): every entry has a view path or `n/a — <reason>` · every view path ends `.html` and resolves on disk · every view carries a sealed approval `<name>, <date> · fp:<12 hex>` whose fingerprint matches the file's current content. A work item declaring no concerns passes design vacuously. |
| `handoff` | `docs/design/<S>.md` exists · ≥1 file matching `docs/gates/*-<S>-design.md` (the design GO record) |
| `loop` | ≥1 file matching `docs/plans/*-<S>-spec.md` (latest by filename is THE contract spec) · that spec has section `Pieces` with ≥1 line matching `^- \[[ x]\] ` · every `^### Step ` heading in it is followed, before the next `###`, by a line starting `**Verify:**` — lines inside ``` fenced code blocks are invisible to this parse (a step may quote headings without splitting itself). This is the loop's ENTRY — the machine checks at the container's edges, never inside it. |
| `acceptance` | zero unchecked boxes (`- [ ] `) in the contract spec's `Pieces` section. This is the loop's EXIT: zero unchecked boxes; evidence ready for producer review. |

`acceptance` uses the loop's contract-spec checklist as the "every piece
landed" proxy — declared simplification, not the real signal. Git-derived
landing (a landed piece is a pushed commit) belongs to the progress view
and will cross-check this later; a checked box is the mechanical stand-in
for now.

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

## Ready to release — the derived terminal

`route` reports `ready-to-release` when every rung's inputs already exist
AND the acceptance evidence is on disk: a gate record matching
`docs/gates/*-<S>-acceptance.md` carrying a non-empty `Release condition`
section (a legacy `*-<S>-goal.md` carrying `Done condition` reads forever
— see Retired names, below), plus `.github/workflows/gate.yml`.

`ready-to-release` is a route **verdict**, never a rung: it is derived,
never declared. `check` takes live rung names only (`gate.py check <slug>
<rung>` where `rung not in kit.RUNGS` is a usage error, exit 2) — there is
no `check <slug> ready-to-release`. A product doc's front matter can
declare `stage: ready-to-release`, but that declaration with no matching
acceptance record on disk is itself a named problem (AU2, below) — a
human can no more type a work item into `ready-to-release` than into
`designed`. `rungs` in the routed result stays a 7-entry list keyed by
`RUNGS`; the terminal never appears as a rung row in it.

## Front-matter schema

The canonical write-down — this README, not the dated spec it came from,
is now the standard.

YAML front matter: the first line of the file is exactly `---`, closed by
a line `---` within 120 lines, containing `key: value` lines. A leading
`---` with no closing fence, or no `key: value` line inside it, is NOT
front matter — it parses to nothing, the same as if it weren't there.

| Key | Values | Meaning |
|---|---|---|
| `route` | `new` \| `problem` \| `spike` | triage class. QUESTION never becomes work — it has no route. `spike` is the one licensed ladder bypass. |
| `stage` | `framed` \| `viable` \| `scoped` \| `designed` \| `handed-off` \| `looping` \| `ready-to-release` | last completed rung, past-tense. A retired stage value (Retired names, below) is also legal to READ, but nothing ever writes one. |
| `concerns` | a list — see Views | the agreed concern list. Declaring it opts the design rung into the view count; absent, the rung behaves as before. |

Both keys travel together: front matter carrying either key must carry
both, with legal values — one without the other is incomplete and fails
the check. Front matter is required on `docs/product/*.md` and
`docs/gates/*.md`, optional elsewhere, and validated wherever present
(that "wherever" is AU4, below — it validates this rule against every
markdown file in `docs/`, not just the two required directories).

The six system design docs in `docs/design/` are the system's own specs,
not work climbing the ladder — they do NOT get retrofitted front matter.

## Retired names — read forever, written never

The ladder was renamed on 2026-08-25. Four rung names, four stage values,
one filename suffix set, and one section name were retired by that
rename. Every one of them is a **read-only alias, forever**: the parser
still recognizes them because pre-rename records carry them and no file
on disk is ever renamed or rewritten to catch up — but nothing ever
writes one again.

| Kind | Retired (read-only) → Live |
|---|---|
| rung / stage-root | `slice` → `scope` |
| rung / stage-root | `contract` → `handoff` |
| rung / stage-root | `build` → `loop` |
| rung / stage-root | `goal` → `acceptance` |
| stage value | `sliced` → `scoped` |
| stage value | `contracted` → `handed-off` |
| stage value | `building` → `looping` |
| stage value | `done` → `ready-to-release` |
| gate-record filename suffix | `slice`, `contract`, `build`, `goal` → `scope`, `handoff`, `loop`, `acceptance` |
| section name | `Done condition` → `Release condition` |

The rule, stated once and binding everywhere in this repo: **the parser's
legal set is the union of live names and retired aliases; the writer only
ever emits live names.** `legal_stage(v)` accepts `v in STAGES or v in
STAGE_ALIASES`; `stage_index(v)` maps a retired value to its live name
before ordering it. Have/need/problem lines always print the stage value
AS WRITTEN in the file, never the mapped one. An alias that is still
*written* by anything is the defect this rename exists to remove — and no
file on disk is ever renamed or rewritten to make an old one stop
appearing.

**A named limit.** AU3 (below) validates a gate record's *filename*
against a pattern that accepts both live and retired suffixes — it has no
way to tell a NEW file written today with a retired suffix (e.g. a
freshly authored `2026-09-01-foo-goal.md`) from an old, legitimate
record. A filename check cannot see intent. The write discipline — new
gate records use live rung names only — lives here, in this README, and
in the skills that write gate records; the machine holds the read side
only, never the write side.

## Why dated plans still say slice, contract and goal

The ladder was renamed on 2026-08-25 (seven rungs: frame → viability →
scope → design → handoff → loop → acceptance). Living surfaces —
this README, the progress renders, the journey pages — were regenerated
with the new names; dated records under `docs/plans/` (and elsewhere)
deliberately were not. A dated render or a dated spec shows the
vocabulary that was current on its date. **Old words inside a dated
record are not drift** — they are the record being honest about when it
was written. Any current link to a dated drawing should label it
*historical / pre-rename* where the ambiguity matters, and every record
generated from now on uses the new vocabulary only. (The ruling:
`docs/design/rung-vocabulary.md`, section "A living surface regenerates;
a dated record stands — RULED 2026-08-25".)

## Gate records

A gate record is a dated file in `docs/gates/` whose name AU3 pins:
`YYYY-MM-DD-<slug>-<rung>.md`, where `<rung>` may be a live rung name or
one of the retired filename suffixes (Retired names, above). The body is
prose for the human — the gate reads exactly two things from it: that the
file exists (the `handoff` rung's design GO record) and, for the derived
`ready-to-release` terminal, a `Release condition` section (or its
legacy `Done condition` alias) — plus the front matter every
`docs/gates/` record carries (Front-matter schema, above).

The last-gate record is `YYYY-MM-DD-<slug>-acceptance.md` with
`## Release condition`. Prose describing it says **"accepted as ready
for release"**, never "done" — the producer's ruling.

One optional line is standardized. Directly under the `# ` title:

    **Clock:** YYYY-MM-DD HH:MM TZ

when the record was written. Git already times the commits at both ends
of a rung exactly; the Clock line is the missing end that makes rung
*duration* derivable for new records. Write it under the same-turn rule
(`docs/state-contract.md`): a `date` run in the same turn as the record,
never a remembered time.

**Deliberately not validated.** No rule checks the line — not AU3, not a
rung input. Nothing retrofits it into an existing record either: a
backfilled time is manufactured history. Acceptance records adopt it
first. Graduating presence to a checked rule is held by the accepted
risk's review trigger in `docs/product/time-awareness.md` ("first
observed missing Clock line in a new record"), not by this README.

## Refusals

`check` is the refuser. Passing prints one line:

    PASS <rung> — <slug>: <n> inputs on disk

Refusing prints the full have/need render, then the verdict:

    gate: design — <slug>
    have: docs/product/<slug>.md — file exists
    have: docs/product/<slug>.md — front matter route=new stage=viable
    have: docs/product/<slug>.md — section "Value"
    have: docs/product/<slug>.md — Risk ledger names 1 killer risk(s) (Killer? = yes)
    have: docs/product/<slug>.md — section "Risk ledger" (3 rows, all qualified)
    need: docs/product/<slug>.md — section "Scope"
    REFUSED at design — <slug>: 1 missing
    enters at: viability

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
`scope`, nothing. A spike's output is expected to re-enter the ladder
normally once it exists; the bypass only covers the spike itself.

## Audit

The repo-wide mechanical sweep — `gate.py audit` — is the day-one live
refusal surface: the rules below run against the real tree on every
push, not just against a named slug.

| # | Rule |
|---|---|
| AU1 | `docs/design/*.md` filenames must NOT start `YYYY-MM-DD-` — living docs are undated. Runs against ten real files today. |
| AU2 | `docs/product/*.md`: undated filename · front matter required and legal · stage-vs-sections within the file: `framed`+ requires `Value`, `viable`+ requires `Risk ledger`, `scoped`+ requires `Scope`, `ready-to-release`+ requires an acceptance record (`docs/gates/*-<slug>-acceptance.md`, or a legacy `*-<slug>-goal.md`) — a stage claiming more progress than the file's sections (or its evidence) show is a named problem. |
| AU3 | `docs/gates/*.md` filenames MUST match `^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*-(frame\|viability\|slice\|scope\|design\|contract\|handoff\|build\|goal\|loop\|acceptance)\.md$` — live rung names and retired filename suffixes both legal (Retired names, above). |
| AU4 | Any `docs/**/*.md` whose front matter carries `route` or `stage`: both keys present, both values legal — this validates the front-matter schema against every file that opts into it, including dated spec files like this piece's own contract. |
| AU5 | `docs/product/*.md` carrying a `## Grounding` section: every `- ` list line must parse as `- <ref> — <why>` (split on the FIRST ` — `, the em-dash separator) and `<ref>` — a path or glob relative to the repo root — must resolve to ≥1 match on disk. Absent section = vacuous pass: declaring grounding is opting in. |
| AU6 | `docs/product/*.md`: exactly one legal `Rigor level: <spike\|mvp\|production-v1>` line INSIDE the `## Scope` section — a line outside the section, a missing line, duplicate lines, or an illegal value is a named problem. No `## Scope` section = vacuous pass. Lines inside ``` fenced code blocks are invisible (a quoted example is content, not a declaration). |
| AU7 | `docs/requirements/register.md` blocks and states, against the schema `docs/requirements/catalog.md` declares: legal ID (`^[A-Z]{2,4}-\d{3}$`, prefix agreeing with `Category`), no duplicate IDs, an unknown field is a hard error, `State` in the five, `Source` and statement present, `Category`/`Tags` declared `applies`/declared in the project's own `categories.md` (nothing hardcoded — the legal set is per-project; a register without the disposition file is one named problem and category judgments are skipped, not guessed), `final` owes an `Approved` hash that MATCHES the statement — divergence is refused and the state never rewritten — and `Approved` may not ride a non-final block; `superseded` owes its `superseded-by` link. Absent register = vacuous pass. One mechanical limit, stated: `dropped` owes a *reason* in Source; the machine checks only that Source is non-empty. |
| AU8 | Register links: every `- <role> → <ID> (sha256:<12 hex>)` line must parse, carry a role registered in the catalog grammar (both directions writable), and name an ID that exists. Two catalog rules are non-blocking FINDINGS, in the catalog's own flag-vs-refuse vocabulary: a link stamp diverging from its target's current statement ("flagged for re-look") and a non-origin block with no `refines` parent (aggregated to one line; "a finding, not an error, until slice 2"). Findings print in the audit's text output and never turn it red; the `--json` shape stays a bare problems list. |
| AU9 | every `docs/product/*.md` declaring `concerns:`: the block parses and no view is in a wrong state — a render (`.png`) named as the view, a path not on disk, an approved drawing whose fingerprint no longer matches, an unreadable approval line. Pending approvals (no line, or a hand-written line not yet sealed) are the design rung's business and do not fail the audit. |

AU3's pattern, verbatim from `kit.py`:

```python
GATE_RECORD_RE = re.compile(
    r'^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*-'
    r'(frame|viability|slice|scope|design|contract|handoff|build|goal|loop|acceptance)\.md$'
)
```

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
the first three: the fixture suite (`selftest`, exercising the 32 cases
against a temp tree), the real repo (`audit`, exercising AU1–AU8 against
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

Every `## Scope` section must declare how rigorously its work is
measured — one line, machine-checked:

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
  line inside the `## Scope` section; a `Rigor level:` line anywhere
  else, a missing line, duplicates, or an illegal value is a named
  problem. Fenced code blocks are invisible to the parse — a quoted
  example line is content, not a declaration. The problem strings,
  verbatim, in emission order — outside-line first, then exactly one
  of missing / duplicate / illegal: `Rigor level line outside Scope`;
  `Scope missing 'Rigor level: <spike|mvp|production-v1>' line`;
  `duplicate Rigor level lines (want exactly one)`; `illegal rigor
  level '<value>' (legal: spike, mvp, production-v1)`.
- **The scope rung** refuses work whose product doc violates the law,
  with one need row: `need: docs/product/<S>.md — Scope declares a
  legal rigor level (Rigor level: spike|mvp|production-v1)`.

A doc with no `## Scope` section passes vacuously — the section's
absence is already the scope rung's own refusal, and the rigor rule
does not double-refuse it. The declared level is data for later slices
(the rigor catalog and per-class disposition tables); this slice
enforces only that the level question is asked and answered legally.

## Views — the design gate's lock

A work item's front matter may declare `concerns:` — the agreed list of
what matters about this work, in ISO/IEC/IEEE 42010's vocabulary: a
**concern** is framed by a **viewpoint** (the diagram type), and a
**view** is the actual drawing made from that viewpoint. Declaring the
list opts the design rung into checking that every concern owns a view
or a named reason it does not.

### The schema

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

Absent `concerns:` = the design rung behaves exactly as today; declaring
it is opting in.

### What each view row checks

Computed per entry, in entry order, first failing rule wins. `P` =
`docs/product/<slug>.md — `.

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

**A render is never the view.** A `view:` path that does not end `.html`
is refused (rule a5) — the PNG is a render of the `.html`, and a derived
artifact is never approved.

### The fingerprint — rule 9, over the `.html` only

**Bytes hashed.** Rule 9's recipe (`docs/design/requirement-shape.md`),
with the file's content as the Statement and the other three fields
empty: read the file as UTF-8 text; trim it and collapse every internal
whitespace run to a single space; join the four fields with single `\n`
(so the hashed text is the collapsed content followed by three newlines);
SHA-256 over the UTF-8 bytes; first twelve hex characters. Equivalent by
hand:

```python
hashlib.sha256((" ".join(text.split()) + "\n\n\n").encode("utf-8")).hexdigest()[:12]
```

Collapsing whitespace is the recipe's own rule — a formatting-only edit
must not un-approve a drawing.

**Test vector:**

```python
FX = '<svg viewBox="0 0 8 8">\n  <rect x="0" y="0" width="4" height="4"/>\n</svg>\n'
view_fingerprint(FX)                                    == "2878c07db022"
view_fingerprint(FX + "   \n\n")                        == "2878c07db022"   # whitespace-only edit: same
view_fingerprint(FX.replace('height="4"', 'height="8"')) == "c938aa15c609"   # content edit: different
```

### `seal` — completing a hand-written approval

The producer types `<name>, <date>` by hand and never a hash; `seal`
computes rule 9's fingerprint over the drawing he actually agreed to and
writes it back:

    python3 tools/gates/gate.py seal <slug> [--root PATH] [--json]

Output, one line per entry plus a summary:

    seal — <product>
      sealed     <c>  <p>  <n>, <d> · fp:<fp>
      already    <c>  <p>  fp:<fp>
      DIVERGED   <c>  <p>  approved at fp:<was>, now fp:<now> — the drawing changed since it was agreed. Not rewritten.
      REFUSED    <c>  <p>  <why>
      unapproved <c>  <p>  no approval line — nothing to seal
      UNREADABLE <c>  approval line <text> is neither `<name>, YYYY-MM-DD` nor a sealed approval. Nothing was assumed.
      <n> sealed · <n> refused · <n> already approved · <n> diverged

**A divergence is reported, never rewritten** — the requirement-register
precedent (AU7). An approved drawing whose content changed since it was
agreed is `DIVERGED`, not silently re-approved; a human decides whether
the design still stands or the build needs fixing. `seal` exits 0 only
when nothing was refused, diverged or unreadable, and it writes nothing
at all while the concerns block fails to parse.

### The stated limit

The gate counts that a view exists, is approved and is unchanged, never
that it was worth drawing.

## Progress view

The gate is a seam, not a renderer: `--json` on `route`, `check`, and
`audit` dumps the same structured dict the text output is built from, and
every `kit.py` function takes `root` as a plain parameter so it can be
imported directly rather than shelled out to. That is the interface the
progress view is expected to consume — have/need lists, `enters_at`,
audit problem lines — but this tool draws no view of its own; rendering
that data as a UI is out of scope here and belongs to the progress-view
piece.
</content>
