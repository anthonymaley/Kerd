---
name: interrogate
description: "Use when the user says 'interrogate', 'risk ledger', 'qualify risks', 'killer assumption', 'interview me', 'walk me through this plan', 'stress-test this idea', 'help me figure out if this is viable', or has a plan/idea whose risks need qualifying — sized, evidenced, with Severity and Treatment each stated — across every viability axis (technical, business, legal, operational). Produces a tiered risk ledger: everyday work fills the ledger in the framing conversation without invoking this skill; a large bet runs the full co-signed session at docs/interrogations/. Does NOT produce the implementation plan itself — produces qualified risks."
---

# Interrogate (Risk Ledger)

Interview the user relentlessly about a plan or idea until every risk is QUALIFIED — sized, evidenced, with Severity and Treatment each stated — because a named, unsized risk reads as managed, and that is the failure this skill exists to stop. The interview engine is the instrument; the tiered risk ledger is the output. For a large bet, the exit ritual is mutual co-sign of the ledger.

This skill is the countermeasure to the convergence pull in normal brainstorming — verbose framing, premature multiple-choice, unilateral declarations of "done." It cannot be ratified with a yes/no.

## Invocation

`/kerd:interrogate` start from zero — agent asks "what's the idea?"
`/kerd:interrogate <plan-ref>` interrogate an existing plan

`<plan-ref>` is a file path, an idea description, or a reference like "current TODO" or "the latest session log."

## Tiering

| Tier | Instrument | Home |
|---|---|---|
| Everyday | the ledger filled inside the framing conversation — normal-sized work, no skill invocation | the living `## Risk ledger` section of `docs/product/<slug>.md`, overwritten in place |
| Large bet | the full interrogate session — exhaustive across the axes (technical · business · legal · operational) | dated session record at `docs/interrogations/YYYY-MM-DD-<slug>.md`; the co-signed ledger is copied into the living section at sign-off |

**Everyday.** This skill's Ledger section is the reference for the everyday practice: same ten columns, same Severity and Treatment vocabulary, same rules — killer first, FATAL discipline, a risk without a countermeasure is a BLOCKER, an unqualified risk must not reach the next stage — applied inside the normal framing conversation without invoking this skill. The ledger is living state: states flip as countermeasures land and review triggers fire, so it is overwritten in place, never dated.

**Large bet.** The full session below. Its co-sign is written in the shape of the viability gate record: when the entry gates are live, sign-off will also emit `docs/gates/YYYY-MM-DD-<slug>-viability.md` (dated, per the gate-record naming rule); until then the signed interrogation document is that record. Documented here — no record-emitting machinery ships with this skill.

## Entry Paths

**Plan-ref path.** Read the plan at the given reference. Propose the viability axes you infer from the plan content (not a mandatory exhaustive checklist — inferred from the plan itself). Ask the user to prune: which axes to keep in scope, mark out-of-scope, or defer up front. Then enter the interview loop.

**Zero path.** Ask one open question — *"what's the idea?"* — and build the document from blank. Axis identification happens organically as ideas surface. The universal core (see Default Axis List below) always applies.

Both paths converge on the same artifact — a co-signed risk ledger — under the same exit rules.

**The value declaration comes first.** Impact has no units until the value is declared. The canonical home is the `## Value` section of `docs/product/<slug>.md` — the same section the viability gate checks. If it exists, read it and denominate every Impact cell in its units. If it does not, the interview's first thread establishes it and writes it there (creating the file with legal `route`/`stage` front matter if needed) before any risk row is opened — frame first, then qualify.

**The killer question comes next.** Immediately after scope pruning (plan-ref path) or once the idea is stated and the value declared (zero path), ask: *"What is the one assumption that, if false, kills this?"* That row opens first and gets the cheapest decisive evidence — a SPIKE, declared as such, if a test is needed — before any other risk is examined.

## Interview Discipline

These rules govern every turn during a session. They are not aspirational — they are the structural floor.

