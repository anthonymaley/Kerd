# Rework Conductor: strong process, lightweight records

**Next proposal. Not implemented.** This revision follows the user's decision
to remove complex rung gates, seals, requirement fingerprinting and elaborate
approval schemes. It replaces this pack's earlier “keep and extend the gates”
proposal. Live skills and the parked Conductor session are unchanged.

Start with the [process drawing](diagrams/kerd-conductor-rework.html) and
[implementation spec](conductor-rework-spec.md). Earlier pack documents are
supporting material, not authority to reintroduce the mechanisms removed here.

## What we are proposing

Conductor guides a person from an idea to completed, evidenced work. It asks
useful questions, captures the agreement, shows the design, prepares appropriate
model jobs, and runs build, review and improvement within agreed boundaries.

Keep that discipline. Remove the paperwork and infrastructure that have become
a second product to operate.

**No CI is required to install, start, resume, advance or complete work with any
Kerd skill.** Kerd's developers may use CI to test Kerd. A consuming project may
already have CI and use its results as evidence. Neither makes CI a dependency
of using Kerd. Do not silently install it or replace it with mandatory local
gate scripts.

No custom hooks are required for the new process either. Use the execution
environment's existing tools and permissions. Do not build a hook framework
just to enforce every sentence in the process.

## A clear process, not a gate ladder

| Stage | What happens | What is captured |
|---|---|---|
| Understand | Recover relevant facts, guide the conversation, challenge assumptions and resolve important unknowns | Outcome, deliverables, success measures, boundaries and open questions |
| Shape | Analyse/design enough; show the parts and flow in a rendered product view; explain consequential choices | Direction, useful detail, risks, evidence approach, resources and authority |
| Agree | Show a concise, self-contained direction and ask for agreement before building | What was agreed, the user's actual response, and any conditions |
| Deliver | Prepare model-specific jobs, build, independently review, validate and improve | Current activity, decisions, outputs, findings, evidence and next action |
| Complete | Compare results with the original agreement and present deliverables and proof | What is met, not met or cannot be assessed; remaining limitations |

Stages help people understand the work. They are not a mandatory collection of
files or parser gates. Earlier questions establish consequential choices; a
small task need not spend five separate turns passing through five labels.
Meaningful uncertainty still gets resolved before action.

The journey must be visible, not merely present in instructions. At entry,
resume, stage changes and consequential questions, show where we are across
Understand → Shape → Agree → Deliver → Complete. Beneath that, identify the
current decision or active build/review job. Before a material decision,
summarise what the analysis established, the remaining uncertainty and the
recommended direction with its tradeoff. The question says which part of the
outcome it affects and what the answer enables. Keep routine updates short.

The product view explains what we are creating; the journey view locates the
person in the work. Use a sequence or comparison when it clarifies the actual
choice, not decorative panels in place of analysis. Link deeper evidence without
hiding material consequences there. After a response, Conductor records it and
acts: advances the conversation, investigates, updates the design or starts the
next authorized job. It does not require a new “okay” at every transition.

Fresh work starts with “What are you trying to achieve?” unless the request
is already supplied. Check only for active work before the opener. Relevant
repository discovery follows the intent. Resumed work returns to the recorded
question or next action instead of replaying the interview.

### Adaptive understanding — agreed 2026-09-08

~~Present the same ten questions for every project and confirm every topic.~~
Superseded by the user's agreement to the Codex intake review: retain
[ten internal coverage areas](../../../skills/conductor/references/understanding.md), but
ask only consequential gaps after reusing the request and relevant context.

Natural build/create/plan requests should make Conductor discoverable without a
special command; host selection and instruction precedence still apply. A quoted
trigger is not intent. Resume restores existing work. Small explicit authorized
changes run directly with proportionate verification; status/review/input stays
scoped. No installation or global trigger changes are implied by this design.

Conductor investigates available facts, proposes appropriate answers/checks and
asks when an unresolved answer changes the next action or prevents a consequential
mistake. The internal guide says when each area matters, when needed, what to do
if unknown and how to retain status/source. These are writing distinctions, not
a mandatory field register. No question-count quota or topic-completion meter.

Show “What we're building”: result, checks, boundaries, room to decide and open
issues. Keep actual requirements, preferences and delegated choices distinct.
Use relaxed, concrete language; keep the question and supported answer bounded.
A correction changes the affected understanding without restarting. “Help me
decide” invites a recommendation; “not sure” remains unresolved; “you decide”
doesn't grant unrelated authority. Known facts do not need repeated confirmation.

