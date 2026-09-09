# Earlier prototype implementation specification

**Superseded adoption sequence.** This document preserves the earlier
standalone-first prototype plan, including baseline experiments that are no
longer requested. Do not execute it as the current work order. Use
[the Conductor rework specification](conductor-rework-spec.md) instead.

The historical content below explains existing prototype artifacts; unchecked
pieces and example commands are not evidence that the process was built.

Contract for this folder's [proposal](proposal.md) and [design](design.md). This
specification builds the smallest test that can decide whether model-ready
briefs should replace Kerd's common process prompt. It does **not** rewrite
Conductor.

The first proof uses the two real-work contracts in
[the trial pack](trials/README.md), each in a disposable repository. Live Kerd
stays frozen. Live Drive and Conductor retain their current ownership until the
trials provide evidence and the conflicting contracts are explicitly resolved.

## Outcome contract

One canonical work brief is prepared for a neutral baseline, one tested Claude
family, and one tested OpenAI reasoning-model family. Matched tasks are run and
independently judged against measures frozen before execution. The result is
a decision backed by task success, time, tokens, interventions, and evidence—not
preference for shorter prompts.

## Pieces

- [ ] 1. Producer gate — approve the process views, product journey, and measurable trial targets before any run.
- [ ] 2. Add schemas and readable examples for the build brief, feature brief, feature map, and execution work brief.
- [ ] 3. Build the adaptive interview loop: reflect understanding, retrieve existing answers, rank uncertainties by information value, ask one small related group, update assumptions, and stop when ready.
- [ ] 4. Add origin and challenge handling. A no-question assumption must be reversible inside the slice, change no measure or boundary, create no external commitment, and not reasonably change the person's decision to run. Everything else is asked or refused.
- [ ] 5. Add success-measure assistance that distinguishes activity, output, outcome, and proof, with approval before results exist.
- [ ] 6. Implement proposed Quick, Standard, and Important/Deep levels derived from consequence, reversibility, uncertainty, external commitment, and proof strength. Lower-safety overrides name the lost protection and hard safety boundaries remain non-overridable.
- [ ] 7. Add the ready-to-run verdict with fixtures for missing outcomes, measures, proof, boundaries, dependencies, decision rights, and done conditions.
- [ ] 8. Implement feature-map derivation and state checks; the map summarizes feature records but cannot redefine them.
- [ ] 9. Implement slice selection: accept one ready feature or a proven inseparable group; reject flat backlogs and unsatisfied dependencies.
- [ ] 10. Implement inheritance of only relevant build boundaries, dependency evidence, context, and integration points.
- [ ] 11. Build focused context packs with required-now, retrieve-if-needed, and excluded sections.
- [ ] 12. Add source fingerprints and invalidation rules so stale requirements, dependencies, or files refuse execution until refreshed.
- [ ] 13. Implement the plain-language preparation preview and user-facing work view: product outcome, feature map, selected slice, live activity, proof state, next action, and needed decision—all derived from underlying records.
- [ ] 14. Implement deterministic work-brief validation and neutral preparation in `mvp/compiler.py`; no model call on the fast path.
- [ ] 15. Implement the coverage report and fixtures proving that prepared prompts cannot drop or alter required work.
- [ ] 16. Complete local, versioned guidance and Kerd-owned examples for every available Claude and OpenAI model family.
- [ ] 17. Implement the starting model/effort table and evidence-based escalation; a model's self-report cannot trigger escalation alone.
- [ ] 18. Encode the execution contract: act when ready, choose the method, respect decision rights, verify proportionally, map proof to measures, and stop only on completion or a demonstrated blocker.
- [ ] 19. Add consequence-based review and bounded cross-model jobs. Every job has inputs, outputs, measures, proof, decision rights, a stop condition, a cost/time ceiling, and a declared measure it should improve; open-ended model chats are refused.
- [ ] 20. Add derived Product, Flow, Architecture, Detail, and Evidence views plus the plain-language outcome report. Unmet mandatory outcomes, losses, unresolved decisions, weak proof, external commitments, blocked dependencies, and safeguard changes appear in every approval view.
- [ ] 21. Classify failed runs as requirement, context, selection, execution, proof, or product failures and change only the responsible layer on retry.
- [ ] 22. Capture the current Conductor path as the baseline without changing it; separate stable instructions from task context.
- [ ] 23. Define a mixed trial set: quick communication or documentation work, an ordinary product or project deliverable, a software feature slice, and a consequential executive, research, operational, or migration decision. Freeze outcome measures before model selection.
- [ ] 24. Build the run recorder for fingerprints, model, guidance version,
  effort, time, tokens, tool calls, interventions, stops, output, proof, review,
  and total elapsed time from initial request to accepted usable outcome. Model
  cost may compare capable eligible routes; it may not make an incapable model
  eligible.
- [ ] 25. Execute randomized repeated runs where access permits; never change a brief, target, or review rule after seeing results.
- [ ] 26. Independently review outcomes, prove roll-up, compare efficiency and consistency, and publish raw results and exclusions.
- [ ] 27. Apply the anti-bloat learning order and test model guidance one instruction at a time; classify current Conductor instructions into machine rule, universal brief rule, model guidance, task-specific guidance, or delete.
- [ ] 28. Producer adoption decision, full suite, documentation and visual review, release handling, commit, push, and observed CI verdict.

