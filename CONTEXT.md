# Context

## What This Is

Kerd — a Claude Code plugin: twelve workflow skills (conductor, switch, visuals and agent replaced or joined at 0.107.0–0.109.0). Core skills: drive (the work-item umbrella, v0.104.0), switch (session handoff/boundary), conductor (session discipline), kivna (vault/knowledge), tend, slainte, skriv, lorg, interrogate (the tiered risk ledger), pair. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0 — the lifecycle IS the ladder), mode + all eleven modes/ files (v0.75.0 — routing belongs to the gates), trim (v0.87.0 — its core job was machine-refused by construction).

## Where We Are

**Current release boundary: 0.115.0.** Anthony authorized review, implementation
and publication of the compact arrival and coordinated Out, then added ongoing
Agent roles. Branch `main`, subject
"Release Kerd 0.115.0: compact arrival and coordinated closeout". This pointer
is prepared before that save; resolve its revision and remote state with Git.
Includes the tight completion/YOU boxes and end marker, one Out owner preserving
participating sessions' context, memory readiness separate from Git save, and
private ongoing partner roles. Evidence and review disposition:
`docs/work/switch-coordinated-closeout/work.md`. No installation refresh or live
UX verdict. The prior source release was 0.114.0 at b80d932.

**0.112.0 and 0.113.0 are released — 2026-09-12, late.** On `origin/main`: 0.107.0 through 0.111.0, then 0.112.0 (branch
`main`, subject "One arrival, one decision; the saved-place box returns":
one arrival with the decision in YOU, the Out saved-place box, Codex's five
follow-up fixes). 0.113.0 — the Codex core package (Conductor, Switch,
Visuals, Agent from one source, no legacy skills or hooks), measured reading
selections (`read_args`, `reaches_eof`), and the pickup clarifications — was
reviewed by both sessions, released by Codex on `main` as `4532f4c`, subject
"Release Kerd 0.113.0: Codex core and reliable pickup", remote-verified from
this session after a fetch and CI green.

**Records:** [the Codex package record](docs/work/codex-plugin/work.md)
(package, install, reviews, live checks);
[the release-111 spec](docs/work/release-111-followup/spec.md) and
[the Out-box review](docs/work/release-111-followup/out-box-review.md);
[the closure-review trial](docs/work/model-ready-work/trials/2026-09-12-conductor-session-closure-review.md).

**Installed state, not to be overclaimed:** the local Codex user installation
is an older generated 0.113.0 snapshot that predates the pickup corrections;
it needs an explicit refresh before those are tested. The Claude installation
was not changed; this machine's plugin cache held 0.111.0 at midday.

**Owed, none a build:** the live checks in TODO `## Now` — a fresh Codex
session on the refreshed snapshot, a fresh Claude pickup on a released build,
the behavioural clarification scenario run by a model — and recording today's
three product rulings in `docs/decisions.md`. The Agent TUI route re-run owed
since 0.109.0 is met: two Codex reviews came back by `codex queue` today.

**The launch sequence is retained and untouched** — five outcomes, 0 of 5:
`risk-state-split` at acceptance owing its evidence-backed record,
`gate-reachability` refusing at viability on row 2, the four exposed
fatal/accepted risks, then the `agent-request` pilot. Detail in TODO.md under
"Earlier launch sequence — retained pending reconciliation" and in
`kivna/sessions/2026-09-03.md`.

**Kept out of Git by instruction, exact paths:** `kerd-laptop-result.patch` at
the root (2026-09-09). Name it with `--preserve` at every save.

**Pickup reading set** (Switch Out, 2026-09-12): this file complete;
`TODO.md` `## Now`; `kivna/sessions/2026-09-12.md` complete. Add
`docs/work/codex-plugin/work.md` only when acting on the Codex package.
Helper arguments: `--record CONTEXT.md --file kivna/sessions/2026-09-12.md --section TODO.md "## Now"`.
Measured at that Out, before the 0.114.0 release-pointer edits: 18,626 bytes,
about 4,657 tokens estimated at four bytes each (not a
tokenizer reading), against the 8,000 target — within target.

## Key Decisions

Rulings only, kept here while they govern the next work; the full case for each, and every
other standing decision, is in [docs/decisions.md](docs/decisions.md) (158 entries at the
2026-09-11 move, newest first, indexed by ruling). The three risk-ledger and acceptance
rulings are held because the retained launch sequence resumes under them; they leave when
it does.

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
