# Requirements — Kerd

Written against the normative form in `docs/design/requirement-shape.md`.

**This file is a migration, not an authorship.** Every block below was
transcribed from the previous register's 51 requirements. The old
identifiers are not carried — not as references, not as aliases. Under the
producer's ruling of 2026-08-14 (*"absolutley ignore the past, move to the
future"*) the old scheme dies with the old register; git history holds it.
References here are freshly minted under rule 2, in the old register's
reading order, which is the only creation order a migration has.

**Where the set stands — 2026-08-14.** Fifty-one requirements were migrated
into a register with an empty graveyard. **Eight have since been killed and
moved to `## Graveyard`** — R-0001, R-0002, R-0004, R-0016, R-0017, R-0034,
R-0039 and R-0045 — on the recommendations in `docs/requirements/triage.md`,
each with Tony as the named authoriser under rule 10. One replacement was
minted, **R-0052**, which carries forward the visibility intent underneath
R-0039. **The live set therefore holds 44 requirements and the graveyard
holds 8.**

**The live numbering has gaps, and the gaps are correct.** Rule 2 forbids a
reference from ever being changed or reused, so nothing was renumbered when
the eight left — the live set simply has no R-0001, R-0002, R-0004, R-0016,
R-0017, R-0034, R-0039 or R-0045 in it. The graveyard is what makes that rule
observable: a reader who finds a number missing from the live set finds it at
the end of this file, taken, with the reason it went and what to take from it.
A set with no gaps would mean either that nothing had ever been killed or that
a number had been quietly reused.

**One dependency dangles, named rather than fixed.** R-0035 declares
`Depends on. R-0034`, and R-0034 is now dead. Under rule 8 an unresolved
reference is an error that stops the run. R-0035 survives on its own merit and
its dependency needs re-pointing — but that is an edit to a live requirement,
and the authorisation given on 2026-08-14 was for the eight kills, not for
rewriting a survivor.

**Every requirement lands unapproved, deliberately.** The old register carried
approval fingerprints over the statement alone. The new fingerprint covers
statement, Why and links, and the Why is content that did not exist before —
so no old approval can survive, however careful the transcription. No
fingerprint below is computed and no old hash is carried across.
Re-approving the whole set in one sitting is the textbook
approval-fatigue scenario the Law 4 research documented; each is approved
when work touches it and the producer is reading it anyway.

**Statements are carried verbatim.** No statement below was reworded. Where a
statement fails the adopted plain-language word list, that is recorded in
`## Findings` rather than silently corrected — rewording 51 approved
statements is authorship, and it is his call, not the migration's.

**Machine names are absent by design.** Rule 4: nobody hand-writes one. The
checking tool mints and inserts them on its next run.

**Where a Why could not be honestly written it says so.** Forty-six migrated
blocks carry an unwritten Why, because their migrated source recorded
provenance and nothing else. No rationale is invented anywhere in this file,
and the kills of 2026-08-14 invented none either — a dead requirement's
`Why it was proposed` says that no reason was ever recorded, exactly as the
live block did. All forty-six are listed in `## Findings`; **eight of them are
now in the graveyard, so thirty-eight live blocks await his words.** R-0052,
the one block written rather than migrated, carries a real Why.

## Requirements

### R-0003 — the taxonomy ships as default

**Statement.** The twenty-category discipline taxonomy ships as the default; projects extend it, never invent one

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G8

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0005 — project type and release type are one vocabulary

**Statement.** Project type and release type are the same thing for the twelve types that ship; Ideation, Spike and Security Review produce findings instead

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0006 — the alignment gate is a shared structure

**Statement.** The alignment gate is a shared structure both parties can point at — a drawing is its usual form, not its only one

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G1, G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0007 — the register feeds the tooling

**Statement.** The register is the data source for release planning, dependency and visualization tooling — not merely a record

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G5

**Depends on.** R-0041

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0008 — the evaluation mark set

**Statement.** The evaluation mark set is `◎` perfect · `○` fully meets (`○+`/`○-`) · `△` meets with a countermeasure (`△+`/`△-`) · `×` cannot meet

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0009 — the cross takes no modifier