1. **One question per turn.** No "Question 1 of N." No bundled questions. Each turn surfaces exactly one open thread.

2. **No multiple choice unless genuinely discrete and small.** Default open-ended. Force articulation, not selection. Multiple choice is a cop-out that lets the user agree without thinking.

3. **No extrapolation.** Do not sketch the plan from partial answers. No *"so it sounds like you want X, Y, Z."* That pre-shapes the design before understanding is reached.

4. **Response shape constrained.** Your response in the interview = at most one sentence of acknowledgment + the next question. No insight blocks, no padding, no *"let's think about."* Verbosity is a tell of lack of understanding; the discipline forbids it during the interview itself.

5. **User-veto on stop.** Never declare the session done. The interview continues until the user explicitly says stop. You *may* propose intermediate transitions — like *"I've exhausted my known unknowns; ready to enter recitation?"* — but the user can veto any proposal to keep interviewing.

6. **Three "done" gates, all required for sign-off.**
   - **(a)** You have exhausted your known unknowns AND the ledger passes the qualification check before recitation can be proposed. The qualification check requires:
     - every in-scope axis has at least one ledger row OR an explicit clear line in **Axis coverage** (*"no qualifying risk found — <basis>"*)
     - every row fully qualified: **Impact** in declared-value units (never a vibe word) · **Likelihood** present, recorded separately · **Evidence** non-empty, naming a test or an analysis · **Severity** `fatal` or `non-fatal` · **Treatment** exactly one of the four · **Countermeasure** named with a confidence statement when Treatment begins *Countermeasure* (plus a return condition when TEMPORARY) · **Treatment evidence** for a fatal row: the planned form `planned — <what will exist> · <expected location>` or a resolving citation — never empty · **Review trigger** non-empty when Treatment begins *Accepted*, and when Severity is fatal with a temporary countermeasure
     - no fatal-severity row whose Treatment is accepted, accepted unknown, or empty — an untreated fatal row blocks recitation: the idea is killed (recorded in *What we ruled out* with the ledger row as evidence and its return condition attached) or reshaped until the row is no longer FATAL

     If the check fails, continue interviewing on the failing rows — no recitation proposal. If it passes, *propose* entering recitation. User can veto ("more to discuss") to keep interviewing.
   - **(b)** User has no more answers, requirements, or ideas to share.
   - **(c)** Recite the ledger back **row-by-row**; user confirms each risk individually. Whole-ledger recitation is rejected as the easy-ratification trap this skill is designed to avoid.

7. **Killer-first, then tree-aware ordering.** THE killer assumption is resolved first, always — the riskiest thing gets the cheapest test before anything else is examined. Below it, decisions that constrain other decisions get resolved first. Within each decision, depth-first: resolve fully — including the ledger rows the decision affects — before sliding sideways to the next branch.

8. **Adversarial lean — graduated and user-dialable.** Default trajectory follows saturation:
   - **Gather** (early) — open questions, no challenges. *"Tell me about X."*
   - **Probe** (mid) — drill into vagueness, ask for specifics. *"What does that mean concretely?"*
   - **Stress-test** (late) — challenge claims, ask for evidence. *"How do you know that's true?"*
   - **Adversarial** (deep) — actively look for holes. *"What would have to be different for this not to work?" / "What's the strongest objection?"*

   User can dial level at any moment in either direction: *"go harder now"* / *"ease off, still ideating"* / *"stay at probe for this axis."* Track the current level in the document's `adversarial-level` frontmatter field.

**Pause/resume.** Sessions can run long. The document is persistent state — leaving and returning resumes from the document, not from conversation memory. Session state lives in document frontmatter (see Document Structure section). On resume, restate the level and target, then **re-ask the last unanswered question verbatim** from the `last-question` frontmatter field — e.g. *"Resuming at stress-test on Security. Last question: [verbatim]."* — and stop. The user can ask for refinement if needed; do not offer a meta-choice. The unanswered question is the active edge; re-present it, nothing more.

