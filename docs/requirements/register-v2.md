# Requirements — Kerd

Written against the normative form in `docs/design/requirement-shape.md`.
Findings about this set live beside it, in `docs/requirements/findings.md`:
under rule 13 the register holds the requirements and the graveyard and
nothing else, and the graveyard is last.

**This file is a migration, not an authorship.** Every block below was
transcribed from the previous register's 51 requirements. The old
identifiers are not carried — not as references, not as aliases. Under the
producer's ruling of 2026-08-14 (*"absolutley ignore the past, move to the
future"*) the old scheme dies with the old register; git history holds it.
References here are freshly minted under rule 2, in the old register's
reading order, which is the only creation order a migration has.

**Where the set stands — 2026-08-14, after two rounds of kills.** Fifty-one
requirements were migrated into a register with an empty graveyard.

*First round, on the recommendations in `docs/requirements/triage.md`:* **eight
were killed and moved to `## Graveyard`** — R-0001, R-0002, R-0004, R-0016,
R-0017, R-0034, R-0039 and R-0045 — each with Tony as the named authoriser
under rule 10. One replacement was minted, **R-0052**, which carries forward
the visibility intent underneath R-0039. That left 44 live.

*Second round, 2026-08-14 14:54, on three rulings Tony authorised after the
research he commissioned* (the second round of `docs/design/requirements-prior-art.md`):
the twenty subject areas are dead; twelve work types collapse to the one
distinction between work that ships a change and work that produces a finding,
which changes the definition of done and nothing else; and the nine-link
traceability chain is dead, leaving only the requirement → goal link the shape
already carries. **Five more were killed** — R-0003, R-0019, R-0022, R-0025 and
R-0037 — and **six were reworked in place**, keeping their references: R-0005,
R-0018, R-0020, R-0021, R-0026 and R-0048. **The live set therefore holds 39
requirements and the graveyard holds 13.** No reference was minted in this
round and none was reused.

**The live numbering has gaps, and the gaps are correct.** Rule 2 forbids a
reference from ever being changed or reused, so nothing was renumbered when the
thirteen left — the live set simply has no R-0001, R-0002, R-0003, R-0004,
R-0016, R-0017, R-0019, R-0022, R-0025, R-0034, R-0037, R-0039 or R-0045 in it.
The graveyard is what makes that rule observable: a reader who finds a number
missing from the live set finds it at the end of this file, taken, with the
reason it went and what to take from it. A set with no gaps would mean either
that nothing had ever been killed or that a number had been quietly reused.

**Six statements are no longer the migrated wording, and each says so on its
own block.** A rework keeps the reference, keeps the block in the live set, and
records the change in place: the previous statement quoted whole, the ruling
that authorised the change, the evidence behind it, and the date. Nothing was
reworded quietly. The rework note is written as prose beside the five required
fields, not as a sixth field — the same shape R-0035's re-pointing note took.
None of the six carries an invented Why: an authorised ruling says what the
requirement must now say, not why it exists, and the two are different things.

**Every dependency in the live set resolves, checked after the second round.**
Nine blocks declare a dependency — R-0007, R-0009, R-0010, R-0012, R-0015,
R-0020, R-0021, R-0028 and R-0049 — carrying ten references between them, and
every one points at R-0008, R-0011, R-0014, R-0018 or R-0041, all live. No kill in this round created a dangling
reference, because everything that hung on the type vocabulary hung on R-0018,
which was reworked rather than killed. One coupling was removed rather than
repaired: R-0048 no longer depends on R-0018, because its reworked statement
asks about no type — recorded on its own block. The earlier dangle is closed
too: R-0035 was re-pointed when R-0034 died, and that fix is recorded in place
on R-0035 along with the residue the kill left behind.

**Every requirement lands unapproved, deliberately.** The old register carried
approval fingerprints over the statement alone. The new fingerprint covers
statement, Why and links, and the Why is content that did not exist before —
so no old approval can survive, however careful the transcription. No
fingerprint below is computed and no old hash is carried across.
Re-approving the whole set in one sitting is the textbook
approval-fatigue scenario the Law 4 research documented; each is approved
when work touches it and the producer is reading it anyway.

**Statements are carried verbatim, except the six the producer's rulings
reworded.** The migration itself reworded nothing, and still does not: where a
statement fails the adopted plain-language word list, that is recorded in
`docs/requirements/findings.md` rather than silently corrected, because rewording approved
statements on the migration's own initiative is authorship and it is his call.
The six reworded on 2026-08-14 14:54 are the exception the rulings made, and
they are not silent — each block quotes its previous statement whole and names
the ruling that changed it. Finding 3's word-list table still describes the
statements as they read before that round; R-0003's row in it is now a
graveyard entry.

**Cleaned to the parsing rules, 2026-08-14, and no statement was touched.**
The first tool to read this file mechanically found three format defects the
writing tests never could, and the shape document answered them with three
rules. This file was converged onto them in one pass: eight in-place notes on
seven blocks — the six rework notes, R-0035's re-pointing and the residue it
names — are now blockquotes marked `> **Note — …**` and sit after the five
fields, where no wrapped bold line can be read as a field label (rule 1);
R-0031's `Traces to` carried a sentence, which split on its own comma into a
trace target that did not exist, and now reads `not yet traced`, with the
explanation moved into its Why (rule 7); and the `## Findings` section that
sat between the requirements and the graveyard moved whole into
`docs/requirements/findings.md` (rule 13). **The only field text that changed
anywhere in the file is R-0031's `Traces to` and `Why`**, so R-0031 is the one
block whose fingerprint would move — and nothing here is approved, so no
approval broke. No statement was reworded, no Why was invented, no reference
was renumbered.

**Machine names are absent by design.** Rule 4: nobody hand-writes one. The
checking tool mints and inserts them on its next run.

**Where a Why could not be honestly written it says so.** Forty-six migrated
blocks carry an unwritten Why, because their migrated source recorded
provenance and nothing else. No rationale is invented anywhere in this file,
and the kills of 2026-08-14 invented none either — a dead requirement's
`Why it was proposed` says that no reason was ever recorded, exactly as the
live block did. All forty-six are listed in `docs/requirements/findings.md`; **thirteen of them
are now in the graveyard, so thirty-three live blocks await his words.** The
six statements reworked on 2026-08-14 14:54 are among those thirty-three: a
ruling that says what a requirement must now state does not say why it exists,
so no Why was written for any of them and none was invented. R-0052, the one
block written rather than migrated, carries a real Why.

## Requirements

