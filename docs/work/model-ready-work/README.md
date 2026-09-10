# Model-ready work

## Current direction: strong process, lightweight records

> **Where the three skills live.** Conductor, Switch and Visuals ship from the
> repository's own [`skills/`](../../../skills) as of v0.107.0, which is the single
> maintained source; `packaging/build.py` consumes it. The candidate copy that used
> to sit beside this file is gone — dated records and trial notes below still cite
> those paths, and they resolve in Git history at `716a099`, per the standing rule
> that living surfaces are updated and dated records stand.


The next proposal reworks Conductor inside Kerd and removes complex rung gates,
seals, requirement fingerprints and elaborate approval schemes. No CI or custom
hook setup is required to use any Kerd skill. Keep guided stages, recorded user
agreement, appropriate model jobs, independent review and reliable resume.

Start with these three connected views of the same work:

1. [The process drawing: what stays and how work flows](diagrams/kerd-conductor-rework.html).
2. [The proposal and design: keep, rework, remove](kerd-conductor-rework.md).
3. [The implementation sequence and proof](conductor-rework-spec.md).

**Start here:** [use the current candidate](candidate-entry.md).
It loads the maintained skills directly from this pack; no plugin install or
separate clone is required. [Current consolidation and remaining proof](consolidation.md)
separates ready-to-try behaviour from adoption work.
Explore [the complete solution map](diagrams/solution-map.html): every candidate
command, its read/write flow, actual questions, information homes and unresolved
adoption gaps. It describes current behavior; proposed fixes are marked separately.
See [the working delivery loop](diagrams/working-loop.html).

Current intake: ten internal coverage areas, not ten questions to answer. Natural
work requests use context, supported suggestions and consequential clarifications;
clear small changes proceed directly. [Adaptive understanding](../../../skills/conductor/references/understanding.md)
and the solution map supersede earlier mandatory topic-count examples.

Visuals are now codified in the [candidate visual skill](../../../skills/visuals/SKILL.md).
See the [diagram-design / Archify assessment and examples](visual-tools-assessment.md).
Both are retained choices: Conductor selects for the work, the person may request
either, and one package may use both without a rigid division of uses.

The [guided candidate](trials/conductor-first-slice.md) now covers the whole
journey in its instructions: understanding, visual direction, agreement,
authorized delivery, independent assessment and saved resume. The first trial
exposed an unconditional planning-only stop and insufficient visible guidance;
those instructions were corrected. The subsequent Wholematter run completed a
real work package, but the user's feedback exposed a weak conversation experience.
See [how the journey should appear](../../../skills/conductor/references/journey.md).
The [experience refresh](experience-refresh.md) responds to the completed
Wholematter trial: a clearer working view and answer panel, earlier visuals, and
real work/answer feedback. Completed output did not prove good conversation UX.
That note also parks a future spoken companion: a natural interview alongside
the CLI and visuals, sharing the same saved work. Voice is not current build scope.

The accepted session connection now travels with the candidate. A clean-project
exercise produced a [real user guide through Claude drafting and Codex review](trials/integrated-delivery/using-model-help.md).
The [connected-loop implementation and evidence](trials/integrated-delivery.md)
also records portable-runner tests and the candidate Switch save/pickup check.
These are bounded component/behavior observations, not full Kerd adoption.
The [next behavior pass](trials/experience-checks.md) exercised fresh start,
agreement-to-action, interrupted reassessment, existing project locations and
standalone reviews. It produced two small routing/presentation corrections;
the subsequent real-person Wholematter run is discussed in the experience refresh.
Whether the refreshed interface feels better remains unproved.

Current delivery work: [Switch In / Out / To / Roll](trials/switch-redesign/direction.html).
The [active Studio → laptop trial](trials/switch-redesign/device-build/results.md)
now includes the returned patch, a focused Markdown correction, 33 current tests,
19 original tests and independent review. Source release was observed on Studio;
laptop execution is reported in the user's transcript; the returned artifact was
directly tested on Studio. The user opened the destination and returned the result.
The
[Conductor + Roll integration trial](trials/switch-redesign/conductor-roll-proof.md)
adds observed Codex context usage and a reviewed readable status tool; its proof
separates automatic continuation from manually assisted recovery and keeps the
remaining source-exit and context-budget gaps visible.
The [live-controller connection trial](trials/switch-redesign/live-control/results.md)
now connects Conductor to its actual running worker: request a checkpoint, recover
a failed save through the same channel, release the source, then continue in a fresh
local destination without another user turn. The result has 19 passing tests;
remote destination startup and arbitrary interactive-host exit remain outside that proof.

These are not changes to installed Kerd behavior. They supersede both
the standalone-first plan and the later plan to extend Kerd's gate machinery.
Supporting documents below contain earlier designs, including retired work-level
menus, fingerprints and schema checks; those mechanisms are not current build
requirements. Prior trial results do not prove this redesign is implemented.

This is the complete proposal for helping each model do its best work without
making people learn prompt engineering.

The idea in one sentence:

> A person describes the outcome and the proof; Conductor prepares the right
> brief for the chosen model; the model chooses how to do the work; the result
> is judged against the original outcome.

## Supporting material

1. Open the [complete process drawing](diagrams/model-ready-work.html).
2. Open the [guided experience and viewing-depth drawing](diagrams/guided-experience.html).
3. Read the [guided-interview decisions](guided-interview-decisions.md) for the
   agreed Conductor boundary and autonomous build loop.
4. Open the [MVP trial pack](trials/README.md) for the two approved real-work
   trials and their shared proof.
