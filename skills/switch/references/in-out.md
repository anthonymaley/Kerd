# In and Out: useful context, clean boundaries

## In

For a precise To handoff, read the entry and destination instructions in
[To and Roll](to-roll.md). Use its exact saved revision with the helper's `--commit`
option; don't replace it with “whatever is latest”. Require source-release evidence
before continuing active work. Ordinary latest-state pickup is unchanged.

A specifically named handoff takes precedence over generic pickup discovery.
Check its supplied repo, branch and record first, using only necessary local
identity checks and explicitly authorized Git synchronization. Missing or wrong:
stop before reading a legacy checklist as the task. A machine being reachable or
able to build does not prove that the intended handoff was restored. Once found,
read the handoff's authority before acting on linked project instructions; standing
project notes cannot expand a read-only trial into probes, builds or deployment.

Resolve the current project and branch. An explicitly requested Git-backed pickup
includes synchronization under the agreed Git authority. Inspect local changes,
staged work and remote identity first; preserve them. Fast-forward only when safe.
Don't auto-stash, force-reset, resolve a meaningful conflict by guessing, or quietly
claim local memory is current with GitHub when sync failed. An offline/local-only
pickup can proceed only as such, with that limitation visible.

Read the project's existing current-context/handoff pointer and selected active
work. Recover current stage, actual user agreement, last result, pending question
or next action, failure/resource state and relevant project constraints. Follow
necessary evidence links; avoid loading the full log archive and every retired
plan. An explicitly stale or contradictory pointer must be reconciled with current
artifacts and dated evidence before work continues. What makes a pointer stale is
an obsolete next action, not an old revision: `overtaken_revisions` in a pickup or
prepared packet is a diagnostic hint, and citing history or a pre-save position is
legitimate. Reach an exhaustive changed-file list with `git show --name-only` on
the named boundary rather than reading a manifest copied into memory.

Local files a project has deliberately kept out of Git do not block a pickup.
Name those exact paths with `--preserve` and the helper proceeds, reporting them
as local only; it stops, untouched, if the incoming revision carries one of them,
because that collision is a real decision. Unnamed changes still stop a pickup.

The start point names a **pickup reading set** — the exact files and complete
sections Out chose for this next action (see "Leave a lean start point" below).
Read those first, in full, and nothing else by default. It is a saved navigation aid, not a ban on further reading: check linked
detail when a contradiction or the next action requires it. Where the host can
assemble those named sources before starting the fresh worker, use `prepare`
below so the model receives their text once. Otherwise read them normally.
For a long work record, locate its current-position section before reading from
the top. Then load its named agreement and supporting sections. A supplied record
path is not by itself a reason to load every prior implementation observation.

Restore saved state; do not re-audit every citation during pickup. A current,
sourced handoff can establish what the last sitting recorded. Open supporting
history when the current record is missing, contradictory, or insufficient for
the next action or its authority—not merely because it contains a link. Keep
saved observations distinct from fresh verification. If no build is active,
there is no reason to load its whole stage history or neighboring backlog work.
When deeper retrieval is needed, read the complete relevant entry, not a broad
range of adjacent tasks; a few very long lines can still load pages of material.

Ordinary In ends with restored memory, status and the saved plan on screen, and
a Conductor session open on that place, stopped at its dashboard decision as described
below. It does not execute the plan before that approval, draft replies, start
reviews, repair files or investigate backlog issues. Keep checks to safe requested
Git synchronization and resolving facts necessary to restore position; flag other
uncertainty for the work itself. Do not measure pickup cost inside every pickup;
assess the session logs afterward unless measurement was requested. A user
explicitly asking to continue after In can proceed through Conductor without
another approval. Managed To/Roll remains separate and keeps its agreed
continuation. When neither a saved next action nor a NOW item exists, say that
no task is selected rather than manufacturing one. Existing project restrictions
still apply.

Context-cost targets come from the work agreement, not a universal magic number.
Report added input separately from host overhead where measurable. The Switch trial
uses 8,000 additional input tokens and 5% of observable usable context, plus correct
restoration. A shorter but incomplete read fails; unknown usage is not a pass.

