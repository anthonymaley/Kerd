# Progressive A3 with Evidence-First Display — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the A3 artifact build progressively (rewritten at each step), with evidence displayed as ASCII art in `<pre>` blocks instead of narrative prose, and add Solution + Plan section with lifecycle status.

**Architecture:** Two files change: `skills/shared/a3-template.html` (the HTML template with CSS and placeholders) and `skills/work/SKILL.md` (the LLM discipline instructions). The template gets new CSS states, evidence `<pre>` blocks, and new sections. The skill gets progressive build instructions, evidence display examples, and restructured right-column steps.

**Tech Stack:** HTML/CSS (template), Markdown (skill instructions)

**Spec:** `docs/specs/2026-04-14-progressive-a3-design.md`

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `skills/shared/a3-template.html` | Modify | Add section state CSS, evidence `<pre>` styling, restructure sections |
| `skills/work/SKILL.md` | Modify | Progressive build, evidence display, restructured steps 2/4/6/7/8/9 |

---

### Task 1: Add section state CSS and evidence block styling to template

**Files:**
- Modify: `skills/shared/a3-template.html:7-69` (CSS block)

- [ ] **Step 1: Add section state CSS classes**

Add these rules after the existing `.section` styles (after line 23 in the current file):

```css
.section.active { border-left: 3px solid #1a6eb5; padding-left: 13px; background: #fafcff; }
.section.locked { opacity: 0.35; }
.section.locked .section-label::after { content: " — Pending"; font-weight: 400; font-style: italic; color: #999; text-transform: none; letter-spacing: 0; }
```

- [ ] **Step 2: Add evidence `<pre>` block styling**

Add after the section state CSS:

```css
pre.evidence { background: #f8f8f5; border: 1px solid #ddd; border-left: 3px solid #1a6eb5; border-radius: 3px; padding: 10px 12px; margin: 8px 0; font-family: 'SF Mono', 'Menlo', 'Consolas', monospace; font-size: 10px; line-height: 1.5; color: #222; white-space: pre; overflow-x: auto; }
```

- [ ] **Step 3: Add lifecycle status badge CSS**

Add after the evidence CSS:

```css
.status-badge { display: inline-block; border-radius: 3px; padding: 2px 8px; font-size: 10px; font-weight: 600; }
.status-badge.in-progress { background: #fff3cd; border: 1px solid #e67e22; color: #7a3d00; }
.status-badge.cm-in-place { background: #e8f0fb; border: 1px solid #1a6eb5; color: #1a3a6e; }
.status-badge.closed { background: #e6f9ee; border: 1px solid #27ae60; color: #0d5a20; }
```

- [ ] **Step 4: Add print CSS for new elements**

Add inside the existing `@media print` block (before the closing `}`):

```css
pre.evidence { border-color: #999; background: #f8f8f8; }
.section.locked { opacity: 0.25; }
.section.active { border-left-color: #999; background: white; }
```

- [ ] **Step 5: Verify CSS doesn't break existing template**

Open `skills/shared/a3-template.html` in a browser. Visually confirm:
- All existing sections render normally (no state class = no change)
- The template structure is intact
- No CSS syntax errors (browser dev tools console)

- [ ] **Step 6: Commit**

```bash
git add skills/shared/a3-template.html
git commit -m "feat: add section state CSS, evidence block, and lifecycle badge styling to A3 template"
```

---

### Task 2: Restructure template HTML sections

**Files:**
- Modify: `skills/shared/a3-template.html:72-184` (HTML body)

- [ ] **Step 1: Rename Step 4 section label and add evidence placeholder**

In the left column, find the section with label "Point of Cause" (around line 115). Replace the entire section:

Old:
```html
<div class="section">
  <div class="section-label">Point of Cause</div>
  <div class="section-text">{{POINT_OF_CAUSE_LOCATION}}</div>
  <div class="poc-box">
    <div class="poc-label">⚠ Breakdown Point</div>
    <div class="poc-should">✓ Should: {{POC_SHOULD}}</div>
    <div class="poc-actual">✗ Actual: {{POC_ACTUAL}}</div>
  </div>
  <span class="tag target">🎯 Target: {{TARGET}}</span>
</div>
```

