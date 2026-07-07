---
name: conductor
description: "Use when you need structured session discipline — frame a task, get a plan approved before building, and execute with verification — or when the user says 'conductor', 'session', 'let's get structured', 'delegate', 'fable on', 'fable off', or wants to plan and track a focused work block. Runs inside an already-open session (switch-in loads context first). Provides a plan-execute-close protocol, with optional delegated execution toggled by `/kerd:conductor fable on|off` (default off): with it on, an expensive model (Fable) writes a detailed spec and hands the mechanical build to cheaper models (in-session subagents or a fresh session)."
---

# Conductor (Session Discipline)

The session conductor — keeps one session in tempo and coherent from open to close, the way an orchestra conductor holds a single performance together. (Renamed from `dian`, which was too opaque to signal the role.)

A protocol for staying focused within a session. Conductor does not touch git boundaries (pull/push). That's switch's job. Conductor keeps you on track once you're working.

## Usage

`/kerd:conductor` run a session inline on the active model (the default)
`/kerd:conductor fable on` turn on **delegated execution** for this session (spec + delegate the build to cheaper models)
`/kerd:conductor fable off` turn delegated execution back off (inline)

The `fable` toggle is an explicit assertion that you're on a top-tier model (Fable) and want to spend those tokens on planning while a cheaper model does the build — conductor never auto-detects your model. It is **off by default** and **session-scoped**: the state rides the conductor line in `kivna/.active-modes` and clears at close-out, so each new conductor session starts inline unless you turn it on. Flip it on the sessions where you have Fable credits; leave it off (or you're out of credits and on a normal model) and conductor plans and builds inline as before. See [Delegated execution](#delegated-execution--the-spec-is-the-contract) under Plan.

## Mode Markers

Conductor is a modal skill. It runs across multiple responses. Announce the current phase so the user always knows what's active.

**On every phase transition**, output a marker on its own line at the top of your response:

- `[conductor: orient]` reading context, summarizing state
- `[conductor: plan]` proposing session plan
- `[conductor: execute]` working through tasks
- `[conductor: execute step N/M]` working a specific plan step (fires at step transitions within execute)
- `[conductor: execute step N/M · delegate→<model>]` a delegated step dispatched to a cheaper model (delegated sessions only)
- `[conductor: close-out]` updating docs, running checks
- `[conductor: closed]` session complete (final marker, then done)

**Why a step-boundary marker within execute:** phase markers fire 3-4 times per session — too coarse to gate claim-level failures (the Claim Discipline problem — gates asserted once don't bind the 50th claim). Step-boundary markers fire 5-30 times per session at the granularity where confident-wrong assertions actually happen. Each step marker is a reminder to re-engage the verification gate, not boilerplate. Don't re-emit the marker mid-step; only at the actual step transition.

**State file:** When entering a phase, write the current phase to `kivna/.active-modes`. When closing out, remove the conductor line from the file (or delete the file if it's the only entry). This lets `/kerd:switch in` report active modes and hooks surface reminders.

Format of `kivna/.active-modes` — conductor owns one line only:
```
conductor: <phase>
```

Example: `conductor: execute`. When delegated execution is toggled on (`/kerd:conductor fable on`), append ` [fable]` so the toggle survives across the session's responses: `conductor: execute [fable]`. This is the sole record of the toggle state — it is session-scoped and clears when the line is removed. Remove the line entirely when closing out (don't write `conductor: closed`). Never touch other skills' lines in this file.

## The Protocol

### 1. Orient

Output `[conductor: orient]` at the top of your response.

Conductor runs inside an already-open session. Loading context is switch-in's job, not conductor's, so orient is conditional:

**Warm path (the common case — switch-in already ran this session):** Don't re-read anything. Switch-in just loaded `CONTEXT.md`, `TODO.md`, the newest session log, and active modes. Confirm the current state in a line or two from what's already in context, then move to planning. Re-reading what switch-in just read is wasted work.

**Cold path (conductor invoked with no switch-in this session):** Do a light orient — read only `CONTEXT.md` (`## Where We Are`) and `TODO.md` (`## Now`). That's enough to plan. Don't sweep the playbook, session logs, and progress files; that's switch-in's read. If you need the full picture, run `/kerd:switch in` first.

**Mode awareness:** Read `kivna/.active-modes`. If a mode is active, report it: what mode, which step, and the session instruction if one was set. Conductor operates within the mode's scope. If the mode says "focus on pricing strategy only," conductor's plan respects that constraint. If no mode is active, proceed normally.

**Pre-flight inventory:** Ask the user for anything execution will need that isn't already in the repo: credentials/access not stored locally, sample inputs not in TODO.md, scope limits not in CLAUDE.md, hardware/environment state, fixtures or test data. Trickle-in friction (each missing input becomes a stop-and-ask round mid-execute) is 5-10x more expensive than collecting upfront. One round of questions now prevents many later. If the inventory is genuinely complete, say so explicitly and skip.

**Consistency sniff test:** Quick cross-check against what's in context — does CLAUDE.md or the playbook reference files, conventions, or a tech stack that no longer match reality? Flag contradictions before planning. This is a light pass; the deep audit is `/kerd:slainte`.

Summarize the current state for the user, including any inconsistencies found, active mode context, and inventory gaps surfaced.

### 2. Plan

Output `[conductor: plan]` at the top of your response.

#### Critical review

Before writing the plan, surface doubts and unresolved risks. If something about the task feels underspecified, contradictory, or risky, say so now. Do not hide concerns to appear confident. Do not guess or infer context. It's cheaper to spend two minutes clarifying than to build the wrong thing.

**Challenge yourself on:**
- Do I actually understand what the user wants, or am I filling in gaps with assumptions?
- Are there dependencies between tasks that affect the order?
- Is anything in the plan vague enough that I might interpret it differently than the user intended?
- What could go wrong, and how will I catch it?
- If a plan step predicts an outcome ("this will fix the issue", "this approach should scale", "this is the right pattern"), what is the prediction based on? Cite the source — prior session, doc, tested precedent, code reference. If no source exists, downgrade the prediction language to "expected outcome — to be verified after execution".

Ask clarifying questions about anything ambiguous. Push back on things that don't make sense.

#### Task framing

Before planning implementation, decompose the request into one or more task candidates. For each candidate, write:

- **Scope:** what is included (and what is explicitly out)
- **Acceptance criteria:** what must be true when the task is done
- **Files likely touched**
- **Verification:** how we prove it worked (command to run, output to check, behavior to observe)

Ask the user to approve the task boundaries before writing the detailed plan. Default to one task per conductor session. If the user's request naturally splits into multiple tasks, present them as candidates and ask: tackle all in this session, or pick one?

If the output from a task is not good enough after execution, the right move is to refine the task framing (scope, acceptance criteria) and restart with a fresh conductor session rather than digging deeper into muddy context.

#### Write the plan

Propose a session plan based on the approved task framing. Each step must be concrete and testable:

- **What:** specific action with file paths
- **Verify:** how to confirm it worked

Ban vague plan items. "Implement feature X" is not a plan step. "Write the handler in `src/api/handler.ts` that accepts POST requests and returns 201" is. Every step should be small enough that you can verify it independently before moving on.

If a mode is active, scope the plan to the mode's current step and instruction. Don't plan beyond the mode's scope.

Write this into TODO.md's `## Now` section with today's date — overwrite the section in place; `## Now` holds the current focus, and during a conductor session the focus is the plan. Wait for user approval before executing. Do not proceed until the user confirms the plan. A good plan prevents rework.

#### Delegated execution — the spec is the contract

Conductor's default is **inline execution**: the session model plans and does the work itself, and the plan lives in TODO.md `## Now`. **Delegated execution** — spending an expensive top-tier model's (Fable's) tokens on the plan and handing the mechanical build to a cheaper model — is **off by default** and turned on with the `fable` toggle (see [Usage](#usage)):

- `/kerd:conductor fable on` — enable it for this session.
- `/kerd:conductor fable off` — disable it (the default; inline on the active model).

The toggle is an explicit assertion, not an auto-detection — conductor does not guess your model. Turn it on the sessions where you're on Fable and want the token economics; leave it off (or you're out of Fable credits and running on a normal model) and conductor plans and builds inline exactly as it always has. Record the toggle state on the conductor line in `.active-modes` (`conductor: <phase> [fable]`) so it holds across the session. When the toggle is **off**, skip the rest of this section — write the plan into TODO.md `## Now` as above and execute inline.

When the toggle is **on** and the task decomposes into mechanical steps, the plan is not a lean TODO stub — it is a **spec file**, the contract handed to the implementer:

- **Location:** `docs/plans/YYYY-MM-DD-<slug>-spec.md`. TODO.md `## Now` shrinks to a one-line pointer at the spec plus the step checklist. The spec file is a committed artifact — switch picks it up at the boundary.
- **Executor tag per step:** mark each step `[fable]` (hard, architectural, or judgment-heavy — the planning model does it inline during execute) or `[delegate]` (mechanical — handed to a cheaper model). The planning model assigns the tags; the user approves them at the plan gate alongside the plan itself. Two buckets only; the actual implementer model (Sonnet, Haiku) is chosen per `[delegate]` step at dispatch time.
- **The bar for a `[delegate]` step is higher than a normal plan step.** It must be implementable by a model that never saw the planning model's reasoning: exact files and paths, the function/type signatures or interfaces to add or change, the *why* behind any non-obvious choice (so the implementer doesn't re-derive intent and drift), and a verification command with its expected output. A vague spec produces a confidently-wrong implementation from a cheaper model with no recourse — spec quality *is* the safety mechanism, and it is the entire reason the expensive planning tokens are worth spending.

Write the spec, write the pointer into TODO.md `## Now`, and wait for approval — the same gate as inline. The user approves the spec, the tags, and the boundaries together before any execution begins.

### 3. Execute

Output `[conductor: execute]` at the top of your response when entering this phase.

Do the work. Stay focused on the plan.

#### Dispatch mode (delegated sessions only)

For an inline session, skip this — just work the plan. For a delegated session (a spec file with `[fable]`/`[delegate]` tags), pick the dispatch mode with the user at execute entry:

- **In-session subagents (default).** Work `[fable]` steps inline. For each `[delegate]` step, spawn a subagent on a cheaper model (Sonnet for standard implementation, Haiku for trivial edits) via the Agent tool with its `model` set, handing it *that step's spec slice* — scope, files, signatures, the why, and the verify command. The subagent returns its result plus evidence (command output, diff summary). You do not re-do the work — you **review the returned evidence against the step's acceptance criteria** (the verification gate below, applied to the subagent's output). This keeps the expensive model in the judgment loop and out of the mechanical grind. Emit `[conductor: execute step N/M · delegate→<model>]` at each dispatch.
- **Handoff to a fresh session.** Finish the spec and stop. Tell the user to open a new session on a cheaper model pointed at `docs/plans/YYYY-MM-DD-<slug>-spec.md`; that session executes every step and self-verifies via the spec's built-in verify commands. The planning model spends zero tokens on the build. Use this when the build is long enough that even orchestration tokens on the expensive model aren't worth it.

Either way the spec is the contract and the verification gate still governs "done" — the only question is who runs the steps. If a subagent's returned evidence fails the acceptance criteria, that counts as a failed attempt under the 3-fix limit: refine the spec slice and re-dispatch, don't silently accept muddy output.

#### Verification gate

After each task, verify it with evidence before claiming it's done. No exceptions.

1. **Identify** the check: what command, file read, or test confirms this task worked?
2. **Run** it. Actually run it. Don't assume.
3. **Read** the output. Look at what came back.
4. **Confirm** the claim: does the evidence support "this task is done"?

Only then mark the task complete. If you catch yourself thinking "should work", "probably fine", or "seems good" without evidence, stop. Run the check.

#### Strong-language gate (claim-formation)

The verification gate above covers "done" claims at end-of-step. The same discipline applies to claims made *during* a step. Before tagging anything with "verified", "fixed", "working", "confirmed", "the right approach", "the only way", "impossible", "always", "never" — or asserting platform/library/API specifics: require evidence in this loop iteration (a check run, an output read, a doc cited, a source URL). Without those, downgrade to "added but not yet verified", "the evidence I have suggests", or "from training data; may be wrong". Each external-system claim must carry a "verified by [URL/doc]" tag.

This mirrors the Claim Discipline some users keep in a global CLAUDE.md; it's restated here so conductor enforces it even in projects without one. It applies at the moment of writing the assertion within execute, not deferred to end-of-step. The verification gate is a backstop; this gate is the primary line.

#### 3-fix limit

If a task isn't working after 3 attempts, stop. Do not attempt fix #4. Instead:
- Summarize what was tried and why each attempt failed
- Surface the problem to the user
- Ask whether to continue with a different approach, skip the task, or rethink the plan

Three failed fixes usually means the approach is wrong, not the execution. If the task framing itself was the problem (scope too broad, acceptance criteria unclear), suggest refining the task and restarting with a fresh conductor session rather than continuing in degraded context.

#### Scope creep

If something comes up that isn't in the plan, stop working on it immediately. Add it to TODO.md backlog. Do not continue on the tangent. Do not "just quickly" do it. Return to the current plan step. The user can reopen the plan if the new work is more important.

#### Decision recording

When a significant decision is made during execution (architecture choice, rejected approach, key trade-off), record it in `CONTEXT.md` immediately — `## Key Decisions` for what was decided and why, `## Open Questions` for what surfaced but wasn't resolved. Don't defer to close-out. Decisions lose their reasoning if you wait.

Do not write to `kivna/sessions/` during execution. Switch owns session log creation at the git boundary. Conductor's decisions accumulate in CONTEXT.md and flow into the session log when switch runs.

#### Docs travel with code

If a task changes behavior, update the affected docs (README, playbook, CLAUDE.md) in the same commit. Don't defer doc updates to close-out. No commit should leave docs inconsistent with code.

#### No mid-session vault writes

Work accumulates in repo-side files (TODO.md) during execution. The vault gets one clean update at close-out. This keeps the vault lean and searchable: one session, one update.

### 4. Close Out

Output `[conductor: close-out]` at the top of your response.

Conductor closes the *work*, not the *session boundary*. Boundary operations — session log, vault save, commit, push — belong to switch. Keep conductor's close-out short:

1. **Update TODO.md and CONTEXT.md**: remove completed tasks from TODO, add new ones discovered during work, then overwrite `## Now` to forward-only state (what's next, a few lines — the completed record is the session log switch writes at the boundary). Record any *unresolved* decisions or questions in CONTEXT.md (`## Key Decisions` / `## Open Questions`). Apply Claim Discipline to summary text — don't claim "we verified X" unless we did; downgrade to "tested with Y; Z untried" when alternates exist; don't promote provisional findings to canonical without the survival test.
2. **Doc impact**: docs should already be current (docs travel with code, see Execute). Confirm nothing was missed against the CLAUDE.md Doc Impact Table if one exists. Don't carry doc updates into the boundary.
3. **Run checks**: run the project's build/test command if one exists. Do not close out with failing tests.
4. **Mode-aware completion**: if a mode is active, do NOT suggest the session is done unless the mode flow is also complete. Conductor may be one step in a larger mode flow. After conductor's close-out, control returns to the mode for the next step. If no mode is active, this is the natural end point.
5. **Clear the conductor marker**: remove the conductor line from `kivna/.active-modes`. Output `[conductor: closed]` as the final marker. Never touch the mode line — mode owns its own state.

Then hand off: tell the user to run `/kerd:switch out` to write the session log, save the vault, and commit. Conductor does not do the boundary, and does not call `/kerd:kivna save` — switch owns the vault write now.

## Principles

- **No git boundary ops.** No `git pull`, no `git push`. Use `/kerd:switch` for that.
- **Evidence before claims.** Every "done" must have a check that was run, output that was read, and a conclusion that follows.
- **Hard stop on scope creep.** Out-of-plan work goes to backlog. No exceptions without reopening the plan.
- **Three fixes, then escalate.** Don't thrash. Surface the problem.
- **Docs travel with code.** If you change behavior, update the docs in the same commit.
- **Conductor doesn't own the boundary.** No git pull/push/commit, no session log, no vault save. Work accumulates in TODO.md and decisions in CONTEXT.md during the session; switch writes the session log, saves the vault, and commits at the boundary.
- **The spec is the contract.** In a delegated session the planning model's (Fable's) job is a spec complete enough that a cheaper implementer never re-derives intent. Spec quality is what makes delegation safe — a vague `[delegate]` step produces a confidently-wrong build with no recourse. Spend the expensive tokens on the spec, not the grind.