When the caller already supplies complete current records and verified local Git
identity, use that material directly rather than discovering and reading it again.
Keep its file/section labels and saved-versus-current distinction. Supporting
links remain available for genuine gaps; a prepared pickup is not a declaration
that historical sources can never matter. The caller selects from the project's
existing memory structure, not a universal fixed list of filenames.

Before calling restoration complete, check the answer against the supplied current
records for unresolved decisions, owed work and restrictions. Keep these in the
restored working state, even when the user-facing summary only shows the next one.
Preserve explicit prohibitions, parked choices, unknowns and not-yet-authorized
actions; do not silently replace them with defaults or drop them for brevity.
Keep the short screen summary separate from retained working state. The existing
source records remain authoritative: keep their named complete selections linked,
and preserve operative conditions in source wording when a portable restoration
record must carry them. Never replace them with labels such as "settled privacy
decisions" that hide an open experience choice or an exception. Open decisions,
settled constraints and instructions for retrieving deeper detail stay distinct.
Do not create another living rules file merely to repeat the same source text.
The short display may show only the next action; it must not imply that omitted
choices are settled or that it is the complete working state.
This is a coverage check of material already loaded, not an instruction to read
the whole archive. A small input is useful only if its meaning survives.

### Load Conductor before the dashboard

Before rendering the dashboard, load the sibling [Conductor](../../conductor/SKILL.md) in
this session using the host's skill mechanism, with an explicit instruction:
“Switch In: open a session on the restored position and authority already in
context; compose the arrival decision in the dashboard and wait.” Resolve the sibling from this Switch
distribution, not another cached version. If native skill invocation is
unavailable, read its SKILL.md directly; if neither route works, disclose that
Conductor was not loaded. Do not claim successful loading merely because its
name appears in the dashboard.

Carry the restored project, selected work (or none), agreement and restrictions,
pending decision and next action forward in context; don't create another record
or re-read the pickup set. Conductor's In paragraph is the full rule for choosing
the bounded next action and composing the one decision before rendering,
including pending-question, explicit-continuation and no-task cases. Do not
append a second report or approval after the dashboard. Managed
To/Roll is the exception and keeps its agreed continuation.

### Welcome back: the screen summary

After restoration, orient before detail. Five short blocks, worded for the project:

- **Now:** the immediate work, from the bullets under the project's `## Now`
  heading (TODO.md by convention). The backlog stays behind the documents link.
- **Last session:** the main achievement or change.
- **This session:** the next agreed work and why. If none is agreed, say so; a
  suggestion stays a suggestion.
- **Where we are:** position in the wider work, in the project's own stage names,
  not the stage of the pickup itself.
- **You:** "Nothing needed right now", or the specific decision and what it
  unlocks, in Conductor's bounded question surface.

Close with the document links; the task list carries the label **Open work**
and points at the existing work/status page — HTML where one exists, otherwise
the Markdown record or task list. Resolve a real
target; don't invent a page or build one during In. The backlog and audit evidence
live behind that link. This replaces an exhaustive switch-in report and adds no
record field. Being short does not suspend the rules above: a contradiction,
failed synchronization or restriction still appears on screen.

An **Insight** is optional: one source-grounded learning, implication or tradeoff
in its own callout — never compulsory, never a hidden question.

```text
★ Insight ─────────────────────────────────────────
The draft is ready, but its benefit is not measured.
A first-reader check can test whether the instructions
actually help someone get started.
───────────────────────────────────────────────────
```

A fictional example. Rewrap to width, use ASCII rules where the star renders
poorly, and omit the callout when there is nothing useful to say.

Render it with the packaged renderer, [scripts/where_we_are.py](../scripts/where_we_are.py),
resolved relative to this skill so it travels with the package:

```sh
printf '%s' "$summary" | python3 "$SKILL_DIR/scripts/where_we_are.py" --summary -
```

