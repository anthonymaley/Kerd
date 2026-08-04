# TPS Problem-Solving Skill: Design Spec
Date: 2026-04-13  
Author: Anthony Maley  
Status: Approved

---

## Overview

Two Claude Code skills that enforce Toyota's 9-step Practical Problem Solving (PPS) framework. Both prevent the most common failure mode (jumping to a solution before the problem is understood) and both produce a live progress document throughout the process plus a final A3 artifact.

---

## Skills

| Command | Mode | Posture |
|---|---|---|
| `/tps:solve` | LLM discipline | Claude is the problem-solver, putting itself on rails |
| `/tps:coach` | Human coaching | Claude is the sensei, drawing answers from a human |

Both live under `skills/tps/` in this repo. Each has its own `SKILL.md`.

---

## The Framework: 9 Steps

### Left Column: Understand First (Steps 0 through 4)
Must be fully confirmed before the right column begins. No exceptions.

| Step | Name | Purpose |
|---|---|---|
| 0 | Perceived Problem | The trigger statement. Labeled "perceived" intentionally — what we think is happening is a hypothesis, not a fact. |
| 1 | What Is Happening | Precise description of the observed reality. Anchored by direct observation (genchi genbutsu), not reports. |
| 2 | What Should Happen + Standard Diagnosis | The standard or ideal condition. Explicitly diagnoses whether a standard exists. |
| 3 | AS IS Condition | Quantified gap — measurement of how often, how much, how fast. |
| 4 | Point of Cause + Target | **The gate.** Exact location in the process where the breakdown occurs. Plus a measurable target for "fixed." |

### Right Column: Resolve (Steps 5 through 9)
Unlocked only after Step 4 is confirmed.

| Step | Name | Purpose |
|---|---|---|
| 5 | Root Cause — 5 Whys | Applied to the Point of Cause, not the symptom. Ask why from that specific location. |
| 6 | Countermeasure + Plan | A hypothesis to test. Not a solution. Includes how results will be measured. |
| 7 | How to Monitor | Measurement-based confirmation that the countermeasure is working. |
| 8 | Prevent / New Standard | Standardize the fix. Elevated to primary output when no standard existed (Step 2 finding). |
| 9 | Knowledge Share (Yokoten) | Who else needs to know. The process is not complete until knowledge spreads. |

---

## Genchi Genbutsu: Go and See (Step 1)

Genchi genbutsu is the non-negotiable foundation of Step 1. "The actual place, the actual thing."

In coaching mode, the coaching question explicitly pushes for direct observation:
- "Have you gone and seen this yourself?"
- "What did you observe directly, not what someone told you, not what the dashboard says?"
- "Can you reproduce it?"

For digital/code problems: reproduce it yourself, read the actual logs, examine the actual code. Secondhand reports are not acceptable input for Step 1.

In solve mode, Claude does not describe what it *thinks* is happening from the problem statement. It investigates first (reads the code, checks the logs, reproduces the condition) then presents findings based on direct observation.

The Ohno principle applies: *"Observe the production floor without preconceptions and with a blank mind."* No assumptions before going to see.

---

## Standard Diagnosis (Step 2)

At Step 2, the skill explicitly surfaces which of three situations applies:

| Finding | What It Means | How It Changes the Process |
|---|---|---|
| **Standard exists, was followed** | The standard itself may be insufficient | 5 Whys focuses on why the standard failed |
| **Standard exists, was not followed** | Deviation from known good | 5 Whys focuses on why it wasn't followed — training gap, visibility, poka-yoke needed |
| **No standard exists** | A gap in the system — a discovery, not a failure | Step 8 becomes primary output: creating the standard IS the countermeasure |

"No standard" is a good outcome. The problem revealed a structural gap. The fix creates a permanent prevention for the whole class of issue.

**Coaching question at Step 2:**
> "Is there a documented standard or expected process for what should happen here? If yes — what does it say? If no — that's an important finding. We'll capture what *should* happen based on your knowledge and build the standard as part of the solution."

---

## `/tps:solve` — LLM Discipline Mode

### Purpose
Prevents Claude from jumping to countermeasures before understanding the problem. When a user reports an issue, Claude uses this framework to discipline its own process.

### Conversational Posture
Claude leads the investigation. The human confirms, corrects, or challenges.

### Flow

1. **Open:** *"Before I make any changes, I'm going to work through this properly. Let me start by understanding what's actually happening."*