New:
```html
<div class="section">
  <div class="section-label">Break Down the Problem</div>
  <pre class="evidence">{{EVIDENCE_BLOCK}}</pre>
  <div class="poc-box">
    <div class="poc-label">⚠ Point of Cause</div>
    <div class="poc-should">✓ Should: {{POC_SHOULD}}</div>
    <div class="poc-actual">✗ Actual: {{POC_ACTUAL}}</div>
  </div>
  <span class="tag target">🎯 Target: {{TARGET}}</span>
</div>
```

- [ ] **Step 2: Remove `{{STANDARD_BADGE}}` from Step 2 section**

In the left column "What Should Happen" section (around line 98-102), remove the line:
```html
{{STANDARD_BADGE}}
```

- [ ] **Step 3: Add evidence `<pre>` to Step 7 (Monitor) in right column**

Find the "How to Check / Monitor" section (around line 150-153). Replace:

Old:
```html
<div class="section">
  <div class="section-label">How to Check / Monitor</div>
  <div class="section-text">{{MONITOR_TEXT}}</div>
</div>
```

New:
```html
<div class="section">
  <div class="section-label">How to Check / Monitor</div>
  <pre class="evidence">{{VERIFY_EVIDENCE_BLOCK}}</pre>
  <div class="section-text">{{MONITOR_TEXT}}</div>
</div>
```

- [ ] **Step 4: Add Solution + Plan section in right column**

After the "How to Check / Monitor" section and its `<hr class="div">`, add a new section before "Prevent / New Standard":

```html
<hr class="div">

<div class="section">
  <div class="section-label">Solution + Plan</div>
  <div class="section-text"><strong>Solution:</strong> {{SOLUTION_TEXT}}</div>
  <div class="section-text"><strong>Plan:</strong> {{PLAN_TEXT}}</div>
</div>
```

- [ ] **Step 5: Split Yokoten into two sections (Prevent/Standard + Yokoten)**

Find the existing "Prevent / New Standard" section. It stays as-is. Find the existing "Yokoten — Knowledge Share" section. It stays as-is. Verify there is an `<hr class="div">` between them. The split is already structurally present in the current template — they are already separate sections. Confirm they each have their own `<div class="section">` wrapper. No HTML change needed here, just confirm.

- [ ] **Step 6: Update footer with lifecycle status**

Replace the footer's `{{STATUS}}` reference. In the header meta div (line 77), the `Status: {{STATUS}}` already exists. No change to the placeholder name — just document in the skill that `{{STATUS}}` now uses lifecycle values ("In progress", "Countermeasure in place", "Closed").

- [ ] **Step 7: Verify template renders correctly**

Open `skills/shared/a3-template.html` in a browser. The `{{PLACEHOLDER}}` text will show literally — that's expected. Check:
- The new "Break Down the Problem" label appears in the left column
- The `<pre>` evidence placeholder block is visible in Step 4 and Step 7
- The "Solution + Plan" section appears between Monitor and Prevent
- No layout breaks, no missing sections

- [ ] **Step 8: Commit**

```bash
git add skills/shared/a3-template.html
git commit -m "feat: restructure A3 template — evidence blocks, solution section, renamed Step 4"
```

---

### Task 3: Rewrite SKILL.md — Step 2 (remove standard diagnosis)

**Files:**
- Modify: `skills/work/SKILL.md:202-218`

- [ ] **Step 1: Remove standard diagnosis from Step 2**

Replace the current Step 2 section (lines 202-218) with:

```markdown
### STEP 2 — What Should Happen

**Share this insight:**
> *"At Toyota, the first question when any defect is found is: 'Was standardized work followed?' But before you can ask that question, you need to know what 'right' looks like. This step defines the ideal — the correct flow when everything works as intended."*

Describe the ideal state. How should this system/process work when everything is right? This sets the reference point — the green-path flow that Step 3 will contrast against.

Do not diagnose standards here. If there is no standard, that will surface naturally through the 5 Whys in Step 5. Step 2 is purely: here is how it should work.

**A3 update:** Rewrite the A3 HTML. Set Step 2 to `.active`, populate the "What Should Happen" section with a green flow diagram (`.flow-box.green`) showing the ideal flow. Set Step 3 to `.active` next. All later sections remain `.locked`.

Present draft:
> "Step 2: Here's how this should work: [ideal flow description]. Does this match the expected behavior?"

**Wait for confirmation before proceeding.**
```

- [ ] **Step 2: Commit**

```bash
git add skills/work/SKILL.md
git commit -m "feat: remove standard diagnosis from Step 2 — surfaces in 5 Whys instead"
```

---

### Task 4: Rewrite SKILL.md — Step 4 (evidence-heavy breakdown)

**Files:**
- Modify: `skills/work/SKILL.md:241-260`

- [ ] **Step 1: Rewrite Step 4 as the evidence-heavy breakdown step**

Replace the current Step 4 section (lines 241-260) with:

```markdown
### STEP 4 — Break Down the Problem + Target (THE GATE)

**Share this insight:**
> *"Jidoka — Toyota's right pillar — is built on one principle: stop and fix at the source. The andon cord is pulled not where the problem is discovered downstream, but at the workstation where it occurs. Finding the point of cause means asking 'where was the work last good?' and tracing forward to the exact moment it breaks. Without this precision, 5 Whys starts from the wrong place and leads to the wrong root cause every time."*

This is the heavyweight step. Deep investigation and measurement. Three deliverables:

**1. Evidence block.** Build the `<pre class="evidence">` content for the A3. This is the ASCII visual that makes the breakdown obvious at a glance. Pick the format that fits the evidence — see the Evidence Display section below for visual tools. The guiding principle: if a reader can't see what's wrong within 5 seconds of looking at the evidence block, the format is wrong.

**2. Point of cause.** The exact location where the breakdown occurs — not where the symptom appears, where it originates. Confirmed by evidence showing data was correct before this point and incorrect after.

**3. Target.** Defined as specific measurements: "these values from the evidence block should return [X] after the countermeasure." This anchors Step 7 verification. The same measurements shown in the evidence block here will be re-run at Step 7 to prove the countermeasure worked.

**Evidence required:** Every claim in this step must cite evidence files. The evidence block content comes directly from what you measured — not from what the code says should happen.

**A3 update:** Rewrite the A3 HTML. Set Step 4 to `.active`, populate the "Break Down the Problem" section with the `<pre class="evidence">` block, point of cause, and target. This completes the left column — all left-column sections are now `.completed`.

Present draft:
> "Step 4: Here is the breakdown [evidence block]. Point of cause: [location, citing evidence]. Target: [measurements should return X]. Left column complete. I will not proceed to root cause or touch any code until you confirm this is correct. Ready?"

**EXPLICIT GATE** — do not proceed until confirmed.

**Wait for confirmation before proceeding.**
```

- [ ] **Step 2: Commit**

```bash
git add skills/work/SKILL.md
git commit -m "feat: rewrite Step 4 as evidence-heavy breakdown with ASCII evidence block"
```

---

### Task 5: Add Evidence Display section to SKILL.md

**Files:**
- Modify: `skills/work/SKILL.md` (insert new section after the Evidence Protocol section, before Live Progress Document)

- [ ] **Step 1: Add Evidence Display section**

Insert after the Evidence Protocol section (after line ~107, before the `## Live Progress Document` heading) a new section:

````markdown
---

## Evidence Display

When building the `<pre class="evidence">` block for the A3 (Steps 4 and 7), use ASCII art and monospace formatting. No HTML inside the `<pre>`. Pick the visual that makes the gap obvious — mix formats as needed.

### Visual Tools

