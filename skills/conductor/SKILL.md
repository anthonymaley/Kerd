---
name: conductor
description: "Use when you need structured session discipline — frame a task, get a plan approved before building, and execute with verification — or when the user says 'conductor', 'session', 'let's get structured', or wants to plan and track a focused work block. Runs inside an already-open session (switch-in loads context first). Provides an orient-plan-execute-close protocol. Coordinates four roles: you compose the intent, a top-tier model is called as a subagent to write the spec and leaves, the session model conducts the build, and cheaper subagents play the steps. It advises the conductor model up front, sizes each step's model and effort, and hands a failing step back to the orchestrator rather than rewriting the spec itself."
---

# Conductor (Session Discipline)

The session conductor — keeps one session in tempo and coherent from open to close, the way an orchestra conductor holds a single performance together. (Renamed from `dian`, which was too opaque to signal the role.)

A protocol for staying focused within a session. Conductor commits and pushes its own work as each task verifies, but never pulls and never writes session state by hand — the boundary is the Switch Out flow's, which close-out invokes as its final act. Conductor keeps you on track once you're working.

## The Stage

Conductor coordinates four roles. Keeping them distinct is what makes both the quality and the cost model work:

| Role | Who | Owns |
|---|---|---|
| **Composer** | you | intent — what to build, and the boundaries |
| **Orchestrator** | a top-tier model, called as a subagent | the score — turning intent into a spec each player can read cold |
| **Conductor** | the session model you're on | the performance — dispatch, tempo, judging returned work against the score |
| **Players** | cheaper subagents, sized per step | execution of one step |

The orchestrator is a **call, not a mode**. It is summoned when a score needs writing, works from a tight brief, and returns to the wings. It never holds session context, never watches the build, and never reviews returned work — which is why buying its reasoning is affordable.

The conductor holds the baton for everything else: orient, dispatch, verification, escalation, close-out. It is genuinely capable of most implementation, so steps it plays itself carry no premium.

