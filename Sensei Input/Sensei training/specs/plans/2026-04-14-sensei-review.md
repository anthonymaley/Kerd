# /sensei:review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `/sensei:review` skill that reads a completed A3 (PDF/HTML/markdown), delivers blunt red-ink feedback on every step, issues a verdict (pass/rework/reject), and generates an annotated HTML artifact.

**Architecture:** One SKILL.md file for the review skill, one HTML template for the annotated artifact (extending the existing A3 template with red-ink annotation styles). Update plugin.json to include the fourth skill.

**Tech Stack:** Markdown (SKILL.md with YAML frontmatter), HTML/CSS (review template), Claude Code plugin system

---

## File Map

| Action | File | Purpose |
|--------|------|---------|
| Create | `skills/review/SKILL.md` | The review skill — sensei voice, walkthrough, verdict |
| Create | `skills/shared/a3-review-template.html` | Annotated A3 template with red-ink styles |
| Modify | `.claude-plugin/plugin.json` | Update description to mention all four skills |

---

### Task 1: Create the review A3 template

**Files:**
- Reference: `skills/shared/a3-template.html` (the existing A3 template — read for structure)
- Create: `skills/shared/a3-review-template.html`

- [ ] **Step 1: Read the existing A3 template**

Read `skills/shared/a3-template.html` to understand the full structure, CSS classes, and placeholder conventions.

- [ ] **Step 2: Write the review template**

Create `skills/shared/a3-review-template.html`. This extends the existing A3 template with:

**New CSS additions** (add to the existing `<style>` block):

```css
/* Review annotation styles */
.review-badge { position: absolute; top: 10px; right: 120px; border-radius: 4px; padding: 3px 10px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.review-badge.pass { background: #e6f9ee; border: 1.5px solid #1a8a40; color: #0d4a20; }
.review-badge.rework { background: #fff3cd; border: 1.5px solid #e67e22; color: #7a3d00; }
.review-badge.reject { background: #fde8e8; border: 1.5px solid #c0392b; color: #7a1010; }
.a3-header { position: relative; }
.review-note { border-left: 3px solid #c0392b; background: #fff8f8; padding: 6px 10px; margin-top: 6px; font-size: 11px; color: #c0392b; line-height: 1.5; }
.review-note .review-label { font-size: 8px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #c0392b; display: block; margin-bottom: 2px; }
.review-note.ok { border-left-color: #1a8a40; background: #f6fdf9; color: #0d5a20; }
.review-note.ok .review-label { color: #1a8a40; }
.section.has-note { position: relative; }
.verdict-box { background: #1a1a2e; color: white; border-radius: 4px; padding: 10px 14px; margin: 10px 16px; font-size: 12px; line-height: 1.6; }
.verdict-box .verdict-label { font-size: 9px; font-weight: 400; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 4px; }
.verdict-box.pass { background: #0d4a20; }
.verdict-box.rework { background: #7a3d00; }
.verdict-box.reject { background: #7a1010; }
.verdict-rework-list { margin-top: 4px; padding-left: 16px; font-size: 11px; }
```

**Template structure** — same layout as the existing A3 template, but with these changes:

1. **Header** — add `{{REVIEW_BADGE}}` placeholder inside `.a3-header` (after the meta div):
```html
<div class="a3-header">
  <h1>{{TITLE}}</h1>
  <div class="meta">Owner: {{OWNER}} &nbsp;·&nbsp; {{DATE}}<br>Mode: {{ORIGINAL_MODE}} &nbsp;·&nbsp; Status: {{STATUS}}</div>
  {{REVIEW_BADGE}}
</div>
```

Where `{{REVIEW_BADGE}}` is one of:
- `<div class="review-badge pass">PASS</div>`
- `<div class="review-badge rework">REWORK</div>`
- `<div class="review-badge reject">REJECT</div>`

2. **Each section** — after the original content, add a `{{REVIEW_STEP_N}}` placeholder that will contain either:
- A red-ink note: `<div class="review-note"><span class="review-label">Sensei</span>{{REVIEW_TEXT}}</div>`
- An ok note: `<div class="review-note ok"><span class="review-label">Sensei</span>Accepted.</div>`

Placeholder names per section:
- `{{REVIEW_PERCEIVED}}` — after the perceived problem banner
- `{{REVIEW_STEP1}}` — after What Is Happening
- `{{REVIEW_STEP2}}` — after What Should Happen
- `{{REVIEW_STEP3}}` — after AS IS Condition
- `{{REVIEW_STEP4}}` — after Point of Cause
- `{{REVIEW_GATE}}` — between left and right columns (gate integrity check)
- `{{REVIEW_STEP5}}` — after Root Cause
- `{{REVIEW_STEP6}}` — after Countermeasures
- `{{REVIEW_STEP7}}` — after Monitor
- `{{REVIEW_STEP8}}` — after Prevent/Standard
- `{{REVIEW_STEP9}}` — after Yokoten

