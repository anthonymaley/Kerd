# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Release boundary: 0.133.0, `7cf5782` on `main`, subject "Release Kerd 0.133.0: a
delegated job names the model it runs on, in the call" (2026-09-16, built and released
by Claude, reviewed by Codex across three before-push rounds; CI entry gate green —
re-resolve its revision and CI with Git and `gh` rather than trusting this line).**
Four releases this sitting:
- **0.131.0**: a native picker may follow the speech bubble, never replace it; Agent's
  missing partner role offers four shortcuts. This withdrew 0.129.0's "no native
  pickers", which was Claude's over-reach defended by a *passing test* for two releases.
- **0.132.0**: visuals by default and the decision capsule, combined. The visual
  threshold is countable — two or more connected parts, a branch, an ownership boundary
  or a before → after change — because "substantial" carries no test a model can fail.
  Both rules behaviourally evidenced; see `docs/work/visual-communication/work.md`.

**The finding worth carrying: the defect was a class of sentence, not one sentence.**
Seven were closed across three files, each reading like discipline while handing the
model an unfalsifiable judgment about its own work ("only if it clarifies a real
relationship", "whenever they help", "when it helps", "a substantial proposal",
"Optional job/diagram tools", the inline-sketch licence). Static gates were green the
whole time all seven were live.

**Evidence went wrong twice before going right**, and the corrections are recorded, not
buried: the first behavioural design had no control arm; the second was scored off disk
while workers were still running and produced a reported failure that did not exist.
The third used three arms isolating each rule, byte-identical prompts, and criteria
fixed in writing before the last runs reported. Method, not just result:
`docs/work/visual-communication/work.md`.

**Installed state, not to be overclaimed:** the plugin cache now carries 0.132.0 and the
session that picked up on 2026-09-16 at 14:33 is running it — the first arrival to run
from an installed post-0.129.0 plugin. Codex still needs a fresh build plus
`codex plugin add`. Nothing from 0.133.0 has run through an installed plugin; its
behavioural run read the working tree directly.
Archify installed 2026-09-15 21:37 at `~/.agents/skills/archify`, `doctor` 15/15, zero
runtime dependencies, still a dev snapshot `2.17.0-dev.1`; its installer reported two
Socket alerts that were never identified.

**0.133.0, the explicit-model dispatch contract — RELEASED** at `7cf5782`, CI green,
Anthony's word given at 18:02. **Claude owns build and release; Codex is the pairing
partner for expert review and investigation** — that ruling supersedes the 08:13
agreement giving Codex the implementation.

**Selected continuation (Anthony's priority, 2026-09-16 18:13, after this release):**
close the records (done in this save), **update the installed plugins — Claude 0.132.0,
Codex 0.129.0, neither running 0.133.0**, then fix the CI/test-path defect as a small
standalone change. Nothing else holds up using 0.133.0.

**Anthony refused the hook design at 16:48** — "It turns a missing tool argument into
a hook subsystem" — and set the contract instead: `model` requests Haiku/Sonnet/Opus/Fable,
`subagent_type` sets the effort, the grid names both concretely before dispatch,
"per definition" or "inherited" is invalid, and `job_evidence.py` verifies afterward.
**A `PreToolUse` hook, a matcher framework and a model×effort matrix are out of scope
by that refusal; the `hooks.json` nesting trap is no longer this release's problem.
Do not revive them.** Palette drift is separate work, and Krutho is Anthony's brand,
not Kerd's.

What the release says, and its ceiling: naming `model` is a *request*. With
`CLAUDE_CODE_SUBAGENT_MODEL_FORCE` set to `1` the host ignores the field and a caller
cannot pass a model at all, and an organization's `availableModels` allowlist can
substitute another; observed evidence, not the call, establishes what ran. An omitted
`model` falls through to `CLAUDE_CODE_SUBAGENT_MODEL` or the caller's model — a model
the call never selected. `requested_model: null` is the countable failure signature,
but only when that job's metadata parsed without a model-related gap.

Evidence: one real mixed-model fan-out — `haiku`/low, `sonnet`/medium, `opus`/high in
one dispatch, observed `claude-haiku-4-5-20251001`, `claude-sonnet-5`, `claude-opus-5`.
The Haiku job returned no effort records, so its effort is unverifiable, not confirmed.
728 tests green, `gate.py release` clean, hooks 21/21.

Reviewed twice: an Opus job at high effort (eleven findings, all acted on) and Codex
`codex-tui`'s before-push gate (**verdict: not ready to push**, five findings, all
applied after retrieval — the all-keys absolute that made the no-effort-agent route
impossible, the unqualified null signature, request-versus-execution overclaims, the
README's narrowing to "player", and this file itself still restoring the refused
design). Round 2 found three more — forced-model mode making the rule unsatisfiable
exactly when it binds, two assertions that guarded phrases rather than facts, and
selection wording where only a request is established. **Round 3 passed: "ready for
Anthony's release decision. No blocking findings."** Anthony authorized the push at
18:02.

