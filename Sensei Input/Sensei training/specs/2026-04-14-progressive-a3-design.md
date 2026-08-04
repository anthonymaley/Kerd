# Progressive A3 with Evidence-First Display

**Date:** 2026-04-14
**Status:** Approved
**Scope:** `skills/shared/a3-template.html`, `skills/work/SKILL.md`

## Problem

The current A3 artifact is generated once after Step 9. The evidence display is narrative prose — the LLM summarizes what it found instead of showing the actual measurements. The result is an A3 that looks correct structurally but contains flawed or unverifiable evidence. The user can't catch this until the end.

Observed in the leru Celtic TV replay bug: the generated A3 had a plausible-sounding "What Is Happening" paragraph, but no measurement table showing values across sources. The evidence was a story, not data.

## Design

### Progressive Build

The A3 HTML file is created at Step 0 and rewritten after every confirmed step. The user can open the file in a browser and refresh to see progress.

| Step confirmed | What changes in the file |
|---|---|
| Step 0 | File created. Header, perceived problem banner. All sections visible but locked (greyed out). Full A3 shape visible. |
| Step 1 | Perceived problem text fills in. No interpretation, no reframing — the raw report as stated. |
| Step 2 | "What Should Happen" fills in with green flow diagram — the ideal/correct path. |
| Step 3 | "AS IS Condition" fills in with red flow diagram and gap quantification — how many, how often, how big the gap is between ideal and reality. |
| Step 4 (gate) | "Break Down the Problem" fills in with evidence `<pre>` block — multi-source measurements, ASCII diagrams, concrete numbers. Target set. Left column complete. |
| Step 5 | 5-Why chain and root cause box fill in. |
| Step 6 | Countermeasure cards appear (explicitly temporary). Unintended consequences noted if any. |
| Step 7 | Monitor section fills in with before/after evidence `<pre>` block comparing against Step 4 measurements. Process check included. |
| Step 8 | Solution + Plan fills in — permanent fix, who/what/when. May link to external docs. |
| Step 9a | Prevent / New Standard fills in. |
| Step 9b | Yokoten fills in. Footer metadata completes. Status set to lifecycle stage. No locked sections remain. |

The file is opened in the browser on Step 0 creation (`open` command on macOS). The markdown file is generated once at the end as the archival copy.

### Section States

Each `.section` in the template has one of three CSS states:

- **`.completed`** — full content, normal display
- **`.active`** — subtle accent (left border or background tint) showing "this is where we are"
- **`.locked`** — reduced opacity, placeholder text: "Pending"

The LLM sets the correct class on each section during every rewrite.

### Left Column Visual Progression

1. **Step 1 — Perceived Problem:** Clean text. What the user reported, verbatim. No diagrams, no interpretation.

2. **Step 2 — What Should Happen:** Green flow diagram using `.flow-box.green` classes. Shows the ideal system flow — how it works when everything is right. No standard diagnosis here (that surfaces in Step 5 if relevant).

3. **Step 3 — AS IS Condition:** Red flow diagram using `.flow-box.red` classes showing the broken state. Plus gap quantification — measurement tags showing the scale of the problem: how many affected, how often, how big the gap is between Step 2 (ideal) and reality. This is TBP Steps 2-3: break down the problem into measurable sub-problems and quantify the gap. The reader should leave Step 3 knowing *how bad* it is, not yet *where* or *why*.

4. **Step 4 — Break Down the Problem:** The heavyweight section. Deeper investigation and measurement. Contains:
   - A `<pre class="evidence">` block with the actual measurements — multi-source comparison tables, ASCII box diagrams showing entities/relationships/gaps, input/output pairs, whatever visual makes the breakdown clear at a glance.
   - The point of cause: where exactly in the system the breakdown occurs.
   - The target: "these measurements should return [X] after the countermeasure." This anchors Step 7 verification. The measurements shown here are the ones that will be re-run at Step 7 to prove the countermeasure worked.

### Evidence Display

Evidence goes in `<pre class="evidence">` blocks — monospace, slightly inset, subtle background. The LLM generates the content as ASCII art/tables/diagrams. No HTML structure inside the `<pre>`.

There is no problem-type classification. The LLM reads its own evidence and picks the visual that makes the gap obvious. The guiding principle: **if a reader can't see what's wrong within 5 seconds of looking at the evidence block, the format is wrong.**

Visual tools available (not categories — mix as needed):

