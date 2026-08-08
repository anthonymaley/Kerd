"""Render the same element model to SVG. No dependencies.
Font metrics are approximate — this catches gross layout faults (overflow,
collisions, bad coordinates), not kerning.

The SVG is what a human actually reads; the .excalidraw canvas is what gets
annotated. Those had different fonts until 2026-08-08: the canvases took Tony's
2026-08-04 "packages read in Nunito" call, and the SVGs kept a handwriting
stack, so every rendered diagram he opened was in Comic Sans regardless. Both
sides are sans-serif now, on his call ("can we make it a sans serif font?")."""
import html
import math

FONT = "Nunito,'Helvetica Neue',Helvetica,Arial,sans-serif"


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
        elif t in ("line", "arrow"):
            pts = [(e["x"] + px, e["y"] + py) for px, py in e["points"]]
            d = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
            out.append(
                f'<polyline points="{d}" fill="none" stroke="{sc}" '
                f'stroke-width="{e["strokeWidth"]}"{dash} '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
            if e.get("endArrowhead") == "arrow" and len(pts) >= 2:
                (x0, y0), (x1, y1) = pts[-2], pts[-1]
                ang = math.atan2(y1 - y0, x1 - x0)
                for off in (2.6, -2.6):
                    hx = x1 + 11 * math.cos(ang + off)
                    hy = y1 + 11 * math.sin(ang + off)
                    out.append(
                        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{hx:.1f}" '
                        f'y2="{hy:.1f}" stroke="{sc}" '
                        f'stroke-width="{e["strokeWidth"]}" stroke-linecap="round"/>')
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


def text_overlap_report(els):
    """Free text overlapping other free text.

    The box-collision check above could not see this: two text blocks in
    adjacent rows sit beside boxes, not on them, so nothing flagged when a
    grown block ran into the row below. Every fault it missed was invisible
    for exactly the reason it was written — it was looking at rectangles.
    """
    texts = [e for e in els
             if e["type"] == "text" and not e.get("containerId")]
    faults = []
    for i, a in enumerate(texts):
        ax1, ay1 = a["x"] + a["width"], a["y"] + a["height"]
        for b in texts[i + 1:]:
            bx1, by1 = b["x"] + b["width"], b["y"] + b["height"]
            if a["x"] < bx1 and ax1 > b["x"] and a["y"] < by1 and ay1 > b["y"]:
                faults.append((a["text"].split(chr(10))[0][:40],
                               b["text"].split(chr(10))[0][:40],
                               round(a["x"]), round(a["y"])))
    return faults