**Tables** — comparing the same value across multiple sources or time points:
```
Source           Celtic v StM    Dundee v Celtic    Ross v Celtic
─────────────────────────────────────────────────────────────────
Supabase         80027564/65 ✓   80027101/45 ✓      80026998/99 ✓
CDN Bundle       80027564/65 ✓   80027101/45 ✓      80026998/99 ✓
App Display      80027101/45 ✗   80027564/65 ✗      80026998/99 ✓
─────────────────────────────────────────────────────────────────
Verdict          HYDRATION       HYDRATION          OK
```

**Box diagrams** — showing entities and the flow or gaps between them:
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Celtic TV   │────▶│  Fly.io      │────▶│  Supabase   │
│  source      │     │  classify.py │     │  master     │
│  200 OK ✓    │     │  empty date  │     │  3/4 ✓      │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │ ✗ drops video
                           ▼
                     ┌─────────────┐
                     │  Apr 11     │
                     │  unmatched  │
                     └─────────────┘
```

**Input/output pairs** — what went in and what came out:
```
Input:  parse_video_date("")
Expected: None → fallback to title matching
Actual:   None → find_fixture(None) → returns None → video unmatched

Input:  parse_video_date("2026-04-05")
Expected: 2026-04-05 → find_fixture matches correctly ✓
Actual:   Works as expected ✓
```

**Before/after columns** — showing change (used at Step 7 verification):
```
Measurement              Before (Step 4)    After (Step 7)    Target    Status
──────────────────────────────────────────────────────────────────────────────
Celtic v StM replays     80027101/45 ✗      80027564/65       correct   ✓
Dundee v Celtic replays  80027564/65 ✗      80027101/45       correct   ✓
Apr 11 replay state      pending            80027564/65       assigned  ✓
Hydration overwrites     4/4                0/4               0         ✓
```

**The rule:** if a reader can't see what's wrong within 5 seconds, the format is wrong. Adapt the visual to the evidence, not the evidence to a template.
````

- [ ] **Step 2: Commit**

```bash
git add skills/work/SKILL.md
git commit -m "feat: add Evidence Display section with ASCII visual tool examples"
```

---

### Task 6: Rewrite SKILL.md — Steps 6, 7, 8, 9 (right column restructure)

**Files:**
- Modify: `skills/work/SKILL.md:289-356`

- [ ] **Step 1: Rewrite Step 6 — countermeasure as explicitly temporary**

Replace the current Step 6 section (lines 289-309) with:

```markdown
### STEP 6 — Countermeasure (Temporary)

**Share this insight:**
> *"Toyota forbids the word 'solution.' There are only countermeasures — hypotheses to test. A countermeasure proven effective becomes a standard — 'the best we know today until we find a better one.' The distinction matters: 'solution' closes inquiry; 'countermeasure' keeps the PDCA loop open."*

Now — and only now — propose countermeasures. These are temporary — they get production running while the permanent solution (Step 8) is planned. Format as numbered items:
```
Countermeasure 1: [specific action] — addresses [which why] [evidence: N]
Countermeasure 2: [specific action] — addresses root cause [evidence: N]
```

**Evidence required:** Each countermeasure must cite the evidence that supports why this specific change will fix the problem. A countermeasure without evidence is a guess.

For each: what exactly changes, which Step 4 measurement will confirm it's working, and what this is buying time for (the permanent fix comes at Step 8).

Ask: "Do these countermeasures address the root cause? Confirm before I implement."

**Wait for confirmation, then implement.**

**Watch for unintended consequences.** Implementation is an experiment. After making the changes, observe: did anything unexpected happen? Did the countermeasure break something else? Note any unintended consequences — they feed into Step 7.

**EXPLICIT GATE** — this is the code-change boundary. Do not write a single line of code until the user confirms the countermeasures. State: "Countermeasures agreed. These are temporary — they restore production while we plan the permanent fix. I will not touch any code until you confirm. Ready?"

