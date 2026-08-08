---
route: new
stage: framed
story: proposal
---

# Human input has no address — it becomes prose, and prose cannot be traced, grouped, or reviewed

## Value

Tony, 2026-08-07, arriving at it across one afternoon. The short form first,
because it is the whole item:

> Your input finally gets an address. — yes! input get clarified into a
> requirment and approved as such. love it.

What the address is for, in his words:

> feature to code traceablity (requirments traceablity basically)

> perhapos we need to ensure we are doing requirements tracebility properly?
> give each requirment a Category and ID (UI001, DATA001 for example) and trace
> it back and forward easily. also helps enhacements, release planning etc

> also allows producer (me) to review requirments and consider
> changes/enhancements and release planning and speak in IDs that mean
> something

How a requirement comes into being — the beat that does not exist today:

> any request should be qualified and if its durable we should make it a
> requirement, might go through stages to be final etc but a lot of the
> converstation we have had today is requirment initial or final development
> right? but we are not tracking or categorizing it yet

And whose capability this is, stated as a standing correction after the session
framed it as Kerd's own bookkeeping:

> so KERD is the skill that people use to build things. kerd needs to give
> those projects this capability ( perversley we need it to build kerd too) so
> i am talking about the scope of the skill here all the time.

> it needs to also write the funnel state, requirments, stage data steps,
> journey etc - right? nothing in kerd, ever. we only do it here to build kerd
> skills.

### What winning is

**A durable human input becomes an addressable thing, in the user's own repo,
and stays addressable for the life of the project.**

The chain that address unlocks, in both directions:

- **Forward** — requirement → the measurement that defines it as met → the
  contract piece that builds it → the commit that landed it. *"What satisfies
  `DATA001`?"* is answerable from disk.
- **Backward** — a commit → the requirement it exists to serve. *"Why does this
  exist?"* is answerable without archaeology.
- **Gaps in both directions become states a machine can name** — a requirement
  nothing builds, and work that serves no requirement.

And the three jobs that are the reason IDs must be **categorised** rather than
merely unique — all three are the producer's, none of them are a build activity:

- **Review** — read a category and judge it as a set, instead of re-reading
  prose to reconstruct what was asked for.
- **Enhancements** — a change is expressible as a new requirement against an
  existing category, so its blast radius is a category rather than a guess.
- **Release planning** — a release becomes a named set of IDs. This is the
  missing artifact from the 2026-08-03 decision that a release is a GROUPING,
  not a time axis, which has had no artifact for four days because there was
  nothing stable to group.

### The chain, in the producer's words

> A useful traceability model usually links these as:
> `Business Goal → Stakeholder Need → Product Requirement →
> Functional/Technical Requirement → Design → Implementation → Test Case →
> Release Evidence → Post-Launch Metric`

**Measured against what this repo has on disk, the funnel covers the middle of
that chain and has nothing at either end:**

| Chain link | Artifact today | State |
|---|---|---|
| Business Goal | — | absent |
| Stakeholder Need | — | absent |
| Product Requirement | `docs/product/<slug>.md` `## Value` | prose, no identity |
| Functional/Technical Requirement | — | absent (this is the register) |
| Design | `docs/design/<slug>.md` | present |
| Implementation | work commit + `Piece:` trailer | present, never exercised |
| Test Case | spec verify commands + the measurement table | present |
| Release Evidence | `docs/gates/*-goal.md` | present |
| Post-Launch Metric | — | absent |

**This explains a hole nobody could name.** `docs/design/funnel-steps.md`
(2026-08-07) defines the steps inside each funnel stage and leaves **Live**
deliberately empty, because no source of any kind could be found for it. Live
*is* post-launch. Category 20 below — adoption tracking, feedback loops,
support metrics, defect triage, iteration backlog — is its missing vocabulary.
The stage was not empty because the work was hard; it was empty because nothing
in the system had words for it.

