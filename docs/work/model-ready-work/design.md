# Model-ready work — design

**Integration update:** the current Kerd mapping, ownership changes, compatibility
rules and build order are in [the lightweight-process proposal](kerd-conductor-rework.md)
and [its implementation spec](conductor-rework-spec.md). They supersede both the
standalone-first plan and the subsequent gate-extension plan. This document is
earlier supporting design. Its fingerprint, sealing, mandatory schema, readiness
engine and named work-level mechanisms are not current implementation requirements.

**Status: expanded working design, ready for independent critical review after
the review packet is complete. Three earlier views were approved before the
guided interview, multi-feature, visual-depth, and cross-model additions; those
approvals do not approve the current expanded design. No design GO record has
been written.**

This package designs Conductor as Kerd's **guided work process**. Conductor
understands, shapes, builds, reviews, proves, and completes repository-based
work. It preserves one model-neutral description of the work, selects models
and effort, uses only the guidance each job needs, and runs an autonomous loop
until the original measures pass or the approved direction can no longer be
honoured safely.

Product language leads throughout this design. “Work brief” is the thing a
person supplies. “Model guidance” is how Conductor adapts its presentation.
“Coverage check” is the proof that no requirement was lost. The implementation
may call these a task envelope, adapter, and preservation manifest.

The intended outcomes and current experience hypotheses are separated in
[Product vision](product-vision.md). Technical implementation choices are valid
only when measured results support them; a mechanism is not protected merely
because this design currently proposes it.

## Design laws

1. **One requirement, many prepared briefs.** The work brief is authoritative;
   model-ready prompts are replaceable presentations of it.
2. **Outcome before method.** Objective, deliverable, measurable success,
   evidence, guardrails, authority, and completion are stable. Method is left
   to the executor unless order is itself part of correctness.
3. **The simplest sufficient process.** Use appropriate verification and
   existing permissions; do not require CI, custom hooks, seals or a gate ladder
   to use Kerd. Add no enforcement machinery merely because a rule can be parsed.
4. **Specific and tested, not folklore.** Model guidance names the tested model
   family, version, effort range, official source, and evaluation evidence.
5. **Every clause pays rent.** A clause survives because it protects an
   unenforceable invariant or improves a measured result. Otherwise it leaves.
6. **Preparation never decides success.** The frozen brief and independent
   results review decide success; model guidance cannot edit the test it sits.
7. **Local for routine jobs, official at the source.** Conductor uses the
   checked-in guidance registry for ordinary execution. Missing or stale guidance
   triggers a distinct official-source refresh, not a search on every job.
   Every local rule points to its exact source and retrieval date.
8. **Conversation outside, structure inside.** People describe the need and
   approve a readable brief; Conductor owns schemas and provider syntax.
9. **Smallest safe path.** Brief size, context, model, effort, and review grow
   only when consequence, uncertainty, or measured results require it.
10. **Repair the failing layer.** A retry changes requirements, context,
    selection, execution, proof, or product framing according to the observed
    failure; it does not blindly enlarge the prompt.
11. **Visual truth is part of the product.** The default work view shows the
    product, feature, selected slice, current activity, proven outcomes, and
    next decision in product language derived from the underlying records.
12. **Speed has a quality floor.** Optimization may reduce turns, context,
    model cost, or elapsed time; it may not weaken measures, proof, boundaries,
    or required review.
13. **Challenge before encoding.** Conductor distinguishes a stated outcome
    from a proposed mechanism, tests requirements for contradiction, feasibility,
    unintended loss, and unnecessary constraint, and raises material problems
    before freezing the work brief.
14. **Attribution stays honest.** The record states whether a field came from
    the person, repository evidence, a safe assumption, or a Conductor proposal.
    Approval of a brief does not rewrite every proposal as the person's idea.
15. **Interview for information value.** Conductor asks the smallest adaptive
    set of questions that removes material uncertainty; question count alone is
    never optimized at the cost of silent assumptions.
