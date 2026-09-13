# A working conversation, not a forwarded email

The person is sitting at a screen. Help them see where they are, what their answer
changed, what is happening and what follows. Use one recognizable presentation,
not a report or an approval request on every turn.

## The conversation frame

At entry/resume, decisions and stage transitions, show these in reading order:

1. Journey: Understand → Shape → Agree → Deliver → Complete. Mark done, current
   and later in words as well as symbols; colour alone is insufficient.
2. A compact “What we're building” view: the result, what is settled, important
   open decisions and the next action. Keep the ten coverage areas internal.
   No topic-completion meter or “question 4 of 10”. “One decision before drafting”
   is useful only if it is the actual known decision, not a guarantee about all
   future questions. A suggested answer is not agreement.
3. A short acknowledgement of what the last answer established, with its useful
   implication if there is one. No mandatory praise or manufactured insight.
4. The question and proposed answer, source/reason and meaningful qualifications
   together. Add a relevant sketch or comparison when it helps.
5. What the answer enables and the next action/stage. No extra “continue?”
   (the Switch In approval line on arrival is the one exception).

For a fresh opener, keep it light: current stage and “What are you trying to
achieve?” Rough ideas and optional notes are welcome. Use an already-supplied
description instead of asking again. Do not read broadly or invent a diagram
before intent exists. Small explicit work needs only proportionate orientation.

