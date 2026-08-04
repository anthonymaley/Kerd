# TPS Problem-Solving Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build two Claude Code skills — `/tps:solve` (LLM discipline mode) and `/tps:coach` (human coaching mode) — that enforce Toyota's 9-step Practical Problem Solving (PPS) framework, produce a live progress document at each step, and generate a final A3 HTML + markdown artifact.

**Architecture:** The PPS repo is structured as a Claude Code plugin with namespace `tps`. Both skills share an A3 HTML template file and reference `docs/tps-knowledge-base.md` for insights. The plugin is registered locally so `/tps:solve` and `/tps:coach` are available in any Claude Code session.

**Tech Stack:** Claude Code plugin system, SKILL.md skill definitions, HTML/CSS (no JS framework), markdown.

---

## File Map

```
.claude-plugin/
  plugin.json               ← plugin manifest (name: "tps")
  marketplace.json          ← minimal marketplace metadata

skills/
  tps/
    shared/
      a3-template.html      ← A3 output template (used by both skills)
    solve/
      SKILL.md              ← /tps:solve skill definition
    coach/
      SKILL.md              ← /tps:coach skill definition

kivna/output/               ← gitignored, where artifacts are written
  pps-[slug]/
    pps-[slug].html
    pps-[slug].md
```

Reference files (already exist, read by skills):
- `docs/tps-knowledge-base.md` — TPS concepts and quotes
- `docs/pps-framework.md` canonical 9-step framework

---

## Task 1: Plugin Manifest

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Create `.claude-plugin/` directory and `plugin.json`**

```json
{
  "name": "tps",
  "description": "Toyota Production System problem-solving skills: /tps:solve disciplines LLMs through the 9-step TPS framework before touching code; /tps:coach guides humans through the same framework interactively. Both produce live progress documents and final A3 artifacts.",
  "version": "1.0.0",
  "author": {
    "name": "Anthony Maley"
  },
  "keywords": ["tps", "lean", "problem-solving", "a3", "toyota", "coaching"]
}
```

- [ ] **Step 2: Create `.claude-plugin/marketplace.json`**

```json
{
  "metadata": {
    "name": "tps",
    "version": "1.0.0",
    "description": "TPS problem-solving skills for Claude Code"
  },
  "plugins": [
    {
      "name": "tps",
      "version": "1.0.0",
      "description": "Toyota Production System problem-solving: /tps:solve and /tps:coach"
    }
  ]
}
```

- [ ] **Step 3: Create `skills/tps/shared/` and `skills/tps/solve/` and `skills/tps/coach/` directories**

```bash
mkdir -p skills/tps/shared skills/tps/solve skills/tps/coach
```

- [ ] **Step 4: Register the plugin locally**

```bash
# Check current Claude Code plugin install command
claude plugin install . 2>/dev/null || echo "Use Claude Code settings to register local plugin at: $(pwd)"
```

