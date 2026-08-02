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