**The line that keeps the roles honest: the conductor may re-dispatch, never re-specify.** When a step fails, the conductor may hand the same spec slice to another player, refine *how* it's dispatched, or stop. It may not rewrite the score. A wrong score is the orchestrator's to fix — see [Escalation](#escalation--when-the-score-is-wrong).

## Usage

`/kerd:conductor` run a structured session: orient, advise the conductor model, plan, execute, close.

Conductor runs inside whatever session and model you already started — a skill can't read or change its own model. So it **advises the conductor model** (the one holding the baton for the session) and gates on your confirmation. That advice is now modest: because the hardest reasoning happens in an orchestrator *call* rather than in the session, a hard task no longer requires running the whole session on a top-tier model. From there conductor sizes each mechanical step's model and effort and hands it to a player. There is no toggle — right-sizing is conductor's default behavior, scaled to the task in front of it. See [Model advisory](#model-advisory) and [Delegated execution](#delegated-execution--the-spec-is-the-contract).

## Mode Markers

Conductor is a modal skill. It runs across multiple responses. Announce the current phase so the user always knows what's active.

**On every phase transition**, output a marker on its own line at the top of your response:

- `[conductor: orient]` reading context, summarizing state
- `[conductor: plan]` proposing session plan
- `[conductor: plan · orchestrator→<model>]` calling the orchestrator to write or correct a score
- `[conductor: execute]` working through tasks
- `[conductor: execute step N/M]` working a specific plan step (fires at step transitions within execute)
- `[conductor: execute step N/M · delegate→<model>]` a `[delegate]` step dispatched to a player
- `[conductor: close-out]` updating docs, running checks
- `[conductor: closed]` session complete (final marker, then done)

**Why a step-boundary marker within execute:** phase markers fire 3-4 times per session — too coarse to gate claim-level failures (the Claim Discipline problem — gates asserted once don't bind the 50th claim). Step-boundary markers fire 5-30 times per session at the granularity where confident-wrong assertions actually happen. Each step marker is a reminder to re-engage the verification gate, not boilerplate. Don't re-emit the marker mid-step; only at the actual step transition.

**State file:** When entering a phase, write the current phase to `kivna/.active-modes`. When closing out, remove the conductor line from the file (or delete the file if it's the only entry). This lets `/kerd:switch in` report active modes and hooks surface reminders.

Format of `kivna/.active-modes` — conductor owns one line only:
```
conductor: <phase>
```

Example: `conductor: execute`. Remove the line entirely when closing out (don't write `conductor: closed`). Never touch other skills' lines in this file.

## The Protocol

### 1. Orient

Output `[conductor: orient]` at the top of your response.

Conductor runs inside an already-open session. Loading context is switch-in's job, not conductor's, so orient is conditional:

**Warm path (the common case — switch-in already ran this session):** Don't re-read anything. Switch-in just loaded `CONTEXT.md`, `TODO.md`, the newest session log, and active modes. Confirm the current state in a line or two from what's already in context, then move to planning. Re-reading what switch-in just read is wasted work.

**Cold path (conductor invoked with no switch-in this session):** Do a light orient — read only `CONTEXT.md` (`## Where We Are`) and `TODO.md` (`## Now`). That's enough to plan. Don't sweep the playbook, session logs, and progress files; that's switch-in's read. If you need the full picture, run `/kerd:switch in` first.

**Bare repo (no Kerd structure detected — no CONTEXT.md, no TODO.md, no `kivna/`):** offer `/kerd:tend` to set the structure up before planning — one invoke; tend's own SKILL.md defines the setup. If declined, orient on what exists and continue.

**Mode awareness:** Read `kivna/.active-modes`. If a mode is active, report it: what mode, which step, and the session instruction if one was set. Conductor operates within the mode's scope. If the mode says "focus on pricing strategy only," conductor's plan respects that constraint. If no mode is active, proceed normally.

**Pre-flight inventory:** Ask the user for anything execution will need that isn't already in the repo: credentials/access not stored locally, sample inputs not in TODO.md, scope limits not in CLAUDE.md, hardware/environment state, fixtures or test data. Trickle-in friction (each missing input becomes a stop-and-ask round mid-execute) is 5-10x more expensive than collecting upfront. One round of questions now prevents many later. If the inventory is genuinely complete, say so explicitly and skip.

**Consistency sniff test:** Quick cross-check against what's in context — does CLAUDE.md or the playbook reference files, conventions, or a tech stack that no longer match reality? Flag contradictions before planning. This is a light pass; the deep audit is `/kerd:slainte`.

Summarize the current state for the user, including any inconsistencies found, active mode context, and inventory gaps surfaced.

#### Model advisory

Before planning, size the work and advise the **conductor model** — the one holding the baton for this session. Judge it on what the *conductor* has to do (dispatch, verify returned evidence, decide whether a failure is the player's or the score's), not on how hard the underlying problem is. The hard problem goes to the orchestrator call, not the session.

- **Mechanical / small** (a rename, a config edit, a well-trodden fix): the model you're on is almost certainly fine. Say so and move on.
- **Anything with a real build** — including hard, architectural, or novel work: recommend a strong mid-to-upper model (e.g. Opus). It must judge returned evidence well, because bad conformance judgment is the most expensive failure in the system: it wastes player runs *and* buys an orchestrator callback.
- **Never recommend switching the session to the top tier for difficulty alone.** That was the old shape. Difficulty is now handled by [calling the orchestrator](#calling-the-orchestrator), which costs one brief and one score instead of an entire session at premium rates.

State your recommendation in one line and **gate on it**: ask the user to switch (or confirm they're already there) before you plan. Conductor can't read or set its own model, so this is advice plus a confirmation beat, not detection — proceed on whatever model the user confirms. Skip the gate only when the work is trivially small and the current model obviously suffices; say why you're skipping.

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

#### The gate message carries the content

Every conductor gate ends a turn with a question — the model advisory, the task-framing approval, the plan/spec approval. The message that asks the question must itself contain what is being approved: the orient summary, the findings, the task boundaries, the plan or spec steps. Never assume text written earlier in the turn was seen — display modes like Claude Code's focus mode show the user only the final message of a turn, so analysis written between tool calls may be invisible. A gate message that is only the question ("execute the plan?") erases the analysis for those users. Lead with the findings, end with the one ask — a compact summary is fine; an absent one is not. This applies to every gate in this skill.

When the gate's question is a **decision** — the user choosing between real alternatives, not confirming a plan — the message follows the **Proposal** format from the talk-formats library (`docs/design/talk-formats.md`): what the situation is, why it matters and the gap, what we win, and **what we lose, named**. Those five fields are Proposal's sections (current situation → problems & cause → proposal & benefits); a decision message missing the loss is missing a section.

#### Say it in the user's terms

The rule above governs *whether* the content is in the message. This one governs *what language it's in*. Both fail the same way — a message the user cannot act on — and this one is harder to spot, because the message looks complete. A wall of correct technical detail doesn't slow a decision down; it makes the decision unmakeable, because the user is being asked to arbitrate something that was never theirs to arbitrate.

**Trigger:** any change that alters what the user can *do*, and any question that is theirs to decide. Capability regressions always qualify — those read as improvements until someone spells out what's gone. Routine mechanical work doesn't need it; don't do this for a version bump.

**The shape:**

> **Now:** what they experience today
> **The change:** what they'd experience instead
> **What it means:** the consequence, including the cost

This is the **Compare & Contrast** format from the talk-formats library (`docs/design/talk-formats.md`): current situation → new situation, in the reader's vocabulary.

Write it in the vocabulary of *using* the thing, not building it. File paths, symbol names, table columns, line numbers and migration names belong in the spec and the commit message — not here. If a sentence can't be parsed without the codebase open, rewrite it.

**Name the loss.** When a change removes something the user had, say so in those words: "this is a real capability you had yesterday and don't have now." The same removal described as a feature — "tap now picks the restaurant" — disappears into the good news, and the user approves a regression they never saw. Volunteering the cost of your own change is the substance of this rule, not a politeness.

**The question test — could they answer it without reading the code?** If yes, ask it. If no, either restate it as an outcome, or recognise it as a call you should be making yourself: a question that requires the codebase to answer is usually not the user's question. "Should people be able to change their vote before the room finishes?" passes. "How do you want these three screens verified?" does not.

**Framed well, a question needs no options.** When the change is stated clearly the user answers in their own terms — often resolving more than was asked — rather than picking from a menu that pre-narrows the space to what you already thought of. State the change, ask open, let them steer. Offer options only when they genuinely clarify a choice, never as a substitute for explaining the change.

The same shape carries a **deferral**: what the user would have gained, that it is specced but deliberately not built and why, and an honest cost so a later session doesn't re-derive it and quietly decide it's too expensive.

#### Delegated execution — the spec is the contract

Once the task is framed, decide whether it has **mechanical bulk worth delegating**. Two cases, and conductor picks per task — there is no toggle:

- **Lean/inline** — the task is small or all-judgment (nothing a player should do). Write the plan into TODO.md `## Now` as above and execute inline as conductor. No orchestrator call, no spec file. Skip the rest of this section; most small sessions land here.
- **Delegated** — the task decomposes into mechanical steps a cheaper model can do from a written contract. The plan becomes a **spec file**, and conductor sizes each of those steps and hands them down while it stays in the judgment loop.

When delegating, the plan is not a lean TODO stub — it is a **spec file**, the contract handed to the implementer:

- **Location:** `docs/plans/YYYY-MM-DD-<slug>-spec.md`. TODO.md `## Now` shrinks to a one-line pointer at the spec plus the step checklist. The spec file is a committed artifact — switch picks it up at the boundary.
- **Executor tag per step — assigned *after* the step is written, never before.** Write the step body in full, then read the finished text and ask what decision is still left in it. Writing a spec slice well is the act that *removes* judgment from the model and deposits it in the document, so a tag assigned during planning measures the wrong moment — it records how hard the step felt to plan, not how much judgment survives being written down. The test is mechanical and self-checking: **can this step be written precisely enough to verify by command?** Yes → `[delegate]`. No → `[keep]`, and your inability to write it out is exactly the evidence that it needs judgment. Two buckets only: `[keep]` (the conductor plays it) and `[delegate]` (assigned to a player). Conductor assigns; the user approves at the plan gate alongside the plan itself.
- **Blast radius is answered by a review step, not by keeping the work.** A tempting mistake: tagging a risky step `[keep]` because failure there compounds downstream. It doesn't help. The characteristic blast-radius failure is *mechanical* — a deletion range that swallows adjacent code, a rename that catches a near-match — and a stronger model has no better aim than a weaker one. Keeping such a step buys nothing and costs the conductor's attention. **Delegate the risky edit, then add a separate `[keep]` step that reviews the diff for unintended drift.** That step is a real keep: reading a diff for edits that pass every verify command yet violate the stated scope is judgment, and it cannot be written as a command. Note what the review must catch — "confirm nothing outside the named symbols was removed" — in the step body.
- **What's left in `[keep]` after that is small, and that's correct.** Once tags are assigned against finished text and blast radius is handled by review steps, most keeps dissolve. Expect a spec to be mostly `[delegate]` with one or two `[keep]` review steps at the seams. If `[keep]` is still carrying half your steps, the tags were assigned before the bodies were written. Resist adding a third tag for any of this: tags encode *actions* (who executes), and a tag that encodes a *reason* decays into a vibe marker — reasons go in the step body, where they can say what to check.
- **Sized model + effort per delegated step:** conductor sizes each `[delegate]` step's model and reasoning effort to the work and writes them into the tag — `[delegate, model: haiku, effort: low]` for trivial edits, `[delegate, model: sonnet, effort: medium]` for standard implementation, up to `[delegate, model: sonnet, effort: high]` for core-but-delegatable work. Model tier and effort are two independent levers; omit either and the subagent takes its default. Putting the sizing in the tag makes it reviewable at the plan gate — the user approves the model and effort choices, not just the steps. Sizing is the conductor's call, since it's a staffing decision about the performance; the orchestrator may propose tags with the score, but the conductor owns the final assignment.
- **The bar for a `[delegate]` step is higher than a normal plan step.** It must be playable by a model that never saw the orchestrator's reasoning: exact files and paths, the function/type signatures or interfaces to add or change, the *why* behind any non-obvious choice (so the player doesn't re-derive intent and drift), and a verification command with its expected output. A vague spec produces a confidently-wrong implementation from a cheaper model with no recourse — spec quality *is* the safety mechanism, and it is the entire reason the orchestrator's expensive tokens are worth spending.

#### Calling the orchestrator

The score is written by a top-tier model invoked as a **subagent** (the Agent tool's `model` accepts the top tier, e.g. `fable`), not by the conductor itself. Two passes, both deliberately small:

**Pass 1 — scoping.** Send intent, boundaries, and constraints only. Ask one question: *what do you need to see to write this score?* The orchestrator replies with specific files. **Bound the request in the prompt — name files, not directories.** An unbounded scoping answer collapses this back into a full context dump and forfeits the entire saving.

**Pass 2 — the score.** The conductor fetches exactly what pass 1 named (retrieval is mechanical; it belongs on the conductor) and sends it with the brief. The orchestrator **writes the spec file directly to `docs/plans/YYYY-MM-DD-<slug>-spec.md`** and returns only a short summary — the step list, the tags, and any risk it wants raised at the gate. Writing to disk rather than returning the score as text keeps a 200-line spec out of the conductor's context entirely.

Why two passes: it separates *deciding what's relevant* (judgment, and cheap to express — a list of paths) from *retrieving it* (mechanical, and now on the conductor). A conductor-curated brief is cheaper but makes the conductor's curation error the orchestrator's blind spot — it writes a confident score against terrain it never saw, and nobody finds out until players have failed against it.

The brief carries four things, and deliberately not a fifth:

- **Intent** — the composer's words, plus explicit out-of-scope boundaries
- **Terrain** — the actual file contents from pass 1, not summaries (the score must name exact paths, signatures, and values)
- **Constraints** — binding conventions and standing decisions from CONTEXT.md the design can't violate
- **Available players** — which model tiers exist to be assigned

Not the orient narrative, not how the conductor reached its conclusions, not alternatives already rejected. That's session diary — it's the bulk of what a naive handoff would carry, and the orchestrator needs none of it.

Hand the orchestrator a **template** with judgment-shaped slots (step header, tag, what / why / verify) so its output tokens go to decisions instead of reinventing scaffolding. But **do not delegate spec *detail* to a cheaper model.** A template removes boilerplate; the exact values, signatures, and verify commands are where judgment gets encoded precisely enough to survive a player that never saw the reasoning. That detail *is* the safety mechanism, not padding around it.

Skip the orchestrator call entirely for lean/inline tasks — if there's no score to write, there's no one to summon.

**When the orchestrator is unavailable.** Top-tier capacity runs out — the call can fail on quota, not just on error. Don't stop the session: write the score yourself as conductor, and **say so explicitly at the approval gate** ("orchestrator unavailable — this score is mine, expect it to be thinner"). The user is then approving a lesser score knowingly rather than receiving one silently. Retry the orchestrator for a hand-back if a step later fails on score grounds; capacity may have returned. A conductor-written score is worse, not useless — the failure mode to avoid is the user believing they got the better one.

Write the spec, write the pointer into TODO.md `## Now`, and wait for approval — the same gate as inline. The user approves the spec, the tags, the sized model/effort, and the boundaries together before any execution begins.

### 3. Execute

Output `[conductor: execute]` at the top of your response when entering this phase.

Do the work. Stay focused on the plan.

#### Dispatch mode (delegated plans only)

If the plan is lean/inline, skip this — just work the plan. If it's a spec file with `[keep]`/`[delegate]` tags, pick the dispatch mode with the user at execute entry:

- **In-session players (default).** Play `[keep]` steps yourself. For each `[delegate]` step, spawn a subagent via the Agent tool with its `model` and `effort` set to the step's sized tag — handing it *that step's spec slice*: scope, files, signatures, the why, and the verify command. The player returns its result plus evidence (command output, diff summary). You do not re-do the work — you **review the returned evidence against the step's acceptance criteria** (the verification gate below, applied to the player's output). Emit `[conductor: execute step N/M · delegate→<model>]` at each dispatch.
- **Handoff to a fresh session.** Finish the spec and stop. Tell the user to open a new session pointed at `docs/plans/YYYY-MM-DD-<slug>-spec.md`; that session plays every step and self-verifies via the spec's built-in verify commands. Use this when the build is long enough that even the conductor's dispatch-and-review tokens aren't worth spending in this session — but note the trade: nobody with judgment watches the build, so the spec's verify commands are the only net.

Either way the spec is the contract and the verification gate still governs "done" — the only question is who plays the steps. If a player's returned evidence fails the acceptance criteria, that counts as a failed attempt under the 3-fix limit. Don't silently accept muddy output — and don't quietly rewrite the score to make the failure go away (see [Escalation](#escalation--when-the-score-is-wrong)).

#### Verification gate

After each task, verify it with evidence before claiming it's done. No exceptions.

1. **Identify** the check: what command, file read, or test confirms this task worked?
2. **Run** it. Actually run it. Don't assume.
3. **Read** the output. Look at what came back.
4. **Confirm** the claim: does the evidence support "this task is done"?
5. **Check for collateral:** did anything change that *shouldn't* have? Read the diff, not just the verify output.

Only then mark the task complete. If you catch yourself thinking "should work", "probably fine", or "seems good" without evidence, stop. Run the check.

Step 5 is not redundant. A verify command tests for the *presence* of the intended change; it is silent about the *absence* of unintended ones. A deletion range that swallows three neighbouring helpers, or a rename that catches a near-match, passes every check written for the step it belongs to — the damage lives in code nobody thought to grep for. Bulk deletions, renames across many call sites, and regex-driven edits all need the diff read, not just the command run.

**When you catch your own mistake mid-step, say how you caught it.** One clause is enough — "the build failed", "step 5 diff read", "noticed while re-reading". A silent self-correction looks identical whether the guard worked or you got lucky, and only one of those is worth trusting next time. This is the cheapest signal available about whether the verification gate is actually load-bearing, and it's lost by default.

#### Strong-language gate (claim-formation)

The verification gate above covers "done" claims at end-of-step. The same discipline applies to claims made *during* a step. Before tagging anything with "verified", "fixed", "working", "confirmed", "the right approach", "the only way", "impossible", "always", "never" — or asserting platform/library/API specifics: require evidence in this loop iteration (a check run, an output read, a doc cited, a source URL). Without those, downgrade to "added but not yet verified", "the evidence I have suggests", or "from training data; may be wrong". Each external-system claim must carry a "verified by [URL/doc]" tag.

This mirrors the Claim Discipline some users keep in a global CLAUDE.md; it's restated here so conductor enforces it even in projects without one. It applies at the moment of writing the assertion within execute, not deferred to end-of-step. The verification gate is a backstop; this gate is the primary line.

#### 3-fix limit

If a task isn't working after 3 attempts, stop. Do not attempt fix #4. Instead:
- Summarize what was tried and why each attempt failed
- Surface the problem to the user
- Ask whether to continue with a different approach, skip the task, or rethink the plan

The surfaced report follows the **Correcting Discrepancy from Standard** format (`docs/design/talk-formats.md`): the declaration the work was measured against, the discrepancy the evidence shows, then the countermeasure options. A failure report that never names the declaration it failed against is an anecdote, not a report.

Three failed fixes usually means the approach is wrong, not the execution. It is also the talk-formats **problem-tier trigger** — "a problem that survived a few attempts" — the declared route for a point-of-cause tool (e.g. `/sensei:work`) where one is installed: route on the match, never by default. If the task framing itself was the problem (scope too broad, acceptance criteria unclear), suggest refining the task and restarting with a fresh conductor session rather than continuing in degraded context.

#### Escalation — when the score is wrong

**The conductor may re-dispatch, never re-specify.** When a delegated step fails, first decide which kind of failure it was:

- **The player failed.** The evidence doesn't meet the acceptance criteria, but the spec slice was clear and correct. Re-dispatch — same slice, possibly a stronger tier or higher effort. Counts against the 3-fix limit.
- **The score is wrong.** The spec asked for something that can't be done, contradicts the terrain, or assumed a structure that isn't there. Re-dispatching cannot fix this — a second player fails the same way, and a third confirms it.

Three failures on one step means the score is wrong, not the players. That is the hand-back boundary: **summon the orchestrator again for that passage.** Send the failing slice, the evidence from each attempt, and the terrain that contradicted it, and ask for a corrected passage — not a new score, one passage.

Surface the callback to the user before making it. It spends top-tier tokens, and it means the plan they approved was wrong in a specific way they should see.

If the corrected passage also fails, stop. That's the 3-fix limit applied one level up: the problem is the task framing, not the score. Refine the framing and restart with a fresh conductor session.

Rewriting the score yourself is the failure this rule exists to prevent. It is quiet, it feels efficient, and it destroys the contract — the composer approved a score, the players are building to it, and a conductor editing it mid-performance means nobody can say what was actually agreed.

#### Scope creep

If something comes up that isn't in the plan, stop working on it immediately. Add it to TODO.md backlog. Do not continue on the tangent. Do not "just quickly" do it. Return to the current plan step. The user can reopen the plan if the new work is more important.

#### Decision recording

When a significant decision is made during execution (architecture choice, rejected approach, key trade-off), record it in `CONTEXT.md` immediately — `## Key Decisions` for what was decided and why, `## Open Questions` for what surfaced but wasn't resolved. Don't defer to close-out. Decisions lose their reasoning if you wait.

Do not write to `kivna/sessions/` during execution. Switch owns session log creation at the git boundary. Conductor's decisions accumulate in CONTEXT.md and flow into the session log when switch runs.

#### Docs travel with code

If a task changes behavior, update the affected docs (README, playbook, CLAUDE.md) in the same commit. Don't defer doc updates to close-out. No commit should leave docs inconsistent with code.

#### Work commits

**Commit and push each task once its verification gate has passed.** Don't hold work until the boundary — a session that completes three tasks should leave three commits, not one. Do this on your own; no approval beat. The gate is what makes it safe: an unverified task isn't committable, and a verified one isn't work-in-progress.

- **Stage by name.** Only the code and docs this task touched. Never `git add -A`. Session-state files — `CONTEXT.md`, `TODO.md`, anything under `kivna/` — never ride along in a work commit. Switch owns those at the boundary, and mixing them collapses the split.
- **Push immediately.** Commits piling up unpushed until switch-out reintroduce exactly the risk the always-push convention exists to prevent.
- **Never pull.** Pulling is a boundary sync and belongs to switch — pulling mid-execute can change files under an in-flight task.
- **Commit per task, not per step.** A multi-phase spec may warrant a commit per completed phase; a single task is one commit. If the project's CLAUDE.md defines a pre-commit checklist (version bumps, changelog entries), it governs — and an expensive checklist is a reason to commit per phase rather than per step, not a reason to defer to the boundary.

Why per-task rather than per-session: the collateral check (verification gate step 5) is only affordable when the diff is small. Three tasks' worth of interleaved change in one boundary commit hides exactly the drift that check exists to catch — a swallowed helper is obvious in one task's diff and invisible in a session's.

**At each task's verified commit, name what's next in one line.** While the plan still has steps, that's the next plan step; when the plan is done, it's the top pick from TODO's `## Now` or `## Backlog`. Suggestion only — starting it stays a human reply; no loop, no hook, no auto-start.

#### No vault writes

Work accumulates in repo-side files (TODO.md) during execution. Conductor never writes the vault — and since v0.83.0 neither does the boundary: `/kerd:kivna save` is the deliberate, on-demand export for projects that keep one.

### 4. Close Out

Output `[conductor: close-out]` at the top of your response.

Close-out settles the work, then runs the boundary itself — one act, no handoff ask. By now each verified task is already committed and pushed (see [Work commits](#work-commits)). Keep conductor's close-out short:

1. **Update TODO.md and CONTEXT.md**: remove completed tasks from TODO, add new ones discovered during work, then overwrite `## Now` to forward-only state (what's next, a few lines — the completed record is the session log switch writes at the boundary). Record any *unresolved* decisions or questions in CONTEXT.md (`## Key Decisions` / `## Open Questions`). Apply Claim Discipline to summary text — don't claim "we verified X" unless we did; downgrade to "tested with Y; Z untried" when alternates exist; don't promote provisional findings to canonical without the survival test.
2. **Doc impact**: docs should already be current (docs travel with code, see Execute). Confirm nothing was missed against the CLAUDE.md Doc Impact Table if one exists. Don't carry doc updates into the boundary.
3. **Run checks**: run the project's build/test command if one exists. Do not close out with failing tests.
4. **Mode-aware completion**: if a mode is active, do NOT suggest the session is done unless the mode flow is also complete. Conductor may be one step in a larger mode flow. After conductor's close-out, control returns to the mode for the next step. If no mode is active, this is the natural end point.
5. **Clear the conductor marker**: remove the conductor line from `kivna/.active-modes`. Never touch the mode line — mode owns its own state.
6. **Release close-out pass**: if this session's work commits changed the three plugin `"version"` fields (CI's release definition, rule R1), invoke `/kerd:tend` and then `/kerd:slainte` before the boundary — the structural drift check and the narrative pass with fixes, each defined in its own SKILL.md, not here. The pass's edits are work commits under the verification gate. No version change, no pass.
7. **Run the boundary**: invoke `/kerd:switch out` via the Skill tool — full mode, the standalone default. The flow is defined once, in `skills/switch/SKILL.md` Switch Out; do not re-describe its steps here or anywhere in this file. When it completes, output `[conductor: closed]` as the final marker.

## Principles

- **Commit your work, never pull.** Work commits (code + the docs travelling with it) are conductor's, pushed at each verified task boundary, staged by name. Pulling is a boundary sync and belongs to `/kerd:switch` — it can change files under an in-flight task.
- **Evidence before claims.** Every "done" must have a check that was run, output that was read, and a conclusion that follows.
- **Hard stop on scope creep.** Out-of-plan work goes to backlog. No exceptions without reopening the plan.
- **Three fixes, then escalate.** Don't thrash. Surface the problem.
- **Docs travel with code.** If you change behavior, update the docs in the same commit.
- **Conductor closes the session it conducted.** Work commits per verified task, then close-out invokes the Switch Out flow (`/kerd:switch out`) as its final act — one definition of the boundary, two callers. Standalone switch out serves sessions without conductor. Conductor still never pulls (pull is switch-in's) and never writes session state by hand.
- **Four roles, kept distinct.** Composer owns intent, orchestrator owns the score, conductor owns the performance, players execute. Nobody's authority overlaps — that's what makes each one affordable to staff correctly.
- **The orchestrator is a call, not a mode.** Top-tier reasoning is summoned for a brief and a score, then leaves. It never holds session context, watches the build, or reviews returned work. Buying it this way costs one brief and one score instead of a whole session at premium rates.
- **Re-dispatch, never re-specify.** A failing step is either a player problem (re-dispatch) or a score problem (hand back to the orchestrator). The conductor never edits the score to make a failure go away — that silently voids the contract the composer approved.
- **Tag the step after writing it.** Writing a spec slice well is what removes the judgment from the model and puts it in the document. A tag assigned during planning measures how hard the step *felt*, not what judgment survives being written down. If you can write it precisely enough to verify by command, it's delegatable — and if you can't, that's the evidence it isn't.
- **Advise the model, don't assume it.** Conductor can't read or set its own model. It sizes the work, recommends the *conductor* model, and gates on the user confirming (or switching) before it plans — then sizes each delegated step's model and effort down from there. Difficulty never argues for running the whole session at the top tier; that's what the orchestrator call is for.
- **The spec is the contract.** The orchestrator's job is a score complete enough that a player never re-derives intent. Spec quality is what makes delegation safe — a vague `[delegate]` step produces a confidently-wrong build with no recourse. Spend the expensive tokens on the score, not the grind, and never delegate the *detail* to a cheaper model to save a few of them.
- **The gate message carries the content.** Any message that asks for approval must contain what's being approved — findings, summary, plan — in that same message. Mid-turn text may be invisible to the user (focus mode shows only a turn's final message); a question-only gate erases the analysis.
- **Say it in the user's terms.** When a change alters what the user can do, describe it as *now / the change / what it means* in the vocabulary of using the thing — and name any capability it removes as a loss, or it disappears into the good news. Ask only questions answerable without reading the code; if it needs the codebase to answer, it's usually your call, not theirs.
- **Talk moments follow the format library.** Decision gates speak Proposal, user's-terms changes speak Compare & Contrast, failure reports speak Correcting Discrepancy from Standard, and three survived fixes trigger the problem tier. Formats and their used-when triggers are canonical in `docs/design/talk-formats.md`; a message claiming a format carries that format's sections.
