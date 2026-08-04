# Diagram generator

Living design diagrams in the whiteboard grammar: numbered movements, a constant
verdict line per option, colour marking cost only, containment as boundary, and
named bets. Regenerate as decisions land — do not hand-edit the outputs.

    python3 tools/diagram/gen_excalidraw.py

Writes two files side by side into `docs/plans/`:

- `.excalidraw` — opens in Excalidraw (web, or Obsidian with the Excalidraw plugin). Editable.
- `.svg` — opens in any browser. Read-only, but renderable headlessly for review.

To look at the result without a browser session:

    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
      --screenshot=/tmp/d.png --window-size=1285,4000 --hide-scrollbars \
      --default-background-color=FFFFFFFF \
      "file://$PWD/docs/plans/2026-08-02-product-to-build.svg"

The generator runs two layout checks and prints them: bound text wider than its
container, and free text colliding with a box. Both existed because the first two
diagrams shipped unseen — the checks are the fix for generating blind, and they
caught a real overflow in the "Never" group on the first run after being added.

**One-directional.** Regenerating overwrites the `.excalidraw`, so edits made in
Excalidraw are lost. Fine while the diagram is generated; wrong if a hand-drawn
diagram is ever the source of truth. Pick which owns the file, per diagram.

## Progress renderer

The pull-only progress view: what has landed, what is in flight, what is
missing — derived from disk, never self-reported.

    python3 tools/diagram/progress.py [--json]
    python3 tools/diagram/progress.py selftest

The first invocation renders; the second runs the fixture suite (10 cases,
each in a fresh temp git tree) and exits 0/1.

One model, three surfaces: the plain invocation prints a stdout table
(BOARD ladder + GOAL strips); `--json` prints that same model as
`json.dumps(model)` and nothing else, so it pipes; every render (both
modes) also writes the canvas pair `docs/plans/progress.excalidraw` and
`docs/plans/progress.svg`.

A commit is the landing signal, never a checkbox: a `Piece: <slug>/<n>`
trailer anywhere in `git log` is the primary evidence for piece `n`, and
only specs written before any trailer exists fall back to legacy mode —
box `n` checked in the HEAD version of the contract. A checkbox alone,
checked only in the working tree, never lands a piece; it renders in
flight until a commit (trailer or HEAD-committed box) ratifies it.

Push wiring — the stage-close PUSH, dated `docs/gates/` close records,
the liveness tick, and pushed-vs-local commit annotation — is deferred
to the conductor-role graduation map. This piece builds the pull surface
those will call.

To review `docs/plans/progress.svg` headlessly, use the same Chrome
command as above, pointed at the progress SVG:

    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
      --screenshot=/tmp/d.png --window-size=1285,4000 --hide-scrollbars \
      --default-background-color=FFFFFFFF \
      "file://$PWD/docs/plans/progress.svg"