If `claude plugin install .` works, run it from the repo root. If not, open Claude Code settings → Plugins → Add local plugin → point to this directory. The namespace will be `tps` (from plugin.json `name` field).

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/ skills/
git commit -m "feat: add tps plugin manifest and skill directory structure"
```

---

## Task 2: A3 HTML Template

**Files:**
- Create: `skills/tps/shared/a3-template.html`

This template is the final A3 artifact. Both skills generate it on completion by substituting `{{PLACEHOLDER}}` values. It uses inline CSS only — no external dependencies.

- [ ] **Step 1: Create `skills/tps/shared/a3-template.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PPS A3 — {{PERCEIVED_PROBLEM_SLUG}}</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f0; color: #1a1a1a; padding: 16px; font-size: 12px; }
.a3 { background: white; border: 1px solid #ccc; max-width: 1100px; margin: 0 auto; box-shadow: 0 2px 12px rgba(0,0,0,0.12); }
.a3-header { background: #1a1a2e; color: white; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; }
.a3-header h1 { font-size: 14px; font-weight: 600; }
.a3-header .meta { font-size: 10px; color: #aaa; text-align: right; line-height: 1.6; }
.perceived-banner { background: #f8f4e8; border-bottom: 2px solid #e8a020; padding: 7px 16px; font-size: 11px; }
.perceived-banner strong { color: #b07010; text-transform: uppercase; font-size: 9px; letter-spacing: 1px; margin-right: 6px; }
.a3-body { display: grid; grid-template-columns: 1fr 1fr; }
.col { padding: 14px 16px; }
.col-left { border-right: 2px solid #ddd; }
.col-heading { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px; padding-bottom: 5px; border-bottom: 2px solid; }
.col-left .col-heading { color: #1a6eb5; border-color: #1a6eb5; }
.col-right .col-heading { color: #c05a00; border-color: #c05a00; }
.section { margin-bottom: 14px; }
.section-label { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #666; margin-bottom: 5px; }
.section-text { font-size: 11px; line-height: 1.6; color: #222; }
.flow { display: flex; align-items: center; gap: 0; margin: 6px 0; flex-wrap: wrap; gap: 2px; }
.flow-box { border: 1.5px solid #1a6eb5; border-radius: 4px; padding: 5px 8px; font-size: 10px; font-weight: 600; color: #1a3a6e; background: #e8f0fb; text-align: center; min-width: 72px; }
.flow-box.green { background: #e6f9ee; border-color: #1a8a40; color: #0d4a20; }
.flow-box.red { background: #fde8e8; border-color: #c0392b; color: #7a1010; }
.flow-box.orange { background: #fef3e2; border-color: #e67e22; color: #7a3d00; }
.flow-arrow { font-size: 14px; color: #999; margin: 0 2px; flex-shrink: 0; }
.flow-arrow.red { color: #c0392b; }
.process-label { font-size: 9px; color: #888; margin-bottom: 3px; font-style: italic; }
.poc-box { border: 2px solid #c0392b; border-radius: 5px; padding: 8px 10px; background: #fff8f8; margin-top: 6px; }
.poc-box .poc-label { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #c0392b; margin-bottom: 5px; }
.poc-box .poc-should { color: #1a8a40; font-size: 11px; margin-bottom: 4px; }
.poc-box .poc-actual { color: #c0392b; font-size: 11px; }
.tag { display: inline-flex; align-items: center; gap: 4px; border-radius: 3px; padding: 2px 7px; font-size: 10px; font-weight: 600; margin: 3px 3px 3px 0; }
.tag.measure { background: #e6f9ee; border: 1px solid #27ae60; color: #0d5a20; }
.tag.target { background: #fde8e8; border: 1px solid #c0392b; color: #7a1010; }
.tag.verified { background: #e8f0fb; border: 1px solid #1a6eb5; color: #1a3a6e; }
.tag.no-standard { background: #fff3cd; border: 1px solid #e67e22; color: #7a3d00; }
.why-tree { margin: 4px 0; }
.why-row { display: flex; align-items: flex-start; margin-bottom: 6px; }
.why-num { color: white; border-radius: 50%; width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 700; flex-shrink: 0; margin-top: 1px; }
.why-num.w1 { background: #c0392b; }
.why-num.w2 { background: #e67e22; }
.why-num.w3 { background: #d4ac0d; color: #333; }
.why-num.w4 { background: #27ae60; }
.why-num.w5 { background: #1a6eb5; }
.why-text { border-left: 2px solid #eee; padding-left: 8px; margin-left: 6px; font-size: 11px; line-height: 1.4; color: #222; }
.why-answer { font-size: 10px; color: #555; font-style: italic; margin-top: 2px; }
.root-cause-box { background: #1a1a2e; color: white; border-radius: 4px; padding: 8px 12px; font-size: 11px; font-weight: 600; margin-top: 8px; line-height: 1.5; }
.root-cause-box .label { font-size: 8px; font-weight: 400; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 3px; }
.cm-card { border: 1.5px solid #ddd; border-radius: 5px; padding: 9px 10px 9px 14px; margin-bottom: 8px; position: relative; }
.cm-card .cm-num { position: absolute; top: -8px; left: 8px; background: #c05a00; color: white; border-radius: 50%; width: 17px; height: 17px; font-size: 9px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.cm-card .cm-title { font-size: 11px; font-weight: 700; color: #222; margin-bottom: 3px; }
.cm-card .cm-body { font-size: 11px; color: #444; line-height: 1.5; }
.cm-card.verified { border-color: #27ae60; background: #f6fdf9; }
.cm-card.verified .cm-num { background: #27ae60; }
hr.div { border: none; border-top: 1px solid #eee; margin: 12px 0; }
.a3-footer { background: #f8f8f8; border-top: 1px solid #ddd; padding: 7px 16px; display: flex; gap: 20px; flex-wrap: wrap; font-size: 10px; color: #888; }
.a3-footer span { color: #444; font-weight: 600; }
@media print {
  body { background: white; padding: 0; }
  .a3 { box-shadow: none; border: 1px solid #999; }
}
</style>
</head>
<body>
<div class="a3">

  <div class="a3-header">
    <h1>{{TITLE}}</h1>
    <div class="meta">Owner: {{OWNER}} &nbsp;·&nbsp; {{DATE}}<br>Mode: {{MODE}} &nbsp;·&nbsp; Status: {{STATUS}}</div>
  </div>

  <div class="perceived-banner">
    <strong>Perceived Problem:</strong> {{PERCEIVED_PROBLEM}}
  </div>

  <div class="a3-body">

    <div class="col col-left">
      <div class="col-heading">◀ Understand the Problem</div>

      <div class="section">
        <div class="section-label">What Is Happening</div>
        {{WHAT_IS_HAPPENING_FLOW}}
        <div class="section-text">{{WHAT_IS_HAPPENING_TEXT}}</div>
      </div>

      <hr class="div">

      <div class="section">
        <div class="section-label">What Should Happen</div>
        {{WHAT_SHOULD_HAPPEN_FLOW}}
        <div class="section-text">{{WHAT_SHOULD_HAPPEN_TEXT}}</div>
        {{STANDARD_BADGE}}
      </div>

      <hr class="div">

      <div class="section">
        <div class="section-label">AS IS Condition</div>
        <div class="section-text">{{AS_IS_TEXT}}</div>
        {{AS_IS_MEASUREMENTS}}
      </div>

      <hr class="div">

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
    </div>

    <div class="col col-right">
      <div class="col-heading">▶ Resolve</div>

      <div class="section">
        <div class="section-label">Root Cause — 5 Whys</div>
        <div class="why-tree">
          {{WHY_CHAIN}}
          <div class="root-cause-box">
            <span class="label">Root Cause</span>
            {{ROOT_CAUSE}}
          </div>
        </div>
      </div>

      <hr class="div">

      <div class="section">
        <div class="section-label">Countermeasures</div>
        {{COUNTERMEASURES}}
        {{VERIFICATION_MEASUREMENT}}
      </div>

      <hr class="div">

      <div class="section">
        <div class="section-label">How to Check / Monitor</div>
        <div class="section-text">{{MONITOR_TEXT}}</div>
      </div>

      <hr class="div">

      <div class="section">
        <div class="section-label">Prevent / New Standard</div>
        <div class="section-text">{{PREVENT_TEXT}}</div>
        {{NEW_STANDARD_BADGE}}
      </div>

      <hr class="div">

      <div class="section">
        <div class="section-label">Yokoten — Knowledge Share</div>
        {{YOKOTEN_FLOW}}
        <div class="section-text">{{YOKOTEN_TEXT}}</div>
      </div>

    </div>
  </div>

  <div class="a3-footer">
    <div>Generated by <span>{{MODE}}</span></div>
    <div>Date: <span>{{DATE}}</span></div>
    <div>Steps challenged: <span>{{CHALLENGED_STEPS}}</span></div>
    <div>Time to countermeasure: <span>{{TIME_TO_CM}}</span></div>
    {{CONCEPTS_SURFACED}}
  </div>

</div>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add skills/tps/shared/a3-template.html
git commit -m "feat: add A3 HTML output template"
```

---

## Task 3: `/tps:solve` Skill

**Files:**
- Create: `skills/tps/solve/SKILL.md`

- [ ] **Step 1: Create `skills/tps/solve/SKILL.md`**

```markdown
---
name: solve
description: "Use when an LLM is about to solve a problem, fix a bug, or address something that isn't working correctly. Forces the LLM through Anthony Maley's 9-step TPS problem-solving framework — building a live progress document throughout — before proposing any countermeasure or touching any code. Prevents the jump-to-solution failure mode."
---

# /tps:solve — TPS Problem-Solving (LLM Discipline Mode)

You are being put on rails. A problem has been reported. Before you write a single line of code, make a single change, or propose a single fix, you will work through the full TPS 9-step framework below.

**HARD RULE: Do not propose any code changes, fixes, or countermeasures until Step 6. If you identify what looks like the fix during investigation, hold it. The discipline is the point.**

Read `docs/tps-knowledge-base.md` before starting — it contains the TPS concepts and quotes you will surface at each step.

---

## Opening

State clearly:
> "Before I make any changes, I'm going to work through this properly using the TPS problem-solving framework. This will take a few minutes but will prevent us from chasing the wrong fix. Let me start by understanding what's actually happening."

Capture the perceived problem from what the user said. Label it explicitly as "perceived" — it is a hypothesis, not a fact.

---

## Live Progress Document

After each confirmed step, output a formatted progress block. Update it in place (output the full block each time so the human can see the current state).

Format:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PPS Progress — [Perceived Problem Short Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[PERCEIVED PROBLEM]
[text]

✓ Step 1 — What Is Happening
  [confirmed content]

✓ Step 2 — What Should Happen  [STANDARD: EXISTS/NOT FOLLOWED | EXISTS/FOLLOWED | NONE — creating now]
  [confirmed content]

▶ Step 3 — AS IS Condition  ← active
  [in progress content]

  Step 4 — Point of Cause + Target          (locked)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 5 — Root Cause                        (locked — complete left column first)
  Step 6 — Countermeasure
  Step 7 — Monitor
  Step 8 — Prevent / New Standard
  Step 9 — Yokoten
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## The 9 Steps

### STEP 0 — Perceived Problem
Extract from what the user said. If not clear, ask: "What's the problem you're seeing?"
Output: `[PERCEIVED PROBLEM] [text]`

---

### STEP 1 — What Is Happening

**TPS Insight to share:**
> *"Taiichi Ohno drew a circle on the shop floor and made students stand in it for hours — observing without explanation. Truth lives at the gemba, not in a report. When a hospital tried to solve a patient response-time problem in a conference room, intelligent people fabricated root causes that were completely wrong. Going to see revealed the real causes in minutes."*

**Your job:** Investigate before describing. Read the relevant code, check logs, reproduce the condition if possible. Do not describe what you *think* is happening from the problem statement alone.

Investigate:
- Read the relevant files
- Check for error messages, logs, or test output
- Attempt to trace the failure path in the code

Then present your findings as a **draft**:
> "Here's what I found for Step 1. [Description of the actual observed behavior based on investigation.] Does this match what you're seeing? Anything to correct?"

**Wait for confirmation before proceeding.**

---

### STEP 2 — What Should Happen + Standard Diagnosis

**TPS Insight to share:**
> *"At Toyota, the first question when any defect is found is: 'Was standardized work followed?' If no → correct the behavior. If yes and defects still occur → improve the standard. If no standard exists, that is the finding — creating one becomes the most important countermeasure. Henry Ford: 'If you think of standardization as the best you know today, but which is to be improved tomorrow — you get somewhere.'"*

**Standard diagnosis — explicitly surface one of:**
- `[STANDARD: EXISTS / FOLLOWED]` → The standard was followed but failed. 5 Whys will focus on why the standard itself is insufficient.
- `[STANDARD: EXISTS / NOT FOLLOWED]` → There is a known correct behavior but it wasn't followed. 5 Whys focuses on why it wasn't followed.
- `[STANDARD: NONE — creating now]` → No documented standard exists. This is a discovery. Step 8 becomes the primary output.

Present draft:
> "Step 2 draft: [What should happen based on code/spec/docs]. Standard status: [one of the three above]. Does this match the expected behavior? Correct if needed."

**Wait for confirmation before proceeding.**

---

### STEP 3 — AS IS Condition

**TPS Insight to share:**
> *"Visual management at Toyota means any deviation from standard is immediately visible to anyone walking through — no special knowledge required. Without measurement, 'there's a problem' is an opinion. With it, it becomes a fact that demands action."*

Quantify the gap. Investigate:
- How often does this occur? Under what conditions?
- What is the scope — all users, specific paths, specific environments?
- Is there a measurable metric (error rate, failure rate, frequency)?

Present draft with measurements:
> "Step 3 draft: [Gap description]. Measurement: [specific data]. Does this capture the scale correctly?"

**Wait for confirmation before proceeding.**

---

### STEP 4 — Point of Cause + Target (THE GATE)

**TPS Insight to share:**
> *"Jidoka — Toyota's right pillar — is built on one principle: stop and fix at the source. The andon cord is pulled not where the problem is discovered downstream, but at the workstation where it occurs. Finding the point of cause is the discipline of asking 'where was the work last good?' — and tracing forward to the exact moment it breaks. Without this precision, 5 Whys starts from the wrong place and leads to the wrong root cause every time."*

Identify:
- The exact file, function, component, or step where the breakdown occurs
- NOT where the symptom appears — where it originates
- The specific mechanism: what should happen at that location vs. what actually happens

Present draft:
> "Step 4 draft: The breakdown occurs in [specific location]. At that point: should [X], actually [Y]. Target: [measurable definition of fixed]. Is this the right point of cause? This is the gate — I will not proceed to root cause until you confirm."

**EXPLICIT GATE:** Do not proceed until the user confirms. State:
> "**Left column complete.** Point of cause: [X]. Target: [Y]. Confirming before I touch any code or proceed to root cause analysis — does this look correct?"

---

### STEP 5 — Root Cause — 5 Whys

**TPS Insight to share:**
> *"Ohno's oil spill example: oil on floor → gasket failed → wrong gasket → not specified → purchasing agent untrained → evaluation criteria wrong. The fix at the root changed purchasing agent evaluation. A surface fix would have recurred indefinitely. Warning: when people are defensive, 5 Whys becomes 5 Whos — finding blame instead of system causes. Always focus on the system, never the individual."*

Start from the Point of Cause confirmed in Step 4. Ask why iteratively:
- Why does [Point of Cause] happen?
- Why does [answer 1] happen?
- Continue until you reach a systemic cause — something in the process, architecture, or configuration that allowed this failure class to occur

Surface the 5-why chain:
```
W1: [symptom at point of cause] → because [answer]
W2: [answer 1] → because [answer]
W3: [answer 2] → because [answer]
W4: [answer 3] → because [answer]
W5: [answer 4] → because [systemic root cause]

Root cause: [systemic statement]
```

Ask: "Does this why chain look right? Is the root cause systemic enough — or does it still feel like a symptom?"

**Wait for confirmation before proceeding.**

---

### STEP 6 — Countermeasure + Plan

**TPS Insight to share:**
> *"Toyota forbids the word 'solution.' There are only countermeasures — hypotheses that might reduce the gap. A countermeasure proven effective becomes a standard — 'the best we know today until we find a better one.' The distinction matters: calling something a solution closes inquiry. Calling it a countermeasure keeps the PDCA loop open."*

Now — and only now — propose the countermeasure(s).

Format as numbered items:
```
Countermeasure 1: [specific action] — addresses [which why]
Countermeasure 2: [specific action] — addresses root cause
```

For each, specify:
- What exactly will change
- What measurement will confirm it's working
- Whether this is a short-term containment or root-cause fix

Ask: "Do these countermeasures address the root cause? Should we adjust before I implement?"

**Wait for confirmation, then implement.**

---

### STEP 7 — How to Monitor

**TPS Insight to share:**
> *"'We can't afford to have PDCA that takes three weeks anymore. We want a PDCA done before the end of that shift.' The Check step is not a formality — it is how you know whether your hypothesis was correct. A countermeasure that 'seems to be working' is not verified. Only measurement confirms."*

After implementing: define how to verify the fix held.
- What specific test, metric, or observation confirms the countermeasure worked?
- Run it. Show the result.

Output:
> "Verification: [what was checked]. Result: [measured outcome]. Target was [X] — actual is now [Y]. ✓ Confirmed / ✗ Not yet resolved."

---

### STEP 8 — Prevent / New Standard

**TPS Insight to share:**
> *"'Standardized work is today's best-known way, which can be improved tomorrow.' When a countermeasure proves effective, it becomes the new standard — not filed away, but visible at the point of work. If no standard existed (Step 2 finding), this is the primary output: you are closing a structural gap that allowed this entire class of problem to occur."*

Define the standard:
- What new process, check, test, or configuration prevents recurrence?
- If Step 2 found no standard: write the standard explicitly
- If Step 2 found standard not followed: propose why it wasn't followed and how to ensure it is

Output the standard text clearly so it can be documented.

---

### STEP 9 — Yokoten (Knowledge Share)

**TPS Insight to share:**
> *"Yokoten means 'across everywhere' — horizontal, peer-to-peer knowledge transfer. At Toyota, the learner is not done until the new process is shared with others who might benefit. Yokoten is not 'copy exactly' — people go see how another area solved the problem, then adapt with their own wisdom. The process is not complete at Step 8."*

Suggest:
- Who else on the team should know about this?
- Where should the fix / new standard be documented?
- Is there a related area with the same vulnerability?

---

## Contextual TPS Concept Suggestions

During the process, watch for these patterns and surface the relevant concept as a non-blocking insight. Surface at the indicated step, after confirming that step's content.

| Pattern | Concept | When |
|---|---|---|
| Uneven workload, bursty demand, batch processing | **Heijunka** (Production Leveling) | Step 3-4 |
| Cluttered process, things hard to find, disorganized | **5S** | Step 4 |
| Recurring human/operator error, wrong step skipped | **Poka-Yoke** (Error Proofing) | Step 5-8 |
| Defect discovered downstream from where it occurred | **Jidoka** (In-Station Quality) | Step 4 |
| Team or process overloaded beyond capacity | **Muri** (Overburden) | Step 3 |
| Irregular demand creating chaos downstream | **Mura** (Unevenness) | Step 3 |
| Non-value-added steps, waiting, unnecessary motion | **Muda** / 7 Wastes | Step 1-4 |
| Large batches sitting idle, high WIP | **One-Piece Flow / JIT** | Step 4 |
| Fix keeps slipping back after implementation | **SDCA** | Step 8 |

Format for concept suggestions:
> 💡 **TPS Concept: [Name]** — [one-sentence hook]. [2-3 sentences from tps-knowledge-base.md explaining why it's relevant to what was just discovered.]

---

## Artifact Generation

On completing Step 9, generate two output files. Create `kivna/output/` directory if it doesn't exist.

**Slug:** Derive from the perceived problem — lowercase, hyphens, max 40 chars. E.g., "thumbnails-not-displaying-prod"

### 1. HTML A3 — `kivna/output/pps-[slug].html`

Read `skills/tps/shared/a3-template.html`. Substitute all `{{PLACEHOLDER}}` values with the content confirmed at each step.

For flow diagrams, generate HTML using these classes from the template:
- Normal path boxes: `<div class="flow-box green">Label</div>`
- Failure path boxes: `<div class="flow-box red">Label</div>`
- Arrows: `<span class="flow-arrow">→</span>` (red arrows: `class="flow-arrow red"`)

For the 5 Whys chain, generate:
```html
<div class="why-row">
  <div class="why-num w1">1</div>
  <div class="why-text">[Why question / observation]
    <div class="why-answer">→ [Answer / because]</div>
  </div>
</div>
```
Use w1-w5 classes for color coding.

For countermeasure cards:
```html
<div class="cm-card verified">  <!-- or cm-card if not yet verified -->
  <div class="cm-num">1</div>
  <div class="cm-title">[Countermeasure title]</div>
  <div class="cm-body">[Detail]</div>
</div>
```

Standard badge (Step 2 finding):
- No standard: `<span class="tag no-standard">⚠ No Standard Found — Created in Step 8</span>`
- Not followed: `<span class="tag no-standard">⚠ Standard Not Followed</span>`
- Followed: omit badge

Footer values:
- `{{MODE}}`: `/tps:solve`
- `{{CHALLENGED_STEPS}}`: list any steps the user corrected (e.g., "Step 4 revised once")
- `{{TIME_TO_CM}}`: approximate time from start to Step 6
- `{{CONCEPTS_SURFACED}}`: TPS concepts suggested during the process

### 2. Markdown — `kivna/output/pps-[slug].md`

```markdown
# PPS Report: [Perceived Problem]

**Date:** [date]
**Owner:** [user or "LLM-assisted"]
**Mode:** /tps:solve
**Status:** [Countermeasure verified / In progress]

---

## Perceived Problem
[text]

## Left Column — Understand

### What Is Happening
[text]

### What Should Happen
**Standard:** [EXISTS/FOLLOWED | EXISTS/NOT FOLLOWED | NONE — created in Step 8]
[text]

### AS IS Condition
[text]
**Measurement:** [data]

### Point of Cause
**Location:** [specific file/component/step]
**Should:** [expected behavior]
**Actual:** [actual behavior]
**Target:** [measurable definition of fixed]

---

## Right Column — Resolve

### Root Cause — 5 Whys
1. [W1]
2. [W2]
3. [W3]
4. [W4]
5. [W5]

**Root Cause:** [systemic statement]

### Countermeasures
1. [CM1 — status]
2. [CM2 — status]

**Verification:** [measurement result]

### How to Monitor
[text]

### Prevent / New Standard
[text]

### Yokoten — Knowledge Share
[text]

---

## TPS Concepts Surfaced
[list of concepts suggested during the process, if any]
```

---

## Completion Message

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PPS Complete — [Perceived Problem Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ All 9 steps confirmed
✓ Countermeasure: [CM title] — [verified/pending]
✓ Standard: [new/updated/restored]

Artifacts:
  HTML: kivna/output/pps-[slug].html
  Markdown: kivna/output/pps-[slug].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

- [ ] **Step 2: Commit**

```bash
git add skills/tps/solve/SKILL.md
git commit -m "feat: add /tps:solve LLM discipline skill"
```

---

## Task 4: `/tps:coach` Skill

**Files:**
- Create: `skills/tps/coach/SKILL.md`

- [ ] **Step 1: Create `skills/tps/coach/SKILL.md`**

```markdown
---
name: coach
description: "Use when a human wants to work through a problem using the TPS problem-solving framework. Claude acts as sensei — asking coaching questions to draw out the human's thinking at each step, never providing answers, building a live progress document throughout, and generating a final A3 artifact on completion. For any problem type: technical, business, process, or personal."
---

# /tps:coach — TPS Problem-Solving (Human Coaching Mode)

You are the sensei. Your job is to draw out the human's thinking — not to provide answers. Ask one question at a time. Reflect back what you hear. Challenge thin answers. Never fill in the blank for them.

Read `docs/tps-knowledge-base.md` before starting.

---

## Sensei Rules (enforce throughout)

1. **One question per turn.** Never ask two questions in one message.
2. **Reflect before advancing.** Before moving to the next step: "So what you're saying is [X]. Is that right?"
3. **Challenge thin answers.** If the answer is still a symptom: "That's still describing what you see. Why does [X] happen?"
4. **Never fill in the answer.** If they're stuck, give a prompt — not the answer: "Think about where in the process the work was last correct."
5. **Praise specific, accurate answers.** Brief recognition when a step is solid: "Good — that's the point of cause. Let's lock that in."
6. **The document is the artifact.** Update the progress block after every confirmed step so the human can see their own thinking taking shape.

---

## Opening

> "Let's work through this together using the TPS problem-solving framework. We'll go step by step — I'll ask questions, you'll do the thinking, and we'll build a document as we go that you can share when we're done.
>
> What problem are you facing?"

Capture the answer as the Perceived Problem. Reflect it back:
> "So the perceived problem is: [restatement]. That's our starting point — we're calling it 'perceived' because the real problem often turns out to be different once we dig in. Ready to start?"

---

## Live Progress Document

Same format as /tps:solve. Update after every confirmed step.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PPS Progress — [Perceived Problem Short Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[PERCEIVED PROBLEM]
[text]

✓ Step 1 — What Is Happening
  [confirmed content]

▶ Step 2 — What Should Happen  ← active
  ...

  Step 3 — AS IS Condition                  (locked)
  Step 4 — Point of Cause + Target          (locked)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 5 — Root Cause                        (locked — complete left column first)
  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## The 9 Steps

### STEP 1 — What Is Happening (Genchi Genbutsu)

**Share insight first:**
> 💬 *"Before we describe the problem, I want to make sure we're working from direct observation — not a report or assumption. Taiichi Ohno made his students stand in a circle drawn on the shop floor for hours, just observing. He called it 'going to the gemba' — the actual place. When teams try to solve problems in a conference room without going to see, they consistently fabricate root causes. So: have you gone and seen this yourself?"*

**Coaching question:**
> "Describe exactly what you observed directly — not what someone told you, not what a dashboard shows. What did you see, hear, or reproduce with your own hands?"

Follow-up if vague: "Can you be more specific? What is the exact behavior?"
Follow-up if secondhand: "That's what someone told you. Have you gone and seen it yourself? If not, that's your next step before we continue."

Reflect and confirm before moving on.

---

### STEP 2 — What Should Happen + Standard Diagnosis

**Share insight:**
> 💬 *"At Toyota, the first question when any defect is found is: 'Was standardized work followed?' This surfaces three possible situations: the standard was followed and still failed (the standard is wrong), the standard exists but wasn't followed (a deviation problem), or no standard exists (a gap to close). Each leads to a different countermeasure."*

**Coaching question:**
> "What should happen instead? And — is there a documented standard or expected process for this? If yes: what does it say? If no: that's important — we'll define what correct looks like right now."

After answering, surface the standard diagnosis:
- "So the standard exists and was followed — good. That tells us the standard itself may need improving."
- "The standard exists but wasn't followed. We'll need to understand why."
- "No standard exists. That's a significant finding — creating one will be part of our countermeasure."

Tag the finding in the progress document: `[STANDARD: EXISTS/FOLLOWED | EXISTS/NOT FOLLOWED | NONE]`

---

### STEP 3 — AS IS Condition

**Share insight:**
> 💬 *"'Without measurement, there's a problem' is an opinion. With measurement, it's a fact that demands action. Toyota's visual management makes every deviation immediately countable — inventory outside its marked boundary, a board behind schedule, an error rate above zero. We need that same clarity here."*

**Coaching question:**
> "How do you *know* this is a problem? What's the measurement — how often does it happen, how many people are affected, what's the rate or volume?"

If they can't measure it yet: "That's worth noting. Part of our countermeasure may be establishing how to measure this. What's your best estimate right now?"

---

### STEP 4 — Point of Cause + Target (THE GATE)

**Share insight:**
> 💬 *"Jidoka — Toyota's quality pillar — is built on one principle: stop and fix at the source. The andon cord is pulled not where the defect is discovered, but where it originates. The discipline here is asking: 'Where was the work last good?' — then tracing forward to the exact moment it breaks. If we start our 5 Whys from the symptom instead of the point of cause, we'll end up fixing the wrong thing."*

**Coaching question (point of cause):**
> "Where exactly does the breakdown occur? Not where you discover the problem — where it actually happens. Can you point to the specific step, component, person, or handoff where it should work but doesn't?"

If vague: "You've described where you *notice* it. Where does it *start*? Where was the last point where things were working correctly?"

**Coaching question (target):**
> "What does 'fixed' look like, measured? How will you know when you've hit the target?"

**GATE:** Confirm explicitly:
> "Left column complete. Point of cause: [X]. Target: [Y]. Before we move to root cause — does this feel right? Once we cross this line, we're committing to solving this specific problem at this specific location."

---

### STEP 5 — Root Cause — 5 Whys

**Share insight:**
> 💬 *"Ohno's original five whys: oil on the floor → gasket failed → wrong gasket spec → purchasing agent untrained → evaluation criteria don't require technical knowledge. The fix changed how purchasing agents are evaluated — not the gasket. A surface fix would have recurred forever. One warning: under pressure, five whys becomes five whos — blame-finding. We stay focused on the system, never the person."*

**Lead the five whys iteratively:**
> "Why does [point of cause] happen?"

After each answer:
> "And why does [that answer] happen?"

Continue until a systemic root cause is reached. Test it: "If we fixed [root cause], would this problem recur? If yes, we haven't gone deep enough."

Challenge person-blame answers: "That describes who — we need to understand why the system allowed that to happen."

---

### STEP 6 — Countermeasure + Plan

**Share insight:**
> 💬 *"Toyota forbids the word 'solution.' Every fix is a countermeasure — a hypothesis to test. When proven, it becomes a standard. The distinction matters: 'solution' closes inquiry; 'countermeasure' keeps the door open for improvement. One exception: if a known standard already covers this, applying it is restoring compliance, not a new countermeasure."*

**Coaching question:**
> "What's your proposed countermeasure — the hypothesis you want to test? How will you implement it, and what result would tell you it's working?"

If they jump to implementation without a measurement plan: "How will you know it worked? What would you measure?"

---

### STEP 7 — How to Monitor

**Share insight:**
> 💬 *"The Check in PDCA is not a formality. Toyota wanted PDCA completed within a single shift. A countermeasure that 'seems to be working' is not confirmed. Only measurement verifies."*

**Coaching question:**
> "How will you check this stays fixed over time? What specific measurement, at what cadence?"

---

### STEP 8 — Prevent / New Standard

**Share insight:**
> 💬 *"'Standardized work is today's best-known way, which can be improved tomorrow.' The standard isn't bureaucracy — it's the baseline that makes future improvement possible. You can't improve a process that isn't first stabilized. If no standard existed at Step 2, this is your most important output today."*

**Coaching question:**
> "How do you prevent this from recurring? What new process, check, or standard needs to exist — and where does it need to live so the people doing the work can actually see and follow it?"

If Step 2 found no standard: "This is where we write the standard. What should it say? Who owns it?"

---

### STEP 9 — Yokoten

**Share insight:**
> 💬 *"Yokoten means 'across everywhere' — horizontal, peer-to-peer. At Toyota, you are not done until others who could benefit have learned what you learned. It's not 'copy exactly' — it's go see, understand, then adapt with your own wisdom. The problem is not solved until the knowledge spreads."*

**Coaching question:**
> "Who else could have this problem, or benefit from what you just worked out? How are you going to share it with them?"

---

## Contextual TPS Concept Suggestions

Same trigger map as /tps:solve. Surface after confirming the relevant step. Format:
> 💡 **TPS Concept: [Name]** — [hook]. [Why it's relevant here, from tps-knowledge-base.md.]

| Pattern | Concept | When |
|---|---|---|
| Uneven workload, bursty demand | **Heijunka** | Step 3-4 |
| Cluttered, hard to find things | **5S** | Step 4 |
| Recurring human error | **Poka-Yoke** | Step 5-8 |
| Defect found late / downstream | **Jidoka** | Step 4 |
| Overloaded team or process | **Muri** | Step 3 |
| Irregular demand | **Mura** | Step 3 |
| Waste: waiting, motion, over-processing | **Muda** / 7 Wastes | Step 1-4 |
| High WIP, large batches | **One-Piece Flow / JIT** | Step 4 |
| Fix keeps slipping | **SDCA** | Step 8 |

---

## Artifact Generation

Identical to /tps:solve. On completing Step 9:

- Generate `kivna/output/pps-[slug].html` from `skills/tps/shared/a3-template.html`
- Generate `kivna/output/pps-[slug].md`
- `{{MODE}}` = `/tps:coach`

Output the completion message:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PPS Complete — [Perceived Problem Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ All 9 steps confirmed
✓ Countermeasure: [title] — [status]
✓ Standard: [new/updated/restored]

Artifacts:
  HTML: kivna/output/pps-[slug].html
  Markdown: kivna/output/pps-[slug].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

- [ ] **Step 2: Commit**

```bash
git add skills/tps/coach/SKILL.md
git commit -m "feat: add /tps:coach human coaching skill"
```

---

## Task 5: Install Plugin + Smoke Test

**Files:** none created — verification only

- [ ] **Step 1: Ensure `kivna/output/` is gitignored**

Check `.gitignore` contains `kivna/output/`. If not:
```bash
echo "kivna/output/" >> .gitignore
git add .gitignore && git commit -m "chore: gitignore kivna/output"
```

- [ ] **Step 2: Install the plugin**

```bash
# From repo root
claude plugin install . --scope user
```

If that command isn't available, register manually:
Open Claude Code → Settings → Plugins → Add local plugin → select this directory.

Expected: plugin `tps` registered, skills `tps:solve` and `tps:coach` available.

- [ ] **Step 3: Smoke test `/tps:solve`**

In a Claude Code session in any project directory:
```
/tps:solve
```
With problem: "The login button doesn't work on mobile"

Expected behavior:
- Opening statement says "Before I make any changes..."
- Step 1 investigation happens before any proposed fix
- Progress block appears after Step 1 confirmation
- Right column locked until Step 4 gate
- No code changes proposed until Step 6

- [ ] **Step 4: Smoke test `/tps:coach`**

```
/tps:coach
```

Expected behavior:
- Opens with "Let's work through this together..."
- Asks one question at a time
- Surfaces TPS insight before each step's coaching question
- Reflects back answers before advancing
- Progress block updates after each step

- [ ] **Step 5: Verify artifact output**

After completing either smoke test through Step 9:
```bash
ls kivna/output/
open kivna/output/pps-*.html
```

Expected: HTML file opens in browser showing two-column A3 with flow diagrams, 5-why chain, countermeasure cards. Markdown file present alongside.

- [ ] **Step 6: Final commit**

```bash
git add .
git commit -m "feat: complete tps plugin — /tps:solve and /tps:coach"
```
