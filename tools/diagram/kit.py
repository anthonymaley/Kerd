#!/usr/bin/env python3
"""Shared drawing primitives for Kerd's generated diagrams.

Extracted from gen_excalidraw.py once a second generator needed them. The board
(gen_excalidraw) and the per-stage flows (gen_flow) must not drift into two
dialects of the same grammar, so they draw with one set of helpers.

Grammar reminder: colour marks COST, not category. Containment is the default
boundary. Arrows are used only where SEQUENCE is the point — a flow — never to
express membership, which containment already says better.
"""

INK = "#1e1e1e"
RED = "#e03131"
GREY = "#e9ecef"
FAINT = "#f8f9fa"


class Canvas:
    """Element accumulator. One per output file."""

    def __init__(self):
        self.els = []
        self._n = 1000
        self._o = 0

    def _id(self, p):
        self._n += 1
        return f"{p}{self._n}"

    def _idx(self):
        self._o += 1
        return "a" + str(self._o).zfill(4)

    def _base(self, kind, x, y, w, h, stroke, bg, sw, dashed):
        return {
            "id": self._id(kind[0]), "type": kind, "x": x, "y": y,
            "width": w, "height": h, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
            "strokeWidth": sw, "strokeStyle": "dashed" if dashed else "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "index": self._idx(), "seed": 10000 + self._n * 7,
            "version": 1, "versionNonce": 20000 + self._n * 13,
            "isDeleted": False, "boundElements": [], "updated": 1785400000000,
            "link": None, "locked": False, "customData": {"gen": "kerd"},
        }

    def rect(self, x, y, w, h, stroke=INK, bg="transparent", sw=1, dashed=False):
        e = self._base("rectangle", x, y, w, h, stroke, bg, sw, dashed)
        e["roundness"] = {"type": 3}
        self.els.append(e)
        return e

    def ellipse(self, x, y, w, h, stroke=INK, bg="transparent", sw=1, dashed=False):
        e = self._base("ellipse", x, y, w, h, stroke, bg, sw, dashed)
        e["roundness"] = None
        self.els.append(e)
        return e

    def txt(self, s, x, y, size=16, stroke=INK, align="left", container=None):
        lines = s.split("\n")
        e = self._base("text", x, y,
                       max(len(l) for l in lines) * size * 0.55,
                       len(lines) * size * 1.25,
                       stroke, "transparent", 2, False)
        e["roundness"] = None
        e.update({
            "text": s, "fontSize": size, "fontFamily": 5, "textAlign": align,
            "verticalAlign": "top", "containerId": container, "originalText": s,
            "autoResize": True, "lineHeight": 1.25,
        })
        self.els.append(e)
        return e

    def box(self, label, x, y, w, h, stroke=INK, bg="transparent", size=16,
            sw=1, dashed=False):
        r = self.rect(x, y, w, h, stroke, bg, sw, dashed)
        lines = label.split("\n")
        tw = max(len(l) for l in lines) * size * 0.55
        th = len(lines) * size * 1.25
        t = self.txt(label, x + (w - tw) / 2, y + (h - th) / 2, size, stroke,
                     "center", r["id"])
        t["width"], t["height"], t["verticalAlign"] = tw, th, "middle"
        r["boundElements"] = [{"type": "text", "id": t["id"]}]
        return r

    def line(self, pts, stroke=INK, sw=1, dashed=False, arrow=False):
        """Polyline through absolute points. arrow=True puts a head on the last
        segment. Excalidraw stores points relative to the element origin."""
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, y0 = xs[0], ys[0]
        e = self._base("arrow" if arrow else "line", x0, y0,
                       max(xs) - min(xs), max(ys) - min(ys),
                       stroke, "transparent", sw, dashed)
        # roundness MUST be None. With {"type": 2} Excalidraw curve-fits the
        # polyline, and an orthogonal path (down, across, down) comes out as a
        # loop. The SVG mirror drew them straight and passed every check —
        # the fault was only visible on the real canvas.
        e["roundness"] = None
        e["points"] = [[p[0] - x0, p[1] - y0] for p in pts]
        e["lastCommittedPoint"] = None
        e["startBinding"] = e["endBinding"] = None
        e["startArrowhead"] = None
        e["endArrowhead"] = "arrow" if arrow else None
        e["elbowed"] = False
        self.els.append(e)
        return e

    def arrow(self, pts, stroke=INK, sw=1, dashed=False):
        return self.line(pts, stroke, sw, dashed, arrow=True)