### R-0005 — Every piece of work either changes the product or answers a question

**Statement.** Work shall carry one distinction and no other: does it change the product, or does it answer a question. That distinction shall set what finished means. No gate, approval or template shall depend on it

**Why.** a clear and obvious way to measure and judge the quality of the output.

**Traces to.** G3

**Depends on.** none

**Approval.** Tony, 2026-08-15 · fp:098ae5e0676d

> **Note — Reworked 2026-08-14 14:54, on the producer's authorised ruling.** The statement
> read *(verbatim, as migrated)*: "Project type and release type are the same thing
> for the twelve types that ship; Ideation, Spike and Security Review produce
> findings instead". The twelve-type list is dead; the findings-versus-ships-a-change
> distinction inside it is what the ruling kept, so this block is reworked rather
> than killed and its reference is unchanged. The second research round Tony
> commissioned found human type assignment unreliable and the structure without
> prior art — Herzig, Just & Zeller (ICSE 2013) measured "33.8% of bug reports
> misclassified" across 7,000+ manually reviewed issue reports; "Scrum has zero work
> item types"; Shape Up "refuses them too"; and SAFe's Enabler, "the type closest to
> our 'produces findings' idea, changes nothing procedurally", its own text calling
> enablers "treated and managed similarly to customer-facing backlog items". What
> recurs everywhere is one axis — "discovery versus delivery" — and "what it changes
> is **the definition of done, not the pipeline**". The statement's final clause is
> the ruling's second half, written into the statement so a build can be rejected
> against it: a gate or template keyed to the distinction is a defect, not a design.

---

### R-0006 — A design is agreed by both people looking at the same structure

**Statement.** Before a design is agreed, the producer and the model shall both be able to point at the same structure. A drawing is the usual form of that structure, but it is not the only one

**Why.** high level box and line visuals can convey meaning faster than 1000 words on a screen, use the visuals to align and agree

**Traces to.** G1, G4

**Depends on.** none

**Approval.** Tony, 2026-08-15 · fp:630ca2a88559

---

### R-0007 — Other tools read the register to plan releases and draw views

**Statement.** The register is the data source for release planning, dependency and visualization tooling — not merely a record

**Why.** the requirements are what lead to features, design, architecture and eventually plans that dictate release schedules and roadmaps. the register though is not the place to do that work, it form the foundation for all of it.

**Traces to.** G5

**Depends on.** R-0041

**Approval.** Tony, 2026-08-15 · fp:d064fcbc0922

---

### R-0008 — There are four evaluation marks

**Statement.** Evaluation for choices, features, technology, services that we want to consider to build the project shall use simple and clear evaluation methods. An evaluation shall use one set of marks. `◎` means perfect. `○` means it fully meets the criterion, and can carry a plus or minus. `△` means it meets the criterion only with a countermeasure, and can carry a plus or minus. `×` means it cannot meet the criterion

**Why.** visual indications of rating are easy to see and understand vs numbers, we can see x and know the option is not viable

**Traces to.** G4

**Depends on.** none

**Approval.** Tony, 2026-08-15 · fp:c9460fd63e18

---

### R-0009 — A cross in an evaluation has no plus or minus version

**Statement.** within evaluation matrix ratings, Where an option cannot meet a criterion even with a countermeasure, the evaluation shall mark it `×`. A cross shall carry no plus or minus, because there is no degree of impossibility

**Why.** make it clear for evaluator to declare a feature or category or capability as not viable. and a final rating is declared.

**Traces to.** G4

**Depends on.** R-0008

**Approval.** Tony, 2026-08-15 · fp:83537d6b6b6c

---

### R-0010 — Building the missing piece ourselves counts as a countermeasure

**Statement.** During Evaluation matrix, where an option's gap can be closed by building the missing piece ourselves, the evaluation shall count that as a countermeasure and mark it `△`, `△+`, or `△ -`". based on the effort or size of the countermeasure to fill the gap to fully meets the criteria. The actual monetary cost or quality of countermeasure shall be shown in the summary columns rather than hidden inside the mark

**Why.** surface the cost and quality of the countermeasures appropriately.

**Traces to.** Law 4, G7

**Depends on.** R-0008, R-0011

**Approval.** Tony, 2026-08-15 · fp:2da4c569b118

---

### R-0011 — Every evaluation has the same four summary columns

**Statement.** Every evaluation shall carry four summary columns: cost, quality, due date, and rating

**Why.** standardized columns make it easier to see cost and quality, time to deliver and an overall rating across multiple evaluations.

**Traces to.** G4

**Depends on.** none

**Approval.** Tony, 2026-08-15 · fp:62d8c9e4e682

---

### R-0012 — Any mark below a circle says why

**Statement.** For each evaluation mark,, the evaluation column text shall say why in a few words rather than in sentences.

**Why.** eval matrix should be easy to understand, for every rating quickly and easily.

**Traces to.** G4

**Depends on.** R-0008

**Approval.** Tony, 2026-08-15 · fp:2566f655b460

---

### R-0013 — What a tool costs is what it adds beyond what we already use

**Statement.** An evaluation shall judge the cost of adding something by what it brings beyond what the project already needs, weighed against how much of the value it buys. Something the ecosystem installs as a matter of course shall not count as a burden. A whole new runtime bought for a small part of the value shall

**Why.** we need to understand total cost of solutions.

**Traces to.** Law 4, G7

**Depends on.** none

**Approval.** Tony, 2026-08-15 · fp:1af9e1a3df8c

---

### R-0014 — Approving the design is the only approval needed to build

**Statement.** Approving the design shall be enough to proceed, and there shall be no separate plan approval

**Why.** requirements > analysis, architecture and UI design all in place, then build can proceed, spec and planning can be done in the loop or by the conductor and composer

**Traces to.** G1, G3

**Depends on.** none

**Approval.** Tony, 2026-08-22 · fp:5293470c167f

> **Note — Discuss: explain** what about specs and plans etc?

---

### R-0015 — A plan carries out a design that is already approved

**Statement.** A plan shall carry out a design that has already been approved, and shall carry the measurements that prove the goals were met

**Why.** the design must have the measurements that prove the goals were met

**Traces to.** G6

**Depends on.** R-0014

**Approval.** Tony, 2026-08-22 · fp:a8caa1be7008

---

### R-0018 — Whether work changes the product or answers a question is decided once, at the start

**Statement.** Whether a work item changes the product or answers a question shall be decided once when conductor starts, and shall not be asked again after the work has begun

**Why.** to reduce overthinking and constant asking, the question is answered once, at the start