**Statement.** `×` means cannot meet **even with a countermeasure**; cross takes no modifier, because there is no degree of impossibility

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** R-0008

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0010 — building it ourselves is a legal countermeasure

**Statement.** Building the missing piece ourselves **is** a legal countermeasure — marked `△-`, with its cost carried by the summary columns rather than hidden in the mark

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 4, G7

**Depends on.** R-0008, R-0011

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0011 — the four summary columns

**Statement.** Every evaluation carries four summary columns: **COST · QUALITY · DUE DATE · RATING**

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0012 — a lesser mark says why, briefly

**Statement.** A mark that is not `◎` or `○` states why, in a few words — never a sentence

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** R-0008

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0013 — dependency cost is marginal and proportionate

**Statement.** Dependency cost is judged **marginally and proportionately**: what the option adds beyond what the project already needs, weighed against the share of value it buys. An ecosystem-normal install is not a burden; a whole new runtime bought for a fraction of the value is

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 4, G7

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0014 — approving the design is enough

**Statement.** Approving the design is enough — no plan-approval gate

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G1, G3

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0015 — a plan executes the design and carries its measurements

**Statement.** A plan is execution of the design, carrying the measurements that prove the goals met

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G6

**Depends on.** R-0014

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0018 — project type is declared once

**Statement.** Project type is declared once at conductor start, from the list, and not re-asked once a project has started

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G1

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0019 — the goal gate increments the type

**Statement.** The goal gate increments the project type to the next appropriate type

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** R-0018

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0020 — conductor suggests a type change, the producer agrees it

**Statement.** Conductor may suggest a type change — at the gate or mid-flight — and the producer agrees it

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G1, G5

**Depends on.** R-0018

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0021 — type is a stack

**Statement.** Type is a stack: items inherit the project's type, an override is opt-in and forward-only

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** R-0018

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0022 — route and rigor are derived, not declared

**Statement.** `route` and `Rigor level` are derived from project type, not declared

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** R-0018

**Approval.** none — and this one was **never approved under the old rules either**: it stood at `qualified`, not final, when the register was migrated on 2026-08-14. It has never been agreed by anyone. The Why is unwritten.

---

### R-0023 — conductor sizes the model and the effort

**Statement.** Conductor effectively manages model usage and effort in both directions: an overpowered session (e.g. Fable xhigh) is advised down to the right conductor tier and effort (e.g. Opus medium), and Fable and other models are then brought in per-call to do the work at the right effort too

**Why.** Tony asked for this mid-session on 2026-08-13, verbatim: *"we need kerd conductor to effectively manage model usage and effort, i.e. if we are at fable xhigh, it should tell us to change to opus medium or whatever and then bring fable and other models in to do the work at the right effort too"*. The statement is a transcription of that ask, not a derivation from it. What his words carry that the statement makes checkable is the two directions — advising the session down as well as calling stronger models in per-step.

**Traces to.** G7

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the fingerprint now covers the Why and the links, which no earlier approval saw.

---

### R-0024 — the boundary records everything agreed

**Statement.** The boundary records everything agreed; efficiency is a tiebreaker, never a reason to record less

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G2, G7

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0025 — floors compose as a union

**Statement.** Floors compose as a union — a nested piece owes its own type's floor plus every floor of the project containing it

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** none

**Approval.** none — and this one was **never approved under the old rules either**: it stood at `proposed`, not final, when the register was migrated on 2026-08-14. It has never been agreed by anyone. The Why is unwritten.

---

### R-0026 — a spike carries its own rigor

**Statement.** A spike carries its own rigor: scope boundary, timebox, spec, design, and measurements

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0027 — artifacts do not scatter

**Statement.** The mechanism must not scatter artifacts

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G5

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0028 — the mark carries the verdict, not the box

**Statement.** **In the evaluation matrix**, boxes are never coloured; the mark carries the verdict — `○` green, `△` yellow, `×` red

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** R-0008

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0029 — mark size inside its cell

**Statement.** **In the evaluation matrix**, a mark is drawn at 40–50% of the cell it sits in

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0030 — headings render as headings

**Statement.** **In the evaluation matrix**, column and row headings render as headings — `GROUP: CRITERION NAME`, `OPTION n: ID`, with the declaration below

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0031 — diagrams use a sans-serif font

