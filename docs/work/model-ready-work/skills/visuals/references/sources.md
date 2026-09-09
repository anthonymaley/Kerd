# Source and deliberate adaptation

Based on [Cathryn Lavery's diagram-design](https://github.com/cathrynlavery/diagram-design),
MIT, inspected at commit 4451eadc484d76aa860edf3289c16fcd082dcdbf.
The source skill declares version 2.6. This is a curated Kerd adaptation, not
an installation or complete copy of the upstream skill and its 39-type library.

Source files inspected include:

- skills/diagram-design/SKILL.md
- references/type-architecture.md, type-nested.md, type-swimlane.md and type-flowchart.md
- assets/template.html

The reference and asset paths above are relative to the upstream skill unless
the path begins with skills/. The worked HTML adapts the upstream template's
single-file structure, semantic colour roles and accessible inline-SVG approach.
Upstream licensing is retained in [LICENSE](../LICENSE).

Kept: choose the type by meaning; containment and arrows communicate real
relationships; restrained emphasis; overview before detail; accessible SVG;
inspect the rendered output; preserve meaning when simplifying.

Changed for Kerd:

- No first-use brand setup gate or pre-drawing confirmation beat.
- System fonts and no external assets by default; remove the template's 900px
  minimum SVG width so the output can be used on narrow screens.
- No global profile files or installation required to use this candidate.
- Geometry/grid/node-count guidance is a design aid, not a work-blocking rule.
- No mandatory linter suite, CI, seals or SHA receipts. Visual and semantic
  inspection remain required practice; unavailable inspection is disclosed.
- Map patterns to what the person needs to understand, not Kerd rungs.

This is development material in the proposal pack. Conductor's candidate loads
this SKILL.md explicitly when preparing the direction visual. It is not yet
registered as an installed Kerd command. Promote the same files, not a second
instruction copy, when the reworked skill is adopted.