### The category scheme, supplied by the producer

Given 2026-08-07 as a standard product-definition-to-launch taxonomy. It is
**discipline-based** — which specialism owns the requirement — rather than
domain-based, which is why it travels to any project rather than being fitted
to one.

| # | Code | Category | Covers |
|---|---|---|---|
| 1 | BUS | Business | revenue goals · strategic objectives · market positioning · success metrics · business constraints |
| 2 | STA | Stakeholder | executive · customer · sales · support · partner needs |
| 3 | USR | User | personas · jobs to be done · user workflows · accessibility needs · usability expectations |
| 4 | PRD | Product | product scope · feature requirements · use cases · MVP definition · out-of-scope items |
| 5 | FUN | Functional | system behaviours · feature logic · user actions · rules and calculations · workflow states |
| 6 | NFR | Non-functional | performance · scalability · reliability · availability · maintainability |
| 7 | UX | UX/UI | interaction patterns · navigation · visual design constraints · content requirements · responsive behaviour |
| 8 | TECH | Technical | architecture · APIs · data models · infrastructure · platform/browser/device support |
| 9 | INT | Integration | third-party services · internal systems · import/export · webhooks · API contracts |
| 10 | DATA | Data | capture · retention · quality · reporting data · migration |
| 11 | SEC | Security | authentication · authorization · encryption · audit logging · threat mitigations |
| 12 | PRIV | Privacy | consent · personal data handling · deletion · user controls · disclosures |
| 13 | CMP | Regulatory / Compliance | legal obligations · industry standards · certification · records retention · compliance evidence |
| 14 | ANA | Analytics / Measurement | events · funnels · KPIs · experimentation · launch success tracking |
| 15 | OPS | Operational | monitoring · alerting · incident response · admin tools · runbooks |
| 16 | SUP | Support | help content · support workflows · troubleshooting tools · known-issue handling · customer communications |
| 17 | TST | Testing / Validation | acceptance criteria · test cases · verification methods · UAT · regression coverage |
| 18 | REL | Release | launch criteria · rollout plan · feature flags · migration plan · rollback plan |
| 19 | DOC | Documentation | user docs · internal docs · API docs · training materials · release notes |
| 20 | POST | Post-Launch | adoption tracking · feedback loops · support metrics · defect triage · iteration backlog |

**ID format:** `<CODE>-<NNN>`, e.g. `UX-001`, `DATA-001`. Stable for the life of
the project; never renumbered, never reused.

### Not every project owes every category — applicability must be declared

Tony, 2026-08-07, on seeing that Kerd fills four categories and leaves five
empty:

> not every project is the same structure, so requirments are not the same
> everytime, so we dont have a structure for storeing all rquirments types so
> maybe we need to have a minimum set or temolates that we use for types of
> projects or sugest classifications from a list?

**The requirement underneath the three options: emptiness carries no meaning
until applicability is declared.** An empty `SEC` in Kerd is correct — there is
no security surface. An empty `SEC` in a payments product is a defect. Today
those two are indistinguishable, so "empty" is not a signal at all. This
falsifies a line in an earlier draft of this frame which claimed an empty
category is information; it is information only once the project has said
whether it owes that category.

Each category therefore carries one of two dispositions, and **`n/a` requires a
named reason** — the same discipline the risk ledger already enforces on
`accepted`, and the rigor design on a waiver:

| Disposition | Meaning | Empty means |
|---|---|---|
| `applies` | this project owes requirements here | a gap |
| `n/a — <reason>` | it does not, and why | correct |

The three options in the quote are then one mechanism, not a choice between
three:

- **the full twenty** is the catalog
- **templates by project type** pre-fill the disposition so the producer edits
  deviations rather than ruling on twenty rows
- **a minimum set** is the floor — a `production-v1` project cannot mark `SEC`
  or `PRIV` as `n/a`, exactly as `docs/design/rigor-level.md` decided that
  production-v1 cannot waive security

