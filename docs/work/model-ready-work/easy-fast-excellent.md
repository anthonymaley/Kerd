# Making model-ready work easy, fast, and excellent

This is the working product experience to validate. A person should be able to describe a
desired result in ordinary language, approve a clear brief, and receive proven
work without learning prompt engineering or supervising the model's method.

It is an adopted direction for a trial, not a claim that every mechanism below
is already correct. The person owns intended outcomes and consequential
decisions. Conductor must challenge contradictions, infeasible expectations,
hidden costs, and mechanisms that constrain models without evidence. Each
mechanism graduates only when the trial supports it.

The minimum useful journey has seven connected capabilities:

```text
Conversational intake
        |
        v
Ready-to-run check
        |
        v
Feature or slice selection
        |
        v
Model and effort choice
        |
        v
Focused context + prepared brief
        |
        v
Execution + coverage check
        |
        v
Plain-language outcome report
```

## 1. Conversational intake

People begin with the need in their own words. Conductor drafts the structured
brief and asks only questions whose answers could materially change the work.

```text
Person: Add team invitations so account owners can invite colleagues.

Conductor drafts what is already clear, then asks:
- Who is allowed to invite someone?
- Is sending the email part of this first slice?
- What should happen when the email already belongs to an account?
- What observable result will prove the invitation works?
```

Conductor must:

- Infer ordinary, reversible details when safe.
- Show every assumption visibly.
- Ask consequential questions in one small batch.
- Explain why a difficult question changes the result.
- Offer examples when a field is hard to answer.
- Refuse only when the missing answer would materially change the work.
- Ask the person to approve the finished brief, not its internal schema.
- Label each material statement as person-provided, evidence-derived, assumed,
  or proposed where its origin would affect a later decision.
- Challenge a requested requirement when it conflicts with another outcome,
  creates an unacknowledged loss, cannot be verified, or prescribes a method
  without showing why the method is necessary.

## 2. Ready-to-run check

Before model selection, Conductor gives a short readiness verdict.

```text
READY

Outcome: clear
Deliverable: clear
Success measures: 3 observable results
Proof: available
Boundaries: clear
Decision ownership: clear
Dependencies: satisfied
Open questions: 1 safe assumption
```

Or:

```text
NOT READY

“Improve onboarding” does not define what improvement means. Choose an
observable result before execution.
```

The readiness check prevents expensive execution from becoming requirements
discovery. It must name the smallest missing input and help the person supply
it.

## 3. Success-measure assistance

Conductor helps people move from activity to outcome:

| Kind | Example |
|---|---|
| Activity | Create an invitation screen. |
| Output | An invitation screen exists. |
| Outcome | An owner can successfully invite a teammate. |
| Proof | The invitation is recorded, delivered, accepted, and creates membership in a test. |

For each measure, Conductor proposes:

```yaml
result: Invited users can join the correct account.
target: Every acceptance fixture passes.
proof: Invitation acceptance test and resulting membership record.
reviewer: Automated check followed by product review.
```

The person approves measures before results exist. Conductor may suggest but
must never backfill or weaken a target after seeing an output.

### Interview rhythm

```text
Hear the need
    -> reflect current understanding
    -> retrieve what the project already knows
    -> identify the highest-value uncertainty
    -> ask one small related question group
    -> update the brief and visible assumptions
    -> stop when ready, or repeat
```

Conductor does not optimize for the fewest questions in isolation. It optimizes
for the fewest **avoidable** questions while keeping consequential assumptions
at zero. A question is avoidable when the repository already answers it, it
concerns a decision delegated to the model, or its answer would not change the
work, safety, proof, or level.

## 4. Three work levels

Conductor chooses the smallest form that safely fits.

### Quick

For narrow, reversible, mechanically checked work:

- Outcome
- Deliverable
- Done condition
- Boundaries

### Standard

For normal product work:

- Full work brief
- Success measures and proof
- Dependencies
- Decision rights

### Important / deep

For security, deletion, live migrations, releases, or irreversible effects:

- Full work brief
- Required ordering where order is part of safety
- Recovery plan
- Independent verification
- Explicit producer approvals

The work level is determined by consequence, uncertainty, reversibility, and
proof needs—not prestige or the length of the desired output. The complete
experience contract for each level is in [Product vision](product-vision.md).

## 5. Feature slicing assistance

Conductor proposes slices that produce observable value, cross only the layers
needed for that value, can be tested independently, reduce uncertainty, and
leave the product coherent.

```text
Team invitations

Slice 1: Owner creates an invitation and receives a shareable link.
Slice 2: Email delivery sends that link.
Slice 3: Invited user accepts and joins the account.
Slice 4: Owner views, revokes, and resends invitations.
```

Conductor explains why it proposed the split. The producer may combine,
reorder, or replace slices before the measures are fixed.

## 6. Focused context

Conductor assembles a context pack containing:

- Selected feature brief
- Relevant product boundaries
- Direct dependency results
- Applicable repository instructions
- Likely relevant files and decisions
- Available tools and known failures
- Explicit exclusions

It divides context into:

- **Required now**
- **Retrieve if needed**
- **Do not load unless the task changes**

