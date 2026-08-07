# TODO

## In flight — written live, not at close-out

*Updated 14:59 EDT mid-session. switch-fidelity gap 13: anything worth keeping
is written the moment it exists. Tony declined to close this session because
the boundary is unverified — this section and the session log are the manual
countermeasure.*

1. **funnel-driver — THE ACTIVE ITEM.** Framed 2026-08-07
   (`docs/product/funnel-driver.md`), at the **design** rung — the 2026-08-04
   spec `docs/design/conductor-role.md` is its design. **Slice 1 shipped
   (v0.91.0):** the entry gates took conductor's pre-flight inventory, and work
   commits carry a `Piece:` trailer. **Slice 2 is the substantive one and is
   NOT framed: the three funnel stages with no owner in any skill** — nothing
   in `skills/` writes `docs/product/<slug>.md`, `docs/design/<slug>.md`, or a
   `## Release slice`. Killer risk on any further work: conductor is the only
   working instance of half the system's functions across three repos, so it
   sheds one piece at a time — additions and guarded substitutions only.
2. **switch-fidelity — MUST BE FIXED, Tony 2026-08-07.** At design. Slice 1
   shipped as v0.90.0 and **ships unverified by design**: nothing checks that a
   pickup restored what the close recorded. That is why this session could not
   safely be closed. Its slice 2 (capture the thinking layer, gaps 8-14)
   remains unframed. **Open: "let's go to slice 2" was ambiguous between this
   item and funnel-driver — not resolved.**
3. **shared-memory — journey page agreed as directional.** Three annotation
   rounds taken and recorded in `docs/design/shared-memory.md`. Steps per stage
   now defined in `docs/design/funnel-steps.md` (six harvested, Idea is Tony's,
   Live deliberately empty). Remaining stages are undrawn, which the page
   renders as blockers — correctly.

**Queued, not started:** the `rung`→`stage` machine rename across `gate.py`,
its JSON and CI (cross-cutting, owes the standing grep sweep); the gap-analysis
region on the journey head; automating the fidelity check.

## Now

**Read `## In flight` above — it is written live and supersedes this section.**

`## Now` is the current focus in one line: **funnel-driver slice 2 (the three
unowned funnel stages) and switch-fidelity's fidelity check.** Everything else
is Backlog.

**Standing conduct (2026-08-07):** Tony's rungs are frame, viability, slice and
design, plus evaluation at goal; contract and build are the model's. Do not
narrate build mechanics — commits carry the detail.

**Working default:** per-piece evidence check, no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)`
on the board (Design: machine-checkable interface values).

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **Frame switch-fidelity slice 2 — capture human input.** Gaps 10/11/12 first. The three empty homes: `what we considered` (evaluation matrix built, CI-enforced, 0 on disk), `what was thrown away` (decided 2026-08-03, 0 artifacts — the first instance now exists in switch-fidelity's own `## What we ruled out`), and the someday/maybe pile (27 dormant review triggers and return conditions, nothing fires them). Key constraint from the root cause: derivation cannot fix these — human input leaves no artifact, so capture must become a **declared artifact with a gate**, the way `## Value` already is. That is the one piece of human input that reliably survives, and it survives because `gate.py` refuses without it.
- **The release-planning artifact.** "A release is a GROUPING, not a time axis" was decided 2026-08-03 with five factors and an assembled-not-authored done condition, and **has no artifact** — `docs/product/*.md` carries a per-item `## Release slice` and nothing groups items into a release. Tony's shape (2026-08-07): roadmap → release plan → review the someday/maybe pile for what is now more feasible or relevant → pull candidates in → **once sliced, the pile is invisible and work is focused only on what made the release until "release shipped" is met.** A phase, never a notification. Interlocks with slice 2: the pile is the artifact the review reads.
- **The fidelity check** (accepted unknown from switch-fidelity, review trigger already fired by Tony asking "how can we be sure this session will be picked up?"). Nothing verifies a pickup restored what the close recorded. Ran manually once on 2026-08-07 — enumerate what the session produced, write it, read it back, report anything unfindable. That manual run is the spec for automating it.
- **boundary-cycle, in-half** (Tony 2026-08-06; the out half and the next-pick suggestion SHIPPED as conductor-boundary v0.84.0 — close-out invokes switch out and names the pick, no loop): what remains is the reset ritual's automation — today it's the banner's two keystrokes (`/clear`, then switch in). **Killer feasibility question first, verified against harness docs at frame, never from memory**: a session cannot run `/clear` on itself (wall confirmed 2026-08-06); candidate mechanism is a marker file + SessionStart/UserPromptSubmit hooks. Used at every 50%-context reset. The wider loop question (auto-pick between boundaries) was resolved to suggestion-not-loop by Tony's key; the 2026-08-02 loop-guard flip (CI can refuse now) stays noted here if it's ever re-argued.
- ~~**Boundary auto-sizing**~~ — **CLOSED 2026-08-07.** Two halves, both resolved: the modifiers were removed in v0.90.0 (they trade fidelity for cost, which requirement 5 forbids), and auto-sizing itself was **premise-dead** — it was filed against a cost that `vault-unhook` v0.83.0 had already removed. This row is the worked example behind the new `dead` closure verdict: undone, but the reason it existed had gone.
- **Plugin cache repin debt reopens on every ship.** The repo shipped v0.90.0 while the cache serves 0.88.0, so this session ran stale conductor text (missing the v0.89.0 per-phase marker instructions) and only got the marker right by reading the whole file. Structural: the only session running current cache text is one where nothing shipped. Needs a real answer, not another repin.
- **Stashes and local-equals-remote are unchecked at the boundary.** Zero mentions of `stash` in `skills/switch/SKILL.md`; a stash survives a window clear and is invisible to every other check. Surfaced by the external review 2026-08-07 and kept as the two parts of its handoff-manifest proposal that are genuinely not derivable.
- **The playbook's `## Current Status` duplicates CONTEXT.md** (59 of 229 lines) and is the section that rots — the 2026-08-06 release pass found it claiming v0.60.0 against a repo at 0.89.0 and 21 hook tests against 26. Kill it or make it a pointer.
- **Out-of-repo artifacts have no home** — PRs, URLs, decks, external docs. In-repo artifacts are reached by the board and `## Grounding`; nothing reaches these.
- **Stop-hook over-prescription**: the hook nudges full switch-out when the honest need is a conductor work commit or a TODO touch — distinguish work-dirty from session-state-dirty at a real stopping point.

