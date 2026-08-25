#!/usr/bin/env python3
"""Worked example — 'Celtic Ticket Exchange' walked through the whole agreed
flow, spark to shipped. Skills/tools called out right; RED BOXES mark places
needing Tony's deeper consideration (legend overrides the usual red = cost
for the boxes only).

    python3 tools/diagram/gen_flow_celtic_example.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREEN, BLUE, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("CELTIC TICKET EXCHANGE — the whole flow, spark to shipped",
         "a worked example through every agreed rung · drawn 2026-08-04\n"
         "skills + tools in the right gutter · the flow is the WALK's agreed "
         "system, not today's tooling.")

SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

f.txt("RED BOX — a place where Tony must think more deeply before the flow "
      "may pass (overrides red=cost, boxes only)", X, 252, 14, RED)
f.y = 300


def deeper(text):
    """Full-spine red callout box with left-aligned bound text."""
    lines = text.split("\n")
    h = int(len(lines) * 15 * 1.25) + 26
    r = f.rect(SP_X, f.y, SP_W, h, stroke=RED, sw=2)
    t = f.txt(text, SP_X + 18, f.y + 13, 12, RED, container=r["id"])
    t["textAlign"] = "left"
    t["verticalAlign"] = "middle"
    r["boundElements"] = [{"type": "text", "id": t["id"]}]
    f.y += h + 18


# ── 1 — the spark ────────────────────────────────────────────────────────
f.step("1", "SPARK", "An idea arrives: Celtic Ticket Exchange",
       "'an app where Celtic season-ticket holders pass their seat to\n"
       "another fan for matches they can't attend.' a bare idea — nothing\n"
       "declared, nothing on disk. the ENTRY GATES push it to the top:\n"
       "no rung below PRODUCT will admit work whose inputs don't exist.",
       artifact="tools: none yet — the gates\nthemselves route. today's only\n"
                "gate instance is conductor's\npre-flight inventory.")
f.down()

# ── 2 — frame the intent ─────────────────────────────────────────────────
f.step("2", "FRAME", "Frame the intent → an IDEA BRIEF",
       "triage: NEW. one conversation produces docs/product/\n"
       "celtic-ticket-exchange.md + .excalidraw: what it is · what it must\n"
       "become · the gap (matchday seats sit empty while fans want in) ·\n"
       "comparison — Twickets, StubHub, the club's own exchange · THE\n"
       "VALUE, measurable · a viability SIGNAL, not a verdict · the next\n"
       "stage's inputs. grounding: competitor scan + evidence of need +\n"
       "what we ruled out (empty on day one — read anyway, by rule).",
       artifact="skills: sensei IF its route\nmatches (asserting a position).\n"
                "sherpa Explore is the drafted\nserver — unused today.\n"
                "acceptance: machine key +\nTony approves the brief.")
deeper("DEEPER — THE VALUE, IN UNITS. what is this worth, and to whom:\n"
       "empty seats filled? fan goodwill? money? every fatal-risk verdict\n"
       "and every priority call downstream divides by this number, and it\n"
       "has exactly one source: you.")
f.down()

# ── 3 — viability ────────────────────────────────────────────────────────
f.step("3", "VIABILITY", "Test viability → qualify the killer assumption",
       "every candidate-fatal risk gets EVIDENCE — a test or an analysis —\n"
       "impact in the value's units, likelihood recorded separately, never\n"
       "multiplied. candidates here: will fans list through a non-club\n"
       "app? can a seat actually transfer inside the club's ticketing\n"
       "system? is resale even lawful? a risk left unqualified reads as\n"
       "managed — that is the failure this stage exists to stop.",
       artifact="skills: interrogate serves\nthis today. the SPIKE is the\n"
                "cheapest test of the killer\nassumption — declared, cheap,\n"
                "kill-or-keep.")
deeper("DEEPER — UK LAW MAKES UNAUTHORISED FOOTBALL TICKET RESALE A\n"
       "CRIMINAL OFFENCE (s.166 CJPOA 1994 — from training data; have\n"
       "counsel verify). impact >= the declared value at ANY likelihood =\n"
       "FATAL. the only countermeasure class visible is CLUB AUTHORISATION\n"
       "— which makes partner-with-Celtic the survival condition, not a\n"
       "feature. face-value-only exchange between verified holders may be\n"
       "the one lawful shape. this risk can reshape or kill the idea.")
f.down()

# ── 4 — scope ────────────────────────────────────────────────────────────
f.step("4", "SCOPE", "Slice a release · Set the goal",
       "a release is a GROUPING, not a date. MVP candidate: verified\n"
       "season-ticket holders only · home league games · face value only\n"
       "(the lawful shape) · one club-blessed pilot stand. dependency\n"
       "forbids groupings, what a user can absorb caps them, effort/risk/\n"
       "opportunity shape the rest. DONE is ASSEMBLED: every item is a\n"
       "check against something an earlier stage declared.",
       artifact="skills: sherpa Launch drafted\nfor this — unused today.\n"
                "risk arrives PRE-QUALIFIED\nfrom viability; never\nre-argued here.")
f.down()

# ── 5 — choose ───────────────────────────────────────────────────────────
f.step("5", "CHOOSE", "Choose what matters next",
       "two axes, both outcome: consequence × value. every candidate names\n"
       "WHAT WE LOSE by not choosing it; blocked items are separated, not\n"
       "ranked. the first pick writes itself: the club-authorisation\n"
       "conversation — highest consequence, and it gates everything else\n"
       "on this page.",
       artifact="view: a choose-what-matters\nboard, regenerated per\ndecision.")
f.down()

# ── 6 — design ───────────────────────────────────────────────────────────
f.step("6", "DESIGN", "Design the solution → ONE package",
       "one conversation → docs/design/celtic-ticket-exchange.md +\n"
       ".excalidraw: detailed specs, architecture (ticket custody, QR\n"
       "re-issue, seat map, identity), testing strategy, diagrams for as\n"
       "many aspects as we can. grounding: standing decisions · what we\n"
       "ruled out · the living design docs of whatever this touches.\n"
       "GO is two keys: everything drawn and nothing left to annotate\n"
       "(you) · every stage-2 measurement has a NAMED ANSWER (machine).\n"
       "GO writes docs/gates/<date>-celtic-ticket-exchange-design.md.",
       artifact="tools: superpowers\nbrainstorming CAPABILITY\n"
                "(2-3 approaches) without its\nwaterfall · excalidraw round\n"
                "trip · A3 story formats.\nhands to HANDOFF — never\nwriting-plans.")
f.down()

# ── 7 — handoff ──────────────────────────────────────────────────────────
f.step("7", "HANDOFF", "Write the contract · Size and assign",
       "the design package arrives INTACT — never a digest. the work\n"
       "order: self-contained pieces ('listing service', 'seat-transfer\n"
       "flow', 'holder-verification screen'), each carrying its own check,\n"
       "sized and assigned AFTER writing. two-tier access: the overseer\n"
       "holds all truth; each builder gets exactly its piece plus related\n"
       "materials. NO human gate — every piece measurable against an\n"
       "upstream declaration, or pushed back to design.",
       artifact="tools: conductor's spec\nmachinery is today's instance.\n"
                "sizing declares tier + effort\n+ why, per piece — the\n"
                "ladder's roles made\ncomputable.")
f.down()

# ── 8 — the loop ─────────────────────────────────────────────────────────
f.step("8", "LOOP", "Drive to done — unattended",
       "next unblocked piece → build → prove against ALL RELEVANT specs →\n"
       "commit as it verifies → repeat. the driver holds nothing: state\n"
       "lives in the declared artifacts, so it cuts and resumes fresh\n"
       "between pieces. every question rides the LADDER — builder →\n"
       "overseer → intent-holder → you — and only a role-unanswerable\n"
       "blocker reaches you. the liveness view ticks at every piece\n"
       "boundary: landed · in flight · remaining. motion, not 'working…'.",
       artifact="tools: /goal + /loop (future),\nconductor + sized players\n"
                "(today). show-where-we-are\npushed at each piece boundary\n"
                "and each stage close.")
deeper("DEEPER — THE LOOP MAY NOT RUN YET. nothing in any repo can refuse\n"
       "from outside the model: 0 CI workflows, 0 hooks. until a check can\n"
       "BLOCK, this page is a description, not a machine. CI is the first\n"
       "build item for exactly this reason — and deciding its shape (what\n"
       "refuses, where, on what signal) is yours.")
f.down()

# ── 9 — acceptance gate ──────────────────────────────────────────────────
f.step("9", "ACCEPTANCE\nGATE", "Prove the whole · Acceptance gate",
       "cold eyes see ONLY the work order and the change — verdict can\n"
       "BLOCK. per-layer conformance, never one verdict: code · logic ·\n"
       "architecture · pixel vs the approved design · the product\n"
       "measurements (an exchange completes end-to-end, the seat\n"
       "transfers, the empty-seat number moves). then the human key.",
       artifact="this is the escalation\ncontract's promised report:\n"
                "GOAL ACHIEVED — the first\nthing you hear since the\ncontract was written.",
       dashed=True)
deeper("DEEPER — YOUR EXPERT-USER PASS, DEFINED. what do you DO to say\n"
       "goal achieved: list a real ticket, transfer it to a real fan,\n"
       "stand at the turnstile when the QR scans? the pass is experiential\n"
       "by design — naming its scenario is the one gate only you can write.")
f.down()

# ── 10 — shipped ─────────────────────────────────────────────────────────
f.step("10", "SHIPPED", "Release shipped → the flow repeats",
       "the gate record is dated and kept; the code IS the product truth;\n"
       "what was ruled out is on the record and read in grounding by the\n"
       "next round — a dead option stays dead. the next slice (away\n"
       "fixtures? cup games? guest passes?) enters at the gates — and\n"
       "enters LOWER, because its upstream declarations now exist.",
       artifact="switch + kivna keep the\nboundary · the vault tells the\n"
                "human story · git holds every\ndeclaration the checks\nmeasure against.")

# ── write ────────────────────────────────────────────────────────────────
out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-04-celtic-example-flow.excalidraw")

_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-04-celtic-example-tony.json")
if os.path.exists(_ann):
    _a = json.load(open(_ann))["elements"]
    for _e in _a:
        _e.setdefault("customData", {})["author"] = "tony"
        _e["index"] = "z" + str(len(f.els)).zfill(4)
        f.els.append(_e)
    print(f"merged {len(_a)} preserved annotation(s)")

_marked, _supp = mark_deltas(f.els, out)
print(f"blue: {_marked} changed since last reviewed"
      if _marked or _supp else "blue: no reviewed snapshot yet")

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
       "elements": f.els,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
       "files": {}}
json.dump(doc, open(out, "w"), indent=1)
print("wrote", out)
print(f"elements: {len(f.els)}")

svg_out = out.replace(".excalidraw", ".svg")
w, h = to_svg(f.els, svg_out)
print("wrote", svg_out, f"({w:.0f}x{h:.0f})")

for label, faults, fmt in (
        ("bound-text overflow", overflow_report(f.els),
         lambda z: f"{z[0][:52]:<52} text {z[1]}px > box {z[2]}px"),
        ("text/box collision", collision_report(f.els),
         lambda z: f"{z[0]:<46} at ({z[1]},{z[2]})"),
        ("text/text overlap", text_overlap_report(f.els),
         lambda z: f"{z[0]:<40} over {z[1]:<40} at ({z[2]},{z[3]})")):
    if faults:
        print(f"!! {len(faults)} {label}(s):")
        for z in faults:
            print("   " + fmt(z))
    else:
        print(f"no {label}s")
