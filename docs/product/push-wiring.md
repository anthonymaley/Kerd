---
route: new
stage: sliced
---

# Push wiring — the progress render pushes itself

## Value

Today the living render (`docs/plans/progress.{excalidraw,svg}`) updates
only when someone remembers to run the renderer and commit the pair —
measured 2026-08-04: two manual refresh-and-commit rounds in one session,
and between them the committed render misstates position (the mode-cut
strip sat at "9 landed · 1 in flight" after all 11 pieces had landed).

Value, in units:

- **Staleness at a push tip** — commits by which the committed render lags
  a fresh render at any pushed HEAD: today unbounded (whenever someone
  forgets), target **0** (a push whose tip carries a lying render is
  refused).
- **Remember-steps per ship** — render obligations a human or model must
  hold in their head: today 1–2, target **0** (enforced from outside the
  model, never remembered).

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Self-reference loop: the refresh commit changes what the next render shows, so a strict staleness rule or auto-push never converges and every ship deadlocks | yes | all ships blocked — full declared value lost and the ship flow with it | certain without countermeasure | 2026-08-04 probes: re-render after the trailer commit modified both files (depth-1 drift); two consecutive renders byte-identical (md5 pair) — render-only commits carry no `Piece:` trailer, so divergence stops at depth 1 | countermeasure - permanent | Render-only commits never carry a trailer; the refresh commit follows its trailer commit in the same push, so every pushed HEAD is converged and a plain byte-compare suffices | |
| Moving the push into CI needs write-back permission and races concurrent pushes | no | render commits from CI could conflict with local work or fail silently on token scope | medium | `.github/workflows/gate.yml` carries no `permissions:` block and no push step today; untested | accepted unknown | | Fires if any slice proposes CI-side commits — test token scope + race behaviour first |
| The staleness gate changes conductor's work-commit flow: a trailer commit can no longer push alone — its render refresh must ride the same push | no | per-piece pushes become a two-commit pair; forgetting refuses the push at CI, cost is one extra local round | high (every ship) | this session's flow: 874c93e (trailers) pushed before 8318029 (render) — under the gate that first push would refuse | countermeasure - permanent | Ship flow becomes commit → refresh → commit render → push once; the refusal message names the fix | |

## Release slice

Smallest valuable slice: **the staleness refuser** — `progress.py` gains a
`stale` subcommand (fresh render byte-compared against the committed pair
at HEAD; differing = exit 1 naming both files), wired as a seventh CI
step. Deliberately excluded from this slice, named: any auto-push
mechanism (hook or CI-side commit — the second ledger row stands untested)
and gate.py rendering its have/need through the view (a later slice).
The slice's win: a pushed HEAD can never silently carry a lying render —
forgetting becomes a refusal, not a drift.