**Statement.** Diagrams render in a sans-serif font

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** not yet traced — see Findings. No goal or law is served by this statement without inventing a rationale for it, and the migration will not.

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten, the trace is unresolved, and no earlier approval covered either.

---

### R-0032 — the preferred option's verdict cell

**Statement.** **In the evaluation matrix**, the preferred option's verdict cell is filled green

**Why.** Partly written. The migrated source records provenance and one verbatim ruling: this came from the producer's own tweaks to the evaluation-matrix render on 2026-08-08, and its scope was corrected at 21:23 on his statement — Tony: *"UX-001 was for the eval matrix only"* — which is why the statement binds inside the evaluation matrix and nowhere else. That explains the scope; it does not explain why the requirement exists. The reason still awaits his words.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is only partly written, and the fingerprint now covers the Why and the links.

---

### R-0033 — brevity is the point of a table

**Statement.** The point of a table is to **avoid reading lots of text** to understand it — brevity is the requirement, not a preference

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0035 — a stale view's marks are refused

**Statement.** A generated page carries the hash of the state it was rendered from, so marks made against a stale view are refused rather than applied blind

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Re-pointed 2026-08-14, as a consequence of an authorised kill.** This declared
`Depends on. R-0034` until R-0034 was moved to the graveyard, which left an
unresolved reference — the error its own graveyard entry predicted. The
dependency was **incidental rather than real**: this requirement guards a
generated page against accepting marks made from a stale render, and that guard
holds whatever a page lets a reader mark. It needed R-0034 only because R-0034
happened to be the marking interface first written down.

**Unhomed by that kill, and named here rather than lost:** R-0034's live half —
marking on the page, saved to a file, applied later — survives its own death.
The producer agreed that mechanism on 2026-08-14 08:20 as the first step:
*"ideally directly to reduce overhead for many requirments but we can start with
a paste option while we build the proess and ui out if you want as a first
step"*. No live requirement carries it. Same residue shape as R-0002's *plan
releases*.

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0036 — state lives in the user's repo

**Statement.** The user's repo holds funnel state, requirements, stage data, steps and journey — nothing in Kerd, ever

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0037 — the nine-link traceability chain

**Statement.** Traceability runs the nine-link chain: Business Goal → Stakeholder Need → Product Requirement → Functional/Technical → Design → Implementation → Test Case → Release Evidence → Post-Launch Metric

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 2, G2

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0038 — the machinery aims at the consuming project

**Statement.** The machinery must aim at the consuming project, never at its own install path

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1

**Depends on.** none

**Approval.** none — and this one was **never approved under the old rules either**: it stood at `qualified`, not final, when the register was migrated on 2026-08-14. It has never been agreed by anyone. The Why is unwritten.

---

### R-0040 — the register is a standalone file

**Statement.** The register is a standalone file at a known location — never embedded in a product doc — so it can be read quickly by a person and directly by a tool

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G5

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0041 — a requirement carries its dependencies

**Statement.** A requirement row carries its **dependencies** on other requirement IDs

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G5

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0042 — git-native, per project

**Statement.** The mechanism must be git-repo native and Claude Code friendly, per project

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0043 — one representation, no parallel store

**Statement.** The register must be **the same files** — one representation, never a parallel store alongside the project's own

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 1, G2

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0044 — a requirement is a block, liftable as a unit

**Statement.** A requirement is a **block**, not a table row — heading, bolded meta lines, statement as text, links as a trailing list. It must be readable and **liftable as a unit**: copy-pasteable elsewhere without reassembly

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G4

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0046 — the funnel needs a conductor session

**Statement.** Funnel interaction requires a conductor session; Q&A, reports and admin work stay available outside it

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G1

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0047 — the plan proves the measurements carried across

**Statement.** The plan must check the design's measurements are carried in accurately, and show it

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 3, G6

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0048 — every type owes every gate

**Statement.** Every project type owes every gate unless that type explicitly marks it `n/a` with a reason

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G3

**Depends on.** R-0018

**Approval.** none — and this one was **never approved under the old rules either**: it stood at `proposed`, not final, when the register was migrated on 2026-08-14. It has never been agreed by anyone. The Why is unwritten.

---

### R-0049 — due date, not effort

