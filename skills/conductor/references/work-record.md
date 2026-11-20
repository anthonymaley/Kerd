# A small record that survives the conversation

Contents:

- The record template and how to keep it: headings as a writing aid, the risks section, score-and-delivery lines
- [Record agreement and carry the work forward](#record-agreement-and-carry-the-work-forward): where the record lives, capturing agreement, the next authorized action, status requests and save or pickup
- [Keep the chief of staff's queue table](#keep-the-chief-of-staffs-queue-table): only when Switch In reported a chief of staff on; the five moments, `cos.py write` and its exit codes

Write in the person's language. Use only the detail this work needs; these
headings are a writing aid, not a parser contract. If the project has a suitable
record, update that instead of making a second source of truth.

Start after intent is known. During understanding, leave undecided matters
clearly undecided. An incomplete draft is useful; invented certainty is not.

**Save how they want it.** When the person says how much technical detail they
want, less (“keep the technical stuff out of my way”) or more (“show me the
commands”), write it, in their words and dated, on the record's `How they want it:`
header line the same turn, so a fresh session reads it before it speaks. Only words
they said go on that line; an impression that they are not technical shapes this
sitting's language but is never saved as their preference. Keep it when the stage
changes; when they change their mind, replace it with their new words. (First-user round 5, 2026-11-14: “keep the technical stuff
out of my way” was saved nowhere, and the next sitting opened on a stage label.)

```markdown
# Work: <outcome>
How they want it: <a standing preference in the person's own words, such as
"keep the technical stuff out of my way"; leave the line out when none was said>

## Direction
<Who this is for, the desired change and deliverables.>
View: <relative link, when created; proposed until agreed>

## Worth it and design
<Whether it can work and is worth doing, and what sets it apart. How the solution
will work, with its view. Leave out what is not settled yet; never invent it.>

## Risks to keep in view
<One line per risk: the risk in a plain sentence, what is being done about it or
"accepted", and the date it was named. Leave the section empty when nothing has
been named; never invent a risk to fill it.>

## Success and proof
<Desired benefit, observable results, what is good enough and how an independent
reviewer can assess it. Distinguish agreed criteria from proposals and unresolved
questions; identify the user input or response establishing agreement. A list of
functional tests alone does not establish the person's definition of success.>

## Boundaries and decisions
<In/out; what may be decided or changed; consequential questions still open.>
<Where useful: Must / Prefer / Open, with a basis for hard requirements.>
Time/resources: <what was actually stated or agreed; unknown if unresolved>
Stopping point: <what counts as finished; external publication only if authorized>

## Agreement
Not yet requested / awaiting response / agreed with these conditions.
<After agreement: the actual user response, the direction it refers to,
and conditions. Do not fill this from an example or an agent's recommendation.>

## Decisions and changes
<Significant decisions, sources and changes, with reasons. Preserve previous
agreement distinguishably; a draft update is not a new user decision.>

## Now
Stage: Understand / Shape / Agree / Deliver / Complete
Current activity: <what is happening, not a percentage guessed from documents>
Analysis so far: <key findings, evidence, recommendation and remaining uncertainty>
Current understanding: <settled intent, source/status and actual decisions>
Open issues: <what is unknown/proposed, when needed and how it will be resolved>
Pending question: <exact user-visible wording, or none>
Decision context: <which part of the outcome it affects and what the answer enables>
Next action: <specific next action and who owns it>

## Score and delivery (when used)
Score: <relative link to the current score, or none>
Current passage: <stable score-step identifier/link, or none>
Assignment: <step author (Conductor/composer); performer (player/controller); actual
route, owner and disposition>
Fit: <the Fit line for each selected model job and any model/effort/route change>
Settings: <requested model and effort per job, and the observed model and effort
from `job_evidence.py` or the route, or "unverified" with its reason>
Review plan: <reviewer, recorded cadence and the gates it protects; reviews done
and whether a later change reopened a gate; or none planned and why>
Change read: <per return, the `Change read ·` line against the recorded baseline>
Evidence: <what was returned, checked, failed or remains unproved>
Repair/attempt state: <affected passage, unresolved repair and cumulative relevant
attempts, or none>

## Results and evidence
<When available: what was actually checked and what remains unproved.>
```

Save the question before asking it. Once answered, record the decision and
replace the pending question with the next one, or the next action. A fresh
reader should not have to infer which of several old questions is still live.
Keep understanding with the relevant brief content, not duplicated in a separate
questionnaire. The ten internal areas need no ten headings, counters or empty fields.
Distinguish user-stated/sourced/proposed/confirmed/explicitly absent/unknown where
it matters; a source is not new permission. An old topic number need not be shown
on resume. Keep its answers and the actual pending decision, not a mandatory sequence.
Drafting an answer does not advance progress; record the person's actual response.
Keep changed authority in time order: what was authorized and done, and what is
allowed next. A later restriction is not an instruction to undo earlier work.
Record relevant delivery facts (local, committed, pushed, merged, deployed) and
remaining gaps separately from the agreed completion state. Retire completed
backlog entries within scope, preserving still-open clauses and evidence links.
A native task list is a display, not the only home of a pending decision.

The risks section keeps risks in view; it is not a ledger and it gates nothing.
Write a line when the person or the work names something that could sink the work
or hurt later, with what is being done about it or that it is accepted as it
stands, and the date it was named. No sizing, columns or tiers. Read the list
back before Ready and before the goal check, and say which risks are still open.
An empty list is fine.

Use the optional score-and-delivery lines only when a score helps this work; they
are not a second tracker or required schema. Keep the score link and its current
passage resolvable, but do not duplicate the complete score step as a new prompt
artifact. Record who wrote each step (Conductor or an actual composer call) and each player
assignment, with
requested and observed model/effort facts kept distinct. Keep transport-only
supplements or private requests identified by location and access boundary rather
than copied into the record. A submitted request is not running, a returned
result is not checked, and a failed check is not repaired merely because a new
request was sent. For a score defect, record the affected passage, discrepancy,
evidence and repair disposition; retain the cumulative relevant attempt state
without treating a renamed request as a reset. Preserve the actual agreement,
pending question and delivery facts while repair is unresolved.

Keep links relative within the work package. Don't copy credentials, private
session routing data or an entire conversation into the record. A reference
to restricted material is preferable to exposing it. If progress cannot be
saved, say so and offer a compact handoff; don't promise reliable resume.

Preserve any explicit planning-only stopping point. Otherwise, actual agreement
and authorization lead into delivery, not an artificial handoff.
The record must not claim the solution is built just because direction is agreed.

## Record agreement and carry the work forward

Keep one readable record per work package, normally
`docs/work/<short-work-name>/work.md`, or `notes:<short-work-name>/work.md` in
the private vault repo when `kivna/vault.json` sets `work_notes`; use a suitable
existing location instead when the project already has one. Name
`<short-work-name>` from the person's own words for the work (“the launch brief”
→ `launch-brief`), never a label they have not used; first-user round 3
(2026-11-14) put a brief in `docs/work/overture/`, and the person had to ask what
“overture” was. The record, its diagrams and supporting detail stay in the
record's own location (the work folder, or the vault when `work_notes` is set). A deliverable the person will use themselves (a brief, a plan, a letter)
goes beside their own files, where they would look for it, unless they name
another place; code goes where the project keeps its code. Say where it is in
plain words. Read
[the writing aid](work-record.md)
when first saving work. It is not a required schema or a condition for permission.
Keep diagrams and any necessary supporting detail with this record.

Update it as the conversation progresses, including the exact pending question
or next action before each pause. When the person approves or answers, rewrite in
that same turn the record's position and header lines (stage, current activity,
pending question, next action, and any line saying something is not yet approved)
and every field marked pending or asked that the answer resolves, so it never
still reads as waiting on what they have already given. A “settled” note appended
below while those lines still say otherwise leaves the record stale. (Round 3:
“Waiting on the owner's reaction” stayed after he approved; round 4: “Drafting the
brief itself is not yet approved” and “Format they will read it in: ASKED,
pending” stayed after he approved and answered.) Capture the actual agreement response and
its conditions; no invented approval or timestamps. An earlier discussion,
draft or example is not the person's agreement to this direction. Preserve
previous agreement when recording a material revision and its reason. Revisit
the changed decision, not every unaffected detail. No hashes or fingerprints.

