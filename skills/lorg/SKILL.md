---
name: lorg
description: "Use when the user says 'lorg', 'discover', 'find skills', 'what plugins', 'skill gap', 'what am I missing', 'new skills', 'explore plugins', 'lorg report', 'lorg installed', 'lorg available', 'lorg explore', 'lorg all', 'last scan', or wants to find skills and plugins that would help with the current project. Default scans installed-but-unused skills only (Tier 1). Use subcommands for wider search."
---

# Lorg (Skill Gap Analysis)

**Asking the person:** every question is one speech-bubble line at the end of the message, `> 💬 **The question?**`, with any options, context or proposed answer listed above it, never inside it — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

From Gaelic "lorg" (to seek, track down). Pronounced "LORG".

Scans the current project and recommends skills or plugins you should be using but aren't. Three tiers of widening search radius, all informed by the same project signals. Each tier runs independently with its own freshness tracking.

Not a health check. Not about what's broken or unused elsewhere. Purely about finding opportunities for THIS project.

## Usage

```
/kerd:lorg                → Tier 1 only (installed but unused). Fast, cheap, no web dependency.
/kerd:lorg installed      → Tier 1 (same as default)
/kerd:lorg available      → Tier 2 (marketplace + curated sources)
/kerd:lorg explore        → Tier 3 (GitHub + web search). Opt-in research, most expensive.
/kerd:lorg all            → Full scan across all tiers
/kerd:lorg report         → Display last saved report without rescanning
```

### When to run each tier

- **Tier 1** (`installed` / default): Normal usage. Run anytime. Cheapest, fastest, most actionable.
- **Tier 2** (`available`): Before spending time on workflow or tooling gaps. Run when you suspect something exists but don't know where.
- **Tier 3** (`explore`): Occasional discovery sweep. After a release, or once a month. Most expensive, least reliable.
- **All**: Periodic full audit. Reasonable cadence: monthly or at major milestones.

## Boundary with Other Skills

- **lorg**: skill/plugin opportunities (what tools would help this project)
- **tend**: structural health (dirs, vault, config, naming)
- **slainte**: content health (doc accuracy, staleness)

## Report Subcommand

When invoked as `/kerd:lorg report`:

1. Check if `docs/lorg-report.md` exists. If it does, read and display its contents. Each tier section includes its own `Last scanned: YYYY-MM-DD` date so the user knows how fresh each tier is.
2. If the file doesn't exist, say: "No lorg report found. Run `/kerd:lorg` to scan."
3. Stop. Do not scan, do not modify any files.

## The Process

### 1. Build project profile

Always runs first, regardless of which tier is requested. The profile is computed fresh each run.

#### Layer 1: Tech signals (file-based, mechanical)

Scan for these files and extract language, framework, deployment, and CI information:

- `package.json`: Node/JS/TS ecosystem, frameworks (Next.js, React, Vue), scripts
- `pyproject.toml`, `requirements.txt`: Python ecosystem
- `Cargo.toml`: Rust
- `go.mod`: Go
- `Dockerfile`, `docker-compose.yml`: containerized deployment
- `vercel.json`, `netlify.toml`: deployment targets
- `.github/workflows/`, `.gitlab-ci.yml`: CI/CD pipeline
- `.env.example`: environment variables, external services
- `Makefile`: build automation
- Dominant file extensions: scan for `.tsx`, `.py`, `.go`, `.rs`, etc.

#### Layer 2: Work signals (theme extraction from prose)

Read these files if they exist and extract keywords and themes (not categories, a project can be "startup + legal + content" all at once). Skip any that don't exist. A missing file is not an error, just fewer signals:

- `README.md` for project description, what it's for
- `docs/playbook.md` for integrations, architecture intent
- `TODO.md` for active work and backlog themes
- Vault `[Name] Status.md` for where the project stands, what's open, what's next
- Vault MOC (`[Name].md`) to discover other vault files (Architecture Decisions, Playbook, etc.) and scan any that exist for themes
- `kivna/sessions/` for last 3-5 session logs, recurring task patterns

Resolve the vault path using `kivna/vault.json` (read `vault`, `folder`, `name` fields, expand `~`).

From these docs, extract recurring themes as keywords. Examples: "fundraising", "pitch deck", "compliance", "content writing", "SEO", "API integration", "testing", "deployment". These keywords drive search alongside tech signals.

#### Display the profile

Show the project profile at the top of the report:

```
Project profile:
  Tech: [languages, frameworks, deployment targets]
  Themes: [extracted keywords from work signals]
```