**Statement.** **DUE DATE, not EFFORT** — can it meet the plan in time, an outcome measure, rather than how much work it is, an input measure

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-07/08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** G6

**Depends on.** R-0011

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0050 — the completeness check is tiered

**Statement.** **The completeness check is tiered: the LIGHT check fires at every step; BOTH light and heavy fire at the design GO.** Light is machine facts only — did the register move, do approval hashes still match, are link stamps stale, does declared grounding resolve. Heavy is N independent readers working from the RAW sources, never from a summary, with convergence as the signal

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 3

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0051 — the check binds on facts from outside the model

**Statement.** A completeness check must not be a step the model can assume or skip — it binds on countable facts, from outside the model, never on a question the model answers about itself

**Why.** Not yet written — the migrated source recorded provenance only (2026-08-08 session, via `docs/product/requirements-traceability.md`) and no reason. Awaiting the producer's words; nothing is invented here.

**Traces to.** Law 3

**Depends on.** none

**Approval.** none — migrated 2026-08-14; the Why is unwritten and no earlier approval covered the Why or the links.

---

### R-0052 — the process shows its own working

**Statement (derived).** Kerd shall show the producer, for each step of a work item's journey, what the step is, which mechanism performed it, what that mechanism was given, and what it produced; and Kerd shall not hand a step to a mechanism that cannot supply those four facts.

**Why.** This block replaces R-0039 (*"Never route to superpowers"*), killed 2026-08-14 for foreclosing the build-versus-adopt decision the approved goals keep open. The intent underneath it survives, and these are his words for it, from the G8 grounding in `docs/kerd-goals.md`: *"superpowers does some great things... so we can learn from it, i just want the process to be ours and visable"*. G5 carries the same want as a design input — *"show the work, show the state, show the tools being used"* — and names the failure it prevents: *"its not clear what or why its doing in a black box way"*. **The statement is the model's derivation of a checkable obligation from those words; approving this block approves that derivation.** What the derivation deliberately does not do is name a tool: the test is what a mechanism can show, so any mechanism that meets it is admissible and any that does not is refused — including one we build ourselves. That keeps the decision Law 4 protects open while the visibility his words demand is binding.

**Traces to.** G5, G8

**Depends on.** none

**Approval.** none — drafted 2026-08-14 as the replacement for R-0039. **The statement is the model's draft and awaits the producer's approval; the kill it replaces is authorised, this wording is not.**

---

## Findings

Written for the producer. Nothing below has been acted on.

### 1 — Forty-six requirements have no honest Why, and one reason explains all of them

Forty-four of the 51 blocks carry the same `Source` in the old register:

> `2026-08-07/08 session — docs/product/requirements-traceability.md`

Two more carry the same shape with a different date (`2026-08-08 session —
docs/product/requirements-traceability.md`): R-0050 and R-0051.

That string is a **pointer to where the words came from**, not a reason the
requirement exists. It supports no Why at all. Writing one from it would be
manufacturing rationale, so none was written. The forty-six:

R-0001, R-0002, R-0003, R-0004, R-0005, R-0006, R-0007, R-0008, R-0009,
R-0010, R-0011, R-0012, R-0013, R-0014, R-0015, R-0016, R-0017, R-0018,
R-0019, R-0020, R-0021, R-0022, R-0024, R-0025, R-0026, R-0027, R-0031,
R-0033, R-0034, R-0035, R-0036, R-0037, R-0038, R-0039, R-0040, R-0041,
R-0042, R-0043, R-0044, R-0045, R-0046, R-0047, R-0048, R-0049, R-0050,
R-0051.

*(That list is 46 references; 44 carry the 2026-08-07/08 pointer and two —
R-0050 and R-0051 — carry the 2026-08-08 one. All 46 need his words.)*

**Four have a partial Why** — R-0028, R-0029, R-0030, R-0032. Their source
carries one verbatim ruling of his, *"UX-001 was for the eval matrix only"*
(2026-08-08 21:23), which honestly explains **the scope** of the statement
and nothing else. What is written is exactly that, and it says on the page
that the reason itself is still missing.

**One has a full, honest Why** — R-0023. Its old source carried his words
verbatim and in full; they are carried across unchanged, under the reserved
italic-quotation form.

