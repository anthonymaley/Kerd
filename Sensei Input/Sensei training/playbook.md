# Playbook: Toyota Sensei

How to rebuild this project from scratch.

## Tech Stack
- Claude Code skill plugin (SKILL.md files, no runtime dependencies)
- HTML/CSS for A3 output artifact (no build step, renders in any browser)
- Markdown for secondary output artifact

## Setup
1. Clone repo
2. Install plugin: reference this repo's `plugin.json` in Claude Code settings or copy skills/ into your plugin directory
3. Verify: `/sensei:work`, `/sensei:coach`, `/sensei:learn`, `/sensei:review`, and `/sensei:story` should be available as slash commands

## Architecture
- `skills/work/SKILL.md` LLM discipline mode (/sensei:work)
- `skills/coach/SKILL.md` human coaching mode (/sensei:coach)
- `skills/learn/SKILL.md` sensei teaching mode (/sensei:learn)
- `skills/review/SKILL.md` red-ink A3 review mode (/sensei:review)
- `skills/story/SKILL.md` A3 story type router (/sensei:story)
- `skills/story/types/` 7 story type definitions (one file per type)
- `skills/shared/a3-template.html` A3 artifact template (work + coach output)
- `skills/shared/a3-review-template.html` annotated A3 template (review output)
- `skills/shared/a3-story-template.html` story A3 template (configurable sections, nemawashi footer)
- `docs/sensei-knowledge-base.md` Toyota Way concepts, read by all skills at invocation (curated synthesis)
- `docs/sources/` source extraction files, one per book (not read by skills directly)
- `docs/sources/sources-index.md` catalog of ingested sources
- `docs/tps-framework.md` canonical 9-step framework reference

Work and coach follow the same 9-step framework. Left column (steps 0 through 4) must be confirmed before the right column begins. Both produce progressive A3 artifacts. Learn is conversational: no artifacts, no step progression. Review reads a completed A3 and produces an annotated HTML artifact with red-ink feedback and a verdict (pass/rework/reject). Story routes to one of 7 story types (proposals, comparisons, education, roadmaps, discrepancy correction, illumination), then builds the A3 progressively with Rock Solid compression discipline. Works in coaching mode (human builds) or LLM mode (sensei builds).

Source files are the raw material. The knowledge base is the refined product. Five sources: Liker, 1973 TPS Handbook, Ohno, Platt (TMMNA pocketmod), and Japanese source analysis. When adding a new book: extract to docs/sources/, update the sources index, then rebuild the knowledge base.

## Integrations
- None (self-contained Claude Code plugin)
- docs/sensei-knowledge-base.md synthesized from five sources: Liker, 1973 TPS Handbook, Ohno, Platt pocketmod, Japanese source analysis
- Toyota website (global.toyota/en/company/vision-and-philosophy/production-system/), attempted but unreachable during setup

## Deployment
Plugin is installed locally via Claude Code plugin settings. No remote deployment needed.

## Gotchas
- EPUB processing: unzip the epub, strip HTML tags with sed, read the resulting text files. The Read tool cannot handle EPUB natively.
- Knowledge base size: `docs/sensei-knowledge-base.md` is read at skill invocation. Currently 933 lines, 14 sections (synthesized from 5 sources). If it grows past 2,000 lines, split into core (always loaded) + supplementary (on demand).
- Story type files: `skills/story/types/` contains one file per story type. The SKILL.md reads only the selected type file after routing. Do not inline type definitions into SKILL.md. The modular structure keeps context lean.
- Skill directory structure: skills must live at `skills/{skill-name}/SKILL.md` (one level deep), not nested under a subdirectory. The plugin name already provides the namespace.
- Toyota website unreachable: `global.toyota/en/.../production-system/` returned connection errors. The books are the primary sources.
- Source files in docs/sources/ are not read by skills directly. Only the knowledge base is.
- Claude-in-Chrome browser tools refuse `file://` URLs. To test a local HTML artifact in-browser, serve it over localhost first (`python3 -m http.server` in the directory) and navigate to `http://127.0.0.1:<port>/...`.
- Directory renames break the Claude Code shell permanently for the rest of the session. The Bash tool validates CWD before executing, so if the directory moves, all git/shell commands fail. Do directory renames as the very last step or accept you'll need a fresh session.