**This is `rigor-level` slice 2's object, not a new one.** That slice is
designed and unbuilt, and its own description is *"catalog + pre-filled
disposition table (producer touches deviations only)"*. Two disposition
mechanisms declaring what a project does and does not owe would eventually
disagree with each other. Whether they share one table or one pattern is a
design-rung decision; that they must not be invented twice is recorded here.

**This scheme ships as the default.** An earlier draft of this frame claimed
every hardcoded scheme is wrong; that was falsified by the producer supplying
one. The distinction it missed: *domain* categories cannot be hardcoded because
they describe the thing being built, but *discipline* categories can, because
they describe who owns a requirement — and that is the same in every project. A
project may extend the set; it does not have to invent one.

### The unit, and why prose fails at it

The unit of value is **a sentence the producer can say and the machine can
check**: *"`DATA001` is unbuilt"*, *"this commit serves no requirement"*,
*"`ROLE001` through `ROLE004` are the next release"*. Every one of those is
answerable today only by reading everything, which means in practice it is not
answerable.

Prose loses the thread for a nameable reason: it gets summarised, paraphrased
and compressed at every boundary, and none of those operations preserve a
handle. An ID survives all three. That is the entire mechanism.

This is the 2026-08-07 root cause with a countermeasure attached. Tony that
morning: *"we solve for code level but all the context is not code — much of it
is human input that we lose."* Code leaves artifacts that cannot lie; human
input leaves nothing unless a model chooses to write it down. An ID is the
cheapest artifact that makes a human contribution un-losable, because it makes
it referenceable — and a reference can be checked.

## Grounding

- docs/design/conductor-role.md — the graduation map; deleting the plan gate is what surfaced this
- docs/design/funnel-steps.md — the steps inside each stage, where a requirement obligation would land
- docs/design/risk-ledger.md — the precedent this borrows: every row in exactly one state from a closed set
- docs/product/funnel-driver.md — the driver frame; this item was cut out of its slice 2
- docs/product/switch-fidelity.md — gaps 8-14, the diagnosis of losing human input
- docs/state-contract.md — who owns and reads which files
- tools/gates/kit.py — the gate ladder, and the ROOT derivation that stops the machinery travelling
- hooks/session-start.sh — the CLAUDE_PROJECT_DIR pattern that already solves aiming
- CONTEXT.md — the standing decisions this must not violate

## The gap list

### Gap 1 — the register already exists, disguised as a decisions list

`CONTEXT.md` `## Key Decisions` is doing the job of a requirements register and
cannot do it: append-only prose, no IDs, no categories, no state. It cannot
answer *show me every ROLE requirement*, *what changed since Tuesday*, or
*which of these are in the next release* — which are exactly the three jobs
named in Value.

### Gap 2 — measured live: forty-three requirements produced across one session and its follow-on, none tracked