After agreement, use [the work entry](entry.md#enter-work-not-another-pickup) and perform
the next authorized action in this turn. Don't end with “next is implementation” or “ready for implementation”
when implementation is authorized and possible. Interpret a brief “okay” or “go”
against the live decision, not an older suggestion or arbitrary backlog item.
For repeated instructions, changed limits or a finished task, use the delivery
guide's [reply handling](execution.md#resolve-the-reply-against-the-current-work).
If execution is genuinely unavailable or outside the agreed scope, state the
exact boundary and save an honest handoff.

For status requests, give the stage, current activity, open issue and next
action from the record and actual artifacts. Distinguish reported work from
verified results. No commit, board render or CI result is required to save or
resume. Do not commit, push or publish just to finish a status request.

For an explicitly requested session save or pickup, use
[Switch](../../switch/SKILL.md). It carries a work pointer and session
history, not another copy of the plan. Do not assume a local save transferred
native model sessions elsewhere.

## Keep the chief of staff's queue table

This section exists only when this sitting's Switch In reported `chief_of_staff`
on: its `prepare` or `pickup` output carried `"on": true`. With the signal off or
absent, none of this exists and nothing is said about it: a cold start (Conductor
with no Switch In this sitting) and a hand pickup (Switch In done by hand, or from
records the caller supplied) carry no signal, so the chief of staff is off for that
sitting. Conductor then never calls `cos.py`, never touches a `### Queue` block and
never mentions a chief of staff. A config added mid-sitting takes effect at the next
helper-run Switch In.

When it is on, the project's `TODO.md` `## Now` opens with a ranked `### Queue`
table that the chief of staff reads on its own scans. Conductor keeps it at five
moments: when it **adds** a task, **starts** one, **finishes** one, when one
**slips or blocks**, and when it **reorders** tasks. At each, it writes the whole
table, never a single row, by calling

    python3 <switch skill dir>/scripts/cos.py write --project P [--scope S]

with the full rows as JSON on stdin. `<switch skill dir>` is the Switch skill
beside this one (`../../switch` from this guide); `P` is the project's absolute
path, and `--scope S` is passed when the project is a scoped folder, as Switch
passes it. Rank is the array order, so a reorder is just the new order:

```json
[{"id": "cos-support", "task": "Chief-of-staff support", "link": "notes:chief-of-staff/design.md", "outcome": "Optional table and role, trialled in Kerd", "status": "in progress", "qualifier": "review", "eta": "~1 sitting", "depends": []}]
```

- `id` is a short slug written once and never changed or reused in the project:
  lowercase letters, digits and hyphens, at most 40 characters, no names of people
  or secrets. `status` is `queued`, `in progress` or `blocked`, with an optional
  short `qualifier`. `eta` is a plain estimate or empty for `unknown`; no invented
  precision. `depends` lists ids in the same table.
- There is no `done` status. Finishing a task means writing the table without its
  row. Before writing a table without a finished row, record the completion in that
  task's own record (its work record, or the record its Task cell links): what
  finished, the evidence and the date. The session log stays Switch Out's. This
  step is model-followed; nothing checks it.
- Never edit the `### Queue` block by hand: it is written only through `cos.py
  write`, which validates the rows, stamps `Updated:` from the clock and touches
  nothing else in `TODO.md`. Other Now lines are edited as today.
- Exit 0: written. Exit 2: the rows are invalid; fix what it names and write again.
  Exit 3: the chief of staff was switched off (config removed, project skipped or
  opted out): say so once, in one plain line, and stop updating the table for the
  rest of the sitting, with no further `cos.py` calls. Exit 4: `TODO.md` is
  missing or has no `## Now`; say so once and leave the table to Switch Out. Exit
  5: `TODO.md` changed underneath; re-read `TODO.md` and retry once, and if it
  fails again, say so and leave the table to Switch Out.
- `docs/work/queue.md` is not Kerd's: Conductor never writes it and never reads its
  contents. A project that keeps one by hand keeps it; choosing between the two
  lists is that project's own decision, never Kerd's.
