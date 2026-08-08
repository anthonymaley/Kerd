# Requirements register

Written against the schema in `catalog.md`, which declares every field, state,
obligation and link role used below.

One block per requirement — heading, meta lines, statement, links (`TECH-009`).
A block is liftable as a unit: copy one out and it is still complete.

**`Approved` is a hash of the statement as it read when the producer keyed it
`final`** (`TECH-010`). When the statement and the hash diverge the audit
REFUSES; it never rewrites the state. `sha256`, first 12 hex of the stripped
statement.

Live requirements are grouped by category below. `superseded` and `dropped`
blocks move to `## Archive` at the foot of this file — a section, not a
separate file, so every ID stays resolvable in one parse.

Seeded 2026-08-08 from `docs/product/requirements-traceability.md` gap 2, which
was the evidence table that carried these until the register existed.

## PRD — Product

### PRD-001 — Kerd gives consuming projects this capability

**Category**: PRD
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:99f7ddf0d58d

Kerd gives consuming projects this capability; Kerd is only a user of it

### PRD-002 — Requirements exist so the producer can review, plan enhancements, plan…

**Category**: PRD
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:ec694eddb7c6

Requirements exist so the producer can review, plan enhancements, plan releases, and speak in IDs that mean something

### PRD-003 — The twenty-category discipline taxonomy ships as the default

**Category**: PRD
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:9b0e0ade5df5

The twenty-category discipline taxonomy ships as the default; projects extend it, never invent one

### PRD-004 — Applicability is declared per category

**Category**: PRD
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:796aed8b3961

Applicability is declared per category — `applies`, or `n/a` with a named reason

**Links**
- depends-on → PRD-003 (sha256:9b0e0ade5df5)

### PRD-005 — Project type and release type are the same thing for the twelve types that…

**Category**: PRD
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:d35ad0c8148d

Project type and release type are the same thing for the twelve types that ship; Ideation, Spike and Security Review produce findings instead

### PRD-006 — The alignment gate is a shared structure both parties can point at

**Category**: PRD
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:47a7b84345cc

The alignment gate is a shared structure both parties can point at — a drawing is its usual form, not its only one

### PRD-007 — The register is the data source for release planning, dependency and…

**Category**: PRD
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:7dec6aaca224

The register is the data source for release planning, dependency and visualization tooling — not merely a record

**Links**
- depends-on → TECH-006 (sha256:3c21e2c5416f)

### PRD-008 — The evaluation mark set is ◎ perfect · ○ fully meets (○+/○-) · △ meets with a…

**Category**: PRD
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:31a310b5f422

The evaluation mark set is `◎` perfect · `○` fully meets (`○+`/`○-`) · `△` meets with a countermeasure (`△+`/`△-`) · `×` cannot meet

### PRD-009 — × means cannot meet even with a countermeasure

**Category**: PRD
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:4153bd6015d5

`×` means cannot meet **even with a countermeasure**; cross takes no modifier, because there is no degree of impossibility

**Links**
- refines → PRD-008 (sha256:31a310b5f422)

### PRD-010 — Building the missing piece ourselves is a legal countermeasure

**Category**: PRD
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:c21fa58a63cb

Building the missing piece ourselves **is** a legal countermeasure — marked `△-`, with its cost carried by the summary columns rather than hidden in the mark

**Links**
- refines → PRD-008 (sha256:31a310b5f422)
- depends-on → PRD-011 (sha256:4d708711ca10)

### PRD-011 — Every evaluation carries four summary columns: COST · QUALITY · DUE DATE ·…

**Category**: PRD
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:4d708711ca10

Every evaluation carries four summary columns: **COST · QUALITY · DUE DATE · RATING**

### PRD-012 — A mark that is not ◎ or ○ states why, in a few words

**Category**: PRD
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:6b58da638798

A mark that is not `◎` or `○` states why, in a few words — never a sentence

**Links**
- refines → PRD-008 (sha256:31a310b5f422)

### PRD-013 — Dependency cost is judged marginally and proportionately: what the option…

**Category**: PRD
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:8de61f1c1b2c

Dependency cost is judged **marginally and proportionately**: what the option adds beyond what the project already needs, weighed against the share of value it buys. An ecosystem-normal install is not a burden; a whole new runtime bought for a fraction of the value is

## FUN — Functional