2. **For each left-column step:**
   - Claude investigates (reads code, logs, reproduces the condition)
   - Presents findings as a **draft** for that step
   - Updates the live progress document
   - Asks: *"Does this match what you're seeing? Anything to correct or add?"*
   - Waits for confirmation before advancing

3. **Gate at Step 4:**
   > *"Left column complete. Point of cause: [X]. Target: [Y]. I'm not going to touch any code until you confirm this is correct. Ready to proceed to root cause?"*

4. **For each right-column step:**
   - Same pattern: Claude proposes, user confirms before advancing

5. **Completion:** Generate A3 HTML + markdown artifacts.

### Critical Rule
Claude holds any fix it identifies during investigation. It does not propose code changes, countermeasures, or solutions until Step 6. If it's obvious what the fix is, it still works through Steps 1 through 5 first. The discipline is the point.

---

## `/tps:coach` — Human Coaching Mode

### Purpose
Guides a human through the framework to solve their own problem. Claude acts as sensei, drawing out the thinking, not providing answers.

### Conversational Posture
Human leads the thinking. Claude asks questions, reflects back, and challenges weak reasoning.

### Flow

1. **Open:** *"Let's work through this together. What's the problem you're facing?"* (Captures perceived problem)

2. **For each step:** One coaching question, then reflect back the answer, update the document, confirm before advancing.

3. **Gate at Step 4:** Same explicit confirmation as solve mode.

4. **Completion:** Same A3 HTML + markdown output.

### Coaching Questions + Step Insights

At each step, the skill surfaces a brief insight from TPS/Toyota Way to explain *why* this step matters, teaching the method as it coaches through the problem. Insights come from `docs/tps-knowledge-base.md`.

---

**Step 1 — What Is Happening (Genchi Genbutsu)**

> **Insight:** *"Taiichi Ohno drew a circle on the shop floor and made students stand in it for hours — sometimes an entire day — observing without explanation. The lesson: truth lives at the gemba, not in a report. 'Observe the production floor without preconceptions and with a blank mind.' When one hospital tried to solve a patient response-time problem in a conference room, intelligent people fabricated root causes that were completely wrong. Going to see revealed the real causes in minutes."*

> **Coaching question:** "Before we go further — have you gone and seen this yourself? I want to know what you observed directly, not what someone told you or what a report shows. Can you describe exactly what you saw or reproduced?"

Follow-up if vague: *"Can you be more specific? What exact behavior are you observing?"*

---

**Step 2 — What Should Happen + Standard Diagnosis**

> **Insight:** *"At Toyota, the first question asked when any defect is found is: 'Was standardized work followed?' If no → correct the behavior. If yes and defects still occur → improve the standard. If no standard exists, that is itself the finding — and creating one becomes the most important countermeasure. Henry Ford said it best: 'If you think of standardization as the best you know today, but which is to be improved tomorrow — you get somewhere.'"*

> **Coaching question:** "What should happen instead? And — is there a documented standard or process for this? If yes, what does it say? If no, that's an important finding — we'll define what 'correct' looks like right now and build the standard as part of the solution."

---

**Step 3 — AS IS Condition**

> **Insight:** *"Visual management at Toyota means any deviation from standard is immediately visible to anyone walking through — no special knowledge required. 'Hear a piece of information and three days later you'll remember 10% of it. Add a picture and you'll remember 65%.' The AS IS condition makes the gap concrete and undeniable. Without measurement, 'there's a problem' is an opinion. With it, it becomes a fact that demands action."*

> **Coaching question:** "How do you *know* this is a problem? What measurement or evidence do you have — frequency, rate, volume, error count? How often does it happen, and under what conditions?"

---

**Step 4 — Point of Cause + Target**

> **Insight:** *"Jidoka — Toyota's right pillar — is built on one principle: stop and fix at the source. The andon cord is pulled not where the problem is discovered downstream, but at the workstation where it occurs. Finding the point of cause is the discipline of asking 'where was the work last good?' — and tracing forward to the exact moment it breaks. Without this precision, 5 Whys starts from the wrong place and leads to the wrong root cause every time."*

> **Coaching question (point of cause):** "Where exactly does the breakdown occur? Not where you discover it — where it actually happens. Can you point to the specific step, component, or handoff where it should work but doesn't?"

> **Coaching question (target):** "What does 'fixed' look like, measured? How will you know when the target is achieved?"

---

**Step 5 — Root Cause — 5 Whys**

