# A small record that survives the conversation

Write in the person's language. Use only the detail this work needs; these
headings are a writing aid, not a parser contract. If the project has a suitable
record, update that instead of making a second source of truth.

Start after intent is known. During understanding, leave undecided matters
clearly undecided. An incomplete draft is useful; invented certainty is not.

```markdown
# Work: <outcome>

## Direction
<Who this is for, the desired change and deliverables.>
View: <relative link, when created; proposed until agreed>

## Worth it and design
<Whether it can work and is worth doing, and what sets it apart. How the solution
will work, with its view. Leave out what is not settled yet; never invent it.>

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