16. **Jobs, not chats.** Multiple models receive bounded responsibilities and
    shared measures. Conductor merges evidence; models do not debate indefinitely
    or author speculative documentation for one another.
17. **One truth, several depths.** Product, flow, architecture, detail, and
    evidence views derive from the same records. Users choose viewing depth,
    while consequential hidden facts rise to the approval surface.
18. **Safe assumptions have a test.** An assumption may proceed without a
    question only when it is reversible inside the slice, changes no measure or
    boundary, creates no external commitment, and would not reasonably change
    the person's decision to run the work.
19. **Important facts rise.** Unmet mandatory outcomes, material losses,
    unresolved producer decisions, weak proof, external commitments, blocked
    dependencies, and changed safeguards appear in every approval view.
20. **Evidence admission is explicit.** Model output enters product truth only
    when it maps to a measure, resolves a named uncertainty, or supplies
    independently verifiable evidence.
21. **One Conductor, not a skill per phase.** Building, peer review, proof,
    improvement, and completion are responsibilities inside Conductor. Switch
    remains the separate continuity capability; another skill is added only
    when repeated work proves it needs a stable lifecycle of its own.
22. **Direction fixed, route flexible.** After the person approves the outcome,
    experience, measures, guardrails, authority, resources, and stopping point,
    Conductor may change the route but not those consequential facts.
23. **The builder does not grade itself.** A peer or different model judges the
    original measures from admissible evidence. Three materially different
    failed corrections against one measure return routing control to Conductor.

## 1. Requirements at two levels

A one-off task uses a work brief directly. A product containing several
features uses a build brief plus one feature brief per independently testable
capability. A feature map records dependencies and readiness without redefining
the briefs.

Conductor selects one ready feature or one coherent slice for execution. It
inherits relevant product boundaries and dependency evidence, then becomes the
work brief described below. The whole backlog is never copied into every
model's prompt.

The schemas, examples, state vocabulary, combination rules, and three levels
of success are defined in
[Capturing requirements and features](requirements-and-features.md).

Success rolls up in order: feature result, integrated result, then product
result. Passing every feature separately does not prove the user journey works.

## 2. The product journey

The normal interface is:

1. Enter: fresh work asks “What would you like to make happen?” unless the
   invocation already contains the request. Active work resumes its saved
   question or next action. Do not infer new intent from a preloaded trial.
2. Understand: conversational intake retrieves relevant known facts after the
   initial request, challenges the
   request, and asks only questions that can materially change the work.
3. Shape: Conductor defines the outcome, experience, connected parts, measures,
   proof, guardrails, authority, resources, and stopping point.
4. The person approves one plain-language visual direction. The recorded
   approval references the exact displayed version; content changes invalidate it.
5. Conductor selects a coherent slice, focused context, model, effort, and peer
   review appropriate to each bounded job.
6. A coverage check proves the prepared job lost or changed no obligation.
7. Build runs autonomously: execute, peer review, prove, and improve.
8. A failed measure returns to the loop. After three materially different
   failed attempts, Conductor changes the route or raises one consequential
   decision when the approved direction cannot be honoured.
9. Conductor completes only when every measure independently passes and the
   agreed stopping point has been reached.

Switch preserves project and session continuity throughout. It is not a phase
inside Conductor. The decisions behind this boundary are recorded in
[Guided-interview decisions](guided-interview-decisions.md).

The complete behavior, examples, failure classes, and minimum product are in
[Making model-ready work easy, fast, and excellent](easy-fast-excellent.md).

## 3. The work brief

The work brief is intentionally small. It contains facts about the job, never
provider syntax and usually no execution plan.

