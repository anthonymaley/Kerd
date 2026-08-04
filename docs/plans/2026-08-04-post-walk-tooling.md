# Post-walk tooling decisions

The post-walk phase: how the skills must change to support the agreed
requirements. Opened on the nine questions from the Celtic worked-example
review (`annotations/log.md`, 2026-08-04). Standing rule: decisions here,
rips only after the design is approved.

## 1. Sensei — the grammar leaves the tool; the tool keeps its depth (AGREED 2026-08-04)

Grounding read: `Sensei Input/story layout visuals` (nine A3 layouts, each
carrying its own "this outline is used when…" — route declarations already),
`Sensei Input/example diagrams` (Tony's real papers; the 2013 API Gateway
proposal is the reference exemplar: current drawn · ideal drawn · numbered
pains · target · scored evaluation on constant axes · costs · roadmap, ONE
page), and `~/toyota-sensei/skills/story/SKILL.md` (7 types, two-column A3
HTML built progressively, coaching/LLM modes, compression discipline).

**Three tiers, split by weight:**

1. **Everyday visuals — the layout library.** The nine story layouts are
   extracted as the system-wide talk-format library, owned by *How we talk*
   (function 19). Any function that asks or reports picks the layout by its
   used-when trigger and draws it on the whiteboard, in the moment, no skill
   invocation. Mappings already visible: Proposal ↔ idea brief · Compare &
   Contrast ↔ now/new/what-it-means · Correcting Discrepancy from Standard ↔
   conformance-failure report (current vs the DECLARATION → discrepancy →
   countermeasure) · Roadmap ↔ slicing · Known→Unknown, Simple→Detail ↔ the
   altitude rules for educating the human.
2. **Large stories — `/sensei:story`.** Full A3 in real detail. Boundary
   test: WHO READS IT, AND WHEN — a visual for Tony-in-this-conversation is
   everyday; a document an audience reads cold, or a record that persists,
   earns the full build.
3. **Problems — `/sensei:work`.** Unchanged from the walk: point of cause,
   5 whys, invoked on the declared route (position to assert · gap to prove
   with measurement · problem that survived a few attempts).

**Reference exemplar:** the API Gateway paper is the bar for any one-page
decision document the system produces (idea brief, design GO, proposal).

What we lose: nothing measured — sensei stays whole; the layouts stop being
exclusively its.

## 2. Superpowers — build our own, and the evaluation matrix is the comparison standard (AGREED 2026-08-04)

**Build, not extract.** The one capability that earned its keep (2-3
independent approaches) gets built as Kerd's own, specified by the walk's
DESIGN requirement: from the framed intent + qualified risks, generate
genuinely independent approaches, drawn as Compare-and-Contrast layouts,
scored on constant axes. One-time mining of brainstorming's probing
questions, then the tie is cut. Superpowers stays installed but UN-ROUTED
while the replacement proves; removal is a later evidence decision.

**The Technical Evaluation Matrix is THE WAY options are compared** (Tony:
"THIS IS THE WAY TO DO IT") — copied out of xls (`FSS DB Technical
Evaluation.xls`) into our grammar. The format:

- **Options as rows**, each with its ID, description, and an ARCHITECTURE
  OVERVIEW drawn per option.
- **Criteria as columns, grouped** (e.g. hosting environment · quality:
  strategy/performance/support/engineering/scaling · due date · cost), each
  carrying: **Target or Minimum Score** (the declared bar — measured against
  a declaration, never assertion) · **Category M/D** (mandatory/desirable —
  the fatal split) · **Weighting Factor**.
- **Verdict per option per criterion, the Toyota marks** (the xls letters
  were stand-ins): **○ circle** = good — meets the requirement, no
  countermeasure needed · **△ triangle** = meets the requirement but only
  WITH a countermeasure · **× cross** = cannot meet it and no countermeasure
  is available — the walk's risk vocabulary exactly ("a risk without a
  countermeasure is a BLOCKER"; a × on a mandatory criterion kills the
  option, and every △ carries its countermeasure with a confidence
  statement).
- **OVERALL + RANK**, then sections: Proposal + next steps · Risks or
  Countermeasures Required · Countermeasures per option, each with a
  CONFIDENCE statement.

Home: the design function's evaluation instrument, fed by Test viability's
qualified risks; renders via the diagram toolkit (movement-9-style table),
never a spreadsheet.

## 3. Interrogate — modify into the risk ledger, tiered (AGREED 2026-08-04)

Keep the exhaustive-interview engine; replace the output with a RISK LEDGER
in the walk's states: risks as rows — impact in the value's units ·
likelihood (separate, never multiplied) · evidence (test OR analysis) ·
state (countermeasure permanent/TEMPORARY-with-return-condition / accepted /
accepted unknown: by whom, when, why not gathered / FATAL) · countermeasure
confidence. Killer assumption first; the SPIKE is its cheapest test; output
hands to slicing PRE-CHEWED, never re-assessed. The co-sign becomes the
viability gate record. TIERED like sensei: everyday = the ledger filled
inside the framing conversation; large bets = the full interrogate session.

## 4. Sherpa — CUT, dissolved into the ladder (AGREED 2026-08-04)

The walk built what sherpa was going to be. Its five stages map one-to-one
onto the rungs; graduation = a gate passing; jump-back = the gate's
push-back; "what stage am I at" = Show where we are reading the declared
artifacts; park = a work order with no active goal. Its stage specs were
explicitly skeletons (Phase 2 never happened), and its expedition log
(kivna/sherpa.md) is now a SECOND SOURCE that drifts — the Hold-product-
truth argument. The SPIKE also loses its original purpose: it tested
whether routing revives a dead skill, and routing-to-skills died with
function 16 — skills are instruments of functions, not destinations.
**RETURN CONDITION:** a lifecycle need arises that the gates + the view
cannot answer (nearest candidate: a portfolio view across many ideas).

## 5. Ratifications (AGREED 2026-08-04)

- **Top tier at FRAME**: the sizing rule gains one clause — the intent
  interview is the single place the top tier is the DEFAULT; a wrong word
  there poisons every downstream declaration.
- **Progress renderer**: Show where we are gets its instrument by growing
  the diagram toolkit — progress state (landed · in flight · remaining)
  beside the map it already renders. MVP-sequence build item, not a skill.
- **Documentation**: derived, never a standing skill — docs are pieces
  carrying their own checks.
- **Domain tools** (Swift, Apple UI, …): enter per the tool rule — declared
  route, bounded contract, killable. A needed-tools inventory runs when a
  real project enters the gates, not speculatively.

## 6. Conductor — the driving role; the protocol is a seedbed (AGREED 2026-08-04)

Conductor's protocol pieces are FIRST INSTANCES of the system's functions,
incubated in one skill because the system didn't exist yet: pre-flight
inventory = the only entry-gate instance · spec machinery = CONTRACT's
instance · verification gate + work commits = Build a piece · Prove it ·
3-fix + hand-back = the role ladder · model advisory = Size work to a
model. **The pieces graduate out** into the functions as each instrument
lands (gates, matrix, ledger, renderer). **What remains conductor is the
DRIVING ROLE**: dispatch, judging returned evidence, park-vs-stop, deciding
which tools are needed, kill authority — rung two of the ladder, under the
intent-holding role, under Tony. One role, two tempos: INTERACTIVE today
(unchanged — it works, ran twice), UNATTENDED as the loop's driver, switched
on only when the refusal property has a real instance. Transition rule:
no-rip — conductor sheds a piece only as its replacement proves.
