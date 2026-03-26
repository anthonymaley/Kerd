# Kerd

"Ceird" means skill in Gaelic. Respelled.

Nine workflow skills plus community-contributed modes for Claude Code. Skills handle the operational side of working across sessions and machines: when to pull, what to commit, where to put notes, how to audit for drift, how to maintain structural health. Modes orchestrate skills from Kerd, GSD, Superpowers, and other plugins into guided flows for different types of work. They keep the plumbing clean so you can focus on the work.

## Install

```
claude plugins add-marketplace anthonymaley/Kerd
claude plugins install kerd
```

## Skills

### dian (Session Discipline)

Dian gives a session structure. You start it when you sit down to work, and it walks through four phases: orient (read the project state, cross-check for inconsistencies), plan (propose what to do, ask questions, push back on ambiguity), execute (do the work, verify each task, record decisions immediately), close out (diff review, update docs, update the playbook, run checks, clear the session block). It writes the session plan to TODO.md and keeps you honest about scope creep. If something comes up that isn't in the plan, it goes on the list for later.

On close-out, dian creates or updates `docs/playbook.md`, a living guide for rebuilding the project from scratch. Tech stack, setup steps, architecture decisions, integrations, gotchas, current status. It grows with the project, session by session.

During execution, decisions and progress accumulate in repo-side files (session logs, TODO.md). On close-out, dian calls `/kivna save` once, updating the vault's Status.md and proposing updates to any other vault files where new knowledge belongs. One clean vault update per session, not ten incremental dumps.

Dian announces its current phase with a mode marker (`[dian: orient]`, `[dian: execute]`, etc.) so you always know what's active. When the session closes, it outputs `[dian: closed]` so there's no ambiguity.

Dian doesn't touch git. No pulls, no pushes. That's switch's job.

```
/dian
```

### switch (Machine Handoff)