```yaml
task:
  id: foreign-repo-gate-probe
  objective: Prove a Kerd gate can inspect a consuming repository.
  deliverable:
    - A reproducible probe and its captured output.
  success:
    - id: S1
      measure: Target repository named by the refusal
      target: equals the disposable foreign repository, never Kerd
    - id: S2
      measure: Manual path supplied by the producer
      target: zero
  evidence:
    - command transcript
    - fixture result linked to S1 and S2
  context:
    required:
      - skills/drive/SKILL.md
      - tools/gates/gate.py
    retrieve_if_needed:
      - tools/gates/kit.py
  guardrails:
    - Read-only probe; do not edit either repository.
    - Do not infer environment-variable availability; measure it.
  authority:
    may_decide:
      - probe command and disposable-repository contents
    producer_owned:
      - fallback mechanism if the plugin variable is absent
  unknowns:
    - Is CLAUDE_PLUGIN_ROOT available inside a skill-invoked command?
  completion:
    - Stop when S1 and S2 have observed results or a blocker is evidenced.
```

Required fields: `id`, `objective`, at least one `deliverable`, at least one
measurable `success` row, `evidence`, `guardrails`, `authority`, and
`completion`. Context may be empty for a self-contained task. Unknowns may be
empty; an empty unknown set is not permission to invent one.

The envelope distinguishes four easily-confused things:

- **Success** says what winning changes and how it will be observed.
- **Evidence** says what artifact makes that observation reviewable.
- **Guardrails** say what must not happen while pursuing it.
- **Completion** says when the executor stops rather than continuing to polish.

The anatomy is drawn in [the work-brief view](diagrams/task-envelope.html).

## 4. Assessment and routing

Conductor assesses the envelope, not the perceived prestige of the work.

| Axis | Question | Output |
|---|---|---|
| Capability | What modalities, tools, context length, coding or reasoning ability are required? | eligible model families |
| Consequence | What is the cost of a wrong action or false conclusion? | autonomy and verification tier |
| Complexity | How much decomposition, ambiguity resolution, and tool-loop depth remains? | effort starting point |
| Latency | Is this interactive, routine, or asynchronous? | effort ceiling and response budget |
| Evidence | Can success be checked mechanically, by blind review, or only by the producer? | evaluator and stop gate |
| Familiarity | Does a tested adapter exist for this task class? | deterministic compile or prompt-composer call |

The assessment emits a **model choice** with its premise visible:

```yaml
dispatch:
  provider: anthropic
  model_family: opus-5
  model_id: claude-opus-5
  adapter: anthropic-opus-5@2026-09
  effort: high
  compilation: deterministic
  rationale:
    - multi-step repository investigation
    - false-root conclusion is high consequence
    - adapter evaluated on tool-heavy coding probes
```

This remains advice where the harness cannot observe or set the actual pair.
Conductor states the believed pair and the producer confirms it, as today.

## 5. Preparing the model-ready brief

Conductor takes four inputs:

1. Frozen task envelope.
2. Dispatch decision.
3. Versioned model-family adapter.
4. Retrieved context bundle, with provenance.

It emits:

- the execution prompt;
- a preservation manifest mapping every envelope obligation to a prompt region
  or native tool/schema mechanism;
- prompt metadata: adapter version, source date, token count, compilation path;
- an evaluation handle binding the run to the frozen success rows.

Compilation order:

1. Validate the envelope and freeze its digest.
2. Select eligible models and an initial effort from the assessment.
3. Select a tested adapter; otherwise use the neutral baseline.
4. Retrieve only declared context, keeping dynamic material after stable
   instructions where the platform benefits from caching.
5. Render model-native structure.
6. Check semantic preservation and prompt budget.
7. Execute, collecting trace measures.
8. Judge against the original envelope, never the compiled prose.

See [the detailed preparation flow](diagrams/compiler-flow.html).

## 6. Model-guidance contract

```yaml
adapter:
  id: anthropic-opus-5
  version: 2026-09
  provider: anthropic
  model_family: opus-5
  tested_models: [claude-opus-5]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
      read: 2026-09-04
  last_evaluated: null
  clauses:
    - id: xml-boundaries
      applies_when: prompt mixes instructions, context, examples, and input
      rendering: use descriptive XML containers
      basis: provider-guidance
      evaluation: pending
```

