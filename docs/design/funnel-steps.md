# The steps inside each stage

The funnel has eight **stages**. Each stage has **steps** — the numbered work
you actually go through inside it. The entry gates check a stage's *outputs*;
this file defines its *work*. Until 2026-08-07 only the outputs existed, which
is why a journey page could show what a stage produced and never what it
involved.

Vocabulary, settled 2026-08-07 (Tony: *"actually it's a funnel not a ladder
right? funnel with stages and steps in each stage"*). The machine still says
`rung` in `gate.py`, its JSON and CI; renaming those is a cross-cutting sweep
queued as its own item, and the page translates — exactly as it already
translates `frame` to "Idea".

**This file defines steps, never their status.** A definition is the same for
every work item; status is per item. Where a work item declares nothing, its
page shows the step with no status rather than inventing one — the same rule
as everywhere else here: an honest blank beats a plausible claim.

**Provenance.** Six of the eight stages are harvested from flows already drawn
and agreed (`tools/diagram/gen_flow_*.py`), where this content had been sitting
inside diagram-drawing code rather than written as steps. Idea is Tony's, from
his mockup of the journey page, 2026-08-07. **Live is the one stage with no
source at all** and is left empty rather than guessed.

## Idea

*Tony's, 2026-08-07. No flow was ever drawn for this stage.*

1. Capture the idea or problem — from the prompt input, as typed
2. Gather what supports it — comparable documents, diagrams, references, prior experience, sites, images
3. Interview in rapid Q&A — one question at a time, on purpose, constraints and success criteria
4. Visualise the idea — a diagram or HTML, iterated in a paired session

## Validated

*From the viability flow.*

1. Sort what is already on the table — unmitigated, unqualified, accepted unknown
2. Estimate cheaply whether any one of them could be fatal
3. Qualify with evidence — a test or an analysis; measured, not asserted
4. Ask of each: is there a countermeasure? A risk without one is a blocker
5. Acceptance — two keys, neither sufficient alone

## Scoped

*From the slice flow.*

1. Work out what actually decides the grouping — dependency, comprehension, effort, risk, opportunity
2. State the grouping — what is in, what is deferred
3. Walk the upstream declarations for every item claimed done
4. Check that every done item points at a declaration that exists
5. Acceptance — two keys

## Designed

*From the design flow.*

1. Read before proposing anything — the grounding, the standing decisions, the living design docs it touches
2. Generate at least two approaches, then choose between them
3. Produce one package — specs, architecture, testing strategy, and the diagrams for as many aspects as possible
4. GO — two keys, neither sufficient alone: every aspect drawn and nothing left to annotate, and every declared measurement given a named answer

## Spec'd

*From the contract flow.*

1. Receive the GO'd design package intact — never a digest of it
2. Read before writing the order
3. Write the order so a stranger could build from it
4. Size and assign each piece — after it is written, never before
5. Approval by machine key alone — no human gate where the machine can measure

## Built

*From the build flow, steps 1-3.*

1. Take one piece of the work order
2. Build it and measure it against every relevant spec — its own criteria plus everything the change touches
3. Decide: the piece is done, or it is the overseer's problem

## Proven

*From the build flow, steps 4-6.*

1. Cold eyes on the whole change, reviewed unanchored
2. Check conformance per declared layer — never one overall verdict
3. The expert-user pass — the human uses the output itself

## Live

*No flow was ever drawn for this stage, and no steps are defined. Left empty
deliberately rather than invented.*
