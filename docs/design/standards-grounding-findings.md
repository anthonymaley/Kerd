# Standards grounding spike — findings

Run 2026-08-22. Frame, candidate map and kill-or-keep criteria:
`docs/product/standards-grounding.md`. Three research players, one per
ungrounded area (process · product · the two requirements extras), each
required to fetch real sources and tag every verdict with its evidence tier.
The judgement against the criteria is the conductor's; the producer's
agreement is what turns a verdict into a decision.

**Findings only. Nothing here is adopted.** Each `adapt` verdict below is a
separate small change that re-enters the ladder on its own.

## The scorecard — 4 of 4 layers can name a standard, two by adaptation

| Layer | Standard | Verdict | Evidence tier | What Kerd would stand on |
|---|---|---|---|---|
| architecture | ISO/IEC/IEEE 42010 | **adopted** (2026-08-22, `docs/design/gate-visuals.md`) | — | its completeness rule |
| requirements | ISO/IEC/IEEE 29148 | **adopted** (`docs/design/requirement-shape.md`) | — | plain-language wording, the `each` rule |
| requirements | ISO 9241-210:2019 | **adapt** — its *output categories*, not its process | full text | §7 + Table 1 |
| requirements | ISO/IEC 26550 | none fits — killed on criterion 1 | scope + secondary; 26580 full text | — |
| process | ISO/IEC/IEEE 24774:2021 | **adapt** — a three-field header above every skill | full text | §5.3 |
| process | ISO/IEC/IEEE 12207 | none fits — killed on criterion 2 | scope + secondary | — |
| process | BPMN 2.0 / ISO/IEC 19510 | none fits — killed on criteria 1 and 2 | full text (ch. 1–2) | — |
| product | ISO/IEC 25010:2023 | **adapt** — a checklist *behind* the quality column, never columns | **scope + secondary only** | the nine characteristics |
| product | ISO/IEC/IEEE 15289 | none fits — the gap is already filled, tighter | scope + secondary | — |
| product | ISO 10007 | none fits — killed on all three, incl. criterion 3 (`R-0042`, `R-0043`) | scope + secondary | — |
| product | ISO/IEC/IEEE 24748 | not a product-layer standard — it is process vocabulary; **untested** there | scope + secondary | — |

**Winning, measured:** the frame said 2 of 4 layers grounded. After the
spike, every layer can point at a standard — architecture and requirements
adopted, process and product by adaptation. **4 of 4 — pending the producer's
agreement on the two adaptations.**

## The verdicts that carry a decision

### Process — ISO/IEC/IEEE 24774: three fields, and a finding about what a skill is

Read in full. Its scope is exactly the gap: *"requirements and recommendations
for the description of processes by identifying elements and rules for their
formulation."* The minimum for conformance (§5.3) is **three elements: name,
purpose, outcomes** — lighter than what a `SKILL.md` already carries
informally, which is why Law 2's ceremony limit does not bite. Everything else
(§5.4: activities, tasks, inputs, outputs, controls) is optional.

**What it disclaims, which bounds the adaptation:** it does not say how
processes compose into a life cycle (§1) and does not assess performance. So it
grounds *how a skill describes itself*, never the ladder's rung order — that
stays `gate.py`'s own mechanism — and never whether a skill ran well.

**The finding underneath:** §5.2 — *"Procedures differ from process
descriptions in that procedures are written in steps to be followed in order…
ISO/IEC/IEEE 82079-1 provides detailed requirements for writing instructions."*
Kerd's skill files are **procedures** in the standard's own vocabulary. 24774
governs the purpose-and-outcomes header; the step body underneath is a
different information item with a different standard. 82079-1 surfaced, was
not read, and is not on the map — it is the process layer's second candidate if
the header adaptation lands.

**Term mapping:** 24774 does not redefine *viewpoint* — §3.22 Note 2 reads
*"For a detailed explanation of view and viewpoint… see ISO/IEC/IEEE 42010"*.
It imports the term. *Stakeholder* and *concern* have no counterpart among its
22 defined terms; *process purpose* runs the opposite direction from a concern
(the process's own objective, not an external party's interest in it).

### Product — ISO/IEC 25010: the matrix had already decomposed quality without saying so

**Evidence tier is the weakest in the spike and it matters here:** every ISO
mirror of the 2023 text refused the fetch; the characteristic list below is
corroborated across three secondary sources, which disagree on one
sub-characteristic (whether *accessibility* was folded into *inclusivity*). The
nine characteristics: functional suitability · performance efficiency ·
compatibility · interaction capability (was *usability*) · reliability ·
security · maintainability · flexibility (was *portability*) · safety (new in
2023).

**The concrete test the frame asked for** — re-scoring
`docs/design/requirements-traceability.md`'s quality row against 25010 — came
back with the real finding: **the matrix's own criteria table had already
split "quality" into four or five of 25010's characteristics under its own
names.** *Human-readable with no tooling* is interaction capability;
*Maintenance and survival* is maintainability; *Git-repo native* and
*Machine-readable by stdlib* are compatibility; the `expressiveness` and
`doctrine` groups are functional suitability. The summary column's own row
definition is narrower still — *"solves the whole need rather than a part of
it"* — which is functional completeness alone.