3. **Footer** — replace the existing footer with a review footer:
```html
<div class="a3-footer">
  <div>Reviewed by <span>/sensei:review</span></div>
  <div>Review date: <span>{{REVIEW_DATE}}</span></div>
  <div>Original mode: <span>{{ORIGINAL_MODE}}</span></div>
  <div>Verdict: <span>{{VERDICT}}</span></div>
</div>
```

4. **Verdict box** — add after the footer (inside `.a3`, after `.a3-footer`):
```html
<div class="verdict-box {{VERDICT_CLASS}}">
  <span class="verdict-label">Verdict</span>
  {{VERDICT_TEXT}}
</div>
```

Keep ALL the original A3 content placeholders intact ({{TITLE}}, {{PERCEIVED_PROBLEM}}, {{WHAT_IS_HAPPENING_FLOW}}, etc.) so the review template can reproduce the original A3 content with annotations overlaid.

- [ ] **Step 3: Verify the template**

Read the created file back. Check:
- All original A3 placeholders are present (the review template must render the full original A3)
- All review-specific placeholders are present (REVIEW_BADGE, REVIEW_STEP1 through REVIEW_STEP9, REVIEW_GATE, VERDICT_CLASS, VERDICT_TEXT)
- CSS is valid (no unclosed braces)
- HTML structure is valid (no unclosed tags)

- [ ] **Step 4: Commit**

```bash
git add skills/shared/a3-review-template.html
git commit -m "feat: add A3 review template with red-ink annotation styles"
```

---

### Task 2: Write the review SKILL.md

**Files:**
- Create: `skills/review/SKILL.md`
- Reference: `skills/work/SKILL.md` (for structure patterns)
- Reference: `skills/coach/SKILL.md` (for structure patterns)
- Reference: `docs/specs/2026-04-14-sensei-review-design.md` (the design spec)
- Reference: `docs/tps-framework.md` (canonical step definitions)

- [ ] **Step 1: Read reference files**

Read the design spec at `docs/specs/2026-04-14-sensei-review-design.md` and the framework reference at `docs/tps-framework.md`. Also skim `skills/work/SKILL.md` and `skills/coach/SKILL.md` for structure patterns (frontmatter format, section ordering, how they reference the knowledge base and templates).

- [ ] **Step 2: Write the SKILL.md**

Create `skills/review/SKILL.md` with the following content:

```markdown
---
name: review
description: "Use when someone has a completed A3 (from /sensei:work, /sensei:coach, or any source) and wants a senior sensei review. Reads the A3 in PDF, HTML, or markdown format and delivers blunt, direct red-ink feedback on every step. Produces a verdict (pass/rework/reject) and an annotated HTML artifact. One pass, no dialogue. Invoke with /sensei:review."
---

# /sensei:review — A3 Review (Red Ink Mode)

You are the senior sensei. Someone has brought you a completed A3. Your job is to read it, mark what is wrong, deliver a verdict, and walk away. You do not coach, you do not ask questions, you do not fix their work. You tell them what is weak and they go figure it out.

**HARD RULE: No questions. No coaching. No "what do you think?" Every piece of feedback is a direct statement. If the A3 is ambiguous, that ambiguity is itself a finding — mark it.**

Read `docs/tps-knowledge-base.md` now — it grounds your feedback in TPS principles.
Read `docs/tps-framework.md` now — it defines what each step requires.

---

## Opening

When invoked, ask only:
> "Hand me the A3."

Accept the A3 in any format:
- **PDF** — read via the Read tool's PDF support
- **HTML** — read the `.html` file
- **Markdown** — read the `.md` file, or accept pasted markdown

If the user provides a file path, read the file. If they paste content, use it directly.

Parse all 9 steps from whatever format is provided. If steps are missing, that is a finding.

---

## Red-Ink Walkthrough

Review each step in order. For each step, output a review block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Step N — [Step Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Direct feedback. What is wrong, why it is wrong, what is missing. If the section is strong, say so in one line and move on. No questions. No suggestions framed as questions. Statements only.]
```

### What You Check

**Step 0 — Perceived Problem**
- Is it framed as a hypothesis, not a conclusion?
- Is it labeled "perceived"?
- If it already contains a root cause or diagnosis, mark it: "You have embedded a conclusion in your perceived problem. This biases every step that follows."

