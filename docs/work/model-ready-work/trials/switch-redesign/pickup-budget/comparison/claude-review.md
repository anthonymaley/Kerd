# Claude review — first paired answers

## Method

I compared both answers against the files on disk, not just the packet. The packet's records are faithful: `CONTEXT.md` on disk is the packet text verbatim (110 lines), and the packet's TODO selection matches `TODO.md:8-39` exactly. I also opened every file the legacy answer cites, to test whether its extra claims are real or invented.

Corroborated: `docs/work/switch-trial/device-handoff.md` (62 lines), `kivna/sessions/2026-09-06.md` (179 lines), `docs/work/switch-trial/changes.md` (40), `TODO.md` (323), `kivna/sherpa.md:3` ("**Stage:** 4 Build"). Legacy's line counts are accurate — it read what it says it read.

`★ Insight ─────────────────────────────────────`
The two answers fail in opposite directions, which makes this a clean comparison: legacy is the better *verification* artifact (it touched disk, checked git, caught a branch mismatch) and the worse *restoration* artifact (it dropped the binding constraints). Candidate is the reverse. A restored working state is judged by what a next session can safely do from it alone — verification quality does not substitute for a carried prohibition.
`─────────────────────────────────────────────────`

## Legacy answer

**L1 — Omits the entire "Standing protections" section (`CONTEXT.md:36-52`). Severity: high.**
All five bullets are absent: per-occasion approval for real-share playback and the rule that device restrictions cannot lapse by time or unrelated assent (`:38-41`); coordinate Krutho work through work-anthony, do not unilaterally patch core-api (`:42-44`); identify a running listener before changing it, never treat a saved address as current proof (`:45-46`); ask before TV work, one open question at a time (`:47-48`); and the archive-relocation bullet (`:49-52`). The last is the most consequential: without it, a session restoring from this artifact can read the trial's archive relocation as license to prune the real main checkout — the one irreversible action in the record. The request explicitly required carrying scoped restrictions from the loaded records; this section *is* that requirement.

**L2 — Omits "Decisions that must not be reopened" (`CONTEXT.md:54-75`) in full. Severity: high.**
Missing: 401 non-disclosure / fail-closed / Home default (`:56-58`), sudo docker as intended policy (`:59-60`), debug test flags explicitly retained (`:61-64`), the prohibition on reusing `KruthoHolder.unlock()` for a local privacy gate (`:68-71`), B1 ownership and the CRLite investment stop (`:72-75`). Its `next_decision.also_open` mentions `add_shares` as "unrecorded" — source-faithful wording (`session:116` says "still owed"; `session:104-105` says the Build-exit call "is still unrecorded") — but it drops the attached prohibition that dropping the toggle "remains the producer's decision, not an automatic cleanup" (`CONTEXT.md:65-67`, `TODO.md:43`). Listing an item as open without its guard converts a settled boundary back into an available action.

**L3 — Omits the second Owed obligation entirely (`TODO.md:18-25`). Severity: high.**
`next_obligation` carries only the Krutho message. The interim-token FIELDS item — `Location.token`, three server-form UI fields, `Agent.interimToken`, `establishBridgingSession()` — is absent, along with its "**Not a tidy-up**" warning and its migration decision for stored locations. Combined with L2's loss of "debug test flags were explicitly retained; don't delete them as dead code," the restored state actively invites the deletion both sources forbid. The callerless bridging function reads as dead code to anyone who has only this artifact.

**L4 — Omits the Owed tail (`TODO.md:30-36`) and the staged D1 file (`TODO.md:26-28`). Severity: moderate.**
`handle_post_endorse`'s lenient `device_pub` decode at `:6613` against a strict unlock path, the camera-less endorsement fallback, cross-segment deployment, and Seinn's own absent revocation pipeline all vanish. Legacy's `unresolved_memory` does not recover them.

**L5 — Retains one of three evidence caveats. Severity: moderate.**
It keeps the wrong-target deletion (`CONTEXT.md:85-87`) but drops the playback-evidence caveat (`:79-84`, including "Do not repeat the overbroad claim that the journal can never supply playback evidence") and the agent-source caveat (`:88-90`, `server/seinn_agent.py` in this repo, reverify source/deployment identity before operational work). The section is titled "Evidence caveats that change the next decision"; the second is a pre-operational safety instruction.

