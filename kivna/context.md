# Context — Kerd

## Current Focus
Session complete. Tested startup and dian playbook creation — both pass. v0.3.1 with Insights section in switch template. Backlog: sotu playbook audit test, version bump automation, third-person descriptions.

## Mental Model
Kerd is a Claude Code plugin with six skills defined in markdown (SKILL.md). Each skill has a thin command wrapper in commands/. The plugin is pure markdown + JSON — no build step, no dependencies.

The information flow has three layers:
1. **Stable docs** — CLAUDE.md (conventions), playbook (architecture), README (user-facing). Updated on close-out.
2. **Living context** — `kivna/context.md`. Updated at task boundaries. Captures the thinking: decisions, reasoning, rejected approaches, assumptions.
3. **Historical record** — session logs (`kivna/sessions/`), checkpoint archives (`kivna/checkpoints/`), memories (`kivna/memories/`). Append-only.

Cold start reads: CLAUDE.md + playbook + context.md. Three files, fully caught up.

## Decisions
- **context.md is cumulative, not incremental** — each checkpoint captures the full working state.
- **Rolling file + daily archive** — context.md overwritten each checkpoint, previous version appended to checkpoints/YYYY-MM-DD.md.
- **Context save triggers: auto at dian task boundaries + manual /kivna save**
- **Switch in offers dian (ask first, don't auto-start)**
- **No sidebar skill** — deferred. Context checkpointing reduces the need.
- **Subagents must not expand command files** — commands stay thin wrappers.
- **Resume IDs not worth tracking in switch** — they're local to one machine, and switch is for cross-machine handoff.
- **Anthropic plugin-dev review: no urgent changes** — skills are lean (<1,000 words), trigger well. Third-person descriptions worth adopting opportunistically. Progressive disclosure (references/ dirs) not needed until skills cross ~2,000 words.

## Rejected Approaches
- **Detecting context limits automatically** — not possible from inside the conversation.
- **Sidebar skill** — single-turn subagent works but multi-turn can't be isolated.
- **Recording --resume IDs in switch** — local to one machine, defeats the purpose of cross-machine handoff.

## Working Assumptions
- Plugin system loads skills from SKILL.md with YAML frontmatter (name, description).
- Commands are thin markdown wrappers. One-to-one mapping with skills.
- Version synced in three places: plugin.json, marketplace.json metadata.version, marketplace.json plugins[0].version.
- No test suite — pure markdown. Verification is reading files and checking consistency.

## Active Threads
- Sotu playbook audit still untested on a project with a real playbook (not blocking)
- Version bump automation question open (switch-out vs release skill)

## Open Questions
- Should version bumping be part of switch-out or a separate release skill?
