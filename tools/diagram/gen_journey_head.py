#!/usr/bin/env python3
"""The story head of a journey page — drawn, through the excalidraw kit.

    python3 tools/diagram/gen_journey_head.py

Writes one editable canvas holding all three panels side by side:

    docs/plans/journey-<slug>-head.excalidraw   ← open and annotate this
    docs/plans/journey-<slug>-current.svg       ← the page embeds these
    docs/plans/journey-<slug>-problem.svg
    docs/plans/journey-<slug>-proposal.svg

One source, four artifacts. The SVGs are never hand-edited — same discipline as
the progress pair, for the same reason: two serializers means two truths.

**Colour grammar suspended here, deliberately.** The standing rule (2026-08-02)
reserves GREEN for Tony's own input, so a generated element would never use it.
Tony suspended that for these panels on 2026-08-07 — "ignore the color
convention now, just use what you want" — so green carries the benefit. Recorded
rather than silently done: the rule still stands elsewhere, and the collision it
prevents (a model's proposal reading as the human's contribution) is real. The
annotation merge below is what would surface it if it ever bites.

Annotations survive regeneration: anything in
docs/plans/annotations/journey-<slug>-head-tony.json is appended on top,
tagged, and drawn last.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, INK, RED, GREEN, GREY, FAINT, mark_deltas
from to_svg import to_svg, overflow_report, collision_report, text_overlap_report

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "shared-memory"
W = 520          # panel width
GAP = 90         # space between panels on the shared canvas

S1, S2, S3 = 15, 13, 12   # heading, body, caption


def panel_current(c):
    """Where we are: one session, everything shared, then the window clears."""
    c.box("THE SESSION", 0, 0, W, 30, INK, FAINT, S1)

    c.ellipse(30, 55, 46, 46, INK, FAINT)
    c.txt("H", 47, 68, S1, INK)
    c.txt("direction,\nthe spec", 18, 108, S3, INK, "center")

    c.ellipse(W - 76, 55, 46, 46, INK, FAINT)
    c.txt("M", W - 59, 68, S1, INK)
    c.txt("analysis,\nthe build", W - 88, 108, S3, INK, "center")

    c.arrow([(88, 78), (168, 78)], INK)
    c.arrow([(W - 88, 78), (W - 168, 78)], INK)
    c.txt("talking, both ways,\nall the time", 186, 62, S2, INK, "center")

    c.box("THE WHITEBOARD", 40, 150, W - 80, 30, INK, GREY, S2)
    c.txt("the idea  ·  the gaps  ·  the analysis  ·  the plan\n"
          "both of us hold all of it",
          72, 192, S2, INK, "center")

    c.arrow([(W / 2, 240), (W / 2, 280)], INK)
    c.box("we go to lunch", 110, 290, W - 220, 34, INK, FAINT, S1, dashed=True)
    c.txt("the context window clears", 150, 332, S2, INK, "center")


def panel_problem(c):
    """Problems & cause: code survives, human input does not."""
    c.txt("BACK IN THE ROOM", 150, 0, S2, INK, "center")

    c.box("STILL THERE", 0, 34, 235, 28, INK, GREY, S2)
    c.txt("commits · files · gates\ntests · the code", 30, 74, S2, INK, "center")
    c.txt("code leaves artifacts,\nand they cannot lie", 30, 122, S3, INK, "center")

    c.box("GONE", W - 235, 34, 235, 28, RED, FAINT, S2, dashed=True)
    c.txt("the idea · the direction\nwhat we considered", W - 210, 74, S2, RED, "center")
    c.txt("≈90% of the input,\nand it leaves nothing", W - 208, 122, S3, RED, "center")

    c.arrow([(W / 2, 168), (W / 2, 205)], RED)
    c.txt("cause", W / 2 + 12, 176, S3, RED)

    c.box("human input has nowhere to land", 30, 215, W - 60, 34, RED, FAINT, S1)
    c.txt("nothing derives it — there is no git log for a decision", 60, 256, S2, INK, "center")

    c.box("so it gets checked, reminded, and explained again", 10, 292, W - 20, 34, RED, GREY, S2)
    c.txt("nervous → dejected → \"I wasted my time and we lost the opportunity\"",
          22, 336, S2, RED, "center")


def panel_proposal(c):
    """Proposal & benefits."""
    c.box("ONE SHARED STATE, ON DISK", 60, 0, W - 120, 32, INK, GREY, S1)
    c.txt("derived, never hand-kept — it cannot go stale", 105, 42, S2, INK, "center")

    c.arrow([(180, 76), (120, 116)], INK)
    c.arrow([(W - 180, 76), (W - 120, 116)], GREEN)

    c.box("THE MODEL READS", 0, 124, 236, 28, INK, FAINT, S2)
    c.txt("files · markdown · gates\ncommits · the code", 32, 164, S2, INK, "center")
    c.txt("mechanical — its world, and understands\nthe product in human language",
          8, 212, S3, INK, "center")

    c.box("THE HUMAN SEES A WALL", W - 236, 124, 236, 28, GREEN, FAINT, S2)
    c.txt("the funnel · stages · steps\nrisks · architecture · plan", W - 214, 164, S2, INK, "center")
    c.txt("the product, in his language", W - 210, 212, S3, GREEN, "center")

    c.txt("every stage agreed by a drawing before the next one opens",
          46, 254, S2, INK, "center")

    c.arrow([(W / 2, 286), (W / 2, 318)], INK)
    c.box("we walk back in and carry on", 20, 328, W - 40, 34, GREEN, FAINT, S1)
    c.txt("a quick recap, then work — nothing re-explained", 90, 370, S2, GREEN, "center")


PANELS = [("current", panel_current), ("problem", panel_problem),
          ("proposal", panel_proposal)]


def main():
    """The head is ONE composition, not three loose panels.

    Tony's annotation, 2026-08-07: the first two panels sit inside CURRENT
    SITUATION, the third inside IDEAL SITUATION, and a GAP marker sits between
    them. That is his opening description of the room made literal — "capture
    current condition and show the ideal, then figure out the gaps that stop
    ideal from becoming reality". The gap ANALYSIS is deliberately not drawn:
    "the GAP analysis can come later btw — just showing the fit", so the region
    is reserved and labelled rather than filled or omitted.
    """
    out_dir = os.path.join(ROOT, "docs", "plans")
    merged = Canvas()

    for i, (kind, draw) in enumerate(PANELS):
        c = Canvas()
        draw(c)
        dx = i * (W + GAP) + (GAP * 2 if kind == "proposal" else 0)
        for e in c.els:
            e = dict(e)
            e["x"] = e["x"] + dx
            e["id"] = f"{kind}-{e['id']}"
            merged.els.append(e)

    # Frames, drawn under everything so the panels sit inside them.
    cur_w = W * 2 + GAP
    ideal_x = (W + GAP) * 2 + GAP * 2
    frames = Canvas()
    frames.rect(-30, -74, cur_w + 60, 470, INK)
    frames.txt("CURRENT SITUATION", -14, -66, S1, INK)
    frames.rect(ideal_x - 30, -74, W + 60, 470, INK)
    frames.txt("IDEAL SITUATION", ideal_x - 14, -66, S1, INK)

    gx = cur_w + 46
    frames.ellipse(gx, 120, 96, 106, RED)
    frames.txt("GAP", gx + 28, 160, S1, RED)

    # Reserved, not filled — the analysis comes later.
    frames.rect(-30, 452, cur_w + 60, 150, RED, dashed=True)
    frames.txt("GAP ANALYSIS — what stops ideal from being reality", -14, 466, S1, RED)
    frames.txt("comes later; the frame's numbered gaps land here", -14, 492, S2, RED)
    frames.arrow([(gx + 48, 226), (gx + 48, 430), (cur_w / 2, 430), (cur_w / 2, 452)], RED)

    merged.els = frames.els + merged.els

    head_svg = os.path.join(out_dir, f"journey-{SLUG}-head.svg")
    w, h = to_svg(merged.els, head_svg, pad=30)
    print(f"wrote {os.path.basename(head_svg)}  {w:.0f}x{h:.0f}")
    for label, faults in (("bound-text overflow", overflow_report(merged.els)),
                          ("text/box collision", collision_report(merged.els)),
                          ("text/text overlap", text_overlap_report(merged.els))):
        if faults:
            print(f"  !! {len(faults)} {label}(s): {faults[:2]}")

    ann = os.path.join(out_dir, "annotations", f"journey-{SLUG}-head-tony.json")
    if os.path.exists(ann):
        loaded = json.load(open(ann))["elements"]
        for e in loaded:
            e.setdefault("customData", {})["author"] = "tony"
            e["index"] = "z" + str(len(merged.els)).zfill(4)
            merged.els.append(e)
        print(f"merged {len(loaded)} annotation element(s)")

    canvas_path = os.path.join(out_dir, f"journey-{SLUG}-head.excalidraw")
    mark_deltas(merged.els, canvas_path)
    json.dump({"type": "excalidraw", "version": 2,
               "source": "https://excalidraw.com", "elements": merged.els,
               "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
               "files": {}}, open(canvas_path, "w"), indent=1)
    print(f"wrote {os.path.basename(canvas_path)} | elements: {len(merged.els)}")


if __name__ == "__main__":
    main()