**Traces to.** G1

**Depends on.** none

**Approval.** Tony, 2026-08-22 · fp:96c90bf8f2f9

> **Note — Reworked 2026-08-14 14:54, on the producer's authorised ruling.** The statement
> read *(verbatim, as migrated)*: "Project type is declared once at conductor start,
> from the list, and not re-asked once a project has started". "from the list" was
> the twelve-type list, which is dead. The live payload is the anti-nagging rule —
> asked once, never re-asked — and it applies unchanged to the one distinction that
> survives (R-0005). Only the subject of the declaration changed.

---

### R-0020 — Conductor can say the work has changed type, but the producer decides

**Statement.** Conductor may say that a work item has changed type, either at a gate or during the work, and the producer shall decide

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G1, G5

**Depends on.** R-0018

**Approval.** none — migrated 2026-08-14 and reworked the same day; the Why is unwritten, the statement is no longer the migrated wording, and no earlier approval covered any of it.

> **Note — Reworked 2026-08-14 14:54, on the producer's authorised ruling.** The statement
> read *(verbatim, as migrated)*: "Conductor may suggest a type change — at the gate
> or mid-flight — and the producer agrees it". The payload is who decides, not what
> is decided: a change to how a work item is classified belongs to the producer
> rather than to the model's discretion. That holds over the one surviving
> distinction exactly as it held over twelve types. "the gate" became "a gate"
> because the definite article pointed at the goal gate of R-0019, now dead.

> **Note — Discuss: kill?** duplicate

---

### R-0021 — Work inside other work inherits its type

**Statement.** A work item shall inherit the type of the work that contains it. Changing that shall be a deliberate choice, and shall apply only to the work that follows

**Why.** simple execution, reduce overthinking and the avoid the use of sub categories with work.

**Traces to.** G3

**Depends on.** R-0018

**Approval.** Tony, 2026-08-22 · fp:de1fe3a19ba1

> **Note — Reworked 2026-08-14 14:54, on the producer's authorised ruling.** The statement
> read *(verbatim, as migrated)*: "Type is a stack: items inherit the project's type,
> an override is opt-in and forward-only". Inheritance with an opt-in, forward-only
> override is not machinery keyed to type — it is how the value of the one surviving
> distinction is determined for nested work, and it is the only rule in the set
> covering nesting at all. A spike inside a shipping project is the case it exists
> for. Only the noun changed.

---

### R-0023 — Conductor picks the right model and effort, up or down

**Statement.** Conductor shall manage which model runs and at what effort, in both directions. A session running a model that is too powerful shall be advised down to the right one, and other models shall then be called for individual steps at the effort those steps need. conductor should not try to achieve powerful work with lesser models and vice versa..

**Why.** ensure we are not under or over-specifying agent effort and mode type and work is performed at appropriate levels always

**Traces to.** G7

**Depends on.** none

**Approval.** Tony, 2026-08-22 · fp:521634c50898

---

### R-0024 — The boundary records everything that was agreed

**Statement.** The boundary shall record each thing agreed. Where two ways of doing that would both keep the whole record, the cheaper one shall be chosen. Saving effort shall not be a reason to record less. The goal is quality at the most efficient cost.

**Why.** we need to ensure the recoding of agreements to avoid re-inventing and redoing effort the next time we touch that item

**Traces to.** G2, G7

**Depends on.** none

**Approval.** Tony, 2026-08-22 · fp:b9408f0581a8

---

### R-0026 — Work that answers a question still needs the same rigor

**Statement.** Work that answers a question shall carry its own rigor: a scope boundary, a time limit, a spec, a design, and measurements

**Why.** spikes and other question-answering work requires rigor just like any other work. we do it right.

**Traces to.** G3

**Depends on.** none

**Approval.** Tony, 2026-08-22 · fp:7bd1abed6fe4

> **Note — Reworked 2026-08-14 14:54, on the producer's authorised ruling.** The statement
> read *(verbatim, as migrated)*: "A spike carries its own rigor: scope boundary,
> timebox, spec, design, and measurements". "A spike" was one of the twelve dead
> types, so the statement silently keyed itself to a list that no longer exists —
> the failure mode that gets no flag, because the dead word is not the dead
> structure's name. What it says is the definition of done for the findings side of
> the one surviving distinction, which is the single thing that distinction is
> allowed to change. Restated over the distinction, it survives whole and gains
> reach: every piece of findings work owes this, not only the one that used to be
> called a spike.

---

### R-0027 — The tools keep a project's files where they belong

**Statement.** The tools shall not scatter a project's files

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G5

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0028 — In the matrix the mark is coloured and the box is not

**Statement.** Where the render is the evaluation matrix, the box shall stay uncoloured and the mark shall carry the verdict: `○` green, `△` yellow, `×` red

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** R-0008

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0029 — A mark fills about half its cell

**Statement.** Where the render is the evaluation matrix, a mark shall be drawn at 40 to 50 per cent of the cell it sits in

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0030 — Headings look like headings

**Statement.** Where the render is the evaluation matrix, the column and row headings shall be rendered as headings, written as `GROUP: CRITERION NAME` and `OPTION n: ID`, with the declaration underneath

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0031 — Diagrams use a sans-serif font

**Statement.** A rendered diagram shall use a sans-serif font

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here. The trace is unresolved for the same reason and is recorded here rather than in the field, under rule 7: no goal and no law is served by this statement without inventing a rationale for it, and the migration will not — see finding 2 in `docs/requirements/findings.md`.

**Traces to.** not yet traced

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten, the trace is unresolved, and no earlier approval covered either.

---

### R-0032 — The preferred option's verdict cell is filled green

**Statement.** Where the render is the evaluation matrix, the verdict cell of the preferred option shall be filled green

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0033 — A table exists so you do not have to read a lot of text

**Statement.** A table shall be understandable without reading a lot of text. Brevity is a requirement, not a preference

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0035 — Marks made on an out-of-date page are rejected

**Statement.** A generated page shall carry the fingerprint of the state it was rendered from, and a mark made against an out-of-date page shall be rejected rather than applied

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

> **Note — Re-pointed 2026-08-14, as a consequence of an authorised kill.** This declared
> `Depends on. R-0034` until R-0034 was moved to the graveyard, which left an
> unresolved reference — the error its own graveyard entry predicted. The
> dependency was **incidental rather than real**: this requirement guards a
> generated page against accepting marks made from a stale render, and that guard
> holds whatever a page lets a reader mark. It needed R-0034 only because R-0034
> happened to be the marking interface first written down.

