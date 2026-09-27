---
profile:
  provider: anthropic
  family: fable-5-1
  version: 2026-09-27
  applicable_models: [claude-fable-5-1, claude-mythos-5-1]
  official_sources:
    - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
      retrieved: 2026-09-27
    - url: https://platform.claude.com/docs/en/build-with-claude/effort
      retrieved: 2026-09-27
  last_evaluated: null
  supersedes: fable-5-1@2026-09
---

# Claude Fable 5.1 profile

The provider says Fable 5 prompts carry over to 5.1 unchanged; the clauses
below record only the behaviour differences that change how Kerd briefs a
delegated Fable 5.1 or Mythos 5.1 job.

```yaml
- id: all-efforts-eligible
  applies_when: every new task class
  guidance: Start at high, then include medium and low in the task eval; use xhigh or max only where the task needs the headroom. Effort labels are not assumed equivalent to earlier families.
  basis: provider-guidance
  source: official_sources[1]
  evaluation: pending
  review_trigger: matched effort sweep or source change
- id: low-effort-against-smaller-models
  applies_when: choosing a model for routine or cost-sensitive work where a smaller model at higher effort is the default candidate
  guidance: Put fable-5-1 at low (and medium) into the comparison rather than ruling it out on cost; the provider reports medium roughly matches Fable 5 at lower cost and low often beats Opus and Sonnet on cost per task. Adopt it for a job type only from Kerd's own comparison.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 low versus opus or sonnet comparison on a Kerd job, or source change
- id: finish-long-task
  applies_when: asynchronous or explicitly autonomous multi-step work
  guidance: State that already-authorized next steps should be completed without asking again; do not apply this clause to live pair work.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: premature-stop comparison or source change
- id: scope-is-the-deliverable
  applies_when: an autonomous job has several parts, or may hit an open question or a blocked part partway
  guidance: Tell the job the brief sets the scope and it must not quietly narrow, widen or swap it. On a question, it does every part that does not depend on the answer and states the assumption it made; on a blocked part, it finishes all the others and names exactly what it left out and why.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 job that returns a narrowed or partial result, or source change
- id: assessment-not-fix
  applies_when: the brief asks a question, a review or an investigation rather than a change
  guidance: Say that the deliverable is the assessment, so the job reports findings and stops, making no fix unless the brief asks for one. Autonomy wording written for build jobs can otherwise push a reviewer or reader into applying changes.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first reviewer or reader job that edits files unasked, or source change
- id: evidence-before-state-change
  applies_when: an autonomous job may run commands that change system state (restarts, deletes, config edits)
  guidance: Ask the job to check that its evidence supports that specific action before running it, since a symptom that looks like a known failure can have another cause. This adds a check; it never widens what the brief authorizes.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first state-changing action taken on a mismatched diagnosis, or source change
- id: no-unrequested-extras
  applies_when: a player implements an open-ended feature or change
  guidance: Fable 5.1 tends to fix nearby code, extend unmentioned behaviour and commit more tests than the change needs. The brief should say to report pre-existing bugs and unmentioned issues as follow-ups instead of fixing them, implement the reading of an ambiguity best supported by the wording and code and state it, keep scratch checks out of the repo, and add tests only where asked or where the repo already keeps them for this kind of change, sized like the neighbours; every requested behaviour is still implemented in full.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 player diff with unrequested changes or extra test files, or source change
- id: final-report-stands-alone
  applies_when: any delegated job whose final message is what the caller reads
  guidance: Fable 5.1 writes fewer updates during long tool chains than Fable 5, and its final message may cover only the last step. The brief should say that only the final message reaches the caller and must stand alone, covering what was found, what was done and what is open across the whole job; drop any inherited line telling the job to withhold findings. For live pair work, ask for a one-line intent at the start and brief updates while working.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 report that omits earlier steps, or source change
- id: batch-implied-tool-calls
  applies_when: a coding or computer-use job where the next independent reads or checks follow from the task rather than being named in the brief
  guidance: Fable 5.1 may then issue one tool call per turn, which costs time but not quality. Add one line asking the job to list what it needs next and request every independent item together.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 coding transcript showing serial independent calls, or source change
- id: plain-dense-prose
  applies_when: the job produces prose a person will read (docs, reports, release notes, drafts)
  guidance: Fable 5.1 prose can run dense, with long sentences and few paragraph breaks. Put a short instruction in the brief itself (the user message, which the provider prefers over the system prompt) against mannered prose, asking it to say things literally rather than through metaphor or flourish.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 prose deliverable judged too dense, or source change
- id: formatting-when-needed
  applies_when: the brief or an inherited template carries anti-formatting rules, or the result needs lists, tables or headings
  guidance: Fable 5.1 uses less bold, fewer headers and lists, and fewer quotation marks than earlier models. Remove blanket anti-formatting lines and state where structure is wanted instead, such as the report's required sections or a list when content has several parts.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 result under-structured for its reader, or source change
- id: mark-quoted-source-text
  applies_when: a reader or research job summarises documents, pages or transcripts
  guidance: Fable 5.1 reproduces source passages without marking them as quotes more often than Fable 5. Include one complete worked example in the brief (request, correct response, one sentence on why it is correct) whose response restates sources in its own words and marks the one short phrase it quotes.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1 summary carrying unmarked source wording, or source change
- id: low-effort-search-trigger
  applies_when: effort is low and the task depends on current or unfamiliar facts
  guidance: Explicitly require retrieval of named fast-moving facts rather than relying on model memory.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: low-effort research comparison or source change
- id: safeguard-false-positive-triggers
  applies_when: a coding or review job may hit Fable 5.1's safety classifiers
  guidance: Ask whether code has bugs rather than whether it compiles, give context or docs for a lesser-known language, and keep base64 data out of what tools return to the job. A refusal on a benign job is a trigger to rephrase along these lines, not a finding about the code.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first refusal on a benign Kerd job, or source change
- id: targeted-edits
  applies_when: a small part of an existing file changes
  guidance: Prefer a surgical edit when it preserves the result; do not rewrite the whole file merely for convenience.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: edit-size comparison or source change
- id: long-deliverable-effort
  applies_when: one job produces a single long deliverable (a long document rewrite, a large table, a complete code file)
  guidance: Run it at high; at xhigh or max Fable 5.1 may draft the whole deliverable in its reasoning and then write it again. If xhigh or max is chosen, tell the job that reasoning and reply share one output limit and that drafting in full twice adds length without improving the result, naming the limit only where Kerd knows it (API routes; Kerd's native route sets none).
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first xhigh or max fable-5-1 long-deliverable job, or source change
- id: lead-keeps-working
  applies_when: a fable-5-1 session leads and dispatches subagents
  guidance: Start subagents in the background and let the lead carry on with independent work, reading each result when it arrives, rather than blocking on each one; the provider reports lower time to completion at similar quality and cost. The lead still waits for every result before recording the work done.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first fable-5-1-led fan-out timing, or source change
- id: vision-crop-zoom
  applies_when: the job must judge dense charts, diagrams, screenshots or rendered pages
  guidance: Give the job the raw image file and a way to crop and enlarge regions (for example an image library in its shell) so it can inspect and verify details, rather than a single downscaled view.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: first dense-visual fable-5-1 job, or source change
- id: append-only-history
  applies_when: the harness replays thinking blocks or relies on prompt caching
  guidance: Keep conversation history append-only and record compaction as a new state rather than editing earlier turns.
  basis: provider-guidance
  source: official_sources[0]
  evaluation: pending
  review_trigger: harness state handling changes or source change
```

Kerd-owned example delta:

```xml
<execution_mode>Autonomous batch. Complete the authorized task and its stated
checks. Ask only if a missing producer-owned decision would materially change
the result.</execution_mode>
<edit_scope>Make targeted changes to the named sections. Report unrelated
defects separately instead of fixing them. Add tests only where the brief asks
or the repository already keeps them for this kind of change.</edit_scope>
<report>Only your final message reaches the caller. Make it stand alone: what
you found, what you changed, and what is still open, across the whole job.</report>
```