**Carry this forward:** three of this release's defects were the same error — a rule
stated so absolutely that a legitimate situation could not satisfy it. That is
0.132.0's own defect class, produced three times while removing it. Codex's closing
judgment, worth honouring: three rounds of prose hardening is the limit of useful
refinement; observe real dispatches and change it again only for demonstrated
behaviour.

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

**Routing:** `codex-tui` carries checkpoints + before-push and is now the expert
reviewer and investigator by Anthony's 14:21 ruling; its partner role is still
undefined in the binding. The Claude session holding `kerd-b5-review` designates its
successor against this file after this save.

**Pickup reading set** (Switch Out, 2026-09-16):
- this file complete, for position, the agreed continuation, rulings and deferred items;
- `TODO.md` `## Now` with its child section, the designated active list;
- `kivna/sessions/2026-09-16.md`, the sitting's account including the evidence method
  and the ownership collision;
- `docs/work/visual-communication/work.md` `## Now`, the 0.132.0 record;
- `docs/work/model-dispatch-guard/work.md` complete, the 0.133.0 record — the refused
  design and why, the two review passes, the corrected facts and the ceiling on what
  the contract can promise; `direction.html` beside it is its rendered view.

Open `docs/decisions.md` for any ruling's case (the newest three are the ownership
split, the countable visual threshold and the capsule rule).

## Key Decisions

Rulings only, kept here while they govern the next work; the full case for each, and every
other standing decision, is in [docs/decisions.md](docs/decisions.md) (newest first, indexed
by ruling; four added this sitting — the ownership split, the countable visual threshold,
the decision capsule and the picker correction). The three risk-ledger and acceptance
rulings are held because the retained launch sequence resumes under them; they leave when
it does.

- **CLAUDE OWNS BUILD AND RELEASE; CODEX IS THE PAIRING PARTNER FOR EXPERT-LEVEL REVIEW AND INVESTIGATION — Anthony, 2026-09-16 14:21.** The reviewer does not touch the tree, and the builder reports a release remote-verified before follow-on work starts. Replaces the 08:13 agreement giving Codex the 0.133.0 implementation, after a shared-tree collision made the two change sets inseparable in Git.
- **A RENDERED VIEW IS THE DEFAULT WHENEVER A PROPOSAL CARRIES TWO OR MORE CONNECTED PARTS, A BRANCH, AN OWNERSHIP BOUNDARY OR A BEFORE → AFTER CHANGE; diagram-design AND Archify ARE REQUIRED TOOLS — Anthony, 2026-09-15 15:26/15:31/21:37, released in 0.132.0 and behaviourally evidenced 3/3 against 0/3.** The threshold is countable because "substantial" carries no test a model can fail; only a single action or a factual answer stays text, and being easy to describe in words does not make it one.
- **A CONSEQUENTIAL QUESTION KEEPS ITS ANSWER-READY FACTS IMMEDIATELY ABOVE IT, WITH THE RECOMMENDATION RESTATED THERE EVEN IF IT APPEARS EARLIER; THE BUBBLE NAMES THE CONCRETE ACTION AND TARGET — Anthony, 2026-09-16, released in 0.132.0, 4/4 against 0/4 after tightening from 1/3.** Ordinary Switch In is exempt; that exemption rests partly on a behaviour deferred at 0.131.0 and still unobserved.
- **CONTEXT PRESSURE IS HANDLED BY ROLLING TO A FRESH SESSION FROM KERD'S SAVED PLACE, NEVER BY COMPACTION; AN INTERACTIVE SESSION SWITCHES OUT WHEN THE PERSON DECIDES; AUTOMATIC PRESSURE HANDLING IS ONLY FOR UNATTENDED ROLL — Anthony, 2026-09-15 13:39/13:42, applied in 0.130.0.**
- **AN UNATTENDED CLAUDE ROLL RUN IS ASKED FOR ITS SAVED PLACE AT 65% OF ITS REPORTED CONTEXT WINDOW (USED TOKENS), NO ABSOLUTE CAP; READINGS ARE RECORDED TO TUNE IT — Anthony, 2026-09-15 13:57, released in 0.130.0.**
- **EVERY KERD QUESTION IS ONE SPEECH-BUBBLE LINE AT THE END OF THE MESSAGE, `> 💬 **The question?**`, WITH OPTIONS OR CONTEXT ABOVE IT; A NATIVE PICKER MAY FOLLOW THE BUBBLE FOR ITS OPTIONS WHENEVER ONE SUITS, INCLUDING APPROVALS, BUT NEVER REPLACES OR PRECEDES IT — Anthony, 2026-09-15, released in 0.129.0 and corrected 19:50/19:51. The 0.129.0 "no boxed cards or native pickers" wording was Claude's over-reach, not Anthony's instruction, and a passing test defended it for two releases; **corrected and released in 0.131.0**.**
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
