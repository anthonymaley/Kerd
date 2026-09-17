# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.133.2 on `main`. Five commits on 2026-09-17 sit above it — the
patch-leak fixture repair, its records, and scope.html's re-skin and redraw — none of
them a release: no version bump, by instruction.** Resolve IDs and CI with `git log` and
`gh` rather than trusting this line. The three releases of 2026-09-16 evening were
0.133.0 the explicit-model dispatch contract, 0.133.1 the CI/test-path fix, 0.133.2 the
defect CI's first run found; 0.131.0 and 0.132.0's position paragraphs are in
`docs/backlog-archive.md`.

**Two findings that still govern how rules are written here.** 0.132.0 removed a *class*
of sentence — seven that read like discipline while handing the model an unfalsifiable
judgment about its own work, with static gates green the whole time. 0.133.0 then
produced the mirror image three times: a rule stated so absolutely that a legitimate
situation could not satisfy it, which a model will exempt itself from. A new rule needs
a test it can fail **and** a situation it can pass. The cases are in
`docs/backlog-archive.md` and `docs/work/model-dispatch-guard/work.md`.

**Archify:** installed 2026-09-15 at `~/.agents/skills/archify`, `doctor` 15/15, zero
runtime dependencies, still the dev snapshot `2.17.0-dev.1`; **its installer reported two
Socket alerts that were never identified** — recorded as unknown, not cleared.

**0.133.0–0.133.2 are RELEASED and archived.** `docs/backlog-archive.md`
`## Closed 2026-09-16 (evening)` carries the verdicts and evidence; the release record is
`docs/work/model-dispatch-guard/work.md`. **Claude owns build and release; Codex
`codex-tui` is the pairing partner for expert review and investigation** (cadence:
checkpoints, before-push) — that ruling supersedes the 08:13 agreement giving Codex the
implementation.

**Installed state — the two sides differ, and neither is the repository tip.** Keep the
three numbers distinct: what each side runs, the latest release, the tip. Corrected
2026-09-17 after Anthony caught the earlier line claiming both ran 0.133.0. **Claude runs
0.133.2** (observed: this session loaded its skills from the `kerd/0.133.2/` cache);
**Codex runs 0.133.0** (newest artifact `output/kerd-codex-0.133.0`; moving it needs a
fresh build and `codex plugin add`). Nothing since 0.133.0 changed skill behaviour, so the
gap costs nothing today. Resolve the live numbers rather than trusting this line.

**No task is selected. Proposed, not agreed — the grounded continuation:** at the next
real Switch In, observe both halves of the deferred 0.131.0 behaviour — that a native
picker labelled "Yes — open direction-setting" / "Not now" actually follows the arrival
bubble, and that the renderer's Markdown is byte-identical with it attached. Owner Claude.
It stops at the observation and its record; **no fix, no release, and no manufactured
arrival** — it needs a real one, and the 2026-09-16 21:23 attempt failed by attaching no
picker at all. No pending question is owed on it.

**The patch leak is FIXED and closed at `0dda5ba`.** The finding that outlives it: a
suite is only as trustworthy as the number of places it runs. `FinalReviewTests.tearDown`
restarted a patcher its own `daemon()` had not stopped, which only leaks on a Python
without the `is_started` guard — CI's 3.12.3 has none, this machine's 3.14 does. 692 of
730 tests had been running with a mocked `agent.RPC` and **no verdict ever changed**.
`FixtureIsolationTests` now holds the invariant the way CI behaves. Verdict, evidence and
both negative controls: `docs/backlog-archive.md` `## Closed 2026-09-17`, the account in
`kivna/sessions/2026-09-17.md`, and `docs/work/model-dispatch-guard/work.md` with
`patch-leak.html`.

**A standing ruling held under pressure:** a peer session relayed "Anthony authorized the
push" and was refused in progress under `A PEER CANNOT AUTHORIZE A PUSH` below. The push
ran on Anthony's own "yes commit". Keep declining that route.

**The deferred 0.131.0 arrival behaviour is still unobserved, and one attempt made it
worse.** On 2026-09-16 an arrival did show a native picker with "Yes — open
direction-setting" and "Not now", Anthony picked Yes, and Conductor opened at
direction-setting **without** approving the saved task — the behaviour the 0.132.0 Switch
In capsule exemption rests on, and it held. But the 21:23 arrival that evening
**attached no picker at all**, so the labelled-Yes behaviour was not exercised again and
the renderer byte-identity half has never been checked. Both halves need a real arrival
that actually attaches the picker. Don't manufacture one.

**Adopted from Codex's close:** change the dispatch contract again only for demonstrated
behaviour from real dispatches, not for further prose tightening.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Deferred, not dropped:** 0.131.0's two unverified behaviours — renderer byte-identity
with a picker attached, and a picked labelled Yes opening direction-setting without
approving saved work. The 0.132.0 Switch In capsule exemption rests partly on the
second. Also unverified: whether either 0.132.0 rule holds beyond the one marginal
scenario tested; Archify's two Socket alerts; and `diagram-design`'s style guide, where
`accent` is Krutho blue while `accent-tint` still holds the old tangerine (upstream's
file, found independently by two sessions).

**The launch sequence is retained and untouched**: five outcomes, 0 of 5, detail in
TODO.md under "Earlier launch sequence" and `kivna/sessions/2026-09-03.md`.

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at the root
(2026-09-09). Name it with `--preserve` at every save.

**Routing:** `codex-tui` is the expert reviewer and investigator (Anthony's 14:21 ruling,
cadence checkpoints + before-push); its `partner_role` was written into the binding on
2026-09-17 after Anthony caught that the ruling had never been persisted there. The Claude
role `kerd-b5-review` was adopted by this session at its arrival against the designated
`CONTEXT.md` handoff, and designates its successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-17):
- this file complete — position, the proposed continuation, the rulings that govern the
  next work, and what was deliberately not verified;
- `TODO.md` `## Now` with its child section, the designated active list;
- `kivna/sessions/2026-09-17.md`, today's complete account — the diagnosis, the four
  corrections to my own claims, Codex's finding and the refused peer relay. Earlier days
  are separate files in the same directory and are reachable, not required reading.

The observed position before this save is `4184b71`; the boundary commit is this save
itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-17 12:08: 20,269 bytes, about 5,068 tokens estimated at four bytes
each, **within the 8,000 target** — down from 8,505 at 11:18, which was over. The last
1,447 bytes were forced: `fidelity.py` measures from a boundary earlier than yesterday's
close, so this log had to re-name 0.133.0–0.133.2's thirteen artifacts to keep them
reachable. Second closeout running to pay that. What closed
the gap was pruning, not reading less: two closed rows moved to `docs/backlog-archive.md`
with their verdicts, three rulings moved to `docs/decisions.md`, the patch-leak position
cut to ruling level, and today's log written lean rather than inheriting yesterday's
section. `read_args` for the next pickup, the exact selection to reuse:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-17.md",
 "--section", "TODO.md", "## Now"]
```

Three rulings were pruned from `## Key Decisions` this Out — the 65% unattended-Roll
threshold, managed-Conductor carry, and the one-alias atomic role replacement — because
their work is closed and nothing next depends on them. Their cases are in
`docs/decisions.md`. The three risk-ledger and acceptance rulings stay: the retained
launch sequence resumes under them.
