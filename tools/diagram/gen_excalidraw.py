#!/usr/bin/env python3
"""Kerd product→build flow — living design diagram.
Grammar: numbered movements, constant verdict per row, colour marks cost only,
containment as boundary, named bets. Regenerate as decisions land."""
import json

INK = "#1e1e1e"
RED = "#e03131"
GREY = "#e9ecef"
FAINT = "#f8f9fa"

els = []
_n = [1000]


def _id(p):
    _n[0] += 1
    return f"{p}{_n[0]}"


_o = [0]


def _idx():
    _o[0] += 1
    return "a" + str(_o[0]).zfill(4)


def rect(x, y, w, h, stroke=INK, bg="transparent", sw=1, dashed=False):
    e = {
        "id": _id("r"), "type": "rectangle", "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
        "strokeWidth": sw, "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "index": _idx(), "roundness": {"type": 3}, "seed": 10000 + _n[0] * 7,
        "version": 1, "versionNonce": 20000 + _n[0] * 13, "isDeleted": False,
        "boundElements": [], "updated": 1785400000000, "link": None, "locked": False,
    }
    els.append(e)
    return e


def txt(s, x, y, size=16, stroke=INK, align="left", container=None):
    lines = s.split("\n")
    e = {
        "id": _id("t"), "type": "text", "x": x, "y": y,
        "width": max(len(l) for l in lines) * size * 0.55,
        "height": len(lines) * size * 1.25,
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "index": _idx(), "roundness": None, "seed": 10000 + _n[0] * 7,
        "version": 1, "versionNonce": 20000 + _n[0] * 13, "isDeleted": False,
        "boundElements": [], "updated": 1785400000000, "link": None, "locked": False,
        "text": s, "fontSize": size, "fontFamily": 5, "textAlign": align,
        "verticalAlign": "top", "containerId": container, "originalText": s,
        "autoResize": True, "lineHeight": 1.25,
    }
    els.append(e)
    return e


def box(label, x, y, w, h, stroke=INK, bg="transparent", size=16, sw=1, dashed=False):
    r = rect(x, y, w, h, stroke, bg, sw, dashed)
    lines = label.split("\n")
    tw = max(len(l) for l in lines) * size * 0.55
    th = len(lines) * size * 1.25
    t = txt(label, x + (w - tw) / 2, y + (h - th) / 2, size, stroke, "center", r["id"])
    t["width"], t["height"], t["verticalAlign"] = tw, th, "middle"
    r["boundElements"] = [{"type": "text", "id": t["id"]}]
    return r


X = 300
W = 1180

# ══ Title ════════════════════════════════════════════════════════════════
txt("Kerd — product to build", X, 80, 32)
txt("living design sketch · updated as decisions land · 2026-08-02", X, 124, 15)

# ══ 1. The four altitudes ════════════════════════════════════════════════
txt("1. The four altitudes — where work lives", X, 200, 24)

BANDS = [
    ("Product", "the idea, viability, business model,\nGTM, competitive landscape",
     "no artifact  ·  no read path", "rebuilt by hand, per session", True),
    ("Design", "approaches, architecture,\ncomponents, data flow",
     "superpowers specs  ~110 ln", "alive — but never retrieved", True),
    ("Contract", "exact files, signatures,\nthe why, a verify command",
     "conductor spec file  ~200 ln", "won this rung in July", False),
    ("Implementation", "the steps themselves",
     "superpowers plans  ~510 ln", "0 of 472 boxes ticked", False),
]
y = 250
for name, what, occupant, verdict, gap in BANDS:
    c = RED if gap else INK
    rect(X, y, W, 108, stroke=c, dashed=gap)
    box(name, X + 20, y + 22, 190, 64, stroke=c, bg="transparent" if gap else GREY)
    txt(what, X + 240, y + 22, 15)
    txt(occupant, X + 240, y + 66, 13, c)
    txt(verdict, X + 820, y + 42, 17, c)
    y += 126

txt("release (MVP → v1 → v1.2) is not a fifth rung — it is the time axis,\n"
    "and each release cuts through all four", X + 20, y + 8, 15)

