# Capturing requirements and multiple features

Model-ready work captures a product at two levels:

1. A **build brief** describes the overall outcome and why the features belong
   together.
2. A **feature brief** describes one independently testable capability.

A **feature map** connects them, records dependencies, and shows which feature
or coherent group of features is ready to enter the build loop.

Conductor must not turn a flat feature list into one enormous execution prompt.
It selects one ready feature, or one group that must be built and tested
together, and prepares a focused model-ready brief for that work.

```text
Product goal
    |
    v
Build brief
    |
    v
Feature map
    +-- Feature A
    +-- Feature B
    +-- Feature C
           |
           v
One ready feature or coherent slice
           |
           v
Model-ready execution brief
           |
           v
Feature proof -> integrated proof -> product proof
```

## Build brief

The build brief is the stable parent record. It is a product contract, not an
execution prompt.

```yaml
build:
  id: model-ready-work
  outcome: >
    People describe work once and obtain effective, measurable execution from
    different model families.
  users:
    - Product producer
    - Conductor
    - Model executor
    - Results reviewer
  overall_success:
    - The same requirement works across Claude and OpenAI.
    - Prepared briefs preserve every required obligation.
    - Results equal or beat the current process.
    - At least one meaningful efficiency measure improves.
  shared_boundaries:
    - Do not weaken repository safety rules.
    - Do not change success measures after a run begins.
    - Do not rewrite live Conductor until the trial passes.
  features:
    - work-brief-capture
    - conductor-assessment
    - model-guidance
    - coverage-check
    - execution
    - results-review
    - learning-loop
  release_condition:
    - Every required feature has passed its own measures.
    - The integrated journey has passed end to end.
```

Required build fields:

- Product outcome
- Intended users
- Overall success measures
- Shared boundaries
- Feature list
- Release condition

## Feature brief

Each feature brief must be understandable and measurable without carrying the
whole build plan.

```yaml
feature:
  id: coverage-check
  parent: model-ready-work
  outcome: >
    Prevent a prepared prompt from losing or changing anything required by the
    original work brief.
  user_value: >
    A person can trust that changing prompt style did not change the job.
  deliverables:
    - A coverage report for every prepared brief.
    - A refusal when a required part is missing or changed.
  success_measures:
    - id: S1
      result: Every required field is mapped.
      target: 100 percent
    - id: S2
      result: Deliberately dropped requirements are detected.
      target: Every test case refuses.
    - id: S3
      result: Valid model-specific wording is accepted.
      target: Every valid test case passes.
  proof:
    - Automated test results
    - Example coverage report
    - Demonstration of a refused prompt
  dependencies:
    requires: [work-brief-capture, model-guidance]
    enables: [execution, results-review]
  boundaries:
    - It may verify meaning but may not rewrite the requirement.
    - A failed check must stop execution.
  done_when:
    - S1 through S3 pass and the integrated flow uses the check.
```

Required feature fields:

- Parent build
- Feature outcome and user value
- Deliverables
- Success measures and proof
- Dependencies
- Boundaries and decision rights
- Done condition

## Feature map

The feature map is the operational view. It is derived from feature briefs
where possible; it must not become a second place to redefine their truth.

| Feature | Required? | Depends on | State | Proof needed |
|---|---:|---|---|---|
| Work-brief capture | Yes | — | Ready | Valid and invalid examples |
| Conductor assessment | Yes | Work brief | Proposed | Correct model and effort choices |
| Model guidance | Yes | Assessment | In the loop | Claude and OpenAI comparison |
| Coverage check | Yes | Work brief, guidance | Ready | Requirement-loss fixtures |
| Execution | Yes | Coverage check | Proposed | Completed representative tasks |
| Results review | Yes | Execution | Proposed | Independently scored outputs |
| Learning loop | Later | Results review | Proposed | Improvement across repeated runs |

Every feature has one state:

- **Proposed:** valuable, but not ready to build.
- **Ready:** outcome, measures, boundaries, and dependencies are clear.
- **In the loop:** currently being designed, built, or tested.
- **Blocked:** a named dependency or decision prevents progress.
- **Proven:** its own measures pass.
- **Integrated:** it works with the surrounding features.
- **Accepted:** the producer approves the evidence.

## What enters the build loop together

Conductor combines features only when they create one independently testable
outcome.

Combine them when:

- Neither produces useful value alone.
- They share one success measure.
- Testing either alone would be artificial.
- They must land together to avoid a broken intermediate state.

Separate them when:

- Each can be tested independently.
- They serve different users or outcomes.
- One is optional for the first useful release.
- One could block the others for a long time.
- They need substantially different models, tools, or reviewers.

For this proposal, work-brief capture and the coverage check form a useful
first slice: together they prove that one requirement can be prepared for a
model without being changed. The learning loop can follow after execution and
results review exist.

## How Conductor prepares a feature

The execution brief contains only:

- The selected feature's outcome and proof
- Relevant shared boundaries from the build brief
- Direct dependency evidence
- Context needed for this slice
- The integration point the feature must leave behind

```text
Build brief
  + selected feature brief
  + relevant shared boundaries
  + satisfied dependency evidence
  + necessary context
            |
            v
Model-ready execution brief
```

The entire feature catalogue and build history do not travel in every prompt.

## Three levels of success

1. **Feature result:** does the capability work by itself?
2. **Integrated result:** does it work with its direct dependencies?
3. **Product result:** does the complete journey create the promised outcome?

For the coverage-check example:

- Feature result: a missing obligation is detected.
- Integrated result: Conductor refuses execution when coverage fails.
- Product result: the same requirement produces successful Claude and OpenAI
  runs without the person rewriting it.

A build cannot be called successful merely because every feature has a local
pass. Its integrated and product results must also pass.

