# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.130.0, branch `main`, subject "Release Kerd 0.130.0: unattended
Claude Roll saves its place at 65%" (2026-09-15, released by Claude on Anthony's "yes",
reviewed by Codex; resolve its revision and CI with Git and `gh`).** Since 0.126.0:
- 0.127.0: review cadence at pairing, Fit lines, `change_read.py` baselines.
  0.128.0: `kerd:effort-<level>` agents and `job_evidence.py`. 0.129.0: the
  speech-bubble question form, guarded by `test_question_form.py` (its no-picker half
  is corrected above and awaits the next release).
- 0.130.0 (18:40): `roll.py --target claude --context-aware` watches an unattended
  Claude worker and asks for its saved place at 65% of its window;
  `skills/switch/scripts/claude_roll.py` is the adapter. Codex's route and managed
  Conductor are unchanged.

Records: `docs/work/` carries one folder per release (`context-awareness` 0.130.0,
`effort-sized-players` 0.128.0, `review-and-fit-corrections` 0.127.0,
`conductor-clean-entry` Builds 1–2). The sitting's account is
`kivna/sessions/2026-09-15.md`.

**0.130.0 was the first real paired Conductor build of this run**, evidencing 0.127.0
and 0.128.0 in use: cadence-planned review, Fit lines, `Change read` per return, and
`kerd:effort-xhigh`/`-high` observed by `job_evidence.py` as claude-opus-5 at those
efforts. Record: `docs/work/context-awareness/`. Still unobserved: a pressure-triggered
handover into a second fresh Claude worker, and receipt recovery after a controller
loss; three disclosed test-threshold trials cost $1.24.

**Installed state, not to be overclaimed:** this session loaded Kerd 0.129.0; Claude's
installed plugin was 0.128.0 at 08:47 and 0.129.0 in this session's path. Codex was
updated to 0.129.0 at 13:16 (built to `output/kerd-codex-0.129.0`, `kerd-core`
repointed, confirmed by Codex itself after restarting its thread). Neither side runs
0.130.0 yet. Verify the skill base path before counting a result.
`/usr/bin/git` works again: Anthony accepted the Xcode license at 08:46, after it
failed from 00:27, when a stale `.git/index.lock` also had to be removed.

**Selected continuation (proposed, not agreed):**
1. Build the next release from `TODO.md` `## Now`: the corrected question form (a
   native picker may follow the bubble, including for approvals) across
   `journey.md`, the 12 skill entry points and `test_question_form.py:44`, plus
   Agent's role selector; consider bundling the visual-communication work
   (`docs/work/visual-communication/work.md`) into the same release.
2. Update both sides to 0.130.0 when wanted: Claude sessions on restart; Codex needs a
   fresh `output/kerd-codex-0.130.0` build and `codex plugin add`, which is Anthony's
   call.
3. Observe a pressure-triggered Claude Roll handover into a second fresh worker when a
   real unattended build needs one; don't manufacture it.

Stops at recorded work: no release without Anthony's approval, and no install or
launch without it either. No pending question.

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

**Routing:** `codex-tui` carries the review cadence checkpoints + before-push
(recorded 2026-09-15 15:43); its partner role is still undefined. After this save, the
Claude session holding `kerd-b5-review`
designates its successor against this file with `skills/agent/scripts/agent.py
handoff --record CONTEXT.md`. The next Claude In adopts it with `adopt
--expected-session <bound ID> --record CONTEXT.md`. Receipts and the designation
stop matching when this file's bytes change.

**Pickup reading set** (Switch Out, 2026-09-15 evening):
- this file complete, for position, the selected continuation, risks and rulings;
- `TODO.md` `## Now` with its child section, the designated active list, which carries
  the next release's work;
- `kivna/sessions/2026-09-15.md` section "## Afternoon sitting: Codex on 0.129.0, then
  0.130.0 context-aware Claude Roll", which includes the evening and this closeout;
- `docs/work/context-awareness/work.md` `## Now`, the 0.130.0 record's stage and limits.

Open `docs/work/visual-communication/work.md` when starting the next release,
`docs/work/context-awareness/score.md` for the build's steps, reviews and trials, and
`docs/decisions.md` for any ruling's case.
Helper arguments (`read_args`): `["--record", "CONTEXT.md", "--section", "TODO.md", "## Now", "--section", "kivna/sessions/2026-09-15.md", "## Afternoon sitting: Codex on 0.129.0, then 0.130.0 context-aware Claude Roll (2026-09-15 12:20 – 18:40 EDT, same Claude session, now holding `kerd-b5-review` as f9d4da17; Codex in the paired TUI)", "--section", "docs/work/context-awareness/work.md", "## Now"]`.
Measured reading: 31,986 bytes, about 7,997 tokens estimated at four bytes each (not a tokenizer reading), within the 8,000 target, including this line. Five rulings moved out of this file at this Out; their cases stay in `docs/decisions.md`.

## Key Decisions

