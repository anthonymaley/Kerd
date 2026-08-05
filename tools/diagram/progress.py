#!/usr/bin/env python3
"""Progress renderer: the pull-only progress view over the whole repo,
derived from disk — git log, gate route, Pieces checklists, docs/gates/ —
never self-reported, never prose.

    python3 tools/diagram/progress.py [--json]   # render: writes docs/plans/progress.{excalidraw,svg}; prints table (or the model as JSON)
    python3 tools/diagram/progress.py selftest   # fixture suite in temp trees — exit 0 / 1
    python3 tools/diagram/progress.py stale      # check-only: fresh temp render vs committed pair — exit 0 current / 1 stale

Render always exits 0 — it is a report, like `gate.py route`; drift is
shown, never failed on. With --json the canvas pair is still written, but
nothing except the JSON model is printed. Any other invocation prints this
usage text and exits 2. Every decision lives in progress_kit.py; this
module only parses argv, writes files, and prints. stale is the refuser: it
renders to a temp directory, byte-compares against the committed pair, and
exits 1 naming each differing or missing file plus the fix command; it
mutates nothing.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import progress_kit
from to_svg import overflow_report, collision_report, text_overlap_report


def _cmd_render(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if argv:
        print(__doc__)
        return 2

    model = progress_kit.derive(progress_kit.REPO)
    canvas = progress_kit.build_canvas(model)

    out, svg_out, w, h = progress_kit.write_pair(
        canvas, os.path.join(progress_kit.REPO, "docs", "plans"))

    if as_json:
        print(json.dumps(model))
        return 0

    print(progress_kit.render_table(model))
    print()
    print("wrote", out)
    print("wrote", svg_out, f"({w:.0f}x{h:.0f})")

    faults = overflow_report(canvas.els)
    if faults:
        print(f"\n!! {len(faults)} bound-text overflow(s):")
        for t, tw, cw in faults:
            print(f"   {t[:52]:<52} text {tw}px > box {cw}px")
    else:
        print("\nno bound-text overflow")

    col = collision_report(canvas.els)
    if col:
        print(f"!! {len(col)} text/box collision(s):")
        for t_, x_, y_ in col:
            print(f"   {t_:<46} at ({x_},{y_})")
    else:
        print("no text/box collisions")

    tcol = text_overlap_report(canvas.els)
    if tcol:
        print(f"!! {len(tcol)} text/text overlap(s):")
        for a_, b_, x_, y_ in tcol:
            print(f"   {a_:<40} over {b_:<40} at ({x_},{y_})")
    else:
        print("no text/text overlaps")

    return 0


def _cmd_stale():
    code, lines = progress_kit.stale(progress_kit.REPO)
    for line in lines:
        print(line)
    return code


def main(argv):
    if argv == ["selftest"]:
        sys.exit(progress_kit.selftest())
    if argv == ["stale"]:
        return _cmd_stale()
    if not argv or argv == ["--json"]:
        return _cmd_render(argv)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