> **Note — Unhomed by that kill, and named here rather than lost:** R-0034's live half —
> marking on the page, saved to a file, applied later — survives its own death.
> The producer agreed that mechanism on 2026-08-14 08:20 as the first step:
> *"ideally directly to reduce overhead for many requirments but we can start with
> a paste option while we build the proess and ui out if you want as a first
> step"*. No live requirement carries it. Same residue shape as R-0002's *plan
> releases*.

---

### R-0036 — A project's own repository holds its information, not Kerd

**Statement.** The user's own repository shall hold the funnel state, the requirements, the stage data, the steps and the journey. Kerd shall hold none of a project's information

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0038 — The tools work on the project you are in, not on where they were installed

**Statement.** The tools shall work on the project they are pointed at, rather than on the folder they were installed into

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1

**Depends on.** none

**Approval.** none — and this one was **never approved under the old rules either**: it stood at `qualified`, not final, when the register was migrated on 2026-08-14. It has never been agreed by anyone. The Why is unwritten.

---

### R-0040 — The register is its own file, in a known place

**Statement.** The register shall be a file of its own in a known place, so a person can read it quickly and a tool can read it directly. A product document shall not contain it

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G5

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0041 — A requirement lists what it depends on

**Statement.** A requirement shall list the other requirements it depends on, by reference

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G5

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0042 — The mechanism works inside a git repository, one project at a time

**Statement.** The mechanism shall work inside a git repository, shall suit Claude Code, and shall operate one project at a time

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0043 — There is one copy of the register and no second store

**Statement.** The register shall be the same files the project already keeps. There shall be one copy, and the tooling shall not keep a second store alongside it

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1, G2

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0044 — A requirement can be copied out whole, in one piece

**Statement.** A requirement shall be written as one block rather than a row in a table, with a heading, its labelled lines, the requirement itself as text, and its links at the end. It shall be possible to copy the whole thing somewhere else without putting it back together

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0046 — You need a conductor session to work the funnel

**Statement.** Working with the funnel shall require a conductor session. Questions, reports and admin work shall stay available outside one

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G1

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0047 — The plan shows it kept the measurements from the design

**Statement.** A plan shall check that it carried the design's measurements across accurately, and shall show that check

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 3, G6

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0048 — Every work item owes every gate unless it says why not

**Statement.** Every work item owes every gate unless it explicitly marks that gate `n/a` with a named reason

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** none

**Approval.** none — reworked 2026-08-14 and **never approved under the old rules either**: it stood at `proposed`, not final, when the register was migrated. It has never been agreed by anyone, the Why is unwritten, and the statement is no longer the migrated wording.

> **Note — Reworked 2026-08-14 14:54, on the producer's authorised ruling, and its
> dependency dropped in the same edit.** The statement read *(verbatim, as
> migrated)*: "Every project type owes every gate unless that type explicitly marks
> it `n/a` with a reason". Two things sat inside it. The dead one is gate
> applicability keyed to type — the research is explicit about refusing "approval
> gates keyed to type", and the ruling says the distinction changes the definition
> of done and nothing else. The live one is the obligation itself: a gate is never
> skipped silently, and an excused gate names its excuse. That obligation is
> load-bearing and now unique — R-0004 was killed on 2026-08-14 as a duplicate of
> this block, so killing this one would have taken the declared-applicability rule
> out of the set entirely with nothing left carrying it. Reworked onto the work item,
> it binds without a type vocabulary. **Depends on** went from `R-0018` to `none` in
> the same edit: R-0018 was needed only to supply the type being asked about, and
> the reworked statement asks about no type. R-0018 is live, so this is a false
> coupling removed rather than a dangling reference fixed.

---

### R-0049 — Evaluations score the due date, not the effort

**Statement.** An evaluation shall score whether an option can meet the plan in time, which is a measure of the outcome, rather than how much work it is, which is a measure of the input

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G6

**Depends on.** R-0011

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0050 — The quick check runs at every step, the full check at the design gate

**Statement.** The completeness check shall have two levels. The quick check shall run at every step and shall use machine facts only: did the register move, do the approval fingerprints still match, are the link stamps out of date, and does the reading a document declared still exist. The full check shall run at the design gate alongside the quick one, and shall use several independent readers working from the original sources rather than from a summary, with agreement between them as the signal

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 3

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0051 — The check relies on facts the model cannot make up

**Statement.** A completeness check shall be settled by countable facts produced outside the model, so the model can neither assume it nor skip it. It shall not rest on a question the model answers about itself

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 3

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0052 — Kerd shows how each step was done

**Statement (derived).** Kerd shall show the producer, for each step of a work item's journey, what the step was, which mechanism did it, what that mechanism was given, and what it produced. Kerd shall not hand a step to a mechanism that cannot supply those four facts

**Why.** This block replaces R-0039 (*"Never route to superpowers"*), killed 2026-08-14 for foreclosing the build-versus-adopt decision the approved goals keep open. The intent underneath it survives, and these are his words for it, from the G8 grounding in `docs/kerd-goals.md`: *"superpowers does some great things... so we can learn from it, i just want the process to be ours and visable"*. G5 carries the same want as a design input — *"show the work, show the state, show the tools being used"* — and names the failure it prevents: *"its not clear what or why its doing in a black box way"*. **The statement is the model's derivation of a checkable obligation from those words; approving this block approves that derivation.** What the derivation deliberately does not do is name a tool: the test is what a mechanism can show, so any mechanism that meets it is admissible and any that does not is refused — including one we build ourselves. That keeps the decision Law 4 protects open while the visibility his words demand is binding.

**Traces to.** G5, G8

**Depends on.** none

**Approval.** none — drafted 2026-08-14 as the replacement for R-0039. **The statement is the model's draft and awaits the producer's approval; the kill it replaces is authorised, this wording is not.**

---

## Graveyard

*Thirteen entries, from two rounds on the same day, and Tony is the named
authoriser on every one. Eight were killed earlier on 2026-08-14 on the
recommendations in `docs/requirements/triage.md`; five more — R-0003, R-0019,
R-0022, R-0025 and R-0037 — at 14:54, on three rulings he authorised after
research he commissioned, and their instrument is analysis in every case:
superseded by that research, not by a test and not by a ruling on the
requirement's own merits. The purpose is his, verbatim, 2026-08-14 09:28:*
**"we need a graveyard so we dont add them again and learn from them"** *— which
is why the* **What was learned** *field is written as guidance to the next
proposer rather than as a summary of the death. Links are dropped on death, per
rule 10.*