`$summary` is the shape below, filled from what pickup already read. **Copy it
from here; do not open the script to work out the keys.** The example is one
coherent sitting — a task is selected, so the session names it; a decision is
genuinely open, so `question` is filled. Use `null` or `[]` for anything the work
has nothing for.

```json
{
  "phase": "Design needed — freshness alert",
  "task": "Design the freshness alert",
  "task_reason": null,
  "state": "Awaiting your approval",
  "state_reason": null,
  "now": [
    "Design the freshness alert",
    "Later: implement the agreed design"
  ],
  "last_session": "Diagnosed the pipeline outage. No alert has been built.",
  "this_session": "Proposed: design the alert. Implementation and deployment are not included in this approval.",
  "question": {
    "text": "Starting on the alert design — approve?",
    "proposed": "Decide where it runs, what it checks and how it notifies you.",
    "reply": "Approve / Change"
  },
  "documents": [
    ["Open work", "docs/work/model-ready-work/consolidation.md"],
    ["Design", "docs/work/model-ready-work/design.md"]
  ],
  "warnings": ["Publisher health is a saved observation, not rechecked during pickup."],
  "insight": "A freshness check makes an otherwise silent stop visible.",
  "source": "CONTEXT.md, TODO.md, the newest session log",
  "updated": "2026-09-10 17:34 EDT",
  "base": ".",
  "restored": "yes",
  "restore_note": null
}
```

`documents` are `[label, path]` pairs resolved against `base`; a path that does
not exist is reported as a warning rather than offered as a link. `task_reason`
and `state_reason` carry the sentence after an explicit "none". `restored` is
`"yes"`, `"partial"`, `"no"`, or omitted when no pickup claim is being made;
`restore_note` says what is missing when it is not `"yes"`.

**What the caller should supply, and what the renderer checks — they are not the
same thing.** Given a correctly shaped JSON object, no field is validated: a
missing, misspelled or null one degrades quietly, so a typo costs you a blank
line rather than an error. That tolerance is about *fields*, not about input —
malformed JSON exits 2 with a message, and a top-level value that is not an
object (an array, say) exits 1 on an unhandled error. `PHASE`, `TASK`, `STATE`, `NOW`, `LAST SESSION`, `THIS SESSION` and the
`YOU` box **always render**, falling back to "not recorded" or a plain sentence
when they have nothing — they are the frame, and a gap in them is information.
`now` is the list of bullets under the project's `## Now` heading, copied as
read; the backlog is not supplied here.
Only the attention panel, `DOCUMENTS` and the `★` insight line are **omitted
entirely** when empty. Always supply `source`: it names what the pickup actually
read, and it is the one field nothing else can stand in for.

It reads stdin, so nothing is written to disk. Do not re-read files to fill it,
and do not stop for approval before showing it. If the renderer cannot run, say
the same things as plain text; the information is the requirement, the frame is
not.

`restored` states whether the necessary context was recovered. Which presentation
ran is a separate fact: an older Switch producing the long report is not an
incomplete restore, and belongs in the attention lines if it matters at all.

## Out

Read the active state and inspect what actually changed. Preserve the current
agreement, decisions, exact next action, unresolved jobs and important findings.
Append an evidence-backed session account to the existing history; read the clock
for dates/times written now. Unknown start time stays unknown. Do not retain the
whole native conversation or private session IDs as project history.

Reconcile active work against evidence. Remove completed tasks from active lists
while retaining their completion record. Retire redundant work only with a known
reason. Keep independent sub-findings and migration-sensitive work open. Archive
historical detail with reachable links; age alone doesn't retire a decision,
dependency or risk. For an initial legacy reorganization, keep a recoverable
original. Do not rewrite dated history or maintain duplicate living plans.

Update the next session's lean start point with what is true and what to do next.
Historical decisions needed by a future feature remain discoverable by subject;
the active memory must include constraints that affect the next work. Be explicit
about unreconciled historical sections rather than calling the migration lossless.

