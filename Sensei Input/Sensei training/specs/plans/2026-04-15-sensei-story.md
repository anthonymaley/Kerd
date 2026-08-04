# /sensei:story Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `/sensei:story` to the Toyota Sensei plugin — a router skill that guides users through Toyota's 7 A3 story types with progressive build, compression discipline, and nemawashi tracking.

**Architecture:** Router + story type definition files. One SKILL.md handles routing, mode switching (LLM/human), compression enforcement, progressive build, and nemawashi. Seven type definition files (one per story type) define sections, column mappings, coaching prompts, and examples. One configurable HTML template serves all types. Knowledge base renamed and enriched with A3 communication section.

**Tech Stack:** Markdown (skill + type files), HTML/CSS (template)

**Spec:** `docs/specs/2026-04-15-sensei-story-design.md`

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `docs/tps-knowledge-base.md` | Rename → `docs/sensei-knowledge-base.md` | Knowledge base rename |
| `docs/sensei-knowledge-base.md` | Modify | Add A3 communication section, expand nemawashi entry |
| `skills/work/SKILL.md` | Modify (lines 12, 480) | Update KB read path |
| `skills/coach/SKILL.md` | Modify (lines 12, 276) | Update KB read path |
| `skills/learn/SKILL.md` | Modify (line 10) | Update KB read path |
| `skills/review/SKILL.md` | Modify (line 12) | Update KB read path |
| `skills/shared/a3-story-template.html` | Create | Configurable story A3 template |
| `skills/story/SKILL.md` | Create | Router + shared rules |
| `skills/story/types/1-educate-details.md` | Create | Type 1 definition |
| `skills/story/types/2-illumination-unknown.md` | Create | Type 2 definition |
| `skills/story/types/3-compare-contrast.md` | Create | Type 3 definition |
| `skills/story/types/4-standard-proposal.md` | Create | Type 4 definition |
| `skills/story/types/5-correcting-discrepancy.md` | Create | Type 5 definition |
| `skills/story/types/6-develop-roadmap.md` | Create | Type 6 definition |
| `skills/story/types/7-education-satisfaction.md` | Create | Type 7 definition |
| `.claude-plugin/plugin.json` | Modify | Add /sensei:story to description, bump to 1.4.0 |

---

### Task 1: Rename knowledge base and update all read paths

**Files:**
- Rename: `docs/tps-knowledge-base.md` → `docs/sensei-knowledge-base.md`
- Modify: `skills/work/SKILL.md:12,480`
- Modify: `skills/coach/SKILL.md:12,276`
- Modify: `skills/learn/SKILL.md:10`
- Modify: `skills/review/SKILL.md:12`

- [ ] **Step 1: Rename the knowledge base file**

```bash
git mv docs/tps-knowledge-base.md docs/sensei-knowledge-base.md
```

- [ ] **Step 2: Update work skill KB path**

In `skills/work/SKILL.md`, replace all occurrences of `tps-knowledge-base.md` with `sensei-knowledge-base.md`. There are two: line 12 (the read instruction) and line 480 (the concept surfacing template).

Line 12 change:
```
Read `docs/sensei-knowledge-base.md` now — it contains the TPS concepts and quotes you will surface at each step.
```

Line 480 change:
```
> 💡 **TPS Concept: [Name]** — [one-sentence hook from sensei-knowledge-base.md]. [2–3 sentences explaining why it's relevant to what was just discovered.]
```

- [ ] **Step 3: Update coach skill KB path**

In `skills/coach/SKILL.md`, replace all occurrences of `tps-knowledge-base.md` with `sensei-knowledge-base.md`. There are two: line 12 and line 276.

Line 12 change:
```
Read `docs/sensei-knowledge-base.md` now — it contains the TPS concepts and quotes you will surface at each step.
```

Line 276 change:
```
> 💡 **TPS Concept: [Name]** — [one-sentence hook from sensei-knowledge-base.md]. [2–3 sentences explaining why it's relevant to what was just discovered.]
```

- [ ] **Step 4: Update learn skill KB path**

In `skills/learn/SKILL.md`, line 10, change:
```
Read `docs/sensei-knowledge-base.md` now — it is the source of everything you teach. Every substantive claim must be grounded in this knowledge base, with source citations: [Handbook], [Ohno], or [Liker].
```

- [ ] **Step 5: Update review skill KB path**

In `skills/review/SKILL.md`, line 12, change:
```
Read `docs/sensei-knowledge-base.md` now — it grounds your feedback in TPS principles.
```

- [ ] **Step 6: Verify no remaining references to old name**

```bash
grep -r "tps-knowledge-base" skills/ docs/ --include="*.md"
```

Expected: no results. If any remain, fix them.

- [ ] **Step 7: Commit**

```bash
git add docs/sensei-knowledge-base.md skills/work/SKILL.md skills/coach/SKILL.md skills/learn/SKILL.md skills/review/SKILL.md
git commit -m "rename: tps-knowledge-base → sensei-knowledge-base, update all skill read paths"
```

---

### Task 2: Enrich knowledge base — A3 communication section and nemawashi expansion

**Files:**
- Modify: `docs/sensei-knowledge-base.md:779` (nemawashi entry in vocabulary section)
- Modify: `docs/sensei-knowledge-base.md` (add new section 14 after section 13)

- [ ] **Step 1: Expand the nemawashi vocabulary entry**

In `docs/sensei-knowledge-base.md`, find line 779:
```
**Nemawashi**: "Going around the roots." Building consensus before formal decisions. Everyone's input considered; everyone supports the final decision. [Liker]
```

Replace with:
```
**Nemawashi**: "Going around the roots." Building consensus through cross-organizational communication before formal decisions. Toyota's operational method has 8 components organized in two phases — Relationships (Be Personable, Build Partnerships, Be Proactive, Build Pyramid) then Communication (Be Provider, Begin with Peers, Break for Preview, Bare Prospects). The key principle: start with peers, spiral up through layers, return to lower levels if needed. Benefits: no surprises, collective knowledge, give and take. A decision reached through nemawashi takes longer to plan but executes at the speed of full commitment. [Liker, Platt]
```

- [ ] **Step 2: Add section 14 — A3 as Communication Tool**

After the `## 13. Key Quotes for Coaching` section (after line 855, before the final `---`), add:

```markdown
## 14. A3 as Communication Tool

The A3 is not only a problem-solving format. At Toyota, the A3 is used for any communication that needs to be clear, compressed, and reviewable. The discipline of one page forces the author to understand their own thinking well enough to compress it. [Platt]

### The 7 Story Types

Toyota uses 7 story types for A3 communication, organized into two categories:

**Information Stories** (telling a story to inform):
1. **Educate to the Details** — Simple overview → Medium detail → Full detail. Start with the big picture, drill into specifics.
2. **Illumination of the Unknown** — Known → Unknown. Anchor new information to what the audience already understands.
3. **Compare & Contrast** — Current Situation → New Situation. Show what changed or will change.
7. **Education / Satisfaction** — Introduction → Topics → Conclusion. Educate on a series of related topics.

**Recommendation Stories** (telling a story to get agreement):
4. **Standard Toyota Proposal** — Situation → Problems & Cause → Proposal & Benefits. Show the problem before proposing the solution.
5. **Correcting Discrepancy from Standard** — Current Situation → Standard & Gap → Countermeasures. A known standard is not being followed.
6. **Develop the Roadmap** — Trends & Analysis → Strategic Direction. Propose direction based on identified trends.

These are separate from problem-solving (the 9-step framework). Problem-solving is investigation — you don't know the answer when you start. Story types are communication — you know what you want to say and the A3 structures how you say it. [Platt]

### The 5-Step Story Creation Process

1. **Select the outline** — pick the story type that fits what you're communicating
2. **Fill each box** — 3-7 key bullet points per section, developed at the level of your intended audience
3. **Test against the Rock Solid principles** — if it fails any test, compress further
4. **Illustrate** — add charts or pictures where they help, keep them simple
5. **Nemawashi and refine** — review with others, adjust, repeat

### Rock Solid Principles

Four tests for whether a story is ready. If it fails any one, it needs more work:
- If it's too much to handwrite, you have too much
- The audience should know why they're reading this
- Someone with no context (a grandparent) should be able to follow it
- You should be able to tell the story in a 3-minute elevator ride

These tests enforce the A3 constraint: one page is not a limitation, it is the discipline that produces clarity. [Platt]

### Nemawashi as Method

The 8 components of operational nemawashi:

**Relationships (1-4):**
1. **Be Personable** — be part of the organization, say hello, speak to people in the halls
2. **Build Partnerships** — build personal relationships with a select few, converse regularly on work and personal topics
3. **Be Proactive** — identify the key stakeholders for specific activities before you need them
4. **Build Pyramid** — understand the formal hierarchy and the informal organization, know who has established relationships

**Communication (5-8):**
5. **Be Provider** — stay in touch with key stakeholders, keep them informed of progress, share information
6. **Begin with Peers** — when building consensus, start with peers and spiral up through the layers; return to a lower level if necessary
7. **Break for Preview** — have preliminary informal discussions, hand sketch the concept and story
8. **Bare Prospects** — outline for informal discussions: review the history, identify previous reviewers, relay current thoughts, ask questions, get feedback, adjust, repeat with others

Benefits: no surprises, collective knowledge, give and take, each person is a person not an enemy. [Platt]
```

- [ ] **Step 3: Update the source citation header**

At the top of `docs/sensei-knowledge-base.md` (lines 3-8), add the Platt source to the list. Find:
```
- **Liker**: "The Toyota Way" by Jeffrey Liker (2nd ed., 2021)
```

After it, add:
```
- **Platt**: TMMNA Pocketmod by Tim Platt (1998-2001), Toyota internal training material
```

- [ ] **Step 4: Commit**

```bash
git add docs/sensei-knowledge-base.md
git commit -m "docs: enrich KB with A3 communication section, expand nemawashi to 8-component method"
```

---

### Task 3: Create the shared story A3 template

**Files:**
- Create: `skills/shared/a3-story-template.html`

Reference the existing `skills/shared/a3-template.html` for CSS patterns and styling conventions. The story template shares the same visual language (header, fonts, section styles, evidence blocks) but has a different body structure (configurable sections, audience banner, nemawashi footer).

- [ ] **Step 1: Create the story template HTML file**

