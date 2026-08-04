---
route: new
stage: contracted
---

# Risk ledger — interrogate becomes the tiered risk ledger (build spec)

The contract for transforming `/kerd:interrogate` from a plan-readiness
document producer into the tiered risk ledger instrument, per
`docs/design/risk-ledger.md`. The interview engine is kept whole; the
output artifact is replaced. Modification, not rip: the skill keeps its
name and directory (`skills/interrogate/`).

## Scope

**In:**
- `skills/interrogate/SKILL.md` — rewritten (engine kept, output replaced, four deltas below)
- `README.md` — interrogate section rewritten; one cross-reference phrase in the capturerequirements section; What's New entry + heading
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — version bump 0.71.1 → 0.72.0 (three fields) + capability-list wording

**Out (boundaries — a step that wants to cross these stops and reports):**
- No other skill's SKILL.md is touched
- No gate-table changes (`tools/gates/` untouched)
- No new skill; no rename; no directory move
- No `docs/gates/` creation machinery — the gate-record shape is *documented*, never emitted by this change

**The four deltas** (the whole behavioral change, nothing else):
1. **Killer-first ordering** — THE killer assumption is identified and resolved first, always; ledger rows ordered killer-first.
2. **FATAL discipline** — Impact in declared-value units; Likelihood recorded separately, never multiplied; FATAL = impact ≥ declared value at ANY likelihood, set by impact alone.
3. **Tiering** — everyday tier: ledger filled in the normal framing conversation without invoking the skill (documented practice); large-bet tier: full interrogate session, co-sign written in the shape of the dated viability gate record (`docs/gates/` shape), documented for when gates are live.
4. **Dead exit fixed** — the `superpowers:writing-plans` exit is replaced by the walk's real flow: after viability, risks arrive pre-chewed at slicing and design, never re-assessed there.

## Acceptance bar

All of the following, in order, before the ship commit is considered done:

1. `python3 tools/gates/gate.py selftest` — exit 0
2. `python3 tools/gates/gate.py audit` — prints `audit: clean`, exit 0
3. `python3 tools/gates/gate.py release` — exit 0 (this enforces the three-field version sync R1 and the skills/ slash-ref rule R3)
4. `python3 tools/diagram/progress.py selftest` — exit 0
5. `grep -c 'writing-plans' skills/interrogate/SKILL.md` → `0`
6. README interrogate section and SKILL.md tell the same story (same columns, same states, same tiers, same homes)
7. `python3 tools/diagram/progress.py` output includes a `risk-ledger` strip (this spec's Pieces checklist paired with the ship commit's `Piece: risk-ledger/<n>` trailers)

## Decisions (settled here so no step has to re-litigate them)

**D1 — the everyday-tier ledger's on-disk home: the `## Risk ledger`
section of `docs/product/<slug>.md`.** Three reasons. (a) The date-split
rule: living = undated, overwritten; records = dated, immutable. The
ledger is living state — states flip as countermeasures land and review
triggers fire — so it belongs in the undated class, overwritten in place.
(b) The gate table already declares this exact location: the `slice` rung
mechanically checks section `Risk ledger` in `docs/product/<S>.md`
(tools/gates/README.md rung table). Inventing a second home would fork
the canonical vocabulary. (c) Downstream (slicing, design) must read ONE
home regardless of tier — so the large-bet session's signed ledger is
*copied into this same section* at sign-off.

**D2 — the large-bet session document stays at
`docs/interrogations/YYYY-MM-DD-<slug>.md`, dated.** It is a session
record — immutable once signed — so it belongs in the dated class. Its
filename `<topic>` becomes `<slug>`: the work slug matching
`docs/product/<slug>.md` when one exists (so record and living doc pair
by name), a kebab-case topic name otherwise. The co-sign block inside it
is written in the shape the future viability gate record will carry;
when gates are live, sign-off will also emit
`docs/gates/YYYY-MM-DD-<slug>-viability.md` per the record naming rule
`^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*-viability\.md$` — documented in
the skill, not built (boundary).

