# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.128.0, branch `main`, subject "Release Kerd 0.128.0:
effort-sized native Claude players" (2026-09-15, released by Claude on Anthony's "y",
reviewed by Codex; the save helper verified the remote and CI entry-gate run
34970583757 succeeded).** Since 0.126.0:
- 0.127.0 (2026-09-15 00:42): pairing records a review cadence; Conductor plans
  review from it; Fit lines for every model job; returned work is read against a
  private content baseline with `skills/conductor/scripts/change_read.py`. CI ran on
  the empty trigger commit that follows it (run 34931229115), because GitHub
  registered no push event for the release itself.
- 0.128.0 (08:43): five `kerd:effort-<level>` agents set a native Claude job's effort
  while the call still passes the model; `job_evidence.py` observes what ran; the
  portable package ships the agents.

Records: `docs/work/effort-sized-players/work.md` (0.128.0),
`docs/work/review-and-fit-corrections/work.md` (0.127.0),
`docs/work/conductor-clean-entry/composer-restoration-comparison.md` (Builds 1–2, real
use of 0.126.0). The sitting's account is `kivna/sessions/2026-09-15.md`.

**The current work is proof again.** 0.127.0 and 0.128.0 were built from real-use
evidence (the 2026-09-14 23:08 ruling), but neither has run in real use yet.
- Evidence so far: fixtures and suites; four Codex review rounds for 0.127.0 and two
  for 0.128.0; one end-to-end probe (`kerd:effort-low` + `model: sonnet` observed as
  claude-sonnet-5 at low, Claude Code 2.1.272).
- Nothing yet shows reviews planned without a reminder, Fit lines, `Change read` lines
  or effort agents in a real build.

**Installed state, not to be overclaimed:** Claude's `installed_plugins.json` records
Kerd 0.128.0 (installed 2026-09-15 08:47). Sessions started before then keep their
loaded version; this one loaded 0.126.0. Codex runs 0.124.0 (reported by Codex
2026-09-14, not rechecked). Verify the skill base path before counting a result.
`/usr/bin/git` works again: Anthony accepted the Xcode license at 08:46, after it
failed from 00:27, when a stale `.git/index.lock` also had to be removed.

**Selected continuation (proposed, not agreed):**
1. Anthony starts fresh Claude sessions on 0.128.0 and brings Codex to 0.128.0 (his
   action, or needs his authorization).
2. The next real paired Conductor build is observed and recorded like Builds 1–2.
   Record: review planned from the cadence or offered once; Fit lines; a `Change read`
   line per return; `kerd:effort-<level>` dispatch with a `job_evidence.py`
   observation. Observed by the session doing the build or the `kerd-b5-review` role.

Stops at recorded observations: no manufactured build, no release. Pending question:
may Codex be updated to 0.128.0?

**Urgent or imminent risks:** none recorded in Kerd's active records (`TODO.md` and the
current work records checked at this Out, 2026-09-15). Weefish's unrecorded drive4
capacity readings belong to that project (session log 2026-09-14, Gotchas).

**The launch sequence is retained and untouched**: five outcomes, 0 of 5:
`risk-state-split` at acceptance owing its evidence-backed record,
`gate-reachability` refusing at viability on row 2, the four exposed
fatal/accepted risks, then the `agent-request` pilot. Detail in TODO.md under
"Earlier launch sequence — retained pending reconciliation" and in
`kivna/sessions/2026-09-03.md`.

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at
the root (2026-09-09). Name it with `--preserve` at every save.

**Routing:** after this save, the Claude session holding `kerd-b5-review`
designates its successor against this file with `skills/agent/scripts/agent.py
handoff --record CONTEXT.md`. The next Claude In adopts it with `adopt
--expected-session <bound ID> --record CONTEXT.md`. Receipts and the designation
stop matching when this file's bytes change. The role's pairing has no recorded review
cadence yet (0.127.0 asks for one at the next pairing).

**Pickup reading set** (Switch Out, 2026-09-15):
- this file complete, for position, the selected continuation, risks and rulings;
- `TODO.md` `## Now` with its child section, the designated active list;
- `kivna/sessions/2026-09-15.md` complete, the sitting's account;
- `docs/work/effort-sized-players/work.md` `## Now`, the latest record's stage and
  next action.

