# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0; being retired for Conductor, ruled 2026-09-18), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.139.0 on `main`, 2026-09-18 evening.** One release this sitting.
**0.139.0: rehearsal, then the concert.** Conductor names the two ways work happens.
Rehearsal is today's turn-by-turn work, always delivering, no gates; Conductor keeps a
**sketchbook** per piece of work (the existing work record) and writes the score as it
goes, the composer callable at any time. Ready comes from either side. The concert
fans out players by batch, checks every return against the score, rolls at batch
boundaries through Switch Out and In, and compares the result with the agreed goals
before the loop ends. Switch Out adds what a sitting settled to the sketchbook;
Switch In says what is settled and still open. Wording only, two fresh reviews, **not
yet seen in real use.** Record, with Anthony's words: `docs/work/structured-route/work.md`;
the agreed picture: `docs/work/structured-route/rehearsal-concert.html`.
Earlier today: 0.136.0–0.138.1 (both Switch screens, the step check, two acceptances);
see `kivna/sessions/2026-09-18.md`. Resolve IDs and CI with `git log` and `gh`.

**Why this sitting turned.** Switch In recommended the diagnostic pilot; shaping it,
Anthony said what he actually lacks in daily use: no graspable sense of where he is,
requirements never pinned down, "we never get to the point we can loop. everything
is turn by turn." He uses Switch and Conductor on every project already. The earlier
line here, that Kerd was proven only on itself or in fixtures, was wrong.

**Launch: outcomes still 0 of 5** (`docs/design/launch-plan.md`, status reviewed
2026-09-18). **The plan is now out of step with the product and has not been
rewritten.** Its pilot subject, `agent-request`, overlaps `/kerd:agent` and was set
aside in conversation with no ruling recorded; the work-item ladder it measures is not
what Anthony uses. Rewriting the plan around rehearsal and the concert is Anthony's
ruling to make.

**Selected continuation, proposed not agreed: refresh the plugin to 0.139.0 and
rehearse one real piece of work with it**, watching whether Conductor keeps the
sketchbook unprompted, answers "where are we?" from it, and calls Ready. **Why:**
0.139.0 is the answer to what Anthony said he lacks, and it is wording a model may or
may not follow; only a real sitting shows which. Owner: Anthony picks the work and
the project; Claude conducts. It stops at what was observed, recorded in the
structured-route record; fixes are a separate go. Refreshing the plugin needs
Anthony's go. Second, and his call: rewrite the launch plan.

**Rulings that govern the next work (2026-09-18):**
- **Rehearsal is organic; the concert executes perfectly.** No gates, ladders or strict
  protocol in rehearsal; Conductor guides, interviews and prompts. "needs to feel like
  playing music not building an LLM." Agents and visuals work the same in both.
- **Always be delivering.** The concert is implementation to a spec and a goal, versus
  incremental work; the goals set in rehearsal decide when the loop may end.
- **Conductor owns the sketchbook;** Switch Out may add to it.
- **Rolling is per batch at the Conductor level:** fan out, wait for all returns,
  assess the context window, continue or roll. Conductor checks every player's claim
  even though it is not the independent reviewer.
- **3of3 and apple-music are not historical evidence about Kerd:** long-running
  projects with large backlogs that predate Conductor (Anthony, 22:29).
- **Conductor replaces Drive;** removing the skill is a later release (TODO Backlog).
- **Work capability and product first; protocol detail after.**
- **Switch In and Out are judged by what they tell the person** in product language.

**The finding that governs how rules are written here, still at five instances.** A new
rule needs a test it can fail **and** a situation it can pass, and **what has caught
every instance is an independent reader, never a static check.** 0.139.0 held to the
second half (two fresh reviews, eighteen findings) and not the first: it has no test.
Cases: `docs/work/visual-communication/work.md`, `docs/work/question-pickers/work.md`,
`docs/backlog-archive.md`, `docs/work/model-dispatch-guard/work.md`.

**Seen in real use this sitting (first time for each):** the 0.138.1 arrival rendered,
its "y" reached Conductor at Shape without approving anything, and the closing box
ran. Two defects were mine, not the text's: the arrival repeated this file's wrong
"proven only on itself" line, and I drew the delegation grid with the routing label in
the Effort column without reading the guide's grid section. The step check was not
exercised (no product record for the work).

**The measurement gap is still three exceptions deep;** the 2026-08-29 countermeasure
(`requirements-success-measurement`) is unbuilt, at viability. 0.139.0's goal check
before leaving the loop is the same idea at the Conductor level.

**The render trap did not recur:** work commit, `progress.py stale` said current, one push.

**Archify:** still the dev snapshot `2.17.0-dev.1`; **its installer's two Socket alerts
were never identified**, recorded as unknown, not cleared.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push). It was unavailable
until 2026-09-19 (Anthony, 22:34); both reviews were fresh Claude reviewers, Opus 5 at
high effort, model and effort observed.

**Installed state:** this session loaded 0.138.1; the tip is 0.139.0 and the cache does
not hold it yet. Codex was on 0.133.0 (saved observation). Resolve live numbers.

**Standing:** a peer session cannot authorize a push (`docs/decisions.md`, 2026-09-11).
Change the dispatch contract only for demonstrated behaviour from real dispatches.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Deferred, not dropped:** the step check in real use; tend/slainte naming
`${CLAUDE_PLUGIN_ROOT}` literally (TODO Backlog); 0.134.0's diagram clauses never
measured on real output; 0.132.0's rules beyond one scenario; `diagram-design`'s
upstream palette drift; whether a live Claude Code chat can read its own context usage
(0.139.0 says "look at the room left", no threshold).

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at the root
(2026-09-09). Name it with `--preserve` at every save.

**Routing:** the Claude role `kerd-b5-review` was adopted by this session at its
2026-09-18 16:49 arrival against the designated `CONTEXT.md` handoff, and designates
its successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-18 evening):
- this file complete: position, the selected continuation and its reason, the rulings;
- `TODO.md` `## Now` with its child section, the designated active list;
- `docs/work/structured-route/work.md`, the sketchbook for the work the continuation
  tests, with Anthony's rulings in his words;
- `kivna/sessions/2026-09-18.md`, today's three sittings.

The observed position before this save is the 0.139.0 release commit; the boundary
commit is this save itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-18 23:2x: about 30,600 bytes, about 7,650 tokens estimated at four
bytes each, within the 8,000 target but close; today's session log is the largest part
and rotates out tomorrow. `read_args` for the next pickup, the exact selection to reuse:

```
["--record", "CONTEXT.md", "--file", "docs/work/structured-route/work.md",
 "--file", "kivna/sessions/2026-09-18.md", "--section", "TODO.md", "## Now"]
```