Every clause declares:

- when it applies;
- what it changes;
- whether its basis is provider guidance, a Kerd evaluation, or an invariant;
- the evaluation that keeps it alive;
- any known interaction with effort, tool use, or output length.

Provider guidance is permission to test, not permanent evidence of benefit.
After the first pilot cycle, a provider-only clause either gains evaluation
evidence or expires.

### Local model guidance

[`guidance/`](guidance/README.md) is the runtime knowledge source. It holds:

- `README.md` — the registry contract, source policy, lifecycle, and precedence;
- `anthropic/shared.md` and `openai/shared.md` — provider-wide guidance only;
- one model-family profile per family Kerd can actually dispatch;
- local examples compiled from Kerd task envelopes, never copied wholesale
  from vendor documentation;
- a manifest recording source URL, retrieval date, applicable model IDs,
  superseded profile, evaluation status, and next review trigger.

The official pages are not vendored as full mirrors. Full copies would become
large, stale, and difficult to distinguish from current authority. The local
files retain the actionable guidance and examples Kerd needs quickly, while the
URL and retrieval date preserve provenance and make an update audit possible.

Precedence is explicit:

1. Repository and producer guardrails.
2. Frozen task envelope.
3. Native platform/tool contract.
4. Evaluated model-family guidance.
5. Provider-shared guidance.
6. Unevaluated official recommendation, admitted only as a pilot clause.

Nothing lower on the list may weaken or reinterpret anything above it.

## 7. Example preparations

All three examples below compile the envelope in §1. They preserve identical
success measures and guardrails.

### Neutral baseline

```markdown
Objective: Prove a Kerd gate can inspect a consuming repository.

Deliver a reproducible, read-only probe and captured output. Success means the
refusal names the disposable foreign repository rather than Kerd, with no path
manually supplied by the producer. Provide the command transcript and link each
fixture result to S1 and S2.

Use the listed context. Do not edit either repository and do not assume the
plugin environment variable exists—measure it. Choose the execution method.
Stop when both success rows have observed results or an evidenced blocker.
```

### Claude-family rendering

```xml
<role>You are the repository investigator responsible for producing a
reproducible, evidence-backed result.</role>
<objective>Prove a Kerd gate can inspect a consuming repository.</objective>
<success_criteria>
  <criterion id="S1">The refusal names the disposable foreign repository,
  never Kerd.</criterion>
  <criterion id="S2">The producer manually supplies zero paths.</criterion>
</success_criteria>
<guardrails>
  <rule>Run a read-only probe; edit neither repository.</rule>
  <rule>Measure CLAUDE_PLUGIN_ROOT availability; do not infer it.</rule>
</guardrails>
<context>…retrieved documents with path labels…</context>
<task>Choose the most efficient method. Return the transcript and map observed
evidence to S1 and S2. Stop on proof or an evidenced blocker.</task>
```

Why it differs: Claude's current guidance recommends clear/direct language,
descriptive XML boundaries for mixed prompt material, a focused role, and
general rather than hand-authored reasoning steps. Examples are included only
when evaluation shows the output shape needs them.

### OpenAI reasoning-model rendering

```markdown
# Outcome
Prove a Kerd gate can inspect a consuming repository.

# Success and evidence
- S1: the refusal names the disposable foreign repository, never Kerd.
- S2: producer-supplied paths = 0.
- Return the command transcript and map evidence to S1 and S2.

# Guardrails and authority
- Read-only: edit neither repository.
- Measure environment-variable availability; do not infer it.
- You may choose the probe and disposable-repository contents.
- Stop when S1 and S2 are observed or a blocker is evidenced.

# Context
…dynamic retrieved context placed after stable instructions…
```

Why it differs: current official OpenAI guidance favors outcome-first prompts,
explicit success/stopping rules, native tool and structured-output contracts,
and less prescribed process. Reasoning effort is request configuration, not a
paragraph telling the model how intelligent to be.