So the adaptation is a **definition, not a restructuring**: `R-0011`'s quality
column means *a mark against whichever of the nine characteristics this
evaluation declared relevant*, with the characteristic list consulted before
the mark is written. It is never nine columns — `R-0012` and `R-0033` bind a
cell to a few words, and criterion 2 kills any version that expands the table.
25010 supplies vocabulary the matrix was already using without a name, which
is precisely the invention-where-a-standard-exists cost the frame measures.

**Surfaced, and a better fit for what `tools/design/` actually does:**
ISO/IEC 25040:2024, the SQuaRE *evaluation process* — establish evaluation
requirements → specify → design → execute. The matrix format standard
(declare criteria before scoring · mark against a target · arithmetic ·
preferred-solution write-up) is that process, reinvented. Not read; on the map
for the product layer's second pass.

### Requirements — ISO 9241-210: it justifies the UI concern and cannot supply the viewpoint

This is the finding `gate-visuals` was held for, and the answer is **no**.

Read in full. 9241-210 is a *process* standard and says so twice: *"does not
assume any particular design process"* (§5.1) and *"does not provide detailed
coverage of the methods and techniques for design"* (§1). Its Table 1 names
output *categories* — user group profiles, as-is scenarios, personas, user
requirements, scenarios of use, low- and high-fidelity prototypes, a UI
specification, evaluation reports — and supplies a drawing convention for none
of them. No wireframe grammar, no persona template, no screen-layout notation.

In 42010's terms that is the whole problem: a viewpoint is *"the conventions
for the creation, interpretation and use of a view"*, and 9241-210 has no
counterpart for the term at all. It establishes **that** a UI concern belongs
on a design's concern list, and that is real and worth adapting (Table 1 as the
category vocabulary). It cannot close `gate-visuals` open question 1, because
closing it needs layout rules to obey — the toolkit's own operator rule — and
no ISO standard defining a wireframe or screen-layout grammar surfaced in the
search. **Closing the UI viewpoint gap is a build** (Law 4 step 5), borrowing
notation from design practice rather than a standard.

Against the 39 toolkit types: *scenario / as-is* is already `journey`.
Persona, prototype, wireframe and UI specification are not among the 39.

## The one-vocabulary hypothesis — killed as stated, and something truer survives

The producer's hypothesis: *"42010's concepts (stakeholders, concerns,
viewpoints) are general enough that people often reuse them to organize the
other layers too"* — if so, one vocabulary covers four layers.

The kill rule, declared at frame: killed if mapping any grounded layer onto the
four terms needs a term the standard does not have, or bends one past its
definition.

| Layer's standard | stakeholder | concern | viewpoint | view |
|---|---|---|---|---|
| 24774 (process) | **no counterpart** | **no counterpart** (purpose runs the other way) | direct — imported from 42010 | direct |
| 25010 (product) | bent — lives in SQuaRE's separate quality-in-use model | direct — a characteristic | reasonable — a characteristic's measurement approach | direct — the mark |
| 9241-210 (requirements) | direct — §3.11 | bent — names the subject matter, never the category | **no counterpart** | bent — categories without conventions |
| 29148 (requirements) | **not tested** — no player mapped the already-adopted standard; a gap in this spike, named rather than filled | | | |

**KILLED.** Two of the three grounded standards lack a counterpart for at least
one term, and one lacks two. One vocabulary does not *replace* four.

**What survives, and it is the more useful shape:** 42010 is the vocabulary the
others **import**. 24774 does not define *viewpoint*; it points at 42010. A
25010 characteristic *is* a concern, cleanly. So the four layers do not share
one vocabulary — they share one **spine**: *view* and *viewpoint* are 42010's
everywhere they appear, and *stakeholder* and *concern* are supplied per layer
by the layer's own standard. That is a smaller claim than the hypothesis and,
unlike it, it is what the texts actually say.

## What the spike did not do

- **Did not read 25010's full text.** The live adaptation rests on the weakest
  evidence in the spike. Before the `R-0011` definition is written, one
  reliable full-text source for the nine characteristics is owed.
- **Did not map 29148** onto the four terms, so the requirements layer's own
  adopted standard sat out the one-vocabulary test.
- **Did not assess the three that surfaced** — 82079-1 (procedures), 25040
  (evaluation process), 24748 (life-cycle stages, misfiled under product on the
  map). Each is on the map for a second pass, none was read.
- **One player grepped the wrong tree** — looked for `process` and `swimlane`
  in `tools/diagram/` instead of the toolkit's type list, and reported a
  discrepancy in the frame that does not exist (`docs/design/diagram-types-by-rung.md:56,65`).
  Caught on review; the frame is correct. Same class as the 2026-08-08 finding:
  reading the label is not reading the thing.

## Kept — what re-enters the ladder, each as its own item

1. **ISO 25010 → the definition of `R-0011`'s quality column.** A definition,
   not a restructuring. Smallest; needs one full-text source first.
2. **ISO/IEC/IEEE 24774 §5.3 → a name / purpose / outcomes header on every
   `SKILL.md`.** Three fields. Brings the finding that skills are procedures,
   and names 82079-1 as the next thing to read for the step bodies.
3. **ISO 9241-210 Table 1 → the UI concern is real, and its viewpoint is a
   build.** Feeds `gate-visuals` open question 1 with an answer: *no standard
   supplies it.* The design GO can now be taken with that gap named rather
   than open.
4. **The spine, not the vocabulary.** 42010 is where *view* and *viewpoint*
   come from at every layer; the other two terms are per-layer. One sentence,
   for `docs/design/gate-visuals.md`'s 42010 section.