- UserPromptSubmit hook format: requires nested structure (matcher + hooks array), not flat type/command. Hooks fire immediately without restart; CLAUDE.md requires session restart. See ~/.claude/settings.json for correct format.

- /sensei:work evidence protocol: the LLM will create `kivna/output/sensei-[slug]/evidence/` directories during problem-solving. These contain numbered observation files with raw query outputs. They are part of the deliverable, not temporary files.
- Progressive A3 build (reworked 2026-07-20): the A3 HTML file is created at Step 0 with one full write, then updated after every confirmed step with targeted Edit operations anchored on the template's `id="step-N"` attributes. Full-file rewrite is the fallback when an Edit anchor fails. If the A3 doesn't auto-open, run `open kivna/output/sensei-[slug]/sensei-[slug].html` manually.
- The `id="step-N"` attributes in `skills/shared/a3-template.html` are Edit anchors for the progressive build — renaming or removing them silently breaks the update rules in work/story SKILL.md (the fallback masks it as constant full rewrites).
- Progressive A3s carry a `<meta http-equiv="refresh" content="10">` tag inserted at Step 0 so the open browser tab tracks progress live. It MUST be removed at close (work Step 9b, story closing) — a finished artifact must not refresh forever. Scroll-position behavior on auto-refresh is not yet verified.
- A3 content that *mentions* placeholder names must HTML-entity-escape the braces (`&#123;&#123;NAME&#125;&#125;`) — otherwise mid-build they render as if unfilled and the close-out invariant grep for leftover raw `{{` false-positives on content. Discovered in the first /sensei:story live run (2026-07-20).
- `/sensei:coach` uses the same `a3-template.html` one-shot at completion — that's why the template ships with bare (unlocked) sections and no refresh tag; the progressive skills add both at Step 0.

## Current Status
Five skills: /sensei:work, /sensei:coach, /sensei:learn, /sensei:review, /sensei:story. Plugin namespace: sensei. Version 1.6.0. GitHub repo: anthonymaley/toyota-sensei. Registered as sensei@sensei-marketplace with autoUpdate. Knowledge base at 933 lines, 14 sections, covering all 14 Toyota Way principles plus A3 communication, nemawashi, and Japanese source nuance analysis. Synthesized from five sources: Liker, 1973 Handbook, Ohno, Platt pocketmod, and Japanese original text analysis. /sensei:work hardened with evidence-first protocol (v1.2.0), progressive A3 build (v1.3.0), and v1.5.0 improvements: enforced progressive rendering, perceived problem preservation, standard observation at Step 2, verify+monitor split at Step 7, plan file output, measurement discipline. /sensei:story adds Toyota's 7 A3 story types (v1.4.0). TPS Practitioner Prompt v0.2.0 installed at ~/.claude/CLAUDE.md with UserPromptSubmit hook. All five skills end-to-end tested: /sensei:review (3 external A3s, PNG + PDF + HTML), /sensei:learn (Path 9 Leadership), /sensei:coach (earlier session), /sensei:work (leru team-name-matching, PASS verdict on review), /sensei:story (Type 4 proposal, LLM mode, 2026-07-20 — matrix closed 5/5). A3 render path overhauled 2026-07-20: progressive builds switched from full-file rewrite per step to targeted Edits anchored on template section ids (~6-7x fewer output tokens on the render path, confirmed sections immutable on disk), plus live auto-refresh while in progress; verified by 77-edit flow simulation and a live /sensei:story Type 4 run (21 targeted Edits, 0 fallback rewrites, 2026-07-20); a live /sensei:work run under the new rules remains untested.