Before substantial execution, make new direction and meaningful choices clear
and agreed. Explicit unchanged authorization need not be confirmed again.
“Enough to start” applies to the next action: safe exploration can proceed while
a later decision remains open, but that decision blocks its affected action.
Old answers and dated interview records remain intact.

Success is established with the person, not inferred from a list of features or
tests. Recover criteria already supplied; otherwise ask what a successful result
would mean. Help make that observable, including what is good enough and how a
peer could assess it. Present the concise success-and-proof summary for agreement
as part of shaping the direction. Scope agreement alone does not approve proposed
measures. If the desired benefit cannot be assessed by the stopping point, explain
that and agree the available proof without pretending it establishes the benefit.

The conversation is a user interface, even in a CLI. Questions and agreement
requests appear in a fully bounded card containing the topic, question, answer,
short source/reason and **1. Correct / 2. Change**. The answer being confirmed
belongs inside the box, not in surrounding narration. Change starts a normal
conversation about the correction, not an inline editor. For a missing answer,
ask openly without these confirmation choices. Use a native card when available, otherwise a
four-sided text box in a monospace code block. A blockquote or bold heading alone
does not provide enough distinction. Default boxes to about 80 columns, adapting
to the available width and wrapping without truncation; no special UI dependency.
Longer optional explanation stays
outside; the complete card is the final actionable element. Progress leads with what is happening;
handoffs say what finished, what has not started and who acts next. Deeper detail
is available without burying a decision or hiding a material tradeoff.

The person sees a simple visual of what will exist and how the parts connect.
Analysis, architecture, prompts and evidence are available at greater depth.
Less visible detail must not hide a consequential tradeoff or an unproved claim.

The [local visual skill](../../../skills/visuals/SKILL.md) now codifies a lightweight
diagram-design adaptation for that job. See the [visual-tools assessment](visual-tools-assessment.md)
for its scope and the Archify evaluation. Both tools are retained choices:
Conductor selects what best explains the work, and the person may request either.
There is no rigid division of uses. Neither introduces another approval gate or
a global installation requirement.

## Who decides what

Conductor assesses necessary analysis and verification from consequence,
uncertainty, reversibility and scope. There is no compulsory Quick / Standard /
Deep menu, second rigor declaration or fixed mapping between job size and model
price. The person controls viewing depth, scope, authority and resources—not a
technical work classification.

The user agrees the direction before Build. Conductor can change methods,
tools, work order and reversible implementation details within that agreement.
It cannot silently change the desired experience, success measures, scope or
permissions. A meaningful proposed change is explained and agreed; spelling,
layout or equivalent wording changes do not trigger resealing or fresh approval.

Conductor answers questions from facts and the agreement, not invented user
preferences. It asks when it lacks a sound basis or a decision materially
affects quality, experience, outcome or guardrails. Routine progress updates
do not have to end with a question.

Completion under the original authority is not a new human approval. If the
work requires final human acceptance, agree that during understanding. Do not
impose it through a work-level label or manufacture it afterward.

## The model work loop

1. Select a useful next job from the agreed work, accounting for dependencies.
2. Assess its capability, context, tool and evidence needs; select an appropriate
   available model and effort. Do not underpower it merely to cut cost.
3. Prepare its prompt using relevant locally stored official guidance and
   examples. Include outcome, inputs, boundaries, success measures and expected
   result; leave method flexible where safe.
4. Execute. A peer or different model reviews the actual result against the
   original measures, including effects on related work.
5. Correct a specific failure or continue to the next job. Prove the integrated
   outcome as well as the individual pieces.

Conductor reads the [local model suitability guide](guidance/model-choice.md)
before a new selection: provider-described capabilities, actual execution tools
and comparable task results are different inputs. Consider permitted providers
on the same quality bar, explain the choice briefly, then use the chosen model's
prompt guidance. No brand-based staffing, fabricated capability scores or extra
user selection ceremony. Missing evidence stays explicit; the first real result
is assessed, not treated as proof that the selection is optimal.

Three materially different failed corrections of the same measure return the
problem to Conductor for reassessment. Switching workers does not reset history.
Resource limits cover the whole effort, including review and retries. Conductor
cannot increase a ceiling or weaken success silently.