### FUN-001 — Approving the design is enough

**Category**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:800b79d0aaf9

Approving the design is enough — no plan-approval gate

### FUN-002 — A plan is execution of the design, carrying the measurements that prove the…

**Category**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:19b119bb6265

A plan is execution of the design, carrying the measurements that prove the goals met

**Links**
- refines → FUN-001 (sha256:800b79d0aaf9)

### FUN-003 — Every requirement gets a Category and ID, traceable back and forward

**Category**: FUN
**Tags**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:6b8368a5fbaa

Every requirement gets a Category and ID, traceable back and forward

### FUN-004 — Any request is qualified; if durable it becomes a requirement

**Category**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:ba6e4b40b7cd

Any request is qualified; if durable it becomes a requirement, through stages to final

### FUN-005 — Project type is declared once at conductor start, from the list, and not…

**Category**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:b76da5ae7fe2

Project type is declared once at conductor start, from the list, and not re-asked once a project has started

### FUN-006 — The goal gate increments the project type to the next appropriate type

**Category**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:7223c10e3980

The goal gate increments the project type to the next appropriate type

**Links**
- depends-on → FUN-005 (sha256:b76da5ae7fe2)

### FUN-007 — Conductor may suggest a type change

**Category**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:7a952d874cff

Conductor may suggest a type change — at the gate or mid-flight — and the producer agrees it

**Links**
- depends-on → FUN-005 (sha256:b76da5ae7fe2)

### FUN-008 — Type is a stack: items inherit the project's type, an override is opt-in and…

**Category**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:6c5915e066f4

Type is a stack: items inherit the project's type, an override is opt-in and forward-only

**Links**
- depends-on → FUN-005 (sha256:b76da5ae7fe2)

### FUN-009 — route and Rigor level are derived from project type, not declared

**Category**: FUN
**State**: qualified
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`

`route` and `Rigor level` are derived from project type, not declared

**Links**
- depends-on → FUN-005 (sha256:b76da5ae7fe2)

## NFR — Non-functional

### NFR-001 — The boundary records everything agreed

**Category**: NFR
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:e1269bb5e63d

The boundary records everything agreed; efficiency is a tiebreaker, never a reason to record less

### NFR-002 — Floors compose as a union

**Category**: NFR
**Tags**: FUN
**State**: proposed
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`

Floors compose as a union — a nested piece owes its own type's floor plus every floor of the project containing it

### NFR-003 — A spike carries its own rigor: scope boundary, timebox, spec, design, and…

**Category**: NFR
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:63ed5fc157df

A spike carries its own rigor: scope boundary, timebox, spec, design, and measurements

### NFR-004 — The mechanism must not scatter artifacts

**Category**: NFR
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:ace885d8c846

The mechanism must not scatter artifacts

## UX — UX/UI

### UX-001 — Boxes are never coloured

**Category**: UX
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:78ce341d07d6

Boxes are never coloured; the mark carries the verdict — `○` green, `△` yellow, `×` red

**Links**
- depends-on → PRD-008 (sha256:31a310b5f422)

### UX-002 — A mark is drawn at 40–50% of the cell it sits in

**Category**: UX
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:0712b78cf41b

A mark is drawn at 40–50% of the cell it sits in

### UX-003 — Column and row headings render as headings

**Category**: UX
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:9d442f9ed7e6

Column and row headings render as headings — `GROUP: CRITERION NAME`, `OPTION n: ID`, with the declaration below

### UX-004 — Diagrams render in a sans-serif font

**Category**: UX
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:c886dcd08537

Diagrams render in a sans-serif font

### UX-005 — The preferred option's verdict cell is filled green

**Category**: UX
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:35adaa7c8fd6

The preferred option's verdict cell is filled green

### UX-006 — The point of a table is to avoid reading lots of text to understand it

**Category**: UX
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:7224a470003b

The point of a table is to **avoid reading lots of text** to understand it — brevity is the requirement, not a preference

### UX-007 — The producer marks requirements on the page without typing

**Category**: UX
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:4601babdb3e5

The producer marks requirements **on the page without typing** — status, release assignment — and the page saves those marks to a file the next session applies on the word "updated"

### UX-008 — A generated page carries the hash of the state it was rendered from, so marks…

**Category**: UX
**Tags**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:383c65601ef2

