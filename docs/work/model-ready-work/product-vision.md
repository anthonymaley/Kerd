# Product vision and working hypotheses

This document separates the person's intended outcomes from the mechanisms we
currently believe will produce them. Recording a direction does not make every
proposed mechanism correct. Trials may revise or reject the mechanisms while
preserving the underlying intent.

## Decision status

### Desired outcomes from the producer

- Models receive work in a form that gives them a strong chance of success.
- Clear instructions prevent drift and silent assumptions.
- People face few avoidable turns and questions.
- People do not have to review long internal documents to understand or approve
  ordinary work.
- People can see what is being built, where it stands, what is happening now,
  and what needs them.
- Features stay connected to the product vision and plan.
- Cross-model work, loops, and goals are used where they improve results.
- Speed and efficiency do not come at the expense of quality.

These outcomes can conflict. Fewer questions can increase assumptions; faster
execution can reduce review; more cross-model work can increase cost and delay.
The design must expose and test those trade-offs rather than pretending all
outcomes can always be maximized together.

## Interaction principles

### Guided interview, not a questionnaire

Conductor learns what it needs through a short, adaptive interview. It begins
with the person's description, reflects back its understanding, and asks the
next smallest group of questions that materially reduces uncertainty.

Questions are ordered by information value:

1. What outcome is wanted and for whom?
2. What observable result would count as success?
3. What must not happen or change?
4. Which consequential choices belong to the person?
5. What missing fact would change the slice, model, or safety level?

Conductor fills what repository evidence can answer, proposes reversible
defaults, and labels every remaining assumption. It stops interviewing when
another question would not materially improve readiness. The full schema is
never presented as a form the person must complete.

### Bounded freedom

The model receives a clear destination and boundaries without a prescribed
route. Structure grows with consequence and uncertainty. Required order appears
only when it is part of safety or correctness. Drift is detected against the
fixed brief, not by demanding obedience to a preferred sequence.

The target is enough information for good independent decisions, not enough
instructions to eliminate independent decisions.

### Jobs, not chats

Cross-model work uses bounded jobs with declared inputs, outputs, decision
rights, proof, and stopping conditions. Models do not hold open-ended debates
or create commentary for other models to extend.

A cross-model job may execute a fixed brief, independently review named
measures, investigate one uncertainty, or produce a competing solution against
the same measures. Conductor combines returned evidence and decides what enters
the product record. Agreement between models is never treated as proof.

### Speed comes from readiness

Faster execution comes from clearer outcomes, better context, fewer avoidable
interruptions, correctly sized models, parallel independent jobs, and stronger
proof. It must not come from weakening the work, skipping review, or accepting
incomplete results.

### Progressive disclosure

The project retains enough detail to build and verify correctly, while each
person sees only the depth needed for the current decision. The short view is
derived from the detailed records rather than becoming a second truth.

Every approval surface begins with what is being built, why it matters, where
it stands, what happens next, what decision is needed, and what will prove
success. The person can expand any part without being required to review all
parts.

### Current design hypotheses

- Three work levels may provide enough variation without making the process
  difficult to understand.
- Conversational intake plus a readiness check may reduce both ambiguity and
  avoidable questioning.
- A focused context pack may outperform a large common prompt.
- A derived visual work view may replace much documentation review.
- Model-specific preparation may improve results over one shared prompt.
- Failure classification may prevent retries from creating prompt bloat.

These are proposals to test, not user requirements to preserve at any cost.

### Safeguards

- Never silently change the person's intended outcome or decision ownership.
- Never invent proof or call an unmeasured result successful.
- Never trade away safety, truth, or explicit boundaries for speed.
- Never treat agreement between models as proof.
- Never promote a model-specific technique solely because an official guide
  recommends it; Kerd's results must support it.

### Open decisions

- Whether three work levels are enough in real use.
- When an assumption is safe enough to proceed without asking.
- What visual view is sufficient for ordinary approval.
- When a second model improves confidence enough to justify its cost.
- Which work classes genuinely benefit from separate planning.
- How much outcome improvement warrants additional time or tokens.

## What we are building

People across product, projects, operations, leadership, research, creative
work, and software define what they want in their own language. Conductor turns that intent
into clear, measurable work, chooses the right model and effort, and presents
the work in the form that gives that model the best chance of succeeding.

The model receives enough clarity to avoid drift and assumptions, but retains
freedom to choose the best method. The person sees where the work is, what is
happening now, what is being built, and what evidence supports the result.

The product promise is:

> Get to a proven result quickly, without purchasing speed through lower
> quality or purchasing quality through unnecessary ceremony.

The design is intended to be general-purpose. Current prototype evidence is
limited to repository and software-oriented work. General applicability remains
a hypothesis until trials cover non-software outcomes such as a product
proposal, operating plan, research synthesis, executive decision, and customer
communication.

## What the experience must prevent

### Sub-par generic prompts

Different models must not receive the same large compromise prompt. The stable
requirement remains common; its presentation, context, tools, examples, and
effort are prepared for the selected model family.

### Drift and silent assumptions

Conductor makes safe assumptions visible and asks for consequential decisions.
The approved work brief remains the fixed reference for execution and review.
No model-specific preparation may alter the outcome, measures, boundaries, or
decision ownership.

### Unnecessary turns and questions

Conductor retrieves answers already available in the repository, groups
material questions into one small batch, and proceeds on safe reversible
assumptions. It does not ask people to confirm implementation details the model
is authorized to decide.

### Documentation people will not review

