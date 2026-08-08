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
RED = "#e03131"          # cost, or a route that leaves / blocks
GREEN = "#2f9e44"        # Tony's input into the work — his annotations
YELLOW = "#f08c00"       # meets only with a countermeasure (matrix △ marks)
GREEN_FILL = "#d3f9d8"   # the chosen option's verdict cell — a fill, not a stroke
BLUE = "#1971c2"         # changed since the file was last marked reviewed
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
            "text": s, "fontSize": size, "fontFamily": 6, "textAlign": align,
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


# ── delta marking ────────────────────────────────────────────────────────
# BLUE answers "what changed since I last looked", which on a living document
# regenerated many times a day is the thing you actually want to read.
#
# Baseline is an explicit reviewed snapshot, NOT the previous generated file
# and NOT the last commit — both move far more often than Tony reads, which
# would make blue mean "changed since some moment nobody chose".
#
# Red and green win over blue where they collide: cost and Tony's own input
# are permanent meanings, newness is temporary. A changed red element stays
# red, and the run reports the count so the delta is not silently lost.

import json as _json
import os as _os

REVIEWED_DIR = "/Users/anthonymaley/Kerd/docs/plans/.reviewed"


def _reviewed_path(out_path):
    return _os.path.join(REVIEWED_DIR, _os.path.basename(out_path))


def mark_deltas(els, out_path):
    """Colour text BLUE when it is not in the last reviewed snapshot.

    Returns (marked, suppressed): suppressed counts changed elements that kept
    a red or green colour because those meanings outrank newness.
    """
    snap = _reviewed_path(out_path)
    if not _os.path.exists(snap):
        return (0, 0)                       # never reviewed — nothing is "new"
    was = set(_json.load(open(snap))["texts"])
    marked = suppressed = 0
    for e in els:
        if e["type"] != "text" or e.get("text") in was:
            continue
        if e["strokeColor"] == INK:
            e["strokeColor"] = BLUE
            marked += 1
        else:
            suppressed += 1
    return (marked, suppressed)


class Flow(Canvas):
    """A per-stage flow diagram: a spine of numbered steps, gutters either side.

    Extracted when the second stage was drawn. The board and the flows already
    share drawing primitives; the flows now share their layout too, so a fix to
    step spacing or the legend lands on every stage rather than the one being
    edited.
    """

    X = 300
    SP_X, SP_W = 660, 600        # the spine — the steps themselves
    L_X = 300                    # left gutter — step number and kind
    R_X = 1320                   # right gutter — artifacts, approvals, notes

    def __init__(self, title, subtitle):
        super().__init__()
        self.txt(title, self.X, 80, 32)
        self.txt(subtitle, self.X, 124, 15)
        self.txt("DECISIONS are dashed  ·  ARTIFACTS are listed right",
                 self.X, 172, 14, INK)
        self.txt("RED — cost, or a route that leaves the stage / blocks it",
                 self.X, 192, 14, RED)
        self.txt("GREEN — Tony's input into the work: his annotations, "
                 "his corrections", self.X, 212, 14, GREEN)
        self.txt("BLUE — changed since you last marked this reviewed",
                 self.X, 232, 14, BLUE)
        self.y = 288

    def step(self, n, kind, title, body, artifact="", note="", colour=INK,
             dashed=False, h=None):
        """One box on the spine, with its number/kind left and artifacts right."""
        # Box height follows the TITLE. The body renders below the box, so
        # sizing from body length inflated decisions into tall empty rectangles.
        bh = h or max(60, 30 + (title.count("\n") + 1) * 22)
        self.txt(f"{n}", self.L_X, self.y + 6, 26, colour)
        self.txt(kind, self.L_X + 44, self.y + 12, 13, colour)
        self.box(title, self.SP_X, self.y, self.SP_W, bh, stroke=colour,
                 bg=GREY if not dashed and colour == INK else "transparent",
                 size=14, dashed=dashed)
        if body:
            self.txt(body, self.SP_X + 18, self.y + bh + 8, 12, INK)
        if artifact:
            self.txt(artifact, self.R_X, self.y + 4, 12, colour)
        if note:
            self.txt(note, self.R_X,
                     self.y + 4 + (artifact.count("\n") + 2) * 15, 12, RED)
        self.y += bh + (17 * (body.count("\n") + 1) + 22 if body else 26)
        return bh

    def down(self, gap=34, colour=INK, dashed=False, label=""):
        """Arrow along the spine to the next step."""
        cx = self.SP_X + self.SP_W / 2
        self.arrow([(cx, self.y), (cx, self.y + gap)], stroke=colour,
                   dashed=dashed)
        if label:
            self.txt(label, cx + 16, self.y + gap / 2 - 8, 12, colour)
        self.y += gap


def mark_reviewed(out_path):
    """Snapshot the current output as 'Tony has seen this'. Blue resets.

    Stores only the text strings, not the elements. The question this answers
    is "what wording is new", so a full element dump was 68K of duplicated
    geometry to answer a question about strings — and it would have grown by
    that much per diagram, per review.
    """
    _os.makedirs(REVIEWED_DIR, exist_ok=True)
    snap = _reviewed_path(out_path)
    with open(out_path) as f:
        doc = _json.load(f)
    texts = sorted({e["text"] for e in doc["elements"] if e["type"] == "text"})
    _json.dump({"texts": texts}, open(snap, "w"), indent=1)
    return snap