## The Ledger

Risks as rows, killer rows first. Columns:

| Column | Rule |
|---|---|
| **Risk** | the concept, not the incident — one row per eliminated-or-carried idea |
| **Killer?** | marks THE killer assumption — tested first, always |
| **Impact** | in the units of the declared VALUE (`## Value` of `docs/product/<slug>.md`) — never a vibe word |
| **Likelihood** | recorded SEPARATELY, never multiplied — expected value is the wrong maths for a bet taken once |
| **Risk evidence** | a test OR an analysis — the same kind of evidence, differing in cost. Empty evidence = unqualified |
| **Severity** | `fatal` or `non-fatal` — set by impact against the declared value, at any likelihood |
| **Treatment** | exactly one of the four below |
| **Countermeasure** | named, with a CONFIDENCE statement |
| **Treatment evidence** | what proves the treatment — empty only at non-fatal; `planned — <what will exist> · <expected location>` before the proof exists; a resolving citation once it does |
| **Review trigger** | for accepted states: the date or condition that brings the risk back |

The table header is exact — downstream mechanical checks match it byte-for-byte:

```
| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
```

**Severity:**

| Severity | Meaning |
|---|---|
| **fatal** | impact ≥ the declared value, at ANY likelihood |
| **non-fatal** | impact below the declared value |

**Treatment:**

| Treatment | Meaning |
|---|---|
| **Countermeasure — permanent** | closed by design |
| **Countermeasure — TEMPORARY** | carries its return condition; an unmarked temporary countermeasure is permanent by neglect |
| **Accepted** | by whom, when — and its review trigger |
| **Accepted unknown** | by whom, when, why the evidence was not gathered — and its review trigger |

**The rules:**

- **FATAL is set by impact alone** — likelihood sets the response, never the class.
- **A risk without a countermeasure is a BLOCKER** — silence stops work instead of passing it.
- **The one unacceptable state**: high impact + high likelihood + no countermeasure = dead project. It cannot be accepted by name — a fatal-severity risk cannot carry Treatment accepted or accepted unknown.
- **Killer assumption first**: the riskiest thing gets the cheapest test before anything else is examined. The SPIKE is that instrument — declared up front, cheap, built for a kill-or-keep decision.
- **An unqualified risk MUST NOT reach the next stage.**
- Every △ verdict in an evaluation matrix lands its countermeasure here, with confidence and return condition.
- An idea killed by a FATAL row is recorded in *What we ruled out* with the row as evidence and its return condition attached.
- A treatment is not proven merely because its field is populated — `planned — …` is the honest declaration, and only a resolving citation is called verified (demanded at acceptance).

## Document Structure

This section describes the **large-bet** session document only — the everyday tier writes straight into the living `## Risk ledger` section of `docs/product/<slug>.md` per Tiering above, no separate document. The output is a markdown file at `docs/interrogations/YYYY-MM-DD-<slug>.md`. `<slug>` is the work slug matching `docs/product/<slug>.md` when one exists, else a kebab-case topic name. Dated because it is a session record, immutable once signed; the *living* ledger home is `docs/product/<slug>.md` — this document is how it got there. Create the `docs/interrogations/` directory on first use if it doesn't exist. Update the file incrementally after each meaningful exchange — never reconstruct it wholesale at the end. The user can read it at any point.

### Outline

```
[frontmatter]
## Scope
  ### In scope
  ### Out of scope
## Deferred
## Risk ledger
## Axis coverage
## Notes          (optional — overflow detail a cell references)
## Sign-off       (present only after signing)
```

### Frontmatter

