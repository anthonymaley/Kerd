The controller has already checked local Git identity and assembled the complete current sources below using the candidate handoff helper. Use those supplied records directly; do not repeat discovery or checks already performed. Open supporting sources only for a genuine gap. Attribute supplied verification to the controller. Preserve unresolved decisions, owed work and explicit prohibitions in your restored state. Carry each explicit prohibition from the loaded current records with its scope, using the source wording where paraphrase would weaken it. A concise user-facing display must not replace the working rules.

# Local-only Switch-in measurement

Restore Seinn's saved position in this isolated clone using the candidate Switch
instructions below. This is a NEW local-only memory measurement on the Studio,
not execution of the historical Studio-to-laptop handoff. The laptop check already
completed. Any old device-handoff instructions are historical evidence, not a
request to repeat that trial or to move this session.

The controller pinned this checkout to the tested revision
2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83. Verify necessary local Git identity and
clean state, then start at CONTEXT.md. Follow relevant sources to establish the
actual position and next work. Choose efficient reads; fully read selected files
or explicitly selected complete sections. Do not call truncated output complete.

Read-only, local files/Git only. No fetch, remote check, readiness check, build,
tests, device/playback/SSH probe, messages, source edits, new tasks, delegation,
native session histories, installed skills or extra app tools. Do not turn a
recorded obligation into permission to execute it. There is no user question
pending for this memory test and no time/spend cap was set. Stop after restoration.

Return one concise JSON object with: position (including active-work status),
last_completed, next_obligation, next_decision, authority, unresolved_memory,
and reads. Cite the source file and section for factual answers. Distinguish old
observations from fresh verification. List complete files/sections actually read
and any incomplete retrieval. Do not claim a token-budget result; the controller
measures native usage independently.


## Candidate Switch skill — complete

---
name: switch
description: Save, restore or move repo-based work between sittings and devices, or Roll an authorized Conductor build into fresh context. Handles useful memory and explicitly authorized Git handoffs; distinguishes closeout from exact mid-work continuation.
---

# Switch — development candidate

Keep the work continuous while leaving room in the next context window. Work in
the person's project, not this skill's directory. Identify the candidate briefly.
Do not invoke installed Switch or the old gate/mode machinery to run this version.
No CI, custom hooks or plugin installation is required. Existing host permissions
and repository boundaries still apply.

## Pick the intended action

- **In:** restore current repo state and useful memory; continue the exact
  authorized action. Read [pickup and closeout](references/in-out.md).
- **Out:** close this sitting well: record history, tidy active work and prepare
  the next session. Read [pickup and closeout](references/in-out.md).
- **To:** save the exact mid-work position through GitHub, relinquish source
  control and restore at the destination. Not full Out. Read
  [precise handoff and Roll](references/to-roll.md).
- **Roll:** preserve an active Conductor build across a fresh context window,
  without a new interview or routine go-ahead. Read
  [precise handoff and Roll](references/to-roll.md).

Honor the named action. Don't infer In/Out from a dirty tree, or perform a boundary
when the person asks only about its design/status. Ask only when the requested
action or target is genuinely ambiguous. A new window does not grant new authority.

For a named handoff or trial, resolve that record and any supplied repo/branch
before ordinary project pickup. A missing or mismatched handoff is not a fresh
start: report the mismatch and stop. Do not substitute a familiar Switch flow,
project readiness check or operational task. If the person supplies only a trial
name and no record can be located, request its location rather than infer its work.

## One useful memory of the work

Use existing project context, active-work records and history; don't introduce a
parallel TODO, plan or dashboard. Save the current position, actual agreement and
limits, relevant evidence, unresolved questions/jobs and exact next action. Keep
failure counts and resource accounting across windows. Link source detail instead
of copying the same narrative into several files. Missing information is a gap,
not permission to invent memory or assume acceptance.

