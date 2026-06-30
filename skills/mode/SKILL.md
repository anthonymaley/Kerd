---
name: mode
description: "Use when the user says 'mode', 'greenfield', 'jit', 'quickfix', 'maintain', 'strategy', 'writing', 'research', 'legal', 'sales', or wants to start a guided workflow for a specific type of work. Orchestrates skills from Kerd, Superpowers, and other plugins into customizable session flows."
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
    deepwork      Focused session on existing feature, conductor-driven
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

Parse `core_skills` from the mode's frontmatter. For each skill, check if the plugin is installed by scanning `~/.claude/plugins/cache/` for a matching plugin and skill name. The skill reference format is `plugin:skill-name` (e.g., `superpowers:writing-plans`, `superpowers:brainstorming`, `kerd:switch`).

For Kerd skills, they are always available (same plugin). For external skills, check the cache directory.

Report status:

```
Core skills:
  ✓ superpowers:writing-plans
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

Write the active mode to `kivna/.active-modes` using the structured steps format. Each enabled step gets a line with its stable id, concrete skill invocation (with args resolved), label, and status marker.

```
mode: greenfield (step 1 of 9)
  instruction: focus on pricing strategy only
  steps:
    1: /kerd:switch in | open session, set context [current]
    2: /superpowers:brainstorming | explore the problem space [pending]
    3: /superpowers:writing-plans | produce the implementation plan [pending]
    4: /superpowers:executing-plans 1 | build phase 1 against the plan [pending]
    5: /superpowers:test-driven-development 1 | TDD phase 1 behavior [pending]
    6: /superpowers:verification-before-completion 1 | verify phase 1 [pending]
    7: /superpowers:requesting-code-review 1 | review phase 1 [pending]
    8: /kerd:slainte | run health checks [pending]
    9: /kerd:switch out | close session [pending]
```

Step format: `<id>: <skill> [<args>] | <label> [<status>]`
Status markers: `[done]`, `[current]`, `[pending]`, `[skipped]`

If no session instruction was given, omit the instruction line. Never touch other skills' lines in this file.

**Expanding repeated phases:** When a mode has "repeat per phase" steps (like greenfield's Build phase), expand them into concrete steps with phase numbers at flow setup time. If the phase breakdown isn't known yet (e.g., `/superpowers:writing-plans` hasn't run), create placeholder steps for one iteration and note that the list will expand after the plan is written.

After each step is completed (user confirms it's done, or the invoked skill completes), update the tracker: mark the completed step as `[done]`, advance `[current]` to the next pending step.

Remind the user what's next, and resurface the session instruction if one was set:

```
✓ Step 3 complete: /superpowers:writing-plans
  Instruction: focus on pricing strategy only
  Next: step 4 — /superpowers:executing-plans 1 (build phase 1 against the plan)
```

If the user goes off-script (does something not in the flow), don't block them. When they come back, show where they are in the flow and what remains.

### 6. Complete

When all enabled steps are done (or the user says "done"), remove the mode block from `.active-modes` (don't just clear it, remove all mode lines) and confirm:

```
Mode complete: greenfield (9/9 steps)
```

## Resume and Recovery

If a mode was active but context may have been lost (long session, context compaction, or new conversation picking up mid-flow), recover before continuing:

1. **Read `.active-modes`.** Check if a mode block exists with steps and status markers. This is the source of truth for mode state.
2. **Verify coherence.** Does the `[current]` step make sense given what's in TODO.md and recent session logs? If the current step references a skill that was already completed (visible in git log or session log), the state is stale.
3. **If stale:** Show the user the recovered state and what looks wrong. Ask: "Resume from step N, or recount progress?" If recounting, walk through each step and check git/session evidence for completion. Update status markers accordingly.
4. **If coherent:** Show a brief status line and continue: "Resuming mode: greenfield (step 4 of 9). Instruction: focus on pricing strategy only."

Do not silently continue with a stale step. Do not restart the mode from scratch unless the user asks.

## Notes

- Modes are session configurations, not automations. They guide, they don't drive.
- The flow is a recommendation. Users can skip steps, go out of order, or bail early.
- Mode files live in `modes/` at the repo root. One file per mode.
- Community contributions: PR a single `.md` file to `modes/` to add a mode.
- Modes don't replace conductor. Conductor is session discipline within a mode. A mode can include conductor as a step.
- The mode skill reads from the `modes/` directory relative to the plugin root, not the current working directory. This means the modes ship with the plugin.
