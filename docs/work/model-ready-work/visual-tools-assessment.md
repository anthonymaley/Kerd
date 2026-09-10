# Visual tools: keep both, choose for the work

## Agreed direction

Keep diagram-design and Archify as complementary choices. Conductor chooses
what best explains the work; the person can request either, and a work package
may use both. No tool-selection question is required before understanding the
outcome, and neither tool becomes a universal Kerd dependency.

Diagram-design's broad range suits processes, journeys, responsibilities, scope,
comparisons and other static views. Archify suits exploration where following
paths, focusing on parts or comparing changes helps understanding. These are
useful tendencies, not restrictions by domain, stage or audience. Either can
support a direction-agreement conversation.

This user decision replaces the initial recommendation to reserve Archify for
later technical views. The test observations below remain unchanged. The
[local visual skill](../../../skills/visuals/SKILL.md) remains a curated diagram-design
adaptation, not a complete installation of either upstream package.

Both can help explain a proposal. Neither records or proves that the user agrees
with it. That remains a conversation and a readable work record.

## 1. Diagram-design: now codified

Kerd already had a [spike finding](../../design/diagram-toolkit-spike-findings.md)
and a [type map](../../design/diagram-types-by-rung.md), but no shipped integration.
The strongest lesson remains: choose a layout that conveys a relationship;
paragraphs in rectangles are not enough.

The candidate skill now has a short entrypoint, local pattern guidance, a worked
HTML/SVG example, source attribution and MIT license. It is linked from the new
Conductor spec at the moment the direction visual is prepared. It is ready to
load explicitly for a trial, not globally installed or registered as a live
Kerd command.

This is a curated adaptation, not all 39 upstream types. It retains semantic
grouping, clear connectors, restrained emphasis, progressive detail, accessibility
and rendered inspection. It deliberately omits upstream's first-use brand gate,
pre-drawing confirmation, mandatory lint ritual and external fonts. The skill-
creator guidance informed the short core and on-demand local references.

[Open the worked example](../../../skills/visuals/assets/review-flow.html).
It shows a proposed review request and return, not the whole session-routing
design or a demonstrated transport. Browser inspection at 1440px and 390px found
readable labels and no horizontal overflow; the detail disclosure works and the
dark presentation was also inspected. Skill-format validation passed. These
checks do not substitute for a real user's assessment of the direction.

Source: [diagram-design](https://github.com/cathrynlavery/diagram-design/tree/4451eadc484d76aa860edf3289c16fcd082dcdbf),
commit 4451eadc, skill metadata 2.6, MIT.

## 2. Archify: interactive option, with observed limitations

Archify generates interactive HTML/SVG from structured diagram descriptions.
Its five modes cover architecture, workflow, sequence, data flow and lifecycle.
Focused views, paths and before/after comparison could help someone inspect a
complicated proposal without seeing all details at once. These are renderer
capabilities—not a guided requirements interview or approval system.

The runtime requires Node 18 or newer; the basic rendering path needed no npm
installation in this test. Browser inspection additionally needs a suitable
browser. Its update reminder can make a network request; I disabled that check
and did not install anything globally. This is substantially more tool machinery
than the default visual guide, even though the person need not author its JSON.

The internal format is not inherently a problem. Renderer layout checks are
different from imposing business-process gates on Kerd users. The question is
whether the authoring overhead and viewer controls earn their place for the
particular picture.

### What I actually tested

Authored a four-node, three-role review-request flow with two focused views.
Used the inspected development snapshot d8e4daf2, package 2.17.0-dev.1—not an
assumed stable release. No provider models were called in this smoke test.

- Initial validation reported five label-fit issues at default node widths.
- One correction widened the four nodes to 160. Delivery then passed 9/9
  showcase artifact checks, with zero errors and warnings.
- Opened the resulting HTML with HTTP/HTTPS requests blocked: it rendered.
- The second guided view selected the review job, updated its URL fragment and
  exposed its explanatory note. Theme switching also worked.
- Inspected desktop and narrow-screen renders using actual emulated viewport
  widths, not Chrome's unreliable minimum window width.

[Open the interactive sample](diagrams/archify-review-flow.html), or inspect its
[editable description](diagrams/archify-review-flow.workflow.json).

### Where it does not fit yet

On desktop the example is understandable, but carries presentation/export/style
controls, path/map/lens controls and chapter change counts. Those are useful for
an explorer; they are distracting for a simple “is this what you want?” moment.
The renderer also uses technical component categories and corresponding symbols,
even when the authored labels describe people and work.

At a 390px viewport, this sample scaled the diagram down until node text was
too small to read comfortably, while controls were clipped or horizontally
scrollable. The page-width measurement still passed. At 1440×1000 the page needed
1097px of height. A successful artifact check therefore did not establish mobile
usability or the upstream skill's desired one-screen desktop composition.

These are observations of this small sample, not proof that Archify cannot be
configured better. I did not run its entire test suite or canonical visual-check
receipt workflow, test exports/architecture comparison, or conduct a human
usability trial. The before/after capability is source-reviewed, not exercised.

Source: [Archify](https://github.com/tt-a1i/archify/tree/d8e4daf2610d512821365f41b139d874b29efe81),
particularly archify/SKILL.md, package.json, the workflow/common schemas and
references/delivery-contract.md. MIT notices for the generated example are
retained alongside it.

## How this affects the build

Use the local visual guide to choose the view, then select either available
tool for the first real direction review. Honor a requested tool when available;
explain a missing capability rather than silently substituting. Keep the broad
diagram-design library in scope, not just this pack's few starter patterns.
Use both only when the second view adds understanding, not to duplicate every
diagram. No new abstraction layer, installation requirement, approval receipts
or user-facing setup process follows from keeping both choices.