```yaml
---
created: <ISO timestamp at session start>
last-updated: <ISO timestamp of most recent update>
status: draft           # draft | signed
topic: <short human-readable topic name>
slug: <work slug, when one exists>

# Session state — present while status: draft
current-axis: <axis under interview>
current-thread: <sub-decision being resolved, or empty>
last-question: <verbatim text of the last question asked>
adversarial-level: gather   # gather | probe | stress-test | adversarial
recitation-status:
  <risk-slug-1>: pending    # pending | recited | confirmed | pushed-back
  <risk-slug-2>: pending
---
```

`recitation-status` is keyed by **risk slug** — the kebab-case of the row's Risk cell — initialized to `pending` the moment a row is added; `{}` at document birth before any rows exist. Every ledger row must have an entry — no missing keys.

### Scope (defines project boundaries)

Scope is a boundary concept, not a tracking concept. What's in *and* what's out together define the project. Both are scope.

- **In scope** — list of axes/items the plan covers.
- **Out of scope** — list of axes/items the plan deliberately excludes. Each: item + one-line reason.

### Deferred (separate from scope — tracks timing, not boundaries)

Items in scope but pushed to a later round. Each: item + reason + revisit trigger (timeline, dependency, or condition that would reactivate it).

### Risk ledger

The ten-column table from The Ledger section above, killer rows first.

### Axis coverage

One line per in-scope axis — either `- <axis> — <n> rows` or `- <axis> — clear: <one-line basis>` when no qualifying risk was found. This replaces the old per-axis six-field sections: qualification lives in rows, not prose; this section only proves no axis was skipped.

### Canonical template

A new interrogation document begins as:

```markdown
---
created: 2026-05-02T18:30:00Z
last-updated: 2026-05-02T18:30:00Z
status: draft
topic: <short human-readable name>
slug: <work slug, when one exists>
current-axis: <axis under interview>
current-thread: <sub-decision being resolved, or empty>
last-question: <verbatim text of last question>
adversarial-level: gather
recitation-status:
  <risk-slug>: pending
---

# Interrogation: <topic>

## Scope

### In scope

### Out of scope

## Deferred

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
|---|---|---|---|---|---|---|---|---|---|
| <risk> | <yes/no> | <impact, in declared-value units> | <likelihood> | <test or analysis> | <fatal/non-fatal> | <one of the four treatments> | <named countermeasure + confidence> | <empty · planned — … · citation> | <date or condition> |

## Axis coverage
```

The template is the structural floor. Documents that do not match this shape break the resume / qualification-check / recitation logic.

**Zero-path initialization.** The template above shows a document with a placeholder row already established. In zero-path entry, the initial document begins before any rows exist: `current-axis` is empty, In scope is empty, and `recitation-status` is `{}`. As the interview proceeds and rows get added, they appear in the Risk ledger and `recitation-status` simultaneously, keyed by risk slug. `current-axis` becomes populated as soon as the first axis is under interview.

## Recitation Gate

Before sign-off can occur, do a final recitation pass. Read each ledger row back and ask the user to confirm — **row by row, not all at once**. Whole-ledger recitation is the easy-ratification trap this skill is designed to avoid.

For each row:
1. Update `recitation-status[risk-slug]` to `recited` in frontmatter.
2. Present the row: Risk, Killer?, Impact, Likelihood, Severity, Treatment, and the countermeasure or acceptance gist.
3. Ask: *"Does this row read right?"*
4. If user confirms: set `recitation-status[risk-slug]: confirmed`. Continue to next row.
5. If user pushes back: set `recitation-status[risk-slug]: pushed-back`. Re-enter the interview for that row. Graduated lean continues from where it was. Loop until user vetoes the re-entry, then re-recite that row. Repeat until all rows are `confirmed`.

Only after every ledger row is `confirmed` does sign-off become possible. This is gate (c) of the three "done" gates — the demonstration of understanding, not its declaration.

## Sign-off Ritual