*Three of the second round's entries name a* **residue** *inside* **What was
learned** *— a binding fragment that outlived its dead host and that no live
requirement now carries: R-0003's rule that projects extend the shipped default
rather than inventing their own, R-0022's obligation not to ask the producer to
size the rigor of their own work, and R-0025's guard against nesting laundering
rigor away. They join the two already recorded — R-0002's* plan releases *and
R-0034's marking mechanism, the latter named on R-0035 rather than here.*

*(The reserved italic-quotation form of rule 6 is used below for the
producer's verbatim words and for nothing else. Words belonging to the goals
record, the shape document, or the research survey are in plain quotation
marks and attributed to their source.)*

### R-0001 — DEAD — Kerd is the supplier, not the subject

**Killed.** 2026-08-14, by analysis against the approved goals — the triage of the migrated register against `docs/kerd-goals.md`, not by a test and not by a ruling on this requirement specifically. Kill authorised by Tony.

**Statement as proposed.** Kerd gives consuming projects this capability; Kerd is only a user of it

**Why it was proposed.** Never recorded. The migrated source (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) carried a provenance pointer and no reason, and none was invented at migration or here. What the statement asserts is the repository boundary — the same boundary Law 1 states.

**Why it is dead.** It restates its own law. Law 1 in the approved goals reads: "Kerd installs into a user's own project and operates inside that repository's boundaries; the Kerd project never holds sessions for anybody else's work" — and his own ruling behind it, verbatim: *"the way i work, every project has its own repo, its non negotiable."* Rule 11's boundary test asks what a build could be rejected against, and nothing can be rejected against this statement that is not already rejected by R-0036 (state lives in the user's repo), R-0038 (the machinery aims at the consuming project) or R-0042 (git-native, per project). A requirement that restates the law above it is a second text that will drift from the first, and a reader who finds the two disagreeing cannot tell which governs.

**What was learned.** A law does not need a requirement to carry it, and giving it one costs a duplicate. Before writing a requirement that sounds like a law, ask what a build could be *rejected against* that the law's existing checkable forms do not already reject — if the answer is nothing, the requirement is a restatement. Where a law needs implementing, implement it in the specific: name the data, the execution target, the storage. R-0036, R-0038, R-0042 and R-0043 are that treatment of Law 1 and are why nothing was lost here.

**Superseded by.** nothing — killed outright. Law 1 stands above the set, and R-0036, R-0038, R-0042 and R-0043 are its checkable forms in the live set.

---

### R-0002 — DEAD — requirements exist to be reviewed, planned and named aloud

**Killed.** 2026-08-14, by analysis against the approved requirement shape — it is a statement of purpose and the shape gives purpose a home outside the set. Kill authorised by Tony.

**Statement as proposed.** Requirements exist so the producer can review them, plan enhancements, plan releases, and refer to any of them by a name he can say out loud

**Why it was proposed.** Never recorded as a reason. The migrated source carried a provenance pointer only. The statement had one amendment before death, made 2026-08-14 13:10 under Law 4's ordering rule: its final clause originally read *"speak in IDs that mean something"*, which carried two readings — a name he can point at and say, which survives in the handle beside each reference, and an identifier whose prefix tells you what the thing is, which the standards survey found rots, because "every scheme that encoded meaning in the identifier eventually had the meaning change." The first reading was kept and made explicit; the second was struck by analysis. His ruling licensing that amendment: *"if the analysis proved a better way, then we go agaist what i said before, we chnage the rule."*

**Why it is dead.** What remained after the amendment is a purpose, not an obligation. No build can be rejected against it, which is rule 11's test for statement content. Each of its four clauses is already carried by something checkable: review by R-0007 and R-0040, dependency and planning work by R-0007 and R-0041, and the sayable name by rule 3 of the approved shape, which puts a human handle beside every reference. Rule 13 of the shape gives prose about the set an explicit home — a preamble that is never fingerprinted — so this content has somewhere to live that is not a requirement. Keeping it as one dresses an explanation as a contract.

**What was learned.** Apply the rejection test before writing anything down: if no build could fail against the sentence, it is a Why or a preamble, not a Statement. Purpose prose about the whole set belongs in the register's preamble under rule 13, where it costs no approval and no fingerprint. One clause here was genuinely binding and has no home yet — *plan releases* — and that is a gap in the set, not a reason to resurrect this block; whoever picks it up should write it as an obligation on a release artifact that exists, not as a statement of why requirements exist.

**Superseded by.** nothing — killed outright. Its content belongs in the preamble; its checkable clauses are carried by R-0007, R-0040, R-0041 and rule 3 of `docs/design/requirement-shape.md`.

---

### R-0003 — DEAD — the twenty-category taxonomy ships; projects extend it

**Killed.** 2026-08-14 14:54, by analysis — superseded by the second research round the producer commissioned into the structures around the set, which measured the mechanism this requirement ships and found nothing there. Not by a test and not by a ruling on this requirement's own merits. Kill authorised by Tony.

**Statement as proposed.** The twenty-category discipline taxonomy ships as the default; projects extend it, never invent one

**Why it was proposed.** Never recorded. The migrated source (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) carried a provenance pointer and no reason, and none was invented at migration or here. The triage of 2026-08-14 recorded that the taxonomy was two things at once — the shipped checklist and the filing key for requirements — and that no step-1 research had ever been recorded for it.

**Why it is dead.** The filing half was already gone: the approved shape has no category field. The research killed the other half. It found no prior art for the structure — "Neither ISO 29148 nor INCOSE ships a subject-area list at all" — and it found the mechanism measured at zero: Porter, Votta & Basili (IEEE TSE 21(6), 1995) found the "checklist method no more effective than ad hoc", the reviewer with no checklist doing as well, while "perspective-based reading beat both by about 35%". The research's generalisation is the sentence that kills this block: "a list of topics adds nothing. A defined perspective to read from adds a lot." It also measured what happens when such a list is imposed rather than adopted — Ontario mandating the WHO 19-item surgical checklist across 106,370 procedures moved complications 3.86% → 3.82% and mortality 0.71% → 0.65%, "neither significant" — and observed that schemes genuinely used cluster at five to nine items, not twenty. The research recommended keeping the twenty areas as a reference list consulted when stuck; the producer's ruling of 2026-08-14 14:54 went further and struck them outright, so nothing of this requirement's subject remains to demote.