**D3 — the value declaration's canonical home (settled by conductor):
the `## Value` section of `docs/product/<slug>.md`** — the same section
the viability rung already checks. FATAL's impact units are denominated
in what that section declares. If it does not exist when a session
starts, establishing it is the interview's first thread (frame first,
then qualify).

**D4 — R2 resolved: the capability list changes.** The list names each
capability by its deliverable; interrogate's deliverable is no longer a
readiness document but qualified risks. `plan readiness` → `risk
qualification`, changed byte-identically in `plugin.json → description`
and `marketplace.json → plugins[0].description`. `metadata.description`
(the marketplace one-liner) is untouched — it carries no capability list.

**D5 — ledger table header is pinned byte-for-byte** to what the slice
rung checks, in every place the table appears (SKILL.md rules section,
SKILL.md template, README):

```
| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
```

Five state display forms (each normalizes to a legal gate value —
lowercase, em-dash → `-`): `Countermeasure — permanent` ·
`Countermeasure — TEMPORARY` · `Accepted` · `Accepted unknown` · `FATAL`.

## Composer amendment (approval gate, 2026-08-04)

**No line of the existing skill survives if it is wrong for this or not
needed.** The "keep verbatim" instructions below are conditional, not
reverent: a kept line must earn its place for the LEDGER's purpose. Where
a kept line is wrong for the ledger or carries no weight, the player cuts
or fixes it and reports each such cut with its reason — silent
preservation of dead weight is a contract violation equal to silent
deletion of live machinery.

## Pieces

- [x] Step 1: Rewrite skills/interrogate/SKILL.md
- [x] Step 2: Rewrite the README interrogate section and What's New
- [x] Step 3: Version bump and capability list in the two plugin manifests
- [x] Step 4: Collateral sweep and diff review
- [x] Step 5: Ship gate — full local gate, commit with piece trailers, push

---

### Step 1: Rewrite skills/interrogate/SKILL.md [delegate, model: sonnet, effort: high]

**What:** Rewrite `/Users/anthonymaley/Kerd/skills/interrogate/SKILL.md`
per the section-by-section contract below. "Keep" means keep the current
text verbatim unless a named edit says otherwise. All slash-command
references use the `/kerd:<name>` form; if a line ever needs to
illustrate a bare form, write the literal placeholder `/<skill>`, never a
real bare name (R3, CI-enforced). The string `writing-plans` must not
appear anywhere in the file. The words "readiness" and "readiness
document" must not appear — the deliverable is now qualified risks.

**1a. Frontmatter.** `name: interrogate` unchanged. Replace the
`description` value with exactly:

> Use when the user says 'interrogate', 'risk ledger', 'qualify risks', 'killer assumption', 'interview me', 'walk me through this plan', 'stress-test this idea', 'help me figure out if this is viable', or has a plan/idea whose risks need qualifying — sized, evidenced, and left in exactly one state — across every viability axis (technical, business, legal, operational). Produces a tiered risk ledger: everyday work fills the ledger in the framing conversation without invoking this skill; a large bet runs the full co-signed session at docs/interrogations/. Does NOT produce the implementation plan itself — produces qualified risks.

**1b. Title + intro.** Title becomes `# Interrogate (Risk Ledger)`.
Replace the opening paragraph with:

> Interview the user relentlessly about a plan or idea until every risk is QUALIFIED — sized, evidenced, and left in exactly one state — because a named, unsized risk reads as managed, and that is the failure this skill exists to stop. The interview engine is the instrument; the tiered risk ledger is the output. For a large bet, the exit ritual is mutual co-sign of the ledger.

