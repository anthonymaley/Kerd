# Obsidian Vault Specification

Create an Obsidian vault folder at `~/eolas/vault/{{project-name}}/` that captures the living context of this project. The vault should be readable by someone with no prior knowledge. It is not a repo mirror. It is not a session log. It is not a dump of machine-readable files.

Look at `~/eolas/vault/krutho-strategy/` for the reference implementation.

## Principles

The vault serves humans returning after a month away. Every file answers a question someone would actually ask. If a file only makes sense with context from another system (a repo, a conversation, a task tracker), it does not belong here.

No symlinks to repo files. No CLAUDE.md, README.md, TODO.md, or CONTEXT.md. Those are machine instructions. The vault contains knowledge, not plumbing.

No session logs, context dumps, append-only files, or one-liner changelogs. If something changes, update the existing file. One living summary beats ten dated snapshots.

No kivna exports, session outputs, or LLM handoff artifacts. Those belong in the repo.

Every filename must be self-identifying. Someone using Obsidian's quick switcher (Cmd+O) across multiple project vaults must be able to find any file by name alone. No generic names like "Context.md", "Notes.md", or "Decisions.md". Prefix with the project or company name: `Krutho Positioning Contract.md`, not `Decisions.md`.

## What to Build

Answer these questions. Each answer becomes a file. Not every project needs every file. Start with what exists and add as the project grows.

### Always

**MOC:** `{{Project Name}}.md`
Entry point. Links to every other file with a one-line description. Under 40 lines. Organized by category.

**Status:** `{{Project Name}} Status.md`
Living summary: where we are, what's working, what's open, what's next. Two screens max. Overwritten each session, not appended to.

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

### If there are architecture or design decisions

**Architecture decisions:** `{{Project}} Architecture Decisions.md`
Design choices with rationale. What was decided, why, what alternatives were rejected and why. Updated when new decisions are made.

### If there are users

**Usage guide:** `{{Project}} Usage Guide.md`
How to use the thing. Examples. Common workflows. Written for the target user.

**Install guide:** `{{Project}} Install Guide.md`
How to set up the thing. Prerequisites, steps, verification.

### Research

Name by topic: `CNA Captive Portal Research.md`, not `notes-research-2.md`. Put in a `research/` subfolder or alongside the engagement it supports.

## What NOT to Put in the Vault

- Symlinks to repo files
- CLAUDE.md, README.md, TODO.md, CONTEXT.md
- Session exports, kivna outputs, LLM context dumps
- Append-only logs or changelogs (those belong in git)
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
  Krutho Strategy.md                ← MOC
  Krutho Playbook.md                ← company bible
  Krutho Company.md                 ← company overview
  Krutho Strategy Status.md         ← living status
  Krutho Solution Overview.md       ← technical proposal
  Krutho Positioning Contract.md    ← language and framing rules
  delta/
    Delta Opportunity.md            ← sales case
    Delta Engagement.md             ← relationship map
    Delta Workshop March 12.md      ← key meeting narrative
    Delta Account Research.md       ← external intel
```

Ten files. Zero symlinks. Zero dumps. All self-identifying names. Readable cold.
