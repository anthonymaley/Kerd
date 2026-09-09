# End-to-end Standard example

This example tests the complete proposed experience with a non-software product
job. It is illustrative; the interview and runner are not implemented yet.

## 1. Person's opening request

> We keep losing customers between agreeing to buy and actually getting value.
> Create a better onboarding plan we can start next month.

## 2. Conductor reflects its understanding

```text
You want a practical customer-onboarding plan that reduces the delay between a
customer agreeing to buy and reaching their first useful outcome. You want to
begin next month.

I can retrieve the current onboarding steps and customer feedback. I should not
assume which customer group matters most, what “first value” means, or what
improvement is worth targeting.
```

## 3. Guided interview

Conductor retrieves existing process documents, recent onboarding durations,
customer complaints, and team ownership before asking.

It asks one related group:

1. Which customer group should the first version serve?
2. What event means that group has received its first useful value?
3. What improvement would make the first month successful?

It deliberately does not ask:

- Which document format to use—the model may decide.
- Which interview-analysis method to use—the model may decide.
- Who currently owns each step—the project records answer it.
- Whether to redesign billing—the request and evidence do not yet justify that
  expansion.

## 4. Person's answers

```text
Start with new mid-market customers. First value is when their first team
completes a real workflow, not the setup tutorial. Reducing the median from 18
days to 10 days would be meaningful. Do not change pricing or contracts.
```

## 5. Draft work brief

```yaml
level: Standard
outcome: >
  New mid-market customers complete their first real team workflow within a
  median of 10 days after agreeing to buy.
deliverables:
  - A staged onboarding plan that can begin next month.
  - Owners, dependencies, measures, and the first four-week learning plan.
success:
  - The plan addresses the observed causes of the current 18-day median.
  - Every action has an owner and observable completion condition.
  - The plan can begin next month with current staffing or names the gap.
  - Measurement distinguishes setup completion from a real workflow.
proof:
  - Current-state evidence linked to each proposed change.
  - Dependency and owner confirmation.
  - Measurement definition and reporting example.
boundaries:
  - Do not change pricing or contracts.
  - Do not promise a 10-day result before the trial measures it.
person_decides:
  - Customer experience trade-offs and additional staffing.
model_may_decide:
  - Analysis method, plan structure, and presentation.
done_when:
  - Every success row has resolving evidence or a named blocker.
```

Origins remain visible: the customer group, first-value definition, target, and
boundaries are person-provided; current duration and causes are evidence-derived;
the staged plan is Conductor-proposed; plan structure belongs to the executor.

## 6. Ready-to-run verdict

```text
READY — STANDARD

Outcome: measurable
Proof: available
Boundaries: clear
Decision ownership: clear
Dependencies: current records available
Consequential assumptions: 0

Why Standard: this changes a cross-team operating process but is reversible,
measured as a trial, and has no destructive or externally binding action.
```

## 7. Preparation preview

```text
You asked for
  A customer-onboarding plan that can reduce first real value from 18 to 10 days.

Conductor selected
  Capable model · medium effort · independent evidence review

The model will receive
  Approved brief · current journey · timing data · customer evidence · team ownership

The model may decide
  Analysis method, plan structure, and presentation.

It must return to you if
  The proposal needs pricing, contract, or staffing changes.
```

## 8. Bounded model jobs

Executor job: produce the plan and map every recommendation to evidence and a
success row.

Reviewer job: independently test whether the causes, dependencies, measures,
and claimed feasibility are supported. The reviewer does not see the executor's
persuasive explanation beyond the deliverable and evidence.

## 9. Example outcome report

```text
RESULT: READY FOR A FOUR-WEEK TRIAL

✓ Four observed delay causes are addressed.
✓ Every action has an owner and completion condition.
✓ The trial can begin next month with current staffing.
✓ First value is measured as a real team workflow.

What will change
- Sales hands off a completed outcome statement rather than account notes.
- One onboarding owner remains with the customer through first value.
- Setup and workflow milestones are measured separately.

What is not yet proven
- The changes will produce a 10-day median. The trial exists to measure that.

Needs your decision
- Whether the onboarding owner may pause low-readiness accounts rather than
  starting the clock immediately.

Next
- Approve that policy decision, then begin the four-week trial.
```

## 10. Visual position after the job

```text
Customer onboarding · Standard · Plan proven · Product outcome not yet proven

✓ Current causes understood
✓ Trial plan ready
○ Four-week trial — waiting on one decision
○ 10-day outcome — unmeasured

Needs you: decide when the measurement clock starts.
```

This example demonstrates the essential distinction: completing the requested
plan does not prove the customer outcome. The visual view must show both.

