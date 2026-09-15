---
name: visuals
description: Create readable product, process and system diagrams that help a person understand or agree a direction. Use for connected-parts views, responsibility flows, scope boundaries and decision paths. Produce an actual rendered view, not a document made of text boxes.
license: MIT
---

# Visuals

**Asking the person:** every question is one speech-bubble line at the end of the message, `> 💬 **The question?**`, with any options, context or proposed answer listed above it, never inside it — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

A lightweight Kerd adaptation of Cathryn Lavery's diagram-design. See
[sources and adaptation](references/sources.md). No CI, hooks, seals, branding
onboarding or diagram approval schema is required.

## Draw the relationship the person needs to understand

Use during understanding as well as design, delivery and final review. An early
before/after sketch, audience map or scope boundary can clarify a question before
the full direction exists. Label partial/proposed content; do not infer missing
requirements to complete a picture. A small inline relationship can be enough;
use a rendered artifact when spatial detail warrants it. No visual quota per topic.

Use the current work agreement and conversation. Identify the question the
picture must answer, then read the matching section of
[the local pattern guide](references/patterns.md) before drawing. Do not ask the
person to choose a diagram type or repeat facts already supplied.

Start at product level: people, capabilities, work and outcomes. Technical
architecture is a deeper view when useful, not the default vocabulary. A box
means a component, action or boundary; containment means inclusion; an arrow
means a particular flow or relationship. Paragraphs in panels are not a diagram.

Show one useful main relationship. Group details or make an additional view
when needed; never delete a meaningful constraint just to meet a node quota.
Name what was simplified if it could affect the user's decision. Distinguish
existing facts from proposed behavior and unresolved choices.

## Make it directly usable

Default to one self-contained HTML file with inline SVG/CSS and system fonts,
saved with the work. Start from [the worked flow](assets/review-flow.html) for
an appropriate flowchart, replacing its facts rather than inheriting them.
Use the same visual style for related views; use known project branding when
available without an extra setup conversation. Static first; add interaction
only when it helps explain the work.

Use clear grouping, restrained emphasis and readable labels. Prefer simple
horizontal/vertical connections with clear endpoints; route around unrelated
nodes. Avoid line/label collisions. Make the title and SVG description explain
the actual subject, and do not rely on colour alone. Reflow or split a wide
diagram for narrow screens instead of shrinking its text into illegibility.

Render and inspect the actual output at the intended viewing size. If it is
likely to be opened on a phone, check that too. Use an available browser or
image-capable preview; do not require a specific test framework. If inspection
is unavailable, disclose that limitation instead of claiming visual validation.
Check meaning as well as layout: source facts, arrow direction, ownership and
the visible distinction between proposed and delivered work.

## Help the decision; do not invent another gate

Show the rendered artifact with a short explanation of what it clarifies. When
Conductor needs agreement, its question includes the outcome, boundaries and
meaningful tradeoffs—not “approve this diagram” without context. The user's
actual agreement belongs in the work record, not in a seal or fingerprint.

Offer deeper detail without forcing the person to read it. Do not pause for
routine colour, layout, type or export choices. If the drawing exposes an
important unresolved product decision, ask that decision rather than guessing.

Keep diagram-design and Archify as complementary choices. Choose the available
tool that best explains this work; honor the person's preference. Diagram-design
offers broad static layouts; Archify can help with exploration, focused paths
and comparisons. These are tendencies, not a rigid technical/nontechnical split.
Either can support user agreement, and a work package may use both when each
view adds something. Do not ask the person to select a tool before understanding
the outcome. This local adaptation contains starter patterns, not the full
diagram-design catalogue or an installed Archify runtime. Disclose unavailable
capabilities; do not silently substitute, install tools or start a preview server.

## When an optional tool would help

Built-in diagrams need no additional diagram skill installation. The source
record distinguishes this bundled diagram-design adaptation from the full
upstream catalogue and optional Archify. Do not present either extra as required.

If the person requests an unavailable tool, or it would materially improve the
view, offer to set it up: name the benefit, source, install location and any
dependencies, network use or preview service. Use current upstream instructions
and the host's supported installer. Obtain approval unless existing authority
explicitly covers that installation; ordinary diagram approval does not.
Once setup is approved, perform it and verify the tool can produce a usable view.
Continue the original diagram task without
another routine “shall I install?” turn. The offer is to do the work, not hand
the person a list of commands. Report any genuine access or host limitation.
If setup is declined or blocked, offer the built-in view and disclose any lost capability.
Do not repeat an install question when the tool is already available. Record
the selected tool/version beside the work only when it matters for reproduction.