## Verification by phase

### Work brief and preparer

Commands in this specification are future interface contracts unless the
referenced file exists. The current demonstration exposes only the commands
documented in `mvp/README.md`.

```bash
python3 docs/work/model-ready-work/mvp/compiler.py selftest
python3 docs/work/model-ready-work/mvp/compiler.py validate docs/work/model-ready-work/mvp/examples/*.json
```

Expected: schema failures are named by field; valid work briefs prepare; every
required obligation appears in the coverage report.

### Multi-feature intake

```bash
python3 docs/work/model-ready-work/mvp/compiler.py validate-build <build.json>
python3 docs/work/model-ready-work/mvp/compiler.py validate-feature <feature.json>
python3 docs/work/model-ready-work/mvp/compiler.py select-slice <feature-map.json>
```

Expected: the feature map derives its state from feature records; only ready
features with satisfied dependencies enter a slice; shared boundaries are
inherited without copying unrelated features; feature, integrated, and product
measures remain distinct.

### Usable journey

```bash
python3 docs/work/model-ready-work/mvp/journey.py selftest
python3 docs/work/model-ready-work/mvp/journey.py demo ordinary-feature
```

Expected: ordinary language produces a readable draft; material gaps produce
one small question batch; safe assumptions are visible; the readiness verdict
is accurate; brief size and slice are explained; stale context refuses; the
person sees the preparation preview; and the final result is understandable
without opening the raw prompt or telemetry.

Test the same journey at all three proposed work levels. A product-minded reviewer
must answer what is being built, where it stands, what is happening now, what
has been proven, and what needs them using only the visual work view.

The trial must also determine whether three levels are understandable and
meaningfully different. Failure there changes the level design; it does not
lower the usability measure.

Interview fixtures must show that repository-known and model-owned questions
are not asked, consequential assumptions are not silently made, related
questions are grouped, and the interview stops once further answers would not
change readiness.

Cross-model fixtures must refuse unbounded model conversation, prove that every
job shares the fixed measures, and prevent speculative output from entering the
product record without Conductor review.

Visual fixtures must prove all depth levels derive the same position and result
and that a material loss found in a detailed view appears in the approval view.

### Recovery

Fixtures must independently cause requirement, context, selection, execution,
proof, and product failures. Each retry changes only the classified layer.
Instrumentation must report when a retry adds prompt text so unbounded growth
cannot hide inside recovery.

### Adapter audit

```bash
python3 docs/work/model-ready-work/mvp/compiler.py profiles
```

Expected: each guidance profile is versioned and model-family-specific; each
instruction records when and why it applies, its source, evaluation state, and
review trigger; source-only instructions remain pending until tested; every
available model ID resolves locally; preparation makes no network request.

### Pilot integrity

```bash
python3 docs/work/model-ready-work/mvp/eval.py verify-freeze docs/work/model-ready-work/mvp/evals
python3 docs/work/model-ready-work/mvp/eval.py summarize docs/work/model-ready-work/mvp/evals
```

Expected: envelope and rubric digests predate results; matched variants share
the envelope digest; run metadata is complete; mandatory outcomes are reported
before efficiency; exclusions and unavailable model conditions remain visible.

### Graduation

The pilot recommends adoption only when:

1. Requirement preservation is 100%.
2. No mandatory success result regresses against current Conductor.
3. At least one declared efficiency measure improves by the keyed threshold.
4. The result repeats across enough runs to distinguish a pattern from one
   favorable sample.
5. Every surviving model-specific instruction has results or boundary evidence.
6. Multi-feature trials pass at feature, integrated, and product levels.

If no prepared variant meets all six, the pilot does not fail silently: it
records which premise failed and leaves current Conductor unchanged.

## Example task set

| Class | Candidate Kerd task | Why included |
|---|---|---|
| Routine | Correct one stale documentation claim with its source | tests fast-path overhead and unnecessary ceremony |
| Diagnostic | Find why a gate command targets the wrong repository | tests investigation and tool selection |
| High consequence | Plan an atomic live-schema migration | tests guardrails, ordering-as-requirement, and proof |
| Visual | Correct and verify a sealed design view after a later ruling | tests multimodal/context packaging |
| Research | Compare current provider prompting guidance | tests source discipline and synthesis |
| Judgment | Qualify a fatal risk without conflating severity and treatment | tests producer ownership and ambiguity handling |
| Product | Turn a rough opportunity into an evidence-backed feature proposal | tests non-technical intake and measurable value |
| Executive | Prepare a decision brief with alternatives, losses, and unresolved evidence | tests progressive disclosure and decision ownership |
| Operations | Produce a launch or operating plan with owners, dependencies, and proof | tests multi-feature coordination outside software |

The producer may replace candidates before Piece 9 is keyed. After freeze, no
task is removed merely because one variant performs badly.

## Review gates

- **Design:** the diagrams, work-brief fields, model-guidance contract, measures,
  and thresholds are keyed.
- **Handoff:** every step above has executable detail in the implementation
  score written after the pilot environment and available model IDs are known.
- **Loop:** raw runs, reviews, and guidance tests exist; no summary-only result.
- **Acceptance:** the adoption decision cites the frozen measures and resolving
  evidence. "Prompts are shorter" alone cannot pass.
