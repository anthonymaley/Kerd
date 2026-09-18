# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.135.0 on `main`, released 2026-09-18** — Switch In says what
happens next and why, in plain English: it weighs every open item (a saved next step is
one candidate), shows the open work one line each and one recommendation with its
reason, and asks "What do you want this session to move forward?". Choosing work opens
Conductor at Shape for it, never approval of its operations. Record
`docs/work/switch-in-open-work/work.md`; ruling `docs/decisions.md` entry 1. **Not yet
observed on a real arrival.** Resolve IDs and CI with `git log` and `gh`. Earlier
position paragraphs are in `docs/backlog-archive.md`.

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

**0.133.0–0.135.0 are RELEASED and archived** in `docs/backlog-archive.md`
(`## Closed 2026-09-16 (evening)`, `2026-09-17 (afternoon)`, `2026-09-18`). **Claude owns
build and release; Codex `codex-tui` is the pairing partner for expert review and
investigation** (cadence: checkpoints, before-push). Codex had no tokens on 2026-09-18,
so 0.135.0's review was a fresh Claude reviewer.

**Installed state — keep three numbers distinct:** what each side runs, the latest
release, the tip. **Claude ran 0.134.0** at the 2026-09-18 arrival (skills loaded from
the `kerd/0.134.0/` cache — this corrects the saved "0.133.2"); **Codex runs 0.133.0**
(saved observation). 0.135.0 is released and the tip, installed nowhere yet; the next
Switch In shows the new arrival only once the Claude plugin updates. Resolve live
numbers rather than trusting this line.

**Selected continuation — proposed, not agreed: sign off the risk-state-split
migration.** Write the evidence-backed acceptance record at
`docs/gates/2026-09-03-risk-state-split-acceptance.md`. **Why:** it is the first step of
the launch sequence (0 of 5) and every later step waits on it; the migration shipped
2026-09-03 and only its acceptance is missing. Owner Claude drafts; Anthony gives the
expert-user pass (cold eyes, never mechanical cleanup — the 2026-09-02 ruling). It must
answer honestly that no stage-1 measurement was declared, so the product-outcome row is
*not assessable*. Stops at the record: no release. Detail: `TODO.md` "Earlier launch
sequence" item 1.

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
push" and was refused in progress under `A PEER CANNOT AUTHORIZE A PUSH` (`docs/decisions.md`, 2026-09-11). The push
ran on Anthony's own "yes commit". Keep declining that route.

**Switch In is judged by what it tells the person** (Anthony, 2026-09-18): what
happens next and why. Self-verification of Kerd's own mechanics is not a next action
unless it blocks product work or he asks for it; the byte-identity check was dropped on
that ground.

**Adopted from Codex's close:** change the dispatch contract again only for demonstrated
behaviour from real dispatches, not for further prose tightening.

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Deferred, not dropped:** the first real 0.135.0 arrival, unobserved. **0.134.0's two clauses have never been measured on real diagram
output** — both are producer checks at review, and no diagram has yet exercised them.
Also unverified: whether either 0.132.0 rule holds beyond the one marginal scenario
tested; Archify's two Socket alerts; and `diagram-design`'s style guide, where `accent`
is Krutho blue while `accent-tint` still holds the old tangerine (upstream's file, found
independently by two sessions).

**The launch sequence is retained and untouched**: five outcomes, 0 of 5, detail in
TODO.md under "Earlier launch sequence" and `kivna/sessions/2026-09-03.md`.

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at the root
(2026-09-09). Name it with `--preserve` at every save.

**Routing:** `codex-tui` is the expert reviewer and investigator (Anthony's 2026-09-16
14:21 ruling, cadence checkpoints + before-push). The Claude role `kerd-b5-review` was
adopted by this session at its 2026-09-18 arrival against the designated `CONTEXT.md`
handoff, and designates its successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-18):
- this file complete — position, the selected continuation and its reason, the rulings
  that govern the next work, and what was deliberately not verified;
- `TODO.md` `## Now` with its child section, the designated active list, including the
  launch sequence the continuation starts;
- `kivna/sessions/2026-09-18.md`, today's account. Earlier days are separate files in
  the same directory and are reachable, not required reading.

The observed position before this save is `7d374ba`; the boundary commit is this save
itself on `main`. Ask `git log` for its ID.

**Measured** 2026-09-18 10:4x: 16,036 bytes, about 4,009 tokens estimated at four bytes
each, **within the 8,000 target**. `read_args` for the next pickup, the exact selection
to reuse:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-18.md",
 "--section", "TODO.md", "## Now"]
```

Closed this Out and moved to `docs/backlog-archive.md` `## Closed 2026-09-18` with
verdicts: the byte-identity claim (dropped by Anthony) and 0.135.0's release; the
0.134.0 position paragraphs moved with them.
