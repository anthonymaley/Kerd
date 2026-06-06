# Skill Architecture Review — 2026-05-04

Umbrella design doc for a full skill architecture pass on Kerd. First focus is mode redesign; other skills are reviewed afterward and captured in this same doc.

## Context

- This conversation began as a `/kerd:switch in` and pivoted into an architecture audit when dian's prompt verbosity and multiple-choice patterns surfaced.
- An initial diagnosis named three multiple-choice prompt violations in dian (lines 73, 84, 129) against the new global Question-formation gate (#7) shipped on 2026-05-04 in `~/.claude/CLAUDE.md`.
- Scope expanded into a broader question: where do dian, interrogate, mode, and Superpowers' deep skills overlap, what's duplicated, what's missing? A 5-question survey was run across ~30 skills (Kerd + Superpowers + adjacent plugins).
- The survey surfaced six patterns. Pattern #1 ("sequential chains aren't named — each skill is an island") was initially diagnosed as a skill-layer problem (cross-references between skills). The user pushed back: that's mode's job. The reframe below is load-bearing for everything that follows.

## Reframe (load-bearing)

**Kerd plugin = modes only. Skills live in a separate plugin (`kerd-skills` provisional name).** Provisionally locked; may bundle some skills back into Kerd plugin later if "out of the box" UX requires it.

**Skills are atomic capabilities. Modes are the only orchestrators.**

- Skills do not reference each other in flow terms ("after this, call X"). Each skill describes only what it does, not what comes before or after.
- Modes are the bridge. Each mode file defines a complete flow for a given work shape, naming every skill invocation in order.
- The plan-lifecycle chain (brainstorm → interrogate → writing-plans → executing-plans → TDD → verification) doesn't live in any skill — it lives in modes that use that chain.

### Three layers, not two

The architecture has three layers, not two:

1. **Skills (atomic).** Single capabilities. Don't reference each other in flow terms.
2. **Modes (orchestrators).** Define complete flows across skills for a given work shape.
3. **Discipline gates (universal).** Fire on condition from anywhere via skill description triggers. Examples: `superpowers:verification-before-completion`, `superpowers:requesting-code-review`. Gates are not configured per-mode and not exceptions to the skills-are-atomic rule — they live at the global skill-trigger layer and apply to every session, mode or not, Kerd repo or not.

One genuine exception remains at the skill layer: **structural primitives** — single-source-of-truth calls between skills that are plumbing, not flow. Example: `switch.out` calls `kivna save` because kivna is the sole vault-write path.

### Skill vs. mode boundary test

A skill that contains internal orchestration (e.g., `switch` reads files, summarizes, prompts) is still a skill, not a mode. The distinguishing test: **does the orchestration cross skill boundaries?** Mode orchestrates across skills (call brainstorming, then interrogate, then writing-plans). Skill orchestrates within itself (file reads + summary + decision).

Switch's only cross-skill call is `kivna save`, which is a structural primitive. So switch stays a skill.

### What dissolves under this reframe

Several "gaps" identified earlier in the conversation are wrong-shaped under this model:

- ~~"interrogate doesn't hand off to writing-plans"~~ — wrong. The mode that includes both names the order. interrogate stays atomic.
- ~~"dian doesn't know about interrogate"~~ — wrong for the same reason. Mode places interrogate before dian when readiness is needed.
- ~~"dian.execute should defer to TDD/debugging"~~ — partly wrong. The mode names the deep skill; dian.execute defers to the mode's step. If no mode is active, dian.execute is correctly generic.
- ~~Mode frontmatter needs `discipline_gates`~~ — wrong. Gates fire universally via skill description triggers; mode frontmatter doesn't need to list them. Originally proposed as M1 in this doc; M1 is dropped.

## Mode redesign

### Goal

Mode files become real orchestration documents, not checklists. Each mode is a complete flow with explicit per-step guardrails so the agent stays inside the mode's lane.

### File format (new)

```
---
name: <mode-name>
description: <one-line>
category: <category>
capabilities:
  - id: <capability-id>
    description: "What this capability needs to do — articulate it precisely
      so a skill author or skill-assessor knows exactly what fulfilling it
      requires"
  - id: <capability-id>
    description: "..."
discover_keywords:
  - ...
follow_on:                   # optional logical successor mode(s)
  - mode: <mode-name>
    rationale: "..."
---

## Success
What success looks like for this flow as a whole. 1–3 sentences. Gives the agent
flow-level intent so step-level execution stays oriented.

## <Phase Name>

### Step N: <capability-id>
**Goal:** What this step accomplishes within the flow.
**Do:** What the capability should produce in this step's context.
**Don't:** Things to avoid that would drift from the flow.
**Exit when:** Condition that confirms the step is done.
**Produces:** Artifact, if any (e.g., readiness doc, plan file, commit).

### Step N+1: Inline action
(Same five fields. The step header explicitly says "Inline action" — no
capability invocation. The agent acts directly without invoking a mapped skill.)
```

Every step is unambiguously **either a capability invocation (referenced by id) or an inline action**. No skill names appear in mode files. Skill mapping (which skill fulfills which capability) is a separate layer, defined post-mode-design.

Five-field per-step block (Goal / Do / Don't / Exit when / Produces). Optional fields can be omitted (e.g., a step that produces no artifact omits Produces).

### Active-mode tracking

`kivna/.active-modes` semantics extended:

- `mode: <name> (step N of M)` — active mode with progress (existing)
- `mode: free` — explicit user choice to operate without orchestration (new)
- File missing or no `mode:` line — no choice yet; SessionStart hook prompts

`switch.out` clears the mode line in all cases (existing for active modes; new for `free`). User must re-pick on next session.

### Mode entry: switch-in is the single entry point

Update `/kerd:switch in` step 10:

- Today: "Start a `/kerd:dian` session?"
- New: List all available modes by category (Development, Business, Operations, Other) and prompt for selection. Always include `free` as an option (no orchestration). Selected mode becomes the active mode for the session.

`/kerd:mode <name>` remains available as a direct entry point for users who want to start a mode without going through switch-in.

The SessionStart hook (`hooks/session-start.sh`) stays as today — silent-when-quiet, surfaces stale state only (behind remote, last session date, interrupted mode). It does NOT prompt for mode. Mode selection is switch-in's job, not the hook's.

Sessions that bypass switch-in (direct slash commands, quick lookups) skip mode selection — they're typically ad-hoc work that doesn't need orchestration.

### Follow-on mode suggestion

When a mode completes (mode/SKILL.md step 6: "Complete"), if the mode's frontmatter has a `follow_on` field, prompt the user: "Start `<follow_on_mode>` next?"

Example chains:
- `brainstorming` → `interrogate` (after shape, stress-test viability)
- `interrogate` → `planning` (after readiness, write the plan)
- `planning` → `execution` (after plan, build it)

`follow_on` is a list, so a mode can suggest more than one logical successor. User can accept one, decline, or pick a different mode entirely. Default behavior at completion stays: clear the mode block from `.active-modes`. Follow-on prompt is layered on top.

### Final mode set: 16 modes

The existing 10 modes are not the target. The user redefined the canonical mode set during this review. Final list:

| # | Mode | Status | Notes |
|---|---|---|---|
| 1 | new idea | NEW | Capture idea, market analysis, gap, plan next |
| 2 | plan | NEW | What's next, steps, gates, milestones |
| 3 | interrogate | NEW | Mode wrapping `kerd:interrogate` skill — exhaustive understanding |
| 4 | research | reframe | Consultancy-level research across all aspects (broader than today's market-only) |
| 5 | spike | keep | Try-matrix, evidence gates (today's spike already rich) |
| 6 | product design | NEW | Formally design the product — what, how, users, GTM |
| 7 | strategy | reframe | Money, funding, team, launch, investors, positioning (broader) |
| 8 | writing | keep | Content creation |
| 9 | adversarial review | NEW | Self-grilling via personas, find holes |
| 10 | problem analysis | NEW | Wraps `sensei:work` (Toyota 9-step) |
| 11 | sales | keep | Pipeline, outreach, closing |
| 12 | execute | NEW | Pick up an existing plan and build it |
| 13 | maintain | reframe | Hygiene: tend, slainte, lorg, trim, skriv audits |
| 14 | peer review reception | NEW | Receive review of your work, contextualize, draft response |
| 15 | call transcript analysis | NEW | Save transcript, analyze, summarize, action items |
| 16 | project-manage | NEW | Track plans/comms/reviews/updates for a named project; queryable status/next-step/update |

**Retired** (existing modes that drop entirely): `deepwork`, `greenfield`, `quickfix`, `legal`.

Reasoning: deepwork folds into `plan` + actual execution; greenfield folds into `new idea` → `product design` → `plan` → `execute`; quickfix folds into a tiny `plan` invocation; legal folds into `research` + `writing` with legal-context instruction.

### New skill: email-writer

Narrow, reusable. Iterative drafting + paste-ready formatting. Called from sales/peer-review/legal/writing modes when email output is needed.

- **Naming candidate:** `kerd:email` or `kerd:compose` (English per rename plan)
- **Function:** capture intent → iterate (bounce ideas) → produce well-formatted email ready to paste
- **Differs from `sales:draft-outreach`** (sales-specific) — domain-agnostic

### Migration approach for the 16 modes

- 6 modes keep with rewrite: research, spike, strategy, writing, sales, maintain
- 10 modes are new authoring: new idea, plan, interrogate, product design, adversarial review, problem analysis, execute, peer review reception, call transcript analysis, project-manage
- 4 modes retired (deleted): deepwork, greenfield, quickfix, legal

For each: brief first (Purpose / Success / Phases / Key skills / follow_on), then full per-step content during M2 implementation.

### Mode full specs (per-step expansion)

#### Mode 1: new idea — full spec

**Frontmatter:**

```yaml
---
name: new idea
description: "Capture an idea, get to its core, scan the marketplace, identify the gap, decide what to do next"
category: discovery
capabilities:
  - id: session-boundary
    description: "Open and close the session; load prior context that may relate; persist context across machines at close"
  - id: idea-exploration
    description: "Get an idea to its core via open questions; force articulation of what it is, what problem it solves, who for; resist paraphrases of user's intent; hold open until 2–3 distinct angles surface"
  - id: market-research
    description: "Retrieve clean external content on competitors and adjacent products; cite sources for every finding; no training-data fallback for external claims"
  - id: vault-capture
    description: "Persist session output to vault as the durable, human-readable record; one write per session"
discover_keywords:
  - "new idea"
  - "idea"
  - "concept"
  - "what if"
  - "capture"
follow_on:
  - mode: interrogate
    rationale: "default — stress-test the idea before committing"
  - mode: research
    rationale: "if market analysis needs depth"
  - mode: spike
    rationale: "if a technical question blocks decision"
---
```

**Success:** A clear one-paragraph statement of the idea's core; an honest read on competitive landscape (worth doing / learn-from / adopt-existing / abandon); a named gap that justifies pursuing; a chosen next step. All captured in vault with cross-references to existing notes.

##### Phase 1: Setup

**Step 1: session-boundary (open)**
- **Goal:** Open the session and load any prior context that may relate
- **Do:** Invoke the session-boundary capability with "open" semantics; receive its summary back
- **Don't:** Skip context-load; an idea may relate to existing work and missing context produces redundant ideas
- **Exit when:** Session is open, prior context summarized to user
- **Produces:** Session-context summary in conversation

**Step 2: Inline action — confirm idea source**
- **Goal:** Establish what we're capturing — fresh idea, branch off existing work, or response to external trigger
- **Do:** Ask one drilled question: "What's the source of this idea?" Wait for one-sentence answer.
- **Don't:** Bundle multiple framing questions; don't infer the source
- **Exit when:** Source named in one sentence
- **Produces:** Source statement (recorded in session state)

##### Phase 2: Capture

**Step 3: idea-exploration**
- **Goal:** Get the idea to its core — what is it, what problem does it solve, who's it for
- **Do:** Hold the conversation until 2–3 distinct angles surface. Force articulation of the core in the user's own words.
- **Don't:** Jump to solutions. Don't pre-shape into a plan. Don't accept paraphrases of the user's intent — push for the core.
- **Exit when:** A 1-paragraph idea statement is written that isn't a paraphrase and answers: what is it, what problem, who for
- **Produces:** Idea statement (1 paragraph)

**Step 4: Inline action — name a working title**
- **Goal:** Stable referent for subsequent steps so the idea has a name
- **Do:** Propose a 2–4 word working title; user confirms or adjusts
- **Don't:** Skip — every later step (vault filename, follow_on chain, capture) references it
- **Exit when:** Title agreed
- **Produces:** Working title

##### Phase 3: Market scan

**Step 5: Inline action — generate search angles**
- **Goal:** Surface 5–10 competitor candidates and 3–5 search angles so the scan is productive
- **Do:** List candidates by name + URL hint where known. Search angles like "X for Y use case", "alternatives to Z".
- **Don't:** Skip — going straight to web search without angles produces noise and the agent confidently summarizes irrelevant pages
- **Exit when:** Search plan written (candidates + angles)
- **Produces:** Search plan

**Step 6: market-research**
- **Goal:** Retrieve clean external content on competitors and adjacent products
- **Do:** For each search angle, fetch and read candidate sources. Cite source (URL + title) for every finding.
- **Don't:** Make competitor claims without citations. Don't summarize a page you didn't actually fetch.
- **Exit when:** ≥3 competitor products examined with cited findings
- **Produces:** Competitor findings (cited)

**Step 7: Inline action — synthesize landscape verdict**
- **Goal:** Convert raw findings into one of four landscape verdicts
- **Do:** Pick exactly one: **worth doing** (real gap exists) / **learn-from** (adapt an existing approach) / **adopt-existing** (use a competitor's product) / **abandon** (saturated, no gap). State rationale in 2–3 sentences with citations.
- **Don't:** Hedge with "depends" — pick one verdict with the evidence available; downgrade language if uncertain
- **Exit when:** Verdict named with rationale
- **Produces:** Landscape verdict (1 paragraph)

##### Phase 4: Gap

**Step 8: Inline action — name the gap**
- **Goal:** Articulate exactly what this idea would do that no competitor does (or does well enough)
- **Do:** Write the gap in 1–2 sentences. Test it: would this gap convince someone unfamiliar with the idea to pay attention?
- **Don't:** Settle for "do it better" or "differently" — those aren't gaps. Push for specificity (a feature, a market segment, a delivery model, a price point).
- **Exit when:** Gap statement passes the convincing-stranger test in your honest read
- **Produces:** Gap statement (1–2 sentences)

##### Phase 5: Next step

**Step 9: Inline action — pick follow-on mode**
- **Goal:** Choose what happens next based on idea state and landscape verdict
- **Do:** Default mapping — viable + clear → `interrogate`; viable + market unclear → `research`; viable + technical blocker → `spike`; abandon → close out, no follow_on. State the chosen mode explicitly.
- **Don't:** Skip this step — the entry mode's value is partially in handing off cleanly with continuity intact
- **Exit when:** Next mode chosen or "no follow-on" stated
- **Produces:** Next-step decision

**Step 10: vault-capture**
- **Goal:** Persist all session output to vault as the idea's home
- **Do:** Save idea statement, working title, landscape verdict, gap statement, next-step decision, citations. Cross-link to any relevant existing vault notes.
- **Don't:** Save piecemeal earlier in the session — vault-capture is the single vault write
- **Exit when:** Vault entry reflects this session's output
- **Produces:** Vault entry for the idea

**Step 11: session-boundary (close)**
- **Goal:** Close session cleanly with handoff
- **Do:** Invoke the session-boundary capability with "close" semantics
- **Don't:** Skip if multi-machine
- **Exit when:** Session closed
- **Produces:** Session log + remote sync

##### Notes for implementation

- 4 capability ids used (session-boundary used twice — open + close), 6 inline actions
- 11 steps across 5 phases
- Skill mapping deferred — capability ids resolve to skills at runtime via the skill-map (separate layer, defined post-mode-design)
- Steps 5, 7, 8, 9, 10's "Don't" entries encode discipline that would otherwise drift in execution
- The four landscape verdicts in Step 7 are an explicit decision tree — kept linear per locked default, agent picks one and writes rationale

---

#### Mode 3: interrogate — full spec

**Frontmatter:**

```yaml
---
name: interrogate
description: "Exhaustively interrogate an idea/plan via adversarial interview; produce co-signed plan-readiness doc"
category: discovery
capabilities:
  - id: session-boundary
    description: "Open and close the session; load prior context that may relate to the subject; persist context across machines at close"
  - id: adversarial-interview
    description: "Conduct an exhaustive, adversarial interview producing a co-signed plan-readiness document covering all in-scope viability axes. One drilled question at a time. No multiple-choice unless genuinely discrete and small. Graduated adversarial pressure (gather → probe → stress-test → adversarial) with user-dialable level. Tree-aware ordering — decisions that constrain other decisions resolved first; depth-first within each branch. Three sign-off gates required: (a) document passes structural check + user accepts recitation proposal, (b) user has no more answers, (c) axis-by-axis recitation with per-axis user confirmation. User-veto on stop is structural. Pause/resume from document frontmatter, not conversation memory."
  - id: vault-capture
    description: "Persist readiness summary to vault as durable record; vault entry is a pointer + summary, not a duplicate of the readiness doc"
discover_keywords:
  - "interrogate"
  - "interview me"
  - "walk me through this plan"
  - "stress-test this idea"
  - "is this viable"
follow_on:
  - mode: plan
    rationale: "default — write the plan from the readiness doc"
  - mode: execute
    rationale: "if a plan already exists and readiness validated it"
---
```

**Success:** Plan-readiness document at `docs/interrogations/YYYY-MM-DD-<topic>.md` covering all in-scope viability axes; co-signed via axis-by-axis recitation; status assigned in frontmatter (viable / not-yet-viable / blocked / deferred); vault entry pointing to the readiness doc.

##### Phase 1: Setup

**Step 1: session-boundary (open)**
- **Goal:** Open the session and load any prior context that may relate to the subject being interrogated
- **Do:** Invoke session-boundary capability with "open" semantics
- **Don't:** Skip context-load — prior interrogations on related topics are useful priors
- **Exit when:** Session is open, prior context summarized
- **Produces:** Session-context summary

**Step 2: Inline action — confirm interrogation subject**
- **Goal:** Establish what specifically is being interrogated — file path, idea description, current state of execution, or reference like "current TODO" / "latest session log"
- **Do:** Ask one drilled question: "What's the subject?" Wait for one-sentence answer. Resolve references to concrete artifacts.
- **Don't:** Bundle framing questions; don't infer the subject when ambiguous
- **Exit when:** Subject named and resolved to concrete artifact
- **Produces:** Subject statement (and resolved file path if applicable)

##### Phase 2: Scope

**Step 3: Inline action — propose viability axes**
- **Goal:** Surface the axes that should be covered for this subject
- **Do:** Read the subject content. Propose axes inferred from it (default universal axes: Scope, Goals, Stakes, Constraints; subject-specific axes vary — Technical, Business, Legal, Operational, etc.). Don't force a fixed checklist.
- **Don't:** Pre-commit to all axes being in-scope; the user will prune
- **Exit when:** Axis list proposed to user
- **Produces:** Proposed axis list

**Step 4: Inline action — prune axes**
- **Goal:** Agree which axes are in-scope, out-of-scope, or deferred up front
- **Do:** For each proposed axis, confirm: keep / out-of-scope / defer (with revisit trigger). Treat user silence as not-yet-confirmed; require explicit decision per axis.
- **Don't:** Bundle the prune as "are these all OK?" — go axis-by-axis if needed
- **Exit when:** Every axis has an explicit decision
- **Produces:** In-scope axis list, out-of-scope list, deferred list with revisit triggers

##### Phase 3: Interview

**Step 5: adversarial-interview**
- **Goal:** Exhaustively interview across all in-scope axes until shared understanding is reached and co-signed
- **Do:** Invoke the adversarial-interview capability. The capability handles its own internal dynamics: graduated pressure (gather → probe → stress-test → adversarial), one-question-at-a-time discipline, depth-first axis traversal, three-gate sign-off, axis-by-axis recitation, document-as-state for pause/resume.
- **Don't:** Declare done unilaterally — user-veto on stop is structural. Don't bundle questions. Don't slide sideways before resolving the current axis. Don't skip recitation; whole-document recitation is rejected as the easy-ratification trap.
- **Exit when:** All three sign-off gates pass: (a) document passes structural check + user accepts recitation proposal; (b) user has no more answers, requirements, or ideas to share; (c) axis-by-axis recitation complete with per-axis user confirmation
- **Produces:** Plan-readiness document at `docs/interrogations/YYYY-MM-DD-<topic>.md` with frontmatter status

##### Phase 4: Capture & close

**Step 6: vault-capture**
- **Goal:** Persist a pointer-and-summary of the readiness in vault for cross-session discoverability
- **Do:** Save link to readiness doc in vault — either update Status.md if a project context exists, or create `<Topic> Readiness.md` with a 1–2 paragraph summary + link. Cross-link to relevant existing notes.
- **Don't:** Duplicate content from the readiness doc into vault; the readiness doc is the source of truth, vault entry is a pointer
- **Exit when:** Vault entry written with link
- **Produces:** Vault entry with link to readiness doc

**Step 7: session-boundary (close)**
- **Goal:** Close session cleanly
- **Do:** Invoke session-boundary capability with "close" semantics
- **Don't:** Skip if multi-machine
- **Exit when:** Session closed
- **Produces:** Session log + remote sync

##### Notes for implementation

- 3 capability ids (session-boundary used twice — open + close), 4 inline actions
- 7 steps across 4 phases — thinner than mode 1 because the adversarial-interview capability is heavy and handles its own internal turn-by-turn dynamics
- The brief said 5 phases; the full spec collapses Recitation + Sign-off into Capture & close because recitation is inside the interview capability's exit gates, not a separate mode-level step
- Skill mapping deferred — adversarial-interview capability is the most distinct in this mode (likely a single-skill mapping, but we don't name it yet)
- Step 5's "Don't" entries are load-bearing: they encode the discipline that prevents the agent from declaring done without user-veto, bundling, or sliding sideways

---

### Mode briefs (capability-first format, all 16)

Format per brief: Purpose / Success / Phases / Key capabilities (description-only) / follow_on.

**Capabilities are description-only at this stage** — what the capability needs to do, articulated precisely so a skill author or skill-assessor knows exactly what fulfilling it requires. No skill names yet. Skill mapping (which skill fulfills which capability) is a separate layer, defined post-mode-design.

#### 1. new idea

- **Purpose:** Capture an idea, get to its core, scan the marketplace, identify the gap, decide what to do next.
- **Success:** One-paragraph statement of the idea's core; honest read on competitive landscape (worth doing / learn-from / adopt-existing / abandon); named gap justifying pursuit; chosen next step. Captured in vault.
- **Phases:** Setup → Capture → Market scan → Gap → Next step
- **Key capabilities:**
  - **Session boundary:** Open/close the session; load prior context that may relate; persist context across machines at close.
  - **Idea exploration:** Get an idea to its core via open questions; force articulation of what it is, what problem it solves, who for; resist paraphrases of user's intent; hold open until 2–3 distinct angles surface.
  - **Market research:** Retrieve clean external content on competitors and adjacent products; cite source for every finding; no training-data fallback for external claims.
  - **Vault capture:** Persist session output to vault as the durable, human-readable record; one write per session.
- **Inline actions:** confirm idea source; name working title; generate search angles; synthesize landscape verdict (4-way decision); name gap (passes convincing-stranger test); pick follow-on mode.
- **follow_on:** `interrogate` (default — stress-test before committing), `research` (if market analysis needs depth), `spike` (if a technical question blocks decision)

#### 2. plan

- **Purpose:** Define what's next, decompose into steps, identify gates and milestones to reach the goal.
- **Success:** Written plan with goal stated, steps decomposed concretely (each step independently verifiable), gates/reviews identified, risks named.
- **Phases:** Setup → Goal-framing → Step-decomposition → Gates → Capture
- **Key capabilities:**
  - **Session boundary:** Open/close the session; load prior context.
  - **Goal framing:** Articulate the goal, milestones, and success criteria; problem-frame if the goal is solving something specific.
  - **Plan production:** Produce a written implementation plan with concrete, independently-verifiable steps; identify gates/reviews; surface risks.
  - **Plan-readiness check (optional, when stakes high):** Stress-test the plan against viability concerns before committing.
  - **Vault capture:** Persist plan and decisions to vault.
- **follow_on:** `execute` (default — build the plan), `interrogate` (if doubt remains), `spike` (if a step has unknowns)

#### 3. interrogate

- **Purpose:** Exhaustive understanding of an idea/plan via adversarial interview; produce co-signed readiness doc.
- **Success:** Readiness doc at `docs/interrogations/` covering all in-scope viability axes; co-signed; status assigned (viable / not-yet-viable / blocked / deferred).
- **Phases:** Setup → Scope → Interview-loop → Recitation → Sign-off
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Adversarial interview:** Conduct an exhaustive, adversarial interview producing a co-signed plan-readiness document covering all in-scope viability axes; one drilled question at a time, no multiple-choice; axis-by-axis recitation for sign-off; user-veto on stop.
  - **Vault capture:** Persist readiness doc to vault.
- **follow_on:** `plan` (default — write the plan from readiness), `execute` (if a plan already exists and readiness validated it)

#### 4. research

- **Purpose:** Consultancy-level research across all aspects of an idea (market, tech, legal, sales, competitors, platforms, tools).
- **Success:** Comprehensive findings doc with cited sources, gaps named, conclusions drawn, recommendations.
- **Phases:** Setup → Scope → Investigation → Synthesis → Capture
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Scoping:** Define what needs to be learned across all relevant dimensions (market, tech, legal, sales, competitors, platforms, tools).
  - **Web research:** Retrieve clean external content for full-page extraction and spot lookups; cite source for every finding; no training-data fallback for external claims.
  - **Synthesis:** Organize findings into themes, gaps, conclusions, and recommendations.
  - **Vault capture:** Persist findings doc to vault.
- **follow_on:** `strategy` (if findings drive strategic decisions), `product design` (if findings inform product), `interrogate` (if findings raise viability questions)

#### 5. spike

- **Purpose:** Prove a specific aspect works via try-matrix; capture wins AND losses with evidence; commit cleanly so working solutions are extractable.
- **Success:** Working solution(s) extractable for the real build, OR canonical losses recorded with evidence; <10% confident-wrong rate; spec file complete.
- **Phases:** Setup → Try → Close
- **Key capabilities:**
  - **Session boundary:** Open/close the session (minimal context — spike is bounded).
  - **Empirical primitive:** Run a cheap, fast, ground-truth probe for the domain (AASA fetch, curl, sample-data, canary deploy); domain-specific so the capability is the framing, the probe itself is inline per domain.
  - **Try-matrix generation:** Generate variants in batch (N+1 over what was asked); the round-trip is the bottleneck.
  - **Evidence capture:** Persistent record of wins, provisional losses, and canonical losses with citations and "what would change my mind" notes.
  - **Web research with citation:** Retrieve clean external content with cited sources for context-setting and verification.
  - **Vault capture:** Persist to vault only if findings are strategically significant.
- **follow_on:** `execute` (default — build the real thing), `plan` (if more decisions needed before build)

#### 6. product design

- **Purpose:** Formally design the product — what it is, how it works, user base, target audience, GTM.
- **Success:** Design doc covering product definition, user/persona, mechanics, target audience, GTM strategy.
- **Phases:** Setup → Define → User → Mechanics → GTM → Capture
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Design exploration:** Explore product shape via open questions; force articulation of definition, mechanics, GTM angle.
  - **User/persona work:** Generate distinct personas with motivations, contexts, and friction points; drive design decisions through persona-specific probing.
  - **Doc drafting:** Produce voice-consistent, clear design doc.
  - **Vault capture:** Persist design doc to vault.
- **follow_on:** `strategy` (default — money/team/launch follow design), `adversarial review` (stress-test the design before committing), `interrogate` (if design has open viability questions)

#### 7. strategy

- **Purpose:** Money, funding, team, launch, investor management, positioning.
- **Success:** Strategic decisions made with rationale; funding/team plan; launch plan; positioning doc.
- **Phases:** Setup → Define → Analyze → Decide → Draft → Capture
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Strategic exploration:** Explore the strategic question via open questions; surface trade-offs and constraints.
  - **Decision framing:** Frame the strategic decision — options, criteria, evidence; problem-frame when the decision is solving something specific.
  - **Doc drafting:** Produce voice-consistent positioning/strategy doc.
  - **Vault capture:** Persist strategic decisions to vault.
- **follow_on:** `writing` (positioning doc → blog/investor update), `sales` (market-facing strategy)

#### 8. writing

- **Purpose:** Prose creation — blog posts, docs, investor updates, articles.
- **Success:** Published-quality piece; voice-consistent; ready for delivery.
- **Phases:** Setup → Plan → Draft → Review → Publish
- **Key capabilities:**
  - **Session boundary:** Open/close the session (light — writing is bounded).
  - **Topic exploration:** Define audience, angle, structure for the piece.
  - **Voice enforcement:** Maintain human, voice-consistent prose; avoid AI tells.
  - **Vault capture:** Persist piece to vault.
- **follow_on:** none typically (terminal); `sales` if writing supports outreach

#### 9. adversarial review

- **Purpose:** Self-grilling via personas; find holes in own work; persona-based deep probing.
- **Success:** List of holes/weaknesses surfaced from each persona's POV; revisions identified; counterfactuals named.
- **Phases:** Setup → Persona-pick → Grill → Synthesis → Action
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Persona-driven questioning:** Generate persona-specific probing questions (investor, technical reviewer, customer, regulator, etc.); ask from that POV, surface holes the original work didn't address.
  - **Adversarial mindset:** Apply graduated adversarial pressure — probe → stress-test → adversarial — without sliding into generic objections.
  - **Synthesis:** Gather holes across personas, prioritize, name counterfactuals.
  - **Vault capture:** Persist review findings to vault.
- **follow_on:** `plan` (revise plan based on holes), `product design` (revise design)

#### 10. problem analysis

- **Purpose:** Diagnose problems via Toyota 9-step framework; identify root cause; define countermeasure.
- **Success:** A3 problem doc with situation grasped, root cause identified, countermeasure named (not solution); status: tested but not yet verified.
- **Phases:** Setup → Problem-framing → Investigation → Countermeasure
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Problem-solving framework:** Apply Toyota 9-step problem solving — grasp situation, name gap, target condition, root cause, countermeasure (not solution); produce A3 doc.
  - **Vault capture:** Persist A3 doc to vault.
- **follow_on:** `plan` (countermeasure → execution plan), `execute` (if countermeasure is direct enough to act on)

#### 11. sales

- **Purpose:** Reach customers, price, close.
- **Success:** Pipeline reviewed and prioritized; outreach drafts ready; deal status updated; call/meeting prep complete.
- **Phases:** Setup → Prepare → Execute → Capture
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Prospect/account research:** Gather context on prospect/account — company, person, history, relevant news.
  - **Pipeline review:** Aggregate deal state, prioritize, surface risks; produce action plan.
  - **Outreach drafting:** Draft personalized outreach (email, message, proposal); paste-ready format.
  - **Call prep:** Prepare for a sales call — agenda, attendee research, talking points.
  - **Vault capture:** Persist deal/account state to vault.
- **follow_on:** `writing` (if content output needed), `call transcript analysis` (after a call)

#### 12. execute

- **Purpose:** Take an existing plan and build it through to completion.
- **Success:** All plan steps executed with verification at each step; final delivery matches plan acceptance criteria; tests pass.
- **Phases:** Setup → Plan-load → Step-loop → Verify → Close
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Plan loading:** Read the written plan and confirm scope before execution.
  - **Plan execution:** Execute step-by-step with checkpoints; multi-session continuation if plan exceeds one session; parallel execution when steps are genuinely independent.
  - **TDD discipline:** Apply test-driven development when implementing code (test first, fail, implement, pass).
  - **Code review:** Request external review of completed work before merging.
  - **Branch finishing:** Decide and execute integration (merge / PR / cleanup) at completion.
  - **Vault capture:** Persist execution outcomes to vault.
- **follow_on:** `maintain` (post-build hygiene), `peer review reception` (when review comes back)

#### 13. maintain

- **Purpose:** Project hygiene — audit structural health, content drift, skill gaps, writing quality; clean up archived plans and stale memory.
- **Success:** All audits run; high-severity findings addressed; completed plans archived; stale CLAUDE.md/memory pruned. Project measurably leaner than at session start.
- **Phases:** Setup → Audit → Clean → Fix → Close
- **Key capabilities:**
  - **Session boundary:** Open/close the session (light — maintenance is bounded).
  - **Structural audit:** Verify repo structure matches conventions; converge drift.
  - **Content audit:** Read-only check of docs, code, deps for staleness or inconsistency.
  - **Skill gap audit:** Discover installed-but-unused skills and capability gaps.
  - **Writing audit:** Check writing voice and clarity in README, docs, key prose.
  - **Cleanup:** Archive completed plans, prune stale CLAUDE.md/memory, trim completed TODOs.
- **follow_on:** none (terminal — maintenance is its own loop)

#### 14. peer review reception

- **Purpose:** Receive review of your work; contextualize each point; draft response with clarity.
- **Success:** Each review point evaluated critically (not blindly agreed); action items identified; push-backs justified; response drafted in appropriate voice.
- **Phases:** Setup → Read → Evaluate → Decide → Respond
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Review processing:** Process review feedback rigorously — verify before implementing, don't blindly agree, identify what to act on vs push back on with reasoning.
  - **Response drafting:** Produce well-formatted response (email or prose) ready to send.
  - **Vault capture:** Persist decisions and response to vault.
- **follow_on:** `plan` (if review changes the plan), `execute` (if direct fixes are needed)

#### 15. call transcript analysis

- **Purpose:** Analyze a call transcript; save full transcript to location; summarize; surface action items; flag plan changes.
- **Success:** Full transcript persisted to vault/folder; key points summarized; action items listed; plan changes flagged; share-out summary ready.
- **Phases:** Setup → Save → Analyze → Summarize → Capture
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Transcript ingestion:** Read input transcript and persist full text to a durable location.
  - **Theme extraction:** Organize transcript content into themes, decisions, open questions.
  - **Summary drafting:** Produce voice-consistent share-able summary.
  - **Action item extraction:** Parse transcript for explicit and implicit action items; assign owners and timeframes where stated.
  - **Vault capture:** Persist summary and action items to vault.
- **follow_on:** `plan` (if action items change the plan), `peer review reception` (if call WAS a review), `project-manage` (push action items into the project tracker)

#### 16. project-manage

- **Purpose:** Track all plans, steps, communications, reviews, responses, and updates for a named project. Queryable shape: answer "where are we with project X?" / "send update to team" / "what's the next step for X?"
- **Success:** User has a clear answer to their project query (status / next step / drafted update); project state files reflect any new info captured during the session; share-out artifact ready if the query was an update request.
- **Phases:** Setup → Load → Respond → Capture
- **Key capabilities:**
  - **Session boundary:** Open/close the session.
  - **Project state retrieval:** Aggregate project-related artifacts for a named project — plans, TODOs, vault project files, session logs, recent commits, calls — into a coherent state read.
  - **Status synthesis:** Answer "where are we?" by synthesizing retrieved state into a narrative.
  - **Next-step decision:** Identify blockers and pick next action; problem-frame if the next step is solving something specific.
  - **Update drafting:** Produce share-able update (formatted email, prose, or terse status) appropriate to the audience.
  - **Vault capture:** Update project Status.md in vault with new state.
- **follow_on:** none typically (queryable, single-shot); chains as needed: `plan` (if next step needs re-planning), `writing` (if update grew into broader content), `peer review reception` (if responding to a review), `call transcript analysis` (if a recent call hasn't been processed)

**Note:** project-manage assumes a named project. In a single-project Kerd repo, the project name is implicit (the repo). In a multi-project setup (one user managing multiple projects in the same vault), the project name is an argument: `/kerd:mode project-manage <project-name>`. Mode-load logic resolves the name to the right vault folder / TODO.md / plans dir.

### Capability inventory (across all 16 modes)

Aggregated capability descriptions from the briefs. This is the input to the **skill assessment phase** — once mode design is complete, each capability gets matched to a skill (existing, alternative, or build candidate).

Capabilities marked `[recurring]` appear in 2+ modes — strong leverage for skill investment.

- **Session boundary** `[recurring]` — open/close session, load prior context, persist context across machines
- **Vault capture** `[recurring]` — persist session output to vault as durable record, one write per session
- **Idea exploration** `[recurring]` — open questions, force articulation, resist paraphrases
- **Web research / market research** `[recurring]` — retrieve clean external content with cited sources
- **Doc drafting / voice enforcement** `[recurring]` — produce voice-consistent prose
- **Plan production** — produce written implementation plan with verifiable steps
- **Plan-readiness check / adversarial interview** — exhaustive readiness check, axis-by-axis recitation
- **Plan execution** — execute plan step-by-step with checkpoints
- **TDD discipline** — test-driven implementation
- **Code review (request + receive)** — external review of work before merge
- **Branch finishing** — decide and execute integration
- **Goal framing / Decision framing** `[recurring]` — articulate goal, options, criteria; problem-frame when applicable
- **Synthesis** `[recurring]` — organize findings into themes, gaps, recommendations
- **Empirical primitive** — cheap, fast, ground-truth probe (domain-specific)
- **Try-matrix generation** — batch variants for spike work
- **Evidence capture** — record wins/losses with citations
- **User/persona work** `[recurring]` — persona generation, persona-driven probing
- **Adversarial mindset** — graduated probe → stress-test → adversarial pressure
- **Problem-solving framework** — Toyota 9-step (or equivalent structured framework)
- **Prospect/account research** — gather context on a sales prospect/account
- **Pipeline review** — aggregate deal state, prioritize, surface risks
- **Outreach drafting** — personalized outreach, paste-ready format
- **Call prep** — prepare for sales call, agenda, attendee research
- **Plan loading** — read existing written plan and confirm scope
- **Structural audit** — verify repo structure matches conventions
- **Content audit** — read-only check of docs/code/deps for staleness
- **Skill gap audit** — discover unused / missing skills
- **Writing audit** — voice and clarity check on existing prose
- **Cleanup** — archive completed plans, prune stale state
- **Review processing** — critical evaluation of received review feedback
- **Response drafting** `[recurring]` — well-formatted response (email or prose) ready to send
- **Transcript ingestion** — read input transcript, persist full text
- **Theme extraction** — organize transcript content into themes/decisions
- **Action item extraction** `[recurring]` — parse text for explicit and implicit action items
- **Project state retrieval** — aggregate project artifacts (plans/TODOs/vault/sessions/commits) for named project
- **Status synthesis** — synthesize state into a coherent narrative
- **Next-step decision** `[recurring]` — identify blockers and pick next action
- **Inline actions** (across multiple modes) — agent acts directly without invoking a skill: confirm idea source, name working title, generate search angles, synthesize verdict, name gap, pick follow-on, etc.

This inventory is the input to the next phase: skill assessment.

### Skill assessment phase (deferred — comes after mode design)

Once all 16 modes are spec'd in capability-only form, the next phase begins:

1. **For each capability** in the inventory above: identify which existing skill (Kerd, Superpowers, Sensei, Firecrawl, Sales suite, etc.) fulfills it. Multiple skills may be candidates.
2. **For each capability with no matching skill:** name it as a build-or-find gap. Recurring gaps are highest priority.
3. **For each existing Kerd skill:** evaluate whether any capability needs it. Skills that fulfill no capability are drop candidates.
4. **Output:** a skill-map (capability id → recommended skill + alternatives), a gap list (capabilities needing build/find), a Kerd skills disposition (keep / update / drop / move-to-kerd-skills-plugin).

This phase is **not in this design pass.** The doc captures the inventory; the assessment runs after all 16 modes are fully spec'd.

## Plan

| # | Item | Layer | Status |
|---|---|---|---|
| ~~M1~~ | ~~Add `discipline_gates` frontmatter field to mode files~~ | ~~mode~~ | **dropped** — gates fire universally via skill triggers; not per-mode |
| M2 | Author mode files for all 15 in new format (per-step Goal/Do/Don't/Exit/Produces blocks + Success section + `follow_on`). 6 rewrites, 9 new. | mode | proposed |
| M3 | Delete retired modes: deepwork, greenfield, quickfix, legal. Update any references in skills/docs. | mode | proposed |
| M4 | Skills: remove flow-level cross-references (skills are atomic). Keep structural primitives (switch → kivna save). | all skills | proposed |
| **M9** *(new)* | New skill: `email-writer` (kerd:email or kerd:compose) — domain-agnostic email iteration + paste-ready formatting | skill | proposed |
| **M12** *(new)* | Verify Claude Code plugin system supports cross-plugin skill invocation (5-min test) — gates the plugin split | plugin | proposed |
| **M13** *(new)* | Plugin split: extract 9 skills (switch, dian, kivna, interrogate, skriv, tend, slainte, trim, lorg) from Kerd to `kerd-skills` plugin. May bundle some back if OOB UX requires. | plugin | proposed (gated by M12) |
| ~~M5~~ | ~~Extend `hooks/session-start.sh`: prompt for mode when no active mode~~ | ~~hook~~ | **dropped** — switch-in handles mode entry; hook stays silent-when-quiet |
| M6 | Update `/kerd:switch in` step 10: list modes by category, prompt for selection (or `free`). Replaces existing "Offer dian" prompt. | switch | proposed |
| M7 | Add `free` as a pseudo-mode entry in `.active-modes` semantics; `switch.out` clears it. | mode + switch | proposed |
| M8 | Add `follow_on` frontmatter field to mode file format. Mode skill prompts at completion. | mode | proposed |

### Sequencing (proposed)

1. **Spec lock** — finalize this doc (mode design complete, other skills reviewed and items added)
2. **M7, M8** — small mechanical changes, low risk
3. **M2** — biggest item; rewrite modes one at a time, starting with the most-used
4. **M6** — switch.in update (depends on M2 modes existing in new format)
5. **M3** — new modes for missing work shapes
6. **M4** — skill cleanups (depends on M2 establishing the layering rule)

Version bump per Kerd's release checklist:
- M6, M7, M8 → MINOR (changed behavior)
- M2 → MINOR per mode-batch, or one MINOR for the whole rewrite
- M3 → MINOR (new mode files)
- M4 → MINOR (skill behavior change)

## Plugin split (provisional lock)

Going forward, **Kerd plugin is modes-only**. Skills live in a separate plugin (`kerd-skills` provisional name). This lands the open-source positioning shift: Kerd is the workflow framework; skills are interchangeable implementations.

### Provisional shape

**Kerd plugin (modes-only):**
- `modes/` directory — 16 mode files
- `kerd:mode` — the runner skill
- SessionStart hook
- `.claude-plugin/` manifest

**Kerd-skills plugin:**
- 9 skills extracted from current Kerd: `switch`, `dian`, `kivna`, `interrogate`, `skriv`, `tend`, `slainte`, `trim`, `lorg`
- Plus the new `email-writer` skill (M9)
- Plus future capability-fill skills (e.g., persona-work, project-state if built)

### Caveat

We may bundle some skills back into the Kerd plugin if "out of the box" UX requires it. For example, if installing only Kerd modes leaves the user unable to run any mode without separately installing kerd-skills, that's friction. A small core (e.g., `switch` + `kivna`) may colocate to keep modes runnable.

### Gate

M12 (verify cross-plugin skill invocation works in Claude Code's plugin system) gates the split. If cross-plugin calls don't route, the split is forced toward bundled-by-necessity rather than chosen-by-design.

### Migration absorbs rename

The plugin split and the rename (R1–R4) are one migration. Single v1.0.0 release. See "Skill renaming + plugin move" below — the section is now combined.

## Skill renaming + plugin move (combined v1.0.0 migration)

Captured separately because it's breaking and needs its own care.

The five Gaelic-named skills should rename to something more obvious to new users. Kerd stays as the *plugin family* prefix; the modes-only plugin keeps the `kerd:` namespace for the mode skill.

| Current | Proposed | Plugin after move | Notes |
|---|---|---|---|
| `kerd:dian` | `kerd-skills:session` | kerd-skills | "session discipline" matches the skill's intent |
| `kerd:kivna` | `kerd-skills:vault` | kerd-skills | vault management is the actual function |
| `kerd:skriv` | `kerd-skills:write` | kerd-skills | TBD — could collide semantically with other plugins' write skills |
| `kerd:slainte` | `kerd-skills:audit` | kerd-skills | audit captures the read-only health-check shape |
| `kerd:lorg` | `kerd-skills:discover` | kerd-skills | matches the existing trigger keyword |
| `kerd:tend` | `kerd-skills:tend` | kerd-skills | already English; just moves plugin |
| `kerd:trim` | `kerd-skills:trim` | kerd-skills | already English; just moves plugin |
| `kerd:switch` | `kerd-skills:switch` | kerd-skills | already English; just moves plugin |
| `kerd:interrogate` | `kerd-skills:interrogate` | kerd-skills | already English; just moves plugin |
| `kerd:mode` | `kerd:mode` | kerd | runner stays in Kerd (the modes plugin) |

### Migration concerns

- Every `/kerd:<old-name>` reference in skills, hooks, README, modes, vault, session logs, MEMORY.md, TODO.md needs updating.
- Major version bump (v0.39.0 → v1.0.0).
- Backwards-compat aliases worth investigating before flipping (Claude Code skill aliases — feasibility unconfirmed).
- Sequenced **after** the architecture work in this doc lands. Don't bundle.

| # | Item | Status |
|---|---|---|
| R1 | Confirm Claude Code supports skill aliases (or commit to a hard cutover) | research |
| R2 | Rename 5 Gaelic skills + update every reference in repo | proposed |
| R3 | Update vault Status.md / Lorg Report and any active-modes entries | proposed |
| R4 | v1.0.0 release with rename | proposed |

## Mode design — resolved decisions

All five originally-open questions are now resolved.

- **Conditional steps in modes** → **linear only.** No `if X then A else B`. Branching shapes go in separate modes.
- **Mode composition** → **no composition.** One mode cannot call another. Copy-paste between modes is cheaper than composition complexity.
- **`.active-modes` format** → **stay terse.** Tracker stays short; the mode file is the spec. `.active-modes` lists step id, skill invocation, label, status — no Goal/Do/Don't/Exit content.
- **User customization at start of mode** → **stay step-level.** Don't lose granularity by moving to phase-level.
- **What "free" means** → **no orchestration; gates still fire.** Resolved by the three-layer reframe (gates live at the global skill-trigger layer, fire universally regardless of mode).

**Mode design is closed.** Implementation can proceed against this spec.

## Other skills (deferred)

These get full 5-question reviews after mode design is complete. Items added to the plan as decisions land.

- `kerd:dian` — session shell. Verification-gate duplicate fix and three multiple-choice prompt fixes already identified (carry over from earlier in conversation).
- `kerd:switch` — boundary ops. Step-10 update from M6 already identified.
- `kerd:interrogate` — plan-readiness. May need adversarial-level dial review.
- `kerd:kivna` — knowledge plumbing.
- `kerd:skriv` — human writing voice. Pairing rule with `elements-of-style:writing-clearly-and-concisely` open.
- `kerd:tend` — repo structural health.
- `kerd:slainte` — read-only audit. Overlap with tend's audit half open.
- `kerd:trim` — token cleanup.
- `kerd:lorg` — skill discovery.
- Adjacent plugins (claude-md-management, episodic-memory, elements-of-style, pr-review-toolkit, commit-commands) — referenced from modes (M2) but not redesigned by this effort.
- Superpowers skills — referenced from modes; not redesigned by this effort (different plugin).