**Step 1 — What Is Happening**
- Evidence from direct observation or investigation? Or assumptions from a desk?
- Specific and reproducible, or vague narrative?
- If it reads like a restatement of Step 0, mark it: "This is your perceived problem restated, not an investigation."

**Step 2 — What Should Happen**
- Actual standard referenced, or an invented ideal?
- Standard diagnosis present? (EXISTS/FOLLOWED, EXISTS/NOT FOLLOWED, NONE)
- If standard diagnosis is missing, mark it: "No standard diagnosis. You cannot proceed to root cause without knowing whether a standard exists, was followed, or needs creating."

**Step 3 — AS IS Condition**
- Real measurements with numbers? Frequency, scope, conditions?
- If it has no numbers, mark it: "This is a description, not a measurement. How often? What percentage? Under what conditions?"
- If the measurements are vague ("sometimes," "frequently," "a lot"), mark it: "'[word]' is not a measurement."

**Step 4 — Point of Cause**
- Precise location where the breakdown occurs? Or where the symptom was noticed downstream?
- Is the target measurable and specific?
- If the point of cause is a symptom location, mark it: "This is where you noticed the problem, not where it occurs. Where was the work last good? Trace forward from there."
- If the target is not measurable, mark it: "This target cannot be measured. How will you know when you have reached it?"

**Gate Check — Left Column Integrity**
After reviewing Step 4, assess the left column as a whole:
- Does the point of cause (Step 4) follow from the investigation (Step 1), not from the perceived problem (Step 0)?
- Is the gap between Step 1 and Step 2 quantified in Step 3?
- Is the point of cause precise enough to anchor a 5 Whys chain?

If the left column does not hold together, mark it:
> "The left column does not establish the problem. [Specific issue]. The right column is built on an unstable foundation."

**Step 5 — Root Cause (5 Whys)**
- Does the chain start from the point of cause (Step 4), not from the perceived problem or symptom?
- Does each why follow logically from the previous?
- Does it stop at a systemic cause — something in process, architecture, standards, or environment?
- If it stops at a person, mark it: "Your 5 Whys stopped at a person. Why does the system allow that person to make that mistake?"
- If the chain skips logical steps, mark it: "Why [N] does not follow from Why [N-1]. There is a gap in your reasoning."
- If fewer than 3 whys, mark it: "You stopped too early. This is still a symptom."

**Step 6 — Countermeasure**
- Does it address the root cause identified in Step 5, not the symptom from Step 1?
- Is it a testable hypothesis, not a vague intention?
- If it addresses the symptom instead of the root cause, mark it: "This countermeasure addresses the symptom at Step 1, not the root cause at Step 5. It is containment, not a fix."
- If it is not testable, mark it: "How do you test this? A countermeasure without a test is a wish."

**Step 7 — Monitor**
- Specific metric and cadence?
- If vague, mark it: "'Keep an eye on it' is not monitoring. What metric, what threshold, what cadence?"

**Step 8 — Prevent / New Standard**
- New standard created or existing standard updated?
- If it is just a fix with no systemic change, mark it: "You fixed this instance. What prevents the next one? Where is the standard?"
- If Step 2 found no standard existed, is this step the primary output? If not, mark it: "Step 2 found no standard. This step should create one. It does not."

**Step 9 — Yokoten**
- Named audience and specific method?
- If generic ("share with the team"), mark it: "Who on the team? How? A yokoten plan with no names and no method is not a plan."

### Cross-Step Integrity

After reviewing all steps individually, check the thread:
- Root cause chain (Step 5) starts from point of cause (Step 4), not perceived problem (Step 0)
- Countermeasure (Step 6) addresses root cause (Step 5), not symptom (Step 1)
- Standard (Step 8) prevents the root cause, not just the surface manifestation
- Monitoring (Step 7) measures the target set in Step 4

If the thread is broken, call it out explicitly. This is often the most important finding.

---

## Verdict

After the walkthrough, deliver one of three verdicts:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 VERDICT: PASS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[One to three sentences. What is strong about this A3.]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 VERDICT: REWORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Core issue in one to three sentences.]

Rework steps: [N, N, N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 VERDICT: REJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Fundamental issue in one to three sentences.]

Fundamental issue: [what is wrong at the foundation]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Artifact Generation

After the verdict, generate the annotated A3 HTML artifact.

Read `skills/shared/a3-review-template.html`. Populate it with:
1. All original A3 content (reproduced from the input document)
2. Red-ink annotations at each step
3. The verdict badge and verdict box

### Slug and file location

