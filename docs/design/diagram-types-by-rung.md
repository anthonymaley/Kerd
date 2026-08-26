# Which diagram serves which rung

Mapped 2026-08-22 from the 39 type specs in `cathrynlavery/diagram-design`,
using each type's own `Best for:` line rather than its name. Companion to
`diagram-toolkit-spike-findings.md`, whose operating rule governs every row
here: **pick a type and obey its layout rules — do not freelance. A box must
mean something.**

## All 39, with a verdict on each

**Judged for a project that uses Kerd — not for this repository.** Tony's
standing correction, 2026-08-07: *"KERD is the skill that people use to build
things. Kerd needs to give those projects this capability (perversely we need it
to build Kerd too) so I am talking about the scope of the skill here all the
time."* Restated 2026-08-22 against an earlier version of this table: *"projects
that use Kerd might have a need for diagram that the skill itself does not"*.

**Kerd having no database is a fact about Kerd, not a verdict on `db-schema`.**
An earlier version of this file scored the whole set against this repository's
own needs, which is the wrong altitude and a repeatable mistake, because this
repo is the thing on screen. Dogfooding is evidence a capability works; it is
never the definition of what it is for.

**USE** — a job at a named rung, for a project using Kerd ·
**CANDIDATE** — plausible, no use proven yet ·
**TRAP** — looks right for a rung and is not ·
**OURS** — the job belongs to a tool Kerd already supplies

Counts: USE 35 · CANDIDATE 1 · TRAP 1 · OURS 2

| Type | Status | What it draws |
|---|---|---|
| **architecture** | USE · design | System overviews, integration maps, infra topology. |
| **bar** | USE · acceptance | A measured result against the target that was declared. |
| **data-flow** | USE · design | How data moves across roles — who starts it, who processes, who publishes. |
| **db-schema** | USE · design | Physical SQL tables, types and constraints — the DDL made legible. Any project with a database. Kerd has none, which is a fact about Kerd. |
| **dependency** | USE · design, handoff | What depends on what, including cycles a tree cannot show. |
| **deployment** | USE · design | Where the software actually runs. |
| **dp-integration** | USE · frame, design | Hub and spoke: what plugs in, what plugs out, over what wire. Any platform project — and Kerd itself, as hub to the repos that use it. |
| **dp-security-matrix** | USE · handoff | A grid of rows against roles. For us: who holds the key at each rung. |
| **er** | USE · design | Entities and how they relate. |
| **fishbone** | USE · frame, acceptance | One observed effect, causes grouped by category. The problem route. |
| **flowchart** | USE · design | Decision logic and branching. |
| **gantt** | TRAP | Tasks with start and end dates. A release is a grouping, not a time axis. |
| **high-level** | USE · frame, design | An end-to-end stack as a phase chevron, with a strip for concerns that ride every phase. |
| **it-state** | USE · frame | The before picture — what exists now and how it is grouped. |
| **journey** | USE · frame | What a person does across stages and how it feels at each one. |
| **kanban** | OURS | A state census of work in progress. That is the progress board, derived from disk. |
| **layers** | USE · design | Abstraction layers, stacks, cascades. |
| **line** | USE · acceptance | A measure over releases, when the trend is the evidence. |
| **loop** | USE · acceptance | Cycles where the last step feeds the first. |
| **medallion** | USE · design | Tiers of the same dataset at different quality levels, and how data is promoted between them. Any data project. |
| **nested** | USE · design | Hierarchy by containment. Our default grammar — outer is broader. |
| **org-chart** | USE · handoff | Role ownership and routing, including agent teams. |
| **polar** | CANDIDATE | One series across 4–8 categories whose clockwise order carries meaning. Unproven — the ladder being a cycle of eight is the only use found so far. |
| **process** | USE · design | A sequential process with actors and the data passing between them. |
| **pyramid** | USE · frame, scope | Ranks and funnels — what sits above what. |
| **quadrant** | USE · viability | A 2×2 decision frame. Use the type, replace the default axes. |
| **radar** | OURS | Comparing entities across criteria. That is the evaluation matrix. |
| **sankey** | USE · viability | Where a quantity goes as it splits and merges. |
| **scatter** | USE · acceptance | Correlation, when the relationship itself is the claim. |
| **sequence** | USE · design | Multi-actor interactions over time. |
| **state** | USE · design | Finite state logic — lifecycles, wizards, queues. |
| **story-map** | USE · scope | Where the first release gets cut. The strongest match in the set. |
| **swimlane** | USE · design, handoff | Cross-functional flow where the handoffs are the point. |
| **timeline** | USE · loop, acceptance | Release history, milestones, incident reconstruction. |
| **tree** | USE · design | Taxonomies, breakdowns, file trees. |
| **treemap** | USE · viability, scope | Part of a whole, where the relative size is the story. |
| **uml-class** | USE · design | Operations and the inheritance/composition vocabulary, where those are the point. Any project with an object model worth arguing about. |
| **venn** | USE · frame | Where A meets B — overlaps, not sequences. |
| **wardley** | USE · viability | Build, buy or outsource. The interview's open question, drawn. |

