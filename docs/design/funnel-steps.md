# The steps inside each stage

The funnel has eight **stages**. Each stage has **steps** — the numbered work
you actually work through inside it. The entry gates check a stage's *outputs*;
this file defines its *work*. Until 2026-08-07 only the outputs existed, which
is why the journey page could show what a stage produced and never what it
involved.

**Status is per step**, one of: `open` · `in progress` · `not started` ·
`done`. The journey page renders these.

**Not yet defined is the honest state for most of this file.** Tony,
2026-08-07: *"yes we need our own version of this, for each stage and each step —
why don't we do that after this journey."* Idea is seeded from
his mockup of the page; the remaining seven are deliberately empty and render
as open slots rather than being invented here.

Vocabulary, settled 2026-08-07 (Tony: "actually it's a funnel not a ladder
right? funnel with stages and steps in each stage"): the **funnel** holds
eight **stages**, each stage holds numbered **steps**. Before this, "rung"
was doing both jobs — the machine's name for a stage, and the mockup's name
for a step inside one. The machine still says `rung` in `gate.py`, its JSON
and CI; renaming those is a cross-cutting sweep queued as its own item, and
the page translates, exactly as it already translates `frame` to "Idea".

Five stages already have a drawn flow in `tools/diagram/` (viability, slice,
design, contract, build) whose content is the raw material for their rungs —
it is trapped in diagram-drawing code rather than written as steps. frame,
goal and loop have no flow at all.

## Idea

1. `open` — CAPTURE THE IDEA/PROBLEM: do so from the prompt input as typed
2. `open` — Supporting or comparable documents, diagrams, references, experience inputs, sites, images
3. `in progress` — Perform interview in rapid Q&A style to capture the requirement — one at a time, on purpose / constraints / success criteria
4. `not started` — Visualize the idea, diagram or HTML, and iterate in a paired session with the user

## Validated

## Scoped

## Designed

## Spec'd

## Built

## Proven

## Live
