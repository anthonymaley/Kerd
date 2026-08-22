# Which diagram serves which rung

Mapped 2026-08-22 from the 38 type specs in `cathrynlavery/diagram-design`,
using each type's own `Best for:` line rather than its name. Companion to
`diagram-toolkit-spike-findings.md`, whose operating rule governs every row
here: **pick a type and obey its layout rules — do not freelance. A box must
mean something.**

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

### SLICE — what is in the first release, and what is not

| Type | Why it fits |
|---|---|
| **story-map** | *"the Jeff Patton user story map — it answers 'what is the whole story, and where do we cut the first release?'"* **The single strongest match in the whole list.** That sentence is the slice rung's definition. |
| **pyramid** | When the cut is by rank rather than by narrative. |
| **treemap** | When the cut is by size. |

### DESIGN — the solution, and it is where most of these live

Fifteen of the thirty-eight belong here, which matches the rung: *"detailed
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

### CONTRACT — handing pieces to whoever builds them

| Type | Why it fits |
|---|---|
| **dependency** | what must land before what — the ordering the contract encodes |
| **org-chart** | *"human teams, agent teams, support escalation maps, role ownership"* — the four roles and which model plays which |
| **swimlane** | who owns which piece across the handoff |

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

- **gantt** at slice or viability. *"Tasks with explicit start and end dates."*
  Our standing decision is that **a release is a grouping, not a time axis** —
  time may be attached later, or never. A gantt makes the time axis the
  definition, which is the position that decision reversed.
- **kanban** at build. *"A snapshot of work-in-progress by state."* That is the
  progress board, which is derived from disk and byte-compared in CI. This
  toolkit cannot serve it — the spike closed job 2 permanently.
- **radar** and **dp-security-matrix** at viability. Both are comparison grids,
  and comparison between options is the **evaluation matrix** — job 1, ours,
  with 24 criteria and marks the toolkit has no equivalent for. Reaching for
  radar here would quietly replace a machine-checked artifact with a picture.
- **quadrant** with its default axes. Its examples are Impact × Effort. Our
  ranking is **consequence × value**, and *effort is explicitly not an axis* —
  it flatters cheap work. Use the type, replace the axes.

## Not for us — seven types, named so nobody re-evaluates them

`dp-integration`, `dp-security-matrix`, `medallion`, `high-level`, `db-schema`,
`uml-class`, `polar`. All are data-platform or object-model specific. `db-schema`
and `uml-class` would apply to a consuming project that builds that kind of
software; they have no use in Kerd itself.

## What this map is missing

**Examples.** Every row above is an argument from a spec line, not from a
drawing. The spike's own hardest lesson is that a type read is not a type used —
the two diagrams it produced were made with the same toolkit and got opposite
verdicts, because one obeyed a type's layout rules and the other invented panels.

So the next step is one worked example per rung, **rendered and looked at before
it is shown to anyone** — the check the spike skipped.