A generated page carries the hash of the state it was rendered from, so marks made against a stale view are refused rather than applied blind

**Links**
- depends-on → UX-007 (sha256:4601babdb3e5)

## TECH — Technical

### TECH-001 — The user's repo holds funnel state, requirements, stage data, steps and…

**Category**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:d2f2ed2700d9

The user's repo holds funnel state, requirements, stage data, steps and journey — nothing in Kerd, ever

### TECH-002 — Traceability runs the nine-link chain

**Category**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:3bbe6f8ebb65

Traceability runs the nine-link chain: Business Goal → Stakeholder Need → Product Requirement → Functional/Technical → Design → Implementation → Test Case → Release Evidence → Post-Launch Metric

### TECH-003 — The machinery must aim at the consuming project, never at its own install path

**Category**: TECH
**State**: qualified
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`

The machinery must aim at the consuming project, never at its own install path

### TECH-004 — Never route to superpowers

**Category**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:77078870a23e

Never route to superpowers

### TECH-005 — The register is a standalone file at a known location

**Category**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:9582f3a0c390

The register is a standalone file at a known location — never embedded in a product doc — so it can be read quickly by a person and directly by a tool

### TECH-006 — A requirement row carries its dependencies on other requirement IDs

**Category**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:3c21e2c5416f

A requirement row carries its **dependencies** on other requirement IDs

### TECH-007 — The mechanism must be git-repo native and Claude Code friendly, per project

**Category**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:b9e3808abda5

The mechanism must be git-repo native and Claude Code friendly, per project

### TECH-008 — The register must be the same files — one representation, no parallel store

**Category**: TECH
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:d0da108cf69f

The register must be **the same files** — one representation, never a parallel store alongside the project's own

### TECH-009 — A requirement is a block, not a table row

**Category**: TECH
**Tags**: UX
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:7e833af32a5d

A requirement is a **block**, not a table row — heading, bolded meta lines, statement as text, links as a trailing list. It must be readable and **liftable as a unit**: copy-pasteable elsewhere without reassembly

### TECH-010 — A final requirement carries a hash of its statement as keyed. When they…

**Category**: TECH
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:83ec3c1f0fef

A `final` requirement carries a **hash of its statement as keyed**. When they diverge the audit **REFUSES** — it never rewrites the state, because a silent downgrade is a decision made for the producer rather than a question put to them

## OPS — Operational

### OPS-001 — Funnel interaction requires a conductor session

**Category**: OPS
**Tags**: FUN
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:bb9cc221d399

Funnel interaction requires a conductor session; Q&A, reports and admin work stay available outside it

## TST — Testing / Validation

### TST-001 — The plan must check the design's measurements are carried in accurately, and…

**Category**: TST
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:f0a298b09d10

The plan must check the design's measurements are carried in accurately, and show it

### TST-002 — Every project type owes every gate unless that type explicitly marks it n/a…

**Category**: TST
**State**: proposed
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`

Every project type owes every gate unless that type explicitly marks it `n/a` with a reason

**Links**
- depends-on → FUN-005 (sha256:b76da5ae7fe2)

### TST-003 — 

**Category**: TST
**Tags**: PRD
**State**: final
**Source**: 2026-08-07/08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:4459ab786c0b

**DUE DATE, not EFFORT** — can it meet the plan in time, an outcome measure, rather than how much work it is, an input measure

**Links**
- refines → PRD-011 (sha256:4d708711ca10)

### TST-004 — The completeness check is tiered: the LIGHT check fires at every step

**Category**: TST
**State**: final
**Source**: 2026-08-08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:1d711127b148

**The completeness check is tiered: the LIGHT check fires at every step; BOTH light and heavy fire at the design GO.** Light is machine facts only — did the register move, do approval hashes still match, are link stamps stale, does declared grounding resolve. Heavy is N independent readers working from the RAW sources, never from a summary, with convergence as the signal

### TST-005 — A completeness check must not be a step the model can assume or skip

**Category**: TST
**State**: final
**Source**: 2026-08-08 session — `docs/product/requirements-traceability.md`
**Approved**: sha256:e7d2019bff0f

A completeness check must not be a step the model can assume or skip — it binds on countable facts, from outside the model, never on a question the model answers about itself

## Archive

*Empty — no requirement has been superseded or dropped yet.*