Switch owns git boundary operations. All of them. When you leave a machine, it reflects on the session (capturing learnings to CLAUDE.md and memory files), writes session state to TODO.md, creates a session log in `kivna/sessions/`, commits everything, and pushes. When you arrive on a new machine, it pulls, runs a smoke test if tests exist, reads the session logs, and tells you where you left off. It also reads vault Status.md (where the project stands and what's next) and reports any active modes left from a previous session.

If you run it without arguments, it checks for uncommitted changes. Changes present means you're leaving. Clean repo means you're arriving. Add `light` to skip vault operations, reflection, and smoke tests for a faster handoff with lower token cost.

```
/switch out          # full wrap-up (vault, reflection, commit, push)
/switch out light    # quick wrap-up (TODO + session log, commit, push)
/switch in           # full pickup (pull, vault, smoke test, session logs)
/switch in light     # quick pickup (pull, TODO, session log)
```

### kivna (Knowledge Management)

Kivna owns the project's knowledge layer, stored in an Obsidian vault at `~/eolas/vault/[project]/`. The vault is a human knowledge base. Every file answers a question someone would actually ask. No symlinks, no append-only logs, no session dumps. Files are living, updated in place with approval.

Save (`/kivna save`) updates the vault's Status.md, updates the Weekly tracker (achievements and risks by week for quick status report generation), and proposes updates to other vault files (Architecture Decisions, Playbook, etc.), each change shown and approved before writing. This is the same save mechanic dian and switch use at session boundaries. Scaffold (`/kivna scaffold`) creates the vault folder with a MOC and Status.md, then suggests what other files might fit the project. Import (`/kivna in`) reads files from `kivna/input/` and integrates relevant knowledge. Export (`/kivna out`) packages your session for another LLM.

The folder structure:

```
kivna/
  vault.json   # vault config (points to ~/eolas/vault/[project]/)
  sessions/    # session logs from switch (committed)
  input/       # drop files here for import (gitignored)
  output/      # exports land here (gitignored)
```

```
/kivna in                                          # import from inbox
/kivna out                                         # export session context
/kivna save                                        # update vault
/kivna scaffold                                    # set up Obsidian vault
```

### slainte (Project Health)

Slainte audits project health across five areas: docs, code, site, deps, and playbook. It reads a `.slainte` config file at the project root to know what to check. Each area has specific checks. Docs gets cross-referenced against CLAUDE.md, scanned for stale names and broken links. Code runs tests and the build. Deps checks for outdated packages and security issues. Playbook checks whether `docs/playbook.md` exists, whether its Current Status is accurate, whether the tech stack listed still matches reality, and whether setup steps still point to files that exist.

Everything gets a severity grade: high (factually wrong, broken build, security vulnerability), medium (stale but not misleading), low (nitpick). Slainte reports problems. It doesn't fix them.

```
/slainte              # show current config
/slainte add docs README.md   # register a target
/slainte docs         # audit docs area
/slainte playbook     # audit the playbook
/slainte all          # audit everything
```

### skriv (Writing Voice)

Skriv enforces a human writing voice. It has a kill list of words no one actually uses in conversation (leverage, facilitate, delve, holistic, the whole lot), bans all dashes as punctuation (em, en, and double hyphens) along with five-paragraph essay structure, and cuts 20% after drafting. The goal is prose that reads like a first draft by someone who's been in the room, not something generated.

Three modes. Audit reviews a file and reports violations with line numbers. Fix rewrites the file in place. Session mode applies the rules to everything you write for the rest of the conversation. When session mode is on, skriv shows `[skriv: active]` at the top of responses and `[skriv: off]` when it ends.

```
/skriv README.md       # audit against the rules
/skriv fix README.md   # rewrite applying the rules
/skriv on              # session mode on
```

### tend (Structural Health)

Tend audits repo infrastructure against current Kerd conventions and fixes what's drifted. Run it on a new repo to set up everything from scratch, or on an existing repo to catch drift after a Kerd update. It checks seven categories: directory structure, required files, vault integration, deprecated patterns, naming consistency, stray/stale files, and .gitignore hygiene.

The report shows each category as passing (✓), failing (✗), or warning (⚠). Failing and warning items get a current-vs-proposed table with reasons. After the report, choose to fix all, pick individually, or skip. Tend makes changes but never commits. Switch owns that boundary.

```
/tend
```

### lorg (Skill Gap Analysis)

Lorg scans the current project and recommends skills or plugins you should be using but aren't. It works in three tiers. Tier 1 checks what's already installed but not activated in this project, skills gathering dust that match your stack. Tier 2 searches the Claude Code marketplace and a curated list of repos you maintain for plugins that fit your project's tech and themes. Tier 3 goes wider: GitHub and web search for trending or new plugins you haven't heard of yet.

The recommendations aren't just based on file types. Lorg reads your README, playbook, TODO, session logs, and vault decisions to extract work themes (fundraising, compliance, content creation, whatever keeps coming up). Each result shows a rich card with what the skill does, why it fits here, and an action prompt (try it, install it, or explore it).

Each scan writes the full report to `docs/lorg-report.md` (committed, available on any machine) and to the Obsidian vault (searchable alongside other project files). Both get overwritten on the next run. Use `/lorg report` to view the last saved report without rescanning.

The curated source list lives in your Obsidian vault at `discover-sources.json`, synced between machines automatically.

```
/lorg                # full scan across all tiers
/lorg report         # show last saved report
```

### trim (Token Optimization)

Trim keeps active context lean. Run it after every feature ships. It archives completed spec and plan docs, prunes stale CLAUDE.md guidance blocks, cleans up project memory entries that are no longer actionable, and removes checked-off TODO items. A safety gate (haiku subagent) verifies that `/switch in` would still have all the context it needs before anything is finalized.

```
/trim
```

### mode (Workflow Routing)

Mode routes you to the right tools for the type of work you're doing. Each mode is a session configuration: it checks which skills are installed, auto-discovers extras from your plugins, and presents a customizable checklist flow. An interactive TUI picker lets you toggle steps on/off with the spacebar before starting, with a text fallback for non-interactive terminals. The mode then tracks your progress through the session.

Modes orchestrate across toolkits. A greenfield mode sequences GSD for spec-driven building, Superpowers for TDD and code review, and Kerd for session boundaries. A strategy mode loads skriv for writing voice and brainstorming for exploration. Modes don't call skills directly. They guide you through the flow and remind you what's next.

Nine starter modes ship with Kerd. Community members can contribute new modes by PRing a single markdown file to the `modes/` directory.

| Category | Modes |
|----------|-------|
| Development | `greenfield`, `quickfix`, `deepwork`, `maintain` |
| Business | `strategy`, `writing`, `research` |
| Operations | `legal`, `sales` |

```
/mode                # list all modes by category
/mode greenfield     # start the greenfield flow
/mode maintain       # start the maintenance flow
```

## How They Fit Together

**Starting a project:** Create a repo, clone it, run `/tend`. It checks what's missing, shows you the plan, and sets up the full structure with your approval. Run `/lorg` to find plugins that fit your stack. Then `/dian` to start your first session.

**Picking a workflow:** Before diving in, run `/mode` to see what's available. If you're building something new, `/mode greenfield` sequences you through spec writing, planning, execution, and review. Fixing a bug? `/mode quickfix` strips the ceremony down to the essentials. Writing a blog post or strategy doc? `/mode writing` or `/mode strategy` loads the right tools (skriv for voice, brainstorming for exploration). The mode presents a checklist you can customize, then tracks your progress through the session.

**Day to day:** You sit down at your laptop and run `/switch in`. It pulls, reads the session logs, tells you what happened last time. It reads vault Status.md (where the project stands and what's next) plus any other vault files relevant to the work. If a mode was active when you left, switch tells you where you were in the flow. Then it offers to start a dian session. You run `/dian` to plan the session. Work happens, decisions get recorded in session logs and TODO.md. When the work is done, dian's close-out updates the playbook and calls `/kivna save` to update the vault, one clean write with approval. You run `/slainte docs` to check nothing drifted. Then `/switch out` commits, pushes, and writes the session log. Tomorrow, different machine, same state. Periodically run `/lorg` to check if new skills have emerged that would help with the project.

**Quick sessions:** Use the `light` modifier when token cost matters. `/switch in light` skips vault reads and smoke tests, `/switch out light` skips vault saves and reflection. You still get TODO.md, session logs, and git operations. Full context when you need it, lightweight handoff when you don't.

**The layers:** Switch owns git boundaries. Dian owns session discipline. Kivna owns the knowledge vault. Mode sits above all of them, routing you to the right combination based on what you're doing. You can use any skill standalone, but mode ties them into a coherent flow.

## Naming

Gaelic-inspired where it adds character:
- **Kerd**: skill (ceird)
- **Kivna**: memory (cuimhne)
- **Dian**: intense, rigorous
- **Skriv**: the act of writing (scríobh)
- **Switch**: machine handoff
- **Slainte**: health (slàinte)
- **Tend**: from English "to tend" (care for, maintain)
- **Lorg**: to seek, track down

## License

MIT