> **Insight:** *"Ohno's original example: oil on the floor → gasket failed → wrong gasket → not specified properly → purchasing agent not trained → evaluation criteria don't include technical specs. The fix at the root changed how purchasing agents are evaluated. A surface fix (replace the gasket) would have recurred indefinitely. Warning: when people are defensive, 5 Whys degenerates into 5 Whos — finding blame instead of system causes. The investigation always focuses on the system, never the individual."*

> **Coaching question:** "Why does that happen? Let's ask why from that exact point — not from the symptom."
> *(Guide through each Why iteratively. Challenge if the answer is a person rather than a system. Stop when a systemic cause is reached — something in the process, environment, or standard that allowed this to happen.)*

---

**Step 6 — Countermeasure + Plan**

> **Insight:** *"Toyota forbids the word 'solution.' There are only countermeasures — hypotheses that might reduce the gap. A countermeasure proven effective becomes a standard, which is 'the best we know today until we find a better one.' The distinction matters: calling something a solution closes inquiry. Calling it a countermeasure keeps the PDCA loop open. The one exception: if a known standard already addresses this situation, applying it is not a countermeasure — it's restoring compliance."*

> **Coaching question:** "What's your proposed countermeasure — the hypothesis you want to test? How will you test it, and what result would tell you it's working?"

---

**Step 7 — How to Monitor**

> **Insight:** *"'We can't afford to have PDCA that takes three weeks anymore. We want a PDCA done before the end of that shift.' The Check step is not a formality — it is how you know whether your hypothesis was correct. A countermeasure that 'seems to be working' is not verified. Only measurement confirms. The andon system itself is Toyota's factory-wide Check mechanism — every abnormality surfaces immediately rather than being discovered at final inspection."*

> **Coaching question:** "How will you check this stays fixed? What specific measurement, and at what cadence?"

---

**Step 8 — Prevent / New Standard**

> **Insight:** *"'Standardized work is today's best-known way, which can be improved tomorrow.' Toyota turned classical industrial engineering on its head: work groups design and continuously improve their own standards. When a countermeasure proves effective, it becomes the new standard — not filed away, but posted visually at the point of work. If no standard existed (Step 2 finding), this step is the primary output: you are closing a structural gap that allowed this entire class of problem to occur."*

> **Coaching question:** "How do you prevent this from recurring? What new process or standard needs to exist — and where does it need to live so the people doing the work can see and follow it?"
> *(If no standard at Step 2: "This is where we write the standard. What should it say, and who owns it?")*

---

**Step 9 — Yokoten (Knowledge Share)**

> **Insight:** *"Yokoten means 'across everywhere' — horizontal, peer-to-peer knowledge transfer. At Toyota, the learner is not done until the new process is shared with others who might benefit. Critically, yokoten is not 'copy exactly' — people are expected to go see for themselves how another area solved the problem, then adapt it with their own wisdom. The problem-solving process is not complete at Step 8. It is complete when the learning spreads."*

> **Coaching question:** "Who else could have this problem — or who could benefit from what you learned? How are you going to share it with them?"

---

## Contextual TPS Concept Suggestions

Beyond the fixed per-step insights, the skill recognizes patterns in what's being discovered and surfaces relevant TPS concepts as non-blocking suggestions. Educational, not prescriptive. These fire at natural pause points (after confirming a step, or at the end of the process).

