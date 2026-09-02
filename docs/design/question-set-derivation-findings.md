# Question set derivation — findings

Spike frame: `docs/product/question-set-derivation.md`. Run 2026-09-02.
The kill-or-keep this verdict is read off was declared before the derivation
ran, in commit `5fafc19`.

## Verdict: PARTIAL

**Five of six questions in the candidate viability set trace to a
machine-enforced gate need. One traces only to a named standing decision.
The set surfaces the material viability issue in all three items tested.**

PARTIAL was declared a legal outcome in the frame before the work started, so
this is a result rather than a failure to reach one. It sizes the remaining
rungs: **most of a set is free, and the residue is nameable.**

**Two properties bound the verdict, and the second one is the finding that
matters most:**

1. Derivability is real.
2. **Derivability decays.** A derived set reproduces what the repo has already
   learned; it cannot anticipate what a rung has not yet taught it.

## What "derivable" was measured against

Two legal citation sources, declared in the frame:

1. **A machine-enforced gate need** — a check in `tools/gates/kit.py` that
   refuses when the thing is absent. Cited by line.
2. **A named standing decision** — a dated bullet in `CONTEXT.md
   ## Key Decisions`, or a rule in a living design doc.

Anything else — the model's sense of a good question, an unread standard, an
unrecorded convention — is **not** derived, and the finding's job is to name it
rather than to write a plausible question anyway.

## The structural rule the whole derivation rests on

**A rung's exit is the next rung's entry.** Canonical at
`tools/gates/README.md:42`, verbatim: *"Evaluated by `check <S> viability`
because a rung's exit is the next rung's entry; it is the frame gate's input,
not viability's."* Consistent with the 2026-08-28 ruling that a check's code
location and its reader-facing name are two different things and the reader's
one wins.

**So viability's exit demands are what `check_rung(slug, "scope")` adds** — not
what the viability block contains. Verified live: `hooks-autoload` sits at
viability and its single blocker for scope is an illegal `State` value in its
ledger.

## Viability's exit demands, read from the code

Nine machine-enforced demands.

| # | Demand | Refusal site |
|---|---|---|
| 1 | `## Risk ledger` header is exactly the 8 `LEDGER_COLUMNS` | `kit.py:61`, refused at `:457` |
| 2 | At least one data row | `kit.py:469` |
| 3 | Every row: `Evidence` non-empty | `kit.py:482` |
| 4 | Every row: `State` ∈ the five `LEGAL_STATES` | `kit.py:70`, refused at `:486` |
| 5 | No row with `State` = `fatal` — a named refusal that cannot pass | `kit.py:488` |
| 6 | `Countermeasure` non-empty when `State` is `countermeasure - *` | `kit.py:492` |
| 7 | `Review trigger` non-empty when `State` is `accepted*` | `kit.py:496` |
| 8 | `## Scope` section exists | `kit.py:804` |
| 9 | `## Scope` declares a legal `Rigor level` | `kit.py:81`, refused at `:809` |

**A measured gap inside the demands.** `Impact` and `Likelihood` are columns in
`LEDGER_COLUMNS` (`kit.py:61`) and **the parser never refuses an empty one** —
only `Evidence`, `State`, `Countermeasure` and `Review trigger` are checked per
row. So the sizing of a risk is structurally optional today. This is the single
reason question 6 below has no machine citation.

## The candidate viability set — EVIDENCE, not a seed file

This set is deliberately **not** written to `docs/work/question-sets/`. Placing
it in the directory Drive reads at intake would ship it, and a spike that ships
is not a spike. It appears here so the citations can be checked.

1. **What could stop this being worth doing — all of them, not just the one
   that could kill it?**
   *Derived:* demands 1–2 (`kit.py:457`, `:469`).

2. **For each, what evidence sizes it — a test, or an analysis?**
   *Derived:* demand 3 (`kit.py:482`), plus CONTEXT 2026-08-03 — *"Evidence
   qualifies a risk, and it is a test OR an analysis."*

3. **Is any risk fatal — impact at or above the declared value, at any
   likelihood?**
   *Derived:* demand 5 (`kit.py:488`), plus CONTEXT 2026-08-03 — *"Fatal =
   impact >= declared value, at any likelihood; likelihood sets the response,
   not the class."*

4. **For each risk, which of the four dispositions applies, and what does that
   disposition oblige — a countermeasure, or a review trigger?**
   *Derived:* demands 4, 6, 7 (`kit.py:486`, `:492`, `:496`), plus CONTEXT
   2026-08-03 — countermeasures are permanent or temporary, and *"an unmarked
   temporary one is permanent by neglect."*

5. **What is the smallest valuable increment, what is deliberately excluded,
   and at what rigor level will it be measured?**
   *Derived:* demands 8–9 (`kit.py:804`, `:809`). **Limit stated:** the machine
   checks that `## Scope` *exists* and that one `Rigor level:` line is legal. It
   checks nothing about the section's content, so the question's *shape* derives
   and its *substance* rests on CONTEXT 2026-08-25 — *"scope … is where we lock
   in what we want, what features etc."*

6. **What is each risk's impact in the declared value's own units, and its
   likelihood, recorded separately?**
   **NOT derived from any machine need** — see the measured gap above. Rests
   solely on CONTEXT 2026-08-03: *"Qualified = proven AND measured: impact in
   the value's units, likelihood recorded **separately** — never multiplied,
   because expected value is the wrong maths for a bet taken once."*

## Tested against three items that genuinely passed viability

The test is not whether a question reads well. It is: **would this question
have surfaced the material viability issue the item actually hit?**

