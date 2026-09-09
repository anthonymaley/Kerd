# Guided-interview decisions

This record captures the product decisions reached through the first live guided
interview. It is part of the working design, not evidence that the experience has
yet been implemented or validated.

## Later direction: simplify the machinery

The user has since clarified that the staged guidance, capture, validation and
user agreement remain important, but complex rung gates, seals, requirement
fingerprints and elaborate schemes should be removed. CI is not required for
any Kerd usage, and custom hook setup is not a dependency. Conductor assesses
necessary depth; the user does not choose a compulsory work-level menu.

The current [proposal](kerd-conductor-rework.md) and
[spec](conductor-rework-spec.md) replace the previous machinery-preserving
integration plan. The earlier interview below records how the idea developed;
it does not restore superseded mechanisms. No live skill has changed yet.

## The product in one view

```text
Any kind of repository-based work
               |
               v
UNDERSTAND — learn the outcome, why it matters, and what is already known
               |
               v
SHAPE — design and analyse enough to define the parts, flow, measures,
        guardrails, authority, resources, and completion point
               |
               v
PERSON APPROVES ONE VISUAL DIRECTION
               |
               v
BUILD <-> PEER REVIEW <-> PROVE <-> IMPROVE
               |
               v
Every agreed measure independently passes
               |
               v
CONDUCTOR COMPLETES THE REQUESTED WORK
```

## The Kerd family

Kerd remains the project system. Its repository may contain software or any
other durable work: product strategy, research, executive decisions, operating
processes, project plans, communications, designs, launch material, evidence,
or software.

```text
KERD PROJECT REPOSITORY
|
+-- Switch
|   Keeps project and session continuity across people, models, and sittings.
|
+-- Conductor
    Understands, shapes, builds, reviews, proves, and completes the work.
    It may call models, tools, and existing specialist skills as bounded jobs.
```

Building, reviewing, proving, and improving are Conductor responsibilities, not
new Kerd skills. A Review, Evidence, or Release skill must not be invented merely
to mirror a phase. A specialist skill is justified only after repeated work
shows that it needs a stable contract and lifecycle of its own.

## Before Build

Entry correction from the live trial: a new process opens with “What would you
like to make happen?” An invocation that already contains the outcome supplies
that answer. Only then does Conductor select and read relevant project context.
An active process instead resumes its exact saved question or next action.
Minimal continuity detection comes first; a prewritten task or repository
backlog cannot substitute for the person's initial intent.

The guided interview asks one useful question at a time. It retrieves answers
already present in the repository, challenges unsafe or contradictory requests,
and labels its assumptions. It stops when another answer would not materially
change the work.

The approval view must show, in ordinary language:

- what will exist when the work is complete;
- the non-technical and technical parts and how they connect or flow;
- the intended experience and outcome;
- success measures and the evidence that can prove them;
- scope, exclusions, guardrails, authority, and consequential decisions;
- assumptions and unresolved uncertainty;
- time and resources as declared constraints, goals, or visible derived bounds;
- the point at which Conductor will stop.

This approval fixes the direction, not the implementation route.

Approval records refer to the exact displayed direction and its content hash.
A changed version requires renewed approval. The controller checks consistency;
the host supplies the actual conversation reference. This is not independent
authentication of the person or a restriction on arbitrary filesystem access.

## The autonomous loop

After approval, Conductor continues without routine user input. It may change
the implementation approach, work order, internal structure, tools, model
assignments, and reversible details inside the approved guardrails. It may not
silently change the experience, outcome, scope, measures, guardrails, external
commitments, or irreversible decisions.

The builder does not grade itself. A peer or different model reviews each
measure against the original direction and admissible evidence. A failure
returns to Build. Three materially different failed correction attempts against
the same unresolved measure return control to Conductor; they are not three
rewordings of the same retry. Conductor may change the route, work breakdown,
model, effort, reviewer, or evidence method. It asks the person only when the
approved direction can no longer be honoured safely.

## Completion and external action

The requested stopping point is part of Shape. It may be finished artifacts,
a release-ready package the person will publish, or an externally delivered and
verified result. Publishing is simply work when it is named in the approved
request with sufficient authority. Conductor does not need a separate Release
skill, and it must not infer broad external authority from an ambiguous word
such as “launch.”

## What remains to prove

- That the interview obtains enough clarity without becoming a questionnaire.
- That the visual direction is sufficient for approval across work domains.
- That users understand the boundary between direction and implementation.
- That three materially different attempts are a useful recovery bound.
- That peer-model review improves outcomes enough to justify its cost.
- That the same repository-centred process succeeds on software and
  non-software work.

## Approved live-work view

During autonomous work the default view shows what Conductor is creating, the
work happening now, completed outcomes, the next expected action, overall
health, whether the person is needed, and time and resources against the
approved direction.

Prepared prompts, model jobs, decisions, evidence, and history remain available
at deeper levels. The default view cannot hide a blocker, weak proof, changed
guardrail, material loss, or decision that needs the person.

## Approved routing and resource rules

The person approves cross-model authority once during Shape. The authority names
allowed providers, job types, repository and data boundaries, resource bounds,
external-action limits, and escalation conditions. Conductor may then dispatch
inside those limits without interrupting the autonomous loop. A person may also
direct a job in ordinary language, such as “ask Codex to review this,” without
knowing a session ID.

Model selection never uses low price as permission to underpower a job. Conductor
first establishes which models and effort levels are capable enough. It may
choose the most efficient proven option inside that eligible set. If a lower
budget requires a lower work level, narrower scope, or weaker stopping point,
the resulting loss is shown and belongs to the person's approval.

## Compatibility decision before live adoption

Live Kerd currently records a different division: Drive owns the work item from
idea through acceptance, while Conductor owns the session. This proposal gives
Conductor the guided work loop and leaves Switch with continuity. The isolated
trials may test that proposal without changing live behavior. Adoption may not
silently leave both contracts standing; it must explicitly supersede, rename,
or reconcile Drive's ownership after the trials supply evidence.

## Approved MVP trials

Two real-work trials will run in disposable repositories. Live Kerd stays frozen.
The trials move quickly and stop when they have produced enough evidence to
develop Kerd responsibly; valuable follow-on work remains available afterward.

1. A working multi-model session-routing prototype.
2. A launch-ready Wholematter DDIL Outcomes offering package.

Their complete contracts are in [the trial pack](trials/README.md).