**What was learned.** Where completeness is the worry, ship a **perspective to read from**, not a list of topics to tick — "read this as the person who gets paged at 3am" is the intervention with a measured edge, and the topic list has a measured zero. That is the shape any future completeness proposal in this territory should take, and it is what the adversarial reviewer in this repo already does. Two further tests before proposing a checklist of any kind: does it fit in five to nine items and 60–90 seconds against a defined pause point, and is it adopted by the people running it rather than imposed on them — the Ontario result says an imposed list of the right content still does nothing. And a residue to place rather than lose: this requirement also carried an anti-fragmentation rule — *projects extend the default, they do not invent their own* — which is a claim about where defaults come from, not about taxonomies, and which no live requirement now carries. Whoever wants it back should write it about defaults generally and bring the measurement the taxonomy never had.

**Superseded by.** nothing — killed outright. No live requirement carries a completeness check by subject area, and none should; the perspective-based replacement the research recommends is unproposed.

---

### R-0004 — DEAD — applicability is declared, never assumed

**Killed.** 2026-08-14, by analysis against the flat live set — it duplicates R-0048. Kill authorised by Tony.

**Statement as proposed.** Applicability is declared per category — `applies`, or `n/a` with a named reason

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only.

**Why it is dead.** R-0048 states the same obligation about the same kind of object: "Every project type owes every gate unless that type explicitly marks it `n/a` with a reason." Same rule, same escape hatch, same demand that the excuse be named. In the old register the two sat under different category headings and read as two requirements; flat in one list they read as one requirement written twice. The duplicate is also the weaker of the two, because its subject noun is the category field the approved shape removed and it depends on R-0003, whose survival is still the producer's call.

**What was learned.** Section headings hide duplicates: two statements about the same obligation look distinct while they live under different headings and identical once the set is read flat. When proposing, read the live set flat and search for the obligation, not for the wording. And prefer the version whose subject still exists in the shape — a requirement keyed to a field the shape does not have is dead the moment the shape lands, however well it is written.

**Superseded by.** R-0048.

---

### R-0016 — DEAD — every requirement gets a category and an ID

**Killed.** 2026-08-14, by analysis against the approved requirement shape — contradicted in one half, superseded in the other. Kill authorised by Tony.

**Statement as proposed.** Every requirement gets a Category and ID, traceable back and forward

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only. His one recorded ask in this territory is the reference itself, verbatim: *"Reference numbers"*.

**Why it is dead.** The Category half is contradicted: the approved shape has no category field, and the survey's scale lesson behind that removal is blunt — "every scheme that encoded meaning in the identifier eventually had the meaning change." The ID half is superseded by rule 2 of the shape, which says the same thing with the doctrine attached, adopted from ISO 29148: "Once assigned, the identification is unique — it is never changed (even if the identified requirement changes) nor is it reused (even if the identified requirement is deleted)." Rule 2 adds what this statement never had — opacity, permanence, non-reuse, and minting only at filing. The survivor is strictly stronger than what died.

**What was learned.** Do not encode meaning in an identifier, and do not propose it back: the one fact about a requirement that can never change is the order it was created in, which is why a bare sequence number survives the scale lesson and a category prefix does not. Where a filing key is wanted, it is a tag or a rendering, never the name. Identity doctrine now lives in rule 2 of `docs/design/requirement-shape.md` rather than in the set — so a future proposal in this territory should first check whether the shape already binds it, because a requirement restating the shape is the same duplicate defect as a requirement restating a law.

**Superseded by.** nothing — killed outright. Rule 2 of `docs/design/requirement-shape.md` carries the surviving half. Whether that doctrine should also stand as a requirement in the set is open and unproposed.

---

### R-0017 — DEAD — a request is qualified before it becomes a requirement

**Killed.** 2026-08-14, by analysis against the approved requirement shape — it names a lifecycle the shape deliberately cut. Kill authorised by Tony.

**Statement as proposed.** Any request is qualified; if durable it becomes a requirement, through stages to final

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only.

**Why it is dead.** *"through stages to final"* is the five-state lifecycle the approved shape removed. Its settled decision reads: "there is no lifecycle or status field on a requirement" — and the standards research found no standard in the surveyed territory that defines a status on a requirement at all, while the two tools that did ship one shipped it unenforced, which the research called "the worst of both worlds: it looks like a contract and isn't one." A `final` state cannot be reached because it no longer exists; what the state was standing in for — is this agreed? — is now computed from the approval fingerprint under rule 9, so nobody maintains it and nobody forgets to downgrade it.

**What was learned.** The qualification work is real and is untouched: qualifying a request before it becomes a requirement is what `/kerd:interrogate` does, and it serves G2's refusal to guess. What died is the machinery of states, so a future proposal about qualification must describe the *work* — what gets asked, what evidence closes it — and must not smuggle a status field back in as the way of recording that the work happened. If you find yourself needing somewhere to write down which stage a requirement has reached, that is the signal to stop: the shape's answer is that approval is an event computed from a fingerprint, and where a requirement has reached is derived from what links to it.

**Superseded by.** nothing — killed outright. The qualification idea is unproposed in the live set; the approval mechanism that replaced the lifecycle is rule 9 of `docs/design/requirement-shape.md`.

---

### R-0019 — DEAD — the goal gate increments the type

**Killed.** 2026-08-14 14:54, by analysis — superseded by the second research round the producer commissioned, which collapsed the twelve-type vocabulary this statement steps through. Kill authorised by Tony.

**Statement as proposed.** The goal gate increments the project type to the next appropriate type

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only. The triage of 2026-08-14 named what it did that nothing else did: it was "the only statement saying the type advances rather than being re-declared".

**Why it is dead.** The statement is a progression rule, and a progression needs an ordered list to walk. Twelve types collapsed to one distinction — does this ship a change, or produce a finding — and a binary has no "next appropriate" member to increment to. The research found the list itself unsupported: "Scrum has zero work item types. One noun: Product Backlog Item. No bug, no task, no spike"; Shape Up "refuses them too"; and where a type does mean something, ITIL 4 and SAFe's Epic are the only surveyed cases, while SAFe's Enabler — "the type closest to our 'produces findings' idea, changes nothing procedurally". Herzig, Just & Zeller (ICSE 2013) measured the cost of asking people to classify at all: across 7,000+ manually reviewed issue reports, "33.8% of bug reports misclassified". Advancing an item automatically through a vocabulary that is wrong a third of the time compounds the error rather than correcting it. What the statement was reaching for — that a work item's classification can change without being re-asked from scratch — survives in R-0020, which puts a change of the distinction under the producer's agreement.

