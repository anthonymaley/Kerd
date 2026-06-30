---
name: interrogate
description: "Use when the user says 'interrogate', 'interview me', 'walk me through this plan', 'stress-test this idea', 'help me figure out if this is viable', or has a plan/idea they want exhaustively interrogated across every viability axis (technical, business, legal, operational) until a co-signed readiness document is produced. Produces a markdown document at docs/interrogations/. Does NOT produce the implementation plan itself — produces readiness."
---

# Interrogate (Plan Readiness)

Interview the user relentlessly about every aspect of a plan or idea until shared understanding is reached and co-signed. Produces a comprehensive plan-readiness document covering all viability axes (technical, business, legal, operational), with mutual sign-off as the exit ritual.

This skill is the countermeasure to the convergence pull in normal brainstorming — verbose framing, premature multiple-choice, unilateral declarations of "done." It cannot be ratified with a yes/no.

## Invocation

`/kerd:interrogate` start from zero — agent asks "what's the idea?"
`/kerd:interrogate <plan-ref>` interrogate an existing plan

`<plan-ref>` is a file path, an idea description, or a reference like "current TODO" or "the latest session log."

## Entry Paths

**Plan-ref path.** Read the plan at the given reference. Propose the viability axes you infer from the plan content (not a mandatory exhaustive checklist — inferred from the plan itself). Ask the user to prune: which axes to keep in scope, mark out-of-scope, or defer up front. Then enter the interview loop.

**Zero path.** Ask one open question — *"what's the idea?"* — and build the document from blank. Axis identification happens organically as ideas surface. The universal core (see Default Axis List below) always applies.

Both paths converge on the same artifact (a co-signed plan-readiness document) under the same exit rules.

## Interview Discipline

These rules govern every turn during a session. They are not aspirational — they are the structural floor.

1. **One question per turn.** No "Question 1 of N." No bundled questions. Each turn surfaces exactly one open thread.

2. **No multiple choice unless genuinely discrete and small.** Default open-ended. Force articulation, not selection. Multiple choice is a cop-out that lets the user agree without thinking.

3. **No extrapolation.** Do not sketch the plan from partial answers. No *"so it sounds like you want X, Y, Z."* That pre-shapes the design before understanding is reached.

4. **Response shape constrained.** Your response in the interview = at most one sentence of acknowledgment + the next question. No insight blocks, no padding, no *"let's think about."* Verbosity is a tell of lack of understanding; the discipline forbids it during the interview itself.

5. **User-veto on stop.** Never declare the session done. The interview continues until the user explicitly says stop. You *may* propose intermediate transitions — like *"I've exhausted my known unknowns; ready to enter recitation?"* — but the user can veto any proposal to keep interviewing.

