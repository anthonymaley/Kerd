---
route: new
stage: framed
concerns:
  - concern: the model-neutral task envelope and what belongs in it
    viewpoint: annotated anatomy
    view: docs/work/model-ready-work/diagrams/task-envelope.html
    approval: superseded by expanded working design, 2026-09-04
  - concern: compilation from one requirement into a model-specific execution prompt
    viewpoint: flowchart
    view: docs/work/model-ready-work/diagrams/compiler-flow.html
    approval: superseded by expanded working design, 2026-09-04
  - concern: proving that an adapter improves work rather than merely changing it
    viewpoint: experiment loop
    view: docs/work/model-ready-work/diagrams/evaluation-loop.html
    approval: superseded by expanded working design, 2026-09-04
  - concern: guided interview, bounded model jobs, and progressive viewing depth
    viewpoint: product experience
    view: docs/work/model-ready-work/diagrams/guided-experience.html
    approval:
---

# Model-ready work — proposal

**Adoption update:** [Rework Conductor, keep Kerd](kerd-conductor-rework.md)
is now the proposed integration path. Keep this document for product rationale;
use that proposal and its linked spec for implementation. No live behavior has
changed and earlier approvals do not approve the rework automatically.

**Further supersession:** the next design removes gate ladders, seals,
requirement fingerprints, mandatory registers and CI/hook usage dependencies.
The historical risk/grounding schema below and the former requirement to consume
the full measurement protocol are not obligations of the new process. Reuse
useful existing measures without imposing their old machinery.

**Plain-language summary:** people describe the job once. Conductor prepares
that same job for the chosen model without changing what success means. The
model gets freedom over how to work, and evidence decides whether it succeeded.

## Value

Tony's direction, 2026-09-04:

> Conductor should analyse the effort required for a task, then take the
> requirement and model the prompt specifically to be optimal for that model
> and to get the best results. Template the requirements so that is easy:
> high-level clarity, measurable success, guardrails — then let the models cook
> to their best abilities.

Kerd currently gives every model a large common process and varies mainly the
model and effort used for a call. This item inverts that arrangement. The
requirement becomes a stable, model-neutral **work brief**. Conductor selects a
model and effort, then prepares the brief using versioned guidance for that
model family. The executor owns the method unless the method is itself a
requirement. The same stable success measures judge every prepared version.

**Winning, in units:**

- A producer can state one requirement once and use it with at least two model
  families without rewriting the requirement.
- Every prepared prompt preserves 100% of the brief's objective, required
  deliverable, success measures, evidence obligations, guardrails, authority,
  and completion condition.
- On the two agreed new-process trials, the work must meet its original measures
  and show its actual elapsed time, resource use, interventions and proof.
  Comparative improvement remains a hypothesis: the user chose not to duplicate
  the work through current Conductor as a baseline.
- No model-specific instruction becomes universal merely because it sounds
  prudent. It survives only when a named evaluation shows a repeatable gain or
  it protects an invariant that machinery cannot enforce.

The product promise is not "short prompts" by itself. It is **less instruction
load without less truth**: precise outcomes and proof, model-native prompting,
and freedom over method.

The experience promise is equally important: a product-minded person can state
the need conversationally, approve a clear brief, and understand the result
without seeing provider syntax or learning prompt engineering. The adopted
experience is defined in
[Making model-ready work easy, fast, and excellent](easy-fast-excellent.md).

Tony's desired outcomes, 2026-09-04, are captured separately from the proposed
mechanisms in [Product vision](product-vision.md). Quick, Standard, and
Important/Deep; the visual work view; question batching; and cross-model
routing are working hypotheses to validate, not requirements attributed to the
producer merely because they currently look promising.

## External grounding read 2026-09-04

- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview — Anthropic's sequence: define success criteria and an empirical test before tuning a prompt.
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices — current Claude guidance on clear/direct instructions, relevant context, diverse examples, XML for mixed prompt material, model-specific behavior, and general reasoning instructions over prescriptive human-written steps where order is not required.
- https://platform.claude.com/docs/en/build-with-claude/effort — effort is a model-and-workload control whose setting must be tested on the actual use case.
- https://developers.openai.com/api/docs/guides/latest-model — current OpenAI guidance on outcome-first prompts, explicit success and stopping conditions, reduced step-by-step process guidance, evaluated reasoning effort, and native structured/tool contracts.

The gate's Grounding format cannot resolve external sources; that known format
gap is not bypassed by pretending URLs are repository paths. The locally stored
interpretations below carry the external provenance into the checkable tree.

## Grounding

