# Real-use comparison checklist

Use while assessing ordinary project sessions, not as extra steps the working
agent must perform. The user requested a file-by-file audit as well as outcome,
memory, model collaboration and experience comparisons. Kerd holds the assessment;
each consuming project retains its own work, authority and memory.

## Evidence for a session

- [ ] Identify project, session/time window, task, host, loaded Kerd version and
  actual skill path. Separate requested model/effort from observed identity.
- [ ] Use available tool transcripts, job results and before/after Git state.
  Include delegated workers when their logs are available. A pasted final report
  alone is reported evidence, not a complete activity trace.
- [ ] State missing evidence. Git records writes, not reads; a tool invocation
  shows access/returned content, not proof the model understood it. Never claim
  every file was audited when logs, workers or uncommitted changes are missing.

## Every file read or written

Account for each observable access, including repeats, skill/reference reads,
searches, shell reads, generated artifacts and writes that were later reverted.
Use one compact inventory per assessed session; repeated operations can share a
row if their counts, ranges and order remain traceable to the original events.

| File / project-relative path | Actor and event reference | Read/search/write; range and repeats | Why needed / finding |
| --- | --- | --- | --- |
| Fill from observed tool events, not an invented example | | | |

- [ ] Distinguish filename discovery, search snippets, partial reads and complete
  reads. Mark truncated output and unknown coverage. Do not reread every file
  just to audit that it was read; inspect content where correctness requires it.
- [ ] Assess relevant versus avoidable input: broad archive loads, duplicate
  reads, generated files, oversized tool output and useful material missed.
- [ ] Check each written file's diff against the agreed scope. Preserve unrelated
  edits; inspect overwrites, deletions, renames, stale pointers and lost decisions.
- [ ] Compare observed writes with Git changes, including untracked files, staged
  content and relevant commits. A final diff cannot reveal all transient writes.
- [ ] Keep secrets, private native session IDs and raw customer content out of
  Kerd's comparison notes. Reference local evidence instead of copying transcripts.

## Switch and memory

- [ ] In restores the correct project, active task, agreement, constraints,
  pending question and exact next action, without reopening completed work.
- [ ] Measure pickup elapsed time and actual added input where available; separate
  host overhead, cached input and output. Byte conversions remain estimates.
- [ ] Out saves decisions, results, unresolved work, authority and evidence;
  CONTEXT/TODO/current pointers agree and do not retain an obsolete next action.
- [ ] Kivna/session history is retained and reachable; cleanup removes completed
  work from active lists without erasing operative decisions or rewriting history.
- [ ] Distinguish local save, commit and verified remote save. Check the next In
  against the preceding Out; preserved local-only files do not pretend to travel.

## Conductor, prompts and collaboration

- [ ] Work meets agreed success measures, backed by actual checks/review. Proposed
  measures, agreed measures and observed results are not interchangeable.
- [ ] Questions resolve consequential gaps; context supplies known answers.
  Authorized work continues without routine “next” prompts or scope expansion.
- [ ] Model and effort selection suit the job and available tools; reduced cost
  does not silently lower the agreed quality. Record the selection's basis.
- [ ] Inspect the actual execution prompt and selected model-profile version.
  Relevant guidance is applied; outcome, sources, proof, authority and stopping
  conditions survive dispatch. A claimed guidance read is not enough.
- [ ] Check Codex and Claude as controllers, workers and reviewers when those
  roles naturally occur. Do not force every session to exercise every role.
- [ ] Check cross-model requests, results and useful contribution to the final
  work. Distinguish new jobs, reused sessions, native subagents and CLI-managed
  background workers; success through one route does not prove the others.
- [ ] Assess review independence, findings addressed, failure accounting and
  handling of unknown outcomes. No duplicate dispatch or abandoned active job
  hidden by a successful final summary.

## Experience, visuals and comparison

- [ ] Appropriate skills were actually loaded and used; wrong installed versions
  or missing guidance are visible. More skill calls is not inherently better.
- [ ] Visuals clarify the product, decisions or status, use real sources, and have
  readable outputs/links. No diagram quota or added installation just for scoring.
- [ ] Progress identifies the work, actor and whether the user is needed. Emitted
  updates and the user's observation of them remain separate evidence.
- [ ] Compare similar tasks and disclose differences in scope, repo size, model,
  effort, tooling and preparation. Use existing baseline evidence when adequate;
  don't rerun whole builds merely to manufacture a comparison.
- [ ] Report correctness, evidence completeness, elapsed time, token usage,
  avoidable turns, rework and missed boundaries together. Cheap but incomplete
  restoration is not an improvement; extra necessary context may be justified.
- [ ] Close with what worked, the highest-impact observed problem and the smallest
  supported correction. Label each conclusion supported, failed or unassessed;
  no aggregate score that hides a lost restriction or poor result.

Start from the sessions/projects the user supplies or explicitly makes available.
No background watcher, automatic access to other terminals, new hooks, CI,
mandatory user questionnaire or project mutation is authorized by this checklist.
Keep detailed inventories out of normal Switch pickup; load them for assessment.
