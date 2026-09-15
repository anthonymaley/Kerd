# Visual communication by default

## Now

Owner: unassigned for the build; recorded by the Claude session holding
`kerd-b5-review` (2026-09-15). Stage: Shape. Nothing is built or authorized. Planned
as a separate MINOR release after context-aware Roll
(`docs/work/context-awareness/work.md`).

Rulings (Anthony, 2026-09-15):
- Reply to the cadence question, about 14:46: "dont know wat that means, diagram?"
  Conductor answered with an ASCII timeline and no `kerd:visuals`.
- Relayed by another Claude session, 15:26: "its more than this also, we should be
  offering visuals as a matter of course, not heavy text only. when we show a solution
  or proposal"
- **15:31, direct: diagram-design and Archify are required for Kerd's rendered views,
  not merely allowed** ("yes required", answering "Did you mean diagram-design and
  Archify to be required for Kerd's rendered views, not just allowed?"). This
  supersedes the "complementary choices… neither tool becomes a universal Kerd
  dependency" wording in `docs/work/model-ready-work/visual-tools-assessment.md`,
  `skills/visuals/SKILL.md:71-85` and `skills/conductor/SKILL.md:270`. Reason, 15:31:
  "otherwise models wull chose to do their own thing". This sitting shows exactly that:
  the model hand-rolled ASCII when the tools were optional.

## Observed gap (this sitting)

- The standard existed but was not followed. `journey.md` says "Load the sibling Visuals
  skill when drawing"; its proactive wording ("consider whether…") is discretionary.
  Every drawing this sitting was ASCII in a code fence. There was no `kerd:visuals`
  load, no diagram-design, no rendered view: the context-aware Roll design, the route
  comparison and the review-cadence explanation.
- Install state, checked 15:31: the `diagram-design@diagram-design` plugin is installed
  in Claude. Archify is not installed: no plugin, nothing on PATH; only the 2026-09-09
  trial sample in `docs/work/model-ready-work/diagrams/`. Codex's state was not
  checked.

## Proposed correction (not agreed; from two read-only peer replies, revised)

- **Explicit request:** every skill entry point invokes `kerd:visuals` when the person
  asks to see something, and the answer is a saved, rendered view.
- **Proactive default:** a substantial Shape or Agree presentation with several
  connected parts, a branch, an ownership boundary or a before → after change carries
  a rendered view of the solution itself. There is no offer question such as "Would
  you like a diagram?" and no quota. Tiny or factual proposals stay text-only.
- **Required tools (new, 15:31):** Visuals renders through diagram-design
  (static layouts: processes, timelines, responsibilities, scope, comparisons) or
  Archify (exploration, focused paths, comparing changes), not the bundled starter
  patterns alone. Archify needs an approved install. Codex availability is to be
  resolved.
- **Guard:** a static test covering the rule anchors in all 12 entry points,
  Conductor and journey.md, Visuals' trigger description, the required-tool wording,
  and a ban on offer phrases. Mutation-checked.
- **Behavioural tests:** real-model, three runs each. T1 explicit request, T2 proactive
  proposal, T3 proportional control, T4 request outside Conductor. Evidence is limited
  to the run's own ordered stream blocks, a bounded slice of its output, and files it
  wrote. The full test design is in the Claude session's peer reply (request
  `ebc1e3b3`, retained privately); carry it into the score.