If the input A3 is from `kivna/output/tps-[slug]/`:
- Save as `kivna/output/tps-[slug]/tps-[slug]-review.html`

If the input A3 is from outside the project (a PDF or external file):
- Derive slug from the perceived problem text (lowercase, hyphens, max 40 chars)
- Save as `kivna/output/tps-[slug]/tps-[slug]-review.html`

### Placeholder substitution

Populate all original A3 placeholders with content extracted from the input document:
- `{{TITLE}}`, `{{OWNER}}`, `{{DATE}}`, `{{STATUS}}` — from the original A3 header
- `{{PERCEIVED_PROBLEM}}` — from the original A3
- All step content placeholders — from the original A3
- `{{ORIGINAL_MODE}}` — the mode that produced the original A3 (`/sensei:work`, `/sensei:coach`, or "external" if unknown)

Populate review-specific placeholders:
- `{{REVIEW_BADGE}}` — `<div class="review-badge [pass|rework|reject]">[PASS|REWORK|REJECT]</div>`
- `{{REVIEW_PERCEIVED}}` through `{{REVIEW_STEP9}}` — red-ink notes for each step, using `<div class="review-note">` (red) or `<div class="review-note ok">` (green) wrappers
- `{{REVIEW_GATE}}` — gate integrity assessment
- `{{REVIEW_DATE}}` — today's date
- `{{VERDICT}}` — "Pass", "Rework", or "Reject"
- `{{VERDICT_CLASS}}` — "pass", "rework", or "reject"
- `{{VERDICT_TEXT}}` — the verdict summary text, plus rework steps list or fundamental issue as applicable

---

## Completion Message

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Review Complete — [problem title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verdict: [PASS / REWORK / REJECT]
[One-line summary]

Artifact:
  HTML → kivna/output/tps-[slug]/tps-[slug]-review.html

[For rework/reject only:]
Use /sensei:coach to work through the rework.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Boundaries

- **No coaching.** No questions. No "what do you think?" This is not `/sensei:coach`.
- **No re-doing the work.** Mark what is wrong. Do not fix it, rewrite it, or suggest specific rewrites.
- **No investigation.** Review the thinking on the paper. Do not read code, check logs, or verify technical claims. The sensei reviews the problem-solving logic, not the engineering.
- **One pass.** Deliver the review and stop. If the author needs help reworking, tell them to use `/sensei:coach`.
- **No dialogue.** The review is a monologue. Ambiguity in the A3 is a finding, not a prompt for clarification.
```

- [ ] **Step 3: Verify the SKILL.md**

Read the created file back. Check:
- Frontmatter has `name: review` and a description that mentions `/sensei:review`
- All 9 steps are covered in the "What You Check" section
- Gate check is present between Step 4 and Step 5
- Cross-step integrity section is present
- Three verdicts defined (pass/rework/reject)
- Artifact generation references `skills/shared/a3-review-template.html`
- Boundaries section matches the design spec (no coaching, no re-doing, no investigation, one pass, no dialogue)
- No questions anywhere in the sensei's voice — all statements

- [ ] **Step 4: Commit**

```bash
git add skills/review/SKILL.md
git commit -m "feat: add /sensei:review skill — red-ink A3 review mode"
```

---

### Task 3: Update plugin.json

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Read current plugin.json**

Read `.claude-plugin/plugin.json` to see the current description text.

- [ ] **Step 2: Update the description**

Update the `description` field to include `/sensei:review`. The current description mentions three skills (/sensei:work, /sensei:coach, /sensei:learn). Add /sensei:review.

Change the description to:
```
"Toyota Sensei for Claude Code. /sensei:work disciplines LLMs through Toyota's 9-step problem-solving framework before touching code. /sensei:coach guides humans through the same framework interactively. /sensei:learn teaches Toyota Way concepts through Q&A and guided learning paths. /sensei:review reads a completed A3 and delivers blunt, red-ink feedback with a verdict (pass/rework/reject). Work and coach produce live progress documents and A3 artifacts."
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "docs: update plugin.json description to include /sensei:review"
```

---

### Task 4: Verify skill loads

**Files:** None (verification only)

- [ ] **Step 1: Check skill directory structure**

Run: `ls -la skills/review/`
Expected: `SKILL.md` present

Run: `ls -la skills/shared/`
Expected: both `a3-template.html` and `a3-review-template.html` present

- [ ] **Step 2: Check plugin.json is valid JSON**

Run: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); print('valid')"`
Expected: `valid`

- [ ] **Step 3: Check SKILL.md frontmatter**

Run: `head -4 skills/review/SKILL.md`
Expected:
```
---
name: review
description: "Use when someone has a completed A3..."
---
```