- **Tables** — comparing the same value across multiple sources or time points
- **Box diagrams** — showing entities (servers, apps, databases, people, locations) and the flow or gaps between them
- **Input/output pairs** — what went in, what came out
- **Before/after columns** — showing change

The skill instructions include examples of each visual tool (not per problem type). The LLM adapts.

### Right Column

- **Step 5 (Root Cause / 5 Whys):** Existing why-chain HTML with gradient badges. No change to template structure.
- **Step 6 (Countermeasure):** Explicitly temporary. Gets production running while the permanent solution is planned. The countermeasure cards stay. Add: the LLM should note unintended consequences observed during implementation (TBP 6: "implementation is an experiment — watch for unintended consequences").
- **Step 7 (Monitor/Verify):** A `<pre class="evidence">` block showing before/after comparison — the same measurements from Step 4, re-run after implementation. Also checks for unintended consequences: did the countermeasure break anything else? Did it create new problems? (TBP 7: "monitor both results and processes").
- **Step 8 (Solution + Plan):** New section. The permanent fix. Two parts:
  - **Solution:** What the permanent fix is. May be identical to the countermeasure ("the temporary fix is the right answer") or may be larger ("rebuild the data pipeline"). Clearly stated regardless.
  - **Plan:** Who does what by when. Simple case: "merge PR #123, owner: Anthony, done." Complex case: "requires data pipeline redesign — see design doc at docs/specs/X.md, owner: Y, target: 2026-05-01." The plan makes the solution actionable. The A3 closes when the solution is agreed and the plan is accepted — not when implementation is complete. Implementation may take months; the problem-solving work paper is done when there is agreement on what the right fix is and a plan to get there.
- **Step 9a (Prevent / New Standard):** Standardize the fix. New process, updated standard, structural change that prevents recurrence. Split from yokoten for focus.
- **Step 9b (Yokoten):** Knowledge share. Who else needs to know, how do we spread it. Existing flow boxes. Kept as a separate section to ensure it doesn't get buried as a footnote on standardization.

### A3 Lifecycle Status

The footer status reflects where the A3 is in its lifecycle:

- **In progress** — still working through steps
- **Countermeasure in place** — production running, permanent solution pending agreement
- **Closed** — solution agreed, plan accepted, standard created, knowledge shared. Implementation proceeds separately.

### Template Changes Summary

Changes to `skills/shared/a3-template.html`:

1. Add CSS for `.section.completed`, `.section.active`, `.section.locked`
2. Add `<pre class="evidence">` styling (monospace, inset, background)
3. Add evidence `<pre>` placeholder in Step 4 section (left column)
4. Add evidence `<pre>` placeholder in Step 7 section (right column)
5. Remove the `{{STANDARD_BADGE}}` from Step 2 — standard diagnosis doesn't belong here
6. Rename Step 4 section label from "Point of Cause" to "Break Down the Problem"
7. Add "Solution + Plan" section between Monitor and Prevent/New Standard (right column)
8. Split Step 9 into two sections: "Prevent / New Standard" and "Yokoten"
9. Update footer to show lifecycle status (In progress / Countermeasure in place / Closed)

The existing flow-box, why-chain, countermeasure-card, and tag styling stays as-is.

### Skill Changes Summary

Changes to `skills/work/SKILL.md`:

1. Move A3 creation from "after Step 9" to "at Step 0." Add rewrite instruction after each step's confirmation gate.
2. Add "Evidence Display" section with examples of each visual tool (tables, box diagrams, input/output, before/after). No problem-type categories — just visual tools.
3. Remove standard badge from Step 2 instructions. Standard gap surfaces through 5 Whys if relevant.
4. Strengthen Step 4 as the evidence-heavy step: this is where measurements go, where the target is set, where the `<pre>` block gets filled.
5. Step 6: make countermeasure explicitly temporary. Add instruction to watch for unintended consequences during implementation.
6. Step 7: re-run Step 4 measurements in `<pre>` evidence block. Add instruction to check for unintended consequences (monitor processes, not just results).
7. Add Step 8 (Solution + Plan): permanent fix, who/what/when. May reference external docs for complex work.
8. Split current Step 8/9 into 9a (Prevent / New Standard) and 9b (Yokoten) for focus.
9. Add A3 lifecycle status to footer: In progress → Countermeasure in place → Closed.
10. Add instruction to open the file in the browser at Step 0.

### Source Alignment

Cross-referenced against the three canonical sources and Anthony's framework doc (`docs/tps-framework.md`):