Open `docs/work/review-and-fit-corrections/work.md` and
`composer-restoration-comparison.md` when recording the next build, and
`docs/decisions.md` for any ruling's case.
Helper arguments (`read_args`): `["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-15.md", "--section", "TODO.md", "## Now", "--section", "docs/work/effort-sized-players/work.md", "## Now"]`.
Measured reading: 29,449 bytes, about 7,363 tokens estimated at four bytes each (not a tokenizer reading), within the 8,000 target, including this line.

## Key Decisions

Rulings only, kept here while they govern the next work; the full case for each, and every
other standing decision, is in [docs/decisions.md](docs/decisions.md) (182 entries at the
2026-09-15 Out, newest first, indexed by ruling). The three risk-ledger and acceptance
rulings are held because the retained launch sequence resumes under them; they leave when
it does.

- **EFFORT IS SET PER NATIVE CLAUDE JOB THROUGH KERD'S kerd:effort-<level> AGENTS WHILE THE CALL STILL PASSES THE MODEL; WHAT RAN IS OBSERVED WITH job_evidence.py, AND PARTIAL OR MISSING EVIDENCE IS UNVERIFIED; CODEX MODELS ARE NOT CLAUDE AGENT FILES — Anthony, 2026-09-15, released in 0.128.0.**
- **OBSERVATIONS EXIST TO DRIVE CORRECTIONS: RECORD WHAT REAL USE SHOWS, FIX THE GAPS IT EVIDENCES, THEN OBSERVE AGAIN — Anthony, 2026-09-14 23:08.**
- **EVERY MODEL JOB SHOWS A FIT LINE; RETURNED WORK IS READ AGAINST A PRIVATE CONTENT BASELINE, AND ANY UNEXPECTED, OUTSIDE, COMMITTED OR HEAD CHANGE IS A FINDING — Anthony, 2026-09-14/15, released in 0.127.0.**
- **PAIRING ASKS ONCE FOR ROLE AND REVIEW CADENCE AND CARRIES IT ACROSS SESSION CHANGES; CONDUCTOR PLANS INDEPENDENT REVIEW FROM IT OR OFFERS ONCE; A CADENCE GRANTS NOTHING; A CHANGE AFTER A REVIEW REPEATS ITS GATE — Anthony, 2026-09-14, released in 0.127.0.**
- **DELEGATE CLEAR WORK WITHOUT A COMPOSER: CONDUCTOR CHOOSES WHO WRITES EACH STEP — ITSELF FOR CLEAR WORK, THE COMPOSER WHEN THE SPECIFICATION NEEDS DESIGN, INLINE ONLY FOR TINY, COUPLED OR JUDGMENT-BOUND WORK; DELEGATION IS THE DEFAULT WHEN A JOB CAN BE BRIEFED, CHECKED AND IS WORTH ITS HANDOFF COST; A DEFECT RETURNS TO THE STEP'S AUTHOR — Anthony, 2026-09-14, released in 0.126.0.**
- **RESTORE THE COMPOSER AS A BOUNDED TWO-PASS CALL, THE SCORE AS THE EXECUTION CONTRACT, TAGS AFTER WRITING AND PER-STEP PLAYERS FROM v0.105.0; RE-DISPATCH, NEVER RE-SPECIFY; CONDUCTOR READS EVERY RETURNED DIFF — Anthony, 2026-09-14, released in 0.125.0.**
- **ORDINARY SWITCH IN ALWAYS ENDS ON "START A CONDUCTOR SESSION?"; A PLAIN YES OPENS DIRECTION-SETTING, NEVER APPROVAL OF THE SAVED TASK; IN RESTORES THE DESIGNATED ACTIVE LIST; A HUMAN-BLOCKED CONTINUATION IS NOT A PROJECT-WIDE HOLD — Anthony, 2026-09-14 (reported by Codex), released in 0.125.0.**
- **SUBSTANTIAL BUILD, DESIGN OR WORKFLOW REQUESTS OFFER CONDUCTOR, NEW OR EXISTING; SMALL FIXES STAY DIRECT; A CHOSEN CONDUCTOR ASSESSES EVERY TASK FOR MODEL/EFFORT FIT AND WHO DOES IT, STARTING FROM THE TASK, NOT THE INHERITED PAIR; SWITCH COMPOSES ITS OWN ARRIVAL WITHOUT LOADING CONDUCTOR — Anthony, 2026-09-14 (reported by Codex), released in 0.124.0–0.125.0.**
- **MANAGED CONDUCTOR SESSIONS CARRY AN AUTHORIZED LOCAL BUILD ACROSS FRESH DECISION CONTEXTS, WITH THE CHAT AS THE CONTROL SURFACE; NO TUI TAKEOVER; UNCERTAIN WORK IS INSPECTED, NEVER BLINDLY RELAUNCHED — Anthony, 2026-09-13/14 (reported by Codex), released in 0.123.0.**
- **OUT SAVES THE SELECTED CONTINUATION — OWNER, ACTION, AGREED OR PROPOSED STATUS, STOPPING POINT AND PENDING QUESTION — AND KEEPS EVERY RECORDED URGENT OR IMMINENT RISK INSIDE THE PICKUP READING SET — Anthony, 2026-09-13/14, released in 0.122.0–0.122.1.**
- **SWITCH IN RETURNS THE RENDERED DASHBOARD UNCHANGED; CORRECTIONS GO INTO THE INPUT AND ARE RENDERED AGAIN; NOW HOLDS ONLY IMMEDIATE OWNER-LABELLED ACTIONS AND NECESSARY FOLLOW-THROUGH — Anthony, 2026-09-13, released in 0.121.0–0.121.2.**
- **NO YOU BOX; TEAM IS ONE PROVIDER (ROLE) LINE; TEAM COMES ONLY FROM AGENT PAIRING, NEVER PROJECT HISTORY — Anthony, 2026-09-13 (reported by Codex), released in 0.120.0–0.124.0.**
- **AN ESTABLISHED ROLE SURVIVES A LOST SESSION: THE NEXT RESTART RECOVERS IT FROM THE UNCHANGED SAVED ACCOUNT WITHOUT SELECTING THE TEAMMATE AGAIN; NO ONE-RECOVERY CAP — 2026-09-13, Anthony's request (reported by Codex), released in 0.117.0.**
- **PROVE KERD WORKS AS IT SHOULD BEFORE ANY CONSUMER PICKUP; EXISTING ORDINARY-USE EVIDENCE IS THE BASELINE, NOT REPEATED — Anthony, 2026-09-13 10:41, deferring the Codex pickup.**
- **COMPARE ACTUAL SESSION IDs BEFORE AND AFTER A CLEAR OR RESTART; NEVER INFER IDENTITY FROM A TERMINAL, A TITLE OR RECENCY — Anthony, 2026-09-13, agreeing the succession design.**
- **ONE STABLE ALIAS PER ROLE; A SUCCESSOR REPLACES THE ID ATOMICALLY AGAINST THE EXPECTED OLD ID, ON A DESIGNATED HANDOFF OR THE PERSON'S EXPLICIT SELECTION, NEVER ON RECENCY — 2026-09-13, Codex's design chosen over Claude's two-alias chain, Anthony's "lets do it".**
- **ONE OUT OWNER, NAMED BY THE PERSON; MEMORY READINESS IS THE OWNER'S JUDGMENT, SEPARATE FROM THE GIT VERDICT — Tony, 2026-09-13.** The owner alone writes the pointer, active list, session account and the record it is reconciling; contributors return their account; Out names other-branch work, never merges it.
- **A FACTUAL CLARIFICATION IS NOT AUTHORIZATION; THE ARRIVAL QUESTION IS ASKED ONCE; A LOG PRESERVES A CLAIM, NOT PROOF — Anthony, 2026-09-12.**
- **ONE PROPOSAL, NEVER TWO OPTIONS, NEVER AN “OR” — an approval prompt or question carries exactly one proposal. Tony, 2026-09-11.**
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