**Medium**
- **The refusal surface does not travel with the plugin** (found 2026-08-06 answering Tony's CI question): `.github/workflows/gate.yml` is Kerd's own build gate — three steps are self-tests, `release` checks Kerd's version fields, `stale` compares Kerd's board, and `tools/gates/kit.py:24` derives `ROOT` from the tool's own path, so a consuming project cannot audit itself even though the cache ships `tools/`. No skill invokes any tool (grep of `skills/`: zero hits). So in a project *using* Kerd, "a model choosing to comply is not a check" still holds in full — the gates are Kerd's development discipline, not something the plugin confers. **Decided 2026-08-06 (Tony): prompt-layer-only in consuming projects is the intended contract for now.** No work queued. Return condition: the first time someone runs Kerd's ladder in a repo that isn't Kerd — at that point the `--root` flag row below becomes the cheapest first step and this reopens. README needs no amendment; its claim is scoped to "the repo carries machinery", which is true as written.
- **Revisit the journey view when more data exists** (parked 2026-08-05, Tony's call, shape agreed on mock v4 — `docs/plans/2026-08-05-journey-view-mock.html`). Settled shape: one page per journey, the idea/problem as title; A3 Proposal head (current drawn · numbered pains · proposal drawn · targets in units · cost named) + measured-in-use strip; then the ladder as sections — steps with status + facts, "what we created" with links per rung; a front page above it: what's-cooking task cards (name · sentence · % · time-left · status word) + next-up queue. Revisit condition: more journeys walked through the gates. Prerequisite surfaced: progress % and time-left need declared on-disk homes before the real page can show them. progress-html stays held at proving meanwhile; the trio plumbing stays.
- Clean krutho-strategy's stray `sessions-of-record/` — unblocked by the mode cut (v0.75.0).
- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork (`.Codex-plugin`, `/kerd:dian` references, line 42 "updated by dian close-out" — re-spotted by cold eyes 2026-08-06); its identity line was fixed locally in the cut, the rest of the drift stands.
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- PR-event edge in the stale CI step (goal-gate cold review find): on `pull_request` the merge ref carries base-branch trailers the branch never rendered — a converged branch could go red. Unexercised (no PR flow); scope the step to `push` or contract PR behaviour when PRs become real.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).
- **lorg-cut candidate** (Tony's canvas comment 2026-08-06: "never used… Claude has plugin management now") — evidence check per the rip discipline before any license: usage archaeology (lorg artifacts anywhere?), overlap vs `claude plugin` CLI (management ≠ gap-discovery — name what dies), README/capability-list rows die with it. **Interrogate rides the same review**: the walk found it never-invoked; its everyday tier already works without invocation; the question is whether the large-bet co-signed session needs a *skill* or just the ledger standard in docs/design/.
- **kivna verdict** — the same zero-usage smell as the vault (interview 2026-08-06: no user opens Obsidian). Import/export CONFIRMED unused (Tony 2026-08-06); their original intent was **cross-agent handoff** (export for Codex, import its output back) — never exercised, and the state-in-artifacts boundary now covers agent handoff through the repo itself (any agent reading the three files picks up the session). Evidence-checked archaeology per piece (scaffold too) before any license; the vault-unhook coverage table is its input.
- **CI rule for the single-definition law** (cold eyes 2026-08-06 v0.84.0 observation): nothing machine-enforces "conductor never re-describes a Switch Out step" — a future edit passes all seven steps silently. Cheap mechanical candidate: refuse if `skills/conductor/SKILL.md` matches any Switch Out `### ` heading text.
- **Close-out double-write** (same review): conductor close-out step 1 writes CONTEXT/TODO, then step 6's invoked flow overwrites both in place — pre-existing shape, now visibly redundant inside one act. Reconcile (likely: step 1 shrinks to decision-recording only) before it becomes a who-wrote-what incident.
- Derive the rigor refusal messages (and their fixtures) from `RIGOR_LEVELS` via join — closes the goal gate's BLOCK 1 in code instead of by named risk (cold eyes 2026-08-06; doc amendment shipped meanwhile).
- `gate.py` CLI pins root to `kit.ROOT` — run from any other cwd it silently audits Kerd, not the cwd tree (cold-eyes trap 2026-08-06); consider a `--root` flag.
- Gate records can only say GO: a refused gate has no dated home — AU3 rejects any non-rung filename in docs/gates/ and a `*-goal.md` file would satisfy the route glob (found 2026-08-05 when progress-html's goal was refused; verdict lives in the product doc instead). Consider a refusal-record shape in the gates schema.

**Low — genuinely ignorable, and you can see what ignoring costs**
- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.68.0, and absent from the release checklist. Revive or delete.
- Stale `Kerd.md` MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**
- skriv voice profile wiring — needs non-founder-genre samples.