Historical records stay reachable and unchanged. Completed work can leave the
active list without erasing decisions that still govern new work. When reorganizing
legacy memory, preserve a recoverable original and reconcile conflicting current
claims. Do not silently apply a candidate migration to an unrelated live project.

## Make the transition visible

Show actual state: saving → saved locally / pushed → restoring → continuing, or
the specific blocker. Link the saved place. Distinguish planned, running, returned
and verified work. Don't claim a file save exited a session, moved a process or
proved full restoration. No fake activity or progress percentages.

An active Conductor build resumes its next authorized action in the same turn
through [candidate Conductor](../conductor/SKILL.md). Restore a pending question
with its shown answer using Conductor's journey layout. Apply a new answer already
given rather than asking it again. A completed/inactive project does not become
a new build merely because In ran. Never stop only to ask “start Conductor?”

Keep pickup selective and explicit: fully read the chosen current working set,
then relevant historical entries as needed. Don't silently truncate records or
claim that small output means low input. Measure instructions, memory and tool
output when testing context cost; disclose unavailable readings.

## Implementation boundary

[Git helper](scripts/handoff.py) supplies explicit-file save, safe fast-forward
pickup and optional assembly of caller-selected current records. It does not
choose what is done, select relevant memory, grant authority or control sessions.
[Roll helper](scripts/roll.py) manages fresh CLI runs through the existing model
connection. It does not take over arbitrary already-open interactive sessions.
Read the relevant guide before running either. Unknown outcomes stop automatic
relaunch; tests do not make this an enforcing security boundary.

For a concise read-only view of a managed run, use
`python3 /path/to/switch/scripts/roll_status.py --project /path/to/project`.
It shows recorded state, next action and completed-worker history without private
session IDs. This is recorded progress, not a live health probe or quality verdict.


## Candidate In/Out reference — complete

# In and Out: useful context, clean boundaries

## In

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
artifacts and dated evidence before work continues.

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
When producing a saved restoration report, carry each explicit prohibition from
the loaded current records with its scope, using source wording where a paraphrase
would weaken it. A concise display is not a replacement for those working rules.
This is a coverage check of material already loaded, not an instruction to read
the whole archive. A small input is useful only if its meaning survives.

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

Inspect pending jobs before ending a sitting. A running job is not saved merely
because its task name appears in a file. Respect existing direction on whether
it continues; a genuine unresolved ownership issue needs a decision.

Under the agreed Git authority, commit the relevant work/session files by name
and push to the intended branch. Unexpected or already-staged work needs resolution,
not blanket staging. Show locally saved vs committed vs remotely verified. A failed
push leaves useful local work recoverable; do not call that a cross-device handoff.

## Optional Git primitive

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


## Controller-prepared sources and local identity