Extracted from this session's own conversation on 2026-08-07, which is the
demonstration Tony asked for (*"a lot of the converstation we have had today is
requirment initial or final development right?"*):

Filed under the producer's own taxonomy above. **Extended at the session's close
(2026-08-07 21:30) when Tony asked "okay we captured all requirements we defined
today before we close out?"** — the honest answer was no. The count went from
eight to forty-three, because the session kept producing requirements while
the register that would hold them did not exist.

| ID | Requirement (compressed) | State |
|---|---|---|
| **FUN** | | |
| FUN-001 | Approving the design is enough — no plan-approval gate | final |
| FUN-002 | A plan is execution of the design, carrying the measurements that prove the goals met | final |
| FUN-003 | Every requirement gets a Category and ID, traceable back and forward | final |
| FUN-004 | Any request is qualified; if durable it becomes a requirement, through stages to final | final |
| FUN-005 | Project type is declared once at conductor start, from the list, and not re-asked once a project has started | final |
| FUN-006 | The goal gate increments the project type to the next appropriate type | final |
| FUN-007 | Conductor may suggest a type change — at the gate or mid-flight — and the producer agrees it | final |
| FUN-008 | Type is a stack: items inherit the project's type, an override is opt-in and forward-only | final |
| FUN-009 | `route` and `Rigor level` are derived from project type, not declared | qualified |
| **PRD** | | |
| PRD-001 | Kerd gives consuming projects this capability; Kerd is only a user of it | final |
| PRD-002 | Requirements exist so the producer can review, plan enhancements, plan releases, and speak in IDs that mean something | final |
| PRD-003 | The twenty-category discipline taxonomy ships as the default; projects extend it, never invent one | final |
| PRD-004 | Applicability is declared per category — `applies`, or `n/a` with a named reason | final |
| PRD-005 | Project type and release type are the same thing for the twelve types that ship; Ideation, Spike and Security Review produce findings instead | final |
| PRD-006 | The alignment gate is a shared structure both parties can point at — a drawing is its usual form, not its only one | final |
| **TECH** | | |
| TECH-001 | The user's repo holds funnel state, requirements, stage data, steps and journey — nothing in Kerd, ever | final |
| TECH-002 | Traceability runs the nine-link chain: Business Goal → Stakeholder Need → Product Requirement → Functional/Technical → Design → Implementation → Test Case → Release Evidence → Post-Launch Metric | final |
| TECH-003 | The machinery must aim at the consuming project, never at its own install path | qualified |
| TECH-004 | Never route to superpowers | final |
| **NFR** | | |
| NFR-001 | The boundary records everything agreed; efficiency is a tiebreaker, never a reason to record less | final |
| NFR-002 | Floors compose as a union — a nested piece owes its own type's floor plus every floor of the project containing it | proposed |
| NFR-003 | A spike carries its own rigor: scope boundary, timebox, spec, design, and measurements | final |
| NFR-004 | The mechanism must not scatter artifacts | final |
| **TST** | | |
| TST-001 | The plan must check the design's measurements are carried in accurately, and show it | final |
| TST-002 | Every project type owes every gate unless that type explicitly marks it `n/a` with a reason | proposed |
| **TECH (cont.)** | | |
| TECH-005 | The register is a standalone file at a known location — never embedded in a product doc — so it can be read quickly by a person and directly by a tool | final |
| TECH-006 | A requirement row carries its **dependencies** on other requirement IDs | final |
| TECH-007 | The mechanism must be git-repo native and Claude Code friendly, per project | final |
| TECH-008 | The register must be **the same files** — one representation, never a parallel store alongside the project's own | final |
| **OPS** | | |
| OPS-001 | Funnel interaction requires a conductor session; Q&A, reports and admin work stay available outside it | final |
| **PRD (cont.)** | | |
| PRD-007 | The register is the data source for release planning, dependency and visualization tooling — not merely a record | final |
| PRD-008 | The evaluation mark set is `◎` perfect · `○` fully meets (`○+`/`○-`) · `△` meets with a countermeasure (`△+`/`△-`) · `×` cannot meet | final |
| PRD-009 | `×` means cannot meet **even with a countermeasure**; cross takes no modifier, because there is no degree of impossibility | final |
| PRD-010 | Building the missing piece ourselves **is** a legal countermeasure — marked `△-`, with its cost carried by the summary columns rather than hidden in the mark | final |
| PRD-011 | Every evaluation carries four summary columns: **COST · QUALITY · DUE DATE · RATING** | final |
| PRD-012 | A mark that is not `◎` or `○` states why, in a few words — never a sentence | final |
| PRD-013 | Dependency cost is judged **marginally and proportionately**: what the option adds beyond what the project already needs, weighed against the share of value it buys. An ecosystem-normal install is not a burden; a whole new runtime bought for a fraction of the value is | final |
| **UX** | | |
| UX-001 | Boxes are never coloured; the mark carries the verdict — `○` green, `△` yellow, `×` red | final |
| UX-002 | A mark is drawn at 40–50% of the cell it sits in | final |
| UX-003 | Column and row headings render as headings — `GROUP: CRITERION NAME`, `OPTION n: ID`, with the declaration below | final |
| UX-004 | Diagrams render in a sans-serif font | final |
| UX-005 | The preferred option's verdict cell is filled green | final |
| UX-006 | The point of a table is to **avoid reading lots of text** to understand it — brevity is the requirement, not a preference | final |
| **TST (cont.)** | | |
| TST-003 | **DUE DATE, not EFFORT** — can it meet the plan in time, an outcome measure, rather than how much work it is, an input measure | final |

**States are honest, not flattering.** `final` means Tony stated it directly.
`qualified` means the wording is agreed but was synthesised rather than spoken.
`proposed` means it is the model's derivation from his input and he has not
ratified it — NFR-002 and TST-002 are both consequences drawn while writing,
and TECH-003's framing was corrected twice before settling. Four of
forty-three are not `final`, and marking them so is the difference between a
register and a flattering list.

**The measurement this table is: forty-three durable requirements produced in
one session, zero promoted through any beat, because no beat exists.** Eight
were counted at 18:00 and the number more than tripled over the next three
hours while the session discussed building the thing that would have caught
them. Filed here as frame evidence — **this is not the register**, which is
slice 1's build and whose design is currently blocked.

**TECH-005 makes this table's own location a defect.** Tony at 21:33: *"i think
we also have to separate the requirements table to its own file or location so
we can use that quickly. its also the basis of any visualization or tooling
around releases and dependency."* A table buried inside a product doc's gap
list cannot be read quickly by a person or at all by a tool. Its placement here
is deliberate and temporary — frame evidence must live in the frame — and it is
the first thing slice 1's build moves.

**TECH-006 is new and has no home in the current design.** The design package
defines a five-column row with no dependency field. Dependency is also the
missing artifact from a standing decision: 2026-08-03 settled that a release is
a GROUPING whose five deciding factors begin with *"dependency forbids (hard
constraint)"*, and nothing on disk has ever expressed a dependency. Requirement
IDs linked to other requirement IDs are that artifact, which is why PRD-007
matters — the register is a **data source**, not a record. It becomes a
nineteenth block against the design package, and the first thing to fix when it
is re-worked.