| Item | Material issue | Surfaced by |
|---|---|---|
| `rigor-level` | hollow waiving — waived-by-name is the cheapest state, so the level means nothing | Q1, Q2, Q4 |
| `requirements-success-measurement` | friction so high the capability is skipped every time, leaving 0 of 52 at 0 of 52 | Q1, Q2, Q4, Q6 |
| `gate-visuals` | a visual approved without being read, becoming declared truth | Q1, Q4 |

**Three of three.** Q4 carries the most weight in the test, because in all three
cases the disposition and its obligation are where the honest answer lives —
`gate-visuals` sits at `accepted unknown` with `none yet` in its Countermeasure
cell, which is legal precisely because the state does not demand one.

## Finding 1 — derivation is backward-looking, and this is the durable problem

`requirements-success-measurement`'s ledger carries the sharpest content of the
three: the likelihood cell states that *"medium with the control"* is **an
explicit producer judgment, not a derived or measured one … Drive does not
structurally guarantee compliance."*

That content **is** citable today — CONTEXT 2026-08-31 records it as a standing
decision — so a derivation run now produces a question that would surface it.
**But the decision did not exist until that item's own scope gate produced it.**
A derivation run on 2026-08-05 could not have asked it, because nothing on disk
knew it yet.

**So the property is: a derived set is exactly as good as the decisions
accumulated at the moment it was derived, and it goes stale silently.** Nothing
about the set's own text changes when a new ruling lands. This is the repo's own
recurring class — two living sources joined by nothing, where the test is *what
fails if one side moves?* and the answer is nothing.

## Finding 2 — kill criterion 3 could not be tested

The declared criterion: *"A derived question passes an item that should have
been stopped."*

**Searched and not found.** No item on the board carries a recorded case of a
viability decision that passed and should not have. `hooks-autoload` is held at
viability by an illegal `State` — the gate working, not failing. Drive's
invented `unqualified` state was machine-refused, not waved through.

Reported as *searched `docs/product/`, `docs/gates/`, CONTEXT decisions; not
found* — **never as "the criterion is satisfied."** Criteria 1 and 2 were
testable and neither fired.

## Recommended mechanism — NOT implemented here

The producer's ruling, 2026-09-02, on where the staleness pressure belongs:
**source change, not every use.** A derived set should carry four things:

1. **The exact gate demands and standing decisions it was derived from**, named
   individually.
2. **A derivation fingerprint** over those named sources.
3. **A refusal condition:** if any named source changes, the set is **stale**
   and must be re-derived before use.
4. **A periodic Law 4 review trigger**, for discovering relevant new sources
   that were never named.

**His reasoning, recorded because it rules out the two obvious alternatives:**
re-deriving on every invocation *"wastes work without solving the harder
problem: an unlisted new decision would remain invisible."* A date-only review
trigger *"is also too weak."* The durable model is **source-bound invalidation
plus a scheduled discovery review** — the two halves answer different failures,
and neither alone is sufficient.

**Candidate shape for element 2, not decided:** reuse
`approval_fingerprint(category, fields)` — the one versioned mechanism with
artifact-specific canonical payloads, keyed 2026-09-01 — rather than inventing a
second recipe. That is the rule-9 lesson: two implementations tested against each
other by nothing. Whether a question set is a legal category for it is a design
question for the adoption item, not settled here.

**Nothing above is built.** No `kit.py` edit, no check, no AU rule, no seed
file. `tools/` was untouched for the whole spike.

## What this sizes

- **The other five rungs are not six research items.** Each rung's exit demands
  are enumerable from `check_rung` the same way, and the two citation sources
  are the same two. Expect most of each set to derive.
- **The residue is nameable per rung** rather than unknown, which is what makes
  a bounded estimate possible at all.
- **The real work is the mechanism above, not the questions.** Writing six sets
  is cheap; keeping them honest as the gates keep teaching is the part that
  needs designing.

## Scope — what was NOT tested

Stated explicitly, because a spike's reach is the first thing over-read.

- **Only the viability rung was derived.** Scope, design, handoff, loop and
  acceptance were not attempted. The claim that they will behave similarly is an
  expectation from shared structure, **not** a measurement.
- **Only three items were tested**, all software-change work in this repo. No
  content plan, business plan, document or repair was tested, so the
  work-type-neutrality claim recorded on 2026-09-01 is untouched by this spike
  either way.
- **Question quality was not assessed.** Derivability was tested; wording was
  not.
- **The frame set was used as a worked example, not reviewed.**
- **Kill criterion 3 is untested**, per Finding 2.

## Filed, not fixed

`CONTEXT.md`'s 2026-08-25 bullet reads *"viability requires killer risks named
… scope requires every row qualified."* Under `tools/gates/README.md:42` and
the 2026-08-28 naming ruling, both labels sit **one rung high**: killer-risks-
named is the **frame** gate's input, every-row-qualified is the **viability**
gate's input. The machine description is accurate; the reader-facing rung names
are not.

Not edited here — it is a keyed tree, and the standing rule is *file, don't
edit*. It matters to this spike specifically: **the second citation source
carries vocabulary that predates the naming ruling, so a derivation citing it
naively would file questions against the wrong rung.**

## Grounding

- tools/gates/kit.py — every machine citation in the derivation, by line
- tools/gates/README.md — the canonical "a rung's exit is the next rung's entry" rule
- docs/product/question-set-derivation.md — this spike's frame and its declared kill-or-keep
- docs/work/question-sets/software-change.md — the worked example the derivation was checked against
- docs/product/rigor-level.md — test item 1, hollow waiving
- docs/product/requirements-success-measurement.md — test item 2, and the source of Finding 1
- docs/product/gate-visuals.md — test item 3, approved-unread
- docs/product/hooks-autoload.md — the live at-viability item that verified the structural rule
- CONTEXT.md — the standing decisions cited as the second legal source
