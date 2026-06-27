# Obsidian Vault Specification

Create an Obsidian vault folder at `~/eolas/vault/{{project-name}}/` that captures the living context of this project. The vault should be readable by someone with no prior knowledge. It is not a repo mirror. It is not a session log. It is not a dump of machine-readable files.

Look at `~/eolas/vault/krutho-strategy/` for the reference implementation. (Ignore its `sessions-of-record/` folder — that is legacy drift; session history is repo-side, see the boundary below.)

## The repo / vault boundary

A Kerd project has two homes, and they hold different things:

- **The repo** holds machine and working state: code, `CLAUDE.md`, `TODO.md`, and the session history in `kivna/sessions/`. This is plumbing — written and read by tools.
- **The vault** holds human knowledge: what the project is, where it stands, what's been decided. This is for a person returning cold.

**Session history lives in the repo (`kivna/sessions/`), never in the vault.** The vault's `Status.md` and `Weekly.md` summarize where things stand; they do not archive what happened session by session. If you find yourself wanting a `sessions/` folder in the vault, that belongs in the repo.

## Principles

The vault serves humans returning after a month away. Every file answers a question someone would actually ask. If a file only makes sense with context from another system (a repo, a conversation, a task tracker), it does not belong here.

No symlinks to repo files. No CLAUDE.md, README.md, TODO.md, or CONTEXT.md. Those are machine instructions. The vault contains knowledge, not plumbing.

No session logs, context dumps, append-only files, or one-liner changelogs. If something changes, update the existing file. One living summary beats ten dated snapshots.

No kivna exports, session outputs, or LLM handoff artifacts. Those belong in the repo.

Every filename must be self-identifying. Someone using Obsidian's quick switcher (Cmd+O) across multiple project vaults must be able to find any file by name alone. No generic names like "Context.md", "Notes.md", or "Decisions.md". Prefix with the project or company name: `Krutho Positioning Contract.md`, not `Decisions.md`.

## The Spine (always scaffolded)

Every project gets the same small skeleton — the files that answer the same questions in every project: *what is this, where does it stand, what's the cadence.* `{{Project Name}}` is the title-case project name (e.g. `Leru`, `Weefish`), matching the existing convention.

**MOC:** `{{Project Name}}.md`
Entry point. Links to every other file with a one-line description. Under 40 lines. Organized by category. The thing you point a person — or an AI — at first.

**Status:** `{{Project Name}} Status.md`
Living summary: where we are, what's working, what's open, what's next. Two screens max. Overwritten each session, not appended to.

**Weekly:** `{{Project Name}} Weekly.md`
Rolling tracker of achievements and risks by week. Each week gets a section (anchored to Monday's date) with achievements (what shipped, what was decided) and risks (with `[open]` or `[mitigated]` markers). Weeks in reverse chronological order. Updated by Kivna save, not overwritten. This is the one append-style file in the vault — it exists because status reports need history, and Status.md (which captures only current state) can't provide that. Created up front with its header/structure ready for the first weekly entry, so the spine is uniform across projects.

### Rule: scaffold the spine, never the content

When creating a project, create the spine and nothing else. Do not pre-create optional slots. Do not create empty domain files. An empty file is the same sin as a generic template — it implies content that isn't there. Slots get created the moment they have something to hold, not before. (The spine's three files are the exception: MOC and Status are seeded with real content from the intake below; Weekly carries only its known structure, ready to fill.)

## Optional slots (created only when needed, canonical names)

Everything beyond the spine is an optional slot. The point is not to pre-create them — it's that when a project *does* need one, it uses the canonical, project-prefixed name so it never drifts (`{{Project}} Decisions.md`, not `decision-log.md` or notes buried in the hub). Add a file the moment it has something to hold.

Domain content (Strategy, Positioning, Design, Tokens, client subfolders) is explicitly **not** slotted. It varies by project and should.

### If there is a company or product

**Company:** `{{Company}} Company.md`
What is this thing, who built it, what's the history. Written so a stranger understands.

**Playbook:** `{{Company}} Playbook.md`
The bible. How to describe and position the company/product. Descriptions at multiple lengths (tagline, elevator pitch, networking intro, short text, long text). Messaging for different audiences. Proof points with sources. Common objections and answers. Voice and tone rules. Buyer profiles. Sales motion. If something contradicts another doc, the playbook wins. Grows over time.

### If there are client engagements

Create a subfolder per client: `{{client-name}}/`

**Engagement:** `{{Client}} Engagement.md`
How it started, who's involved (both sides), contacts by team, timeline, context definitions (explain jargon and systems the client uses), the opportunity, outcomes.

**Opportunity:** `{{Client}} Opportunity.md`
The sales case. Why this deal matters strategically. What the client needs. Why only we can solve it. Revenue impact. Expansion potential. Deal risks with severity and mitigation. Signals of strength.

**Key meetings/workshops:** `{{Client}} Workshop {{Date}}.md`
Readable narrative of what happened. Who was there, what was presented, what debates occurred, what landed, what's still open. Not a transcript. A story someone can read cold.

**Account research:** `{{Client}} Account Research.md`
External intel: recent news, hiring signals, qualification signals, discovery questions.

### If there are positioning rules

**Positioning contract:** `{{Project}} Positioning Contract.md`
Language rules ("say this, not that" with context for why). Framing decisions. Technical decisions with rationale. Updated when new decisions are made.

### If there is technical content

**Solution overview:** `{{Project}} Solution Overview.md`
What is being proposed, how it works step by step, key technical details. Written so a smart non-expert can follow it. Not a repo README. A human explanation.

### If the project makes commitments worth a paper trail