Keep the second paragraph ("This skill is the countermeasure to the
convergence pull…") verbatim.

**1c. `## Invocation`.** Keep. Change the second line's tail to
"interrogate an existing plan" if it says otherwise; the `<plan-ref>`
explanation stays.

**1d. New section `## Tiering`** immediately after Invocation:

> | Tier | Instrument | Home |
> |---|---|---|
> | Everyday | the ledger filled inside the framing conversation — normal-sized work, no skill invocation | the living `## Risk ledger` section of `docs/product/<slug>.md`, overwritten in place |
> | Large bet | the full interrogate session — exhaustive across the axes (technical · business · legal · operational) | dated session record at `docs/interrogations/YYYY-MM-DD-<slug>.md`; the co-signed ledger is copied into the living section at sign-off |
>
> **Everyday.** This skill's Ledger section is the reference for the everyday practice: same eight columns, same five states, same rules — killer first, FATAL discipline, a risk without a countermeasure is a BLOCKER, an unqualified risk must not reach the next stage — applied inside the normal framing conversation without invoking this skill. The ledger is living state: states flip as countermeasures land and review triggers fire, so it is overwritten in place, never dated.
>
> **Large bet.** The full session below. Its co-sign is written in the shape of the viability gate record: when the entry gates are live, sign-off will also emit `docs/gates/YYYY-MM-DD-<slug>-viability.md` (dated, per the gate-record naming rule); until then the signed interrogation document is that record. Documented here — no record-emitting machinery ships with this skill.

**1e. `## Entry Paths`.** Keep both paths (plan-ref, zero) and the
convergence sentence, then append two new paragraphs:

> **The value declaration comes first.** Impact has no units until the value is declared. The canonical home is the `## Value` section of `docs/product/<slug>.md` — the same section the viability gate checks. If it exists, read it and denominate every Impact cell in its units. If it does not, the interview's first thread establishes it and writes it there (creating the file with legal `route`/`stage` front matter if needed) before any risk row is opened — frame first, then qualify.
>
> **The killer question comes next.** Immediately after scope pruning (plan-ref path) or once the idea is stated and the value declared (zero path), ask: *"What is the one assumption that, if false, kills this?"* That row opens first and gets the cheapest decisive evidence — a SPIKE, declared as such, if a test is needed — before any other risk is examined.

**1f. `## Interview Discipline`.** Keep rules 1–5 and rule 8 and the
Pause/resume paragraph verbatim. Two rewrites:

Rule 6 becomes:

> 6. **Three "done" gates, all required for sign-off.**
>    - **(a)** You have exhausted your known unknowns AND the ledger passes the qualification check before recitation can be proposed. The qualification check requires:
>      - every in-scope axis has at least one ledger row OR an explicit clear line in **Axis coverage** (*"no qualifying risk found — \<basis\>"*)
>      - every row fully qualified: **Impact** in declared-value units (never a vibe word) · **Likelihood** present, recorded separately · **Evidence** non-empty, naming a test or an analysis · **State** exactly one of the five · **Countermeasure** named with a confidence statement when State begins *Countermeasure* (plus a return condition when TEMPORARY) · **Review trigger** non-empty when State begins *Accepted*
>      - no row in **FATAL** — a FATAL row blocks recitation: the idea is killed (recorded in *What we ruled out* with the ledger row as evidence and its return condition attached) or reshaped until the row is no longer FATAL
>
>      If the check fails, continue interviewing on the failing rows — no recitation proposal. If it passes, *propose* entering recitation. User can veto ("more to discuss") to keep interviewing.
>    - **(b)** User has no more answers, requirements, or ideas to share.
>    - **(c)** Recite the ledger back **row-by-row**; user confirms each risk individually. Whole-ledger recitation is rejected as the easy-ratification trap this skill is designed to avoid.

Rule 7 becomes:

> 7. **Killer-first, then tree-aware ordering.** THE killer assumption is resolved first, always — the riskiest thing gets the cheapest test before anything else is examined. Below it, decisions that constrain other decisions get resolved first. Within each decision, depth-first: resolve fully — including the ledger rows the decision affects — before sliding sideways to the next branch.

**1g. New section `## The Ledger`** (before Document Structure). Content,
transcribed from `docs/design/risk-ledger.md` so the skill is
self-contained:

> Risks as rows, killer rows first. Columns:
>
> | Column | Rule |
> |---|---|
> | **Risk** | the concept, not the incident — one row per eliminated-or-carried idea |
> | **Killer?** | marks THE killer assumption — tested first, always |
> | **Impact** | in the units of the declared VALUE (`## Value` of `docs/product/<slug>.md`) — never a vibe word |
> | **Likelihood** | recorded SEPARATELY, never multiplied — expected value is the wrong maths for a bet taken once |
> | **Evidence** | a test OR an analysis — the same kind of evidence, differing in cost. Empty evidence = unqualified |
> | **State** | exactly one of the five below |
> | **Countermeasure** | named, with a CONFIDENCE statement |
> | **Review trigger** | for accepted states: the date or condition that brings the risk back |
>
> The table header is exact — downstream mechanical checks match it byte-for-byte:
>
> ```
> | Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
> ```
>
> **The five states:**
>
> | State | Meaning |
> |---|---|
> | **Countermeasure — permanent** | closed by design |
> | **Countermeasure — TEMPORARY** | carries its return condition; an unmarked temporary countermeasure is permanent by neglect |
> | **Accepted** | by whom, when — and its review trigger |
> | **Accepted unknown** | by whom, when, why the evidence was not gathered — and its review trigger |
> | **FATAL** | impact ≥ the declared value, at ANY likelihood |
>
> **The rules:**
>
> - **FATAL is set by impact alone** — likelihood sets the response, never the class.
> - **A risk without a countermeasure is a BLOCKER** — silence stops work instead of passing it.
> - **The one unacceptable state**: high impact + high likelihood + no countermeasure = dead project. It cannot be accepted by name.
> - **Killer assumption first**: the riskiest thing gets the cheapest test before anything else is examined. The SPIKE is that instrument — declared up front, cheap, built for a kill-or-keep decision.
> - **An unqualified risk MUST NOT reach the next stage.**
> - Every △ verdict in an evaluation matrix lands its countermeasure here, with confidence and return condition.
> - An idea killed by a FATAL row is recorded in *What we ruled out* with the row as evidence and its return condition attached.

**1h. `## Document Structure`** — replace the current content. It now
describes the **large-bet** session document only (the everyday tier
writes straight into `docs/product/<slug>.md` per Tiering). Required
content:

- Path: `docs/interrogations/YYYY-MM-DD-<slug>.md`; `<slug>` is the work slug matching `docs/product/<slug>.md` when one exists, else a kebab-case topic name. Dated because it is a session record, immutable once signed; the *living* ledger home is `docs/product/<slug>.md` — this document is how it got there. Create `docs/interrogations/` on first use. Update the file incrementally after each meaningful exchange — never reconstruct wholesale at the end.
- Outline:

  ```
  [frontmatter]
  ## Scope
    ### In scope
    ### Out of scope
  ## Deferred
  ## Risk ledger
  ## Axis coverage
  ## Notes          (optional — overflow detail a cell references)
  ## Sign-off       (present only after signing)
  ```

- Frontmatter, draft state:

  ```yaml
  ---
  created: <ISO timestamp at session start>
  last-updated: <ISO timestamp of most recent update>
  status: draft           # draft | signed
  topic: <short human-readable topic name>
  slug: <work slug, when one exists>

  # Session state — present while status: draft
  current-axis: <axis under interview>
  current-thread: <sub-decision being resolved, or empty>
  last-question: <verbatim text of the last question asked>
  adversarial-level: gather   # gather | probe | stress-test | adversarial
  recitation-status:
    <risk-slug-1>: pending    # pending | recited | confirmed | pushed-back
    <risk-slug-2>: pending
  ---
  ```

  `recitation-status` is keyed by **risk slug** — the kebab-case of the row's Risk cell — initialized to `pending` the moment a row is added; `{}` at document birth before any rows exist. Every ledger row must have an entry — no missing keys.
- Scope keeps its current semantics (boundary concept: in *and* out define the project; out-of-scope items carry a one-line reason). Deferred keeps its current semantics (timing, not boundary: item + reason + revisit trigger). Both sections' current prose may be carried over with axis-section references removed.
- `## Risk ledger`: the eight-column table from The Ledger section, killer rows first.
- `## Axis coverage`: one line per in-scope axis — either `- <axis> — <n> rows` or `- <axis> — clear: <one-line basis>`. This replaces the old per-axis six-field sections: qualification lives in rows, not prose; this section only proves no axis was skipped.
- A canonical template code block showing a fresh document (frontmatter + empty Scope/Deferred + the exact table header with one placeholder row + empty Axis coverage), plus the current file's closing sentence pattern: the template is the structural floor; documents that do not match it break the resume / qualification-check / recitation logic. Keep the zero-path initialization paragraph, adapted: before any rows exist, `current-axis` is empty, In scope is empty, `recitation-status` is `{}`.

**1i. `## Recitation Gate`** — rewrite to row-by-row. For each ledger
row: (1) set `recitation-status[risk-slug]: recited`; (2) present the
row: Risk, Killer?, Impact, Likelihood, State, and the countermeasure or
acceptance gist; (3) ask *"Does this row read right?"*; (4) confirmed →
`confirmed`, next row; (5) pushed back → `pushed-back`, re-enter the
interview on that row (graduated lean continues from where it was),
re-recite until confirmed. Only after every row is `confirmed` does
sign-off become possible — gate (c), the demonstration of understanding,
not its declaration. Whole-ledger recitation stays explicitly rejected.

**1j. `## Sign-off Ritual`** — keep the current mechanics (present the
document; user types `signed` in chat — the commit-message-rejection
parenthetical stays; frontmatter flips to `status: signed` with
`signed-at` + `signers`; session state folds into `final-session-state`,
now with the risk-keyed recitation map). Two additions:

- New step after the frontmatter update: **Copy the ledger to its living home.** Overwrite the `## Risk ledger` section of `docs/product/<slug>.md` with the signed table (create the section if absent), so downstream reads one home regardless of tier. The signed interrogation document freezes as the dated record.
- New closing paragraph: the `## Sign-off` section written into the document (signed-at, signers, row count, killer count, `FATAL rows: 0`) is the content the viability gate record will carry; when the entry gates are live, sign-off will also emit `docs/gates/YYYY-MM-DD-<slug>-viability.md` — same date, same slug, `-viability` suffix. Until then, the signed interrogation document is the record.

Keep the "complete as of [signed-at], not eternally" paragraph.

**1k. `## Composition with Kerd`** — keep the three invocation contexts
and the stop-without-sign-off paragraph. One edit: the mid-conductor
bullet's second sentence becomes "The co-signed ledger arrives
pre-chewed at conductor's plan phase."

**1l. `## Default Axis List`** — keep verbatim; append one sentence to
the universal-core intro: "Every axis feeds the same ledger — axes
organize the questioning; rows are the output."

**1m. `## What This Skill Does Not Do`** — keep the auto-detect-sign-off,
insight-blocks, multi-user, and axis-checklist bullets verbatim. Replace
the first bullet with:

> - **Does not produce the implementation plan itself.** This skill produces *qualified risks*. After sign-off, the work moves down the walk — slice a release, then design the solution — with its risks pre-chewed; they are never re-assessed there. In a Kerd session that continuation runs through `/kerd:conductor` (this session's build) or `/kerd:sherpa` (the lifecycle walk). Boundary kept to prevent design synthesis from sneaking in too early.

Add two bullets:

> - **Does not multiply impact by likelihood — ever.** Expected value is the wrong maths for a bet taken once. Impact sets the class; likelihood sets the response.
> - **Does not write `docs/gates/` records.** The co-sign is written in that record's shape; emitting it belongs to the entry gates when they are live.

**Why:** This is the whole behavioral change — engine kept (the interview
discipline is the skill's proven value), output replaced (the ledger is
what downstream consumes), the four deltas encoded at the exact points
where the old document shape lived. Row-keyed recitation replaces
axis-keyed because the row is now the unit of shared understanding.

**Verify:**

```
grep -c 'writing-plans' skills/interrogate/SKILL.md
grep -ci 'readiness' skills/interrogate/SKILL.md
grep -cF '| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |' skills/interrogate/SKILL.md
grep -nE '/(interrogate|conductor|sherpa|kivna|switch|tend|trim|mode|pair|lorg|skriv|slainte|capturerequirements)\b' skills/interrogate/SKILL.md | grep -v 'kerd:'
grep -c 'FATAL' skills/interrogate/SKILL.md
```

Expected: `0` · `0` · `2` or more (rules section + template) · empty
output · `5` or more. (The first two greps exit 1 on zero count — that
is the pass condition, not a failure.)

### Step 2: Rewrite the README interrogate section and What's New [delegate, model: sonnet, effort: medium]

**What:** Three edits to `/Users/anthonymaley/Kerd/README.md`.

**2a.** Replace the entire `### interrogate (Plan Readiness)` section
(heading through the closing code fence, up to but not including
`### capturerequirements`) with exactly:

```markdown
### interrogate (Risk Ledger)

Interrogate qualifies the risks of a plan or idea until every one is sized, evidenced, and left in exactly one state — because a named, unsized risk reads as managed, and that is the failure this skill exists to stop. The interview engine is unchanged: one question per turn, no extrapolation, graduated adversarial lean (gather → probe → stress-test → adversarial), user-veto on stop, deterministic pause/resume from frontmatter session state, and row-by-row recitation before co-sign. The output is the tiered risk ledger: eight columns (Risk / Killer? / Impact / Likelihood / Evidence / State / Countermeasure / Review trigger), five states (Countermeasure — permanent, Countermeasure — TEMPORARY, Accepted, Accepted unknown, FATAL), killer assumption first, always.

Two tiers. Everyday work fills the ledger inside the framing conversation — no skill invocation — directly into the living `## Risk ledger` section of `docs/product/<slug>.md`. A large bet runs the full interrogate session, exhaustive across the viability axes (technical, business, legal, operational), producing a dated session record at `docs/interrogations/YYYY-MM-DD-<slug>.md` whose co-signed ledger is copied into the living section at sign-off. Impact is denominated in the units of the declared value (the `## Value` section of `docs/product/<slug>.md`); FATAL means impact ≥ that value at any likelihood — set by impact alone, never by multiplying in likelihood. Interrogate does not produce the implementation plan — after sign-off the work moves down the walk to slicing and design with its risks pre-chewed, never re-assessed there.

Design at `docs/design/risk-ledger.md`; the interview engine's original design at `docs/plans/2026-05-02-interrogate-design.md`.

​```
/kerd:interrogate              # zero-path: interview from an idea
/kerd:interrogate <plan-ref>   # interrogate an existing plan
​```
```

(The code fence above is the section's own fence — write it as a normal
triple-backtick fence in the README.)

**2b.** In the `### capturerequirements` section, replace the phrase
`co-signs a readiness document` with `co-signs a qualified risk ledger`.
(Consistency edit only — interrogate is being described there; nothing
else in that section changes.)

**2c.** What's New: change the heading `## What's New (v0.68.0)` to
`## What's New (v0.72.0)`, and insert directly beneath it (above
`### v0.68.0`) a new entry:

```markdown
### v0.72.0

**Interrogate now produces a tiered risk ledger.** The interview engine stays — one question per turn, no extrapolation, graduated adversarial lean, user-veto on stop, pause/resume, recitation before co-sign — but the output document is replaced by the risk ledger: eight columns (Risk / Killer? / Impact / Likelihood / Evidence / State / Countermeasure / Review trigger), five states, killer assumption tested first. FATAL discipline: impact is denominated in the declared value's units (the `## Value` section of `docs/product/<slug>.md`), likelihood is recorded separately and never multiplied in, and impact ≥ value at any likelihood is FATAL — set by impact alone. Two tiers: everyday work fills the ledger inside the framing conversation, straight into the living `## Risk ledger` section of `docs/product/<slug>.md`; a large bet runs the full session at `docs/interrogations/`, its co-sign written in the shape of the future dated viability gate record. The dead planning-skill exit is replaced by the walk's real flow: risks arrive pre-chewed at slicing and design. Design at `docs/design/risk-ledger.md`.
```

**Why:** Release checklist item 2 (README tracks skill behavior), and the
README follows an observable newest-entry-at-top What's New convention
whose heading names the newest documented version. The changelog entry
says "the dead planning-skill exit" rather than naming it so the
`writing-plans` grep surface stays confined to genuinely historical
entries.

**Verify:**

```
awk '/^### interrogate /,/^### capturerequirements /' README.md | grep -c 'writing-plans'
awk '/^### interrogate /,/^### capturerequirements /' README.md | grep -c 'Risk / Killer? / Impact / Likelihood / Evidence / State / Countermeasure / Review trigger'
grep -c '^### v0.72.0' README.md
grep -cF "What's New (v0.72.0)" README.md
grep -c 'co-signs a qualified risk ledger' README.md
grep -c '### interrogate (Plan Readiness)' README.md
```

Expected, in order: `0` (grep exits 1 — that is the pass) · `1` · `1` ·
`1` · `1` · `0` (exit 1). If `grep -n 'Plan Readiness' README.md` still
hits anywhere, every hit must sit inside the `## What's New` history —
historical entries are records and stay untouched.

### Step 3: Version bump and capability list in the two plugin manifests [delegate, model: haiku, effort: low]

**What:** Two files, five field changes.

- `/Users/anthonymaley/Kerd/.claude-plugin/plugin.json`:
  - `version`: `0.71.1` → `0.72.0`
  - `description`: replace the substring `plan readiness` with `risk qualification` (list position unchanged — between `token optimization` and `requirements capture`)
- `/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json`:
  - `metadata.version`: `0.71.1` → `0.72.0`
  - `plugins[0].version`: `0.71.1` → `0.72.0`
  - `plugins[0].description`: same single-substring replacement — the resulting string must be byte-identical to plugin.json's `description`
  - `metadata.description`: DO NOT TOUCH (it is intentionally a different shape — the marketplace one-liner, no capability list)

**Why:** MINOR bump (changed behavior) per the version strategy; R1 is
CI-enforced on the three-field sync. D4 settles the capability wording:
the list names deliverables, and interrogate's deliverable is now
qualified risks.

**Verify:**

```
python3 - <<'EOF'
import json
p = json.load(open('/Users/anthonymaley/Kerd/.claude-plugin/plugin.json'))
m = json.load(open('/Users/anthonymaley/Kerd/.claude-plugin/marketplace.json'))
assert p['version'] == '0.72.0', p['version']
assert m['metadata']['version'] == '0.72.0'
assert m['plugins'][0]['version'] == '0.72.0'
assert p['description'] == m['plugins'][0]['description'], 'capability lists diverged'
assert 'risk qualification' in p['description']
assert 'plan readiness' not in p['description']
assert m['metadata']['description'] == 'Kerd: opinionated workflow skills and community-contributed modes for Claude Code'
print('ok')
EOF
```

Expected: `ok`.

### Step 4: Collateral sweep and diff review [keep]

**What:** Two passes, no edits outside the Scope list without stopping.

1. **Sweep** — run:

   ```
   grep -rn 'plan.readiness\|readiness document\|docs/interrogations' skills/ modes/ docs/playbook.md CLAUDE.md README.md
   grep -rln 'interrogate' skills/ modes/ | grep -v 'skills/interrogate'
   ```

   Classify every hit: (a) inside this change's Scope and stale → fix it now; (b) outside Scope (another skill/mode referencing interrogate's old deliverable) → do NOT edit; collect into a report for the approval gate. Historical What's New entries in README are records — never rewritten. The `kerd:capturerequirements` SKILL.md frontmatter ("Not the exhaustive viability sweep that /kerd:interrogate runs") is expected to still read true — confirm rather than assume.