Format:
> 💡 **TPS Concept: [Name]** — *[One-sentence hook from the book, then brief explanation and why it's relevant to this specific problem.]*

The skill does not interrupt the flow. It offers the concept, the human can ask to learn more or move on.

---

### Concept Trigger Map

| Pattern Detected | Concept Surfaced | When to Trigger |
|---|---|---|
| Uneven workload, bursty demand, batch processing, irregular schedule | **Heijunka** (Production Leveling) | Step 3 or Step 4 |
| Cluttered workspace, can't find things, missing tools, disorganized process | **5S** (Sort, Straighten, Shine, Standardize, Sustain) | Step 4 |
| Recurring human error, wrong part used, step skipped | **Poka-Yoke** (Error Proofing) | Step 5 or Step 8 |
| Defect discovered late, downstream from where it occurred | **Jidoka** (In-Station Quality / Stop and Fix) | Step 4 |
| Overloaded person, team, or machine — pushed beyond capacity | **Muri** (Overburden — one of the Three Ms) | Step 3 |
| Unevenness in demand or process causing downstream chaos | **Mura** (Unevenness — one of the Three Ms) | Step 3 |
| Non-value-added steps, waiting, unnecessary movement | **Muda** (Waste — 7 wastes) | Step 1 or Step 4 |
| Large batches of work sitting idle, high WIP | **One-Piece Flow / JIT** | Step 4 |
| Problem keeps recurring despite fixes | **SDCA** (Standardize-Do-Check-Act — maintaining standards) | Step 8 |
| Improvement effort itself — any active problem solving | **PDCA** (Plan-Do-Check-Act — the scientific method) | Opening or Step 6 |
| Team not aligned on priorities, improvement efforts scattered | **Hoshin Kanri** (Strategy Deployment) | Step 9 |
| Supplier, partner, or handoff involved in the failure | **Principle 11** (Respect your value chain partners) | Step 4 or Step 5 |
| Complexity hidden, process not visible end-to-end | **Value Stream Mapping** | Step 2 or Step 4 |
| Leader not present at gemba, problem solved from a desk | **Genchi Genbutsu** (reinforce) | Step 1 or Step 4 |
| Team engagement low, suggestions not being made | **Kaizen culture / psychological safety** | Step 9 |

---

### Concept Cards (surfaced inline)

**Heijunka (Production Leveling)**
> 💡 **TPS Concept: Heijunka** — *"The tortoise beats the hare."*
> The unevenness you're seeing (mura) is likely causing the overburden (muri) that produced this defect. Heijunka levels production by both volume AND mix — removing the peaks and valleys that stress the system. Ohno: "When you try to apply TPS, the first thing you have to do is level the production. And that is the responsibility primarily of management." Addressing heijunka may prevent an entire class of similar problems.

**5S (Workplace Organization)**
> 💡 **TPS Concept: 5S** — *"Cleaning IS inspection."*
> Sort, Straighten, Shine, Standardize, Sustain. 5S isn't about neatness — it's about making abnormalities immediately visible. A tool out of its shadow position is a problem. Inventory outside its marked boundary is a problem. Toyota actually uses 4S — sustaining is assumed: "without sustaining, why bother?" Applied properly here, 5S would make this type of failure impossible to miss before it causes damage.

**Poka-Yoke (Error Proofing)**
> 💡 **TPS Concept: Poka-Yoke** — *"Make errors nearly impossible."*
> The root cause you found is human-error-susceptible. A poka-yoke device makes the correct action the only possible action — physically, digitally, or procedurally. NUMMI's front axle line had 27 poka-yoke devices. Each one started as exactly the type of problem you're solving now. The question to ask: how could we redesign this so the wrong action cannot happen, rather than relying on people to always do the right thing?

**Muda / 7 Wastes**
> 💡 **TPS Concept: Muda (Waste)** — *"All we are doing is looking at the timeline."*
> Toyota's 7 wastes: overproduction, waiting, unnecessary transport, over-processing, excess inventory, unnecessary motion, defects. The problem you're solving is a defect — but the process that created it likely contains other wastes that contributed. Eliminating the defect is the countermeasure. Eliminating the wastes around it is the standard.

**PDCA (Plan-Do-Check-Act)**
> 💡 **TPS Concept: PDCA** — *"Navigate with a compass, not a GPS."*
> This entire process IS a PDCA cycle. Plan = understanding the problem and forming a hypothesis (Steps 1-6). Do = implementing the countermeasure. Check = monitoring results (Step 7). Act = standardizing and sharing (Steps 8-9). The key distinction: false PDCA commits to a known solution at maximum uncertainty. True PDCA runs experiments and learns. You're doing the second kind.

**SDCA (Standardize-Do-Check-Act)**
> 💡 **TPS Concept: SDCA** — *"SDCA removes small rocks; PDCA removes big boulders."*
> Once you've established a new standard (Step 8), SDCA maintains it. When a deviation from that standard occurs in the future, the response is SDCA — restore the standard, understand why it was deviated from. PDCA is for improving; SDCA is for maintaining. Running both at all levels is how Toyota sustains gains rather than regressing.

**Jidoka (In-Station Quality)**
> 💡 **TPS Concept: Jidoka** — *"If you are not shutting down the assembly plant, it means you have no problems — which means you are hiding your problems."*
> Cho to a GM veteran. Jidoka means building quality in at the source — stopping the process the moment an abnormality appears, rather than passing defects forward. The countermeasure you're designing should include a detection mechanism: how does the process signal when this type of failure is occurring, before it reaches the next step?

**Value Stream Mapping**
> 💡 **TPS Concept: Value Stream Mapping** — *"The map is not the destination — it's the starting point."*
> The complexity of this problem suggests the value stream may not be fully visible. VSM maps all material and information flows — cycle times, wait times, handoffs, inventory levels. The gap between your current-state map and a future-state map IS the improvement agenda. This problem may be one node in a larger flow that deserves a full VSM exercise.

**Hoshin Kanri**
> 💡 **TPS Concept: Hoshin Kanri** — *"Strategy sets the direction; execution is a series of iterative learning experiments."*
> If this problem reflects a broader gap in organizational alignment — teams working on conflicting priorities, improvement energy scattered — hoshin kanri is the tool. It cascades challenging goals from senior vision to daily work-group actions through A3s at every level. The problem you solved today might deserve to become a hoshin item if it reflects a systemic organizational gap.

---

### Sensei Rules
- One question at a time. Never ask two questions in one turn.
- Reflect back before advancing: *"So what you're saying is [X]. Is that right?"*
- Challenge thin answers: *"That's still a symptom. Why does [X] happen?"*
- Never fill in the answer. Draw it out.
- If the human is stuck, give a prompt — not the answer: *"Think about where in the process the work was last good."*

---

## Live Progress Document

Updated after every confirmed step. Written to the conversation as a formatted block.

**Format:**
- Confirmed steps: shown with full content (green marker)
- Active step: shown as amber/in-progress
- Future steps: shown as locked/greyed
- Right column: locked and labelled "Locked — complete left column first" until gate passed

**Structure (progress stack, top to bottom):**
```
[PERCEIVED PROBLEM]
Thumbnails not showing on product page

✓ Step 1 — What Is Happening
  Images return HTTP 404 in production. Dev unaffected.

✓ Step 2 — What Should Happen  [Standard: EXISTS / NOT FOLLOWED]
  All product images load from CDN within 2 seconds.

▶ Step 3 — AS IS Condition  ← active
  ...

  Step 4 — Point of Cause + Target  (locked)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 5 — Root Cause  (locked — complete left column first)
  ...
```

---

## Final Artifacts

Generated on completion. Saved to `kivna/output/pps-[slug]/`.

### 1. `pps-[slug].html` — A3 Report

Two-column HTML document. Visual language:
- **Process flow diagrams** — boxes and arrows; green = normal path, red = failure path
- **Point of cause box** — red border, explicit should vs. actual contrast
- **5 Whys chain** — cascading visual, color-coded by Why number
- **Root cause callout** — highlighted box at base of why chain
- **Standard finding badge** — "No Standard Found" or "Standard Not Followed" displayed prominently when applicable
- **Countermeasure cards** — numbered, status-trackable (proposed / testing / verified)
- **Yokoten flow** — mini diagram showing knowledge distribution
- **Footer metadata** — owner, date, steps challenged, time to countermeasure

### 2. `pps-[slug].md` — Markdown Report

Same content, structured for pasting into tickets, Notion, Confluence, GitHub issues, etc.

---

## File Structure

```
skills/
  tps/
    solve/
      SKILL.md
    coach/
      SKILL.md
  
kivna/output/        ← gitignored
  pps-[slug]/
    pps-[slug].html
    pps-[slug].md
```

---

## Design Principles

1. **Perceived ≠ real.** The header framing is deliberate. The skill treats the initial problem statement as a hypothesis to be investigated, not a fact to be fixed.

2. **Left before right, no exceptions.** The gate at Step 4 is hard. No countermeasures before the point of cause is confirmed and the target is set.

3. **Genchi genbutsu first.** Observation precedes analysis. No 5 Whys in a conference room.

4. **Measurement at three points.** AS IS condition (how big is the gap), countermeasure verification (is it working), monitoring (does it stay fixed).

5. **Countermeasure, not solution.** Every fix is a hypothesis until proven and standardized. The only exception: when a known standard already addresses the situation.

6. **Standards as output.** "No standard exists" is a discovery, not a failure. The most important countermeasures create permanent prevention through new standards.

7. **Yokoten is mandatory.** The process is not complete until knowledge is shared. Step 9 is not optional.

8. **The document is the challenge surface.** It builds live so the human can red-ink it at any step. Visibility throughout is not a UX nicety. It is the TPS mechanism.