All forty-three lived as prose until this table. The extraction took one pass
and immediately exposed something invisible in prose: **four of the forty-three
are not `final`** — `NFR-002` and `TST-002` are `proposed`, `FUN-009` and
`TECH-003` are `qualified`. A state column made a distinction visible that
paragraphs had hidden — which is the argument for the whole item, and the same
result the journey page produced on its first render.

**Two things the filing exercise itself showed.** Nine of the forty-three land
in `FUN`, and the whole set fills only **seven of the twenty categories** —
`UX`, `INT`, `SEC`, `PRIV` and `CMP` are among the thirteen left empty, because
Kerd has no UI, no integrations, no user data and no security surface. That is
evidence the scheme is general rather than fitted to this repo, and a warning
that **Kerd is a thin dogfood for it**: the capability will ship having
exercised under a third of its own categories. And `NFR-001` filed itself —
"fidelity beats efficiency" is a textbook non-functional requirement, and it had
spent four months as a paragraph nobody could reference.

### Gap 3 — requirements have no identity anywhere in the chain

| Link | Artifact | Identity today |
|---|---|---|
| Requirement | `docs/product/<slug>.md` `## Value` | prose, quoted verbatim — none |
| Gaps | `### Gap N` | numbered per-doc, not addressable across docs |
| Measurement | the design doc's stage-1 measurement table | table rows — none |
| Piece | `docs/plans/*-<slug>-spec.md` `## Pieces` | numbered `Step N` |
| Code | work commit `Piece: <slug>/<n>` trailer | built at v0.91.0 |

