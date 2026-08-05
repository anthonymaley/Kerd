# The design instrument — approaches and the evaluation matrix

Living design doc. Owner: **Design the solution** (the DESIGN rung's one
function). Source: post-walk decision 2 — build our own, with the Technical
Evaluation Matrix as THE way options are compared (`Sensei Input/example
diagrams/FSS DB Technical Evaluation.xls`, de-spreadsheeted; legend
corrected to the Toyota marks 2026-08-04).

## What it does

One conversation, one package — this instrument is the part of that
conversation that generates the candidate solutions and settles which one
wins, on evidence, in a form reviewable at a glance.

## Half one — approach generation

- **Input:** the framed intent (idea brief or problem statement) with its
  declared measurements, plus the qualified risks from the ledger
  (pre-chewed — never re-assessed here).
- **Generate 2–3 genuinely independent approaches.** Independence test:
  different mechanism or architecture, not variations of one idea — if two
  approaches share their riskiest assumption, they are one approach.
- **Every approach is drawn**: an architecture overview per option is a
  matrix REQUIREMENT (the xls carries one per row), not decoration.
- Grounding before generating (the design function's rule): standing
  decisions · *What we ruled out* (a dead option must not be re-proposed —
  and if one is proposed anyway, the record answers it) · the living design
  docs of whatever the work touches.
- One-time salvage (done 2026-08-04): brainstorming's probing questions
  were mined into *The prompt set* below; the superpowers tie is cut.

## The prompt set

Mined once from the superpowers brainstorming skill (2026-08-04), adapted
to this system's grammar: one question per turn, open questions — never
multiple-choice menus, which pre-narrow the answer space. Used while
generating approaches, before anything is scored.

**Framing probes** — before any approach exists:

- What is this for — what changes for whom when it works?
- Which constraints are actually fixed (platform, budget, standing
  decisions), as opposed to habits worth questioning?
- What does success look like, in the declared VALUE's units?
- Is this ONE piece of work? If it hides several independent subsystems,
  decompose first and evaluate the first piece — a matrix over a bundle
  compares nothing.

**Independence probes** — while generating the 2–3 approaches:

- What is this approach's riskiest assumption? If two approaches share
  it, they are one approach — generate a genuinely different mechanism.
- What does each approach look like drawn? No architecture overview, no
  option row.
- What is the smallest version of each approach that still wins its case
  — what survives YAGNI?

**Boundary probes** — per approach, before scoring:

- For each unit: what does it do, how is it used, what does it depend on?
- Could someone understand a unit without reading its internals? Could
  the internals change without breaking consumers? If not, the
  boundaries need work before the option is scoreable.
- Does the approach follow the patterns of the code it touches, or
  import a foreign idiom — and if foreign, is that cost on the matrix?

**Self-review scans** — on the filled matrix, before the verdict:

- Placeholder scan: any TBD, any vague target, any score without basis?
- Consistency scan: does any closing section contradict a mark?
- Ambiguity scan: could any criterion's target be read two ways? Pick
  one reading and write it down.

## Half two — the evaluation matrix

**Options as rows** — ID · description · the drawn architecture overview.

**Criteria as columns, in groups** — and criteria DERIVE from declarations
(the DONE-assembled rule applied to evaluation: a criterion nothing
declared cannot be scored, so it cannot exist). Sources: the intent's
measurements · qualified risks · standing constraints. Typical groups, from
the exemplar: hosting/environment · quality (strategy · performance ·
support · engineering · scaling) · due date · cost.

Each criterion carries three declarations:

| Field | Meaning |
|---|---|
| **Target / Minimum Score** | the declared bar this criterion is measured against |
| **Category M / D** | Mandatory (fatal class) or Desirable |
| **Weighting Factor** | OPTIONAL — another mechanism for when the evaluation needs it; absent means criteria weigh equally |

**Verdict per option per criterion — the Toyota marks:**

| Mark | Meaning | Consequence |
|---|---|---|
| **○** | meets the requirement, no countermeasure needed | scores |
| **△** | meets the requirement only WITH a countermeasure | countermeasure NAMED, with a CONFIDENCE statement; if temporary, its return condition — recorded in the risk ledger |
| **×** | cannot meet it, and no countermeasure available | on an M criterion: the option is DEAD, regardless of overall score |

**Scoring — the arithmetic that makes the comparison honest.** The marks
carry the risk semantics; the scores carry the comparison. The mechanisms
layer in as the evaluation needs them: **marks always** · **scores** when
options are close or the stakes are real · **weights** only when criteria
genuinely differ in importance:

- **Score per criterion per option** on the declared scale (1–5 in the
  exemplars), or measured directly against the target where the criterion
  is numeric.
- **Weighted contribution = score × weighting factor**; **OVERALL = the
  weighted sum**; **RANK** orders the options.
- **Weights and targets are declared BEFORE any option is scored** — set
  with the criteria, never after seeing the candidates. A weight tuned
  after scoring is the evaluation fitting the answer.
- **Every score cites its basis** — a test, an analysis, a document. A
  score without evidence is an assertion wearing a number.
- **Scores never overrule marks**: the highest OVERALL with an × on an M
  criterion is still dead. Rank decides among the living.

**Then the closing sections** in the exemplar's order: **Preferred
Solution** (the banner) · **Proposal & next steps** · **Risks /
countermeasures required** · **Countermeasures per option, each with
confidence**.

## Where the output goes

- The winning approach + the filled matrix enter the **design package**;
  the GO gate record references the matrix.
- **The losing options go to *What we ruled out*** — the matrix row is the
  evidence, the elimination is by analysis, and each carries its return
  condition. An evaluated-out option is a ruled-out concept by
  construction; capture is a byproduct of the evaluation itself.
- Every △'s countermeasure lands in the risk ledger with its confidence
  and return condition.

## Rendering

A movement-9-style table via the diagram toolkit (`tools/diagram/`) —
never a spreadsheet. The instrument is `tools/design/matrix.py`: `check`
validates a matrix section, `audit` sweeps every living design doc on
every push (the CI instance), `render` draws the table to Excalidraw +
SVG beside the doc. The section format standard is
`tools/design/README.md`. The matrix is an everyday-tier render during
the design conversation; the design package's copy is part of the package
document.