- skills/conductor/SKILL.md — today's common orchestration prompt, model/effort advisory, composer/player split, and verification discipline.
- docs/product/requirements-success-measurement.md — existing work that makes a requirement's measurement a first-class artifact; this item consumes that contract rather than inventing a second measurement system.
- tools/gates/kit.py — deterministic refusal stays outside the generated prompt; the compiler never replaces a machine-checkable invariant with prose.
- docs/work/model-ready-work/guidance/README.md — local guidance contract, source fields, precedence, and update lifecycle.
- docs/work/model-ready-work/guidance/anthropic/shared.md — locally stored interpretation of current cross-model Claude guidance with direct official-source provenance.
- docs/work/model-ready-work/guidance/openai/shared.md — locally stored interpretation of current cross-model OpenAI reasoning guidance with direct official-source provenance.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
|---|---|---|---|---|---|---|---|---|---|
| Preparing work for a model silently changes the requirement — model guidance drops an awkward boundary or softens success | yes | The model returns a polished answer to a different task. The product's whole value is inverted | High without a coverage check: every model-specific rewrite creates this opportunity | Kerd's repeated two-sources drift class; OpenAI and Anthropic both distinguish stable task intent from model-specific prompting technique | fatal | countermeasure - permanent | Work-brief fields are fixed inputs. Preparation emits a coverage report mapping every required field to its prepared location or machine rule; execution refuses missing or altered obligations | planned — coverage report and preservation fixtures · mvp/compiler.py | Any prepared brief whose coverage report cannot point to every required field reopens the row |
| Kerd replaces one giant prompt with a library of giant model guides | yes | Instruction load and conflict move rather than shrink; models remain constrained and maintenance multiplies by model family | High: every historical failure invites another permanent sentence, and model profiles create more places to put one | `skills/conductor/SKILL.md` is about 8,600 words with 83 strong directives; vendor guidance says to dial back legacy anti-laziness and detailed process scaffolding for newer models | fatal | countermeasure - permanent | Model guidance requires one of two justifications: a cited provider recommendation for the exact model family, or a named evaluation failure improved by the instruction. Preparation records prompt-token count and rejects undocumented guidance | planned — guidance source schema and size report · docs/work/model-ready-work/guidance/README.md | Any model guide grows without a linked source or evaluation result; any prepared prompt exceeds the current baseline without a measured gain |
| The evaluation rewards compliance artifacts rather than useful outcomes, so the most constrained prompt wins | no | Kerd optimizes for looking orderly while speed, correctness, or producer value stagnate | High: the schema-split completed fourteen steps with no predeclared measurable outcome, proving structural compliance can pass alone | `risk-state-split` acceptance finding, 2026-09-04: no stage-1 measurements existed, so outcome could only be recorded as cannot be assessed | fatal | countermeasure - permanent | Every trial declares outcome measures before variants run. Artifact compliance is diagnostic, never the task-success score. Independent review sees outputs without model identity | planned — trial protocol and independent result sheet · mvp/evals/ | A run begins before its success measure and review method are fixed |
| Model profiles rot as providers change model behavior | no | A once-helpful instruction becomes redundant or harmful; results regress while the guidance still looks authoritative | Certain over time: both official guides publish model-specific advice and explicitly identify legacy-prompt overtriggering | Current Anthropic guidance separates Fable, Sonnet, and Opus behavior; current OpenAI guidance tells teams not to carry every older instruction forward | non-fatal | countermeasure - permanent | Every profile declares provider, model family, profile version, source URL/date, tested model identifier, and last evaluation. New model families start from the neutral work brief, not by copying the nearest profile | planned — versioned guidance header and staleness finding · docs/work/model-ready-work/guidance/README.md | Provider guidance changes, a model identifier changes, or the profile's last evaluation crosses the declared age limit |
| Preparing a model-ready brief costs more time than it saves on routine work | no | Small tasks become slower and more ceremonial than today's inline path | Medium: preparation can become another model call if designed naively | Today's Conductor already distinguishes trivial and inline work; both vendors recommend low effort for simple or latency-sensitive tasks where evaluations hold | non-fatal | countermeasure - permanent | Deterministic templates prepare common task shapes without a model call. A composing call is reserved for novel, high-judgment work; quick tasks use the neutral brief directly | planned — fast-path timing fixture and no-model preparation path · mvp/compiler.py | Median preparation overhead exceeds 10% of end-to-end time for the routine trial class |
| Optimizing separately for Claude and OpenAI teaches provider folklore rather than measured behavior | no | Model guides accumulate XML, roles, or reasoning phrases that add tokens without improving results | Medium-high: official examples are starting points, not proof for Kerd's workload | Both vendors explicitly require empirical testing on the actual use case | non-fatal | countermeasure - permanent | Official guidance permits a trial; only repeated Kerd results promote a technique into model guidance. Source-only instructions expire unless the trial confirms them | planned — instruction sources and one-at-a-time guidance results · mvp/evals/ | A model-specific instruction has a citation but no Kerd evaluation after the first trial cycle |
| Conversational intake confidently turns an ambiguous request into the wrong brief | yes | The system executes efficiently against a requirement the person never intended | High without approval: ordinary product language contains implied users, edge cases, and decisions | The structured brief exists precisely because an initial request is rarely a complete outcome contract | fatal | countermeasure - permanent | Conductor distinguishes safe assumptions from consequential decisions, shows both, asks one small material-question batch, and requires approval of the readable brief before execution | planned — intake ambiguity fixtures and approval record · easy-fast-excellent.md | A person rejects a drafted outcome, boundary, decision right, or measure after execution began |
| Focused context is incomplete or stale | yes | A well-prepared model acts on missing or outdated product truth and returns persuasive but invalid work | High in a changing repository: requirements, dependency results, and source files move between selection and execution | Kerd's derived-from-disk and stale-render rules already establish that agreeing prose can still be wrong | fatal | countermeasure - permanent | Every context item records source, fingerprint, relevance, and invalidation condition; changed inputs refuse execution until the context pack is refreshed | planned — context freshness fixtures · easy-fast-excellent.md | Any run uses changed required context without refusal or explicitly recorded refresh |
| Automatic retry hides the cause and grows the prompt after every failure | no | Cost and instruction load rise while the actual requirement, context, selection, proof, or product defect remains | High without classification: adding more instructions is the easiest generic reaction to a weak result | The current common process accumulated corrections from many historical failure classes | fatal | countermeasure - permanent | Every failed run is classified before retry; only the responsible layer changes; prompt growth is reported and universal instructions remain the last resort | planned — six failure-class fixtures and retry-diff report · easy-fast-excellent.md | A retry changes more than one layer without a named reason or adds universal prompt text without evaluation evidence |

