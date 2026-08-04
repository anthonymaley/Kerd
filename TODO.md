# TODO

## Now

**Five releases shipped 2026-08-04 evening/night (0.70.0 → 0.74.0)** — see `kivna/sessions/2026-08-04.md` (final section). Next candidates, in rough order: **the last graveyard verdict (mode + modes/)** · the remaining design-layer builds (talk-formats wiring · approaches capability + evaluation matrix · conductor graduation map · grounding-was-read · push wiring). Working default: per-piece evidence check before each transformation — no blanket license.

Debt carried: `Frame the intent` route-specific acceptance checklists; one `(?)` left on the board (Design: machine-checkable interface values); cache pinned at kerd/0.68.0, several behind.

## Backlog

*Ranked by the function 5 axes — consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**
- **The graveyard queue** (Tony, 2026-08-04: "be careful of the graveyard of skills we built and never used"). Measured never-used: mode, sherpa, interrogate, capturerequirements (+ jit mode). Interrogate transformed (0.72.0, earned its keep); capturerequirements cut (0.73.0); sherpa cut (0.74.0). **One verdict remains: the mode skill + the eleven modes/ files** (reconciliation; jit's "kept for dogfood" rationale died with the SPIKE; jit's Reqs step already re-points at the frame flow). Per-piece evidence check before execution. Principle: a tool serves a declared route or dies — never kept because it exists.
- **CI on `~/3of3`** — *3of3 is its own project, not part of Kerd* (clarified 2026-08-04); a possible trial ground for the refusal pattern, taken up only if that project wants it. `/loop` still cannot run there until something refuses.
- Repin `leru`, `krutho-strategy`, `krutho-founders` off `kerd/0.65.0` — high consequence, **no value**: pure hygiene, one cache GC from silent breakage. `obair` has no pin at all (deliberate, or drift — unchecked).

**Medium**
- Regenerate the choose-what-matters view before its next use: Bree item removed, and candidate cards must carry no skill names (`gen_choose.py`).
- Hook version staleness check in `/kerd:tend` — four occurrences now.
- Guard switch-in step 3 smoke test against context bloat (delegate the run; absorb a verdict, never a full log).

**Low — genuinely ignorable, and you can see what ignoring costs**
- Decide whether switch should commit the vault repo (contract vs behaviour disagree).
- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.68.0, and absent from the release checklist. Revive or delete.
- Surface model-tiered delegation in the two plugin capability-list descriptions. Open since v0.64.0.
- Stale `Kerd.md` MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**
- Clean krutho-strategy's stray `sessions-of-record/` — rides the mode/modes verdict (the graveyard item above).
- skriv voice profile wiring — needs non-founder-genre samples.
