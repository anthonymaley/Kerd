---
name: discover
description: "Use when the user says 'discover', 'find skills', 'what plugins', 'skill gap', 'what am I missing', 'new skills', 'explore plugins', or wants to find skills and plugins that would help with the current project. Searches installed plugins, marketplace, curated sources, and the web."
---

# Discover — Skill Gap Analysis

Scans the current project and recommends skills or plugins you should be using but aren't. Three tiers of widening search radius, all informed by the same project signals.

Not a health check. Not about what's broken or unused elsewhere. Purely about finding opportunities for THIS project.

## Usage

`/kerd:discover` — run in the root of a git repo

## Boundary with Other Skills

- **discover** — skill/plugin opportunities (what tools would help this project)
- **tend** — structural health (dirs, vault, config, naming)
- **sotu** — content health (doc accuracy, staleness)

## The Process

### 1. Build project profile

Read the project to understand what it needs. Two layers of signals:

#### Layer 1: Tech signals — file-based, mechanical

Scan for these files and extract language, framework, deployment, and CI information:

- `package.json` — Node/JS/TS ecosystem, frameworks (Next.js, React, Vue), scripts
- `pyproject.toml`, `requirements.txt` — Python ecosystem
- `Cargo.toml` — Rust
- `go.mod` — Go
- `Dockerfile`, `docker-compose.yml` — containerized deployment
- `vercel.json`, `netlify.toml` — deployment targets
- `.github/workflows/`, `.gitlab-ci.yml` — CI/CD pipeline
- `.env.example` — environment variables, external services
- `Makefile` — build automation
- Dominant file extensions — scan for `.tsx`, `.py`, `.go`, `.rs`, etc.

#### Layer 2: Work signals — theme extraction from prose

Read these files if they exist and extract keywords and themes (not categories — a project can be "startup + legal + content" all at once). Skip any that don't exist — a missing file is not an error, just fewer signals:

- `README.md` — project description, what it's for
- `docs/playbook.md` — integrations, architecture intent
- `TODO.md` — active work and backlog themes
- Vault `[Name] Status.md` — where the project stands, what's open, what's next
- Vault MOC (`[Name].md`) — discover other vault files (Architecture Decisions, Playbook, etc.) and scan any that exist for themes
- `kivna/sessions/` — last 3-5 session logs, recurring task patterns

Discover the vault path using `kivna/vault.json` (read `vault`, `folder`, `name` fields, expand `~`).

From these docs, extract recurring themes as keywords. Examples: "fundraising", "pitch deck", "compliance", "content writing", "SEO", "API integration", "testing", "deployment". These keywords drive search alongside tech signals.

#### Display the profile

Show the project profile at the top of the report:

```
Project profile:
  Tech: [languages, frameworks, deployment targets]
  Themes: [extracted keywords from work signals]
```

### 2. Tier 1 — Installed but not activated here

Scan installed plugins and skills:

1. Read `~/.claude/plugins/` to find all installed plugins. If the directory does not exist or is empty, skip Tier 1 and note: "No installed plugins found. Tier 1 skipped."
2. For each plugin, read its skills (check `skills/` subdirectories for SKILL.md files, or read the plugin's manifest)
3. Match each skill's description and capabilities against the project profile
4. Filter to skills that are relevant to this project but have not been invoked here — check `kivna/sessions/` and git history for `/[plugin:skill-name]` invocations. If the skill has been invoked in this project, exclude it. If no invocation is found, include it as a recommendation.
5. For each match, read the skill's SKILL.md to get a proper description

Report matches as rich cards:

```
┌─────────────────────────────────────────────────┐
│ [plugin:skill-name]                             │
│                                                 │
│ [Description from SKILL.md — what it does,      │
│ 2-3 lines max]                                  │
│                                                 │
│ Why here: [specific match to project signals]   │
│                                                 │
│ Already installed — try: /[plugin:skill-name]   │
└─────────────────────────────────────────────────┘
```

### 3. Tier 2 — Available but not installed

Search two sources:

**Source A: Claude Code marketplace**

Search for Claude Code plugins matching the project profile. Use web search to find plugins on the Claude Code marketplace or plugin directories. Search with terms combining the project's tech stack and themes with "Claude Code plugin" or "Claude Code skill." Filter out anything already installed.

**Source B: Curated repo list**

1. Discover vault path via `kivna/vault.json`
2. Read `~/Obsidian/[folder]/discover-sources.json`
3. For each repo in the `repos` list, fetch the repo's README (via GitHub API or web fetch) to understand what skills it offers
4. Match against the project profile
5. Filter out anything already installed

If `discover-sources.json` doesn't exist, skip Source B and note: "No curated sources found. Create `discover-sources.json` in your vault to add trusted repos."

Format:

```json
{
  "repos": [
    "owner/repo-name",
    "another-owner/another-repo"
  ],
  "urls": [
    "https://github.com/topics/claude-code-plugin"
  ]
}
```

Report matches as rich cards:

```
┌─────────────────────────────────────────────────┐
│ [Plugin/Skill Name]                             │
│ [github.com/owner/repo or marketplace link]     │
│                                                 │
│ [Description — what it does, 2-3 lines]         │
│                                                 │
│ Why here: [specific match to project signals]   │
│                                                 │
│ Install: claude plugin add [owner/repo]         │
└─────────────────────────────────────────────────┘
```

### 4. Tier 3 — Explore the unknown

Search beyond known sources:

**GitHub search:** Search GitHub for repositories related to Claude Code plugins/skills that match the project's tech stack and work themes. Look for repos with recent activity, stars, and relevant keywords.

**Web search:** Search for trending Claude Code plugins, community recommendations, blog posts about new plugins. Use the project's themes as search terms alongside "Claude Code plugin" or "Claude Code skill."

Also fetch any URLs listed in `discover-sources.json` `urls` array and scan them for plugin/skill references.

Filter out anything already surfaced in Tiers 1 and 2.

Report matches as rich cards:

```
┌─────────────────────────────────────────────────┐
│ [Name]                                          │
│ [github.com/owner/repo] ⭐ [stars] · [activity] │
│                                                 │
│ [Description — what it does, 2-3 lines]         │
│                                                 │
│ Why here: [specific match to project signals    │
│ or themes]                                      │
│                                                 │
│ Explore: [full URL]                             │
└─────────────────────────────────────────────────┘
```

### 5. Display report

Combine all tiers into a single report:

```
┌─────────────────────────────────────────────────┐
│  /kerd:discover — [project-name]                │
└─────────────────────────────────────────────────┘

Project profile:
  Tech: [languages, frameworks, deployment]
  Themes: [extracted work themes]

━━━ Tier 1: Installed but not activated here ━━━━

[rich cards or "No matches — you're using everything relevant."]

━━━ Tier 2: Available but not installed ━━━━━━━━━

[rich cards or "No matches found in marketplace or curated sources."]

━━━ Tier 3: Worth exploring ━━━━━━━━━━━━━━━━━━━━

[rich cards or "No new discoveries this scan."]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 N installed matches · N available · N to explore
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 6. Post-report walkthrough

After the report, walk through each item individually. Different actions per tier:

- **Tier 1:** "Want me to show how to use [skill] in this project?"
- **Tier 2:** "Install [plugin]?" — on approval, run the install command
- **Tier 3:** "Want me to fetch the README for [repo] so you can see more?"

No batch actions across tiers — different trust levels require different handling.

If the user says "skip" or "done" at any point, stop the walkthrough.

## Curated Sources

The curated source list lives in the Obsidian vault, synced between machines:

**Location:** `~/Obsidian/[folder]/discover-sources.json` (resolved via vault discovery from `kivna/vault.json`)

**Format:**

```json
{
  "repos": [
    "owner/repo-name"
  ],
  "urls": [
    "https://example.com/plugins-list"
  ]
}
```

- `repos` — GitHub repos to check for Claude Code plugins/skills
- `urls` — web pages to scan for plugin references and recommendations

To add a source: edit the file directly or ask discover to add one.

## What Discover Does NOT Do

- **No auto-install.** Every install is prompted and approved individually.
- **No removal suggestions.** A skill unused in this project may be critical in another. Discover finds gaps, not waste.
- **No health checks.** That's tend's job (structure) or sotu's job (content).
- **No caching of results.** Fresh scan every run — the ecosystem and your project both change.
- **No rating or ranking.** Presents what it finds with context. You decide what's valuable.

## Notes

- The project profile is computed fresh each run. Not stored. Projects evolve; stale profiles would mislead.
- Layer 2 (work signals) is what makes discover genuinely useful beyond simple file-extension matching. It catches non-technical skill gaps like "you keep writing investor updates."
- If no vault is found, Tiers 1 and 3 still work. Tier 2's curated sources are skipped with a note suggesting vault setup.
- Discover is read-only except when the user approves a Tier 2 install. It never modifies project files.