**A3 update:** Rewrite the A3 HTML. Set Step 6 to `.completed`, populate countermeasure cards. Set Step 7 to `.active`.
```

- [ ] **Step 2: Rewrite Step 7 — monitor with evidence block and process check**

Replace the current Step 7 section (lines 312-328) with:

```markdown
### STEP 7 — Monitor + Verify

**Share this insight:**
> *"'We can't afford PDCA that takes three weeks anymore. We want a PDCA done before the end of that shift.' The Check step is not a formality — it is how you know whether your hypothesis was correct. A countermeasure that 'seems to be working' is not verified. Only measurement confirms."*

After implementing: re-run the measurements from Step 4. This is not optional.

1. Open the evidence block from Step 4
2. Re-run the exact same commands, queries, or checks
3. Save the results as new evidence files (e.g., `evidence/012-verify-[description].md`)
4. Build the before/after evidence block for the A3 (see Evidence Display — before/after columns)

**Check for unintended consequences.** Did the countermeasure break anything else? Did it create new problems? Monitor processes, not just results. If unintended consequences were noted during Step 6 implementation, verify they were addressed.

Output with evidence citations:
> "Verification: re-ran [measurement from Step 4]. Before: [X, from evidence: N]. After: [Y, from evidence: M]. Target was [Z]. ✓ Confirmed / ✗ Not yet resolved."

If the measurements don't match the target defined in Step 4, the countermeasure failed. Do not rationalize. Report the gap and go back to Step 5.

**A3 update:** Rewrite the A3 HTML. Set Step 7 to `.completed`, populate the `<pre class="evidence">` block with the before/after comparison. Set Step 8 to `.active`.
```

- [ ] **Step 3: Add new Step 8 — Solution + Plan**

After Step 7 (and after a `---` divider), add:

```markdown
---

### STEP 8 — Solution + Plan

**Share this insight:**
> *"The countermeasure gets production running. The solution ensures the problem never returns. At Toyota, the A3 is not complete until there is agreement on both — what the permanent fix is and who will do what by when to implement it."*

The countermeasure from Step 6 is temporary. Now define the permanent fix:

**Solution:** What is the permanent fix? It may be identical to the countermeasure ("the temporary fix is the right answer — no further work needed") or it may be larger ("the data pipeline needs to be restructured — see design doc"). State it clearly regardless.

**Plan:** Who does what by when. Format:
```
Solution: [what the permanent fix is]
Owner: [who is responsible]
Target date: [when]
Reference: [link to design doc, ticket, or "self-contained — countermeasure is the fix"]
```

The A3 closes when the solution is agreed and the plan is accepted — not when implementation is complete. Implementation may take months. The problem-solving work paper is done when there is agreement on what the right fix is and a plan to get there.

**A3 update:** Rewrite the A3 HTML. Set Step 8 to `.completed`, populate the "Solution + Plan" section. Set Step 9a to `.active`.
```

- [ ] **Step 4: Rewrite Steps 8/9 as 9a and 9b**

Replace the current Step 8 (Prevent/Standard, lines 331-343) and Step 9 (Yokoten, lines 347-355) with:

```markdown
---

### STEP 9a — Prevent / New Standard

**Share this insight:**
> *"'Standardized work is today's best-known way, which can be improved tomorrow.' When a countermeasure proves effective, it becomes the new standard. The standard is not bureaucracy — it is the floor from which the next improvement begins."*

Define the standard:
- What new process, check, test, or configuration prevents recurrence?
- If no standard existed before this investigation (discovered during 5 Whys), write one explicitly
- If a standard existed but wasn't followed, address why and how to enforce it

**Evidence required:** The new standard must reference the Step 7 verification evidence that proved the countermeasure worked. A standard based on an unverified countermeasure is premature.

Output the standard text clearly so it can be documented.

**A3 update:** Rewrite the A3 HTML. Set Step 9a to `.completed`. Set Step 9b to `.active`.

---

### STEP 9b — Yokoten (Knowledge Share)