## The map

### FRAME — what is happening now, and what is wrong with it

| Type | Why it fits |
|---|---|
| **it-state** | *"documenting the before picture of a modernization proposal — the legacy landscape grouped by phase or department"*. This is the current-situation drawing the frame rung asks for, by name. |
| **journey** | *"what a person does across the stages of an experience and how it feels at each one. The sentiment curve is the load-bearing element."* The pain, drawn, with the feeling kept rather than summarised away. |
| **fishbone** | *"structured root-cause analysis. One observed effect, causes grouped by category."* The `route: problem` frame, exactly. |
| **venn** | *"where A meets B, ikigai-style frames (desirable/viable/feasible)"*. Useful when the frame is about an overlap rather than a sequence. |
| **pyramid** | Prioritisation ranks and conversion funnels — where the frame is about what sits above what. |

### VIABILITY — is this worth doing, and what would kill it

| Type | Why it fits |
|---|---|
| **wardley** | *"positioning the components of a value chain against how evolved each one is, so a reader can see what to build, buy or outsource."* This is the build-versus-adopt question the interview left open, drawn. |
| **quadrant** | 2×2 decision frames. **With our axes, not the default ones** — see the traps below. |
| **sankey** | *"where a quantity goes as it splits and merges"*. For cost and budget viability. |
| **treemap** | Part-of-whole *where relative size is the story* — where the effort or the spend actually goes. |

### SCOPE — what is in the first release, and what is not

| Type | Why it fits |
|---|---|
| **story-map** | *"the Jeff Patton user story map — it answers 'what is the whole story, and where do we cut the first release?'"* **The single strongest match in the whole list.** That sentence is the scope rung's definition. |
| **pyramid** | When the cut is by rank rather than by narrative. |
| **treemap** | When the cut is by size. |

### DESIGN — the solution, and it is where most of these live

Fifteen of the thirty-nine belong here, which matches the rung: *"detailed
specs, architecture plans, testing strategy, and diagrams for as many aspects
as we can."*

| Type | Draws |
|---|---|
| **architecture** | system overviews, integration maps, infra topology |
| **nested** | containment — scope boundaries, trust zones, blast radius. **Our grammar's default.** |
| **layers** | abstraction layers, stacks, cascades |
| **sequence** | multi-actor interactions over time, call traces |
| **state** | finite state logic — lifecycles, wizards, queues |
| **flowchart** | decision logic and branching |
| **process** | sequential business process with actors and data |
| **swimlane** | cross-functional flows, handoffs, who-does-what |
| **data-flow** | how data moves *across roles* — who initiates, processes, publishes |
| **er** | domain models, entities and relationships |
| **dependency** | what depends on what, including cycles a tree cannot show |
| **deployment** | where the software actually runs |
| **tree** | taxonomies, breakdowns, file trees |
| **org-chart** | role ownership and routing — including **agent** teams |
| **uml-class** | static object structure, where that is the story |

### HANDOFF — handing pieces to whoever builds them

| Type | Why it fits |
|---|---|
| **dependency** | what must land before what — the ordering the handoff encodes |
| **org-chart** | *"human teams, agent teams, support escalation maps, role ownership"* — the four roles and which model plays which |
| **swimlane** | who owns which piece across the work handoff |

### BUILD — mostly nothing

Building is execution and leaves commits, not pictures. The one candidate,
**kanban**, is a trap — see below.

### GOAL — did it meet what was declared

| Type | Why it fits |
|---|---|
| **bar** | measured result against declared target, per criterion |
| **line** | a measure over releases, when the trend is the evidence |
| **scatter** | when the claim is about a relationship rather than a level |
| **timeline** | what actually shipped, and when |

### LOOP — what we learned, and what comes next

| Type | Why it fits |
|---|---|
| **loop** | *"reinforcing cycles, flywheels, feedback loops, operating loops — anything where the last step feeds the first."* The rung's own name. |
| **fishbone** | when the loop is entered because something failed |
| **timeline** | release history, incident reconstruction |

## Traps — types that look right for a rung and are not