Piece → code is wired. Requirement → measurement → piece is not, so no question
about a requirement can be answered mechanically.

### Gap 4 — the promotion beat does not exist

Today a request becomes prose inside `## Value` and is never promoted to
anything. Tony's sequence — **request → qualified → durable? → requirement →
stages → final** — has no step, no artifact and no approval anywhere in
`skills/`. `/kerd:interrogate` qualifies *risks* on exactly this shape (sized,
evidenced, in exactly one state); nothing does it for requirements.

### Gap 5 — the machinery cannot aim at the project that owns the state

`tools/gates/kit.py:24` derives `ROOT` from the tool file's own path. The plugin
cache ships `tools/`, so the code travels — but run from a consuming project it
resolves to **the cache**, not that project. `gate.py` has no argument parser.

Since the funnel state belongs to the user's repo (DIST002), the tools that
derive and render it have to read it there.

**The pattern is already in this repo and predates the problem.** All four
hooks solve exactly this: `${CLAUDE_PLUGIN_ROOT}` finds the *script*,
`$CLAUDE_PROJECT_DIR` finds the *state*, and each hook guards the variable and
`cd`s there before doing anything. Shipping since v0.19.0. The Python tools
never got that treatment because they were written as Kerd's own build
machinery and never as something that travels. This is one class of file
missing a pattern the repo already proved, not a new design problem.

### Gap 6 — the chain has nine links and this repo holds the middle five

Set against the producer's chain (Value, above), `Business Goal` and
`Stakeholder Need` have no artifact at the top, and `Post-Launch Metric` has
none at the bottom. The funnel starts at Product Requirement and stops at
Release Evidence.

The bottom hole is already visible in the machine and nobody could name it:
`docs/design/funnel-steps.md` leaves the **Live** stage empty because no source
for its steps could be found. Live is post-launch, and the missing vocabulary is
category 20.

The top hole is quieter and probably worse. Nothing in this repo records *why a
piece of work is worth doing in business terms*, so every prioritisation
argument is re-had from memory — which is what the 2026-08-03
choose-what-matters work was trying to fix from the other end, with axes rather
than with recorded goals.