## 8. Evaluation design

The pilot is an A/B/n comparison over the same frozen envelopes:

- A — current Conductor path.
- B — neutral envelope baseline.
- C — Claude adapter at its selected effort.
- D — OpenAI adapter at its selected effort.

Where model access permits, each eligible condition runs at least three times.
Run order is randomized. The reviewer sees the deliverable, evidence, and
success rows, but not the model, adapter, effort, or prompt.

### Measures

| Dimension | Measure | Better means |
|---|---|---|
| Outcome | success rows met / total | higher; mandatory rows all met |
| Correctness | blind-review defects by severity | fewer |
| Evidence | required evidence present and resolving | higher |
| Speed | wall-clock time to adjudicable result | lower at outcome parity |
| Cost | input, cached-input, reasoning, and output tokens | lower at outcome parity |
| Agency | producer corrections and avoidable approval stops | fewer |
| Efficiency | tool calls, repeated reads, unnecessary files | fewer without missed evidence |
| Robustness | variance across repeated runs | lower |

No weighted composite hides a failed mandatory outcome. Pareto comparison is
used first: a variant graduates when it maintains task success and improves at
least one efficiency measure without a material regression elsewhere.

### Clause ablation

After a model adapter wins, remove or add one clause at a time against the same
task set. The clause survives only if the change produces a repeatable benefit
or it names an invariant no machine surface can enforce. This is how Kerd stops
historical failure corrections from accumulating forever.

See [the results-and-learning loop](diagrams/evaluation-loop.html).

## 9. Relationship to current Kerd

The pilot classifies current instructions into five destinations:

| Destination | Test | Example |
|---|---|---|
| Machine invariant | Can code enforce it more reliably than prose? | stale-render refusal |
| Universal envelope rule | Is it true for every model and task? | preserve producer-owned decisions |
| Model adapter | Does one tested family benefit measurably? | XML separation for a complex Claude prompt |
| Retrieved task module | Is it needed only for this work type? | document-render QA workflow |
| Delete | Does it protect no invariant and improve no evaluation? | legacy anti-laziness repetition |

Conductor keeps session ownership—orient, select work, confirm authority,
compile, dispatch, evaluate, close. It stops prescribing the executor's inner
method unless that method is itself part of the product contract.

## Stage-1 measurements — named answers

| Measurement | Target | How it will be answered |
|---|---|---|
| Requirement preservation | 100% of required work-brief obligations mapped in every coverage report | preparation fixtures plus coverage audit |
| Task success | model-ready variant equals or beats current Conductor on every mandatory success row | independent pilot review |
| Efficiency gain | at least one of elapsed time, total input tokens, interventions, or unnecessary stops improves by 20% median with no material regression | run telemetry across repeated matched tasks |
| Instruction reduction | compiled prompt contains at least 40% fewer instruction tokens than the current-path prompt for the pilot median | tokenizer report, same task context excluded from both counts |
| Cross-model portability | one fixed work brief runs through Claude and OpenAI model guidance without producer rewriting | work-brief fingerprint identical across both run records |
| Guidance accountability | 100% of model-specific instructions name a source or boundary and evaluation state | model-guidance audit |
| Local lookup | preparation performs zero web requests and resolves its chosen model profile locally | offline preparation fixture |
| Intake usability | a product-minded test user reaches an approved brief without seeing the schema or raw prompt | observed journey test and question count |
| Time to ready | quick tasks reach a ready verdict in one exchange when the request contains all required facts | intake transcripts across quick-task fixtures |
| Context freshness | every changed required source or dependency invalidates the context pack before execution | stale-context fixtures |
| Retry isolation | 100% of failure fixtures change only the classified layer unless another cause is evidenced | retry-diff report across all six failure classes |
| Result readability | a reviewer can state what passed, failed, changed, and needs a decision using only the outcome report | cold-eyes comprehension check |

These are proposed targets. They must be keyed before the first pilot run; the
pilot may resize them, but never after seeing results.