# ══ 2. What is actually used ═════════════════════════════════════════════
y2 = y + 90
txt("2. What Tony actually uses", X, y2, 24)

GROUPS = [
    ("Daily", ["switch  20×/day", "skriv"], INK, "the boundary and the writing"),
    ("Implicit", ["kivna", "conductor"], INK, "ride along with switch"),
    ("Occasional", ["tend", "trim"], INK, "setup, and janitorial"),
    ("Never", ["mode", "sherpa", "interrogate", "capturerequirements"], RED,
     "the entire front of the lifecycle"),
]
gy = y2 + 50
gx = X
_gh = 56 + max(len(m) for _, m, _, _ in GROUPS) * 52 + 34   # stack + caption band
for gname, members, colour, note in GROUPS:
    gw = 290
    rect(gx, gy, gw, _gh, stroke=colour, dashed=(colour == RED))
    txt(gname, gx + 16, gy + 12, 19, colour)
    my = gy + 52
    for m in members:
        box(m, gx + 20, my, gw - 40, 42, stroke=colour,
            bg=FAINT if colour == INK else "transparent", size=15)
        my += 52
    txt(note, gx + 16, gy + _gh - 26, 12, colour)
    gx += gw + 15

txt("pair is not in this list — it is a one-time toggle, on in this repo right now,\n"
    "its hook firing on every message. Correct usage, not a dead skill.",
    X, gy + _gh + 18, 14)

# ══ 3. Why the front is dead ═════════════════════════════════════════════
y3 = gy + _gh + 92
txt("3. Why — nothing routes to them", X, y3, 24)

ry = y3 + 50
rect(X, ry, W, 250, stroke=INK)

box("switch", X + 60, ry + 40, 190, 55, bg=GREY)
box("conductor", X + 60, ry + 140, 190, 55, bg=GREY)
txt("offers", X + 268, ry + 52, 14)
box("kivna   slainte   switch", X + 340, ry + 140, 330, 55, bg=FAINT, size=14)
txt("conductor's only routes — all lateral or downstream", X + 340, ry + 205, 13)
txt("no upward route exists", X + 340, ry + 108, 15, RED)

box("sherpa", X + 830, ry + 80, 250, 75, stroke=RED, dashed=True, size=18)
txt("ORPHAN — referenced by nothing.\nreachable only by typing its name.",
    X + 790, ry + 168, 14, RED)

txt("superpowers wins the same contest by injecting a routing instruction at session\n"
    "start: \"you MUST use this before any creative work\". It routes itself. Sherpa waits.",
    X + 20, ry + 268, 15)

# ══ 4. The bets ══════════════════════════════════════════════════════════
y4 = ry + 340
txt("4. What this rides on", X, y4, 24)

by = y4 + 50
rect(X, by, W, 300, stroke=INK)

txt("DESIGN RUNG — genuinely missing, and the one conductor reached outside for.\n"
    "   Not sherpa (staging), not interrogate (viability), not capturerequirements (MVP reqs).\n"
    "   None of the four dead skills is a design step. Routing would not have filled this.",
    X + 25, by + 22, 15, RED)

txt("ROUTING BET — that the dead four come alive once reachable.\n"
    "   Untested, and it is the fork: if you would skip them anyway, wiring routes just\n"
    "   adds gates between you and the build. Rip instead. — PENDING APPROVAL",
    X + 25, by + 110, 15, INK)

txt("ENFORCEMENT — no bet. 0 CI workflows, 0 pre-commit hooks, every repo.\n"
    "   Every gate in this system is a model choosing to comply. Nothing can refuse.\n"
    "   The only item that changes what is possible rather than what is likely.",
    X + 25, by + 198, 15, INK)

# ══ 5. trim's exit ═══════════════════════════════════════════════════════
y5 = by + 350
txt("5. trim disappears — once its causes do", X, y5, 24)

