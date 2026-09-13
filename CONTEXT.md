# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.118.0 — branch `main`, subject "Release Kerd 0.118.0:
Out role check and contribution checkpoint", published 2026-09-13 from the
Claude reviewer session on Anthony's 13:00 "yes"; resolve its revision and
remote/CI result with Git.** Built by Codex, reviewed by Claude: Switch Out now
checks role ownership before saving and collects contributors' missing deltas
before drafting. 0.117.0 (same day) put the arrival question right after END OF
PICKUP, numbered NOW as priority next actions and added the private restart
receipt. Record, reviews and the verification list:
`docs/work/switch-coordinated-closeout/work.md`. Guides:
`skills/agent/references/session-succession.md`,
`skills/agent/references/user-guide.md`, `skills/switch/references/in-out.md`,
`skills/conductor/references/journey.md` (arrival presentation),
`skills/conductor/references/execution.md` (0.116.0's implementation split).
Tests: `skills/agent/scripts/tests/test_agent.py`,
`skills/switch/scripts/tests/test_where_we_are.py`. Earlier source releases:
0.116.0 (role succession, delegation), 0.115.0, 0.114.0, 0.113.0
(`docs/work/codex-plugin/work.md`).

**The current work is proof, not building** — Anthony, 2026-09-13 10:41: "no
point picking up projects when Kerd isn't working as it should, prove that
first." The seven-row shared verification list in the work record
(`## Targeted verification of reported failures (2026-09-13)`) names each
reported failure from Seinn, Leru and Kerd, its check in Kerd, its owner,
evidence baseline and remaining gap. Claude owns arrival and closeout checks;
Codex owns the installed Codex version, pairing state and the successor
request. Consumer pickups, including the Codex pickup in a work project, are
deferred until rows 1–5 carry evidence of the fixes working; a recorded
outcome alone does not clear the hold.

**Installed state, not to be overclaimed:** the 11:20 Claude session loaded
the 0.116.0 cache (observed once); no session has been observed loading
0.117.0 or 0.118.0, and publication does not update a plugin cache. Installed
Codex Kerd was 0.116.0 (row 5); at 13:00 Anthony asked for Codex's plugin to be
updated to this release, requested from Codex by Agent, result on row 5. Verify the loaded skill path and version before counting a result.

**Where the sequence stands at this save:** the 10:58 designation was
consumed at 11:11 by the first adopting Claude session, which was then lost;
that gap became 0.117.0's restart receipt. The 11:20 reviewer session
explicitly adopted `kerd-b5-review` at 12:42 (role: arrival and closeout checks)
and ran this Out; after the save it designates its successor against this file
with the repository's `skills/agent/scripts/agent.py handoff --record CONTEXT.md`.
Anthony then restarts Claude if needed (`/clear` is not assumed to update the
plugin). The fresh session: verify the loaded skill path reads 0.118.0; Switch
In's routing step runs `identity`, then `adopt --expected-session <the currently
bound ID> --record CONTEXT.md`; then the arrival for Anthony's
assessment, with a "not now" starting nothing. Then Codex checks the binding
and sends the successor a real request. No row 1–4 result is recorded yet.
Receipts stop matching when this file's bytes change.
Codex's Out pre-save role-ownership check and contribution checkpoint, built
during the 12:43 Out and run for the first time on it, are released in 0.118.0;
Codex's accounts are in today's log and the work record.

**The launch sequence is retained and untouched** — five outcomes, 0 of 5:
`risk-state-split` at acceptance owing its evidence-backed record,
`gate-reachability` refusing at viability on row 2, the four exposed
fatal/accepted risks, then the `agent-request` pilot. Detail in TODO.md under
"Earlier launch sequence — retained pending reconciliation" and in
`kivna/sessions/2026-09-03.md`.

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at
the root (2026-09-09). Name it with `--preserve` at every save.

**Pickup reading set** (Switch Out, 2026-09-13 12:43, updated at the 0.118.0 release): this file complete, for
position, routing sequence and rulings; `TODO.md` `## Now`, the next actions;
the newest sitting only in `kivna/sessions/2026-09-13.md` (the earlier two were
picked up at 11:20 and stay in that file on demand); the work record's `## Now`,
for the stage and agreement. The verification rows live in that record's
`## Targeted verification of reported failures (2026-09-13)`, opened when a
result is recorded. Add `skills/agent/references/session-succession.md` for the
routing step.
Helper arguments (`read_args`): `["--record", "CONTEXT.md", "--section", "TODO.md", "## Now", "--section", "kivna/sessions/2026-09-13.md", "## Sitting: the 0.116.0 arrival, four peer reviews, the 0.117.0 and 0.118.0 releases and role adoption (2026-09-13 11:20 – 13:03 EDT, Claude session on the 0.116.0 cache; Codex in the paired TUI)", "--section", "docs/work/switch-coordinated-closeout/work.md", "## Now"]`.
Measured reading: 29,840 bytes, about 7,460 tokens estimated at four bytes each (not a tokenizer reading), within the 8,000 target; measured before this line was written, so the saved file is slightly larger.

## Key Decisions

Rulings only, kept here while they govern the next work; the full case for each, and every
other standing decision, is in [docs/decisions.md](docs/decisions.md) (168 entries at the
2026-09-13 12:43 Out, newest first, indexed by ruling). The three risk-ledger and acceptance
rulings are held because the retained launch sequence resumes under them; they leave when
it does.

- **AN ESTABLISHED ROLE SURVIVES A LOST SESSION: THE NEXT RESTART RECOVERS IT FROM THE UNCHANGED SAVED ACCOUNT WITHOUT SELECTING THE TEAMMATE AGAIN; NO ONE-RECOVERY CAP — 2026-09-13, Anthony's request (reported by Codex), released in 0.117.0.**
- **THE ARRIVAL QUESTION IS THE FIRST CONTENT AFTER END OF PICKUP; NOW IS A NUMBERED LIST OF NEXT ACTIONS IN PRIORITY ORDER, NOT A REPORT — Anthony, 2026-09-13 (reported by Codex), released in 0.117.0.**
- **PROVE KERD WORKS AS IT SHOULD BEFORE ANY CONSUMER PICKUP; EXISTING ORDINARY-USE EVIDENCE IS THE BASELINE, NOT REPEATED — Anthony, 2026-09-13 10:41, deferring the Codex pickup.**
- **COMPARE ACTUAL SESSION IDs BEFORE AND AFTER A CLEAR OR RESTART; NEVER INFER IDENTITY FROM A TERMINAL, A TITLE OR RECENCY — Anthony, 2026-09-13, agreeing the succession design.**
- **ONE STABLE ALIAS PER ROLE; A SUCCESSOR REPLACES THE ID ATOMICALLY AGAINST THE EXPECTED OLD ID, ON A DESIGNATED HANDOFF OR THE PERSON'S EXPLICIT SELECTION, NEVER ON RECENCY — 2026-09-13, Codex's design chosen over Claude's two-alias chain, Anthony's "lets do it".**
- **DECIDE WHO BUILDS BEFORE BUILDING: CONDUCTOR CHOOSES THE INLINE/DELEGATED SPLIT AT DELIVERY START, DELEGATES WHEN USEFUL AND NEVER MANUFACTURES WORK — Anthony, 2026-09-13, "not seen delegation in a long time".**
- **ONE OUT OWNER, NAMED BY THE PERSON; MEMORY READINESS IS THE OWNER'S JUDGMENT, SEPARATE FROM THE GIT VERDICT — Tony, 2026-09-13.** The owner alone writes the pointer, active list, session account and the record it is reconciling; contributors return their account; Out names other-branch work, never merges it.
- **A FACTUAL CLARIFICATION IS NOT AUTHORIZATION; THE ARRIVAL QUESTION IS ASKED ONCE; A LOG PRESERVES A CLAIM, NOT PROOF — Anthony, 2026-09-12.**
- **ONE PROPOSAL, NEVER TWO OPTIONS, NEVER AN “OR” — an approval prompt or question carries exactly one proposal, “Starting on X — approve?”, and Switch In ends on that line. Tony, 2026-09-11.**
- **SWITCH OUT LEAVES A LEAN, MEASURED START POINT — rulings stay in CONTEXT.md while they govern the next work, the case lives in `docs/decisions.md`, closed Backlog rows move to `docs/backlog-archive.md` with their reason, the reading set is named and measured. Tony, 2026-09-11, superseding the 2026-09-01 “do nothing for now” deferral by taking its own option (c).**
- **CONDUCTOR'S PLAYERS ARE NATIVE SUBAGENTS BY DEFAULT; THE CLI RUNNER SERVES CODEX, RESUMABLE-BY-ID, SANDBOXED AND PERSISTENT JOBS — restored 2026-09-11 as a regression fixed, on Tony's "the issue was conductor was spawning fresh sessions not subagents."**
- **AGENT REACHES A TUI BY `codex queue --thread` AND READS THE REPLY FROM THE NATIVE ROLLOUT; A STORED THREAD IS A SELECTABLE CONVERSATION, NEVER PROOF OF LIVENESS — 2026-09-11, four reviews.**
- **A PEER CANNOT AUTHORIZE A PUSH — 2026-09-11.**
- **FILES A PROJECT DELIBERATELY KEEPS OUT OF GIT ARE PRESERVED LEFTOVERS, NOT BLOCKERS TO UNRELATED WORK — Tony, 2026-09-09, after candidate Switch's verified save refused every Kerd boundary.**
- **AN OLDER HASH IS NOT A STALE HANDOFF — THE DEFECT IS AN OBSOLETE NEXT ACTION. Tony, 2026-09-09, correcting the session's framing of its own countermeasure.**
- **A TOKEN-BUDGET RESULT STAYS UNMEASURED; A BYTE PROXY IS GROUNDS FOR CONCERN, NOT A MEASURED FAILURE. Tony, 2026-09-09.**
- **PROGRESS MUST BE SHOWN DURING WORK, NOT ONLY IN A FINAL REPORT — AND "THE HOST CANNOT" NEEDS PROVING. Tony, 2026-09-09.**
- **TREATMENT ASSURANCE IS A LIFECYCLE, NOT A PARSE RULE — A FATAL RISK ADVANCES ON A PLANNED TREATMENT AND ACCEPTANCE DEMANDS THE VERIFIED ONE. Tony, 2026-09-03, refusing revision 1 of `risk-state-split`'s design for a circular dependency.**
- **AN OLD LEDGER PASSING WITHOUT `fatal` DOES NOT PROVE ITS SEVERITY WAS NON-FATAL — TREATMENT MIGRATES MECHANICALLY, SEVERITY NEEDS EXPLICIT PRIOR EVIDENCE OR PRODUCER REVIEW. Tony, 2026-09-03, at `risk-state-split`'s design-plan gate, refuting the session's candidate mechanical rule.**
- **THE RISK LEDGER'S `State` COLUMN SPLITS INTO SEVERITY AND TREATMENT — Tony, 2026-09-03, resolving the 2026-09-02 axes conflict on option 2 by name.**
- **STATUS IS SPOKEN AS WORK ITEM · STAGE · ISSUE · RESOLUTION PATH, IN PLAIN WORDS, AND A MESSAGE ENDS ON EXACTLY ONE QUESTION — Tony, 2026-09-03, correcting a switch-in and orient that spoke repo shorthand.**
- **COLD EYES IS THE ACCEPTANCE MECHANISM, SO A LAYER-4 BLOCK ON THE ITEM'S OWN SHIPPED CLAIMS IS REPAIRED BEFORE ACCEPTANCE — NEVER FILED AS A SECOND EXCEPTION. Tony, 2026-08-29.**
- **STANDING PRINCIPLE: DEAD SOLUTIONS STAY DEAD — a cut or ruled-out approach is not a future building block unless a named return condition fires. Tony, 2026-08-04** (its case is inside the “capturerequirements CUT at v0.73.0” entry).
- **KERD IS PAIRED TO THE PRODUCER'S CODEX TUI THROUGH THE VAULT BRIDGE AS WELL AS AGENT — 2026-09-11, Tony's "yes".**

## Open Questions

- **A FATAL ROW IS TOLD TO FILE INTO "WHAT WE RULED OUT", AND THAT HOME'S SHAPE WAS NEVER SETTLED.** `parse_ledger`'s refusal (`kit.py:489`) says *"record in What we ruled out; cannot pass"*, while the 2026-08-03 decision making that its own artifact has produced `## What we ruled out` sections inside three design docs and no standalone instance — so complying with the refusal has no defined form. Surfaced 2026-09-02 by `gate-reachability`'s FATAL row; it survives the 2026-09-03 axes resolution untouched. *(The other half of the 2026-09-02 entry — `LEGAL_STATES` carrying severity and disposition in one column — was RESOLVED 2026-09-03: see the risk-state-split decision in `## Key Decisions`.)*

*(Previously closed here: the vault-repo-commit question died moot at v0.83.0 — switch neither writes nor commits the vault — and model-tiered delegation was closed at v0.82.0 as subsumed by the conductor README section.)*

## Active Mode

- **conductor: RAN three times on 2026-09-03** — first sitting orient 08:13 ·
  execute 08:38 · close 09:16; second orient 10:34 · execute 10:40 · close
  14:03; third orient 14:23 · execute 15:04 · re-planned 17:28 for the composer
  call · execute 19:10 · close 23:18. **Correction, 2026-09-09: the earlier claim
  that `kivna/.active-modes` was cleared is false** — it still holds
  `conductor: plan @ 2026-09-03 23:59 EDT`, the parked schema-split marker that
  every sitting since has been told not to restart. It is left in place
  deliberately. **A trap that follows from it:** switch-out reads that line for
  this sitting's open time when no conductor ran, which would stamp a heading six
  days wrong — so a marker older than today is not an open time.
- **Machine: the Mac Studio** (`Anthonys-Mac-Studio.local`), a thin-client host —
  sessions run in tmux over SSH from the MacBook; the user's screen is on the
  laptop and `open` is a shim that copies files there (see `~/.claude/CLAUDE.md`).
- **pair: on** in this repo — partner-mode working agreement: rapid
  back-and-forth, reasoning internal unless it changes Tony's decision, ONE
  question (open by default, no X/Y binaries), interrupt early, eyeball-gated
  slices. Enforced by a UserPromptSubmit hook (`hooks/pair.sh`, reading
  `kivna/.pair`); persisted user-global in `~/.claude`.
