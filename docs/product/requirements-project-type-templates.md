---
route: new
stage: framed
story: proposal
---

# Requirements project-type templates

## Value

Not every project is the same shape, so the requirements it owes are not the
same either. A project declares its **type**, and the type says which
categories are required, which are conditional, and which are usually not
applicable — plus the gates that type must pass and the floors it cannot go
below. The producer edits deviations rather than ruling on twenty categories
from scratch, and no project can quietly skip a gate that its type says is
mandatory.

*(Drafted from Tony's framing 2026-08-07 and approved by him verbatim: "yes
thats it".)*

## Annotation round 1 (2026-08-07, on `docs/plans/project-types.excalidraw`)

Tony's annotations on the drawing, verbatim, and what each settles:

> on conducter start, we show the list and ask user to pick STARTING POINT but
> only if project has not already started.

**The type is declared once, at conductor start, from the floors table below —
not per work item, and not re-asked once the project is under way.**

> Then we have the correct project type that can increment upon goal achieved
> to the next appropriate project type and avoid the confusion.

**The type is a project's current STATE, and the goal gate advances it.** This
answers the open question the drawing posed — whether the type belongs to the
work item or to the release. It is neither: the project holds one current type,
every item inherits it, and achieving a goal increments it to the next
appropriate type (Ideation → Spike → MVP → Pilot → Beta → Full Release →
Maintenance). **Consequence: movement 5's second cost dissolves.** There is no
retrofit problem for the twenty existing slugs, because the type was never
per-slug — nothing needs a type it cannot honestly acquire.

> any not /conductor session does not interact with project funnel and is
> blocked - needs to be in a /conductor session to proceed.
>
> this allows for basic q and a or reports or admin work to be done outside of
> that funnel flow by users in repo

**Funnel interaction requires a conductor session; everything else stays open.**
A refusal, not a convention — and one no skill text can enforce on itself, since
a model choosing to comply is not a check. The layer that can enforce it is a
hook, which fires outside the model.

## Annotation round 2 (2026-08-07, in conversation)

**Conductor may propose a type change, and the producer agrees it.** Tony:
*"'/conductor' can suggest or agree to a project type change also. i.e. we need
a spike before MVP now that we have done a little analysis, or we completed
goal so suggest pilot not beta as tests are good."* Two mechanisms, and they
carry different risk:

| Trigger | What moves | Risk |
|---|---|---|
| **At the goal gate** | the type advances, and the next one is chosen on evidence rather than taken from a fixed order | low — a gate fires, the producer's key is already on it |
| **Mid-flight** | the type changes because what was learned invalidated the type chosen | higher — no gate fires; nothing is checking |

**The transition is worth more than the state.** *"We are in Spike"* is
recoverable from disk cheaply. *"We went MVP → Spike because the analysis
showed X"* is the expensive half, and it is the class of human input the
2026-08-07 root cause says is lost by default. A type change writes a dated
record carrying the reason and the producer's key — the shape
`docs/gates/<date>-<slug>-<rung>.md` already has.

**Named risk — type-thrash.** Each change is individually reasonable; the
sequence can be pathological. A project that keeps stepping back to Spike never
ships, and with only the current type on disk nothing would show it. The
transition record is the countermeasure and is free once transitions are
written: thrash is a visible shape in a history and invisible in a current
value.

**A nested type is a stack, not a replacement.** Tony: *"a spike can be run
within MVP imo."* The project keeps its type; a piece of work inside it may
declare its own. Items **inherit** the project's type by default, so the
retrofit dissolution from round 1 still holds — an override is opt-in and
forward-only, and nothing existing needs a type it cannot honestly claim.

**The floor rule that follows: floors COMPOSE AS A UNION.** A nested piece
satisfies its own type's floor *and* every floor of the project containing it.
A spike inside an MVP owes scope-and-timebox (its own) plus
security-before-exposure (the MVP's). Without this, "run a spike" becomes the
documented way around G6.

> **Amended in the same round.** The first wording was *"a nested type may
> raise rigor, never lower it"*, which assumes `spike < mvp < production-v1` is
> an ordering. It is not — see below — so "raise, never lower" is undefined
> between them. Union needs no ordering and says the same thing where an
> ordering does exist.

## Annotation round 3 (2026-08-07, in conversation)

> spikes need rigor also, the need to be scoped

> there is a spec and measurermnt as well as a design - its not a free for all

**A spike is not the low-rigor case; it is rigor on a different axis.** Its
floor is already written into the Spike template above — **scope boundary,
timebox, output expected, decision criteria** — enforced by that type's own
gate: *"Prototype work may start only after timebox, scope boundary, and output
are approved."* And it carries **a spec, a design and measurements** like any
other type: the spec is the spike plan rather than a product spec (G2 in the
Spike table says exactly that), the measurements are its decision criteria, and
the design is how it will answer its question.

**This exposes a readability defect in this document, of the hollow-waiving
shape.** The universal-gates section says the gates *"apply to every project
type unless the type explicitly says the gate is not applicable"* — so omission
is not exemption. But the per-type gate tables list only *some* gates: Spike's
names Entry, Spec, Build, Security and Exit, and never mentions G3 design or
G4 build-traceability. A reader who reads the Spike section alone would
conclude a spike owes no design. **The per-type tables were partial views, not
the law**, and nothing on the page said so.

**FIXED in the same round (2026-08-07).** All fifteen tables now carry all nine
gates — 135 cells — with every omission converted to an explicit `n/a` carrying
its reason. Tony's original wording is preserved verbatim in every row he
wrote; only the missing rows are new. Omission can no longer read as exemption,
because there are no omissions.

**What filling them out showed: only 6 of 135 cells are `n/a`, and 5 of those
are Ideation.** The gates are very nearly universal. Ideation is exempt from
almost everything because it builds nothing; Spike's single `n/a` is G7 launch,
and even that is conditional — *"n/a unless the prototype is deployed, and if
it is deployed this stops being a spike."* Every other type owes every gate.
That is a stronger claim than the original document made, and it was invisible
until the empty cells had to be filled one at a time.

**This closes the killer risk on a different work item.**
`docs/product/rigor-level.md:51` grades **hollow waiving** as fatal, and the
reason it grades the likelihood *medium* rather than low is stated there:
*"waiving IS the designed cheap path for spikes, so the habit is licensed."*
Spike was the level at which waiving everything was legitimate, which is what
licensed the habit everywhere else. With a spike carrying mandatory items of
its own, waiving is no longer the cheap path at any level, and the row's
likelihood argument no longer holds as written.

**Consequence for the rigor axis: the three levels are not a ladder.** An MVP
requires no timebox; a spike requires no launch readiness. They are three
disposition *profiles*, not three rungs, and comparisons of the form "more
rigorous than" are not defined between them. Only the union rule above is.

These templates sit on top of the stable requirement category scheme:

These templates sit on top of the stable requirement category scheme:

`BUS`, `STA`, `USR`, `PRD`, `FUN`, `NFR`, `UX`, `TECH`, `INT`, `DATA`,
`SEC`, `PRIV`, `CMP`, `ANA`, `OPS`, `SUP`, `TST`, `REL`, `DOC`, `POST`.

Canonical requirement IDs stay category-based: `PRD-001`, `FUN-001`,
`SEC-001`, `UX-001`. Project type is a field, not part of the ID.

## Universal requirement row

```text
ID:
Project Type:
Category:
Subtype:
Title:
Requirement Statement:
Source / Rationale:
Priority:
Owner:
Status:
Acceptance Criteria:
Verification Method:
Trace Links:
Evidence:
Decision / Launch Gate:
```

## Universal gates

These gates apply to every project type unless the type explicitly says the
gate is not applicable.

| Gate | Name | Rule | Required evidence |
|---|---|---|---|
| G0 | Intake qualified | The request has an owner, reason, and project type. | Intake note or opportunity row |
| G1 | Requirement disposition declared | Each category is marked `applies` or `n/a` with a reason. | Category disposition table |
| G2 | Spec approved | Build cannot start until the approved spec exists. | Approved product/spec artifact with requirement IDs |
| G3 | Design / approach approved | Implementation cannot start until the approach is accepted for the chosen rigor level. | Design, spike plan, technical approach, or explicit waiver |
| G4 | Build complete | Work is traceable back to requirement IDs. | Commits, PRs, tickets, or implementation notes linked to IDs |
| G5 | Verification passed | Acceptance criteria and required tests have evidence. | Test results, UAT notes, QA record, or review checklist |
| G6 | Security / privacy reviewed | Nothing can go to production, production data, or external users without the required security and privacy review. | Security review result, privacy assessment, or approved risk acceptance where policy permits |
| G7 | Launch readiness approved | Release, support, rollback, monitoring, and documentation are ready. | Launch checklist |
| G8 | Post-launch evidence captured | The launch result is measured against the success criteria. | Metrics, support signal, incidents, feedback, or close-out |

Hard stops:

- **No build without G2.**
- **No production exposure without G6.**
- **No general availability without G5, G6, and G7.**
- **No closure without G8, unless the project type is explicitly discovery-only.**

## 1. Ideation / Exploring

Use when the work is still about whether the idea is worth pursuing.

```text
Artifact Type: Opportunity / Hypothesis
ID: IDEA-001 or HYP-001
Problem:
Target User / Segment:
Hypothesis:
Why Now:
Evidence We Have:
Evidence Needed:
Assumptions:
Constraints:
Risks:
Success Signal:
Decision Needed:
Next Step:
```

Required categories:

| Disposition | Categories |
|---|---|
| Required | `BUS`, `USR`, `PRD`, `ANA` |
| Conditional | `STA`, `SEC`, `PRIV`, `CMP`, `DATA` |
| Usually n/a | `FUN`, `TECH`, `OPS`, `REL`, `DOC`, `POST` |

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. State the problem, user, and decision needed. |
| G1 Disposition | Required. Empty categories only mean something after disposition is declared. |
| G2 Spec | **n/a** — nothing is built, so there is nothing to spec against. The Opportunity / Hypothesis artifact is the record. |
| G3 Design | **n/a** — nothing is being built. |
| G4 Build | **n/a** — no build. If build is needed, convert to Spike, MVP, or Experiment first. |
| G5 Verification | **n/a** — evidence needed is *named* here, not gathered. Gathering it is a Spike or an Experiment. |
| G6 Security | Required before using real user data, production data, third-party data, or external participants. |
| G7 Launch | **n/a** — nothing ships. |
| G8 Post-launch | Discovery decision only. Continue, kill, reframe, or create Spike/MVP/Experiment with linked source. |

## 2. Spike

Use when the goal is to reduce uncertainty, not ship product value.

```text
Artifact Type: Spike Requirement
ID: SPIKE-001
Question To Answer:
Uncertainty / Risk:
Scope Boundary:
Approach:
Timebox:
Inputs Needed:
Output Expected:
Decision Criteria:
Findings:
Recommendation:
Follow-up Requirements Created:
```

Required categories:

| Disposition | Categories |
|---|---|
| Required | `TECH` or `UX` or `DATA` or `SEC`, `TST`, `ANA` |
| Conditional | `INT`, `PRIV`, `CMP`, `OPS` |
| Usually n/a | `REL`, `SUP`, `DOC`, `POST` |

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. The question and uncertainty must be explicit. |
| G1 Disposition | Required. A spike inherits the project's disposition and may add to it; it may not drop a category the project marked `applies`. |
| G2 Spec | Required, but the spec is the spike plan, not a product spec. |
| G3 Design | Required — the design is *how the spike will answer its question*: the approach, and why that approach settles the uncertainty. Small, but not absent. |
| G4 Build | Prototype work may start only after timebox, scope boundary, and output are approved. Prototype code is not required to trace to product requirement IDs; it is required to stay inside the scope boundary. |
| G5 Verification | Required against the **decision criteria**, which are the spike's measurements. A spike that cannot say what result would answer its question has not been scoped. |
| G6 Security | Required before touching production data, credentials, external integrations, or deployable environments. |
| G7 Launch | **n/a** unless the prototype is deployed. If it is deployed, this stops being a spike. |
| G8 Post-launch | Findings required. Feasible, not feasible, feasible with constraints, or needs another spike. Product work cannot continue until findings are written. |

## 3. MVP

Use when the goal is the smallest coherent product that proves value.

```text
Artifact Type: MVP Requirement
ID: PRD-001 / FUN-001 / UX-001
User / Customer:
Problem Solved:
Requirement Statement:
MVP Scope:
Out of Scope:
Acceptance Criteria:
Must-Have Reason:
Dependency:
Test Case:
Launch Metric:
```

Required categories:

| Disposition | Categories |
|---|---|
| Required | `BUS`, `USR`, `PRD`, `FUN`, `UX`, `DATA`, `SEC`, `ANA`, `TST`, `REL` |
| Conditional | `TECH`, `INT`, `PRIV`, `CMP`, `OPS`, `SUP`, `DOC` |
| Usually n/a | `POST` until launch, then required for close-out |

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. |
| G1 Disposition | Required. |
| G2 Spec | Hard stop. MVP scope and out-of-scope must be approved before build. |
| G3 Design | Required for core flows, architecture, data, and integrations. |
| G4 Build | Requires every build item to trace to an approved requirement ID. |
| G5 Verification | Required for acceptance criteria and core regression tests. |
| G6 Security | Required before any production or external-user exposure. |
| G7 Launch | Required for rollout, monitoring, support, and rollback. |
| G8 Post-launch | Required after launch metric is collected. |

## 4. Pilot

Use for controlled real-world validation with a limited audience.

```text
Artifact Type: Pilot Requirement
ID: PILOT-001 or category ID like REL-001
Pilot Audience:
Pilot Scope:
Entry Criteria:
Exit Criteria:
Operational Constraints:
Support Plan:
Feedback Capture:
Success Metrics:
Failure Conditions:
Rollback Plan:
Decision After Pilot:
```

Required categories:

| Disposition | Categories |
|---|---|
| Required | `STA`, `USR`, `PRD`, `FUN`, `UX`, `DATA`, `SEC`, `ANA`, `OPS`, `SUP`, `REL`, `TST` |
| Conditional | `INT`, `PRIV`, `CMP`, `DOC` |
| Usually n/a | None if external users are involved |

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Pilot audience and success criteria must be named. |
| G1 Disposition | Required. |
| G2 Spec | Required. Pilot scope, entry criteria, and exit criteria must be approved. |
| G3 Design | Required for operational path, feedback path, and rollback. |
| G4 Build | Required where the pilot builds anything. A pilot of existing functionality traces to the requirement IDs it is exercising rather than to new ones. |
| G5 Verification | Required before the first pilot user. |
| G6 Security | Required before pilot users, production data, or partner systems are involved. |
| G7 Launch | Required, including support owner and rollback plan. |
| G8 Post-launch | Required. Decision must be scale, extend, fix and retry, or stop. |

## 5. Full Release

Use for broad availability or general availability.

```text
Artifact Type: Release Requirement
ID: REL-001
Release Scope:
Eligible Users / Markets:
Launch Criteria:
Feature Flags:
Migration Requirements:
Performance Requirements:
Support Readiness:
Documentation Required:
Monitoring / Alerts:
Rollback Plan:
Legal / Compliance Signoff:
Final Approval:
```

Required categories:

| Disposition | Categories |
|---|---|
| Required | `BUS`, `STA`, `USR`, `PRD`, `FUN`, `NFR`, `UX`, `TECH`, `DATA`, `SEC`, `PRIV`, `ANA`, `OPS`, `SUP`, `TST`, `REL`, `DOC`, `POST` |
| Conditional | `INT`, `CMP` |
| Usually n/a | None without a written reason |

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. |
| G1 Disposition | Required. |
| G2 Spec | Required. No build without approved full-release scope. |
| G3 Design | Required for architecture, operations, data, security, and user experience. |
| G4 Build | Requires traceability from every shipped change to requirement IDs. |
| G5 Verification | Required, including regression, performance where applicable, and acceptance evidence. |
| G6 Security | Hard stop. No production release without security and privacy review. |
| G7 Launch | Required, including support, monitoring, rollback, documentation, and final approval. |
| G8 Post-launch | Required. Adoption, incidents, support load, and launch metrics are recorded. |

## 6. Maintenance Release

Use for planned fixes, compatibility updates, stability improvements, and small
enhancements.

```text
Artifact Type: Maintenance Requirement
ID: MAINT-001 or BUG-001 / TECH-001
Issue / Change:
Reason:
Affected Area:
User Impact:
Risk Level:
Compatibility Impact:
Regression Tests:
Acceptance Criteria:
Deployment Notes:
Rollback Notes:
Evidence:
```

Required categories:

| Disposition | Categories |
|---|---|
| Required | `PRD`, `FUN` or `TECH`, `TST`, `REL` |
| Conditional | `NFR`, `DATA`, `SEC`, `PRIV`, `OPS`, `SUP`, `DOC`, `ANA` |
| Usually n/a | `BUS`, `STA`, `POST` unless release goals or post-launch metrics change |

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Affected area and reason must be explicit. |
| G1 Disposition | Inherited from the project. A maintenance release does not re-declare the disposition; it may add a category the change newly touches. |
| G2 Spec | Required. Even small changes need an approved change statement. |
| G3 Design | Required when architecture, data, security, UX, or integrations change. Otherwise **n/a by exception, stated in the change statement** — not by silence. |
| G4 Build | Required. Every change traces to the requirement or defect ID it serves. |
| G5 Verification | Required, focused on regression and affected behavior. |
| G6 Security | Required for any security-sensitive, privacy-sensitive, auth, data, dependency, integration, or infrastructure change. |
| G7 Launch | Required when deployed to production. Rollback notes are mandatory. |
| G8 Post-launch | Required when the release was intended to move a metric or fix a production issue. |

## 7. Security Review

Use when reviewing a product, design, release, dependency, vendor, integration,
or implementation for security risk.

```text
Artifact Type: Security Finding / Requirement
ID: SEC-001
Asset / Area:
Threat / Risk:
Severity:
Exploit Scenario:
Control Required:
Current State:
Required State:
Remediation:
Owner:
Verification Method:
Evidence:
Residual Risk:
Approval:
```

Required categories:

| Disposition | Categories |
|---|---|
| Required | `SEC`, `DATA`, `TST` |
| Conditional | `PRIV`, `CMP`, `INT`, `TECH`, `OPS`, `DOC`, `REL` |
| Usually n/a | `UX`, `SUP`, `POST` unless user-facing controls, support handling, or post-launch monitoring are in scope |

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Scope, assets, and review trigger must be named. |
| G1 Disposition | Required for the review's own scope — which categories the review covers. It does not alter the reviewed project's disposition. |
| G2 Spec | Required. The review cannot start until scope and assets are approved. |
| G3 Design | Required when a remediation changes system behaviour, data flow, access, or operations. A finding that needs no code change needs no design. |
| G4 Build | Remediation work cannot start without approved SEC requirement IDs. |
| G5 Verification | Required for every remediation or control. |
| G6 Security | **The primary gate.** Findings must be accepted, remediated, or risk-accepted according to policy. |
| G7 Launch | No production exposure until blocking findings are closed or formally accepted. |
| G8 Post-launch | Residual risk, evidence, and approval are recorded. |

## Additional project types worth adding

The seven types above are enough for a first system. These additional types are
worth separating because their gates behave differently.

## 8. Experiment / A-B Test

Use when the goal is to measure a product, UX, pricing, onboarding, or growth
hypothesis.

```text
Artifact Type: Experiment Requirement
ID: ANA-001
Hypothesis:
Population:
Variant:
Control:
Success Metric:
Guardrail Metrics:
Sample / Duration:
Instrumentation:
Decision Rule:
Rollback / Stop Condition:
```

Required categories: `BUS`, `USR`, `ANA`, `PRD`, `TST`, `REL`.

Conditional categories: `UX`, `DATA`, `SEC`, `PRIV`, `CMP`, `OPS`, `SUP`,
`DOC`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Owner and the decision the experiment informs must be named. |
| G1 Disposition | Inherited from the project; `ANA` must be `applies` or the experiment cannot be measured. |
| G2 Spec | Required. Hypothesis, metric, population, and decision rule must be approved before build. |
| G3 Design | Required for instrumentation and assignment — how users are split, how events are recorded, and why that measures the hypothesis. |
| G4 Build | Required. Variant and instrumentation trace to the experiment's requirement IDs. |
| G5 Verification | Required. Instrumentation is validated before the experiment runs; an experiment measured by broken telemetry produces a confident wrong answer. |
| G6 Security | Required before using personal data, sensitive segmentation, production traffic, or external users. |
| G7 Launch | Required with stop conditions and monitoring. |
| G8 Post-launch | Required. Result must be ship, iterate, stop, or inconclusive with reason. |

## 9. Hotfix / Emergency Patch

Use when a narrow urgent fix must move faster than normal release cadence.

```text
Artifact Type: Hotfix Requirement
ID: REL-001 or BUG-001
Incident / Trigger:
Impact:
Urgency:
Minimal Fix:
Risk:
Tests Run:
Approver:
Deployment Window:
Rollback:
Post-Fix Follow-up:
```

Required categories: `FUN` or `TECH`, `TST`, `REL`, `OPS`.

Conditional categories: `SEC`, `PRIV`, `DATA`, `SUP`, `DOC`, `ANA`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required, even if brief. Incident, impact, and owner must be named. |
| G1 Disposition | Inherited from the project. A hotfix never re-declares it — that is the one thing emergency pressure would corrupt. |
| G2 Spec | The minimal approved fix statement. No broad cleanup under a hotfix. |
| G3 Design | **n/a for the minimal fix**, by design — that is what makes it a hotfix. If the fix needs a design, it is not a hotfix; the emergency measure is a mitigation and the real fix follows as a Maintenance Release. |
| G4 Build | Required. The change traces to the incident or defect ID. |
| G5 Verification | Required with the fastest credible regression evidence. |
| G6 Security | Required for security, auth, dependency, data, privacy, integration, or infrastructure hotfixes. |
| G7 Launch | Required with rollback and monitor owner. |
| G8 Post-launch | Required. A normal follow-up ticket captures anything skipped under emergency constraints. |

## 10. Migration / Cutover

Use for data migrations, platform migrations, vendor transitions, domain moves,
identity migrations, and operational cutovers.

```text
Artifact Type: Migration Requirement
ID: DATA-001 / TECH-001 / REL-001
Source State:
Target State:
Migration Scope:
Mapping / Transformation:
Cutover Plan:
Backout Plan:
Data Validation:
Downtime / Degradation:
Owner:
Communications:
```

Required categories: `DATA`, `TECH`, `OPS`, `TST`, `REL`, `SEC`.

Conditional categories: `PRIV`, `CMP`, `INT`, `SUP`, `DOC`, `ANA`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Source, target, and the owner accountable for the cutover must be named. |
| G1 Disposition | Required. `DATA` and `SEC` cannot be `n/a` for a migration. |
| G2 Spec | Required. Source, target, mapping, and backout must be approved before build. |
| G3 Design | Required for the mapping and transformation, the cutover sequence, and the backout path. |
| G4 Build | Required. Migration scripts and transformations trace to the mapping they implement. |
| G5 Verification | Required on rehearsal or sampled validation before production cutover — the dry run. |
| G6 Security | Required before moving production data, credentials, identity, or access controls. |
| G7 Launch | Required with communication, monitoring, and rollback owner. |
| G8 Post-launch | Required with validation evidence and incident record if anything failed. |

## 11. Platform / Infrastructure Change

Use for hosting, networking, CI/CD, observability, scaling, reliability,
runtime, database, or shared service changes.

```text
Artifact Type: Platform Requirement
ID: TECH-001 / OPS-001 / NFR-001
System / Service:
Current State:
Required State:
Reliability Target:
Operational Impact:
Access / Secrets Impact:
Migration Plan:
Monitoring:
Rollback:
Evidence:
```

Required categories: `TECH`, `NFR`, `OPS`, `SEC`, `TST`, `REL`.

Conditional categories: `DATA`, `PRIV`, `CMP`, `INT`, `SUP`, `DOC`, `ANA`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. System, current state, and the operational owner must be named. |
| G1 Disposition | Required. `NFR`, `OPS` and `SEC` cannot be `n/a` for a platform change. |
| G2 Spec | Required. Required state, blast radius, and rollback must be approved. |
| G3 Design | Required for architecture, access, reliability, and operational model. |
| G4 Build | Required. Infrastructure-as-code and configuration changes trace to the requirement IDs they serve. |
| G5 Verification | Required through staging, canary, load test, or equivalent evidence. |
| G6 Security | Required before production infrastructure or secrets are changed. |
| G7 Launch | Required with monitoring, alerting, and incident owner. |
| G8 Post-launch | Required for reliability, incident, and performance evidence. |

## 12. Compliance / Regulatory Release

Use when a legal, regulatory, audit, certification, accessibility, retention, or
records obligation is the driver.

```text
Artifact Type: Compliance Requirement
ID: CMP-001
Obligation:
Jurisdiction / Standard:
Required Control:
Evidence Required:
Owner:
Deadline:
Affected Users / Systems:
Verification:
Approver:
Retention:
```

Required categories: `CMP`, `PRIV` or `SEC` or `DATA`, `TST`, `DOC`, `REL`.

Conditional categories: `FUN`, `UX`, `TECH`, `OPS`, `SUP`, `ANA`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Obligation, jurisdiction, deadline, and accountable approver must be named. |
| G1 Disposition | Required. `CMP` and `DOC` cannot be `n/a` for a compliance release. |
| G2 Spec | Required. Obligation, control, evidence, and approver must be approved before build. |
| G3 Design | Required when controls affect system behavior, data, UX, or operations. |
| G4 Build | Required. Every control traces to the `CMP` requirement it satisfies — this trace *is* the audit evidence, not a by-product of it. |
| G5 Verification | Required with audit-ready evidence. |
| G6 Security | Required when the obligation touches data, privacy, access, retention, or security controls. |
| G7 Launch | Required with documentation and support readiness where users are affected. |
| G8 Post-launch | Required with evidence retained in the declared location. |

## 13. Beta / Limited Availability

Use when the product is broader than a pilot but not yet general availability.

```text
Artifact Type: Beta Requirement
ID: REL-001
Audience:
Eligibility:
Known Limitations:
Feedback Path:
Support Model:
Success Metrics:
Exit Criteria:
Rollback / Removal:
GA Decision:
```

Required categories: `USR`, `PRD`, `FUN`, `UX`, `SEC`, `ANA`, `OPS`, `SUP`,
`TST`, `REL`, `DOC`.

Conditional categories: `DATA`, `PRIV`, `CMP`, `INT`, `POST`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Audience, eligibility, and the GA decision this beta informs must be named. |
| G1 Disposition | Required. |
| G2 Spec | Required. Audience, limitations, feedback path, and exit criteria must be approved. |
| G3 Design | Required for the feedback path, eligibility/gating mechanism, and removal path. |
| G4 Build | Required. Beta-gated functionality traces to requirement IDs, including the flag or entitlement that scopes it. |
| G5 Verification | Required before the first beta user. |
| G6 Security | Required before any external user or production data. |
| G7 Launch | Required with support and rollback. |
| G8 Post-launch | Required. Decision must be GA, extend beta, fix and retry, or stop. |

## 14. Decommission / Sunsetting

Use when removing a feature, product, integration, endpoint, data store, or
operational dependency.

```text
Artifact Type: Decommission Requirement
ID: REL-001 / DATA-001 / TECH-001
Thing Being Removed:
Reason:
Users / Systems Affected:
Replacement / Migration:
Notice Plan:
Data Retention / Deletion:
Shutdown Steps:
Rollback / Restore:
Support Plan:
Completion Evidence:
```

Required categories: `PRD`, `DATA`, `TECH`, `OPS`, `SUP`, `REL`, `DOC`.

Conditional categories: `SEC`, `PRIV`, `CMP`, `INT`, `ANA`, `TST`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. The thing being removed, the reason, and who is affected must be named. |
| G1 Disposition | Required. `DATA` cannot be `n/a` — removal always has a retention-or-deletion answer, including "none held". |
| G2 Spec | Required. Removal scope, affected users, and replacement path must be approved. |
| G3 Design | Required when data, integrations, access, or operational dependencies change. |
| G4 Build | Required. Shutdown steps trace to the requirements being retired — and the retired requirement IDs move to `superseded` or `dropped` rather than vanishing. |
| G5 Verification | Required for removal checks and regression of dependent systems. |
| G6 Security | Required when access, data retention, deletion, privacy, or compliance is affected. |
| G7 Launch | Required with communication and rollback/restore plan. |
| G8 Post-launch | Required with completion evidence and support signal. |

## 15. Internal Tooling

Use for admin tools, support tooling, developer tooling, operational consoles,
scripts, and internal workflows.

```text
Artifact Type: Internal Tool Requirement
ID: OPS-001 / TECH-001 / FUN-001
Internal User:
Workflow:
Permission Model:
Inputs:
Outputs:
Audit / Logging:
Failure Mode:
Support / Ownership:
Verification:
```

Required categories: `USR`, `FUN`, `TECH`, `SEC`, `OPS`, `TST`, `DOC`.

Conditional categories: `DATA`, `PRIV`, `CMP`, `ANA`, `REL`, `SUP`.

Gates:

| Gate | Rule |
|---|---|
| G0 Intake | Required. Internal user, workflow, and owning team must be named. |
| G1 Disposition | Required. `SEC` cannot be `n/a` — an internal tool with production access is a privileged surface, and "internal" is not a security boundary. |
| G2 Spec | Required. Workflow, owner, permission model, and failure mode must be approved. |
| G3 Design | Required for access, data, audit logging, and operational model. |
| G4 Build | Required. The tool's behaviour traces to the workflow requirements it automates. |
| G5 Verification | Required before internal rollout. |
| G6 Security | Required before touching production systems, customer data, secrets, admin access, or privileged operations. |
| G7 Launch | Required if the tool is relied on operationally. |
| G8 Post-launch | Required when the tool is tied to efficiency, quality, or incident goals. |

## Minimum floors by project type

| Project Type | Spec approved before build | Security before prod/user/data exposure | Launch readiness | Post-launch close-out |
|---|---|---|---|---|
| Ideation / Exploring | No build allowed | Conditional | n/a | Discovery decision only |
| Spike | Required for prototype | Conditional | n/a unless deployed | Findings required |
| MVP | Required | Required | Required | Required |
| Pilot | Required | Required | Required | Required |
| Full Release | Required | Required | Required | Required |
| Maintenance Release | Required | Conditional, required for sensitive changes | Required if deployed | Conditional |
| Security Review | Required scope | Primary gate | Required if release-blocking | Residual risk required |
| Experiment / A-B Test | Required | Required for production traffic/data | Required | Required |
| Hotfix / Emergency Patch | Required minimal fix | Required for sensitive changes | Required | Required follow-up |
| Migration / Cutover | Required | Required | Required | Required |
| Platform / Infrastructure Change | Required | Required | Required | Required |
| Compliance / Regulatory Release | Required | Required when obligation touches data/access/privacy/security | Required | Required evidence retention |
| Beta / Limited Availability | Required | Required | Required | Required |
| Decommission / Sunsetting | Required | Required when data/access/privacy/compliance is affected | Required | Required |
| Internal Tooling | Required | Required for production systems/data/secrets/admin | Conditional | Conditional |