**What was learned.** A progression rule is not an independent idea; it is a dependent of the list it walks, and it dies with that list without ever mentioning it. Before writing one, name the enumeration it steps through and ask what evidence supports the enumeration — because the progression will look reasonable long after its list has stopped being defensible. And prefer a rule about *who agrees a change* over a rule about *what the change advances to*: the first survives a change of vocabulary, the second does not.

**Superseded by.** R-0020 — conductor suggests the distinction changes, the producer agrees it. It carries a change of classification without an ordered list to advance along.

---

### R-0022 — DEAD — route and rigor are derived, not declared

**Killed.** 2026-08-14 14:54, by analysis — superseded by the second research round the producer commissioned, which confined the surviving distinction to the definition of done and nothing else. Kill authorised by Tony.

**Statement as proposed.** `route` and `Rigor level` are derived from project type, not declared

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only. The triage of 2026-08-14 recorded what it was for: it "derives route and rigor instead of asking, which is where 'sized to the work' stops being a question the producer answers". It stood at `qualified`, never final, and was never agreed by anyone.

**Why it is dead.** It is machinery keyed to type, which is precisely what the ruling of 2026-08-14 14:54 removed: the surviving distinction changes the definition of done, and no gate, approval, template, route or rigor level is keyed to it. The research's recommendation is explicit about the refusals — "Refuse types that only change a label, approval gates keyed to type, and any type whose sole consequence is which template opens" — and a `route` selected by type is a pipeline keyed to type, the strongest form of the thing refused. It also had no source left to derive from: with twelve types gone, a binary cannot carry two derived dimensions.

**What was learned.** *Derived, not declared* is a good instinct pointed at the wrong source. When a rule derives one thing from another, the whole rule inherits whatever kills the source — so before writing it, ask whether the source is measured or merely inherited, because a derivation from an unresearched vocabulary is an unresearched decision wearing an automatic one's clothes. **The residue is worth naming rather than losing:** the payload here was *the producer is not asked to size the rigor of their own work* — the anti-nagging half of the statement, which is independent of type and which no live requirement now carries. Law 3's approved ladder already triggers on the weight of the work rather than on a stage or a budget, so whoever re-proposes this should derive rigor from the weight of the work and write it as an obligation not to ask.

**Superseded by.** nothing — killed outright. The rigor ladder in the approved goals is what a replacement should derive from; no live requirement states the do-not-ask obligation.

---

### R-0025 — DEAD — floors compose as a union

**Killed.** 2026-08-14 14:54, by analysis — superseded by the second research round the producer commissioned, which removed the per-type floors this statement composes. Kill authorised by Tony.

**Statement as proposed.** Floors compose as a union — a nested piece owes its own type's floor plus every floor of the project containing it

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only. The triage of 2026-08-14 recorded it as "the only rule stopping nesting from laundering rigor away". It stood at `proposed`, never final, and was never agreed by anyone.

**Why it is dead.** Its subject is *a type's floor* — a rigor floor attached to each of the twelve types — and that is the type-keyed machinery the ruling of 2026-08-14 14:54 struck, on research that refuses "any type whose sole consequence is which template opens" and holds that the surviving distinction changes "the definition of done, not the pipeline". A union of floors cannot be computed when there are no per-type floors to union. The nesting rule that remains live is R-0021, which composes the distinction itself and not a rigor floor.

**What was learned.** A composition rule is a second-order rule: it presumes the thing it composes. It is the last thing to notice its own subject has died, because it can be read as sound arithmetic long after the operands are gone — which is why a sweep for a dead structure has to look for statements that *operate on* it, not only statements that *name* it. **The residue, named rather than lost:** the guard this rule provided — *nesting must not launder rigor away, and a piece inside a larger piece owes what its container owes* — is real, independent of types, and now carried by nothing in the live set. Whoever re-proposes it should write it over the weight of the work, and should not need a type vocabulary to say it.

**Superseded by.** nothing — killed outright. R-0021 covers inheritance for the surviving distinction only; the anti-laundering guard for rigor is unproposed.

---

### R-0034 — DEAD — the producer marks the page without typing

**Killed.** 2026-08-14, by analysis against the approved requirement shape — both fields it marks were cut by settled decisions. Kill authorised by Tony.

**Statement as proposed.** The producer marks requirements **on the page without typing** — status, release assignment — and the page saves those marks to a file the next session applies on the word "updated"

**Why it was proposed.** Never recorded as a reason. The migrated source carried a provenance pointer only. What the statement is reaching for is legible in his objection of 2026-08-14 08:16, where he itemised what a generated view owes him — *"no simple way for me to see the requirments and their dependencies"*, *"to add comments perhaps for you to pick up or to record notes around the requirments"*, and *"add links or images perhaps as input"*.

**Why it is dead.** It names two things to mark, *"status, release assignment"*, and the approved shape cut both: "there is no lifecycle or status field on a requirement", and "which release a requirement is in lives on the release, never on the requirement". It therefore specifies a marking interface over two fields that do not exist. The mechanism is not what died — marking on the page, saved to a file, applied on the word "updated" — the fields are.

**What was learned.** An interface requirement inherits every dependency of the fields it touches, so it dies whenever one of them is cut. Before writing one, list the fields it manipulates and check each against the current shape; a requirement that survives that check is worth writing, and one that does not was really a requirement about the data model wearing an interface's clothes. The payload here is worth re-proposing over the fields that do exist — approval, comments, links, and dependency edits — and none of those is status or release membership. Note also what the kill leaves behind: R-0035 still declares `Depends on. R-0034`, and under rule 8 an unresolved reference stops the run, so killing an interface requirement is not finished until its dependents are re-pointed.

**Superseded by.** nothing — killed outright. The marking mechanism over the fields that exist is unproposed; his 08:16 itemisation is the brief for it.

---

### R-0037 — DEAD — traceability runs a nine-link chain, goal to metric

**Killed.** 2026-08-14 14:54, by analysis — superseded by the second research round the producer commissioned into traceability depth, which found the chain deeper than aerospace mandates and its cost side unmeasured. Kill authorised by Tony.

**Statement as proposed.** Traceability runs the nine-link chain: Business Goal → Stakeholder Need → Product Requirement → Functional/Technical → Design → Implementation → Test Case → Release Evidence → Post-Launch Metric

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only. The triage of 2026-08-14 read it charitably as an ambition rather than a contradiction — the approved shape implements two of its links and deliberately deferred the mechanism that would compute the rest, with a stated return condition — and referred it to the producer as his call.

