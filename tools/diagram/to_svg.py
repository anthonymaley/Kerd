"""Render the same element model to SVG. No dependencies.
Font differs from Excalifont, so metrics are approximate — this catches gross
layout faults (overflow, collisions, bad coordinates), not kerning."""
import html

FONT = "'Segoe Print','Bradley Hand','Chalkboard SE','Comic Sans MS',cursive"


def to_svg(els, path, pad=40):
    xs = [e["x"] for e in els] + [e["x"] + e.get("width", 0) for e in els]
    ys = [e["y"] for e in els] + [e["y"] + e.get("height", 0) for e in els]
    minx, maxx, miny, maxy = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    w, h = maxx - minx, maxy - miny

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="{minx:.0f} {miny:.0f} {w:.0f} {h:.0f}">',
        f'<rect x="{minx:.0f}" y="{miny:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#ffffff"/>',
    ]

    for e in sorted(els, key=lambda z: z["index"]):
        t, sc = e["type"], e["strokeColor"]
        bg = e["backgroundColor"]
        fill = "none" if bg == "transparent" else bg
        dash = ' stroke-dasharray="8 6"' if e.get("strokeStyle") == "dashed" else ""
        if t == "rectangle":
            out.append(
                f'<rect x="{e["x"]:.1f}" y="{e["y"]:.1f}" width="{e["width"]:.1f}" '
                f'height="{e["height"]:.1f}" rx="8" fill="{fill}" stroke="{sc}" '
                f'stroke-width="{e["strokeWidth"]}"{dash}/>')
        elif t == "ellipse":
            out.append(
                f'<ellipse cx="{e["x"]+e["width"]/2:.1f}" cy="{e["y"]+e["height"]/2:.1f}" '
                f'rx="{e["width"]/2:.1f}" ry="{e["height"]/2:.1f}" fill="{fill}" '
                f'stroke="{sc}" stroke-width="{e["strokeWidth"]}"/>')
        elif t == "text":
            size = e["fontSize"]
            lines = e["text"].split("\n")
            anchor = {"left": "start", "center": "middle", "right": "end"}[e["textAlign"]]
            ax = e["x"] + (e["width"] / 2 if anchor == "middle" else 0)
            out.append(
                f'<text x="{ax:.1f}" y="{e["y"] + size:.1f}" font-family="{FONT}" '
                f'font-size="{size}" fill="{sc}" text-anchor="{anchor}" '
                f'xml:space="preserve">')
            for i, ln in enumerate(lines):
                dy = 0 if i == 0 else size * 1.25
                out.append(f'<tspan x="{ax:.1f}" dy="{dy:.1f}">{html.escape(ln)}</tspan>')
            out.append('</text>')

    out.append("</svg>")
    open(path, "w").write("\n".join(out))
    return w, h


def overflow_report(els):
    """Bound text wider/taller than its container = a layout fault."""
    by_id = {e["id"]: e for e in els}
    faults = []
    for e in els:
        if e["type"] == "text" and e.get("containerId"):
            c = by_id.get(e["containerId"])
            if not c:
                continue
            if e["width"] > c["width"] - 8 or e["height"] > c["height"] - 4:
                faults.append((e["text"].replace("\n", " / "),
                               round(e["width"]), round(c["width"])))
    return faults


def collision_report(els):
    """Free-floating text overlapping a rectangle it is not bound to."""
    rects = [e for e in els if e["type"] == "rectangle"]
    faults = []
    for e in els:
        if e["type"] != "text" or e.get("containerId"):
            continue
        ex0, ey0 = e["x"], e["y"]
        ex1, ey1 = ex0 + e["width"], ey0 + e["height"]
        for r in rects:
            rx0, ry0 = r["x"], r["y"]
            rx1, ry1 = rx0 + r["width"], ry0 + r["height"]
            # a label sitting inside a big container is fine; flag only when it
            # straddles that container's own edge, or overlaps a small box
            small = r["width"] < 420 and r["height"] < 120
            inside = ex0 >= rx0 and ex1 <= rx1 and ey0 >= ry0 and ey1 <= ry1
            overlap = ex0 < rx1 and ex1 > rx0 and ey0 < ry1 and ey1 > ry0
            if overlap and (small or not inside):
                faults.append((e["text"].split(chr(10))[0][:46], round(ex0), round(ey0)))
                break
    return faults