**Share this insight:**
> *"Yokoten means 'across everywhere' — horizontal, peer-to-peer knowledge transfer. At Toyota, you are not done until others who could benefit have learned what you learned. It's not 'copy exactly' — go see, understand, then adapt with your own wisdom. The process is not complete until the knowledge spreads."*

Suggest:
- Who else on the team should know about this?
- Where should the fix / new standard be documented?
- Is there a related area with the same vulnerability?

**A3 update:** Rewrite the A3 HTML. Set Step 9b to `.completed`. All sections now `.completed`. Set footer status to lifecycle stage ("Closed" if solution agreed, "Countermeasure in place" if solution still being planned).
```

- [ ] **Step 5: Commit**

```bash
git add skills/work/SKILL.md
git commit -m "feat: restructure right column — temporary countermeasure, solution+plan, 9a/9b split"
```

---

### Task 7: Rewrite SKILL.md — Artifact Generation (progressive build)

**Files:**
- Modify: `skills/work/SKILL.md:380-511` (Artifact Generation + Completion Message sections)

- [ ] **Step 1: Replace Artifact Generation section with Progressive A3 Build**

Replace the entire "## Artifact Generation" section (lines 380-492) and "## Completion Message" section (lines 496-511) with:

````markdown
## Progressive A3 Build

The A3 HTML artifact is built progressively — created at Step 0, rewritten after every confirmed step. The user can open the file in a browser and refresh to see progress.

### Setup (at Step 0)

1. Create the output directory: `kivna/output/sensei-[slug]/`
2. Create the evidence subdirectory: `kivna/output/sensei-[slug]/evidence/`
3. Read `skills/shared/a3-template.html`
4. Write the initial A3 HTML: populate header (title, owner, date, mode), perceived problem banner. Set all sections to `.locked` class. Set `{{STATUS}}` to "In progress".
5. Save as `kivna/output/sensei-[slug]/sensei-[slug].html`
6. Open in browser: `open kivna/output/sensei-[slug]/sensei-[slug].html`

**Slug:** lowercase, hyphens, max 40 chars from the perceived problem. If a directory with this slug already exists in `kivna/output/`, append `-2`, `-3`, etc.

### Rewrite Rules

After each step is confirmed by the user, rewrite the A3 HTML file:

1. Set the just-confirmed section to `.completed` (remove `.active` and `.locked` classes)
2. Set the next section to `.active`
3. Populate the confirmed section's content with the confirmed data
4. Keep all later sections as `.locked`
5. Save the file (overwrite)

The user refreshes their browser to see the updated A3.

### Step-by-Step A3 Content

| Step | Section populated | Key content |
|---|---|---|
| 0 | Header + perceived problem banner | Title, owner, date. All sections locked. |
| 1 | Perceived Problem | Raw report text, verbatim. No interpretation. |
| 2 | What Should Happen | Green flow diagram (`.flow-box.green`). Ideal system flow. |
| 3 | AS IS Condition | Red flow diagram (`.flow-box.red`). Gap quantification tags. |
| 4 | Break Down the Problem | `<pre class="evidence">` block with ASCII measurements. Point of cause. Target. |
| 5 | Root Cause — 5 Whys | Why chain HTML (`.why-row`, `.why-num.w1-w5`). Root cause box. |
| 6 | Countermeasures | Countermeasure cards (`.cm-card`). Explicitly temporary. |
| 7 | How to Check / Monitor | `<pre class="evidence">` block with before/after comparison. Verification tags. |
| 8 | Solution + Plan | Solution text. Plan: who/what/when. |
| 9a | Prevent / New Standard | Standard text. New standard badge if applicable. |
| 9b | Yokoten — Knowledge Share | Flow boxes. Knowledge distribution. Footer status set to lifecycle stage. |

### Placeholder Reference

Replace these placeholders when populating each section:

**Header:** `{{TITLE}}`, `{{OWNER}}`, `{{DATE}}`, `{{MODE}}` (/sensei:work), `{{STATUS}}` (lifecycle: "In progress" / "Countermeasure in place" / "Closed"), `{{PERCEIVED_PROBLEM}}`, `{{PERCEIVED_PROBLEM_SLUG}}`

**Left column:**
- Step 2: `{{WHAT_SHOULD_HAPPEN_FLOW}}` (green flow boxes), `{{WHAT_SHOULD_HAPPEN_TEXT}}`
- Step 3: `{{WHAT_IS_HAPPENING_FLOW}}` (red flow boxes), `{{WHAT_IS_HAPPENING_TEXT}}`, `{{AS_IS_TEXT}}`, `{{AS_IS_MEASUREMENTS}}` (measurement tags)
- Step 4: `{{EVIDENCE_BLOCK}}` (ASCII evidence in `<pre>`), `{{POC_SHOULD}}`, `{{POC_ACTUAL}}`, `{{TARGET}}`

**Right column:**
- Step 5: `{{WHY_CHAIN}}` (why rows), `{{ROOT_CAUSE}}`
- Step 6: `{{COUNTERMEASURES}}` (cm-card HTML), `{{VERIFICATION_MEASUREMENT}}`
- Step 7: `{{VERIFY_EVIDENCE_BLOCK}}` (ASCII before/after in `<pre>`), `{{MONITOR_TEXT}}`
- Step 8: `{{SOLUTION_TEXT}}`, `{{PLAN_TEXT}}`
- Step 9a: `{{PREVENT_TEXT}}`, `{{NEW_STANDARD_BADGE}}`
- Step 9b: `{{YOKOTEN_FLOW}}`, `{{YOKOTEN_TEXT}}`

**Footer:** `{{MODE}}`, `{{DATE}}`, `{{STEPS_CONFIRMED}}`, `{{CHALLENGED_STEPS}}`, `{{TIME_TO_CM}}`, `{{CONCEPTS_SURFACED}}`

### Markdown Archive (at completion)

After Step 9b is confirmed, generate the markdown archive:

`kivna/output/sensei-[slug]/sensei-[slug].md`

```
# Sensei Report: [perceived problem]