The register is therefore 1 honest Why, 4 partial, 46 needing his words.

**The single sentence that matters here:** the old register's `Source` field
was a *provenance pointer*, and the new format's Why is a *reason*. The
migration cannot convert one into the other, and no amount of care makes it
possible. This is not a transcription defect — the content never existed.

### 2 — One requirement could not be traced

**R-0031 — "Diagrams render in a sans-serif font."** No goal and no law is
served by it without inventing a rationale. G4 is about a message being
readable rather than a wall of noise, and stretching that to cover a font
family is exactly the forced trace the brief said to refuse. It is left as
`not yet traced` and named here.

Two traces I want you to check rather than trust, because they were the
closest calls:

- **R-0005** (project type and release type are one vocabulary) → **G3**. My
  reasoning: collapsing two type vocabularies into one is in service of "one
  path". It is a definitional claim, and G3 is a defensible but not obvious
  home.
- **R-0039** ("Never route to superpowers") → **G8**. My reasoning: G8's
  grounding in the goals file carries *"i just want the process to be ours
  and visable"*. That is the nearest honest anchor, but the requirement
  itself names no goal.

### 3 — No statement wording was changed

Zero statements were reworded. The brief permitted fixing what the format's
plain-language rules require; I did not exercise it, and the reason is a
judgement you should be able to overturn.

The adopted ISO 29148 word list bans totality words (`all`, `always`,
`never`), superlatives, and vague subjects, and holds that `shall` binds.
Rewriting 51 statements into shall-form is **authorship**, not
transcription — it runs straight into your standing law against
paraphrasing requirements, and the format's own open question 5 admits the
technique for carrying universal force without a totality word *"is nowhere
taught"*. So the statements are verbatim and the violations are listed
instead.

**Statements that fail the word list as they stand:**

| Reference | The problem |
|---|---|
| R-0003 | `never invent one` — totality word |
| R-0007 | `not merely a record` — not a checkable clause |
| R-0012 | `never a sentence` — totality word |
| R-0024 | `never a reason to record less` — totality word |
| R-0028 | `boxes are never coloured` — totality word |
| R-0036 | `nothing in Kerd, ever` — totality word |
| R-0038 | `never at its own install path` — totality word |
| R-0039 | `Never route to superpowers` — totality word **and** no subject at all |
| R-0040 | `never embedded in a product doc` — totality word |
| R-0043 | `never a parallel store` — totality word |
| R-0045 | `it never rewrites the state` — totality word |
| R-0051 | `never on a question the model answers about itself` — totality word |

Most of these are absolute laws expressed with an absolute word, which is
the exact case open question 5 has not settled. **Recommendation: settle
open question 5 first, then reword these twelve as one pass — not
requirement by requirement.**

**One change I did make, and it is notation not content:** every heading
handle is fresh. The old headings were mechanically truncated statements
("…plan enhancements, plan…"), which rule 3 says a handle must not be. Under
rule 3 a handle sits outside the fingerprint and may be reworded at any
time, so this costs nothing and can be overruled freely.

### 4 — What the new format has no home for

Named so it does not vanish silently.

**a. The `refines` link role — collapsed, and this is the one I am least
comfortable with.** The old register had 15 link lines in two roles:
11 `depends-on` and **4 `refines`** (R-0009, R-0010 and R-0012 refining
R-0008; R-0049 refining R-0011). The new format's rule 8 gives one link
between requirements — `Depends on` — and rule 7 reserves `Traces to` for
goals and laws only. So `refines` has nowhere to go. I mapped all four onto
`Depends on`, keeping the direction, on the ground that a refinement
genuinely needs its parent to exist. **The parent/child relationship itself
is lost**, and with it the "is this an origin requirement or a refinement?"
question that the shape doc's own `no parent, by design` marker is built to
answer. Recommend either a second link role or an explicit ruling that
refinement is not modelled.

