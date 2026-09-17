# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.134.0 on `main`, the Visuals contract correction** — a diagram's
main relationship must survive having every code reference stripped, and every view
saved beside work names its project, product or repository inside the render. Below it
sit 2026-09-17's morning commits: the patch-leak fixture repair, its records, and
scope.html's re-skin and redraw, none of them a release by instruction. Resolve IDs and
CI with `git log` and `gh` rather than trusting this line. Earlier position paragraphs
for 0.131.0–0.133.2 are in `docs/backlog-archive.md`.

**The finding that governs how rules are written here, now at five instances.** A new
rule needs a test it can fail **and** a situation it can pass. 0.132.0 removed seven
sentences that read like discipline while handing the model an unfalsifiable judgment;
0.133.0 produced the mirror image three times, a rule so absolute no legitimate
situation satisfies it; 2026-09-17 added a renderer check with no failing situation, and
then **two more inside 0.134.0 itself** — including one written hours after its author
had recorded the class. The governing sentence has never needed changing; it catches all
five unchanged. **What has caught every instance is an independent reader, never a
static check**: 731 tests and a clean gate were green on both broken 0.134.0 drafts.
Cases: `docs/work/visual-communication/work.md`, `docs/work/question-pickers/work.md`,
`docs/backlog-archive.md`, `docs/work/model-dispatch-guard/work.md`.

**Archify:** installed 2026-09-15 at `~/.agents/skills/archify`, `doctor` 15/15, zero
runtime dependencies, still the dev snapshot `2.17.0-dev.1`; **its installer reported two
Socket alerts that were never identified** — recorded as unknown, not cleared.

**0.133.0–0.134.0 are RELEASED and archived.** `docs/backlog-archive.md` carries the
verdicts and evidence — `## Closed 2026-09-16 (evening)` for 0.133.x,
`## Closed 2026-09-17 (afternoon)` for 0.134.0. Release records:
`docs/work/model-dispatch-guard/work.md` and `docs/work/visual-communication/work.md`. **Claude owns build and release; Codex
`codex-tui` is the pairing partner for expert review and investigation** (cadence:
checkpoints, before-push) — that ruling supersedes the 08:13 agreement giving Codex the
implementation.

**Installed state — the two sides differ, and neither is the repository tip.** Keep the
three numbers distinct: what each side runs, the latest release, the tip. Corrected
2026-09-17 after Anthony caught the earlier line claiming both ran 0.133.0. **Claude runs
0.133.2** (observed 2026-09-17: this session loaded its skills from the `kerd/0.133.2/`
cache, so 0.134.0 is the repository tip and is installed nowhere);
**Codex runs 0.133.0** (newest artifact `output/kerd-codex-0.133.0`; moving it needs a
fresh build and `codex plugin add`). Nothing since 0.133.0 changed skill behaviour, so the
gap costs nothing today. Resolve the live numbers rather than trusting this line.

**No task is selected. Proposed, not agreed — the grounded continuation:** take the
assistant-side byte-identity reading from **outside** the producing session, the only
thing that can promote 2026-09-17's tested-not-verified claim to verified. Owner Claude.
It stops at the reading and its record: no fix, no release, no push. No pending question
is owed on it.

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

**Both 0.131.0 deferrals are resolved, 2026-09-17.** The authority half is **closed**:
at the 12:23 arrival the picker carried "Yes — open direction-setting", Anthony picked
it, and Conductor opened at Shape while the saved task stayed unapproved and unstarted —
second observation, and the behaviour the 0.132.0 Switch In capsule exemption rests on.
The byte-identity half was **reworded because it could not fail**: it named the renderer,
and `where_we_are.py` has no picker argument, environment variable or awareness across
931 lines, so a picker cannot reach it. It now names the *assistant* returning that
stdout unchanged. That claim is **tested, not verified** — the assistant cannot hash its
own emitted message, so identity is its attestation and needs an outside reading.
Detail: `docs/work/question-pickers/work.md`.

**Adopted from Codex's close:** change the dispatch contract again only for demonstrated
behaviour from real dispatches, not for further prose tightening.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Deferred, not dropped:** the assistant-side byte-identity claim, tested but needing an
outside reading. **0.134.0's two clauses have never been measured on real diagram
output** — both are producer checks at review, and no diagram has yet exercised them.
Also unverified: whether either 0.132.0 rule holds beyond the one marginal scenario
tested; Archify's two Socket alerts; and `diagram-design`'s style guide, where `accent`
is Krutho blue while `accent-tint` still holds the old tangerine (upstream's file, found
independently by two sessions).

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
- `kivna/sessions/2026-09-17.md`, both of today's accounts — the morning's patch-leak
  diagnosis and the afternoon's 0.134.0 release with its five review findings. Earlier
  days are separate files in the same directory and are reachable, not required reading.

The observed position before this save is `43241ae`; the boundary commit is this save
itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-17 15:0x: 26,291 bytes, about 6,573 tokens estimated at four bytes
each, **within the 8,000 target** — up from 5,068 at the morning close, the cost of a
second release and its two review rounds. The second account of the day was appended to
the same log rather than written as a new file, the resolved 0.131.0 deferrals were cut
from position to ruling level, and a duplicated record entry in `TODO.md` was merged.
`read_args` for the next pickup, the exact selection to reuse:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-17.md",
 "--section", "TODO.md", "## Now"]
```

Closed this Out and moved to `docs/backlog-archive.md`
`## Closed 2026-09-17 (afternoon)` with verdicts: 0.134.0's release row, and both
0.131.0 deferrals — one closed by observation, one reworded and reopened in its
corrected form. The three risk-ledger and acceptance rulings stay: the retained launch
sequence resumes under them.
