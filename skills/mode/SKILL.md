---
name: mode
description: "Use when the user says 'mode', 'greenfield', 'quickfix', 'maintain', 'strategy', 'writing', 'research', 'legal', 'sales', or wants to start a guided workflow for a specific type of work. Orchestrates skills from Kerd, GSD, Superpowers, and other plugins into customizable session flows."
---

# Mode (Workflow Routing)

Session configurations that prime the right tools for a type of work. Modes don't call other skills directly. They set up the session, present a customizable flow, and guide you through it.

## Usage

`/kerd:mode` list all available modes by category
`/kerd:mode <name>` load and start the named mode

## The Mechanic

### 1. Load

If no argument given, list all modes. Read every `.md` file in the `modes/` directory, parse the YAML frontmatter, and display grouped by category:

```
Available modes:

  Development
    greenfield    Build a new feature from scratch using spec-driven development
    quickfix      Bug fix or small change with minimal ceremony
    deepwork      Focused session on existing feature, dian-driven
    maintain      Health loop: structural, content, skill, and writing audits

  Business
    strategy      Positioning, go-to-market, competitive analysis
    writing       Prose creation: blog posts, docs, investor updates
    research      Investigation, due diligence, market analysis

  Operations
    legal         Contract review, compliance, policy drafting
    sales         Pipeline review, call prep, outreach drafting

Start a mode: /kerd:mode <name>
```

If an argument is given, read `modes/<name>.md`. If the file doesn't exist, say: "Mode '<name>' not found." Then list available modes.

### 2. Check core skills

Parse `core_skills` from the mode's frontmatter. For each skill, check if the plugin is installed by scanning `~/.claude/plugins/cache/` for a matching plugin and skill name. The skill reference format is `plugin:skill-name` (e.g., `gsd:new-project`, `superpowers:brainstorming`, `kerd:switch`).

For Kerd skills, they are always available (same plugin). For external skills, check the cache directory.

Report status:

```
Core skills:
  ✓ gsd:new-project
  ✓ superpowers:brainstorming
  ✓ kerd:switch
  ✗ superpowers:test-driven-development (not installed)
```

Missing core skills are a warning, not a blocker. The mode still runs.

### 3. Auto-discover extras

If the mode has `discover_keywords` in frontmatter, scan installed plugins for skills whose SKILL.md description contains any of the keywords. Exclude skills already in the core list.

Show matches:

```
Discovered extras:
  + superpowers:using-git-worktrees — isolate feature work
  + pr-review-toolkit:review-pr — comprehensive PR review
```

If no extras found, skip this section silently. These are suggestions only, displayed once.

### 4. Present and customize

Parse the mode body by `##` headers. Each header becomes a phase. Each `- [ ]` line under a header becomes a step within that phase. Present the flow phase by phase using `AskUserQuestion` with `multiSelect: true`.

**Phase selection:** For each phase in the mode, create one `AskUserQuestion` question where:
- The `header` is the phase name (e.g., "Setup", "Build", "Close")
- The `question` is "[Mode name]: which [phase] steps?" (e.g., "Greenfield: which Setup steps?")
- Each step becomes an option with `label` as the short step name and `description` as the full step text
- All options are selected by default (the user deselects what they want to skip)

Group up to 4 phases into a single `AskUserQuestion` call (the tool supports 1-4 questions per call). If the mode has more than 4 phases, use multiple calls.

**Constraint:** Each question supports 2-4 options. Mode files should keep phases to 4 steps or fewer. If a community-contributed mode has a phase with more than 4 steps, split it into two questions (e.g., "Build (planning)" and "Build (execution)").

Example for a mode with 4 phases:

```
AskUserQuestion with 4 questions:

  Q1 header:"Setup" question:"Strategy: which Setup steps?"
     [x] "Switch in" — /kerd:switch in to load project context
     [x] "Review status" — Review vault Status.md for current state

  Q2 header:"Define" question:"Strategy: which Define steps?"
     [x] "Brainstorm" — /superpowers:brainstorming to explore the strategic question
     [x] "Scope" — Define scope, constraints, and success criteria

  Q3 header:"Analyze" question:"Strategy: which Analyze steps?"
     [x] "Research" — Research competitors and market landscape
     [x] "Trade-offs" — Evaluate options with explicit trade-offs

  Q4 header:"Capture" question:"Strategy: which Capture steps?"
     [x] "Decisions" — Document decisions and rationale
     [x] "Draft" — Draft positioning or strategy doc with /kerd:skriv on
     [x] "Vault" — /kerd:kivna save to update vault with decisions
     [x] "Switch out" — /kerd:switch out to persist session context
```

The user deselects any steps they want to skip. Steps they leave selected are enabled.

**Session instructions:** After phase selection, ask one more `AskUserQuestion` for session instructions:

```
AskUserQuestion:
  header: "Focus"
  question: "Any instructions for this session?"
  multiSelect: false
  options:
    - label: "Narrow scope"
      description: "Focus on a specific area (e.g., pricing only, one competitor)"
    - label: "Set constraints"
      description: "Exclude something or set boundaries (e.g., skip competitor X, no code changes)"
    - label: "Output preference"
      description: "Request a specific format (e.g., bullet draft first, decision matrix)"
    - label: "No instructions"
      description: "Run the flow as selected"
```

The user can pick one of these or choose "Other" to type freeform instructions. Store the instruction and surface it at the start of each step as a reminder.

**Confirming the flow:** After both selections, display the final flow summary showing enabled steps with phase grouping and any session instruction. Then ask "Ready to start?" before proceeding. This is the last chance to adjust before locking in.

### 5. Track progress

Write the active mode to `kivna/.active-modes`:

```
mode: greenfield (step 1 of 9)
instruction: focus on pricing strategy only
```

If no session instruction was given, omit the instruction line.

After each step is completed (user confirms it's done, or the invoked skill completes), update the tracker:

```
mode: greenfield (step 3 of 9)
instruction: focus on pricing strategy only
```

Remind the user what's next, and resurface the session instruction if one was set:

```
✓ Step 3 complete.
  Instruction: focus on pricing strategy only
  Next: step 4 — /gsd:discuss-phase N (capture decisions)
```

If the user goes off-script (does something not in the flow), don't block them. When they come back, show where they are in the flow and what remains.

### 6. Complete

When all enabled steps are done (or the user says "done"), clear the mode from `.active-modes` and confirm:

```
Mode complete: greenfield (9/9 steps)
```

## Notes

- Modes are session configurations, not automations. They guide, they don't drive.
- The flow is a recommendation. Users can skip steps, go out of order, or bail early.
- Mode files live in `modes/` at the repo root. One file per mode.
- Community contributions: PR a single `.md` file to `modes/` to add a mode.
- Modes don't replace dian. Dian is session discipline within a mode. A mode can include dian as a step.
- The mode skill reads from the `modes/` directory relative to the plugin root, not the current working directory. This means the modes ship with the plugin.