Alongside the next action, name the small reading set that supports it: actual
files or complete sections, why they matter, and where deeper history lives.
Use the existing handoff/work record; do not add a parallel manifest or duplicate
source text. This lets the next pickup reuse the outgoing session's knowledge
of the work instead of rediscovering the entire repository. Preserve unresolved
decisions and authority even when the next action looks simple.

### Leave a lean start point

The next pickup pays for every byte the start point carries, so Out ends by
making it small on purpose, not by reading less next time. Four moves, in this
order, each leaving a reachable link behind:

1. **Rulings stay, cases move.** The loaded pointer keeps each standing decision
   as its ruling — the bold sentence and its date — only for decisions that
   govern the next work or a constraint the next sitting must honour. The full
   entry (the case, the evidence, the argument) lives in a living decisions
   record (`docs/decisions.md` by convention), newest first with an index of
   rulings so history is discoverable by subject. Superseded decisions are
   marked there, never deleted. A ruling without its case is a link, not a loss.
2. **Closed work leaves the active list with its reason.** The closure review
   already gives every open row a verdict; rows judged done or dead move to a
   backlog archive (`docs/backlog-archive.md` by convention) with the verdict,
   the evidence and the date. Open and unsure rows stay. Age alone closes
   nothing.
3. **Name the reading set in the start point** as exact files and complete
   sections, in the pointer's current-state section, with why each matters.
   The default set is the pointer, the active list's `## Now`, and the newest
   session log; add a work record section only when the next action needs it.
4. **Measure it and record the reading.** Run the helper's `measure` on that
   set and write the result beside the reading set:

   ```sh
   python3 /path/to/switch/scripts/handoff.py --project /path/to/project measure \
     --record CONTEXT.md --section TODO.md '## Now' --file kivna/sessions/<date>.md
   ```

   It counts bytes exactly and estimates tokens at four bytes each, labelled as
   an estimate; the target is the trial's 8,000 unless the work agreement sets
   another (`--target`). Over target is information: prune further under the
   rules above, or record why the set must stay larger. It never blocks a save.

The first run on a legacy pointer is a migration: keep a recoverable original
(the move itself, in Git, plus a dated note in the session log), reconcile any
conflicting current claims, and say what was not reconciled. Do not apply the
migration to an unrelated live project.

The living handoff describes the sitting that is ending, not the moment it was
written. A record states the revision observed while writing, so a boundary
commit made afterwards leaves it naming an ancestor with a next action already
done. Keep those apart: label the observed revision as the position before the
save, and let the next action be what remains after it. Never write the
resulting commit ID into a file inside that commit; name the boundary by branch
and record, and let `git log`/`git show` supply the ID. When the save completes
work the record still lists as pending, correct that record in the same
boundary. Say plainly which the handoff reached — prepared locally, committed,
or verified at the remote; a local memory save is neither of the last two.

Record the scope rule and where the boundary is, not an exhaustive file list.
`git show --name-only <commit>` reproduces that inventory on demand, so a copied
path list costs every later pickup and proves nothing Git does not already hold.
Existing manifests stay as reachable history, not required pickup reading.

Inspect pending jobs before ending a sitting. A running job is not saved merely
because its task name appears in a file. Respect existing direction on whether
it continues; a genuine unresolved ownership issue needs a decision.

Under the agreed Git authority, commit the relevant work/session files by name
and push to the intended branch. A save commits only the named files. Exact paths
the project has already decided to keep locally — a scratch patch, a stray build
artifact — are acknowledged with `--preserve`: they stay untouched and are reported
as local only, not saved. Keep that acknowledgement in the project's existing
memory as exact paths; it is not a pattern, an ignore entry or a new config file,
and it never deletes or stashes. New or unacknowledged work still needs resolution,
not blanket staging. Show locally saved vs committed vs remotely verified. A failed
push leaves useful local work recoverable; do not call that a cross-device handoff.

### Close with the saved-place box

End Out on one box that says how far the save reached, rendered with the same
packaged renderer:

```sh
printf '%s' "$closing" | python3 "$SKILL_DIR/scripts/where_we_are.py" --closing -
```

`$closing` is filled from the helper's save result and what Out just wrote.
**Copy the shape from here; do not open the script for the keys.** `saved` is
one of `remote-verified` (the helper's `saved_to_remote`), `committed` (a local
commit, push not verified) or `not-saved`; the banner and its words follow it.
An absent or unrecognised `saved` renders SAVE STATUS NOT RECORDED, never
"nothing committed": unknown is not evidence. The free-context hint follows
only a remote-verified or committed save; otherwise the box says to keep the
session open and resolve the save first. `local_only` is the helper's
`preserved_local_only`. `tree` is what remains in
the working tree after the save, in words. `next` is the exact next action the
start point names, `reading_set` the files and sections it names, `measured`
the helper's `measure` reading. Use `null` or `[]` for anything Out has nothing
for; a missing field renders as "not recorded", never as a claim.

```json
{
  "project": "Kerd",
  "branch": "main",
  "saved": "remote-verified",
  "commit": "2e59ab7",
  "files": 15,
  "remote": "origin/main",
  "local_only": ["kerd-laptop-result.patch"],
  "tree": "clean",
  "closed": "2026-09-12 12:40 EDT",
  "next": "Run one real Conductor session on 0.112.0 and confirm a Claude player is a native subagent.",
  "reading_set": ["CONTEXT.md", "TODO.md ## Now", "kivna/sessions/2026-09-12.md"],
  "measured": "23,482 bytes, about 5,871 tokens estimated at four bytes each, within the 8,000 target",
  "log": "kivna/sessions/2026-09-12.md"
}
```

The box distinguishes saved locally, committed and remote-verified in words,
names local-only leftovers and an unclean tree rather than hiding them, and
ends by saying the session is still open with the free-context hint. It never
says the session exited or the context was cleared: a save is a Git fact, and
only the person's `/clear` changes what is on screen. If the renderer cannot
run, say the same things as plain text.

## Default verified save when pushing is authorized

For an authorized commit-and-push Out, use `handoff.py save ... --push` by default.
Its successful remote check is the evidence for saying the save reached GitHub;
an attempted push or stale local tracking ref is not. Local-only Out remains a
valid choice and does not require GitHub access or new push permission.

If the helper cannot support the agreed workflow, explain the limitation. A
manual route must retain explicit file selection, existing-index protection and
verification that the intended remote branch contains the exact saved tip before
claiming remote success. Report use of that fallback. Do not sweep unrelated
changes into a commit or replace an unsafe checkout to make the helper pass.

Resolve `scripts/handoff.py` from the skill directory. Example shapes, not literal
commands to run against a guessed project/branch:

```sh
python3 /path/to/switch/scripts/handoff.py --project /path/to/project save \
  --branch trial-branch --file CONTEXT.md --file TODO.md \
  --file path/to/session-log.md --message "Save the working place" --push
python3 /path/to/switch/scripts/handoff.py --project /path/to/project pickup \
  --branch trial-branch --record CONTEXT.md --sync
python3 /path/to/switch/scripts/handoff.py --project /path/to/project prepare \
  --branch trial-branch --record CONTEXT.md --section TODO.md '## Now'
```

List actual changed files, including any archive files; the helper refuses unassigned
changes or an existing staged index. It won't check out a different branch for you.
The loaded record is only the entrypoint: follow its relevant context links and
verify the next action. It is not a parser-based declaration of complete memory.

`prepare` is an optional caller convenience: it returns local Git identity and
raw, source-labelled records together for a fresh reader. Repeat `--file` for
complete files or `--section FILE '## Exact heading'` for complete Markdown ATX
sections, including child sections. Prepared sources must be Git-tracked UTF-8
text; their line endings are preserved. Missing, empty or ambiguous selections fail;
it does not guess replacements. Conductor chooses from the project's actual
memory structure. The helper does not select relevant sources, write a second
memory file, start a session or grant permission. Without `--sync` it is local-only.