2. **Diff review** — read `git diff` in full. Check: the four deltas are all present in SKILL.md; no fifth behavior change snuck in; SKILL.md and README tell the same story (columns, states, tiers, homes, exit flow); the pinned table header is byte-identical everywhere it appears; no edit landed outside the Scope file list.

**Why:** Cross-cutting changes miss files (project memory codifies this),
and the boundary — no other skill touched — needs a judgment call on
every out-of-scope hit, not a mechanical fix. This is the seam where a
human-shaped reviewer earns its keep.

**Verify:**

```
git diff --stat
git status --porcelain
```

Expected: exactly four files changed — `skills/interrogate/SKILL.md`,
`README.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
— plus this spec file untracked or modified; nothing else. Plus a short
written report (may be empty) of out-of-scope stale references for the
approval gate.

### Step 5: Ship gate — full local gate, commit with piece trailers, push [keep]

**What:**

1. Check the boxes in this spec's `## Pieces` for steps 1–4 (and step 5's box as part of the ship commit itself — the commit that ships is the commit where all five are `- [x]`).
2. Run the full local gate, in order, all green:

   ```
   python3 tools/gates/gate.py selftest
   python3 tools/gates/gate.py audit
   python3 tools/gates/gate.py release
   python3 tools/diagram/progress.py selftest
   ```

