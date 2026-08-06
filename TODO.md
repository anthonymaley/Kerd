# TODO

## Now

**vault-unhook at goal, one move from done.** The expert-user pass = the 2026-08-06 boundary observation (recorded in that session log: no vault write, banner line). Next session: write the goal record `docs/gates/` citing the observation → loop rung → conductor close-out. Then pick from Backlog — freshest: the skriv/slainte/tend review (today's queue item 4) · boundary-cycle (High). Working default: per-piece evidence check — no blanket license.

Working default: per-piece evidence check — no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)` left on the board (Design: machine-checkable interface values); cache pinned at kerd/0.79.0, one version behind (repin when convenient; corrected 2026-08-05 — both skills verifiably loaded from 0.79.0 this session).

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **boundary-cycle** (Tony 2026-08-06): one act replaces the manual quit-terminal → restart → switch-in ritual — e.g. a cycle command that switches out, clears the window, switches back in. **Killer feasibility question first, verified against harness docs at frame, never from memory**: a session cannot run `/clear` on itself; candidate mechanism is a marker file + SessionStart/UserPromptSubmit hooks getting it to ~two keystrokes. Used at every 50%-context reset — the highest-frequency ritual in the workflow.
- **Boundary auto-sizing**: light/low have zero users ever (interview 2026-08-06) — kill them as user-facing modifiers; switch reads what the session changed and sizes its own boundary. Protect the three-file switch-in path absolutely.
- **Stop-hook over-prescription**: the hook nudges full switch-out when the honest need is a conductor work commit or a TODO touch — distinguish work-dirty from session-state-dirty at a real stopping point.

**Medium**
- **Revisit the journey view when more data exists** (parked 2026-08-05, Tony's call, shape agreed on mock v4 — `docs/plans/2026-08-05-journey-view-mock.html`). Settled shape: one page per journey, the idea/problem as title; A3 Proposal head (current drawn · numbered pains · proposal drawn · targets in units · cost named) + measured-in-use strip; then the ladder as sections — steps with status + facts, "what we created" with links per rung; a front page above it: what's-cooking task cards (name · sentence · % · time-left · status word) + next-up queue. Revisit condition: more journeys walked through the gates. Prerequisite surfaced: progress % and time-left need declared on-disk homes before the real page can show them. progress-html stays held at proving meanwhile; the trio plumbing stays.
- Clean krutho-strategy's stray `sessions-of-record/` — unblocked by the mode cut (v0.75.0).
- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork (`.Codex-plugin`, `/kerd:dian` references); its identity line was fixed locally in the cut, the rest of the drift stands.
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- PR-event edge in the stale CI step (goal-gate cold review find): on `pull_request` the merge ref carries base-branch trailers the branch never rendered — a converged branch could go red. Unexercised (no PR flow); scope the step to `push` or contract PR behaviour when PRs become real.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).
- **lorg-cut candidate** (Tony's canvas comment 2026-08-06: "never used… Claude has plugin management now") — evidence check per the rip discipline before any license: usage archaeology (lorg artifacts anywhere?), overlap vs `claude plugin` CLI (management ≠ gap-discovery — name what dies), README/capability-list rows die with it. **Interrogate rides the same review**: the walk found it never-invoked; its everyday tier already works without invocation; the question is whether the large-bet co-signed session needs a *skill* or just the ledger standard in docs/design/.
- **kivna verdict** — the same zero-usage smell as the vault (interview 2026-08-06: no user opens Obsidian). Import/export CONFIRMED unused (Tony 2026-08-06); their original intent was **cross-agent handoff** (export for Codex, import its output back) — never exercised, and the state-in-artifacts boundary now covers agent handoff through the repo itself (any agent reading the three files picks up the session). Evidence-checked archaeology per piece (scaffold too) before any license; the vault-unhook coverage table is its input.
- **trim-cut** — gate-routed rip (the mode-cut pattern): the functions map verdict is "dying — no job of its own" and its GAP (TODO closure not holding) has closed on evidence (closure held at every boundary since the split; completed specs are dated immutable records needing no archive). Coverage table per piece; the switch SKILL.md trim-suggestion step (line 228) dies with it — that step is why switch-out still suggests trim today (found 2026-08-06: the live skill predates the verdict); release checklist applies (count Ten→Nine, README, capability lists, version).
- Derive the rigor refusal messages (and their fixtures) from `RIGOR_LEVELS` via join — closes the goal gate's BLOCK 1 in code instead of by named risk (cold eyes 2026-08-06; doc amendment shipped meanwhile).
- `gate.py` CLI pins root to `kit.ROOT` — run from any other cwd it silently audits Kerd, not the cwd tree (cold-eyes trap 2026-08-06); consider a `--root` flag.
- A fenced code block containing a `Rigor level:` line inside a `## Release slice` section counts as a duplicate — the first product doc that documents the rule inside its own Release slice goes red (cold eyes 2026-08-06, robustness wart, nothing trips it today).
- Gate records can only say GO: a refused gate has no dated home — AU3 rejects any non-rung filename in docs/gates/ and a `*-goal.md` file would satisfy the route glob (found 2026-08-05 when progress-html's goal was refused; verdict lives in the product doc instead). Consider a refusal-record shape in the gates schema.

**Low — genuinely ignorable, and you can see what ignoring costs**
- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.68.0, and absent from the release checklist. Revive or delete.
- Stale `Kerd.md` MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**
- skriv voice profile wiring — needs non-founder-genre samples.