Use bounded cross-model jobs, not open-ended discussion between agents. Record
the requested model/effort, separately observed identity, prompt, result and reviewer. Do not claim cross-model
review when the requested provider was unavailable. The existing
[examples](examples.md) and [local guidance](guidance/README.md) are inputs to
test, not proof of optimality. Keep source URLs, dates and model applicability;
no requirement fingerprint scheme is needed to use them.

## One readable work record

Keep each work package together in its project. A normal starting layout is
docs/work/<work-name>/work.md, with the drawing, deliverables and supporting
evidence beside it as needed. Reuse existing sensible locations. No empty folder
tree, global register or naming checker is required.

The record holds the agreed outcome, measures, scope, authority and resources;
what the person actually agreed; important decisions and changes; current work,
linked results, open issues and next action; and an evidenced completion summary.
Keep the earlier agreement distinguishable when changes occur.

Use simple labels to connect measures and jobs when helpful; do not require MSC
registration, reciprocal links, approval hashes or seals. If the project already
uses measurement records, reference them instead of creating duplicate facts.

The work view reads this record and its evidence links. It does not call the old
rung router or infer completion from filenames, checked boxes, commit trailers
or CI status. Reported activity is not proof of success. If the record disagrees
with actual artifacts, surface and correct the disagreement. Do not claim a
tamper-proof or independently enforced status system.

Switch keeps continuity with a pointer to active work and its exact resume
point. Conductor updates the work; Switch writes the session handoff. Do not
duplicate the plan across CONTEXT, TODO and logs. Preserve old logs and approvals
as history, not as current instructions.

The [candidate delivery connection and Switch slice](trials/integrated-delivery.md)
are now exercised in isolated projects. The candidate uses an existing handoff
location or a small docs/work/SESSION.md pointer, without restoring legacy mode
snapshots. Its [working-loop view](diagrams/working-loop.html) distinguishes the
implemented examples from broader, still-unproved product claims. This does not
change installed Kerd or silently adopt the rest of this proposal.

## What comes out

| Remove from the new Kerd usage process | Keep instead |
|---|---|
| Rung routing and artifact-presence gates | Understandable stages and evidence-backed progress |
| Seals, approval fingerprints and hash-triggered reapproval | Recorded agreement and review of meaningful changes |
| Mandatory register, risk-table, rigor and question-set schemas | Clear measures, relevant risk assessment and adaptive questions |
| Pieces/Verify score as permission to build; trailers as proof of completion | Changeable work plans and independently reviewed results |
| CI workflow requirements, staleness and fidelity refusers as usage prerequisites | Suitable project evidence and reliable saved progress |
| Custom hooks as a dependency or a new enforcement project | Existing host permissions, clear limits and honest capability disclosure |
| Mandatory composer, fixed model tiers and per-step approval | Appropriate model jobs within one agreed direction |
| Drive's separate orchestration loop | Conductor owns work; Switch owns continuity |

This is removal, not disabling checks while leaving hidden prerequisites.
Do not recreate them as a “readiness engine,” another schema or local preflight
scripts. Necessary checks of the actual deliverable remain.

## The tradeoff, openly

We give up automatic detection of some missing paperwork and byte-level changes.
A readable agreement and model review can miss a change; they are not a seal or
security boundary. Independent review can also be wrong. Specific tests, source
evidence, realistic demonstrations and existing permission controls provide
confidence appropriate to the task—not a guarantee of infallibility.

Removing machinery does not authorize unsafe operations or relaxed outcomes.
If the host cannot safely support an operation, explain that specific limitation
and narrow or pause it. Do not turn the gap into a universal infrastructure
requirement.

The old Drive rule that Conductor must not change, outside-model rung enforcement
and producer-only acceptance conflict with this direction. Replace their living
instructions explicitly at adoption; do not rewrite dated decisions or reinterpret
prior approvals. The same applies to the old measurement design's producer-only
comparison and elaborate freeze/record machinery: reuse useful measures, not its
mandatory protocol.

## First proof

Use the real session-routing request in an isolated ordinary clone. Demonstrate
the opening conversation, rendered direction, recorded agreement and reliable
resume. No execution loop or legacy record migration is needed for that slice.

Then connect prepared model jobs and independent outcome review, and continue
the session-routing and Wholematter trials. Report actual usability, outcomes,
elapsed time and available resource data. No superiority claim over a baseline
never run. Learning enough for the next Kerd decision does not make an unfinished
trial complete.