| A3 Section | Anthony's Framework | TBP (Cho, 8-step) | Alignment |
|---|---|---|---|
| Step 1: Perceived Problem | Header: "the symptom, not yet the problem" | TBP 1: Clarify the Problem (grasp current condition) | Aligned. Raw report, no interpretation. |
| Step 2: What Should Happen | Step 2: "Standard process or ideal condition" | TBP 1: Define ideal condition | Aligned. No standard diagnosis here — that surfaces in 5 Whys. |
| Step 3: AS IS Condition | Step 3: "Quantify the gap — measurement, rate, volume, scale" | TBP 2-3: Break down + set target | Aligned. Gap quantification between ideal and reality. |
| Step 4: Break Down | Step 4: "Pinpoint exactly where... set a TARGET" | TBP 2 (deeper break down at gemba) | Aligned. Deep investigation, evidence, point of cause, target. |
| Step 5: Root Cause | Step 5: "5 Whys to systemic cause, not a symptom, not a person" | TBP 4: Analyze root cause at gemba | Aligned. Standard gap can surface here naturally. |
| Step 6: Countermeasure | Step 6: "Countermeasure — hypothesis to test" | TBP 5-6: Develop + see through | Aligned. Made explicitly temporary. Added: watch for unintended consequences (TBP 6). |
| Step 7: Monitor | Step 7: "Prove it's working. Measurement-based." | TBP 7: Monitor results AND processes | Strengthened. Added process monitoring + unintended consequence check (TBP 7). |
| Step 8: Solution + Plan | NEW — not in current framework | TBP 5-6 (permanent aspect) | New. Permanent fix with who/what/when. A3 closes on agreement, not on implementation. |
| Step 9a: Prevent / Standard | Step 8: "Standardize the fix" | TBP 8: Standardize successful processes | Aligned. Split from yokoten for focus. |
| Step 9b: Yokoten | Step 9: "Tell others — yokoten" | TBP 8 (bundled with standardize) | Aligned. Kept separate per Anthony's practice — yokoten is non-negotiable, not a footnote. |

Key insights from the source check:
- Step 3 maps to TBP Steps 2-3 (break down + quantify), not just "show the broken flow." The gap must be measured, not just illustrated.
- Step 6 countermeasure is explicitly temporary — it restores production while the permanent solution (Step 8) is planned and executed.
- TBP 7 monitors processes too, not just results. Added to Step 7.
- Yokoten split from standardization to preserve focus (Anthony's practice, stronger than TBP's bundling).

### What Doesn't Change

- The A3 two-column layout
- The header, perceived problem banner, footer
- The flow-box HTML components (green/red boxes with arrows)
- The 5-Why gradient badges
- The countermeasure cards
- The evidence directory (`kivna/output/sensei-[slug]/evidence/`) and numbered evidence files
- The markdown artifact (generated once at the end)
- Print CSS

---

## Amendment — 2026-07-20: Edit-based updates replace full-file rewrites

The original mechanism above ("rewrite the full A3 HTML after every confirmed step") was replaced after a render-path review measured its cost: 11 full writes per investigation ≈ ~190 KB cumulatively emitted (~45–50k output tokens) for ~15 KB of actual content, tens of seconds of render latency per step, and 10 re-transcriptions of already-confirmed content (silent drift risk).

**New mechanism** (see Update Rules in `skills/work/SKILL.md`, A3 Update Instructions in `skills/story/SKILL.md`):

- `skills/shared/a3-template.html` sections carry `id="step-N"` attributes as Edit anchors.
- After each confirmed step: targeted Edits — content placeholders first, class flips second (anchored on ids), footer counter last. Confirmed sections are never re-emitted.
- Fallback: any Edit that fails to find its anchor triggers a full-file rewrite (the original behavior). The andon contract is unchanged — the file on disk is always a complete, current snapshot.
- Progressive builds insert `<meta http-equiv="refresh" content="10">` at Step 0 and remove it at close, making the open tab live.
- The template stays coach-neutral: bare sections, no refresh tag (coach renders one-shot at completion). Progressive skills add lock classes and the refresh tag at Step 0.
- Spec fixes shipped with this change: Step 1/3 section ownership made consistent (Step 1 = What Is Happening text; Step 3 = its red flow + AS IS), Step 4's update line brought into the standard on-confirmation pattern, `.completed` documented as intentionally unstyled.

Verified by simulation (77-edit full-flow run, every anchor unique at time of use; `scratchpad/simulate_a3_flow.py`). Not yet verified by a live `/sensei:work` run. Meta-refresh scroll behavior untested.