5. Read the [earlier product vision](product-vision.md) for experience and
   cross-model rationale; its named work-level menu is superseded.
6. Read the [proposal](proposal.md) for the purpose, boundaries, risks, and
   adoption decision.
7. Read the [design](design.md) for the full product and process behavior.
8. Read [capturing requirements and features](requirements-and-features.md) for
   build briefs, feature briefs, dependencies, slices, and roll-up measures.
9. Read [making it easy, fast, and excellent](easy-fast-excellent.md) for the
   working journey to validate: readiness, context, execution, review, and recovery.
10. Read the [example briefs](examples.md) to see how the same requirement is
   prepared for Claude and OpenAI model types.
11. Read the [earlier implementation specification](implementation-spec.md) for
   historical prototype context; use the current sequence above for new work.
12. Read the [launch story](launch-story.md), [failure story](failure-story.md),
    and [stress-test findings](stress-test-findings.md).
13. Review the [end-to-end Standard example](end-to-end-example.md).
14. Use the [independent review job](review-brief.md).
15. Explore the local [draft website](website/).
16. Run the isolated [working demonstration](mvp/README.md).

Everything for this body of work lives below this directory. Nothing here
changes live Conductor behavior yet.

## Honest implementation boundary

The maintained candidate consists of Conductor, Visuals and Switch, with local
guidance and the model connection. The deterministic prompt prototype and its
20-test diagnostic run are historical experiments, not the runtime Conductor.

Prepared Claude/Codex contributions, independent review, supported corrections,
saved pickup, managed Roll and a bounded cross-device task continuation have real
evidence. A prepared local pickup met the agreed context targets using estimated
added usage and a restoration review; the laptop handoff's cost was not measured.
See [Switch's current evidence and qualifications](trials/switch-redesign/work.md).

Still unfinished: real-person validation of the refreshed full conversation,
broader legacy-skill migration and deliberate live adoption. No general speed,
cost, optimal-prompt or universal memory-preservation claim follows from these
component trials. Remote session startup and arbitrary interactive-session
takeover are not implemented; native conversations do not move through Git.

Older
proposed readiness engines, fingerprint checks and full evaluation frameworks
are not prerequisites to build. Prototype commands do not implement this process.

## The process in plain language

```text
Person describes the work in ordinary language
          |
          v
Conductor interviews, challenges, retrieves known facts, and shapes the direction
          |
          v
Person approves one visual view of the outcome, parts, flow, measures, guardrails,
authority, resources, and completion point
          |
          v
Conductor runs the autonomous build loop
          |
          v
Build -> peer review -> prove -> improve
          |
          v
After three materially different failed attempts on the same measure,
Conductor changes the route or returns one consequential decision
          |
          v
Every agreed measure passes through independent evidence
          |
          v
Conductor completes at the stopping point agreed before Build
```

## Capturing one requirement or many features

A single task starts as a **work brief**. A larger product starts as a **build
brief**, with one **feature brief** per independently testable capability. A
feature map records dependencies and readiness. Conductor sends only one ready
feature or one coherent slice into the execution loop, not the whole backlog.

The complete format and selection rules are in
[Capturing requirements and features](requirements-and-features.md).

## What a person must provide for one execution

The input is a **work brief**. It asks only for product-level facts:

- Outcome: what should be different when the work is done?
- Deliverable: what must exist afterward?
- Success measures: what observable result counts as success?
- Proof: what will let another person verify those measures?
- Context: what information is needed?
- Boundaries: what must not change or happen?
- Decision rights: what may the model decide, and what remains yours?
- Open questions: what must be discovered rather than guessed?
- Done condition: when should the model stop?

The person does **not** need to choose XML, prompt layout, reasoning language,
or a provider-specific technique. That is Conductor's job.

## Everyday words used here

| We say | It means | Technical implementation term |
|---|---|---|
| Work brief | The stable description of the job and its proof | task envelope |
| Model guidance | Local, versioned advice for preparing a brief for one model family | adapter/profile |
| Prepare the brief | Turn the work brief into the clearest form for the chosen model | compile/render |
| Brief review | Check that the prepared job preserves the relevant agreement | no manifest required |
| Results review | Judge the output without favoring the model or prompt that produced it | blind adjudication |
| Guidance test | Remove or change one instruction and see whether results improve | clause ablation |

Technical terms appear only where an implementer needs them. Product decisions
and normal use rely on the plain-language terms.

## Product rules

1. The work brief stays the same across models.
2. The model-specific presentation may change; the requested outcome may not.
3. The model owns the method unless order is part of correctness or safety.
4. Choose useful verification for the work; do not require CI, hooks or gate
   infrastructure to use Kerd.
5. Official guidance earns a trial, not permanent status.
6. A model-specific instruction stays only when results or an unavoidable
   safety boundary justify it.
7. Shorter is useful only when the result remains as good or better.
8. The process never claims success unless the declared proof supports it.
9. People interact with conversational intake and plain-language reports, not
   schemas or raw prompts.
10. Conductor chooses appropriate model/effort and analysis depth. Efficiency
    never makes an unsuitable model acceptable for the job.
11. A failed run changes only the layer that failed; it does not automatically
    make every future prompt longer.

## Current proof status

The isolated demonstration validates the work brief, prepares deterministic
Claude- and OpenAI-shaped briefs, and checks that every required field survives.
Its self-test currently covers 20 cases. One real matched diagnostic run also
exists: the OpenAI condition met all frozen measures and the Claude condition
missed one evidence detail. That single run proves the measurement path works;
it does not establish a general model ranking or justify changing Conductor.