```json
{
  "status": "pickup_prepared",
  "branch": "kerd-switch-trial-20260906",
  "commit": "2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83",
  "clean_at_check": true,
  "synchronized": false,
  "sources": [
    {
      "file": "CONTEXT.md",
      "selection": "complete file",
      "content": "# Seinn — current pickup (isolated Switch trial)\n\nThis is a trial replacement on kerd-switch-trial-20260906, not the live main\ncheckout. The complete prior context is preserved verbatim in\n[CONTEXT-before](docs/work/switch-trial/archive/CONTEXT-before.md); the prior task\nlist is in [TODO-before](docs/work/switch-trial/archive/TODO-before.md). Original\nsource line numbers below refer to those unchanged snapshots. Dated session logs\nare unchanged. No historical permission is renewed merely by this pickup.\n\n## Where we are and what to do now\n\nSeinn is repo-based client/server work with Apple clients and a Python media\nagent. The latest saved sitting is [2026-09-06](kivna/sessions/2026-09-06.md).\n**Nothing is in flight. No active Conductor build is awaiting continuation.**\nThe device rollout is 4/4 complete, build 339 was read from Settings and agent\n2.3.1 was deployed. These are observations from that sitting, not freshly probed\ndevice state. Do not reopen pairing, T4, or the completed playback verification.\n\nSherpa remains Build, stage 4 of 5. Finishing the rollout did not supply the\nmissing Build-exit ruling. See latest log lines 104–108 and kivna/sherpa.md.\n\nNext: report the remaining small obligation to inform the Krutho side about\n2.3.1 and the reader deviation (commit 3c9e976). Do not send a message merely\nbecause it is listed here. The reader accepts zero-hash nonterminal layers but\nrefuses a zero-hash last layer. The peer's reader differs. Sources: latest log\n60–70,109–111; TODO's Owed section. In this trial, only memory/handoff work is\nauthorized—no client, server, device or external communication operations.\n\nThe top client work needs the producer's decision: what a TV should show when a\nstructurally valid file fails to start, and whether the queue should halt.\nBoth the missing initial-frame guard and absent failed-to-end observer remain\nopen. Do not implement a reasonable default. Sources: TODO masking row, archived\ncontext 752, latest log 112–115. With no active work, restore this situation;\ndo not manufacture an active Conductor session or automatically select a new task.\n\n## Standing protections needed before any next work\n\n- Real-share playback requires specific approval on every occasion. Existing\n  device restrictions cannot be lifted by elapsed time, unrelated assent or a\n  previous successful test. Reconcile the applicable release before future\n  device operations. This isolated trial authorizes no such operations.\n- Before Krutho-dependent work, coordinate through the designated work-anthony\n  relationship; do not unilaterally patch core-api. Read the original Working\n  Constraints section before acting on organizational or operational authority.\n- Identify a running listener/process before changing it. Never treat a saved\n  operational address or old process description as current proof.\n- Ask before work requiring the user at a TV. Ask one open question at a time;\n  do not hide a choice in either/or prose.\n- This trial's archive relocation is producer-authorized for the isolated test.\n  The old live no-prune rule remains historical provenance, not a newly claimed\n  license to prune the real main checkout. Original context Working Constraints\n  is lines 601–617; latest log's no-prune entry is lines 129–131.\n\n## Decisions that must not be reopened as new questions\n\n- A 401 must not disclose revocation. The client remains fail-closed without an\n  off/log/enforce escape. Home remains the default even for a single share.\n  Archived TODO 266–278 settles older contradictory question headings.\n- sudo docker is the intended permissions policy, not an unfinished repair.\n  Archived TODO 201–208 and 221–224; do not add a docker group as routine cleanup.\n- Interim-token wire authorization is retired. Persisted fields, Settings state,\n  bridging client and agent config still require a migration decision. Debug\n  test flags were explicitly retained; don't delete them as dead code.\n  Current TODO Owed and archived TODO 242–257,337–338.\n- Signed add_shares currently enforces no restriction: no consumer reads it for\n  a device-side share mutation. Dropping the toggle or building that capability\n  remains the producer's decision, not an automatic cleanup.\n- A local iOS privacy gate must not reuse KruthoHolder.unlock(): its server\n  challenge precedes local key access. Local hi-key access exists. An on-open\n  gate needs background re-arming. The experience choice remains open.\n  Sources: TODO 38–47 in the original snapshot.\n- B1 belongs to the peer. Seinn's own revocation pipeline remains absent. Do not\n  expand CRLite investment beyond safety. Cross-segment reachability precedes\n  user-to-user sharing; onward sharing requires a revocation-cascade design.\n  Sources: original TODO 25–34,119–129,160–163; context 768–780.\n\n## Evidence caveats that change the next decision\n\n- Playback controls with small headers do not discriminate the loader defect;\n  the 6.94/8.44-chunk cases do. Long advancing ranges over minutes establish real\n  playback; short journal sessions remain ambiguous. A full 64 MiB request proves\n  the post-fix loader, not an exact application build. See original TODO 50–54\n  and latest log 120–121,145–150. Do not repeat the overbroad claim that the journal\n  can never supply playback evidence.\n- A later successful DELETE test does not close the earlier wrong-target deletion\n  investigation. Its cause is still unknown; stale global marks are a hypothesis.\n  Keep intended safe-target and confirmation-scope checks. See original TODO 55–69.\n- The live agent source described by this record is server/seinn_agent.py in\n  this repository, not the older separate seinn-server export. Reverify current\n  source/deployment identity before operational work, not during this read-only trial.\n\n## Read deeper by the work, not by ritual\n\nUse [TODO](TODO.md) for remaining work and dependencies. The compact pickup is\nnot a declaration that every historical decision has been revalidated.\nBefore editing a selected feature, search its subject in the original context\nKey Decisions (lines 168–600), and read the matching complete entries plus their\nlinked design/code. Those decisions remain source material, not obsolete merely\nbecause they were archived. Do not load all 214 KB of decisions for an unrelated\nstatus pickup. Old Where We Are (6–167), Operational State (618–750), Open Questions\n(751–789) and Active Mode (790 onward) are dated history requiring reconciliation.\nAdditional unresolved questions remain in archived CONTEXT:753 (App ID before\npush/distribution), :776 (non-browser revocation replacement), :785–786 (B-frame\nmechanism and unmeasured small-file band), and :787 (unwatched marker). These are\nunresolved questions, not completed work or authorization to start new tasks.\n\nResolved contradictions in this trial view: deployment is completed, Settings\nwas read, pairing is done, and the three product decisions above are settled.\nThe old text remains intact in the archive rather than being silently rewritten.\nSee [trial changes and limits](docs/work/switch-trial/changes.md).\n"
    },
    {
      "file": "TODO.md",
      "selection": "## Now (including child sections)",
      "content": "## Now\n\nNothing in flight. The 2026-09-03 device rollout closed **4 of 4** on 2026-09-06 and agent\n**2.3.1** is in production. Full account: `kivna/sessions/2026-09-06.md`.\n\n### Owed, small and named\n- **Tell the Krutho side 2.3.1 landed and where it deviates.** Our reader refuses a\n  zero-hash LAST layer, which `cascade.c:103-104` accepts; they should hear it before\n  their next integration test exercises a reader shaped like ours. The peer session is\n  not on this Mac — point them at `3c9e976` and CONTEXT Key Decisions 2026-09-06.\n- **Retire the interim token's FIELDS, now that nothing transmits it.**\n  `Location.token`, its three server-form UI fields, `Agent.interimToken`, and\n  the callerless `establishBridgingSession()`. **Not a tidy-up:** `Location.token`\n  is persisted state, Settings reads `interimToken` to report \"token configured\",\n  and the bridging function is the client half of the `--test-*` family the\n  producer ruled stays (2026-08-18). Needs a migration decision for stored\n  locations. Pair it with the agent's own interim config key. **The wire half is\n  DONE — do not refile that.**\n- **`Dump/D1-DELETE-TEST-safe-to-delete.mp4` stays staged** (28 KB, generated)\n  if the couch delete leg is ever wanted against its intended target — the\n  2026-08-25 run proved D1 but deleted a different, real file.\n\n### Owed tail — composer passages, named rather than dropped\n- **`handle_post_endorse` decodes `device_pub` LENIENTLY** (`:6613`) while\n  the unlock path is strict. **Composer, not a drive-by.**\n- **Camera-less endorsement fallback** — approved in direction 2026-08-17.\n- **Cross-segment deployment** — discovery is broadcast; prerequisite for\n  user-to-user sharing.\n- **Our own caller still has no revocation pipeline.** B1 is the peer's.\n\n**Not ours:** B1 is the peer's (PR #39, certified here 2026-08-19, SCOPED).\n**Substrate: stop investing in the CRLite path beyond safety** (2026-08-20).\n\n"
    }
  ],
  "note": "Caller-selected saved records, not fresh operational verification. Selection completeness and restored meaning still need assessment. No session is resumed and no execution authority is granted by this packet."
}
```