3. Render the progress view and confirm the strip:

   ```
   python3 tools/diagram/progress.py | grep -i 'risk-ledger'
   ```

4. Commit everything (the four changed files + this spec + the regenerated `docs/plans/progress.{excalidraw,svg}` if the render dirtied them) with a message of the shape:

   ```
   Interrogate becomes the tiered risk ledger (0.72.0)

   Engine kept, output replaced: eight-column ledger, five states,
   killer-first, FATAL by impact alone in declared-value units.
   Everyday tier lives in docs/product/<slug>.md ## Risk ledger;
   large bet co-signs at docs/interrogations/, shaped for the
   future viability gate record. Dead planning-skill exit replaced
   by the walk's flow: risks pre-chewed at slicing and design.

   Piece: risk-ledger/1
   Piece: risk-ledger/2
   Piece: risk-ledger/3
   Piece: risk-ledger/4
   Piece: risk-ledger/5
   ```

   plus the session trailer the harness requires. The `Piece:` trailers
   use the slug `risk-ledger` — matching this spec's filename — so the
   progress renderer pairs commit and checklist.
5. Push to remote (commit rule: always push after committing).

**Why:** The acceptance bar is the local gate green plus a visible strip;
the trailers-and-checklist pairing is what makes the work legible to the
progress view. This is the second genuine judgment seam: nothing ships
on a red or ambiguous gate.

**Verify:**

```
python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && echo GATES-GREEN
python3 tools/diagram/progress.py | grep -ci 'risk-ledger'
git log -1 --format=%B | grep -c '^Piece: risk-ledger/'
git status --porcelain | wc -l
```

Expected: `audit: clean` then `GATES-GREEN` · `1` or more · `5` ·
`0` (clean tree, pushed).