- **gantt** at scope or viability. *"Tasks with explicit start and end dates."*
  Our standing decision is that **a release is a grouping, not a time axis** —
  time may be attached later, or never. A gantt makes the time axis the
  definition, which is the position that decision reversed.
- **kanban** at loop. *"A snapshot of work-in-progress by state."* That is the
  progress board, which is derived from disk and byte-compared in CI. This
  toolkit cannot serve it — the spike closed job 2 permanently.
- **radar** and **dp-security-matrix** at viability. Both are comparison grids,
  and comparison between options is the **evaluation matrix** — job 1, ours,
  with 24 criteria and marks the toolkit has no equivalent for. Reaching for
  radar here would quietly replace a machine-checked artifact with a picture.
- **quadrant** with its default axes. Its examples are Impact × Effort. Our
  ranking is **consequence × value**, and *effort is explicitly not an axis* —
  it flatters cheap work. Use the type, replace the axes.

## The seven I wrongly dismissed — re-evaluated against real Kerd artifacts

**An earlier version of this file blacklisted seven types in one line, on the
grounds that they were "data-platform or object-model specific".** Tony refused
it: *"lets nto blacklist until we are sure… use kerd specifc info so we can
evaluate properly."* He was right twice over — a model may propose a kill and
never record one (rule 10), and a ruled-out thing owes a **return condition**,
not a line through it.

Re-read against their full specs. **Five of the seven were wrong.** The error
has a name worth keeping: **they were dismissed by domain, not by shape.** The
domain is the example the author happened to use; the shape is what transfers.

### Wrongly dismissed — real Kerd uses

| Type | The shape it actually draws | The Kerd artifact |
|---|---|---|
| **dp-security-matrix** | rows × roles, each cell a permission level, one cell markable as focal | **Who holds the key at each rung.** Four roles — producer, composer, conductor, players — against seven rungs. The producer holds frame, viability, scope and design plus evaluation at acceptance; the model holds handoff and loop. The focal cell is the rule that surprises people: *no human key per piece at loop.* This is the division of labour, drawn. |
| **high-level** | phase chevron banner, boundary, and an optional vertical strip for cross-cutting concerns | **The funnel end to end.** frame → viability → scope → design → handoff → loop → acceptance as the chevron; the gates and CI that ride *every* rung as the cross-cutting strip. `gen_kerd_map.py` hand-draws something close to this today in 141 lines. |
| **polar** | one series across 4–8 categories **whose clockwise order is meaningful** | **The ladder is a cycle** — acceptance feeds back into frame — and it has exactly seven positions. Work items per rung, clockwise, makes the cycle the point rather than a detail. No other type in the set treats circular order as load-bearing. |
| **dp-integration** | hub and spoke: what plugs in, what plugs out, over what wire | **Kerd as the hub and consuming repos as the spokes.** Its own framing question — *"what surfaces does this platform expose, and over what wire?"* — is the consuming-project question behind R-0036 and R-0038. |
| **medallion** | tiers of the *same* thing at different quality levels, with who writes each and **how something is promoted between tiers** | **Marginal but real.** The register has draft and approved, live and graveyard, and a promotion beat between them. Weaker than the four above because our tiers are not quality levels of one dataset. Return condition: if the register ever grows explicit tiers. |

### Genuinely no use today — with the condition that would change it

Not blacklisted. Named, with what would bring them back.

| Type | Why not, today | Return condition |
|---|---|---|
| **db-schema** | Column-level physical schema — SQL types, constraints, `ON DELETE` behaviour. Kerd holds no database and writes no SQL. | **A consuming project with a real database.** That is not a hypothetical: the capability is written for a project that is not Kerd, so this type may be needed by a user of Kerd long before Kerd needs it. |
| **uml-class** | Its distinguishing content is the operations compartment and the inheritance/composition vocabulary. Our Python has classes — `Canvas`, `Flow`, `Block` — but the story has never once been what inherits from what. | **The first time the tooling's object model is something we have to argue about**, rather than something we just use. |

### The lesson, because it has happened before

Dismissing by domain rather than by shape is the same error as the 2026-08-08
finding on convergence: three agents agreed on eight category moves because they
had all keyword-matched a column heading rather than read a definition. Reading
the label is not reading the thing. **Seven were judged from their names; five
of the judgements were wrong.**

## What this map is missing

**Examples.** Every row above is an argument from a spec line, not from a
drawing. The spike's own hardest lesson is that a type read is not a type used —
the two diagrams it produced were made with the same toolkit and got opposite
verdicts, because one obeyed a type's layout rules and the other invented panels.

So the next step is one worked example per rung, **rendered and looked at before
it is shown to anyone** — the check the spike skipped.