### 2. Tier 1: Installed but not activated here

**Runs on:** `/kerd:lorg`, `/kerd:lorg installed`, `/kerd:lorg all`

Scan installed plugins and skills:

1. Read `~/.claude/plugins/` to find all installed plugins. If the directory does not exist or is empty, skip Tier 1 and note: "No installed plugins found. Tier 1 skipped."
2. For each plugin, read its skills (check `skills/` subdirectories for SKILL.md files, or read the plugin's manifest)
3. Match each skill's description and capabilities against the project profile
4. Filter to skills that are relevant to this project but underused. Check `kivna/sessions/` and git history for `/[plugin:skill-name]` invocations. A skill is included if:
   - It has never been invoked in this project, OR
   - It was last invoked more than 30 days ago (stale usage — the user may have forgotten about it)

   Exclude skills invoked within the last 30 days (actively used, no gap to fill).
5. For each match, read the skill's SKILL.md to get a proper description

Report matches as rich cards:

```
┌─────────────────────────────────────────────────┐
│ [plugin:skill-name]                             │
│                                                 │
│ [Description from SKILL.md: what it does,        │
│ 2-3 lines max]                                  │
│                                                 │
│ Why here: [specific match to project signals]   │
│ Relevance: 65  (theme: 30, tech: 15,            │
│   recency: 20, friction: 0)                     │
│                                                 │
│ Already installed. Try: /[plugin:skill-name]    │
└─────────────────────────────────────────────────┘
```

### 3. Tier 2: Available but not installed

**Runs on:** `/kerd:lorg available`, `/kerd:lorg all`

Search two sources:

**Source A: Claude Code marketplace**

Search for Claude Code plugins matching the project profile. Use web search to find plugins on the Claude Code marketplace or plugin directories. Search with terms combining the project's tech stack and themes with "Claude Code plugin" or "Claude Code skill." Filter out anything already installed.

**Source B: Curated repo list**

1. Discover vault path via `kivna/vault.json`
2. Read `~/eolas/vault/[folder]/discover-sources.json`
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
│ [Description: what it does, 2-3 lines]          │
│                                                 │
│ Why here: [specific match to project signals]   │
│ Relevance: 55  (theme: 20, tech: 30,            │
│   recency: 0, friction: -5)                     │
│                                                 │
│ Install: claude plugin add [owner/repo]         │
└─────────────────────────────────────────────────┘
```

### 4. Tier 3: Explore the unknown

**Runs on:** `/kerd:lorg explore`, `/kerd:lorg all`

Search beyond known sources:

**GitHub search:** Search GitHub for repositories related to Claude Code plugins/skills that match the project's tech stack and work themes. Look for repos with recent activity, stars, and relevant keywords.

**Web search:** Search for trending Claude Code plugins, community recommendations, blog posts about new plugins. Use the project's themes as search terms alongside "Claude Code plugin" or "Claude Code skill."

Also fetch any URLs listed in `discover-sources.json` `urls` array and scan them for plugin/skill references.

Filter out anything already surfaced in Tiers 1 and 2 (check both current scan results and any preserved results from the report file).

Report matches as rich cards:

```
┌─────────────────────────────────────────────────┐
│ [Name]                                          │
│ [github.com/owner/repo] ⭐ [stars] · [activity] │
│                                                 │
│ [Description: what it does, 2-3 lines]          │
│                                                 │
│ Why here: [specific match to project signals    │
│ or themes]                                      │
│ Relevance: 35  (theme: 20, tech: 15,            │
│   recency: 0, friction: -10)                    │
│                                                 │
│ Explore: [full URL]                             │
└─────────────────────────────────────────────────┘
```

### 5. Score and rank results

Score each result before display. Higher scores appear first within each tier.

**Scoring formula:** `relevance = theme_match + tech_match + recency_boost - friction`

| Factor | Range | How to compute |
|--------|-------|----------------|
| `theme_match` | 0-40 | Count keywords from Layer 2 (work signals) that appear in the skill's description or README. 10 points per keyword, cap at 40. |
| `tech_match` | 0-30 | Direct tech stack match (same language, framework, or deployment target). 15 per match, cap at 30. |
| `recency_boost` | 0-20 | Does the project's TODO.md or recent session logs mention a need this skill fills? 20 if yes, 0 if no. |
| `friction` | 0-15 | Install friction. 0 for Tier 1 (already installed), 5 for marketplace install, 10 for manual clone, 15 for requires additional setup (API keys, MCP servers, etc.) |

Within each tier, sort results by descending relevance score. Drop results scoring below 15 (too weak a match to be useful).

**Dedupe across tiers:** A plugin or skill that appears in one tier must not appear in another. Tier 1 takes priority over Tier 2, Tier 2 over Tier 3. When running `/kerd:lorg all`, check each Tier 2/3 result against Tier 1 results (by plugin name or repo URL). When running a single tier, also check against preserved results from the report file. If a match is found, drop the lower-tier duplicate.

**Explanation quality:** The "Why here" line in each card must cite specific project signals, not generic descriptions. Bad: "This plugin helps with testing." Good: "Your TODO.md mentions 'add integration tests' and your last 3 session logs show repeated manual test runs." Connect the recommendation to something concrete from the project profile. If you can't name a specific signal, the match is too weak — drop it.

### 6. Display report

Show a combined report. Tiers that were not scanned this run show their preserved data with the original scan date, or "Not yet scanned" if no data exists.

```
┌─────────────────────────────────────────────────┐
│  /kerd:lorg: [project-name]                     │
└─────────────────────────────────────────────────┘

Project profile:
  Tech: [languages, frameworks, deployment]
  Themes: [extracted work themes]

━━━ Tier 1: Installed but not activated here ━━━━
Last scanned: YYYY-MM-DD

[rich cards or "No matches. You're using everything relevant."]

━━━ Tier 2: Available but not installed ━━━━━━━━━
Last scanned: YYYY-MM-DD

[rich cards or "No matches found in marketplace or curated sources."]

━━━ Tier 3: Worth exploring ━━━━━━━━━━━━━━━━━━━━
Last scanned: YYYY-MM-DD

[rich cards or "No new discoveries this scan."]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 N installed matches · N available · N to explore
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 7. Save report (incremental)

Write the report to two locations, updating only the tiers that were scanned:

**Repo-side:** `docs/lorg-report.md`. If the file exists, read it first and preserve sections for tiers that were not scanned this run. Overwrite only the scanned tier sections and the project profile. Each tier section retains its own `Last scanned: YYYY-MM-DD` date.

**Vault-side:** `[Name] Lorg Report.md` in the Obsidian vault (e.g., `Kerd Lorg Report.md`). Same incremental logic as repo-side. Resolve the vault path via `kivna/vault.json`.

Both files get identical content. The repo copy travels with git. The vault copy is searchable in Obsidian.

### 8. Post-report walkthrough

After the report, walk through each newly scanned item individually. Different actions per tier:

- **Tier 1:** `> 💬 **Shall I show how to use [skill] in this project?**`
- **Tier 2:** `> 💬 **Shall I install [plugin]?**` On approval, run the install command
- **Tier 3:** `> 💬 **Shall I fetch the README for [repo] so you can see more?**`

No batch actions across tiers. Different trust levels require different handling.

If the user says "skip" or "done" at any point, stop the walkthrough.

Only walk through results from tiers scanned this run. Do not re-walk preserved results from previous scans.

## Curated Sources

The curated source list lives in the Obsidian vault, synced between machines:

**Location:** `~/eolas/vault/[folder]/discover-sources.json` (resolved via vault discovery from `kivna/vault.json`)

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

- `repos`: GitHub repos to check for Claude Code plugins/skills
- `urls`: web pages to scan for plugin references and recommendations

To add a source: edit the file directly or ask lorg to add one.

## What Lorg Does NOT Do

- **No auto-install.** Every install is prompted and approved individually.
- **No removal suggestions.** A skill unused in this project may be critical in another. Lorg finds gaps, not waste.
- **No health checks.** That's tend's job (structure) or slainte's job (content).
- **Incremental saves.** Running one tier preserves other tiers' data in the report. Only `/kerd:lorg all` refreshes everything.
- **Ranked by relevance.** Results are scored (theme match + tech match + recency boost - friction) and sorted within each tier. Weak matches (score below 15) are dropped.

## Notes

- The project profile is computed fresh each run. Not stored. Projects evolve, and stale profiles would mislead.
- Layer 2 (work signals) is what makes lorg genuinely useful beyond simple file-extension matching. It catches non-technical skill gaps like "you keep writing investor updates."
- If no vault is found, Tiers 1 and 3 still work. Tier 2's curated sources are skipped with a note suggesting vault setup.
- Lorg writes two files each run (`docs/lorg-report.md` and the vault report) and optionally installs Tier 2 plugins with approval. It does not modify other project files.