**Slice 1 does not close either end.** It builds the register at the link where
the break is (`Functional/Technical Requirement`), and both holes are recorded
here so that a later slice has somewhere to start rather than rediscovering
them.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Requirements are recorded but the promotion beat is skipped under time pressure, so the register holds the easy requirements and loses the contested ones — which are the valuable ones | yes | the capability is delivered and the loss it exists to stop continues, now with a register that looks complete; worse than absent because it reads as coverage | high — the beat costs producer attention at the exact moment work wants to start, and today's session shows the pull is strong | gap 2: forty-three requirements produced across one session and its follow-on and zero promoted, in a session explicitly about this problem | countermeasure - permanent | promotion is a declared artifact with a gate, on the `## Value` precedent — the one piece of human input that reliably survives is the one gate.py refuses without; a project that declares no categories is silent rather than red, so opting in is explicit | the first session that produces a durable requirement and records it only as prose re-argues this row |
| Retrofitting IDs onto finished work manufactures requirements nobody ever stated | yes | fabricated traceability passes its own check and cannot be told apart from the real thing, which destroys the register's only value | high — 20 slugs exist, 8 have walked the full ladder, and the backfill looks cheap and tidy | the grounding-was-read precedent (2026-08-05) refused retrofits for exactly this reason and made declaring the act of opting in | countermeasure - permanent | forward-only by construction; no retrofit of any existing slug, and the hole where finished work sits is recorded as the honest state | the first request to backfill IDs onto a completed slug re-argues this row |
| The machinery cannot aim at a consuming project, so the capability degrades to a naming convention nobody checks | no | traceability is asserted and unenforced in every repo that is not Kerd, which is every repo the capability is for | high — certain as built today, not probabilistic | gap 5: kit.py:24 derives ROOT from the tool's own path; gate.py has no argument parser; the cache ships tools/ so the code is present and merely misaimed | countermeasure - permanent | apply the hooks' existing pattern — `${CLAUDE_PLUGIN_ROOT}` for the script, project dir for the state; lands in slice 1 as a hard dependency, and the library already takes `root` as a parameter everywhere so this is a CLI argument rather than a refactor | the first consuming project whose check audits the cache instead of itself re-argues this row |
| The machine can check an ID is present and mapped; it cannot check the mapping is true — a piece naming a requirement it does not build passes green | no | the check certifies structure and gets read as certifying substance, so a requirement gap survives a green run | high — a property of the design, not a defect that might not occur | the same declared limit already carried by AU5 (resolution is not comprehension) and fidelity.py (reachability is not comprehension) | accepted | | the first requirement that passes the check and turns out unbuilt re-argues this row |
| The producer authors requirement IDs and the model authors everything downstream, so filing drifts toward what is convenient to build rather than what was asked for | no | the vocabulary stops meaning what the producer meant, which destroys "speak in IDs that mean something" | low — downgraded when the producer supplied a standard discipline taxonomy on 2026-08-07; a fixed external scheme is far harder to drift than one a session invents | the v0.92.0 rename shows the failure is real (names ratified at v0.66.0 came back describing the opposite roles), but that scheme was authored in-session, which this one is not | countermeasure - permanent | the twenty categories are fixed and shipped; a project may extend the set, but no session adds a category without the producer naming it | the first category added by a session rather than by the producer re-argues this row |
| Kerd exercises about a quarter of its own taxonomy, so the capability ships tested against a narrow slice of what it claims to cover | no | filing rules for UX, INT, SEC, PRIV and CMP requirements are unexercised at ship; a consuming project meets those bugs first | high — structural, not probabilistic: this repo has no UI, no integrations, no user data and no security surface | gap 2: filing this session's forty-three requirements put twelve in PRD and left thirteen of the twenty categories empty | accepted unknown | | the first consuming project to file a UX, INT, SEC, PRIV or CMP requirement re-argues this row |
| The `Piece:` trailer, the code end of the chain, has never once been written | no | the forward trace stops at the contract and "requirement to code" is unproven | medium — built and untested rather than known-broken; the product is unfinished so no usage metric exists either way | zero trailers across the 40 commits since v0.91.0, explainable by no contract-run work in that window | accepted unknown | | the first work commit that should carry a trailer and does not re-argues this row |

## Killer risk, read out

**The two killers pull in opposite directions, and together they set the
slice.**

The first is the discipline risk, and it is the one that actually kills this.
Every other row is about machinery; this one is about a beat costing the
producer attention at the exact moment work wants to begin. The evidence is not
hypothetical or borrowed — this session produced forty-three durable
requirements while explicitly discussing the need to capture them, and promoted
none. The
countermeasure is the only one this repo has ever seen work on human input: make
it a declared artifact the machine refuses without, exactly as `## Value` is.
Encouragement has a measured success rate of zero here.

The second says the obvious way to make the register look complete is the way
that ruins it. Twenty slugs exist; eight have finished. Giving them IDs
retroactively would take an afternoon and would produce requirements nobody
stated — the hollow-declaration failure the grounding retrofit was refused for.
Forward-only leaves a visible hole where the finished work is, and that hole is
the honest state.

**The third row is loud but not a killer, and an earlier draft of this frame
had it wrong.** It reads as fatal — a capability that cannot enforce itself
outside this repo. It is not, because the fix is a pattern the repo has shipped
since v0.19.0 in four files, and the library it applies to is already
parameterised for it. It was graded a killer once on the reasoning that Kerd
treats refusal as the test that counts; that test was set for Kerd policing
itself, and importing it here promoted a known, cheap, solved problem into a
blocker.

## Release slice

Rigor level: mvp

