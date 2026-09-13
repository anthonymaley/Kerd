# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.116.0 — branch `main`, subject "Release Kerd 0.116.0:
role continuity and implementation delegation", `b70f07f`, published by Codex
2026-09-13 and remote-verified from the Claude session by fetch; Codex reports
CI run 34762986143 succeeded.** It adds private role succession across
session-ID changes, Conductor's implementation-split decision and the arrival
clarifications. Record, reviews and the verification list:
`docs/work/switch-coordinated-closeout/work.md`. Operational guide:
`skills/agent/references/session-succession.md`. Earlier source releases:
0.115.0, 0.114.0, 0.113.0 (`docs/work/codex-plugin/work.md`).

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

**Installed state, not to be overclaimed:** the Claude plugin cache holds
0.116.0 on disk (its `plugin.json` read 0.116.0 at 10:52); no session has
been observed loading it. This session's ordinary startup at 09:38 loaded the
0.115.0 cache (observed once). Installed Codex Kerd is 0.113.0, confirmed by
Codex at about 11:00 by `codex plugin list` and the cached manifest; nothing
updated. Presence in a cache does not establish what the next start loads:
verify the loaded path and version first.

**Where the sequence stands at this save:** Out from the Claude session on the
0.115.0 cache under the released 0.116.0 guide (a disclosed test route), both
contributions in `kivna/sessions/2026-09-13.md`. After the save, the session
bound as `kerd-b5-review` (role: arrival and closeout checks, defined
explicitly this sitting) designates its continuation with the released helper
`skills/agent/scripts/agent.py handoff --record CONTEXT.md`; then Anthony
clears. The fresh session's In: verify the loaded version, run `identity` and
`adopt --expected-session <old ID> --record CONTEXT.md` during the routing
step, then the dashboard with one question, whether Anthony can give his
assessment of the arrival now. A "not now" must start nothing. Then tell
Codex by a new peer request so it checks the binding and sends the successor
a real request. Results go on the rows. A safe refusal on unknown identity is
a safety observation, not continuation.

**The launch sequence is retained and untouched** — five outcomes, 0 of 5:
`risk-state-split` at acceptance owing its evidence-backed record,
`gate-reachability` refusing at viability on row 2, the four exposed
fatal/accepted risks, then the `agent-request` pilot. Detail in TODO.md under
"Earlier launch sequence — retained pending reconciliation" and in
`kivna/sessions/2026-09-03.md`.

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at
the root (2026-09-09). Name it with `--preserve` at every save.

**Pickup reading set** (Switch Out, 2026-09-13 10:58): this file complete;
`TODO.md` `## Now`; `kivna/sessions/2026-09-13.md` complete;
`docs/work/switch-coordinated-closeout/work.md` section
`## Targeted verification of reported failures (2026-09-13)`. Add
`skills/agent/references/session-succession.md` when running the routing step.
Helper arguments: `--record CONTEXT.md --file kivna/sessions/2026-09-13.md
--section TODO.md "## Now" --section docs/work/switch-coordinated-closeout/work.md
"## Targeted verification of reported failures (2026-09-13)"`.
Measured reading: 33,765 bytes, about 8,442 tokens estimated at four bytes each (not a tokenizer reading), measured before this line was written; over the 8,000 target by about 440 and kept so on purpose: the log carries both of today's sittings and Codex's account, and the verification section is the next action itself. Prune the earlier sitting from the set once the fresh In has picked it up.

## Key Decisions

Rulings only, kept here while they govern the next work; the full case for each, and every
other standing decision, is in [docs/decisions.md](docs/decisions.md) (166 entries at the
2026-09-13 10:58 Out, newest first, indexed by ruling). The three risk-ledger and acceptance
rulings are held because the retained launch sequence resumes under them; they leave when
it does.

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
