# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0; being retired for Conductor, ruled 2026-09-18), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.138.0 on `main`, 2026-09-18.** The afternoon shipped five
releases. **0.136.0:** Switch In opens with a PROJECT · PHASE · NEXT · TEAM grid,
speaks product English and ends on "Start a Conductor session?" with a Yes — <work> /
Something else picker. **0.136.1:** risk-state-split accepted. **0.137.0–0.137.1:**
Conductor checks where a work item stands in the user's own project, and
gate-reachability was accepted. **0.138.0:** the Switch Out box mirrors Switch In.
None of the three screens or the step check has been seen in real use yet. Records:
`TODO.md` `## Now`. Resolve IDs and CI with `git log` and `gh`.

**Launch: outcomes still 0 of 5** (`docs/design/launch-plan.md`, status reviewed
2026-09-18). Done: launch sequence steps 1 (risk-state-split) and 2
(gate-reachability), prerequisites on the critical path, not outcomes. Outcome 1 is
partial: the wiring exists and a fixture proves it, but no real session has driven
it. This session said "launch 2 of 5 done" several times; that was wrong.

**Selected continuation, proposed not agreed: start the diagnostic pilot** (launch
outcome 2). First refresh the Kerd plugin to 0.138.0 (this machine's cache holds
0.136.1), then create the separate `agent-request` repository (never inside Kerd) and
drive its first work item through Conductor, with Kerd frozen for the run. **Why:**
it is the first time Kerd works for someone else's project; everything built so far
has been proven only on Kerd itself or in fixtures. Owner: Claude drives it, and
Anthony decides the subject's direction. The output is a findings document, and
PARTIAL is valid. It stops at the findings: no Kerd edits during the run, and breaks
are recorded, not repaired (the plan's binding rules). Creating a new repository and
installing or refreshing the plugin each need Anthony's go.

**Rulings that govern the next work (2026-09-18):**
- **Conductor replaces Drive.** Drive is dropped, not renamed. Removing the skill is a
  later release (TODO Backlog). Drive's two gate calls stay broken outside Kerd
  until then.
- **Work capability and product first; protocol detail after** (Anthony, 13:07; saved
  as a working preference). Lead with what the user can do.
- **Conductor's step check names the gap and offers it, never refuses;** a go-ahead
  anyway is recorded in the work record.
- **Switch In and Out are judged by what they tell the person** in product language:
  what happens next and why. Self-verification of Kerd's own mechanics is not a next
  action unless it blocks product work or Anthony asks for it.

**The finding that governs how rules are written here, now at five instances.** A new
rule needs a test it can fail **and** a situation it can pass. **What has caught every
instance is an independent reader, never a static check.** Today's releases held to
that: every one had a fresh reviewer, and each review changed the work. Cases:
`docs/work/visual-communication/work.md`, `docs/work/question-pickers/work.md`,
`docs/backlog-archive.md`, `docs/work/model-dispatch-guard/work.md`.

**The measurement gap is now three exceptions deep.** gate-visuals, risk-state-split
and gate-reachability were all accepted with no declared product measure. The
2026-08-29 countermeasure (declare a measure or its inapplicability before acceptance,
`requirements-success-measurement`) is still unbuilt, at viability.

**The render trap recurred** on `8a72c0f` although the playbook recorded it; the
playbook now says so. The order is work commit → render commit → one push.

**Archify:** installed 2026-09-15, still the dev snapshot `2.17.0-dev.1`; **its
installer's two Socket alerts were never identified**, recorded as unknown, not
cleared.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push). It was not asked this
sitting; every review was a fresh Claude reviewer.

**Installed state, three numbers kept distinct:** Claude loaded 0.135.0 at this
sitting's arrival, and the cache now holds up to 0.136.1. Codex was on 0.133.0 (saved
observation). The tip is 0.138.0. Resolve live numbers rather than trusting this line.

**A standing ruling held under pressure:** a peer session relayed "Anthony authorized the
push" and was refused in progress under `A PEER CANNOT AUTHORIZE A PUSH` (`docs/decisions.md`, 2026-09-11). Keep declining that route.

**The patch leak is FIXED and closed at `0dda5ba`.** A suite is only as trustworthy as
the number of places it runs; detail in `docs/backlog-archive.md` `## Closed 2026-09-17`.

**Adopted from Codex's close:** change the dispatch contract again only for demonstrated
behaviour from real dispatches, not for further prose tightening.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Deferred, not dropped:** the three new screens and the step check in real use;
tend/slainte naming `${CLAUDE_PLUGIN_ROOT}` literally, which Claude Code rewrites
(TODO Backlog); 0.134.0's diagram clauses never measured on real output; 0.132.0's
rules beyond one scenario; `diagram-design`'s upstream palette drift.

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at the root
(2026-09-09). Name it with `--preserve` at every save.

**Routing:** the Claude role `kerd-b5-review` was adopted by this session at its
2026-09-18 10:40 arrival against the designated `CONTEXT.md` handoff, and designates
its successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-18 afternoon):
- this file complete: position, the selected continuation and its reason, the rulings
  that govern the next work, and what was deliberately not verified;
- `TODO.md` `## Now` with its child section, the designated active list, including the
  launch sequence the continuation starts;
- `kivna/sessions/2026-09-18.md`, today's two sittings. Earlier days are reachable, not
  required reading.

The observed position before this save is `e83eb5d`; the boundary commit is this save
itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-18 15:5x: about 20,000 bytes, about 5,000 tokens estimated at four bytes each, within the 8,000 target. `read_args` for the next pickup,
the exact selection to reuse:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-18.md",
 "--section", "TODO.md", "## Now"]
```

Closed this Out and moved to `docs/backlog-archive.md` `## Closed 2026-09-18
(afternoon)` with verdicts: the first-arrival observation, launch sequence steps 1
and 2. The superseded position paragraphs moved with them.