**Slice 1 — a durable input becomes an addressable requirement, in the user's
own repo, and the machinery can read it there.** The smallest cut where a
project that is not Kerd gets the value.

- **The register.** One declared artifact in the user's project holding
  requirement rows: ID, category, the requirement in the producer's words, and
  exactly one state from a closed legal set — the risk-ledger shape, which this
  repo has already proven and machine-checks today.
- **The category scheme ships as a default.** The producer's twenty
  discipline-based categories, with the `<CODE>-<NNN>` ID format. A project may
  extend the set; it never has to invent one.
- **A declared disposition per category** — `applies`, or `n/a` with a named
  reason. Without it an empty category cannot be told from a missing one, which
  is the state today. Pre-filling by project type and the per-level floors are
  excluded from this slice (below); slice 1 only requires the declaration to
  exist and be one of the two legal values.
- **The promotion beat.** Request → qualified → durable? → requirement, with
  the producer's key on the promotion. This is the killer risk's countermeasure
  and it is what makes the register non-empty.
- **The tools can aim.** `${CLAUDE_PLUGIN_ROOT}` for the script, the project
  directory for the state — the hooks' existing pattern applied to
  `tools/gates/`. Hard dependency, not a follow-up.

**Deliberately excluded, each with its reason:**

- **Any retrofit of the twenty existing slugs.** The second killer risk. The
  hole closes as those items are next touched.
- **Wiring requirements into the measurement table and the contract pieces.**
  The forward half of the trace. It needs the register to exist first, and
  building both at once means neither gets a real test. Slice 2.
- **Project-type templates and the per-level floors.** The pre-filled
  disposition (producer edits deviations only) and the rule that a
  `production-v1` project cannot mark `SEC` or `PRIV` as `n/a`. Both are real
  requirements and both are the *same object* as `rigor-level` slice 2, which
  is designed and unbuilt — building a second disposition mechanism here would
  guarantee two places that disagree about what a project owes. Excluded until
  that overlap is settled at the design rung.
- **The release-planning artifact.** This slice makes it expressible; building
  it is its own work.
- **Rendering the trace on the journey page.** The page should render something
  that already exists, not be where it is defined.
- **File-level backward trace.** Commit-level backwards comes free with the
  `Piece:` trailer. File-level needs something this repo does not have, and is
  not required by the producer's three jobs.

## What we ruled out

- **IDs on the `## Value` statement itself.** Traces one link further up, and
  was rejected because the value statement is quoted verbatim from the producer
  — imposing structure on it is the fastest way to stop it being his words. The
  register references the statement; it never replaces it.
- **Framing this as funnel-driver slice 2.** It was cut out of that item on
  2026-08-07. Different value, different risks, and the gates would report it
  untracked. funnel-driver keeps the plan-gate work, which is small and now
  unblocked.
- **Splitting "requirements" from "the state lives in your project".** They
  were briefly two candidate items. Split, each is a half-feature: traceability
  without the state in the user's repo is a naming convention, and the state
  without requirements has no handle.
- **Adopting an external memory or session-report tool to hold the register.**
  Standing decision (memory tools: adopt none) — they break git-portable
  handoff, and the register must live in the user's repo as ordinary committed
  files like everything else Kerd writes.

## What this is not

- **Not a ticketing system.** No status workflow, no assignee, no sprint. The
  ladder already carries where work *is*; this carries what the work is *for*.
- **Not a replacement for the value statement.** The prose stays, verbatim. IDs
  are handles onto it, never a compression of it.
- **Not machine-verified correctness.** The check proves presence and mapping.
  Whether a piece truly builds the requirement it names is human judgment at the
  goal gate, and the ledger records that limit rather than implying it away.
- **Not Kerd's own bookkeeping.** Everything this repo carries under
  `docs/product/`, `docs/design/`, `docs/gates/` and the boards is dogfood —
  Kerd is a user of the capability, never where the data lives.