**Date:** [date]
**Owner:** LLM-assisted
**Mode:** /sensei:work
**Status:** [lifecycle status]

---

## Perceived Problem
[text]

## Left Column — Understand

### What Should Happen
[text]

### AS IS Condition
[text]
**Gap:** [quantified measurements]

### Break Down the Problem
```
[evidence block — ASCII art copied from A3]
```
**Point of Cause:** [location]
**Should:** [expected]
**Actual:** [actual]
**Target:** [measurable target]

---

## Right Column — Resolve

### Root Cause — 5 Whys
1. [W1]
2. [W2]
3. [W3]
4. [W4]
5. [W5]

**Root Cause:** [systemic statement]

### Countermeasures (Temporary)
1. [CM1 — status]
2. [CM2 — status]

**Verification:**
```
[before/after evidence block — ASCII art copied from A3]
```

### Solution + Plan
**Solution:** [permanent fix]
**Plan:** [who/what/when]

### Prevent / New Standard
[text]

### Yokoten — Knowledge Share
[text]

---

## TPS Concepts Surfaced
[list, or "None"]
```

### Completion Message

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Sensei Complete — [problem title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ All steps confirmed
✓ Countermeasure: [title] — [verified/pending]
✓ Solution: [agreed/pending]
✓ Standard: [new/updated/restored]
✓ Status: [lifecycle status]

Artifacts:
  HTML → kivna/output/sensei-[slug]/sensei-[slug].html
  MD   → kivna/output/sensei-[slug]/sensei-[slug].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
````

- [ ] **Step 2: Commit**

```bash
git add skills/work/SKILL.md
git commit -m "feat: replace end-only artifact generation with progressive A3 build"
```

---

### Task 8: Add A3 rewrite instructions to each step in SKILL.md

**Files:**
- Modify: `skills/work/SKILL.md` — Steps 0, 1, 3, 5 (the steps that don't already have A3 update instructions from Tasks 3, 4, 6)

- [ ] **Step 1: Add A3 creation to Step 0 (Opening)**

In the Opening section (around lines 16-23), after the line about creating the evidence directory, add:

```markdown
**A3 creation:** Read `skills/shared/a3-template.html`. Write the initial A3 HTML file to `kivna/output/sensei-[slug]/sensei-[slug].html` with header populated (title, owner, date, mode, status "In progress"), perceived problem banner filled in, and all sections set to `.locked`. Open the file in the browser: `open kivna/output/sensei-[slug]/sensei-[slug].html`.
```

- [ ] **Step 2: Add A3 rewrite instruction to Step 1**

At the end of Step 1 (before "Wait for confirmation"), add:

```markdown
**A3 update:** Rewrite the A3 HTML. Set Step 1 (Perceived Problem / "What Is Happening") to `.completed` with the confirmed content. Set Step 2 to `.active`. All later sections remain `.locked`.
```

- [ ] **Step 3: Add A3 rewrite instruction to Step 3**

At the end of Step 3 (before "Wait for confirmation"), add:

```markdown
**A3 update:** Rewrite the A3 HTML. Set Step 3 to `.completed`, populate the "AS IS Condition" section with red flow diagram and gap quantification measurement tags. Set Step 4 to `.active`.
```

- [ ] **Step 4: Add A3 rewrite instruction to Step 5**

At the end of Step 5 (before "Wait for confirmation"), add:

```markdown
**A3 update:** Rewrite the A3 HTML. Set Step 5 to `.completed`, populate the 5-Why chain and root cause box. Set Step 6 to `.active`.
```

- [ ] **Step 5: Commit**

```bash
git add skills/work/SKILL.md
git commit -m "feat: add A3 rewrite instructions to all steps for progressive build"
```

---

### Task 9: Update Contextual Concepts table step references

**Files:**
- Modify: `skills/work/SKILL.md:359-376` (Contextual TPS Concept Suggestions)

- [ ] **Step 1: Update step references in the concept table**

The concept table references "Step 8" for SDCA and "Step 5-8" for Poka-Yoke. Update these to match the new step numbering:

| Pattern | Old "When" | New "When" |
|---|---|---|
| Poka-Yoke | Step 5–8 | Step 5–9a |
| SDCA | Step 8 | Step 9a |

- [ ] **Step 2: Commit**

```bash
git add skills/work/SKILL.md
git commit -m "fix: update concept suggestion step references for new numbering"
```

---

### Task 10: Final verification

**Files:**
- Read: `skills/work/SKILL.md`, `skills/shared/a3-template.html`

- [ ] **Step 1: Read the full SKILL.md and verify internal consistency**

Check:
- Every step (0 through 9b) has an "A3 update" instruction
- Step references are consistent (Step 4 measurements referenced in Step 7, etc.)
- No references to old step numbering (old "Step 8" = prevent, old "Step 9" = yokoten)
- Evidence protocol still references `sensei-[slug]` paths everywhere
- No `{{STANDARD_BADGE}}` references remain

- [ ] **Step 2: Read the full a3-template.html and verify structure**

Check:
- CSS has `.section.completed`, `.section.active`, `.section.locked` rules
- CSS has `pre.evidence` rule
- HTML has `{{EVIDENCE_BLOCK}}` in Step 4 section
- HTML has `{{VERIFY_EVIDENCE_BLOCK}}` in Step 7 section
- HTML has "Solution + Plan" section with `{{SOLUTION_TEXT}}` and `{{PLAN_TEXT}}`
- HTML has no `{{STANDARD_BADGE}}` in Step 2
- Step 4 label says "Break Down the Problem"
- Footer placeholder `{{STATUS}}` exists

- [ ] **Step 3: Open template in browser for visual check**

Open `skills/shared/a3-template.html` in a browser. Check layout integrity.

- [ ] **Step 4: Commit any fixes found during verification**

```bash
git add -A
git commit -m "fix: address issues found during progressive A3 verification"
```

Skip this step if no fixes were needed.