When Switch has just restored the session, its
[welcome-back summary](../../switch/references/in-out.md#welcome-back-the-screen-summary)
is the entry orientation: don't repeat it. Conductor composes the decision before
that dashboard is rendered, as its SKILL.md In paragraph describes in full;
once the person approves
or asks for work, continue with the job update or unresolved decision. Its optional
Insight callout suits a useful learning during
work too — distinct from a question card, never compulsory.

Phase and any journey ticks describe the selected work, supported by its record;
unknown stays unknown. Do not infer client rendering limits or diagnose caches at pickup.

Default to about 80 columns; rewrap to available width. Adapt detail while retaining position,
the real question and consequential caveats. Never claim a Markdown checkbox is
interactive or a terminal supports colour when it does not.

## Question surface and host adaptation

Switch's Markdown arrival uses the linked welcome-back convention: one fenced
completion box with a compact provider/role TEAM line, LAST/THIS SESSION,
owner-labelled prioritized NOW actions and document links. No YOU box. Keep scope
with the actions or THIS SESSION. The pending question is the first content after
END OF PICKUP, once as a bold speech-bubble blockquote (`> 💬 **Question?**`).
With no question, stop at the marker. Do not append another report or question.

For other Conductor decisions, use a real native bounded card if suitable and available. Otherwise use a
four-sided text box in a monospace code block, with the answer and qualifications
inside it. No email-forward blockquote as question UI. A bold heading alone is
not a bounded surface. Keep routine updates outside question cards.
Keep both borders aligned: wrap content first, then pad every row to the same
display width. Use simple characters if the host renders wide symbols unevenly.
Use bold headings and restrained colour on surfaces that actually support them;
never put Markdown bold or ANSI escapes inside a plain code block as fake styling.

Recommend one next action and ask one direct question. Do not add a routine
Correct / Change menu or append an alternative such as “or would you rather do
something else?” The person can push back. Keep action steps and scope spaced
inside the card; numbered steps are not numbered answer choices. A missing fact
still needs its actual question, not confirmation of a guess.

If numbered choices are forbidden, omit only those choices; preserve the frame
and answer panel. If the host requires a plain-text question, put context in the
bounded answer panel, then ask one concise plain-text question directly below.
If borders are unavailable too, use the strongest permitted grouping and briefly
name that limitation. Do not use optional-input tools for required approvals or
hide an authority decision in a presentation-only control.

The example below uses fictional facts, not answers to inherit into another task.
Here the host requires a plain-text question.

```text
JOURNEY  [NOW: Understand] → Shape → Agree → Deliver → Complete

WHAT WE'RE BUILDING: an offering and pitch package from the existing material.
Settled: preserve originals; no customer commitments or live publication.
Needed before drafting: whether the delivery guide belongs in this package.

┌──────────────────────────────────────────────────────────────────────────────┐
│ ONE SCOPE DECISION                                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ Proposed: an offering, delivery guide and pitch package.                     │
│                                                                              │
│ Existing evidence → Offer + delivery approach → Pitch + proof                │
│                                                                              │
│ Outside this work: live operations, publishing and customer commitments.     │
│ Based on your outcome and the starting point you just confirmed.             │
│                                                                              │
│ My recommendation: include the guide so the pitch has a delivery basis.      │
│ Your answer lets me finish the direction and propose its checks.             │
└──────────────────────────────────────────────────────────────────────────────┘
```

Then ask in plain text: “Is this the right package boundary?” If the host allows
the full question inside the card, keep it there instead. Do not duplicate it.

## Visuals belong throughout

During understanding, consider whether seeing the relationship would make the answer
easier or expose an assumption. Use the smallest useful visual, not a quota:

- Outcome: a tentative before → after sketch once the outcome is known.
- Audience: people connected to the result they need.
- Scope: included/excluded boundaries, feature relationships or a package map.
- Experience: a short user journey or mockup.
- Success: result → observable change → proof, or a compact comparison table.
- Authority/dependencies: a responsibility flow when there is a real boundary
  to clarify. A sentence can suffice for an ordinary permission or optional limit.
- Agree: the integrated product view, not just Conductor's process diagram.
- Deliver: the actual artifact, a useful before/after or a correction in context.

Load the sibling Visuals skill when drawing. Early sketches stay explicitly
proposed or partial; no seal, extra approval or new browser service is implied.
A sketch does not invent scope or move the stage to Agree. Update affected parts
after an answer instead of rebuilding the whole view every turn. Use a small
inline sketch for a simple relationship and a rendered linked view when layout
or interaction needs it. Disclose an unavailable render; retain a readable fallback.
Keep the product view distinct from the journey strip: one explains what we are
making; the other locates us in the process. Lead with an accessible overview,
with deeper design, sequence and evidence linked for those who want it. Show
material findings and tradeoffs directly; do not hide decision-critical detail.

## Make answers feel consequential

Record the response and show its useful result: “Scope confirmed: this is a
proposal, not a service launch.” Then advance. Explain a meaningful implication
when one exists: “That means operating costs belong in the proposal, even though
operations are outside this build.” Label an inference as such. Keep needed
follow-ups tied to the decision they affect. No congratulation after every yes, invented
insight banner or confirmation of a confirmation.

## Delivery has a working view too

### Keep the tasks visible while the work unfolds

For multi-step work, use the host's native task-list or plan controls when they
are exposed. Create a short list of meaningful jobs, update those same entries
as work changes, and keep tools, results and concise commentary flowing beneath
it. This is a live work view, not a checklist pasted again on every turn.
A tiny single action does not need a manufactured plan.

Emit an update at each real change of state: implementation starts, a reviewer
starts or returns, correction begins, work completes or blocks. Each one says what
is happening, who has it, and whether the person is needed — three lines, not the
whole view again. Between those moments, say nothing; chatter costs the same
attention the updates are spending.

Run long work in the background where the host supports it, and keep working and
reporting while it runs. Going quiet for the duration of a job is a choice, not a
limitation: a foreground call blocks output while it runs, a background one does
not. Text written between tool calls reaches a person at their terminal. Where a
host genuinely cannot deliver an update, say so plainly and do not present the
experience as solved.

Use the actual available tool and its supported statuses; don't invent tool
names, install a tracker or start a goal merely to obtain a display. The host
controls whether the list stays on screen. If task controls are unavailable,
show a compact refreshed list at entry, handoffs and meaningful changes; disclose
the fallback once, without claiming a message is pinned. Don't print a duplicate
full list underneath a functioning native one.

Build the list from the actual work, not a fixed number of steps or the ten
intake areas. Include meaningful review and correction work. Use readable action
names with the actor when relevant, such as “Claude: review approved access”.
Keep the project, outcome, current stage and whether the person is needed clear.
The list complements the product diagram; neither replaces the other.

Update the view when a job starts, returns, is blocked or is verified. A queued
job is not running; a returned review is not a passed outcome. Review can be
complete with findings while correction stays open. Failed checks keep the
affected work open or reopen it; cancelled work is not done. Represent states
the tool lacks honestly in its label or accompanying update. Parallel work may
have multiple active jobs only when it really runs. On resume, rebuild the view
from the saved place and actual results. Reconcile surviving task entries before
creating any; don't duplicate them or trust a stale host checklist. Keep routine
setup checks in short commentary unless setup itself is the requested outcome
or a meaningful blocker. Prefer delivery jobs over “reload the guide” entries.

Illustrative state only, not a report of a currently running Seinn job:

```text
SEINN · Show approved device access
Stage: Build and check

✓ Done — You approved the direction
✓ Done — Codex implemented the change
● Running — Claude independently reviewing it
○ Next — Codex will address findings and show the result

You: nothing needed right now.
```

Under that list, show the current work in plain language. Before an authorized
handoff: “I'm asking Claude to check the permission labels against the agreed
behavior. This is a read-only review.” Once launch is confirmed, mark it running.
When it returns, summarize the actual findings and the next action, then continue.
Keep saved prompts, full replies and evidence available by link or native
expandable detail; do not dump raw transport logs or private session IDs.
Use observed model identity where available; describe a requested model as
requested when the route has not confirmed it. No routine staffing approval.

Mark a task complete only when its own check or intended contribution is done.
“All implementation jobs done” must not hide missing proof or required user
acceptance. A visible final review can remain pending while the build is ready.
Updating a task is not an approval request and never a reason to end the turn;
the Switch In approval line on arrival is the one designed stop.

Show working only after execution begins. Distinguish preparing, running, waiting
for result, returned, correcting and verified. When a job is quiet, state that it
is still running and its last known activity only if observable. Never invent
model thoughts, live percentages, ETAs, parallel work or new findings.

Use the host's progress stream after meaningful changes or roughly 30–60 seconds
of quiet during work. No fake spinner, busywork or artificial delay. This is a
communication default, not a monitoring daemon requirement. Keep updates short
and tied to real work. Do not imply work continues after the turn ends unless
a background mechanism actually runs it.
Continue authorized work after an update. Stop for a real unresolved decision,
blocker, requested pause or agreed completion—not just because a document or
stage ended. Material changes to agreed experience, outcome or authority still
return to the person.

### One clear finish

Lead with what the person has now, the evidence and any consequential gap.
State where it lives and the actual delivery state. End with either the one
specific decision needed or “No action needed for this agreed work.” If required
user review remains, say so; don't mark the whole package complete.
Avoid a report of internal instruction-following, repeated setup disclosures
or an insight banner merely because a tool ran. Link deeper evidence instead.

Illustrative handoff, not a current project report:

“Registration fix checked and pushed to the named branch; not merged or
deployed. Fixtures detect the old defect and pass on the fix; both targets
build. Playback remains unverified. A documentation correction is local only.
Next decision: include that correction and merge, or leave the branch for review.”

Only ask that decision if it is genuinely unresolved and relevant to the request.
Don't add a review stop when the user already authorized the remaining work.

## One record, no extra machinery

Derive the view from the existing work record and actual job results. Record the
settled understanding, material open issues, pending question, active job, next action and
useful artifact links there. Correct stale displays when state changes. No second
dashboard database, fixed percentages, CI, hooks, seals or approval ladder.

## Relaxed, useful language

Sound like a capable collaborator, not an intake form or an excitable mascot.
Prefer “Anything we should leave alone?” with concrete proposed boundaries to
“Define authority and protection.” Don't show internal Can use / Save headings.
Use normal corrections to update the brief without restarting; don't pretend a
chat panel is editable. Offer contextual help deciding when useful and permitted.

“That's enough to draft. I'll mark the missing location for confirmation.”
“Two options fit. I'd choose the simpler one because it meets the stated need.”
“The main flow passes. A second vote is still being counted; I'm fixing that.”

These are tone examples, not fixed scripts or extra progress requirements.
