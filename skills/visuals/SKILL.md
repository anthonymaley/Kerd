---
name: visuals
description: Create readable product, process and system diagrams that help a person understand or agree a direction. Use whenever the person asks to see something, and whenever a proposal carries two or more connected parts, a branch, an ownership boundary or a before → after change — connected-parts views, responsibility flows, scope boundaries and decision paths. Draw with diagram-design or Archify, which are required: produce a saved, rendered view, never hand-rolled ASCII in a code fence or a document made of text boxes.
license: MIT
---

# Visuals

**Asking the person:** every question is one speech-bubble line, the last prose line of the message, `> 💬 **The question?**`, with any options, context or proposed answer listed above it, never inside it; where the host offers one, a native picker may follow the bubble carrying those same options and always leaving a free-form answer open, never replacing or preceding it — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Putting a decision to the person:** a consequential question — its answer commits to work, spends real effort, releases or deletes something, or reverses a ruling — comes after a decision block: Problem, Facts (with how we know the problem is real and how strong that evidence is), Known options (or “needs study”), Recommendation, Why, Cost, What we lose, Input (who else checked it, or nobody yet). Its bubble is the Recommendation sentence ending “— approve?”, every operation included, or one genuine question the recommendation depends on; never a smaller or softer question than the real decision, and never without the block. A factual question or a small, easily undone step stays one line — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

**Showing the person:** when they ask to see something, and whenever a proposal carries two or more connected parts, a branch, an ownership boundary or a before → after change, the answer carries a saved, rendered view drawn with diagram-design or Archify — never hand-rolled ASCII in a code fence, never an offer question, no quota; only a single action or a factual answer stays text, and being easy to describe in words does not make it one — see [showing the work](../conductor/references/journey.md#visuals-belong-throughout).

A lightweight Kerd adaptation of Cathryn Lavery's diagram-design. See
[sources and adaptation](references/sources.md). No CI, hooks, seals, branding
onboarding or diagram approval schema is required.

## Draw the relationship the person needs to understand

Use during understanding as well as design, delivery and final review. An early
before/after view, audience map or scope boundary can clarify a question before
the full direction exists. Label partial/proposed content; do not infer missing
requirements to complete a picture. Inline prose, a list or a table supplements
the rendered artifact; it never stands in for one, and spatial detail being easy
to describe in words is not a reason to skip the view. No visual quota per topic.

Use the current work agreement and conversation. Identify the question the
picture must answer, then read the matching section of
[the local pattern guide](references/patterns.md) before drawing. Do not ask the
person to choose a diagram type or repeat facts already supplied.

Start at product level: people, capabilities, work and outcomes. Technical
architecture is a deeper view when useful, not the default vocabulary. Symbols,
file names, line numbers, and type or protocol names belong in a subordinate
evidence layer, never in the main relationship. The invariant, for every view:
remove every code reference, and the main relationship must still be
understandable to a reader who has not opened the source. A solution, proposal
or correction view carries more — stripped of those references it must still
show what the person can and cannot do today, where the responsibility sits,
what changes, and any material cost or boundary that exists. Content decides
which applies, never the title or diagram type: any view that depicts or
recommends a change takes the fuller test, and only a view limited to present
facts uses the invariant alone. If
removing them leaves the view unreadable, it was drawn at the wrong level. A
deliberately technical deep-dive may use engineering vocabulary throughout,
provided its title and summary still pass that removal test. A box
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
the actual subject, and name the project, product or repository inside the
render itself — in the title or a small identity label. A filename, browser
tab, surrounding message or filesystem path sits outside the picture and does
not satisfy this, because the view travels without them; where more than one
name could apply, the repository name is the floor. The untouched bundled
starter asset is the sole exception; a rendered view produced from it is not. Do not rely on colour alone. Reflow or split a wide
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

For Kerd's rendered views, diagram-design and Archify are required, not one
option among several: a view goes through one of them. Choose the tool that best
explains this work; honor the person's preference. Diagram-design carries broad
static layouts — processes, timelines, responsibilities, scope, comparisons;
Archify carries exploration, focused paths and comparing changes. These are
tendencies, not a rigid technical/nontechnical split. Either can support user
agreement, and a work package may use both when each view adds something. Do not
ask the person to select a tool before understanding the outcome. The starter
patterns bundled here do not satisfy the rule on their own — they are neither the
full diagram-design catalogue nor a substitute for it; they help choose the view,
and the view itself is drawn with one of the two required tools. Disclose
unavailable capabilities; do not silently substitute or start a preview server.

## When a required tool is not available here

Keeping one of the two tools working is part of the job, not an extra. The source
record still distinguishes this bundled diagram-design adaptation from the full
upstream catalogue and from Archify's own runtime.

If a required tool is missing on this host, or the second one would materially
improve the view, set it up: name the benefit, source, install location and any
dependencies, network use or preview service. Use current upstream instructions
and the host's supported installer. Installing anything still needs approval
unless existing authority explicitly covers that installation; ordinary diagram
approval does not. Once setup is approved, perform it and verify the tool can
produce a usable view. Continue the original diagram task without
another routine “shall I install?” turn. The offer is to do the work, not hand
the person a list of commands. Report any genuine access or host limitation.
If setup is declined or blocked, fall back to the other required tool; if neither
can run here, say plainly that the view is not rendered and what that costs,
rather than substituting a hand-drawn picture. Do not repeat an install question
when the tool is already available. Record the selected tool/version beside the
work only when it matters for reproduction.