ty = y5 + 50
rect(X, ty, W, 150, stroke=INK)
box("superpowers plans\nget huge", X + 40, ty + 30, 260, 80, stroke=INK, bg=GREY, size=15)
txt("SOLVED — conductor took\nthat rung in July", X + 330, ty + 45, 14)
box("TODOs don't\nget cleared", X + 620, ty + 30, 260, 80, stroke=RED, bg="transparent", size=15)
txt("switch-out closure\ninference isn't holding", X + 910, ty + 45, 14, RED)

txt("trim is janitorial work generated by two other problems. Fix the second and it has\n"
    "no job left. Rip after that, not before.", X + 20, ty + 168, 15)


# ══ 6. Functions we need — agnostic of what implements them ══════════════
import sys; sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from gen_functions import FUNCTIONS

W6 = 1560
y6 = ty + 230
txt("6. The functions we need — inputs, outputs, and how we would know", X, y6, 24)
txt("named for what they must do, not for the skill that happens to do it. "
    "working functions merged; gaps kept separate.", X, y6 + 34, 15)

STATUS = {"ok": (INK, GREY), "GAP": (RED, "transparent"),
          "unused": (RED, "transparent"), "external": (INK, "transparent"),
          "dying": (INK, "transparent")}

# column geometry
C_FN, W_FN   = X + 16,   240
C_TD, W_TD   = X + 268,  160
C_IN         = X + 440
C_OUT        = X + 810
C_MEA        = X + 1180
ROW_H        = 66

# header row
txt("FUNCTION", C_FN, y6 + 74, 13)
txt("TODAY", C_TD, y6 + 74, 13)
txt("INPUTS", C_IN, y6 + 74, 13)
txt("OUTPUTS", C_OUT, y6 + 74, 13)
txt("HOW WE WOULD KNOW", C_MEA, y6 + 74, 13)

fy = y6 + 100
for layer, fns in FUNCTIONS:
    h = 38 + len(fns) * ROW_H
    lc = RED if all(f[2] in ("GAP", "unused") for f in fns) else INK
    rect(X, fy, W6, h, stroke=lc)
    txt(layer, X + 18, fy + 9, 17, lc)
    ry_ = fy + 36
    for name, today, status, ins, outs, mea in fns:
        colour, fill = STATUS[status]
        box(name, C_FN, ry_, W_FN, 50, stroke=colour, bg=fill, size=13)
        txt(today if today else "— nothing —", C_TD, ry_ + 4, 12, colour)
        txt(status.upper(), C_TD, ry_ + 34, 11, colour)
        txt(ins, C_IN, ry_ + 8, 12)
        txt(outs, C_OUT, ry_ + 8, 12)
        txt(mea, C_MEA, ry_ + 8, 12, colour if status == "GAP" else INK)
        ry_ += ROW_H
    fy += h + 14

txt("5 gaps  ·  3 built but unused  ·  6 working.\n"
    "\"Route to the altitude\" is the keystone: nothing performs it, and it is what would\n"
    "decide whether the three unused ones are ever reached at all.",
    X + 18, fy + 10, 15, RED)

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
       "elements": els,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
       "files": {}}

out = "/Users/anthonymaley/Kerd/docs/plans/2026-08-02-product-to-build.excalidraw"
with open(out, "w") as f:
    json.dump(doc, f, indent=2)
print("wrote", out)
print("elements:", len(els), "| red:", sum(1 for e in els if e.get("strokeColor") == RED))

# ══ dual output: SVG beside the .excalidraw ══════════════════════════════
sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from to_svg import to_svg, overflow_report, collision_report

svg_out = out.replace(".excalidraw", ".svg")
w, h = to_svg(els, svg_out)
print("wrote", svg_out, f"({w:.0f}x{h:.0f})")

faults = overflow_report(els)
if faults:
    print(f"\n!! {len(faults)} bound-text overflow(s):")
    for t, tw, cw in faults:
        print(f"   {t[:52]:<52} text {tw}px > box {cw}px")
else:
    print("\nno bound-text overflow")

col = collision_report(els)
if col:
    print(f"!! {len(col)} text/box collision(s):")
    for t_, x_, y_ in col:
        print(f"   {t_:<46} at ({x_},{y_})")
else:
    print("no text/box collisions")