**b. The suspect-link stamps — dropped, and the shape doc wants them
kept.** Every old link carried its target's hash: `depends-on → FUN-005
(sha256:b76da5ae7fe2)`. Fifteen stamps. Rule 8 says `Depends on` takes
"references only", so there is no slot for them. This is a live
contradiction inside the shape doc itself: its comparison section says of
the suspect-link stamp *"Recommend keeping it; the new draft's links element
is compatible with it"* — but the normative form has no place to write one.
**Recommend resolving this in the format before the migration lands.**

**c. The `Category` field.** All 51 carried one of the twenty codes. The new
reference is deliberately meaning-free and the shape doc recommends
categories become tags. There is no category slot in the block. The taxonomy
survives as *content* (R-0003 requires it to ship) but the per-requirement
filing key is gone.

**d. The `Tags` field.** Twelve requirements carried tags recording the other
disciplines they touch. No home, and unlike categories, nothing else in the
new format records them.

**e. The `State` field, and four requirements that were not `final`.** The
no-status decision is settled, and the migration's blanket unapproval
happens to be correct for all 51. But the old register distinguished
*proposed* (captured, never qualified) from *final* (approved and later
un-approved by a format change), and that distinction is now invisible. The
four never-final requirements were:

- **R-0022** (`route` and rigor derived) — was `qualified`
- **R-0025** (floors compose as a union) — was `proposed`
- **R-0038** (machinery aims at consuming project) — was `qualified`
- **R-0048** (every type owes every gate) — was `proposed`

Under the new file these read identically to the other 47. If "this was
never agreed at all" is worth telling apart from "this was agreed and the
format un-agreed it", the format has no way to say so.

**f. Forty-seven approval hashes.** Deliberately dropped, per the brief.
Recorded here as a count so the scale of the re-approval debt is visible:
47 previously-approved requirements now sit unapproved.

### 5 — What the format did not tell me how to handle

1. **A Why that cannot be written.** Rule 1 requires all five fields and says
   an inapplicable field writes `none`. But a Why is not *inapplicable* — it
   is *missing*, and `none` would assert the requirement has no reason,
   which is false. I wrote an explicit unwritten-Why sentence naming what
   the source actually said. The format has no sanctioned form for this and
   should get one, because a migration is not the last time it will happen.
2. **A trace that is not yet known.** Rule 7 offers targets or
   `no parent, by design`. It has no value for "not yet determined", and
   using the by-design marker would be a false declaration. R-0031 carries a
   written-out unknown instead.
3. **Bulk minting.** Rule 2 says filing refuses a block arriving with a
   pre-written number and the tool assigns. There is no tool, and 51 numbers
   were assigned by hand. The rule has no migration path.
4. **Migration ordering.** Rule 13 says ascending reference order is creation
   order. A migration has no creation order, so I minted in the old
   register's reading order (PRD → FUN → NFR → UX → TECH → OPS → TST). That
   preserves the document you already read, but it bakes the dead category
   taxonomy into the reference sequence permanently — the one encoding rule
   2 exists to avoid. Worth a conscious ruling before this file replaces the
   old one.
5. **A forward dependency.** R-0007 depends on R-0041 — a higher number. The
   format forbids nothing here, but under natural creation order a
   dependency would normally precede its dependent, and this file has one
   that does not.

### 6 — Recommended for the graveyard, not moved

> **ACTED ON 2026-08-14 — this section records the state before the kills and
> is kept for the record only.** Four of the six named below were killed and
> moved (R-0045, R-0016, R-0017, R-0002), together with four this section
> never named (R-0001, R-0004, R-0034, R-0039), on the fuller triage in
> `docs/requirements/triage.md` and with Tony as the named authoriser. **Two
> of the six were not killed:** R-0003 stays live as this section recommends,
> and **R-0044 stays live against this section's recommendation** — the
> triage found its render detail *is* the approved render (level-three
> heading, bold labelled lines, statement as text, links near the end,
> liftable as a unit), so it predicted rule 1 rather than contradicting it.

Each of these is contradicted or overtaken by the format we are migrating
*into*. I have left all six in the live set. Moving one is a kill, and rule
10 requires a named authoriser, which is you.

**R-0045 — "A `final` requirement carries a hash of its statement as
keyed."** The strongest case. It names the `final` state, which no longer
exists, and a fingerprint over the statement alone, which the recipe now
overrides (statement, Why, links). Its surviving payload — *the audit
refuses on divergence and never rewrites the state* — is genuinely valuable
and is already carried by rule 9. Recommend: killed, superseded by whatever
requirement eventually states the fingerprint recipe.

**R-0016 — "Every requirement gets a Category and ID."** Half of it is dead
outright: the shape has no Category. The other half is now rule 2.
Recommend: killed and re-proposed as an identity requirement without the
category clause.

**R-0017 — "Any request is qualified; if durable it becomes a requirement,
through stages to final."** *"through stages to final"* names the
five-state lifecycle the shape deliberately cut. The qualification idea
survives; the stages do not. Recommend: killed and re-proposed without the
lifecycle clause.

**R-0002 — "…and speak in IDs that mean something."** This is a direct
collision, and it is the one I most want you to look at — see below.

**R-0044 — "A requirement is a block, not a table row — heading, bolded meta
lines, statement as text, links as a trailing list."** The principle
(*liftable as a unit*) survives and is exactly what rule 1 implements. The
render detail it specifies is no longer the render. Recommend: killed and
re-proposed as the principle alone.

**R-0003 — the twenty-category taxonomy ships as the default.** Not dead,
but at risk: the shape doc recommends the categories become tags and the
reference go opaque, and it flags that as its own decision with a real cost.
Recommend: leave live, decide the categories question separately.

### 7 — The one thing to look at first

> **CLOSED 2026-08-14 — the question below no longer needs answering, and it
> did not need escalating.** The migration had already struck the offending
> clause in this same file under Law 4's ordering rule (*"if the analysis
> proved a better way, then we go agaist what i said before, we chnage the
> rule"*), which was the correct application of that rule; escalating a
> question your own governing rule has already answered is how the loop it
> exists to prevent gets started. R-0002 was then killed on 2026-08-14 for a
> different reason entirely — what remained after the amendment states a
> purpose, not an obligation — and is in the graveyard. This section is kept
> for the record only.

**R-0002 — "Requirements exist so the producer can review, plan
enhancements, plan releases, and speak in IDs that mean something."**

That requirement is approved in the old register, in your name, and its
final clause is the exact opposite of rule 2 of the format we are migrating
into: *"The uniform `R-` prefix carries no meaning — every requirement wears
the same one."*

The migration has just replaced `PRD-002` — an identifier that told you it
was a product requirement — with `R-0002`, which tells you nothing. The
research reason for that is strong (*every scheme that encoded meaning in
the identifier eventually had the meaning change*) and the shape doc knows
it costs something. But a live requirement in this file now says the
opposite of the file's own numbering rule, and nothing in the format
notices.

The two readings are genuinely different and only you can pick one: either
"IDs that mean something" meant *IDs I can say out loud and point at* — in
which case `R-0002` satisfies it and the requirement stands unchanged — or
it meant *IDs that tell me what kind of thing this is* — in which case
either the requirement goes to the graveyard or rule 2 is wrong.

## Graveyard

*Eight entries. All eight were killed on 2026-08-14 on the recommendations in
`docs/requirements/triage.md`, and Tony is the named authoriser on every one.
The purpose is his, verbatim, 2026-08-14 09:28:* **"we need a graveyard so we
dont add them again and learn from them"** *— which is why the* **What was
learned** *field is written as guidance to the next proposer rather than as a
summary of the death. Links are dropped on death, per rule 10.*

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

### R-0002 — DEAD — what requirements are for

**Killed.** 2026-08-14, by analysis against the approved requirement shape — it is a statement of purpose and the shape gives purpose a home outside the set. Kill authorised by Tony.

**Statement as proposed.** Requirements exist so the producer can review them, plan enhancements, plan releases, and refer to any of them by a name he can say out loud

**Why it was proposed.** Never recorded as a reason. The migrated source carried a provenance pointer only. The statement had one amendment before death, made 2026-08-14 13:10 under Law 4's ordering rule: its final clause originally read *"speak in IDs that mean something"*, which carried two readings — a name he can point at and say, which survives in the handle beside each reference, and an identifier whose prefix tells you what the thing is, which the standards survey found rots, because "every scheme that encoded meaning in the identifier eventually had the meaning change." The first reading was kept and made explicit; the second was struck by analysis. His ruling licensing that amendment: *"if the analysis proved a better way, then we go agaist what i said before, we chnage the rule."*

**Why it is dead.** What remained after the amendment is a purpose, not an obligation. No build can be rejected against it, which is rule 11's test for statement content. Each of its four clauses is already carried by something checkable: review by R-0007 and R-0040, dependency and planning work by R-0007 and R-0041, and the sayable name by rule 3 of the approved shape, which puts a human handle beside every reference. Rule 13 of the shape gives prose about the set an explicit home — a preamble that is never fingerprinted — so this content has somewhere to live that is not a requirement. Keeping it as one dresses an explanation as a contract.

**What was learned.** Apply the rejection test before writing anything down: if no build could fail against the sentence, it is a Why or a preamble, not a Statement. Purpose prose about the whole set belongs in the register's preamble under rule 13, where it costs no approval and no fingerprint. One clause here was genuinely binding and has no home yet — *plan releases* — and that is a gap in the set, not a reason to resurrect this block; whoever picks it up should write it as an obligation on a release artifact that exists, not as a statement of why requirements exist.

**Superseded by.** nothing — killed outright. Its content belongs in the preamble; its checkable clauses are carried by R-0007, R-0040, R-0041 and rule 3 of `docs/design/requirement-shape.md`.

---

### R-0004 — DEAD — applicability is declared, never assumed

**Killed.** 2026-08-14, by analysis against the flat live set — it duplicates R-0048. Kill authorised by Tony.

**Statement as proposed.** Applicability is declared per category — `applies`, or `n/a` with a named reason

**Why it was proposed.** Never recorded. The migrated source carried a provenance pointer only.

**Why it is dead.** R-0048 states the same obligation about the same kind of object: "Every project type owes every gate unless that type explicitly marks it `n/a` with a reason." Same rule, same escape hatch, same demand that the excuse be named. In the old register the two sat under different category headings and read as two requirements; flat in one list they read as one requirement written twice. The duplicate is also the weaker of the two, because its subject noun is the category field the approved shape removed and it depends on R-0003, whose survival is still the producer's call.

**What was learned.** Section headings hide duplicates: two statements about the same obligation look distinct while they live under different headings and identical once the set is read flat. When proposing, read the live set flat and search for the obligation, not for the wording. And prefer the version whose subject still exists in the shape — a requirement keyed to a field the shape does not have is dead the moment the shape lands, however well it is written.

**Superseded by.** R-0048.

---

### R-0016 — DEAD — every requirement is identified and traceable

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

### R-0034 — DEAD — the producer marks the page without typing

**Killed.** 2026-08-14, by analysis against the approved requirement shape — both fields it marks were cut by settled decisions. Kill authorised by Tony.

**Statement as proposed.** The producer marks requirements **on the page without typing** — status, release assignment — and the page saves those marks to a file the next session applies on the word "updated"

**Why it was proposed.** Never recorded as a reason. The migrated source carried a provenance pointer only. What the statement is reaching for is legible in his objection of 2026-08-14 08:16, where he itemised what a generated view owes him — *"no simple way for me to see the requirments and their dependencies"*, *"to add comments perhaps for you to pick up or to record notes around the requirments"*, and *"add links or images perhaps as input"*.

**Why it is dead.** It names two things to mark, *"status, release assignment"*, and the approved shape cut both: "there is no lifecycle or status field on a requirement", and "which release a requirement is in lives on the release, never on the requirement". It therefore specifies a marking interface over two fields that do not exist. The mechanism is not what died — marking on the page, saved to a file, applied on the word "updated" — the fields are.

**What was learned.** An interface requirement inherits every dependency of the fields it touches, so it dies whenever one of them is cut. Before writing one, list the fields it manipulates and check each against the current shape; a requirement that survives that check is worth writing, and one that does not was really a requirement about the data model wearing an interface's clothes. The payload here is worth re-proposing over the fields that do exist — approval, comments, links, and dependency edits — and none of those is status or release membership. Note also what the kill leaves behind: R-0035 still declares `Depends on. R-0034`, and under rule 8 an unresolved reference stops the run, so killing an interface requirement is not finished until its dependents are re-pointed.

**Superseded by.** nothing — killed outright. The marking mechanism over the fields that exist is unproposed; his 08:16 itemisation is the brief for it.

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
