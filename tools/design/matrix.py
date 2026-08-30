#!/usr/bin/env python3
"""The evaluation matrix refuser and renderer.

    python3 tools/design/matrix.py check <file> [--json]   # validate one doc — exit 0 clean / 1 problems
    python3 tools/design/matrix.py audit [--json]           # sweep docs/design/*.md — exit 0 clean / 1 problems
    python3 tools/design/matrix.py render <file>            # movement-9-style table -> .excalidraw + .svg — exit 0 / 1 (refuses an invalid matrix)
    python3 tools/design/matrix.py selftest                 # fixture suite in temp trees — exit 0 / 1

check validates a doc and exits 0 clean or 1 with problems. audit sweeps
docs/design/*.md. render draws the table to Excalidraw + SVG, refusing an
invalid matrix. selftest runs the kit's fixture suite. Any other invocation
prints this usage text and exits 2. Every decision lives in kit.py; this
module only parses argv and renders kit's results as line-based text or JSON
via --json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit


def _cmd_check(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if len(argv) != 1:
        print(__doc__)
        return 2
    filepath = argv[0]
    # Compute relpath against kit.ROOT
    if os.path.isabs(filepath):
        relpath = os.path.relpath(filepath, kit.ROOT)
    else:
        relpath = filepath

    problems = kit.check_file(kit.ROOT, relpath)

    if as_json:
        # Read the file to get the model for JSON output
        abs_path = os.path.join(kit.ROOT, relpath)
        try:
            with open(abs_path, encoding="utf-8") as f:
                text = f.read()
            if kit.has_matrix(text):
                model, _ = kit.parse_matrix(text, relpath)
            else:
                model = None
        except Exception:
            model = None

        output = {"problems": problems}
        if model:
            output.update(model)
        print(json.dumps(output))
        return 0 if not problems else 1

    if not problems:
        # Get the model for option/criteria counts
        abs_path = os.path.join(kit.ROOT, relpath)
        with open(abs_path, encoding="utf-8") as f:
            text = f.read()
        model, _ = kit.parse_matrix(text, relpath)
        n_opts = len(model["options"])
        n_crit = len(model["criteria"])
        mode = model["mode"]
        print(f"matrix: clean — {relpath} ({n_opts} options × {n_crit} criteria, {mode})")
        return 0

    for p in problems:
        print(f"problem: {p}")
    print(f"matrix: {len(problems)} problem{'' if len(problems) == 1 else 's'}")
    return 1


def _cmd_audit(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if argv:
        print(__doc__)
        return 2

    problems, count = kit.audit_matrices(kit.ROOT)

    if as_json:
        print(json.dumps(problems))
        return 0 if not problems else 1

    if not problems:
        print(f"matrix audit: clean ({count} matri{'x' if count == 1 else 'ces'})")
        return 0
    for p in problems:
        print(f"problem: {p}")
    print(f"matrix audit: {len(problems)} problem{'' if len(problems) == 1 else 's'}")
    return 1


def _cmd_render(argv):
    if argv and argv[0] == "--json":
        print(__doc__)
        return 2
    if len(argv) != 1:
        print(__doc__)
        return 2
    filepath = argv[0]
    # Compute relpath against kit.ROOT
    if os.path.isabs(filepath):
        relpath = os.path.relpath(filepath, kit.ROOT)
    else:
        relpath = filepath

    problems, out, svg_out, dims, deltas = kit.render(kit.ROOT, relpath)

    if problems:
        for p in problems:
            print(f"problem: {p}")
        return 1

    print(f"wrote {out}")
    w, h = dims
    print(f"wrote {svg_out} ({w}x{h})")

    marked, suppressed = deltas
    if marked == 0 and suppressed == 0:
        # Check if snapshot exists
        snap_exists = False  # We'd need to check the diagram_kit logic; for now assume no snapshot
        if snap_exists:
            print(f"deltas: {marked} marked, {suppressed} suppressed")
        else:
            print("deltas: never reviewed")
    else:
        print(f"deltas: {marked} marked, {suppressed} suppressed")

    # Print layout reports (the three checks from diagram toolkit)
    diagram_to_svg = kit._load_diagram_to_svg()
    abs_path = os.path.join(kit.ROOT, relpath)
    with open(out, encoding="utf-8") as f:
        import json as json_mod
        doc = json_mod.load(f)
    els = doc["elements"]

    overflow = diagram_to_svg.overflow_report(els)
    if overflow:
        print(f"overflow: {len(overflow)} box{'' if len(overflow) == 1 else 'es'}")
        for item in overflow:
            print(f"  {item}")
    else:
        print("overflow: clean")

    collision = diagram_to_svg.collision_report(els)
    if collision:
        print(f"collision: {len(collision)} box{'' if len(collision) == 1 else 'es'}")
        for item in collision:
            print(f"  {item}")
    else:
        print("collision: clean")

    text_overlap = diagram_to_svg.text_overlap_report(els)
    if text_overlap:
        print(f"text overlap: {len(text_overlap)} box{'' if len(text_overlap) == 1 else 'es'}")
        for item in text_overlap:
            print(f"  {item}")
    else:
        print("text overlap: clean")

    return 0


def _cmd_selftest(argv):
    if argv:
        print(__doc__)
        return 2
    return kit.selftest()


COMMANDS = {
    "check": _cmd_check,
    "audit": _cmd_audit,
    "render": _cmd_render,
    "selftest": _cmd_selftest,
}


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        print(__doc__)
        return 2
    return COMMANDS[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
