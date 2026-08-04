# /sensei:review — Design Spec

**Date:** 2026-04-14
**Author:** Anthony Maley
**Status:** Approved

## Purpose

A3 review skill. The sensei reads a completed A3 and marks it up with direct, blunt feedback. One pass, no dialogue, no coaching. The author takes the red-inked A3 away and reworks it themselves (using `/sensei:coach` if they need help).

This is the fourth voice in the Toyota Sensei plugin. The three existing voices are disciplined LLM (work), coaching questions (coach), and teaching (learn). Review is the harshest: senior sensei who tells you what's wrong and walks away.

## Input

A completed A3 in any of three formats:
- **PDF** — read via the Read tool's PDF support
- **HTML** — a `.html` file (typically from a prior `/sensei:work` or `/sensei:coach` run)
- **Markdown** — a `.md` file or pasted markdown text

The skill parses all 9 steps from whatever format is provided. If the A3 is incomplete (missing steps), the sensei notes that as a finding — an incomplete A3 is itself a problem.

## Voice

Senior sensei. Blunt, wastes no words, will reject an entire section as insufficient. No softening, no hedging, no "you might consider." Direct statements.

Examples of the voice:
- "This is not a root cause. This is a symptom you stopped investigating too early."
- "You identified the point of cause where the symptom appears, not where the breakdown occurs. These are different things."
- "This countermeasure is containment. It addresses the symptom at Step 1, not the root cause at Step 5."
- "Step 3 has no measurement. 'It happens frequently' is an opinion, not data."
- "Your 5 Whys stopped at a person. Why does the system allow that person to make that mistake?"

When a section is strong, the sensei acknowledges it briefly and moves on. No praise inflation.
- "Step 4 is precise. Good."
- "The why chain reaches a systemic cause. Accepted."

## Flow

### 1. Read the A3

Parse the document. Extract content for each of the 9 steps. Read `docs/tps-knowledge-base.md` to ground feedback in TPS principles.

### 2. Red-ink walkthrough

Step by step, in order, the sensei gives direct feedback on each section. No questions, no coaching. Statements only.

Format for each step:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Step N — [Step Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Direct feedback. What's wrong, why it's wrong, what specifically is missing or weak. If the section is strong, say so in one line and move on.]
```

#### What the sensei checks at each step

| Step | Check |
|------|-------|
| 0 — Perceived Problem | Framed as hypothesis, not conclusion? Labeled "perceived"? |
| 1 — What Is Happening | Evidence from observation/investigation, or assumptions from a desk? Specific and reproducible? |
| 2 — What Should Happen | Actual standard referenced, or invented ideal? Standard diagnosis present (exists/followed, exists/not followed, none)? |
| 3 — AS IS Condition | Real measurements with numbers, or vague descriptions masquerading as data? Frequency, scope, conditions? |
| 4 — Point of Cause | Precise location where the breakdown occurs, or just where the symptom was noticed downstream? Target measurable and specific? |
| **Gate** | Does the left column actually establish the problem before the right column begins? Is the point of cause precise enough to anchor 5 Whys? |
| 5 — Root Cause (5 Whys) | Chain starts from point of cause (not symptom)? Each why follows logically from the previous? Stops at a systemic cause (not a person, not a symptom)? |
| 6 — Countermeasure | Addresses the root cause identified in Step 5, or just contains the symptom? Testable hypothesis? |
| 7 — Monitor | Specific metric and cadence, or "we'll keep an eye on it"? |
| 8 — Prevent / Standard | New standard created or existing standard updated, or just a one-time fix with no systemic change? |
| 9 — Yokoten | Named audience and specific method, or generic "share with the team"? |

#### Cross-step integrity checks

Beyond individual steps, the sensei checks that the A3 holds together as a whole:
- Does the root cause chain (Step 5) start from the point of cause (Step 4), not from the perceived problem (Step 0)?
- Does the countermeasure (Step 6) address the root cause (Step 5), not the symptom (Step 1)?
- Does the standard (Step 8) prevent the root cause, not just the surface manifestation?
- Is there a coherent thread from point of cause → root cause → countermeasure → standard?

### 3. Verdict

After the walkthrough, one of three verdicts:

- **Pass** — A3 is sound. Minor notes only. The problem-solving is rigorous and the logic chain holds.
- **Rework** — structural weaknesses in specific steps. The sensei names exactly which steps need rework and why. The overall approach may be salvageable.
- **Reject** — fundamental failures. The left column isn't established (point of cause is wrong or missing), or the entire right column is built on a wrong foundation. Start over.

Verdict banner:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 VERDICT: [PASS / REWORK / REJECT]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[One to three sentences. What's the core issue (rework/reject) or what's strong (pass).]

[For rework: "Rework steps: N, N, N"]
[For reject: "Fundamental issue: [what]"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Annotated A3 artifact

Generate an HTML file that reproduces the original A3 content with red-ink annotations overlaid on each section.

#### Annotation design

Red annotations appear inline within each A3 section, visually distinct from the original content:
- Red border left edge on annotated sections
- Red text for the sensei's comments
- Original content preserved in black
- Verdict badge in the header (green for pass, amber for rework, red for reject)

File location: `kivna/output/tps-[slug]/tps-[slug]-review.html`

The slug comes from the original A3. If the original A3 is at `kivna/output/tps-thumbnails-not-displaying/`, the review goes in the same directory as `tps-thumbnails-not-displaying-review.html`. If the A3 is from outside the project (a PDF or external file), derive the slug from the perceived problem text (lowercase, hyphens, max 40 chars) and create `kivna/output/tps-[slug]/tps-[slug]-review.html`.

## Boundaries

- **No coaching.** No questions. No "what do you think?" This is not `/sensei:coach`.
- **No re-doing the work.** The sensei marks what's wrong. The sensei does not fix it, rewrite it, or suggest specific rewrites. The author does the work.
- **No investigation.** The sensei reviews what's on the paper. Does not go read code, check logs, or verify claims. Reviews the thinking, not the technical accuracy.
- **One pass.** Delivers the review and walks away. If the author needs help reworking, use `/sensei:coach`.
- **No dialogue.** The review is a monologue. The sensei does not ask clarifying questions about the A3. Ambiguity in the A3 is itself a finding.

## Dependencies

- Reads `docs/tps-knowledge-base.md` at invocation (same as other skills)
- Reads `docs/tps-framework.md` for canonical step definitions
- Uses `skills/shared/a3-template.html` as the base for the annotated artifact (extended with review annotation styles)

## Skill metadata

```yaml
name: review
description: "Use when someone has a completed A3 (from /sensei:work, /sensei:coach, or any source) and wants a senior sensei review. Reads the A3 in PDF, HTML, or markdown format and delivers blunt, direct red-ink feedback on every step. Produces a verdict (pass/rework/reject) and an annotated HTML artifact. One pass, no dialogue. Invoke with /sensei:review."
```

## Relationship to other skills

| Skill | When | Voice |
|-------|------|-------|
| /sensei:work | LLM works the problem itself | Disciplined, on rails |
| /sensei:coach | Human works the problem, LLM coaches | Questions, reflects, challenges |
| /sensei:learn | Human learns TPS concepts | Teaches, stories, sources |
| /sensei:review | A3 is done, needs senior review | Blunt, direct, red ink |

The natural workflow: work or coach produces an A3 → review evaluates it → if rework is needed, coach helps the author improve it.