**L6 — Its distinctive claims check out, and one is genuinely valuable.**
The branch observation is real and neither trivial nor implied by the packet: `device-handoff.md:36-39` requires branch `kerd-switch-trial-20260906`, the packet reports `pickup-comparison` with `synchronized: false`, and legacy correctly concludes no second-device trial success is claimed. Its undiagnosed-items list is grounded — relaunch lock bypass (`TODO.md:75-87`), wrong-target delete (`TODO.md:60-74`) — and its last-completed paraphrase matches `session:34-40` (build 339, `miladystarlight` 8.44 and `Lilie` 19.82 both start, rollout 4 of 4). I found no fabricated citation. One imprecision: `changes.md` has no "Trial authority" heading; the phrase is a lead-in at line 23. Non-material.

I could neither confirm nor refute its `kivna/.active-modes absent or empty` and "no progress renderer found" checks — glob does not surface dotfiles and I ran no shell commands. Not counted against it.

## Candidate answer

**C1 — Restriction carry is complete against the loaded records. Severity: n/a (strength).**
All five standing protections, all six do-not-reopen decisions, both Owed items including the migration decision and "the wire half is DONE," the Owed tail, "do not send a message merely because it is listed," "do not implement a default," and the wrong-target-delete caveat with its "keep safe-target and confirmation-scope checks" instruction. On the criterion the request named explicitly, it holds.

**C2 — Omits two of three evidence caveats (`CONTEXT.md:79-84`, `:88-90`). Severity: moderate.**
Same gap as L5 minus the deletion item it did keep. The agent-source identity caveat matters most: a later session could debug or deploy against the wrong source without the instruction to reverify.

**C3 — Omits the read-routing rule (`CONTEXT.md:96-101`). Severity: moderate.**
"Before editing a selected feature, search its subject in the original context Key Decisions (lines 168–600) and read the matching complete entries," plus the framing of Old Where We Are / Operational State / Open Questions as dated history requiring reconciliation. Its `not_read` note captures the spirit ("their claims remain saved memory, not freshly revalidated") but not the operative route into the archive. Legacy is weaker still here — it records only that archived decisions were not revalidated.

**C4 — Reports git identity without interpreting it. Severity: moderate.**
It states "This is the isolated kerd-switch-trial-20260906 replacement" while simultaneously reporting branch `pickup-comparison` and `not synchronized`. Both come from the packet and neither is false — `CONTEXT.md:3` describes itself that way — but it does not notice that the handoff record requires the checkout to *be* on `kerd-switch-trial-20260906` (`device-handoff.md:36-39`). It performed no independent check; the packet happens to match disk, so nothing false was carried, but the artifact records confidence it did not earn.

**C5 — Does not carry the undiagnosed relaunch-lock bypass (`TODO.md:75-87`). Severity: low.**
This sits in Backlog, outside the packet's `§Now` selection, so it is a limit of the supplied input rather than a fidelity failure — and it is the kind of gap the packet's own note anticipates.

## On the input selection

The packet's TODO selection (`§Now` only) is why both artifacts are thin on Backlog-resident open work. The two masking defects survive in both answers only because `CONTEXT.md:29-34` restates them; `add_shares` survives the same way. That is a finding about the source selection, not about either answer.

## Judgment

**Candidate: supports a restoration pass.** Repair C2 and C3 before any work that touches playback evidence, agent source identity, or a feature with archived decisions behind it. Nothing in it would license an unsafe action.

**Legacy: does not support a restoration pass as durable working state**, notwithstanding that it is the better-verified artifact. Its gaps are exactly the class the request named as required, and two of them (L1's pruning license, L3+L2's deletable fields and flags) point at an irreversible action and an explicitly forbidden one. Severity for safe continuation: high.

This is not a case of the smaller input being better. Legacy read five files, checked git, and produced the single most useful independent observation in either answer (the branch mismatch). Candidate read two supplied records and no more. The differentiator is retention of binding constraints, not input size — and the strongest artifact would be candidate's restriction carry plus legacy's branch verification and Backlog items.

## Limitations

Read-only inspection of files only: I ran no git commands, so the packet's branch, commit, and clean-at-check values are unverified by me. I did not open the archives (`CONTEXT-before.md`, `TODO-before.md`), older session logs, or source code, so line references into the archives (e.g. "TODO 38–47", "context 752") are unchecked. Dotfiles such as `kivna/.active-modes` were not reachable with the tools I used. Native-session usage, token accounting, and whether either answer's device or deployment claims are *currently* true are outside what I examined — both answers correctly mark those as saved observations rather than fresh probes.