## Scope

The smallest valuable increment is a **measured trial**, not a rewrite of
Conductor. Kerd stays frozen while the new path is exercised beside it.

In scope:

- Define the canonical work-brief schema and a human-readable template.
- Define a build brief, feature brief, and feature map so multi-feature products
  roll into focused execution without becoming one giant prompt.
- Define how Conductor selects one ready feature or coherent slice, carries only
  relevant parent boundaries and dependency evidence, and rolls results back up.
- Add conversational intake, measure assistance, three brief sizes, a
  ready-to-run verdict, and a preparation preview.
- Add focused context packing with freshness checks and explicit exclusions.
- Add evidence-based model escalation, consequence-based review, classified
  recovery, and a plain-language outcome report.
- Apply the anti-bloat learning order before adding any new prompt instruction.

### Deliberately not in the first usable slice

- No broad automated model marketplace or universal routing claim.
- No open-ended conversations between models.
- No automatic prompt optimization.
- No attempt to implement every visual depth at once.
- No claim that the system works equally well across domains before mixed-domain
  trials.
- No replacement of live Conductor before the Standard guided journey passes.
- Define how Conductor prepares a brief and proves every obligation survived.
- Define a local, versioned guidance registry and adapter profiles for every
  Claude and OpenAI model family used by Kerd. Each profile stores the relevant
  official guidance as a concise local interpretation, plus Kerd-owned examples
  and source/version metadata; compilation never depends on fetching docs live.
- Produce examples showing one envelope compiled three ways: neutral baseline,
  Claude-optimized, and OpenAI-optimized.
- Define the evaluation protocol, measures, blind adjudication, repetition, and
  graduation rule.
- Run representative tasks from this repository without changing Kerd's live
  skills; record time, prompt tokens, tool calls, interventions, stops,
  correctness, and evidence completeness.
- Decide from results which current Conductor instructions remain universal,
  move into adapters, become machine checks, load only on demand, or die.

Excluded until the pilot earns them:

- No rewrite of `skills/conductor/SKILL.md`.
- No automatic provider or model switching.
- No generated prompt may weaken repository permissions, destructive-action
  rules, producer-owned decisions, or machine gates.
- No universal adapter for "Claude" or "OpenAI"; profiles bind to tested model
  families and versions. A provider-level file may hold only genuinely shared
  guidance and must not erase model differences.
- No LLM call merely to fill a deterministic template.
- No flat feature catalogue is passed wholesale to an executor.
- No feature-local pass is allowed to stand in for integrated or product
  success.
- No claim that fewer tokens means better work without outcome parity.
- No requirement that an ordinary user understand model families, prompt
  structure, schemas, tokens, or internal evaluation vocabulary.
- No automatic retry that changes multiple layers at once and hides the cause.

Rigor level: production-v1