The primary interface is a short readable brief, a visual work view, a
preparation preview, and an outcome report. Full specifications, generated
prompts, model guidance, and telemetry remain available for machinery and deep
inspection but are not required reading for ordinary use.

### An unclear sense of position

Every active build has one visual work view showing:

- The product outcome
- Features and dependencies
- The selected slice
- What is happening now
- What is ready, active, blocked, proven, and accepted
- The next decision or action
- Progress toward feature, integrated, and product outcomes

The view is derived from the underlying records. It cannot independently claim
that work is further along than the machine-derived state.

### Drift from the product vision

Every feature links to its parent build outcome. Every execution brief carries
the relevant parent boundaries and states how its result advances the feature
and product outcome. Review checks local success, integration, and product
value rather than stopping at completed tasks.

### Quality lost in pursuit of speed

Fast means fewer avoidable turns, smaller relevant context, cheaper proven
models, parallel independent work, and mechanical verification. It never means
weaker success measures, missing proof, silent scope changes, or skipped review
for consequential work.

## Proposed three work levels

The three-level structure is the current starting hypothesis. A trial must show
that people classify work consistently and that adjacent levels produce
meaningfully different handling. Otherwise the levels should be simplified or
changed. A level controls preparation, approval, review, and recovery; it does
not change the requirement's truth.

### Quick

Use for narrow, reversible work with clear proof.

```text
Person provides: outcome, deliverable, boundaries, done condition
Conductor: fills safe details, asks only if materially blocked
Execution: direct or fast model, low effort where proven
Review: mechanical checks
Approval: not required when already inside granted authority
```

Examples: correct a sourced statement, rename a local symbol, add a focused
test, or update one bounded configuration value.

### Standard

Use for ordinary features and meaningful changes with manageable consequences.

```text
Person approves: feature outcome, measures, proof, boundaries, decision rights
Conductor: selects a vertical slice, focused context, model and effort
Execution: balanced or capable model with method freedom
Review: machinery plus an independent check where needed
Approval: required for product decisions, not implementation choices
```

Examples: add one complete user capability, repair a repository behavior, or
create a new internal tool with tests.

### Important / deep

Use when mistakes are difficult to reverse, consequences are high, ambiguity
is substantial, or the work requires deep investigation.

```text
Person approves: full brief, consequential decisions, recovery and release conditions
Conductor: uses deep model capability and effort justified by the task
Execution: may use planned loops, independent parallel investigation, or staged landing
Review: mechanical proof plus cold-eyes or producer review
Approval: required before irreversible or externally visible effects
```

Examples: security changes, data migrations, releases, foundational product
architecture, destructive operations, or ambiguous high-impact strategy.

Work may move between levels when evidence changes. The reason must be visible;
the system cannot silently add ceremony or lower safeguards.

## Cross-model advantage

The system should use multiple models where their differences create value:

- One model may execute while another independently reviews.
- Competing approaches may be compared on an important decision.
- Independent investigations may run in parallel against the same fixed brief.
- A fast model may handle bounded mechanical work while a deep model handles
  judgment.
- Results across model families improve future selection and guidance.

Multiple models must share the same outcome measures. Agreement is not proof;
evidence remains the judge. More models are used only when they improve quality,
time, cost, or confidence on a declared measure.

## Proposed user-facing work view

The default view answers five questions without opening repository files:

```text
WHAT ARE WE BUILDING?
Team invitations: owners can bring colleagues into the correct account.

WHERE ARE WE?
Standard feature · Slice 2 of 4 · Working

WHAT IS HAPPENING NOW?
Adding email delivery for the invitation link.

WHAT HAS BEEN PROVEN?
✓ Invitation creation
✓ Correct account ownership
○ Email delivery — active
○ Acceptance and membership — waiting

WHAT NEEDS ME?
No decision right now. Next review after delivery proof passes.
```

The working hypothesis is that diagrams can become first-class product
surfaces. They should use product language,
show real derived state, reveal dependencies and change over time, and make the
next action obvious. They should not require knowledge of prompt compilation,
model adapters, manifests, schemas, or evaluation terminology.

### Visual depth levels

- **Level 1 — Product:** outcome, user value, major capabilities, current
  slice, progress, blockers, and next decision.
- **Level 2 — Flow:** user journey, main states and decisions, inputs, outputs,
  failure paths, and dependencies.
- **Level 3 — Architecture:** components, ownership, data and control movement,
  external systems, trust boundaries, deterministic checks, and model work.
- **Level 4 — Detail:** sequences, state transitions, interfaces, record shapes,
  recovery, concurrency, edge cases, tests, and proof.

The person chooses the depth needed for the current decision. Important/Deep
work may require deeper views to exist for execution even when the producer
approves from a higher-level view. Conductor must surface every consequential
fact from hidden detail in the approval view; progressive disclosure may not
conceal a material loss.

### Text depth levels

- **At a glance:** outcome, position, active work, proof state, next decision.
- **Approval brief:** measures, boundaries, trade-offs, requested decision.
- **Build detail:** dependencies, context, interfaces, verification.
- **Evidence detail:** traces, generated prompts, telemetry, and edge cases.

Each level stays concise and links downward. Detailed records provide rigor
without making every person read a book before approving ordinary work.

## Definition of success for the hypothesis

The product works when a person can:

1. Describe what they want in ordinary language.
2. Reach a clear approved brief with few or no avoidable questions.
3. Understand the product, feature, current slice, and live state visually.
4. Let the selected model choose its method without losing the requirement.
5. Receive a fast result with proof mapped to measurable outcomes.
6. Use different models and loops when they improve the declared result.
7. Understand what happened and what comes next without reviewing long internal
   documents.
