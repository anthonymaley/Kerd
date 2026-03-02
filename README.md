# Kerd

"Ceird" means skill in Gaelic. Respelled.

Six workflow skills for Claude Code. They handle the operational side of working across sessions and machines: when to pull, what to commit, where to put notes, how to audit for drift, how to scaffold a new project. They don't generate code or make architectural decisions. They keep the plumbing clean so you can focus on the work.

## Install

```
claude plugins add-marketplace anthonymaley/Kerd
claude plugins install kerd
```

## Skills

### dian — Session Discipline

Dian gives a session structure. You start it when you sit down to work, and it walks through four phases: orient (read the project state, including the playbook), plan (propose what to do), execute (do the work), close out (update docs, update the playbook, run checks, clear the session block). It writes the session plan to TODO.md and keeps you honest about scope creep. If something comes up that isn't in the plan, it goes on the list for later.

On close-out, dian creates or updates `docs/playbook.md` — a living guide for rebuilding the project from scratch. Tech stack, setup steps, architecture decisions, integrations, gotchas, current status. It grows with the project, session by session.

Dian doesn't touch git. No pulls, no pushes. That's switch's job.

```
/dian
```

### switch — Machine Handoff

Switch owns git boundary operations. All of them. When you leave a machine, it writes session state to TODO.md, creates a session log in `kivna/sessions/`, commits everything, and pushes. When you arrive on a new machine, it pulls, reads the session logs, and tells you where you left off.

If you run it without arguments, it checks for uncommitted changes. Changes present means you're leaving. Clean repo means you're arriving.

```
/switch out    # leaving this machine
/switch in     # arriving on a new machine
```

### kivna — Knowledge Management

Kivna owns the project's knowledge layer. It has three modes. Import (`/kivna in`) reads files you drop into `kivna/input/`, extracts what matters, and writes it into the project. Works with PDFs, markdown, JSON session exports, plain text. Export (`/kivna out`) packages your current session into a portable markdown file another LLM can pick up cold. Quick save (`/kivna memory`) appends a timestamped note to `kivna/memories/` without ceremony.

The folder structure:

```
kivna/
  sessions/    # session logs from switch (committed)
  memories/    # quick notes (committed)
  input/       # drop files here for import (gitignored)
  output/      # exports land here (gitignored)
```

```
/kivna in                                          # import from inbox
/kivna out                                         # export session context
/kivna memory decided to use Postgres over SQLite  # quick note
```

### sotu — Project Health Audit

Sotu audits project health across five areas: docs, code, site, deps, and playbook. It reads a `.sotu` config file at the project root to know what to check. Each area has specific checks. Docs gets cross-referenced against CLAUDE.md, scanned for stale names and broken links. Code runs tests and the build. Deps checks for outdated packages and security issues. Playbook checks whether `docs/playbook.md` exists, whether its Current Status is accurate, whether the tech stack listed still matches reality, and whether setup steps still point to files that exist.

Everything gets a severity grade: high (factually wrong, broken build, security vulnerability), medium (stale but not misleading), low (nitpick). Sotu reports problems. It doesn't fix them.

```
/sotu              # show current config
/sotu add docs README.md   # register a target
/sotu docs         # audit docs area
/sotu playbook     # audit the playbook
/sotu all          # audit everything
```

### skriv — Writing Voice

Skriv enforces a human writing voice. It has a kill list of words no one actually uses in conversation (leverage, facilitate, delve, holistic, the whole lot), bans em dashes and five-paragraph essay structure, and cuts 20% after drafting. The goal is prose that reads like a first draft by someone who's been in the room, not something generated.

Three modes. Audit reviews a file and reports violations with line numbers. Fix rewrites the file in place. Session mode applies the rules to everything you write for the rest of the conversation.

```
/skriv README.md       # audit against the rules
/skriv fix README.md   # rewrite applying the rules
/skriv on              # session mode on
```

### startup — Project Scaffold

Startup is a one-time setup for new projects. Point it at a fresh git repo and it creates the Kerd directory structure: `kivna/sessions/`, `docs/`, and all the initial files — README.md, TODO.md, CLAUDE.md with session workflow conventions, `docs/playbook.md` skeleton, and a `.sotu` config. One commit, one push, ready to go.

It won't overwrite files that already exist. If you created a README during repo init, startup skips it and moves on.

```
/startup
```

## How They Fit Together

New project: you create a repo, clone it, run `/startup`. It scaffolds everything. Then `/dian` to start your first session.

Day to day: you sit down at your laptop and run `/switch in`. It pulls, reads the session logs, tells you what happened last time. You run `/dian` to plan the session. Mid-work, you make a decision worth remembering, so you run `/kivna memory switching to Redis for the cache layer`. When the work is done, dian's close-out updates the playbook with anything new you learned. You run `/sotu docs` to check nothing drifted. Then `/switch out` commits, pushes, and writes the session log. Tomorrow, different machine, same state. The playbook grows with every session — if someone else picks up the project, they can rebuild it from that doc alone.

## Naming

Gaelic-inspired where it adds character:
- **Kerd** — skill (ceird)
- **Kivna** — memory (cuimhne)
- **Dian** — intense, rigorous
- **Skriv** — the act of writing (scríobh)
- **Sotu** — state of the union (English acronym)

## License

MIT