Each important item records its source, version or fingerprint, reason for
inclusion, selection time, and invalidation condition. Changed requirements,
dependencies, or source files make the pack stale and force a refresh before
execution.

## 7. Model and effort selection

The initial operating table is:

| Work shape | Starting model type | Starting effort |
|---|---|---|
| Small, reversible, mechanically checked | Fast | Low |
| Standard implementation with good tests | Balanced | Medium |
| Ambiguous product judgment | Capable | High |
| Risky migration or deep diagnosis | Deep | High or xhigh |
| Large repetitive transformation | Fast with strict fixtures | Medium |
| Visual or document-quality work | Modality-capable | Determined by evaluation |

Start with the least costly pair already proven for that work class. Escalate
only when evidence shows that:

- An important ambiguity remains unresolved.
- Two attempts fail for materially different reasons.
- Required proof remains incomplete.
- The task has expanded beyond the pair's evaluated range.

A model saying that work is difficult is not itself evidence for escalation.

## 8. Preparation preview

Before execution, Conductor shows a human-readable preview:

```text
You asked for
  Add team invitations.

Conductor selected
  Claude Sonnet type · medium effort

Because
  Standard feature, moderate repository work, strong automated checks.

The model will receive
  Feature brief · 7 relevant files · 2 decisions · 4 success measures

The model may decide
  Internal implementation and test structure.

It must stop for you if
  The public invitation lifecycle or email provider must change.
```

The exact generated prompt remains inspectable, but it is not the primary
product interface.

## 9. Execution contract

The prepared brief tells the executor to:

- Start acting once the work is ready.
- Choose the most effective method.
- Inspect before changing.
- Stay within granted decision rights.
- Verify in proportion to consequence.
- Return proof mapped to success measures.
- Stop only on completion or a demonstrated blocker.
- Report unexpected findings without silently expanding scope.

This grants freedom over method without granting freedom over truth, safety,
scope, decision ownership, or completion.

### Cross-model jobs

When more than one model is useful, Conductor issues separate jobs rather than
starting a model conversation. Each job receives fixed measures and a narrow
responsibility. Conductor merges the returned evidence; speculative discussion
does not automatically enter product documentation.

Use cross-model jobs only when they improve a declared dimension such as
correctness, coverage, speed, cost, or confidence. More models are not evidence
of more rigor.

## Visual and written depth

The ordinary user approves from an at-a-glance product view or concise approval
brief. Flow, architecture, sequence, interface, and evidence views remain
available when the decision or work level needs them. They derive from one
underlying record and cannot disagree about position or success.

The visual and text depth contracts are defined in
[Product vision](product-vision.md). The process compensates for detail the user
does not read with deterministic checks, targeted review, and proof underneath.
It must still surface any consequential trade-off or loss before approval.

## 10. Recovery and retry

Before retrying, Conductor classifies the failure:

| Failure | What changes next |
|---|---|
| Requirement | Repair the brief or measures. |
| Context | Add, remove, or refresh information. |
| Selection | Change model or effort. |
| Execution | Retry with the same contract and a targeted correction. |
| Proof | Request or produce the missing evidence. |
| Product | Revisit the feature outcome or slice. |

Only the failing layer changes. A weak run must not automatically produce a
longer universal prompt.

## 11. Review proportional to consequence

| Consequence | Review |
|---|---|
| Routine and reversible | Mechanical checks |
| Consequential correctness | Independent model review plus machinery |
| Product judgment | Cold-eyes human review |
| Irreversible or externally visible | Producer approval |

The reviewer receives the original measures, deliverable, proof, and relevant
boundaries. The executor's persuasive narrative is excluded unless the review
requires it.

## 12. Plain-language outcome report

Every run ends with a report designed for the person who requested the work:

```text
RESULT: PARTIALLY MET

✓ Owners can create an invitation.
✓ Invitation records contain the correct account.
✓ Existing users are handled safely.
✗ Email delivery was not tested because credentials were unavailable.

Changed
- Invitation service
- Owner settings screen
- Four tests

Decisions made
- Invitations expire after seven days.

Needs your decision
- Whether account administrators may also invite users.

Recommended next step
- Supply a test email provider and rerun measure S4.
```

Tokens, tool calls, and detailed traces remain available as diagnostics rather
than dominating the result.

## 13. Learning without prompt growth

Apply improvements in this order:

1. Fix machinery when machinery can prevent the failure.
2. Improve the brief template when intake was unclear.
3. Improve context selection when information was missing.
4. Adjust model or effort selection when capability was wrong.
5. Add model guidance only for a genuinely model-specific failure.
6. Add a universal instruction only as a last resort.

Every new instruction records the failure it addresses, applicable models and
tasks, supporting result, review date, and removal condition.

## 14. First real trial

Run three tasks end to end:

1. A quick documentation correction.
2. An ordinary feature slice.
3. A consequential repository diagnosis or migration.

Compare current Conductor, a neutral work brief, a Claude-ready brief, and an
OpenAI-ready brief. Measure outcome success, defects, proof completeness,
human questions, avoidable stops, time to useful result, tokens, cost, and
rework.

The first trial proves the journey and identifies friction. It does not build
automatic prompt optimization or claim a general model ranking.
