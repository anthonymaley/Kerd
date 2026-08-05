# Push wiring — the staleness refuser

Living design doc. Owner: the `push-wiring` work item
(`docs/product/push-wiring.md`), release slice 1. Parent:
`docs/design/progress-view.md` (the render this piece defends). The
ladder's first design package — routed here by `gate.py route`, not by a
command.

## What it does

Makes a lying render impossible to push. A seventh CI step re-renders the
progress view from the checkout and byte-compares it against the committed
pair (`docs/plans/progress.{excalidraw,svg}`); any difference refuses the
push naming both files and the exact fix. Forgetting the refresh stops
being silent drift and becomes a named refusal.

## The `stale` subcommand

`python3 tools/diagram/progress.py stale` — check-only, mutates nothing.

1. Derive the model and render the pair to a **temp directory** (never the
   working tree — a check with side effects would dirty the CI checkout
   and surprise a local run).
2. Byte-compare each temp file against the committed pair on disk:
   `docs/plans/progress.excalidraw` and `docs/plans/progress.svg`. Both
   files, not just the canvas — a hand-edited SVG is drift too, and the
   second compare is free.
3. **Exit 0** — both identical. Print one line: `render current`.
4. **Exit 1** — any difference or either file missing. The message names
   each differing/missing file and carries the fix verbatim:
   `run: python3 tools/diagram/progress.py && git add docs/plans/progress.excalidraw docs/plans/progress.svg && git commit`.

Comparing against **disk** (not `HEAD:`) keeps one semantics everywhere:
in CI the checkout is the pushed tip, so disk IS the tip; locally the
answer is "would CI refuse this tree?" — the question a shipper actually
has. Usage errors keep the renderer's convention: any other argv prints
usage, exit 2.

## The ship flow

**Now:** commit work (with its `Piece:` trailer) → push. The render
refreshes only when someone remembers — measured 2026-08-04: two manual
rounds in one session, with the committed render misstating position
between them.

**The change:** ship becomes commit → refresh → commit the render pair →
**one push**. A tip whose render is stale is refused by CI with the fix in
the message.

**What it means:** nothing new to remember — the refuser is the teacher.
The named cost (product ledger, row 3): a per-piece push becomes a
two-commit pair, and a forgotten refresh costs one extra local round. A
push touching nothing the render derives from compares equal and passes
untouched. Render-only commits still carry **no trailer** — that is what
bounds refresh divergence at depth 1 (probed 2026-08-04: consecutive
renders byte-identical by md5), so the byte-compare converges.

## CI wiring — and a defect this design caught

Seventh step in `.github/workflows/gate.yml`, after Matrix audit:

```yaml
      - name: Progress render current
        run: python3 tools/diagram/progress.py stale
```

**The checkout must gain `fetch-depth: 0`.** `actions/checkout@v4`
defaults to depth 1; the renderer derives landed pieces from `git log`
trailers, so a shallow checkout would see one commit, derive an emptier
model, and refuse every push. The existing progress selftest never
noticed because its fixtures build their own temp git trees. Same bug
class as the 0.71.1 absolute-REPO refusal: local verifies pass in an
environment CI doesn't have. Found at design time; the build ships:

```yaml
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
```

## Determinism — why byte-compare is safe

The compare is exact, so the render must be byte-reproducible. Evidence,
read from the toolkit 2026-08-04:

- Element ids are counter-based, seeds are arithmetic (`10000 + n*7`) —
  `tools/diagram/kit.py`; no `random`, no time/date anywhere in
  `progress_kit.py` / `to_svg.py`.
- Every glob feeding output is `sorted(...)`; the one unsorted glob is a
  boolean existence check.
- `REPO` derives from `__file__` (root-independent since 0.71.1).
- SVG text metrics are pure Python arithmetic on hardcoded constants —
  no system font query.

Cross-platform byte-identity (Mac-rendered committed pair vs
Linux-rendered fresh pair) is therefore expected but **unproven until the
first CI run**: the ship step's green run on the converged tree is the
proof, and a refusal there is the finding. Named residual: if it ever
diverges, the fallback is normalising before compare — not weakening to
a semantic diff.

## Testing strategy

Fixture suite extends `progress_kit.selftest()` (temp git trees, the
established pattern):

1. **Converged tree** — pair committed from a fresh render → `stale`
   exits 0, prints `render current`.
2. **Drifted tree** — a source changes after the render (a Pieces box
   checked, no re-render) → exit 1, message names both files and carries
   the fix line.
3. **Missing pair** — no committed render → exit 1 naming the missing
   files.

At ship, refusal is demonstrated both ways on the real tree before push
(the 0.70.0 pattern): a planted stale render exits 1; the refreshed pair
returns 0. The first green CI run on the pushed SHA doubles as the
cross-platform determinism proof.

## Named answers — the stage-1 measurements

| Measurement (product doc, Value) | Target | Named answer |
|---|---|---|
| Staleness at a push tip | 0 commits | The seventh CI step byte-compares fresh vs committed at every pushed tip; any difference is a refusal, so no pushed HEAD can carry a lying render. Measured by: the both-ways refusal demonstration at ship + CI history thereafter. |
| Remember-steps per ship | 0 | Enforcement lives outside the model: nothing must be remembered, because forgetting produces a refusal whose message contains the exact fix command (fixture 2 checks the message). Measured by: the fixture asserting the fix line verbatim. |

## Out of scope, named

- **Auto-push of the refreshed render** (hook or CI-side commit) — the
  product ledger's accepted unknown stands untested; its review trigger
  fires if any slice proposes CI write-back.
- **`gate.py` rendering its have/need through the progress view** — a
  later slice.
