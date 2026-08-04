# /sensei:story — A3 Story Types Design Spec

Date: 2026-04-15
Status: Draft

---

## Summary

Add `/sensei:story` to the Toyota Sensei plugin. This skill implements Toyota's 7 A3 story types — structured communication formats used across Toyota for proposals, education, comparison, and strategic direction. These are separate from and parallel to the problem-solving A3 (`/sensei:work`, Type 0). Problem-solving is investigation (you don't know the answer when you start). Story types are communication (you know what you want to say and the A3 structures how you say it).

The 7 story types come from Toyota's internal methodology, documented in the TMMNA pocketmod compiled by Tim Platt. The methodology is Toyota's; Platt recorded it.

Source: `docs/sources/platt-tmmna-pocketmod.md`

---

## The 7 Story Types

### Information Stories (telling a story to inform)

**Type 1 — Educate to the Details**
Structure: Simple overview → Medium detail → Full detail
When to use: You need to teach the audience something complex, starting from the big picture and drilling into specifics.
Left column ("Overview"): Big picture / simple level
Right column ("Detail"): Medium detail / full detail

**Type 2 — Illumination of the Unknown**
Structure: Known → Unknown
When to use: You need to introduce something new by anchoring it to what the audience already understands.
Left column ("What You Know"): Familiar context, shared understanding
Right column ("What's New"): New information, the unknown made clear

**Type 3 — Compare & Contrast**
Structure: Current Situation → New Situation
When to use: You want to show what changed or will change, side by side.
Left column ("Current"): How things are now
Right column ("New"): How things will be / have become

**Type 7 — Education / Satisfaction**
Structure: Introduction (Purpose, Background) → Point 1 → Point 2 → ... → Point N → Conclusion (Summary, Benefits)
When to use: You need to educate the audience on a series of related topics.
Left column ("Introduction"): Purpose, background, and up to 2 topic points
Right column ("Conclusion"): Remaining topic points, summary, benefits
Note: The number of topic points is variable (typically 3-5). The sensei asks "how many topics do you need to cover?" during routing and distributes them across the two columns to maintain visual balance.

### Recommendation Stories (telling a story to get agreement)

**Type 4 — Standard Toyota Proposal**
Structure: Current Situation / Background → Problems & Cause → Proposal & Benefits
When to use: You're proposing an improvement based on identified problems. The audience needs to see the problem before they'll agree to the solution.
Left column ("Context"): Current situation / background, Problems & cause
Right column ("Proposal"): Proposal & benefits

**Type 5 — Correcting Discrepancy from Standard**
Structure: Current Situation → Standard & Discrepancy → Countermeasures
When to use: A standard exists, reality has drifted from it, and you need to show the gap and propose countermeasures to close it. This is NOT problem-solving (Type 0) — this is showing that a known standard is not being followed.
Left column ("Situation"): Current situation, Standard & discrepancy
Right column ("Response"): Countermeasures

**Type 6 — Develop the Roadmap**
Structure: Trends & Analysis → Strategic Direction
When to use: You've identified trends, analyzed their impact, and need to propose a strategic direction.
Left column ("Analysis"): Trends & analysis
Right column ("Direction"): Strategic direction (roadmap)

---

## Architecture

### Approach: Router + Story Type Definition Files

```
skills/story/SKILL.md                          — router + shared rules (~350 lines)
skills/story/types/
  1-educate-details.md                         — type definition (~70 lines)
  2-illumination-unknown.md
  3-compare-contrast.md
  4-standard-proposal.md
  5-correcting-discrepancy.md
  6-develop-roadmap.md
  7-education-satisfaction.md
skills/shared/a3-story-template.html           — configurable story template
```

The SKILL.md contains: router, mode switching (LLM/human), compression discipline (Rock Solid enforcement), progressive build rules, and nemawashi tracking. Each type file defines: sections, column mappings, coaching prompts, LLM directives, compression tests, and one concrete example.

After routing selects a story type, the skill reads only that type's definition file. This keeps context lean — one type per invocation.

### Why not one big SKILL.md?

Seven story types × section definitions, prompts, and examples = 900+ lines inline. The type files keep SKILL.md focused on process (~350 lines) and load only what's needed.

---

## The Router

When `/sensei:story` is invoked, the skill determines the story type and mode.

### Story type selection — three paths:

1. **User specifies directly:** The user's message maps to a type. Sensei confirms: "That's a Standard Toyota Proposal — you're showing a problem and recommending a solution."
2. **User picks from menu:** Sensei presents all 7 types with one-line descriptions. User picks a number.
3. **Sensei recommends:** User describes what they're trying to communicate. Sensei identifies the right type and explains why.

### Mode detection:

Sensei asks: "Are you building this story yourself, or should I build it for you?"

- "I'm building it" → **Coaching mode** (sensei asks questions, human fills sections)
- "You build it" → **LLM mode** (sensei gathers context, drives section by section)

### After routing:

1. Read the selected type file from `skills/story/types/[N]-[name].md`
2. Ask for **audience** (who is reading this A3?) and **subject** (one sentence: what is this story about?)
3. Create the A3 file at `kivna/output/sensei-[slug]/sensei-[slug].html`
4. Open in browser: `open kivna/output/sensei-[slug]/sensei-[slug].html`

---

## Mode Rules

### Coaching Mode (Human)

- One question at a time per section
- Draw out the human's thinking: "What does the audience already know about this?"
- Challenge weak content: "That's your opinion. What's the fact behind it?"
- Never fill in a section for the human — reflect, compress, confirm
- After each section is confirmed, rewrite the A3 and move to the next section

### LLM Mode

- Sensei gathers context (reads files, asks user for input as needed)
- Drafts each section, presents for confirmation before writing to the A3
- Same compression discipline applies — if a section is too long, sensei rewrites tighter before presenting
- After each section is confirmed, rewrite the A3 and move to the next section

Both modes produce the same artifact. The difference is who generates the content (human vs LLM) and how the sensei interacts (questions vs directives).

---

## Compression Discipline — Rock Solid Enforcement

Applied at every section, both modes. These are Toyota's tests for whether a story is ready.

### Per-section checks:

- **Bullet point cap:** 3-7 bullet points per section. More than 7 triggers pushback: "This won't fit on the A3. What's the one thing this section needs to say?"
- **Handwrite test:** "Could you handwrite this section on an index card? If not, cut."
- **Audience test:** "Does the audience need this detail, or is this for you?"
- **Grandparent test:** "Would someone outside this project follow this section?"

### After all sections complete:

- **Elevator test:** "Can you tell this whole story in 3 minutes?"
  - Coaching mode: Sensei asks the human to walk through it verbally
  - LLM mode: Sensei verifies the full A3 reads coherently in under 3 minutes

If a section fails a check, the sensei pushes back and asks for revision before confirming it. The discipline is the point — compression forces clarity.

---

## Progressive Build

Same mechanics as `/sensei:work`:

1. A3 HTML file created at routing, all sections set to `.locked`
2. After each section is confirmed by the user, the A3 is rewritten:
   - Confirmed section filled in (default styling)
   - Next section set to `.active`
   - Remaining sections stay `.locked`
3. User refreshes browser to see progress
4. Status badge updates: "Draft — Step N of M"

The user watches the story take shape and can interject at any step. This prevents the failure mode where the full A3 is generated at the end and the user discovers a structural problem too late to fix cheaply.

---

## Nemawashi Tracking

After all sections are complete, the sensei runs the nemawashi step.

### Step 1: Identify reviewers

Sensei asks: "Who should review this story before it goes to [audience]?"

Captures reviewer names and adds them to the nemawashi footer on the A3. Each reviewer gets a row: name, status (pending/reviewed/approved), date.

### Step 2: Optional PR creation

Sensei offers: "Would you like me to create a PR for reviewers to comment on? (Optional)"

If yes:
- Commits the A3 HTML to a branch
- Opens a PR with `gh pr create`
- Adds the PR link to the nemawashi section on the A3

If no: the nemawashi checklist on the A3 is the tracking mechanism. The user manages reviews outside the tool.

### Rock Solid self-check

The A3 footer includes 4 checkboxes:
1. Could I handwrite this on one page?
2. Does the audience know why they're reading this?
3. Would someone with no context follow it?
4. Can I tell this story in 3 minutes?

These are for the author's own use — a final self-check before sharing.

---

## Shared Story Template

One HTML template (`skills/shared/a3-story-template.html`) serves all 7 story types. The skill populates it based on the type definition.

### Template structure:

**Header:**
- Title (the story subject)
- Story type badge (e.g., "Standard Toyota Proposal")
- Owner, date, status badge ("Draft — Step N of M")

**Audience banner:**
- Who is reading this A3
- Story type badge

**Body — two columns, always:**
- Left column heading (set per type, e.g., "Context", "Overview", "Current")
- Right column heading (set per type, e.g., "Proposal", "Detail", "New")
- Sections within each column (configured per type)
- Each section has states: `.active`, `.locked`, or completed (default)
- Evidence/illustration blocks use `<pre class="evidence">` styling for charts, tables, diagrams

**Footer:**
- Nemawashi checklist (reviewer name, status, date)
- Optional PR link
- Rock Solid self-check (4 checkboxes)

### Template tokens:

The skill replaces these when generating the A3:
- `{{TITLE}}` — the story subject
- `{{STORY_TYPE}}` — full type name
- `{{STORY_TYPE_BADGE}}` — short label for header badge
- `{{AUDIENCE}}` — who is reading
- `{{OWNER}}` — author name
- `{{DATE}}` — creation date
- `{{STATUS}}` — lifecycle status
- `{{LEFT_HEADING}}` / `{{RIGHT_HEADING}}` — column headings
- `{{LEFT_SECTIONS}}` / `{{RIGHT_SECTIONS}}` — section HTML
- `{{NEMAWASHI}}` — reviewer rows
- `{{PR_LINK}}` — optional PR URL

---

## Story Type Definition File Structure

Each file in `skills/story/types/` follows this format:

```markdown
# Type [N]: [Name]

## When to Use
One paragraph describing when this story type applies.

## Column Mapping
- Left column heading: [name]
- Left sections: [ordered list]
- Right column heading: [name]
- Right sections: [ordered list]

## Section Definitions

### [Section Name]
**Purpose:** One sentence.
**Content:** What belongs in this section.
**Compression test:** The specific Rock Solid check.
**Coaching prompts:** Questions the sensei asks in coaching mode.
**LLM directives:** Rules for LLM mode.

[Repeat for each section]

## Example
One concrete example showing what good looks like — the full A3 content for a realistic scenario.
```

---

## Knowledge Base Changes

### Rename

`docs/tps-knowledge-base.md` → `docs/sensei-knowledge-base.md`

All skills that read the KB (`work`, `coach`, `learn`, `review`, `story`) update their read paths.

### New section: A3 as Communication Tool

Add to the KB covering:
- The 7 story types (summary with one-line descriptions — full definitions live in the type files)
- The 5-step story creation process (select type, fill boxes, Rock Solid tests, illustrate, nemawashi)
- The Rock Solid principles (handwrite test, audience test, grandparent test, elevator ride)
- Why A3 is one page: compression forces clarity, the constraint is the feature

### Expand nemawashi entry

Replace the one-line vocabulary entry with the 8-component operational method:
- Relationships (1-4): Be Personable, Build Partnerships, Be Proactive, Build Pyramid
- Communication (5-8): Be Provider, Begin with Peers, Break for Preview, Bare Prospects

This enrichment benefits all skills, not just `/sensei:story`.

---

## Modified Files

| File | Change |
|------|--------|
| `docs/tps-knowledge-base.md` | Rename to `docs/sensei-knowledge-base.md`, add A3 communication section, expand nemawashi |
| `.claude-plugin/plugin.json` | Add `/sensei:story` to description, version bump to 1.4.0 |
| `skills/work/SKILL.md` | Update KB read path |
| `skills/coach/SKILL.md` | Update KB read path |
| `skills/learn/SKILL.md` | Update KB read path |
| `skills/review/SKILL.md` | Update KB read path |

---

## Output Structure

At runtime, story A3s are written to:

```
kivna/output/sensei-[slug]/
  sensei-[slug].html          — the story A3
```

No evidence directory for stories. Unlike problem-solving, story content comes from the user's knowledge, not from measured evidence.

---

## What This Does Not Include

- No changes to `/sensei:work`, `/sensei:coach`, `/sensei:learn`, or `/sensei:review` beyond the KB path update
- No new learning paths for `/sensei:learn` (could be added later, referencing the type files)
- No automatic GitHub Pages deployment
- No PDF export
- SLII leadership model from the pocketmod is not included (Platt's team tool, not relevant here)