6. **Three "done" gates, all required for sign-off.**
   - **(a)** You have exhausted your known unknowns AND the document passes a structural check before recitation can be proposed. The structural check requires every in-scope axis to have:
     - at least one entry in **Known** or **Decision**
     - explicit **Viability conditions**
     - **Evidence / basis** for material claims (decisions, viability conditions)
     - **Unknown** state matches **Status**:
       - if `status: viable`, **Unknown** must be empty (no open questions remain)
       - if `status: not-yet-viable`, **Unknown** must be non-empty (the open questions are why it's not yet viable)
       - if `status: blocked`, **Unknown** may be empty or non-empty, but the blocker must be named in **Viability conditions**
       - if `status: deferred`, **Unknown** may be in any state; the revisit trigger is in the top-level Deferred list

     If the document fails the structural check, continue interviewing on the failing axes — no recitation proposal. If it passes, *propose* entering recitation. User can veto ("more to discuss") to keep interviewing.
   - **(b)** User has no more answers, requirements, or ideas to share.
   - **(c)** Recite the plan back **axis-by-axis**; user confirms each axis individually. Whole-document recitation is rejected as the easy-ratification trap this skill is designed to avoid.

7. **Tree-aware ordering.** Decisions that constrain other decisions get resolved first. Within each decision, depth-first: resolve fully — including per-axis viability where the decision affects an axis — before sliding sideways to the next branch.

8. **Adversarial lean — graduated and user-dialable.** Default trajectory follows saturation:
   - **Gather** (early) — open questions, no challenges. *"Tell me about X."*
   - **Probe** (mid) — drill into vagueness, ask for specifics. *"What does that mean concretely?"*
   - **Stress-test** (late) — challenge claims, ask for evidence. *"How do you know that's true?"*
   - **Adversarial** (deep) — actively look for holes. *"What would have to be different for this not to work?" / "What's the strongest objection?"*

   User can dial level at any moment in either direction: *"go harder now"* / *"ease off, still ideating"* / *"stay at probe for this axis."* Track the current level in the document's `adversarial-level` frontmatter field.

**Pause/resume.** Sessions can run long. The document is persistent state — leaving and returning resumes from the document, not from conversation memory. Session state lives in document frontmatter (see Document Structure section). On resume, restate the level and target, then **re-ask the last unanswered question verbatim** from the `last-question` frontmatter field — e.g. *"Resuming at stress-test on Security. Last question: [verbatim]."* — and stop. The user can ask for refinement if needed; do not offer a meta-choice. The unanswered question is the active edge; re-present it, nothing more.

## Document Structure

The output is a markdown file at `docs/interrogations/YYYY-MM-DD-<topic>.md`. Create the `docs/interrogations/` directory on first use if it doesn't exist. Update the file incrementally after each meaningful axis exchange — never reconstruct it wholesale at the end. The user can read it at any point.

### Outline

```
[frontmatter]
## Scope
  ### In scope
  ### Out of scope
## Deferred
## [Per-axis sections, one per in-scope item]
```

### Frontmatter

```yaml
---
created: <ISO timestamp at session start>
last-updated: <ISO timestamp of most recent update>
status: draft           # draft | signed
topic: <short human-readable topic name>

# Session state — present while status: draft, frozen or removed at sign-off
current-axis: <axis name under interview>
current-thread: <sub-decision being resolved, or empty>
last-question: <verbatim text of the last question asked>
adversarial-level: gather   # gather | probe | stress-test | adversarial
recitation-status:
  <axis-name-1>: pending     # pending | recited | confirmed | pushed-back
  <axis-name-2>: pending

# Sign-off fields — set at sign-off, absent before
# signed-at: <ISO timestamp>
# signers:
#   user: <name>
#   agent: <model-id>
---
```

`recitation-status` is initialized to `pending` for every in-scope axis as soon as the axis is added; transitions to `recited` after recitation, then `confirmed` (user accepted) or `pushed-back` (user pushed back; that axis re-enters interview). At document birth before any axes exist, the map is `{}`. Once axes are added, every in-scope axis must have an entry — no missing keys.

### Scope (defines project boundaries)

Scope is a boundary concept, not a tracking concept. What's in *and* what's out together define the project. Both are scope.

- **In scope** — list of axes/items the plan covers. This list is also the index — each entry has a per-axis section below.
- **Out of scope** — list of axes/items the plan deliberately excludes. Each: item + one-line reason. These items do not have per-axis sections; they live only in this list.

### Deferred (separate from scope — tracks timing, not boundaries)

Items in scope but pushed to a later round. Each: item + reason + revisit trigger (timeline, dependency, or condition that would reactivate it). If an item was deferred mid-interview after content was gathered, it retains its per-axis section with `status: deferred` AND appears in this list.

### Per-axis sections

One section per in-scope item, in the order they appear in the In Scope list. Each has six fields:

- **Known** — what has been established about this axis (general context and facts)
- **Unknown** — open questions still on the table
- **Evidence / basis** — for each item in Known and each Decision, the source: a fetched doc, a user statement, a tested observation, an explicit "from training data; may be outdated." Viability conditions built on unsupported assumptions are surfaced as such, not laundered into Known.
- **Decision / current position** — crisp resolved decisions for this axis (e.g. *"Storage: local markdown files under `docs/interrogations/`"*). Distinct from Known. A decision is something the plan has *committed to*, not just something the plan *knows*.
- **Viability conditions** — what must be true for this axis to be considered viable
- **Status** — `viable` | `not-yet-viable` | `blocked` | `deferred`

Status semantics:
- `viable` — known enough, with stated viability conditions and evidence supporting them. The plan can proceed on this axis.
- `not-yet-viable` — open unknowns remain, but no known blocker. More interview is needed.
- `blocked` — a known condition currently prevents viability. The blocker is named in Viability conditions; status stays `blocked` until it's resolved.
- `deferred` — intentionally postponed with a revisit trigger. Item appears in the top-level Deferred list with its trigger.

`out-of-scope` is not a valid status value. Out-of-scope items don't have per-axis sections.

### Canonical template

A new interrogation document begins as:

```markdown
---
created: 2026-05-02T18:30:00Z
last-updated: 2026-05-02T18:30:00Z
status: draft
topic: <short human-readable name>
current-axis: <axis-name>
current-thread: <sub-decision being resolved, or empty>
last-question: <verbatim text of last question>
adversarial-level: gather
recitation-status:
  <axis-name-1>: pending
  <axis-name-2>: pending
---

# Interrogation: <topic>

## Scope

### In scope
- <axis-name>
- <axis-name>

### Out of scope
- <item> — <one-line reason>

## Deferred
- <item> — <reason> — revisit when <trigger>

## <Axis name>

### Known
- <fact / context>

### Unknown
- <open question>

### Evidence / basis
- <fact> — <source>

### Decision / current position
- <crisp resolved decision>

### Viability conditions
- <what must be true>

### Status
not-yet-viable
```

The template is the structural floor. Documents that do not match this shape break the resume / structural-check / recitation logic.

**Zero-path initialization.** The template above shows a document with axes already established. In zero-path entry, the initial document begins before any axes exist: `current-axis` is empty, the In Scope list is empty, and `recitation-status` is `{}`. As the interview proceeds and axes get added, they appear in the In Scope list and `recitation-status` simultaneously. `current-axis` becomes populated as soon as the first axis is established and the interview moves into it.

## Recitation Gate

Before sign-off can occur, do a final recitation pass. Read each axis back in summary form and ask the user to confirm — **axis by axis, not all at once**. Whole-document recitation is the easy-ratification trap this skill is designed to avoid.

For each axis:
1. Update `recitation-status[axis]` to `recited` in frontmatter.
2. Present the summary: Decision, Viability conditions, Status, and one-line gist of Known.
3. Ask: *"Does this read right for [axis]?"*
4. If user confirms: set `recitation-status[axis]: confirmed`. Continue to next axis.
5. If user pushes back: set `recitation-status[axis]: pushed-back`. Re-enter the interview for that axis. Graduated lean continues from where it was. Loop until user vetoes the re-entry, then re-recite that axis. Repeat until all axes are `confirmed`.

Only after every in-scope axis is `confirmed` does sign-off become possible. This is gate (c) of the three "done" gates — the demonstration of understanding, not its declaration.

## Sign-off Ritual

Once recitation passes for all axes:

1. Present the document with timestamp and signer placeholders ready.
2. Ask the user to type `signed` in chat to sign. (Commit-message signing was considered and rejected — it introduces git-state ambiguity. v1 keeps sign-off in-conversation.)
3. On `signed`: update frontmatter:
   ```yaml
   status: signed
   signed-at: <ISO timestamp>
   signers:
     user: <user name>
     agent: <model id, e.g. claude-opus-4-7>
   ```
4. **Move session state into `final-session-state` block.** Remove the active resume fields (`current-axis`, `current-thread`, `last-question`, `adversarial-level`, `recitation-status`) from the top level of frontmatter. Add them as a snapshot under a `final-session-state:` key, preserving auditability without leaving active resume hooks on a signed document. Example post-sign-off shape:

   ```yaml
   ---
   created: 2026-05-02T18:30:00Z
   last-updated: 2026-05-02T20:15:00Z
   status: signed
   signed-at: 2026-05-02T20:15:00Z
   signers:
     user: <user name>
     agent: <model id>
   topic: <topic>
   final-session-state:
     current-axis: <last axis>
     current-thread: <last sub-decision>
     last-question: <verbatim>
     adversarial-level: <last level>
     recitation-status:
       <axis-1>: confirmed
       <axis-2>: confirmed
   ---
   ```

The document reads "complete as of [signed-at]," not eternally. Future revisits create new sign-off entries with new timestamps; the original signature is preserved as a point-in-time record.

## Composition with Kerd

`/kerd:interrogate` is callable from anywhere — inside a conductor session, inside a mode, or standalone.

- **Invoked mid-conductor:** return to conductor after sign-off. The signed interrogation document is referenced from conductor's plan phase.
- **Invoked mid-mode:** return to the mode after sign-off.
- **Invoked standalone:** exit cleanly after sign-off. No further workflow assumed.

If the user says "stop" without sign-off, save the document as `status: draft` and exit. Re-invoking with the same plan-ref or topic resumes from the draft via the pause/resume mechanism in the Interview Discipline section.

## Default Axis List

A small **universal core** applies to every interrogation regardless of domain:

- **Scope viability** (whether the boundaries already declared in the top-level Scope section are coherent and complete — distinct from the structural Scope section)
- **Users / stakeholders** (who is this for; who has a say)
- **Value** (why this is worth doing; what changes if it works)
- **Constraints** (what must hold; what cannot change)
- **Risks** (what could fail; what consequences if it does)
- **Dependencies** (what this requires from outside the plan)
- **Overall viability** (the cross-axis "what must be true" set — distinct from the per-axis Viability conditions field)

**Domain-specific starter sets** layer on top, proposed by you based on what the plan-ref or zero-mode discussion reveals:

- *Software engineering plans:* technical design, data model, security, performance, testing, deployment.
- *Business / product plans:* business case, ROI, marketing, sales, pricing, competitive landscape.
- *Investment / financial plans:* due diligence, ROI, audit, compliance, term sheet, exit conditions.
- *Legal / contract plans:* compliance, privacy, data protection, jurisdiction, liability.

The user prunes any of these via out-of-scope/defer. Full-list-by-default is rejected as noise-generating.

## What This Skill Does Not Do

- **Does not produce the implementation plan itself.** This skill produces *readiness*. After sign-off, the user transitions to `superpowers:writing-plans` (or another planning skill) — explicitly outside the interrogate session. Boundary kept to prevent design synthesis from sneaking in too early.
- **Does not auto-detect sign-off.** You may *propose* entering recitation when known unknowns are exhausted, but you never declare the session over. User-veto on stop is absolute through to the final ritual.
- **Does not use insight blocks, structured framing, or explanation during interview.** Those belong outside interrogate sessions. During interrogation, you are question-shaped only.
- **Does not support multi-user sign-off in v1.** The signers map supports one user + one agent. Future versions may extend.
- **Does not enforce a mandatory exhaustive axis checklist.** The universal core always applies; domain-specific axes are proposed and pruned by the user.