Rulings only, kept here while they govern the next work; the full case for each, and every
other standing decision, is in [docs/decisions.md](docs/decisions.md) (185 entries at the
2026-09-15 Out, one added at the 0.129.0 release and two for 0.130.0, newest first, indexed by ruling). The three risk-ledger and acceptance
rulings are held because the retained launch sequence resumes under them; they leave when
it does.

- **CONTEXT PRESSURE IS HANDLED BY ROLLING TO A FRESH SESSION FROM KERD'S SAVED PLACE, NEVER BY COMPACTION; AN INTERACTIVE SESSION SWITCHES OUT WHEN THE PERSON DECIDES; AUTOMATIC PRESSURE HANDLING IS ONLY FOR UNATTENDED ROLL — Anthony, 2026-09-15 13:39/13:42, applied in 0.130.0.**
- **AN UNATTENDED CLAUDE ROLL RUN IS ASKED FOR ITS SAVED PLACE AT 65% OF ITS REPORTED CONTEXT WINDOW (USED TOKENS), NO ABSOLUTE CAP; READINGS ARE RECORDED TO TUNE IT — Anthony, 2026-09-15 13:57, released in 0.130.0.**
- **EVERY KERD QUESTION IS ONE SPEECH-BUBBLE LINE AT THE END OF THE MESSAGE, `> 💬 **The question?**`, WITH OPTIONS OR CONTEXT ABOVE IT; A NATIVE PICKER MAY FOLLOW THE BUBBLE FOR ITS OPTIONS WHENEVER ONE SUITS, INCLUDING APPROVALS, BUT NEVER REPLACES OR PRECEDES IT — Anthony, 2026-09-15, released in 0.129.0 and corrected 19:50/19:51. The 0.129.0 "no boxed cards or native pickers" wording was Claude's over-reach, not Anthony's instruction; the skills, `journey.md` and `test_question_form.py` still carry it and are corrected in the next release.**
- **EFFORT IS SET PER NATIVE CLAUDE JOB THROUGH KERD'S kerd:effort-<level> AGENTS WHILE THE CALL STILL PASSES THE MODEL; WHAT RAN IS OBSERVED WITH job_evidence.py, AND PARTIAL OR MISSING EVIDENCE IS UNVERIFIED; CODEX MODELS ARE NOT CLAUDE AGENT FILES — Anthony, 2026-09-15, released in 0.128.0.**
- **OBSERVATIONS EXIST TO DRIVE CORRECTIONS: RECORD WHAT REAL USE SHOWS, FIX THE GAPS IT EVIDENCES, THEN OBSERVE AGAIN — Anthony, 2026-09-14 23:08.**
- **EVERY MODEL JOB SHOWS A FIT LINE; RETURNED WORK IS READ AGAINST A PRIVATE CONTENT BASELINE, AND ANY UNEXPECTED, OUTSIDE, COMMITTED OR HEAD CHANGE IS A FINDING — Anthony, 2026-09-14/15, released in 0.127.0.**
- **PAIRING ASKS ONCE FOR ROLE AND REVIEW CADENCE AND CARRIES IT ACROSS SESSION CHANGES; CONDUCTOR PLANS INDEPENDENT REVIEW FROM IT OR OFFERS ONCE; A CADENCE GRANTS NOTHING; A CHANGE AFTER A REVIEW REPEATS ITS GATE — Anthony, 2026-09-14, released in 0.127.0.**
- **DELEGATE CLEAR WORK WITHOUT A COMPOSER: CONDUCTOR CHOOSES WHO WRITES EACH STEP — ITSELF FOR CLEAR WORK, THE COMPOSER WHEN THE SPECIFICATION NEEDS DESIGN, INLINE ONLY FOR TINY, COUPLED OR JUDGMENT-BOUND WORK; DELEGATION IS THE DEFAULT WHEN A JOB CAN BE BRIEFED, CHECKED AND IS WORTH ITS HANDOFF COST; A DEFECT RETURNS TO THE STEP'S AUTHOR — Anthony, 2026-09-14, released in 0.126.0.**
- **ORDINARY SWITCH IN ALWAYS ENDS ON "START A CONDUCTOR SESSION?"; A PLAIN YES OPENS DIRECTION-SETTING, NEVER APPROVAL OF THE SAVED TASK; IN RESTORES THE DESIGNATED ACTIVE LIST; A HUMAN-BLOCKED CONTINUATION IS NOT A PROJECT-WIDE HOLD — Anthony, 2026-09-14 (reported by Codex), released in 0.125.0.**
- **SUBSTANTIAL BUILD, DESIGN OR WORKFLOW REQUESTS OFFER CONDUCTOR, NEW OR EXISTING; SMALL FIXES STAY DIRECT; A CHOSEN CONDUCTOR ASSESSES EVERY TASK FOR MODEL/EFFORT FIT AND WHO DOES IT, STARTING FROM THE TASK, NOT THE INHERITED PAIR; SWITCH COMPOSES ITS OWN ARRIVAL WITHOUT LOADING CONDUCTOR — Anthony, 2026-09-14 (reported by Codex), released in 0.124.0–0.125.0.**
- **MANAGED CONDUCTOR SESSIONS CARRY AN AUTHORIZED LOCAL BUILD ACROSS FRESH DECISION CONTEXTS, WITH THE CHAT AS THE CONTROL SURFACE; NO TUI TAKEOVER; UNCERTAIN WORK IS INSPECTED, NEVER BLINDLY RELAUNCHED — Anthony, 2026-09-13/14 (reported by Codex), released in 0.123.0.**
- **OUT SAVES THE SELECTED CONTINUATION — OWNER, ACTION, AGREED OR PROPOSED STATUS, STOPPING POINT AND PENDING QUESTION — AND KEEPS EVERY RECORDED URGENT OR IMMINENT RISK INSIDE THE PICKUP READING SET — Anthony, 2026-09-13/14, released in 0.122.0–0.122.1.**
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
- **A TOKEN-BUDGET RESULT STAYS UNMEASURED; A BYTE PROXY IS GROUNDS FOR CONCERN, NOT A MEASURED FAILURE. Tony, 2026-09-09.**
- **PROGRESS MUST BE SHOWN DURING WORK, NOT ONLY IN A FINAL REPORT — AND "THE HOST CANNOT" NEEDS PROVING. Tony, 2026-09-09.**
- **TREATMENT ASSURANCE IS A LIFECYCLE, NOT A PARSE RULE — A FATAL RISK ADVANCES ON A PLANNED TREATMENT AND ACCEPTANCE DEMANDS THE VERIFIED ONE. Tony, 2026-09-03, refusing revision 1 of `risk-state-split`'s design for a circular dependency.**
- **AN OLD LEDGER PASSING WITHOUT `fatal` DOES NOT PROVE ITS SEVERITY WAS NON-FATAL — TREATMENT MIGRATES MECHANICALLY, SEVERITY NEEDS EXPLICIT PRIOR EVIDENCE OR PRODUCER REVIEW. Tony, 2026-09-03, at `risk-state-split`'s design-plan gate, refuting the session's candidate mechanical rule.**
- **THE RISK LEDGER'S `State` COLUMN SPLITS INTO SEVERITY AND TREATMENT — Tony, 2026-09-03, resolving the 2026-09-02 axes conflict on option 2 by name.**
- **STATUS IS SPOKEN AS WORK ITEM · STAGE · ISSUE · RESOLUTION PATH, IN PLAIN WORDS, AND A MESSAGE ENDS ON EXACTLY ONE QUESTION — Tony, 2026-09-03, correcting a switch-in and orient that spoke repo shorthand.**
- **COLD EYES IS THE ACCEPTANCE MECHANISM, SO A LAYER-4 BLOCK ON THE ITEM'S OWN SHIPPED CLAIMS IS REPAIRED BEFORE ACCEPTANCE — NEVER FILED AS A SECOND EXCEPTION. Tony, 2026-08-29.**
- **STANDING PRINCIPLE: DEAD SOLUTIONS STAY DEAD — a cut or ruled-out approach is not a future building block unless a named return condition fires. Tony, 2026-08-04** (its case is inside the “capturerequirements CUT at v0.73.0” entry).