Create `skills/shared/a3-story-template.html` with this complete content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sensei A3 — {{TITLE}}</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f0; color: #1a1a1a; padding: 16px; font-size: 12px; }
.a3 { background: white; border: 1px solid #ccc; max-width: 1100px; margin: 0 auto; box-shadow: 0 2px 12px rgba(0,0,0,0.12); }
.a3-header { background: #1a1a2e; color: white; padding: 10px 16px; display: flex; justify-content: space-between; align-items: center; }
.a3-header h1 { font-size: 14px; font-weight: 600; }
.a3-header .meta { font-size: 10px; color: #aaa; text-align: right; line-height: 1.6; }
.audience-banner { background: #f8f4e8; border-bottom: 2px solid #e8a020; padding: 7px 16px; font-size: 11px; display: flex; justify-content: space-between; align-items: center; }
.audience-banner strong { color: #b07010; text-transform: uppercase; font-size: 9px; letter-spacing: 1px; margin-right: 6px; }
.type-badge { display: inline-block; background: #e8f0fb; border: 1px solid #1a6eb5; color: #1a3a6e; border-radius: 3px; padding: 2px 8px; font-size: 10px; font-weight: 600; }
.a3-body { display: grid; grid-template-columns: 1fr 1fr; }
.col { padding: 14px 16px; }
.col-left { border-right: 2px solid #ddd; }
.col-heading { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px; padding-bottom: 5px; border-bottom: 2px solid; }
.col-left .col-heading { color: #1a6eb5; border-color: #1a6eb5; }
.col-right .col-heading { color: #c05a00; border-color: #c05a00; }
.section { margin-bottom: 14px; }
.section.active { border-left: 3px solid #1a6eb5; padding-left: 13px; background: #fafcff; }
.section.locked { opacity: 0.35; }
.section.locked .section-label::after { content: " — Pending"; font-weight: 400; font-style: italic; color: #999; text-transform: none; letter-spacing: 0; }
.section-label { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #666; margin-bottom: 5px; }
.section-text { font-size: 11px; line-height: 1.6; color: #222; }
.section-text ul { margin: 4px 0 4px 16px; }
.section-text li { margin-bottom: 3px; }
pre.evidence { background: #f8f8f5; border: 1px solid #ddd; border-left: 3px solid #1a6eb5; border-radius: 3px; padding: 10px 12px; margin: 8px 0; font-family: 'SF Mono', 'Menlo', 'Consolas', monospace; font-size: 10px; line-height: 1.5; color: #222; white-space: pre; overflow-x: auto; }
.status-badge { display: inline-block; border-radius: 3px; padding: 2px 8px; font-size: 10px; font-weight: 600; }
.status-badge.draft { background: #fff3cd; border: 1px solid #e67e22; color: #7a3d00; }
.status-badge.review { background: #e8f0fb; border: 1px solid #1a6eb5; color: #1a3a6e; }
.status-badge.final { background: #e6f9ee; border: 1px solid #27ae60; color: #0d5a20; }
hr.div { border: none; border-top: 1px solid #eee; margin: 12px 0; }
.a3-footer { border-top: 2px solid #ddd; padding: 12px 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.footer-section h3 { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #666; margin-bottom: 8px; }
.reviewer-row { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; font-size: 10px; }
.reviewer-status { display: inline-block; border-radius: 3px; padding: 1px 6px; font-size: 9px; font-weight: 600; }
.reviewer-status.pending { background: #f0f0f0; color: #888; }
.reviewer-status.approved { background: #e6f9ee; border: 1px solid #27ae60; color: #0d5a20; }
.reviewer-status.feedback { background: #fff3cd; border: 1px solid #e67e22; color: #7a3d00; }
.check-row { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; font-size: 10px; color: #444; }
.check-box { width: 13px; height: 13px; border: 1.5px solid #aaa; border-radius: 2px; display: inline-block; flex-shrink: 0; }
.check-box.checked { background: #27ae60; border-color: #27ae60; position: relative; }
.check-box.checked::after { content: "✓"; color: white; font-size: 10px; font-weight: 700; position: absolute; top: -1px; left: 1px; }
.pr-link { font-size: 10px; color: #1a6eb5; margin-top: 8px; }
.pr-link a { color: #1a6eb5; text-decoration: underline; }
@media print {
  body { background: white; padding: 0; }
  .a3 { box-shadow: none; border: 1px solid #999; max-width: 100%; width: 100%; }
  .a3, * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .section, .reviewer-row { page-break-inside: avoid; }
  .col-heading, .section-label { page-break-after: avoid; }
  pre.evidence { border-color: #999; background: #f8f8f8; }
  .section.locked { opacity: 0.25; }
  .section.active { border-left-color: #999; background: white; }
}
</style>
</head>
<body>
<div class="a3">

  <div class="a3-header">
    <h1>{{TITLE}}</h1>
    <div class="meta">Owner: {{OWNER}} &nbsp;·&nbsp; {{DATE}}<br><span class="status-badge {{STATUS_CLASS}}">{{STATUS}}</span></div>
  </div>

  <div class="audience-banner">
    <div><strong>Audience:</strong> {{AUDIENCE}}</div>
    <div><span class="type-badge">{{STORY_TYPE_BADGE}}</span></div>
  </div>

  <div class="a3-body">

    <div class="col col-left">
      <div class="col-heading">{{LEFT_HEADING}}</div>
      {{LEFT_SECTIONS}}
    </div>

    <div class="col col-right">
      <div class="col-heading">{{RIGHT_HEADING}}</div>
      {{RIGHT_SECTIONS}}
    </div>

  </div>

  <div class="a3-footer">
    <div class="footer-section">
      <h3>Nemawashi</h3>
      {{NEMAWASHI}}
    </div>
    <div class="footer-section">
      <h3>Rock Solid Self-Check</h3>
      <div class="check-row"><span class="check-box"></span> Could I handwrite this on one page?</div>
      <div class="check-row"><span class="check-box"></span> Does the audience know why they're reading this?</div>
      <div class="check-row"><span class="check-box"></span> Would someone with no context follow it?</div>
      <div class="check-row"><span class="check-box"></span> Can I tell this story in 3 minutes?</div>
      {{PR_LINK}}
    </div>
  </div>

</div>
</body>
</html>
```

- [ ] **Step 2: Open the template in a browser and verify it renders**

```bash
open skills/shared/a3-story-template.html
```

Verify: the template renders with placeholder tokens visible ({{TITLE}}, etc.), two-column layout intact, footer with nemawashi and Rock Solid sections visible. No CSS errors in browser console.

- [ ] **Step 3: Commit**

```bash
git add skills/shared/a3-story-template.html
git commit -m "feat: add configurable A3 story template with nemawashi footer and Rock Solid checks"
```

---

### Task 4: Create type definition files — Information stories (Types 1, 2, 3, 7)

**Files:**
- Create: `skills/story/types/1-educate-details.md`
- Create: `skills/story/types/2-illumination-unknown.md`
- Create: `skills/story/types/3-compare-contrast.md`
- Create: `skills/story/types/7-education-satisfaction.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p skills/story/types
```

- [ ] **Step 2: Create Type 1 — Educate to the Details**

Create `skills/story/types/1-educate-details.md`:

```markdown
# Type 1: Educate to the Details

## When to Use

You need to teach the audience something complex. They need the big picture first, then progressively more detail. The story moves from "what is this?" to "how does it work?" to "what are the specifics?" Used for onboarding, technical explanations, and introducing new systems or processes.

## Column Mapping

- Left column heading: Overview
- Left sections:
  1. Big Picture — the simplest description of what this is and why it matters
  2. Medium Detail — how it works at a functional level
- Right column heading: Detail
- Right sections:
  3. Full Detail — the specifics: numbers, configurations, edge cases, technical depth

## Section Definitions

### 1. Big Picture
**Purpose:** Give the audience the simplest possible understanding of what this is.
**Content:** What is it, why does it exist, who does it affect. No jargon. No implementation details. A non-expert should walk away understanding the concept.
**Compression test:** Can you explain this section in one sentence to someone in an elevator?
**Coaching prompts:**
- "If you had to explain this to someone who knows nothing about your field, what would you say?"
- "What's the one thing the audience must understand before anything else makes sense?"
**LLM directives:** Write at the level of a newspaper summary. No acronyms without expansion. No technical terms without plain-language equivalents.

### 2. Medium Detail
**Purpose:** Explain how it works at a functional level.
**Content:** The mechanism, the process, the flow. Enough detail that the audience could explain it to a colleague. Diagrams or evidence blocks are useful here.
**Compression test:** Could you draw this on a whiteboard in 2 minutes?
**Coaching prompts:**
- "Walk me through how this actually works, step by step."
- "What does the audience need to know to make decisions about this?"
**LLM directives:** Use evidence blocks for process flows or comparisons. Keep explanations functional, not exhaustive.

### 3. Full Detail
**Purpose:** Provide the specifics for those who need to act on this information.
**Content:** Numbers, configurations, timelines, technical specifications, edge cases. This is the reference section.
**Compression test:** Is every detail here something the audience will use? If a detail is "nice to know" but not actionable, cut it.
**Coaching prompts:**
- "What specific details does the audience need to do their job with this information?"
- "Is there anything here that only you find interesting? Cut it."
**LLM directives:** Use evidence blocks for data tables and specifications. Every detail must be actionable for the stated audience.

## Example

**Subject:** New Deployment Pipeline
**Audience:** Development team (20 engineers, mixed seniority)

**Big Picture:** We're replacing manual deployments with an automated pipeline. Code merged to main deploys to staging automatically. Promotion to production requires one approval. Rollback is one click.

**Medium Detail:**
```
Merge to main → Build (2 min) → Test (4 min) → Deploy staging → Smoke test
    ↓ approval
Deploy production → Health check → Done
    ↓ failure
Auto-rollback → Alert on-call
```

**Full Detail:** Build uses Node 20 in GitHub Actions. Test suite runs 340 tests in parallel across 4 runners. Staging deploys to `staging.example.com`. Production approval requires one team lead. Rollback triggers if error rate >1% in first 5 minutes. Alert goes to #ops-oncall.
```

- [ ] **Step 3: Create Type 2 — Illumination of the Unknown**

Create `skills/story/types/2-illumination-unknown.md`:

```markdown
# Type 2: Illumination of the Unknown

## When to Use

You need to introduce something the audience doesn't know yet. The trick: start from what they already understand, then bridge to the new thing. Used when introducing new technology, sharing research findings, or explaining unfamiliar concepts to a knowledgeable audience.

## Column Mapping

- Left column heading: What You Know
- Left sections:
  1. Familiar Ground — the shared understanding you're building from
- Right column heading: What's New
- Right sections:
  2. The Bridge — how the known connects to the unknown
  3. The New Territory — the thing itself, now that the audience has context

## Section Definitions

### 1. Familiar Ground
**Purpose:** Establish the shared starting point. The audience should nod at everything in this section.
**Content:** What the audience already knows, believes, or has experienced. This is not background — it's their existing mental model that you're about to extend.
**Compression test:** Would the audience say "yes, I know this" to every bullet? If anything is new to them, it belongs in the right column.
**Coaching prompts:**
- "What does your audience already know about this area?"
- "What assumptions do they hold that you're going to build on — or challenge?"
**LLM directives:** Write from the audience's perspective, not the author's. Use their vocabulary, not yours.

### 2. The Bridge
**Purpose:** Connect the known to the unknown. This is where the audience's understanding shifts.
**Content:** The insight, analogy, comparison, or evidence that makes the unknown make sense in terms of the known. Often the most important section.
**Compression test:** If you removed this section, would the jump from left to right feel abrupt? If yes, the bridge is doing its job.
**Coaching prompts:**
- "What's the connection between what they know and what you're about to tell them?"
- "Is there an analogy that makes this click?"
**LLM directives:** Use analogies or evidence blocks showing the relationship between known and new. This section carries the "aha" moment.

### 3. The New Territory
**Purpose:** Present the new information, now that the audience has context to receive it.
**Content:** The thing itself. Facts, implications, what it means for the audience. Because of the bridge, this section can go deeper without losing people.
**Compression test:** Does every point connect back to something in the left column or the bridge? Orphan facts that don't connect to the audience's world should be cut.
**Coaching prompts:**
- "Now that they understand the connection, what do they need to know?"
- "What should they do differently because of this new information?"
**LLM directives:** Reference the bridge section explicitly where possible. Show implications for the audience's work.

## Example

**Subject:** Why We're Adopting Edge Computing
**Audience:** Backend engineering team

**Familiar Ground:** Our API serves 50ms p99 from us-east-1. Users in Asia-Pacific see 280ms. We've optimized the application — the latency is physics, not code. CDNs solve this for static assets. Our APIs are dynamic.

**The Bridge:** What if we could run API logic at the CDN edge, the same way we already serve static files from edge nodes? Same principle — move computation closer to the user — but for dynamic responses.

**The New Territory:** Edge functions run in 30+ regions, execute in <5ms cold start, and handle request/response logic. Our auth checks, personalization, and A/B routing can move to the edge. Database queries stay centralized but cached at the edge with 60s TTL. Expected result: Asia-Pacific p99 drops from 280ms to 60ms.
```

- [ ] **Step 4: Create Type 3 — Compare & Contrast**

Create `skills/story/types/3-compare-contrast.md`:

```markdown
# Type 3: Compare & Contrast

## When to Use

You want to show what changed or will change. The story puts current and new side by side so the audience can see the differences clearly. Used for before/after presentations, migration plans, process changes, and any situation where the audience needs to understand a shift.

## Column Mapping

- Left column heading: Current
- Left sections:
  1. Current Situation — how things are today
- Right column heading: New
- Right sections:
  2. New Situation — how things will be (or have become)
  3. What Changes — the specific differences and their impact

## Section Definitions

### 1. Current Situation
**Purpose:** Show the audience the world they know, described clearly enough that the comparison is fair.
**Content:** Facts about the current state. Measurements, processes, tools, outcomes. Neutral tone — don't make the current state sound bad to make the new state sound good.
**Compression test:** Is this a fair description? Would someone who likes the current state agree with every point?
**Coaching prompts:**
- "Describe the current situation as someone who is satisfied with it would describe it."
- "What are the strengths of the current approach? Include them — the comparison is more credible."
**LLM directives:** Neutral language. Include strengths and weaknesses of the current state. Use evidence blocks for metrics.

### 2. New Situation
**Purpose:** Show what the new state looks like, in the same terms as the current state.
**Content:** Same dimensions as the current situation but with new values. If you measured latency on the left, measure latency on the right. Same categories, different numbers.
**Compression test:** Can the reader hold up left and right side by side and see the differences immediately? If the sections use different categories, they can't compare.
**Coaching prompts:**
- "Describe the new situation using the same dimensions as the current one."
- "Where does the new situation have trade-offs? Include them."
**LLM directives:** Mirror the structure of the current situation section. Use evidence blocks with matching formats for direct comparison.

### 3. What Changes
**Purpose:** Make the differences explicit so the audience doesn't have to infer them.
**Content:** A summary of what specifically changes, who is affected, and what the impact is. The "so what" of the comparison.
**Compression test:** If the audience only read this section, would they understand the key differences?
**Coaching prompts:**
- "What are the three biggest differences?"
- "Who is most affected by this change and how?"
**LLM directives:** Use a comparison table in an evidence block. List changes as concrete items, not generalizations.

## Example

**Subject:** Migration from REST to GraphQL
**Audience:** Frontend team leads

**Current Situation:** 47 REST endpoints, average 3 calls per page load, 120ms total fetch time. Frontend maintains a translation layer mapping API responses to component props. New features require backend endpoint changes (2-3 day lead time).

**New Situation:** Single GraphQL endpoint, 1 call per page load with exact field selection, 80ms total fetch time. Frontend queries match component data needs directly. New features: frontend-driven schema queries, no backend changes for existing data.

**What Changes:**
```
                    REST (Current)    GraphQL (New)
Calls per page      3 avg             1
Fetch time          120ms             80ms
New feature lead    2-3 days          0 (frontend-driven)
Learning curve      Known             ~2 weeks ramp
Caching             HTTP native       Requires config
Monitoring          Per-endpoint      Per-query
```
```

- [ ] **Step 5: Create Type 7 — Education / Satisfaction**

Create `skills/story/types/7-education-satisfaction.md`:

```markdown
# Type 7: Education / Satisfaction

## When to Use

You need to educate the audience on a series of related topics. Unlike Type 1 (which drills from overview to detail on one subject), this type covers multiple distinct topics that together tell a complete story. Used for training material, quarterly reviews, status updates, and any presentation that covers several related areas.

## Column Mapping

- Left column heading: Introduction
- Left sections:
  1. Purpose & Background — why we're covering these topics and what ties them together
  2. Topic sections (first half) — individual topic points
- Right column heading: Conclusion
- Right sections:
  3. Topic sections (second half) — remaining topic points
  4. Summary & Benefits — what the audience should take away

Note: The number of topic sections is variable (typically 3-5 total). The sensei asks "how many topics do you need to cover?" during routing and distributes them across the two columns to maintain visual balance.

## Section Definitions

### 1. Purpose & Background
**Purpose:** Tell the audience why they're reading this and what connects the topics.
**Content:** The purpose of the communication, the background that ties the topics together, and what the audience should expect to learn.
**Compression test:** In one sentence, can you state the purpose? If not, the topics might not belong together on one A3.
**Coaching prompts:**
- "What ties these topics together? Why are they on the same page?"
- "What should the audience be able to do after reading this?"
**LLM directives:** State the purpose in the first sentence. Keep background to 2-3 bullets max. The topics do the heavy lifting.

### 2-N. Topic Sections
**Purpose:** Each topic gets its own section with a clear, self-contained point.
**Content:** The key information for this topic. Each section should stand on its own — a reader could skip to any topic and understand it without reading the others.
**Compression test:** Can you state this topic's point in one bullet? The section should expand that bullet, not replace it.
**Coaching prompts:**
- "What is the one thing the audience needs to know about this topic?"
- "If they forget everything else, what should stick?"
**LLM directives:** Each topic section gets a clear heading. 3-5 bullets per topic. Use evidence blocks for data within topics.

### Summary & Benefits
**Purpose:** Bring it together. What did we cover and what does the audience gain from knowing it?
**Content:** Brief recap of each topic's key point (one line each), then the benefits or implications for the audience.
**Compression test:** Is the summary shorter than any individual topic? If not, it's repeating content rather than synthesizing it.
**Coaching prompts:**
- "If someone skipped to the summary, what do they need to know?"
- "What's the benefit to the audience of understanding all of this together?"
**LLM directives:** One sentence per topic in the recap. Benefits stated from the audience's perspective, not the author's.

## Example

**Subject:** Q1 Platform Health Review
**Audience:** Engineering leadership

**Purpose & Background:** Quarterly review of platform reliability, performance, and cost. These three areas are connected — Q1 cost reduction initiatives affected both reliability and performance. The audience should leave knowing where we stand and what Q2 priorities should be.

**Topic 1 — Reliability:** Uptime 99.94% (target: 99.95%). Two incidents >5 min: database failover (Jan 12, 8 min) and CDN config error (Feb 28, 6 min). Both had root cause analyses completed. Error budget consumed: 92%.

**Topic 2 — Performance:** P99 latency improved from 180ms to 140ms after connection pooling migration. Homepage LCP improved from 2.1s to 1.6s. API throughput up 15% with no additional infrastructure.

**Topic 3 — Cost:** Monthly infrastructure spend reduced from $84k to $71k (-15%). Main drivers: reserved instance conversion ($8k), unused resource cleanup ($3k), right-sizing ($2k).

**Summary & Benefits:** Reliability just under target (error budget tight — prioritize in Q2). Performance improved significantly with no cost increase. Cost down 15% and sustainable. Q2 priority: shore up reliability margin before Q3 traffic growth.
```

- [ ] **Step 6: Commit**

```bash
git add skills/story/types/1-educate-details.md skills/story/types/2-illumination-unknown.md skills/story/types/3-compare-contrast.md skills/story/types/7-education-satisfaction.md
git commit -m "feat: add story type definitions — information types (1, 2, 3, 7)"
```

---

### Task 5: Create type definition files — Recommendation stories (Types 4, 5, 6)

**Files:**
- Create: `skills/story/types/4-standard-proposal.md`
- Create: `skills/story/types/5-correcting-discrepancy.md`
- Create: `skills/story/types/6-develop-roadmap.md`

- [ ] **Step 1: Create Type 4 — Standard Toyota Proposal**

Create `skills/story/types/4-standard-proposal.md`:

```markdown
# Type 4: Standard Toyota Proposal

## When to Use

You're proposing an improvement. A problem exists, you understand it, and you have a proposal that addresses it. The audience needs to see the problem and its causes before they'll agree to the solution. This is the most common recommendation A3 at Toyota. Used for budget requests, process changes, tool adoptions, organizational changes, and any situation where you're asking for agreement to act.

## Column Mapping

- Left column heading: Context
- Left sections:
  1. Current Situation / Background — what's happening now and why it matters
  2. Problems & Cause — what's wrong and why
- Right column heading: Proposal
- Right sections:
  3. Proposal & Benefits — what you're recommending and what it gets us

## Section Definitions

### 1. Current Situation / Background
**Purpose:** Give the audience the facts about where things stand today.
**Content:** The current state described in facts, not opinions. Measurements, volumes, timelines, who is involved. Set the stage so the problems section has context.
**Compression test:** Can you state the current situation in 5 bullets or fewer? If not, you're giving background, not a situation.
**Coaching prompts:**
- "Describe the current situation in facts. What would someone see if they walked in today?"
- "What does the audience already know? Don't repeat what they know — add what they're missing."
**LLM directives:** Facts only. No value judgments ("unfortunately", "problematic"). Use evidence blocks for metrics. The facts should speak for themselves.

### 2. Problems & Cause
**Purpose:** Show what's wrong and why. The audience must feel the problem before the right column makes sense.
**Content:** Specific problems with their causes. Each problem should be measurable or observable. The connection between problem and cause should be clear, not assumed.
**Compression test:** For each problem, can you point to a number or observation? If a problem is a feeling ("the team is frustrated"), find the fact behind the feeling.
**Coaching prompts:**
- "What breaks? What's slow? What costs too much? What fails?"
- "How do you know this is a problem? What evidence do you have?"
- "Why does this problem exist? Don't guess — what have you observed?"
**LLM directives:** Each problem gets a clear statement + cause. Use evidence blocks for data supporting the problems. If a cause is uncertain, say so — don't present assumptions as facts.

### 3. Proposal & Benefits
**Purpose:** Present the recommendation and make the benefits concrete.
**Content:** What you're proposing, how it addresses each problem from the left column, and what the benefits are in measurable terms. Each benefit should trace back to a problem.
**Compression test:** Does every benefit connect to a problem on the left? Orphan benefits ("also improves morale") weaken the story. Can the audience say "yes" or "no" to a specific proposal?
**Coaching prompts:**
- "What specifically are you proposing? One sentence."
- "For each problem on the left, how does your proposal address it?"
- "What does the audience have to agree to? Make it concrete."
**LLM directives:** Lead with the proposal in one sentence. Then map benefits to problems. Use evidence blocks for projected metrics. End with a clear ask.

## Example

**Subject:** Migrate CI Pipeline to GitHub Actions
**Audience:** VP Engineering, Platform Team Leads

**Current Situation / Background:** Self-hosted Jenkins cluster serves 14 teams, 340 builds/day across 3 controller nodes. Maintained by 2 SREs + 1 contractor (3 FTE equivalent). Monthly cost: $28,400. Infrastructure is 4 years old.

**Problems & Cause:**
1. Capacity doesn't scale — fixed runner pool, peak hours (9-11am) queue 3x longer. Cause: no autoscaling on self-hosted infra.
2. Maintenance burden is constant — plugin updates, security patches, node failures consume 60% of SRE-2's time. Cause: self-hosted means we own the full stack.
3. No isolation — a bad pipeline crashed the shared controller twice in Q1. Cause: shared execution environment with no sandboxing.

**Proposal & Benefits:** Migrate to GitHub Actions with hosted runners for standard builds, self-hosted for GPU jobs only.
- Benefit 1: Queue wait → near-zero (autoscaling addresses Problem 1)
- Benefit 2: Eliminate 2.5 FTE maintenance burden (hosted infra addresses Problem 2)
- Benefit 3: Full pipeline isolation per run (addresses Problem 3)
- Cost: $16k/month GHA + $4k/month self-hosted GPU = $20k (vs $28.4k current, net savings $8.4k/month)
```

- [ ] **Step 2: Create Type 5 — Correcting Discrepancy from Standard**

Create `skills/story/types/5-correcting-discrepancy.md`:

```markdown
# Type 5: Correcting Discrepancy from Standard

## When to Use

A standard exists and reality has drifted from it. You need to show the gap and propose countermeasures to close it. This is NOT problem-solving (Type 0) — problem-solving investigates the unknown. This story type shows that a known standard is not being followed and proposes corrections. The audience needs to see the standard, see the gap, and agree to the countermeasures.

## Column Mapping

- Left column heading: Situation
- Left sections:
  1. Current Situation — what's happening now
  2. Standard & Discrepancy — what the standard says and where reality diverges
- Right column heading: Response
- Right sections:
  3. Countermeasures — what we're doing to close the gap

## Section Definitions

### 1. Current Situation
**Purpose:** Describe reality as it is, without judgment.
**Content:** Observable facts about the current state. What the process looks like now, what the outputs are, what the metrics show. The audience should be able to verify these facts.
**Compression test:** Is every fact in this section verifiable? If someone went and looked, would they see what you describe?
**Coaching prompts:**
- "What does someone see if they watch this process happen today?"
- "What are the current numbers? Not what you think they should be — what they actually are."
**LLM directives:** Facts only. Use evidence blocks for current metrics. No language that presupposes the standard ("only 22% compliance" is judgment — "22% of PRs reviewed within 4 hours" is fact).

### 2. Standard & Discrepancy
**Purpose:** Show the standard and make the gap visible. This is the core of the story — the audience must see the discrepancy clearly.
**Content:** The standard (what, when it was established, by whom) and the specific gap between standard and current reality. Use side-by-side comparison or evidence blocks.
**Compression test:** Can the audience see the gap in 5 seconds? If they have to read a paragraph to find it, the format is wrong.
**Coaching prompts:**
- "What is the standard? When was it agreed? Who agreed to it?"
- "Show me the gap. Standard says X, reality is Y. What's the number?"
**LLM directives:** State the standard explicitly (source, date, who agreed). Use an evidence block showing standard vs. actual side by side. The gap should be immediately visible.

### 3. Countermeasures
**Purpose:** Propose specific actions to close the gap and return to the standard.
**Content:** Countermeasures that directly address the discrepancy. Each countermeasure should connect to a specific aspect of the gap. Include who is responsible and by when.
**Compression test:** Does each countermeasure point at a specific part of the gap? Generic countermeasures ("improve the process") are not countermeasures.
**Coaching prompts:**
- "For each part of the gap, what specific action closes it?"
- "Who owns each countermeasure? By when?"
- "How will you know if the gap is closing? What will you measure?"
**LLM directives:** Number each countermeasure. Link each to the specific gap it addresses. Include owner and target date. Add a measurement plan — how progress will be tracked.

## Example

**Subject:** Code Review Turnaround
**Audience:** Engineering leads

**Current Situation:** Average PR review time: 3.2 days. 40% of PRs wait >48 hours for first review. Team velocity dropped 15% in Q1. 78% of developers cite review wait time as their top blocker.

**Standard & Discrepancy:**
```
Standard: First review within 4 business hours
(Agreed: team retro, Sept 2025. All leads signed off.)

            Standard    Actual     Gap
First review    4 hrs      26 hrs     6.5x
% on time      100%       22%        78% miss
```

**Countermeasures:**
1. Slack bot pings assigned reviewer at 2-hour mark (→ addresses awareness gap, Owner: Platform team, By: Apr 30)
2. Rotate daily "review first" duty across team (→ addresses no dedicated review time, Owner: Team leads, By: Apr 22)
3. PRs >500 lines auto-flagged for split before review assignment (→ addresses review burden on large PRs, Owner: DevEx, By: May 15)
4. Weekly review-time metric on team dashboard (→ addresses visibility, Owner: Platform team, By: Apr 25)
```

- [ ] **Step 3: Create Type 6 — Develop the Roadmap**

Create `skills/story/types/6-develop-roadmap.md`:

```markdown
# Type 6: Develop the Roadmap

## When to Use

You've identified trends, analyzed their impact, and need to propose a strategic direction. The audience needs to see the evidence (trends) before they'll agree to the direction. Used for strategic planning, technology roadmaps, organizational direction, and any situation where the audience needs to understand why you're heading in a particular direction.

## Column Mapping

- Left column heading: Analysis
- Left sections:
  1. Trends — what's changing in the environment
  2. Impact Analysis — what these trends mean for us
- Right column heading: Direction
- Right sections:
  3. Strategic Direction — where we should go and the roadmap to get there

## Section Definitions

### 1. Trends
**Purpose:** Show the audience what's changing in the environment that matters.
**Content:** Observable trends with evidence. Market shifts, technology changes, competitive moves, internal metrics showing a trajectory. Each trend should be supported by data, not opinion.
**Compression test:** For each trend, can you point to data? A trend without data is a guess.
**Coaching prompts:**
- "What's changing that affects us? Not what might change — what's already changing."
- "What evidence do you have for each trend? Numbers, events, observations."
**LLM directives:** Each trend gets a heading, 1-2 sentences of description, and a data point or evidence block. No speculative trends — only observable ones.

### 2. Impact Analysis
**Purpose:** Translate trends into implications for the audience's world.
**Content:** What each trend means for the organization, team, or product. The "so what" that connects external trends to internal decisions. Include both risks (what happens if we don't act) and opportunities (what we can gain by acting).
**Compression test:** Does each impact trace back to a specific trend? Impacts without trends are opinions.
**Coaching prompts:**
- "For each trend, what does it mean for us specifically?"
- "What's the risk of doing nothing? What's the opportunity if we act?"
**LLM directives:** Map each impact to its trend explicitly. Use evidence blocks for projections. State both risk and opportunity for each.

### 3. Strategic Direction
**Purpose:** Propose where to go and the high-level roadmap to get there.
**Content:** The strategic direction (one clear statement), the key initiatives that support it, and a timeline. Each initiative should connect to an impact from the left column.
**Compression test:** Can you state the strategic direction in one sentence? If not, you have multiple strategies competing on one page — split them.
**Coaching prompts:**
- "In one sentence, where are you recommending we go?"
- "What are the 3-5 things we need to do to get there?"
- "What's the timeline? What comes first and why?"
**LLM directives:** Lead with the direction in one sentence. Then list initiatives mapped to impacts. Use a timeline evidence block for the roadmap. Keep it to 3-5 major initiatives.

## Example

**Subject:** API Platform Strategy 2026-2027
**Audience:** CTO, Engineering VPs

**Trends:**
1. API traffic growing 40% YoY (internal: 2.1B calls/month, up from 1.5B)
2. Partner integrations doubled in 12 months (47 → 94 active partners)
3. Industry moving to event-driven architectures (3 of our 5 largest partners now prefer webhooks over polling)

**Impact Analysis:**
- Trend 1 → Current infrastructure headroom exhausted by Q3 2026 at current growth rate. Risk: degraded latency affecting partner SLAs.
- Trend 2 → Partner onboarding takes 6 weeks average. At current growth, support team becomes bottleneck by Q2. Opportunity: self-service reduces onboarding to <1 week.
- Trend 3 → Polling-based partners generate 60% of our API traffic for 10% of the data value. Opportunity: webhooks reduce load while improving partner experience.

**Strategic Direction:** Build a self-service, event-driven API platform that scales to 5B calls/month and onboards partners in <1 week.

Roadmap:
```
Q2 2026: Event infrastructure (webhooks, event catalog)
Q3 2026: Self-service partner portal (API keys, docs, sandbox)
Q4 2026: Migrate top 10 polling partners to webhooks
Q1 2027: Scale infrastructure to 5B/month capacity
```
```

- [ ] **Step 4: Commit**

```bash
git add skills/story/types/4-standard-proposal.md skills/story/types/5-correcting-discrepancy.md skills/story/types/6-develop-roadmap.md
git commit -m "feat: add story type definitions — recommendation types (4, 5, 6)"
```

---

### Task 6: Create the /sensei:story SKILL.md

**Files:**
- Create: `skills/story/SKILL.md`

This is the main skill file — the router, mode rules, compression discipline, progressive build instructions, and nemawashi tracking. It reads the KB at invocation and the selected type file after routing.

- [ ] **Step 1: Create the skill file**

Create `skills/story/SKILL.md` with the full content below. This is the longest single file in the plan (~350 lines). Read it carefully — it contains the router logic, both mode definitions, compression enforcement, progressive build instructions, and nemawashi tracking.

```markdown
---
name: story
description: "Use when someone needs to communicate clearly using Toyota's A3 story format. Routes to the right story type (proposal, comparison, education, roadmap, discrepancy correction, or illumination), then builds the A3 progressively with compression discipline. Works in two modes: coaching (human builds the story with sensei guidance) or LLM (sensei builds the story for confirmation). Produces a two-column A3 HTML artifact. Invoke with /sensei:story."
---

# /sensei:story — Toyota A3 Story Types

You are a sensei guiding the creation of an A3 communication paper. The A3 is Toyota's format for structured communication — one page, two columns, compressed to clarity.

There are 7 story types. Each has a specific structure for a specific communication purpose. Your job is to route to the right type, then guide the user through building it section by section.

**This is NOT problem-solving.** Problem-solving is `/sensei:work` — investigation where you don't know the answer when you start. Story types are communication — the user knows what they want to say and the A3 structures how they say it.

Read `docs/sensei-knowledge-base.md` now — it contains the A3 communication principles and nemawashi method you will reference.

---

## Step 0: Route

### Determine the story type

Present the 7 types and help the user select one:

> "What kind of story are you telling? Pick the type that fits, or describe what you're trying to communicate and I'll suggest one."
>
> **Information** (telling a story to inform):
> 1. **Educate to the Details** — teach something complex, big picture first then drill down
> 2. **Illumination of the Unknown** — introduce something new by starting from what they know
> 3. **Compare & Contrast** — show what changed or will change, side by side
> 7. **Education / Satisfaction** — cover a series of related topics
>
> **Recommendation** (telling a story to get agreement):
> 4. **Standard Toyota Proposal** — show a problem, propose a solution
> 5. **Correcting Discrepancy from Standard** — a standard isn't being met, here are countermeasures
> 6. **Develop the Roadmap** — trends point in a direction, here's the strategic plan
>
> Or tell me what you're trying to communicate and I'll suggest the right type.

If the user describes their communication rather than picking a number, identify the type and explain why: "That's a Standard Toyota Proposal — you're showing a problem and recommending a solution. Does that sound right?"

### Determine the mode

Ask: "Are you building this story yourself, or should I build it for you?"

- **"I'm building it"** → Coaching mode
- **"You build it"** → LLM mode

### Gather the essentials

After type and mode are set:

1. **Audience:** "Who is reading this A3? Be specific — their role and what they care about determines how you tell the story."
2. **Subject:** "In one sentence, what is this story about?"

### Read the type definition

Read the selected type file from `skills/story/types/[N]-[name].md`. This gives you the section definitions, column mappings, coaching prompts, and examples for this specific type.

### Create the A3

Read `skills/shared/a3-story-template.html`. Write the initial A3 to `kivna/output/sensei-[slug]/sensei-[slug].html` with:
- Title: the subject
- Audience banner: filled
- Story type badge: filled
- Owner, date: filled
- Status: "Draft — Step 1 of N"
- All sections: `.locked`

Open in browser: `open kivna/output/sensei-[slug]/sensei-[slug].html`

The slug comes from the subject (lowercase, hyphens, max 40 chars).

---

## Building Sections

Work through each section defined in the type file, in order. For each section:

### Coaching Mode (Human)

1. **Ask the coaching prompts** from the type definition, one at a time
2. **Listen and reflect** — paraphrase what you heard to confirm understanding
3. **Challenge weak content:**
   - Opinions without facts: "That's your opinion. What's the fact behind it?"
   - Vague statements: "What specifically do you mean? Give me a number or an example."
   - Too much content: "That's more than one A3 section can hold. What's the one thing?"
4. **Apply the compression test** from the type definition for this section
5. **Never fill in the section for the human** — the content comes from them, the structure comes from you
6. **Confirm:** "Here's what I heard for this section: [compressed summary]. Is that right?"
7. **Rewrite the A3** with this section filled in, next section set to `.active`

### LLM Mode

1. **Gather context** — read relevant files, ask the user for specific information needed for this section
2. **Draft the section** — write it following the LLM directives from the type definition
3. **Apply the compression test** — if the draft exceeds 7 bullet points or fails any Rock Solid test, rewrite tighter before presenting
4. **Present for confirmation:** "Here's my draft for [section name]: [content]. Does this capture it?"
5. **Revise if needed** — the user may correct, add, or cut
6. **Rewrite the A3** with this section filled in, next section set to `.active`

### A3 Rewrite Instructions

After each confirmed section, rewrite the full A3 HTML file:

1. Read the current `kivna/output/sensei-[slug]/sensei-[slug].html`
2. Set the confirmed section's content (remove `.locked` or `.active` class, add section text)
3. Set the next section to `.active` class
4. Update status badge: "Draft — Step N of M"
5. Write the updated HTML back to the same file path

Tell the user: "Section [N] confirmed. Refresh your browser to see the A3 update."

---

## Compression Discipline — Rock Solid

These are Toyota's tests for whether a story section is ready. Apply them at every section, both modes.

### Per-section checks

Before confirming any section, verify:

1. **Bullet point cap:** 3-7 bullet points. More than 7 → push back: "This won't fit on the A3. What's the one thing this section needs to say?"
2. **Handwrite test:** Could you handwrite this section on an index card? If not → "Too much. What can you cut?"
3. **Audience test:** Does the audience need this detail? → "Is this for the audience or for you? The audience is [stated audience]."
4. **Grandparent test:** Would someone outside this project follow it? → "Would someone with no context understand this section?"

If a section fails any check, do NOT confirm it. Push back with the specific test that failed and ask for revision.

### After all sections complete

Run the elevator test on the full A3:

- **Coaching mode:** "Walk me through this whole story in 3 minutes. Go."
- **LLM mode:** Read the full A3 and verify it tells a coherent story. If any section doesn't connect to the next, flag it.

---

## Nemawashi

After all sections are confirmed and the A3 is complete:

### Step 1: Identify reviewers

> "Who should review this story before it goes to [audience]? List the names."

Add each reviewer to the nemawashi footer on the A3 with status "Pending."

### Step 2: Optional PR

> "Would you like me to create a PR for reviewers to comment on? (Optional — requires a git repo)"

If yes:
1. Create a branch: `git checkout -b story/[slug]`
2. Stage the A3: `git add kivna/output/sensei-[slug]/`
3. Commit: `git commit -m "story: [subject] — [story type name] A3"`
4. Push: `git push -u origin story/[slug]`
5. Create PR: `gh pr create --title "[Story Type]: [Subject]" --body "A3 story for review. Audience: [audience]. Open the HTML file to read the A3."`
6. Add the PR link to the A3 nemawashi footer
7. Rewrite the A3 with the PR link

### Closing

> "A3 complete. [N] sections, [story type name] format, for [audience]. Nemawashi: [N] reviewers listed. [PR link if created]"
>
> "Remember Platt's rule: review with others to see if it makes sense to them and if they understand. Try it on a friend."
```

- [ ] **Step 2: Verify the skill file has proper frontmatter**

Check that the file starts with the `---` delimited frontmatter containing `name: story` and the `description` field. The description should match what will appear in Claude Code's skill autocomplete.

- [ ] **Step 3: Commit**

```bash
git add skills/story/SKILL.md
git commit -m "feat: add /sensei:story skill — router, modes, compression discipline, progressive build, nemawashi"
```

---

### Task 7: Update plugin.json — add /sensei:story and bump version

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Update plugin.json**

Replace the current content of `.claude-plugin/plugin.json` with:

```json
{
  "name": "sensei",
  "description": "Toyota Sensei for Claude Code. /sensei:work disciplines LLMs through Toyota's 9-step problem-solving framework before touching code. /sensei:coach guides humans through the same framework interactively. /sensei:learn teaches Toyota Way concepts through Q&A and guided learning paths. /sensei:review reads a completed A3 and delivers blunt, red-ink feedback with a verdict (pass/rework/reject). /sensei:story builds A3 communication papers using Toyota's 7 story types — proposals, comparisons, education, roadmaps — with progressive build and compression discipline. Work and coach produce live progress documents and A3 artifacts. Story produces A3 communication papers.",
  "version": "1.4.0",
  "author": {
    "name": "Anthony Maley"
  },
  "keywords": ["tps", "lean", "problem-solving", "a3", "toyota", "coaching", "sensei", "story"],
  "homepage": "https://github.com/anthonymaley/toyota-sensei",
  "repository": "https://github.com/anthonymaley/toyota-sensei",
  "license": "MIT"
}
```

- [ ] **Step 2: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "bump: version 1.4.0 — add /sensei:story, 7 A3 story types"
```

---

## Self-Review Checklist

Spec coverage:
- [x] 7 story types defined (Task 4 + Task 5)
- [x] Router with 3 selection paths + mode detection (Task 6, Step 0)
- [x] Coaching mode rules (Task 6, Building Sections)
- [x] LLM mode rules (Task 6, Building Sections)
- [x] Compression discipline / Rock Solid enforcement (Task 6, Compression section)
- [x] Progressive build (Task 6, A3 Rewrite Instructions)
- [x] Nemawashi tracking + optional PR (Task 6, Nemawashi section)
- [x] Shared story template with configurable sections (Task 3)
- [x] KB rename (Task 1)
- [x] KB enrichment — A3 communication section + nemawashi expansion (Task 2)
- [x] Plugin.json update + version bump (Task 7)
- [x] All existing skills updated with new KB path (Task 1)

Placeholder scan: No TBDs, TODOs, or "implement later" found.

Type consistency: `sensei-knowledge-base.md` used consistently across all tasks. `a3-story-template.html` used consistently. Type file paths match between Task 4/5 definitions and Task 6 SKILL.md references. Template tokens match between Task 3 HTML and Task 6 rewrite instructions.