**Decisions:** `{{Project}} Decisions.md` (see obair) — or, for design-specific choices, **Architecture decisions:** `{{Project}} Architecture Decisions.md`
Design choices with rationale. What was decided, why, what alternatives were rejected and why. Updated when new decisions are made.

### If the work is built on reference material

**Sources:** `{{Project}} Sources.md` plus `{{Project}} Source - {{Title}}.md` per source (see toyota-sensei)
The reference material the work draws on, each source captured as its own self-identifying file with the index in `Sources.md`.

### If there are users

**Usage guide:** `{{Project}} Usage Guide.md`
How to use the thing. Examples. Common workflows. Written for the target user.

**Install guide:** `{{Project}} Install Guide.md`
How to set up the thing. Prerequisites, steps, verification.

### Research

Name by topic: `CNA Captive Portal Research.md`, not `notes-research-2.md`. Put in a `research/` subfolder or alongside the engagement it supports.

## Per-project intake (kivna scaffold)

When scaffolding a new project — or when an existing project is missing information the spine needs — `kivna scaffold` runs a short, light intake to seed the hub note and Status. This replaces "blank folder, figure it out later."

This is a batched intake, not an interrogation: ask everything up front in one round, the way dian's pre-flight inventory does ("one round of questions now prevents many stop-and-ask rounds later"). Batch for *seeding*; drill one-at-a-time only when *deciding* something consequential. Intake is seeding.

### Interview rules

1. **One batch, ≤5 questions.** Ask everything at once, not drip-fed.
2. **Open-ended and consequential only.** Every answer must change what gets written. No yes/no confirmations, no questions whose answer is already on disk or in context.
3. **Skip what's already known.** If the project folder, repo README, or the conversation already answers a question, pre-fill it and move on.
4. **Reflect back, then write.** Summarize understanding in 2–3 lines, let the user correct, then seed the files. Don't interrogate further.
5. **Light by default.** If the user gives a one-line brain-dump that covers it, skip straight to reflect-back. The interview is a floor, not a gate.

### The questions (adapt wording; drop any already answered)

1. **What is this project, in a line or two — and why does it exist?** → seeds `{{Project Name}}.md` opening + purpose.
2. **What does "done" or "working well" look like?** → seeds success criteria / definition of done in the hub.
3. **Where does it stand today — what's already true?** → seeds `{{Project Name}} Status.md`.
4. **What are the hard constraints or non-negotiables?** → seeds constraints in the hub.
5. **What's explicitly *out* of scope, or what do you not want?** → the scope ceiling; prevents over-production.

Optional 6th, only if material clearly exists:

6. **Any existing docs, repos, or references I should read in first?** → triggers a Sources slot + import rather than asking content questions the source already answers.

## Ownership

- **`kivna scaffold`** creates the spine and runs the intake. kivna is the single owner of the knowledge layer — it is the only writer of vault files (see state-contract).
- **`tend`** detects spine drift in existing projects (missing spine file, non-canonical slot name, a `sessions/` folder that belongs in the repo) and converges them.

*Rollout: complete. `kivna scaffold` builds the full spine (MOC + Status + Weekly) and runs the batched intake interview; `tend` (Category 3) detects spine drift in existing projects — missing spine file, vault-side session-history folder, non-canonical slot names — and points the fix back at `kivna scaffold`.*

## What NOT to Put in the Vault

- Symlinks to repo files
- CLAUDE.md, README.md, TODO.md, CONTEXT.md
- Session logs, kivna exports, LLM context dumps (these are repo-side, in `kivna/sessions/`)
- Append-only logs or changelogs other than Weekly
- Operational files (build configs, task lists, CI/CD)
- Empty placeholder files or TBD sections
- Workshop slide files, facilitation guides, or other repo working documents (summarize them in vault-native files instead)

## Quality Test

After building the vault, read every file as someone who knows nothing. Ask:

1. Can I understand what this project is without external context?
2. Can I understand the current state without reading every file?
3. Can I find any file by name in the quick switcher without knowing the folder?
4. Does every file answer a question someone would actually ask?
5. Are terms, systems, and jargon defined where they first appear?
6. Is there a gap where I'd need to leave Obsidian to understand something?

If any answer is wrong, fix it before moving on.

## How to Grow

The vault grows through use. When a new engagement starts, add a folder and the key files. When a positioning decision gets made, add it to the contract. When an objection comes up in a call, add it to the playbook.

Do not add files for things that haven't happened yet. The vault reflects what is known.

## Cross-Linking

Use `[[project-name/File Name]]` wikilinks to link between projects. Use `[[people/Name]]` for people (shared directory at `~/eolas/vault/people/`). Check what exists before creating duplicates.

## Reference

The krutho-strategy vault (`~/eolas/vault/krutho-strategy/`) has the full pattern:

```
krutho-strategy/
  Krutho Strategy.md                ← MOC (spine)
  Krutho Strategy Status.md         ← living status (spine)
  Krutho Strategy Weekly.md         ← weekly cadence (spine)
  Krutho Playbook.md                ← company bible
  Krutho Company.md                 ← company overview
  Krutho Solution Overview.md       ← technical proposal
  Krutho Positioning Contract.md    ← language and framing rules
  delta/
    Delta Opportunity.md            ← sales case
    Delta Engagement.md             ← relationship map
    Delta Workshop March 12.md      ← key meeting narrative
    Delta Account Research.md       ← external intel
```

Spine (MOC + Status + Weekly) plus optional slots. Zero symlinks. Zero session dumps. All self-identifying names. Readable cold. (The on-disk folder also has a stray `sessions-of-record/` — legacy drift to clean up; session history is repo-side.)