## Open Questions

- **A FATAL ROW IS TOLD TO FILE INTO "WHAT WE RULED OUT", AND THAT HOME'S SHAPE WAS NEVER SETTLED.** `parse_ledger`'s refusal (`kit.py:489`) says *"record in What we ruled out; cannot pass"*, while the 2026-08-03 decision making that its own artifact has produced `## What we ruled out` sections inside three design docs and no standalone instance — so complying with the refusal has no defined form. Surfaced 2026-09-02 by `gate-reachability`'s FATAL row; it survives the 2026-09-03 axes resolution untouched. *(The other half of the 2026-09-02 entry — `LEGAL_STATES` carrying severity and disposition in one column — was RESOLVED 2026-09-03: see the risk-state-split decision in `## Key Decisions`.)*

*(Previously closed here: the vault-repo-commit question died moot at v0.83.0 — switch neither writes nor commits the vault — and model-tiered delegation was closed at v0.82.0 as subsumed by the conductor README section.)*

## Active Mode

- **`kivna/.active-modes` still holds `conductor: plan @ 2026-09-03 23:59 EDT`**, a
  parked marker left in place deliberately; never restart it, and never read it as an
  open time (a marker older than today is not one). The 2026-09-03 runs are history.
- **Machine: the Mac Studio** (`Anthonys-Mac-Studio.local`), a thin-client host —
  sessions run in tmux over SSH from the MacBook; the user's screen is on the
  laptop and `open` is a shim that copies files there (see `~/.claude/CLAUDE.md`).
- **pair: on** in this repo — partner-mode working agreement: rapid
  back-and-forth, reasoning internal unless it changes Tony's decision, ONE
  question (open by default, no X/Y binaries), interrupt early, eyeball-gated
  slices. Enforced by a UserPromptSubmit hook (`hooks/pair.sh`, reading
  `kivna/.pair`); persisted user-global in `~/.claude`.
