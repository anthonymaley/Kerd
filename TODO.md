# TODO

## Now

**Next: the journey-view frame conversation** — the human progress page, requirement captured from Tony 2026-08-05 (log tail, `kivna/sessions/2026-08-04.md`). Two levels: (1) *what's cooking* — what's happening right now and what's next; (2) *the end-to-end journey* per endeavour in human phase names (idea → validated → designed → spec → building X), traffic light per phase, work remaining, links opening the design canvases. Looks great, shareable as one file, READ-ONLY, derived from disk. Dropped outright (Tony): input-to-the-loop — likely unneeded if the flow is right. Separate unframed instrument: token/context usage + limits (harness state, not disk). The frame decides shipped `progress.html`'s fate — leading option: keep the trio plumbing, replace the page content. Context: progress-html slice 1 goal — machine keys passed, expert-user key REFUSED (product doc, Goal verdict section). After it: grounding-was-read. Working default: per-piece evidence check — no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)` left on the board (Design: machine-checkable interface values); cache pinned at kerd/0.74.0, four versions behind (repin when convenient).

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **CI on `~/3of3`** — *3of3 is its own project, not part of Kerd* (clarified 2026-08-04); a possible trial ground for the refusal pattern, taken up only if that project wants it. `/loop` still cannot run there until something refuses.
- Repin `leru`, `krutho-strategy`, `krutho-founders` off `kerd/0.65.0` — high consequence, **no value**: pure hygiene, one cache GC from silent breakage. `obair` has no pin at all (deliberate, or drift — unchecked).

**Medium**
- Clean krutho-strategy's stray `sessions-of-record/` — unblocked by the mode cut (v0.75.0).
- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork (`.Codex-plugin`, `/kerd:dian` references); its identity line was fixed locally in the cut, the rest of the drift stands.
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- PR-event edge in the stale CI step (goal-gate cold review find): on `pull_request` the merge ref carries base-branch trailers the branch never rendered — a converged branch could go red. Unexercised (no PR flow); scope the step to `push` or contract PR behaviour when PRs become real.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).
- Gate records can only say GO: a refused gate has no dated home — AU3 rejects any non-rung filename in docs/gates/ and a `*-goal.md` file would satisfy the route glob (found 2026-08-05 when progress-html's goal was refused; verdict lives in the product doc instead). Consider a refusal-record shape in the gates schema.

**Low — genuinely ignorable, and you can see what ignoring costs**
- README conductor section's closing line "Conductor doesn't touch git. No pulls, no pushes." contradicts the commits-its-own-work paragraph above it — stale since v0.67.0. One-line fix, next release that touches the section.
- Decide whether switch should commit the vault repo (contract vs behaviour disagree).
- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.68.0, and absent from the release checklist. Revive or delete.
- Surface model-tiered delegation in the two plugin capability-list descriptions. Open since v0.64.0.
- Stale `Kerd.md` MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**
- skriv voice profile wiring — needs non-founder-genre samples.