**Why it is dead.** Eight of its nine links never existed. What is implemented is the single link the shape already carries — a requirement to the goal or law it serves — and that link survives because it is written once at framing and never maintained. The research is blunt on depth: DO-178C, for software in aircraft, uses "roughly **8 link types**"; ISO 26262 and IEC 62304 about four; "Our nine-step chain is deeper than what is mandated for aircraft." The arithmetic does not support it either. The benefit has one good study — Mäder & Egyed, 71 subjects on real maintenance tasks, "24% faster and 50% more correct solutions" — which "measures the value of *having* links, not of keeping them"; and against it, "The cost side is empty, and that is the finding", with no published figure for the share of effort traceability consumes and the field's own practitioners recorded saying "Cost is way greater than benefit" and "Not worth the effort". What decays first is the links themselves: trace quality "can dramatically degrade over time as the system evolves", maintenance is "cumbersome, error-prone and costly", and "outdated trace links invalidate safety-cases." The remedy the field reaches for is not more discipline — "The field's own remedy is automated re-derivation — that is, to stop maintaining links by hand." A nine-link chain maintained by two people by hand would rot faster than it was written, and a rotted chain is worse than none because it is read as true.

**What was learned.** **Any future link must be derived, never hand-curated** — from a commit trailer, a test name, a filename, something that already exists for another reason and is therefore maintained by someone else's work. If a link needs a person to remember it, it will be wrong, and a wrong link is read as a fact. Two tests before adding one: count the links already mandated in the most safety-critical territory you can find and notice if you are proposing more; and separate the value of *having* the link from the cost of *keeping* it, because the one study in the field measures the first and nobody has measured the second. Refuse bidirectional links, requirement→code, requirement→metric, and any periodic "trace review" — a review is the symptom of a link that cannot maintain itself. And write down which links exist rather than which links are wanted: this statement described nine and delivered one, and nothing in the register let a reader tell those apart.

**Superseded by.** nothing — killed outright. The surviving link is the `Traces to` element of `docs/design/requirement-shape.md`, written once at framing; whether a second, derived link is worth adding returns when a commit, test or filename convention exists to derive it from.

---

### R-0039 — DEAD — no routing to superpowers

**Killed.** 2026-08-14, by analysis against Law 4 and the open questions in the approved goals — it forecloses a decision the goals keep explicitly open. Kill authorised by Tony.

**Statement as proposed.** Never route to superpowers

**Why it was proposed.** Never recorded as a reason. The migrated source carried a provenance pointer only. The nearest honest anchor is the G8 grounding in the goals, which carries his words: *"superpowers does some great things... so we can learn from it, i just want the process to be ours and visable"* — the second half of which is the live payload, recorded below.

**Why it is dead.** Law 4 governs every aspect of the project and its second half, added 2026-08-14 08:36, reads verbatim: *"dont just assume we are correct unless an explicit requirement states this is the only way"*. A blanket ban on one named alternative is exactly the privileged conclusion that clause closes off — and it cannot rescue itself by being the explicit requirement the clause allows, because what the clause licenses is a stated constraint on the *design*, not a pre-emptive verdict on a candidate nobody has yet assessed under step 1. The goals also keep the decision open by name. Open question 2 in `docs/kerd-goals.md`: "What evidence settles build-vs-adopt, and who takes the decision?" — with the instruction that "The prior evaluation in this repo is to be re-examined as evidence, not treated as precedent." A live requirement forbidding the routing settles that question by having been written down first, which is the precise failure Law 4's ordering rule exists to prevent. And his ruling on what happens when the analysis disagrees with an earlier statement is unambiguous: *"if wer agree a better way then we superseed and strike off prior comments for sure. otherwise we go in loops"*.

**What was learned.** **The intent survives; only the instrument died.** His want was never a ban — it was visibility: *"i just want the process to be ours and visable"*, which G5 states as a failure to prevent, *"its not clear what or why its doing in a black box way"*. That is carried forward as R-0052, which names no third-party tool and instead states what any mechanism must be able to show. The lesson for the next proposer: **write the property, never the proper noun.** A requirement naming a specific tool decides an evaluation that has not been run and goes stale the moment that tool changes; a requirement naming the property the tool would have to satisfy survives every candidate, admits anything that qualifies, and refuses anything that does not — including something we build ourselves. If a ban on a named thing ever feels necessary, the question to ask first is what property the ban is protecting, and whether that property is what should be written down instead.

**Superseded by.** R-0052 — the process shows its own working. It carries the visibility intent and drops the named tool; it is drafted by the model and awaits the producer's approval.

---

### R-0045 — DEAD — the audit refuses on divergence

**Killed.** 2026-08-14, by analysis against the approved requirement shape — contradicted on the state it names and superseded on the fingerprint it defines. Kill authorised by Tony.

**Statement as proposed.** A `final` requirement carries a **hash of its statement as keyed**. When they diverge the audit **REFUSES** — it never rewrites the state, because a silent downgrade is a decision made for the producer rather than a question put to them

**Why it was proposed.** Never recorded as a reason. The migrated source carried a provenance pointer only. Its mechanism was borrowed from Doorstop a week before the Law 4 research independently recommended the same thing, and the old schema named where it came from — which the shape document records as one of the things the pre-reset work got right.

**Why it is dead.** Two of its clauses are dead machinery. *"A `final` requirement"* names a state that no longer exists: the approved shape's settled decision is "there is no lifecycle or status field on a requirement". And *"a hash of its statement as keyed"* is a fingerprint over the statement alone, which he overrode himself at 09:00 — *"no point doing half of the fingerprint"* — widened again to the Why at 09:32. Rule 9 now hashes the statement, the Why, the traces and the depends-on together, with an exact recipe and two published test vectors. The requirement therefore describes a narrower fingerprint than the one that governs, over a state that cannot be reached.

**What was learned.** The payload was never the mechanism — it was the refusal, and the refusal survives: rule 9 states that a recorded fingerprint that no longer matches means not approved, computed and reported by the tool and never written into the file. The old schema's phrasing of why is worth keeping in front of whoever builds it: "a red check is a question the producer answers; a silent downgrade is a decision made for them." The transferable lesson is about how to write a rule like this: state the *behaviour* — refuse rather than silently rewrite — and leave the recipe to the document that owns it, because a requirement that inlines a hash recipe dies every time the recipe widens, while a requirement that states the refusal survives the widening untouched.

**Superseded by.** nothing — killed outright. Rule 9 of `docs/design/requirement-shape.md` carries both the recipe and the refusal. Whether the refusal should also stand as a requirement in the live set is open and unproposed.