Once recitation passes for all rows:

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
   slug: <work slug, when one exists>
   final-session-state:
     current-axis: <last axis>
     current-thread: <last sub-decision>
     last-question: <verbatim>
     adversarial-level: <last level>
     recitation-status:
       <risk-slug-1>: confirmed
       <risk-slug-2>: confirmed
   ---
   ```
5. **Write the `## Sign-off` section into the document body**: signed-at, signers, row count, killer count, `untreated fatal rows: 0`.
6. **Copy the ledger to its living home.** Overwrite the `## Risk ledger` section of `docs/product/<slug>.md` with the signed table (create the section if absent), so downstream reads one home regardless of tier. The signed interrogation document freezes as the dated record.

The `## Sign-off` section written into the document (signed-at, signers, row count, killer count, `untreated fatal rows: 0`) is the content the viability gate record will carry; when the entry gates are live, sign-off will also emit `docs/gates/YYYY-MM-DD-<slug>-viability.md` — same date, same slug, `-viability` suffix. Until then, the signed interrogation document is the record.

The document reads "complete as of [signed-at]," not eternally. Future revisits create new sign-off entries with new timestamps; the original signature is preserved as a point-in-time record.

## Composition with Kerd

`/kerd:interrogate` is callable from anywhere — inside a conductor session, inside a mode, or standalone.

- **Invoked mid-conductor:** return to conductor after sign-off. The co-signed ledger arrives pre-chewed at conductor's plan phase.
- **Invoked mid-mode:** return to the mode after sign-off.
- **Invoked standalone:** exit cleanly after sign-off. No further workflow assumed.

If the user says "stop" without sign-off, save the document as `status: draft` and exit. Re-invoking with the same plan-ref or topic resumes from the draft via the pause/resume mechanism in the Interview Discipline section.

## Default Axis List

A small **universal core** applies to every interrogation regardless of domain. Every axis feeds the same ledger — axes organize the questioning; rows are the output.

- **Scope viability** (whether the boundaries already declared in the top-level Scope section are coherent and complete — distinct from the structural Scope section)
- **Users / stakeholders** (who is this for; who has a say)
- **Value** (why this is worth doing; what changes if it works)
- **Constraints** (what must hold; what cannot change)
- **Risks** (what could fail; what consequences if it does)
- **Dependencies** (what this requires from outside the plan)
- **Overall viability** (the cross-axis "what must be true" set — distinct from any single risk row in the ledger)

**Domain-specific starter sets** layer on top, proposed by you based on what the plan-ref or zero-mode discussion reveals:

- *Software engineering plans:* technical design, data model, security, performance, testing, deployment.
- *Business / product plans:* business case, ROI, marketing, sales, pricing, competitive landscape.
- *Investment / financial plans:* due diligence, ROI, audit, compliance, term sheet, exit conditions.
- *Legal / contract plans:* compliance, privacy, data protection, jurisdiction, liability.

The user prunes any of these via out-of-scope/defer. Full-list-by-default is rejected as noise-generating.

## What This Skill Does Not Do

- **Does not produce the implementation plan itself.** This skill produces *qualified risks*. After sign-off, the work moves down the walk — slice a release, then design the solution — with its risks pre-chewed; they are never re-assessed there. In a Kerd session that continuation runs through `/kerd:conductor`. Boundary kept to prevent design synthesis from sneaking in too early.
- **Does not auto-detect sign-off.** You may *propose* entering recitation when known unknowns are exhausted, but you never declare the session over. User-veto on stop is absolute through to the final ritual.
- **Does not use insight blocks, structured framing, or explanation during interview.** Those belong outside interrogate sessions. During interrogation, you are question-shaped only.
- **Does not support multi-user sign-off in v1.** The signers map supports one user + one agent. Future versions may extend.
- **Does not enforce a mandatory exhaustive axis checklist.** The universal core always applies; domain-specific axes are proposed and pruned by the user.
- **Does not multiply impact by likelihood — ever.** Expected value is the wrong maths for a bet taken once. Impact sets the class; likelihood sets the response.
- **Does not write `docs/gates/` records.** The co-sign is written in that record's shape; emitting it belongs to the entry gates when they are live.
