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

If that start point names a pickup reading set, use its complete files/sections
first. It is a saved navigation aid, not a ban on further reading: check linked
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

For an active authorized build, continue without a new permission ceremony. If
there is no active task, show that honestly and the next unresolved decision or
obligation; don't select a new product feature by assumption. A status-only request
stays read-only. Ordinary pickup is not permission for production probes, device
tests, messages or deployments. Project-specific restrictions still govern them.

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

### Welcome back: the screen summary

After restoration, orient before detail. Four short blocks, worded for the project:

- **Last session:** the main achievement or change.
- **This session:** the next agreed work and why. If none is agreed, say so; a
  suggestion stays a suggestion.
- **Where we are:** position in the wider work, in the project's own stage names,
  not the stage of the pickup itself.
- **You:** "Nothing needed right now", or the specific decision and what it
  unlocks, in Conductor's bounded question surface.

Close with **View tasks and details**, linking the existing work/status page —
HTML where one exists, otherwise the Markdown record or task list. Resolve a real
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

Pass the summary already assembled during pickup — phase, task, state, last and
this session, any pending question, the documents the context already names, and
`restored`. It reads stdin, so nothing is written to disk. Do not re-read files to
fill it, and do not stop for approval before showing it. If the renderer cannot
run, say the same things as plain text; the information is the requirement, the
frame is not.

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
