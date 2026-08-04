# Function map. Working functions are merged; gaps stay separate — the things
# that work do not need decomposing, the things missing do.
#
# Fields: name, today, status, inputs, outputs, evidence
#
# The last column is EVIDENCE, not a metric. Per Tony: "an actual measurement we
# can use to know when we have achieved, or to show the gap." So each row states
# what you could point at to prove the function is working — or to prove it is
# missing. Dashboard numbers were the wrong shape.

FUNCTIONS = [
 ("PRODUCT", [
  ("Frame the intent", "sherpa Explore", "unused",
   "a spark, a problem noticed,\na complaint from someone using it",
   "why this exists + what it must do,\nhigh level, enough to inform design",
   "ACHIEVED: design proceeds without asking\nGAP: intent re-derived from code, per session"),

  ("Test viability", "interrogate /\nsherpa Validate", "unused",
   "the framed intent +\nits killer assumption",
   "fatal risks cleared, or the idea\nreshaped or killed",
   "ACHIEVED: a named risk was qualified with evidence\nand survived  GAP: risks are named but UNQUALIFIED —\nunsized, so they read as managed. (the earlier\n'never named' claim was drafted, not measured)"),

  ("Hold product truth", "CUT 2026-08-03", "cut",
   "shipped changes from build,\nrelease slices",
   "CUT. it failed its own test: asked whether any\nquestion had ever needed answering that the CODE\ncould not answer, the answer was no. a document\nrestating mechanism is a second source that drifts,\nand a drifted doc answers confidently and wrongly.",
   "the 6 Jul doc that held 1 Aug's answer is NOT evidence\nthis was missing — the document EXISTED. it is evidence\nRETRIEVAL failed, and another document cannot fix that.\nRETURN CONDITION: a question the code cannot answer."),

  ("Slice a release ·\nSet the goal", "sherpa Launch", "unused",
   "product truth + intent +\nwhat is already built",
   "MVP / v1 / v1.2 — what is in, what is\ndeferred, and the DONE condition",
   "ACHIEVED: a deferred item stayed deferred\nGAP: no line between MVP and someday exists"),

  ("Choose what matters next", "", "GAP",
   "the open work, ranked by\nconsequence — not by what fits",
   "the next thing to do, and why\nit beats the alternatives",
   "ACHIEVED: the highest-consequence item was picked\nGAP: dinner-tonight ranked by session-fit, not harm"),

 ]),

 ("DESIGN", [
  ("Design the solution", "superpowers\nbrainstorming", "external",
   "stage 1's declarations: the intent\ndocument with its MEASUREMENTS +\nthe qualified risks",
   "ONE PACKAGE from ONE conversation:\ndetailed specs, architecture plans,\ntesting strategy, and diagrams for\nas many aspects as we can",
   "ACHIEVED: the contract never re-derives design\nGAP: 3of3 reached outside Kerd to find this.\nFOLDED IN 2026-08-03: Agree the shape · Decide\nwhat proves it · Design the interface. the four-way\nsplit was Claude's decomposition of the brainstorming\nchecklist, never Tony's shape — his answers describe\none conversation producing one package."),
 ]),

 ("CONTRACT", [
  ("Write the contract ·\nSize and assign", "conductor", "ok",
   "the GO'd design package — full\nupstream truth, arriving intact",
   "the written work order: self-contained\npieces, each carrying its own check,\nsized and assigned AFTER writing",
   "ACHIEVED: a delegated step passed on first return\nWATCH: keep/delegate ratio — 50/50 means tags are early"),
 ]),

 ("BUILD", [
  ("Build a piece · Prove it", "conductor", "ok",
   "one piece of the work order —\nexact spec + related materials",
   "the change + its measurement: checked\nagainst ALL RELEVANT specs and\nmeasurements, tests match acceptance",
   "ACHIEVED: collateral check caught an unintended edit\nGAP: 'my deletion range swallowed three helpers'.\nFOLDED 2026-08-03: 'all relevant' covers the piece's\nown criteria PLUS everything its change touches —\nrelevance scoped by the overseer, who holds all truth"),

  ("Prove the whole · Goal gate", "", "GAP",
   "every piece landed + everything\ndeclared upstream: work order, design\npackage, product measurements",
   "cold review of the whole change (can\nBLOCK) · per-layer conformance — code,\nlogic, architecture, pixel vs design,\nproduct measurements · then the EXPERT-\nUSER pass: Tony uses the output itself",
   "ACHIEVED: shipped EXACTLY what was specified\nGAP: 'NOT YET EYEBALLED' — nothing checks conformance.\nFOLDED IN 2026-08-03: Review unanchored (cold eyes,\nonce per goal + on-demand for risky pieces — flaw\nclass is gaps in the DECLARED TRUTH, which live at\nassembly, not per piece). Refuse bad work became the\nRUNG-WIDE PROPERTY: a check that cannot block from\noutside the model is not a check. 0 CI anywhere."),
 ]),

 ("SESSION", [
  ("Drive to done  (/goal + /loop)", "", "GAP",
   "a cut release with its DONE condition —\nentered through the GATES: work enters\nat the LOWEST rung whose declared inputs\nall exist. SPIKE = the one licensed bypass",
   "next unblocked item → build and prove →\nrepeat, unattended. cut + resume fresh\nbetween pieces; stops only at GOAL\nACHIEVED or a human-level blocker",
   "ACHIEVED: a release reached done without being driven\nby hand  GAP: nothing can refuse from outside the model\nCONSOLIDATED 2026-08-04 (4→1 + property): Open/close ·\nHold state became the RUNG-WIDE PROPERTY — state lives\nin the declared artifacts, never in the session. Route\nto the altitude dissolved into the ENTRY GATES in series.\nKeep context optimal dissolved by construction (exact\nslice per piece + free restarts between pieces)."),
 ]),

 ("SUPPORT", [
  ("Converge · Human knowledge ·\nHuman voice", "tend, kivna, skriv", "ok",
   "the repo, the session, the prose",
   "conventions applied, vault updated,\ntext that does not read as generated",
   "ACHIEVED: vault readable by someone with no context\nWATCH: drift found per tend run"),

  ("Keep artifacts lean", "trim", "dying",
   "completed feature docs,\nstale TODO items",
   "archived — and eventually nothing,\nonce TODO closure holds",
   "ACHIEVED: trim has no job left\nGAP: still needed because TODO closure isn't holding"),
 ]),
]

# Cross-cutting. Not steps in the flow — constraints on how EVERY function
# above behaves. Drawn separately because putting them in the stack would
# imply they happen at a point in time, and they do not.

CROSSCUTTING = [
 ("How we talk to each other", "scattered across 5 places", "GAP",
  "any moment of asking, reporting\nor escalating — at any rung",
  "ONE question, drilled. findings led, never\nstripped. the impact of the answer stated.\ngaps named, not smoothed. no vague X-or-Y,\nno menu built on unchecked assumptions",
  "ACHIEVED: one message resolved the decision\nGAP: 3of3 needed 'too much noise' typed to get a\nsimple view — and shipped a 4-option menu anyway"),

 ("Do we have what we need?\n(entry gate, every rung)", "conductor orient only", "GAP",
  "the declared INPUTS of the function\nabout to start — product → design →\ncontract → build",
  "proceed, or PUSH BACK and name exactly what is\nmissing. never start a rung on assumed inputs.\nRENDERED, not prose: have / need / progress",
  "ACHIEVED: a rung refused to start and said why\nGAP: exists at ONE rung — conductor's pre-flight\ninventory — and nowhere else in the flow"),

 ("Stay in control of\nexternal tools", "", "GAP",
  "an external skill or tool we want\na specific capability from",
  "the capability extracted — and its process,\nquestion style, file conventions and handoff\ntargets explicitly NOT adopted. Kerd's\ncontract wins every conflict.",
  "ACHIEVED: took brainstorming's spec quality without\nits waterfall  GAP: it captured the plan phase and\nrouted to writing-plans — and never came back"),

 ("Show where we are", "", "GAP",
  "every function's declared inputs and outputs,\nwhat is agreed vs drafted, what is built vs not",
  "a rendered board — have / need / progress — for\nONE rung and for the whole thing. invocable at\nany time; produced at every phase-gate close",
  "ACHIEVED: 'where are we' got a render, not a paragraph\nGAP: the requirements agreement about to run has no\ninstrument — a chat thread is doing the job"),

 ("Size work to a model", "conductor, one rung", "GAP",
  "a unit of work, already specified —\nnever sized before it is written",
  "the model tier and the effort it needs, and why.\nnever the top tier for difficulty alone",
  "ACHIEVED: a delegated step passed on first return\nGAP: exists at ONE rung. every other function picks\na model by accident, or does not pick at all"),

 ("What we ruled out, and why", "", "GAP",
  "any option eliminated, at any rung —\nby analysis or by a failed attempt",
  "ONE entry per CONCEPT, never per attempt:\nwhat was tried or considered · why it was\neliminated · the evidence · the RETURN CONDITION.\nNOT the code, NOT the diff, NOT the error output —\nconcepts outlive codebases. filter: was it ever a\nCANDIDATE? a slip is not an option.",
  "ACHIEVED: a dead option was not re-proposed, because\nsomeone read the record first  GAP: four functions\nindependently demand this output and none has a home\nfor it; the same option gets re-argued from scratch"),

 ("Where the work is written down", "scattered", "GAP",
  "any function's declared output",
  "the artifact in ONE home, under a derivable name.\ngit = machine-read, diffable, travels with code.\nvault = human-read, assumes no prior context",
  "ACHIEVED: a session found a prior artifact without asking\nGAP: 3 parallel doc trees. a 6 Jul design doc held\n1 Aug's answer and went unread"),
]

# Interviewed detail. A function appears here ONLY once it has actually been
# walked with Tony. Everything absent is not-yet-interviewed, and the diagram
# says so rather than showing a plausible blank.
#
# Four fields, in execution order — the order came out of Tony asking why
# evidence sat after outputs. It did not: one word was carrying three ideas.
#   in         what arrives, and which route triage sends it down
#   grounding  what MUST be read before producing anything (the entry gate's
#              real job — inputs arrive on their own, grounding gets skipped)
#   out        the artifacts
#   acceptance what proves the output is good. machine key + human key.
# The old ACHIEVED/GAP line was neither: it is a diagnostic of whether the
# function exists yet, and it now lives in movement 11.

DETAIL = {
 "Frame the intent": {
  "in":
   "an idea, a product, a feature, an enhancement, a thought,\n"
   "a question, a comparison to another product or repo — or\n"
   "an issue or a complaint.\n\n"
   "TRIAGED into one of three routes:\n"
   "  NEW      — idea / feature / enhancement\n"
   "  PROBLEM  — issue / complaint / something broken\n"
   "  OUT      — a question about the product. answered from\n"
   "             product truth, NOT framed as new work.\n\n"
   "captured by interview, uploaded evidence, or a whiteboard\n"
   "session. the two routes converge on the same output shape.",
  "grounding":
   "PROBLEM route MUST read the CURRENT situation first —\n"
   "code, infra, product specs — and then do the gap analysis.\n"
   "no proposal before the present state is read.\n\n"
   "NEW route: the competitor scan, and the evidence of need.\n"
   "there may be no current situation to read.\n\n"
   "sensei is a TOOL, not a MUST. invoked when its route\n"
   "matches: asserting a position, proving a gap or an idea\n"
   "with measurement, or a complex problem needing point of\n"
   "cause and 5 whys — triggered by a problem that survived\n"
   "a few attempts to fix it. otherwise avoided.\n"
   "same rule for superpowers and every other external tool:\n"
   "it declares the route it serves, and is invoked on match.",
  "out":
   "TWO documents, not one shape with optional sections.\n"
   "both are a .md — machine-read, long-read, measurable,\n"
   "handoff-ready — AND a diagram. the SECTIONS differ,\n"
   "not the artifact types.\n\n"
   "IDEA BRIEF: what it is · what it must become · what gap\n"
   "it addresses · how it compares to other products · its\n"
   "value · a viability SIGNAL, not a verdict · next inputs.\n\n"
   "PROBLEM STATEMENT: what is happening now, READ from code,\n"
   "infra and specs, not assumed · what should be happening ·\n"
   "the gap between them, MEASURED · point of cause, if the\n"
   "sensei trigger fired · the value of closing it · next inputs.",
  "acceptance":
   "TWO KEYS, neither sufficient alone. the routes converge\n"
   "here: shared machinery, route-specific checklist.\n\n"
   "MACHINE: the sections are present — WHICH sections depends\n"
   "on the route · the measurements are stated · the diagram\n"
   "conforms to the pattern it claims · the next stage's\n"
   "declared inputs are all filled.\n\n"
   "HUMAN: Tony says approve.\n\n"
   "any gap or risk that could not be closed is documented\n"
   "AND confirmed. carried is fine — silent is not.\n\n"
   "HANDOFF: both routes go to Test viability. the killer\n"
   "assumption differs, the test does not — a problem going\n"
   "straight to design is the jump-to-countermeasure failure.",
 },

 "Slice a release · Set the goal": {
  "in":
   "what is already built · the framed and viability-tested\n"
   "candidates · their QUALIFIED risks with countermeasures\n"
   "attached, from Test viability · and the record of what\n"
   "was already ruled out.\n\n"
   "risk arrives PRE-CHEWED. do not re-assess it here: a\n"
   "feature carrying a TEMPORARY countermeasure is a different\n"
   "slicing candidate from one carrying a permanent fix.",
  "grounding":
   "the five things that actually decide a grouping, and they\n"
   "do not all work the same way:\n\n"
   "HARD CONSTRAINT — dependency. forbids groupings outright.\n"
   "  B cannot ship before A if B needs A. no trade-off.\n\n"
   "CEILING — how much change a user can absorb AT ONCE.\n"
   "  a release can be too big even when everything in it is\n"
   "  finished. almost nothing enforces this, which is why\n"
   "  'we shipped everything we had' is a real failure mode.\n"
   "  the bound comes from the RECEIVING side, not capacity.\n\n"
   "TRADE-OFFS — effort, risk, opportunity. these shape the\n"
   "  grouping among what is left, they do not forbid it.",
  "out":
   "THE GROUPING. a release is a GROUPING, not a time axis —\n"
   "time may be attached later, or never. MVP / v1 / v1.2 are\n"
   "ordered, not scheduled. conflating the two turns a\n"
   "grouping decision into a deadline argument.\n\n"
   "THE DONE CONDITION — assembled, never authored. every\n"
   "item is a conformance check against an upstream\n"
   "declaration:\n"
   "  met the feature spec        <- the contract\n"
   "  met the product spec        <- the idea brief\n"
   "  goal of the function met    <- the goal set here\n"
   "  looks EXACTLY like design   <- design, approved pre-build\n"
   "  tests pass                  <- every proof layer declared\n"
   "     by Decide what proves it, INCLUDING user testing\n"
   "  documentation complete      <- DERIVED, not declared:\n"
   "     every declaration covered — feature, product and\n"
   "     problem specs, the changes and fixes implemented,\n"
   "     the solution diagrams, and what we ruled out",
  "acceptance":
   "MACHINE: every item in DONE points at a declaration that\n"
   "EXISTS. nothing in DONE that nothing declared — an\n"
   "unbacked item cannot be checked, so it passes by\n"
   "assertion, which is the unqualified-risk failure again.\n"
   "dependencies are satisfied by the ordering. the slice is\n"
   "within the comprehension ceiling.\n\n"
   "HUMAN: Tony approves the grouping — what is in, what is\n"
   "deferred, and why this cut rather than another.",
 },

 "Choose what matters next": {
  "in":
   "the open work — everything not yet done, from every\n"
   "release grouping. plus, for each item, the VALUE that\n"
   "framing declared for it.",
  "grounding":
   "the failure is NOT bad ranking. it is that the items are\n"
   "not in a form you can weigh. three things missing, and\n"
   "only one of them is about order:\n"
   "  NO DIAGRAM         — rendered, not prose\n"
   "  NO CLEAR STRUCTURE — same shape per item, so they are\n"
   "                       actually comparable\n"
   "  NO CLEAR ASK       — what decision is wanted, per item\n\n"
   "'too much noise' is not volume. a list of prose titles\n"
   "gives you nothing to weigh, however short it is.\n\n"
   "items BLOCKED on a dependency are not candidates at all —\n"
   "a dependency is a hard constraint, so they cannot be\n"
   "'next' at any consequence. draw them apart.",
  "out":
   "candidates on TWO CONSTANT AXES, both about OUTCOME:\n"
   "  CONSEQUENCE — what it costs us NOT to do it\n"
   "  VALUE       — what we gain by doing it. already declared\n"
   "                by Frame the intent and already used by\n"
   "                Test viability. third caller, not a new\n"
   "                measure.\n\n"
   "and, per item, WHAT WE LOSE by not choosing it. v0.68's\n"
   "rule applied to work: name the loss, or it disappears into\n"
   "the good news. a ranked list shows what you picked and\n"
   "never what you gave up.\n\n"
   "EFFORT IS NOT AN AXIS. it is an INPUT measure beside two\n"
   "OUTCOME measures, which makes the grid incoherent, and it\n"
   "systematically flatters cheap work. it survives as a\n"
   "tiebreaker inside a cell, and as one of the five slicing\n"
   "factors at Slice a release.",
  "acceptance":
   "MACHINE: every candidate carries consequence, value and\n"
   "its loss. blocked items are separated, not ranked. the\n"
   "view is RENDERED — prose fails this by construction.\n\n"
   "HUMAN: Tony can weigh them at a glance and say which.\n\n"
   "the test is not 'is the ranking right'. it is 'can he\n"
   "compare them at all'. an item he cannot understand\n"
   "without opening it fails, however well it is ranked.",
 },

 "Test viability": {
  "in":
   "the framed artifact — idea brief or problem statement —\n"
   "its killer assumption, and the viability SIGNAL from\n"
   "framing. never a verdict; testing it is this rung's job.\n\n"
   "what counts as KILLER differs by route:\n"
   "  IDEA     — is the need real, and can we win?\n"
   "  PROBLEM  — is the cause correctly located, and is\n"
   "             closing the gap worth what it costs?",
  "grounding":
   "risks are NOT unnamed — that was a drafted claim and it was\n"
   "wrong. they are unmitigated, unqualified, or accepted\n"
   "unknowns. UNQUALIFIED is the dangerous one: a named,\n"
   "unsized risk reads as managed because it is written down.\n\n"
   "EVIDENCE is what qualifies a risk — a TEST or an ANALYSIS,\n"
   "whichever is cheaper and would actually change the decision.\n"
   "analysis is evidence: not everything needs an experiment.\n\n"
   "two passes, or 'risk-driven' becomes a full risk register:\n"
   "  1. cheap estimate, to triage what could be fatal\n"
   "  2. real evidence for those candidates only",
  "out":
   "QUALIFIED = proven AND measured. three fields, never one:\n"
   "  proven by   — the test or the analysis\n"
   "  impact      — measured, in the units VALUE was stated in\n"
   "  likelihood  — separately. do NOT multiply it by impact:\n"
   "                expected value is the wrong maths for a bet\n"
   "                taken once. 5% of ending it is not 5% damage.\n\n"
   "FATAL = impact >= the value framing declared, at any\n"
   "likelihood. likelihood sets the RESPONSE, not the class.\n\n"
   "A RISK WITHOUT A COUNTERMEASURE IS A BLOCKER. that is the\n"
   "default, so silence STOPS the work rather than passing it.\n"
   "each risk therefore lands in one of three:\n"
   "  COUNTERMEASURE, PERMANENT — root cause addressed\n"
   "  COUNTERMEASURE, TEMPORARY — contained, not cured. carries\n"
   "    the condition that brings it back. an unmarked temporary\n"
   "    countermeasure is a permanent one by neglect.\n"
   "  BLOCKER — no countermeasure. clears ONLY by an explicit\n"
   "    act of acceptance: who, when, and on what basis. an\n"
   "    accepted UNKNOWN is a blocker accepted without even\n"
   "    knowing its size — allowed, but never by default.\n\n"
   "THE LIMIT ON ACCEPTANCE: high impact + high likelihood +\n"
   "no countermeasure = DEAD PROJECT. not a kill you choose,\n"
   "a state you recognise. every other blocker may be accepted\n"
   "by name; this one may not, or acceptance becomes an escape\n"
   "hatch for anything. only RESHAPE or KILL remain.\n\n"
   "verdict: proceed only when NO unaccepted blocker remains.\n"
   "otherwise reshape, or kill. a kill here is a SUCCESS —\n"
   "the cheapest place the thing can die.",
  "acceptance":
   "MACHINE: nothing is merely NAMED. every risk is proven,\n"
   "measured and given a likelihood, or is an explicit accepted\n"
   "unknown. impact and value are in comparable units. every\n"
   "countermeasure states what it is expected to do — it is a\n"
   "hypothesis, so it must be checkable later. every TEMPORARY\n"
   "countermeasure carries its return condition. no blocker is\n"
   "unaccepted.\n\n"
   "HUMAN: Tony accepts each blocker BY NAME — including the\n"
   "unknowns and any low-likelihood fatal. rounding a low\n"
   "probability to zero silently is what this gate stops.\n\n"
   "an UNQUALIFIED risk reaching the next stage is the exact\n"
   "failure this function exists to prevent."
 },

 "Design the solution": {
  "in":
   "stage 1's declarations, arriving together:\n\n"
   "the INTENT DOCUMENT — idea brief or problem statement —\n"
   "with its MEASUREMENTS. those numbers are what the package\n"
   "must answer, and what post-build conformance will measure\n"
   "against.\n\n"
   "the QUALIFIED RISKS with countermeasures attached, from\n"
   "Test viability. a countermeasure is a CONSTRAINT on the\n"
   "shape — design builds around it, not a note in a document\n"
   "nobody opens.",
  "grounding":
   "read BEFORE proposing any approach:\n\n"
   "WHAT WE RULED OUT — so a dead option is not re-pitched.\n\n"
   "THE ACTUAL CODE — not summaries. the 08-02 failure: a\n"
   "stale code comment trusted twice while the design doc\n"
   "holding the answer went unread.\n\n"
   "STANDING DECISIONS — conventions already agreed that a\n"
   "design cannot violate. without them, settled ground gets\n"
   "re-litigated.\n\n"
   "LIVING DESIGN DOCS of whatever the work touches — the\n"
   "exact class whose retrieval failed on 08-02. the code\n"
   "cannot tell you WHY a neighbouring piece has its shape.\n"
   "second caller for reachability.",
  "out":
   "ONE PACKAGE from ONE conversation — not four functions.\n"
   "(the draft split — shape / agree / prove / interface —\n"
   "was Claude's decomposition of the brainstorming checklist,\n"
   "never Tony's shape.)\n\n"
   "detailed specs · architecture plans · testing strategy ·\n"
   "solution diagrams · flow diagrams · visualizations for\n"
   "as many aspects as we can.\n\n"
   "at least TWO approaches with trade-offs before one is\n"
   "chosen — on constant axes, costs marked, bets named,\n"
   "resolved in ONE message.\n\n"
   "LIVES AT docs/design/<slug>.md + .excalidraw — living,\n"
   "undated, same slug as the product doc, so the pair is\n"
   "derivable. (chosen over folder-per-piece-of-work, 08-03.)",
  "acceptance":
   "TWO KEYS, neither sufficient alone:\n\n"
   "HUMAN: every aspect Tony cares about is DRAWN, he has\n"
   "reviewed the drawings, and nothing is left to annotate.\n\n"
   "MACHINE: every measurement stage 1 declared has a NAMED\n"
   "ANSWER in the package — point at where the design delivers\n"
   "it. the MEASURING itself is post-build conformance, not\n"
   "here. nothing declared upstream goes unaddressed.\n\n"
   "GO writes a dated gate record — docs/gates/<date>-<slug>-\n"
   "design.md — and hands to CONTRACT (stage 3), where the\n"
   "score is written. NEVER to writing-plans: the working\n"
   "half of brainstorming exits into the dead half today.",
 },

 "Write the contract · Size and assign": {
  "in":
   "the GO'd design package, arriving INTACT — full specs,\n"
   "documents, diagrams, measurements, plans, UX design,\n"
   "systems. nothing summarized on the way in: the contract\n"
   "is written FROM upstream truth, not from a digest of it.\n\n"
   "the qualified risks ride with it — a countermeasure is a\n"
   "constraint the work order must build around.",
  "grounding":
   "the TERRAIN the work will change — the actual code, read\n"
   "not summarized. the order must name exact paths,\n"
   "signatures and values, and it cannot do that from memory.\n\n"
   "WHAT WE RULED OUT — a contract proposes implementation\n"
   "choices, so it reads the record like everything else\n"
   "that proposes.\n\n"
   "STANDING DECISIONS — the conventions a work order\n"
   "cannot violate.",
  "out":
   "THE WRITTEN WORK ORDER: implementable by a builder who\n"
   "NEVER SAW THE REASONING. every piece carries its exact\n"
   "scope, the why behind any non-obvious choice, and ITS\n"
   "OWN CHECK. sized and assigned AFTER the piece is written\n"
   "— a tag assigned during planning measures how hard the\n"
   "piece felt, not what judgment survived being written down.\n\n"
   "TWO-TIER ACCESS, by role:\n"
   "  the OVERSEER holds all upstream truth.\n"
   "  a BUILDER gets the exact spec for their piece plus\n"
   "  access to related materials — AND NO MORE.",
  "acceptance":
   "MACHINE, and machine ALONE when it holds: every piece is\n"
   "measurable against an upstream declaration — the design\n"
   "package, the measurements, the countermeasures. NO HUMAN\n"
   "GATE at this rung, provided that measuring is real.\n"
   "(Tony, 2026-08-03: 'i dont need to approve contract if\n"
   "we can measure it meets output of other stages.')\n\n"
   "a piece NOTHING upstream declared cannot be measured, so\n"
   "it cannot pass by assertion — it is a PUSH-BACK to\n"
   "design. the DONE-assembled rule applied to the contract.\n\n"
   "ESCALATION CONTRACT: the human hears ONLY of a gap no\n"
   "agent role can answer that is a BLOCKER — the blocker-\n"
   "acceptance path from Test viability. otherwise the next\n"
   "report is GOAL ACHIEVED.",
 },

 "Build a piece · Prove it": {
  "in":
   "one piece of the work order, under the two-tier rule:\n"
   "the exact spec — scope, the why, its own check — plus\n"
   "access to related materials. AND NO MORE.",
  "grounding":
   "the piece's related materials, and nothing else. the\n"
   "builder is not grounded in the whole file — a builder\n"
   "holding everything re-derives intent from it; a builder\n"
   "holding one self-contained piece builds that piece.",
  "out":
   "the change, plus its MEASUREMENT: checked against ALL\n"
   "RELEVANT specs and measurements — the piece's own\n"
   "criteria PLUS everything its change touches. relevance\n"
   "is scoped by the overseer, who holds all truth.\n\n"
   "'relevant' is what covers collateral: damage BESIDE the\n"
   "piece shows up, because the neighbouring terrain is\n"
   "relevant by construction. the measured failure this\n"
   "guards: a deletion range that swallowed three helpers\n"
   "while passing every check written for the piece itself.",
  "acceptance":
   "MACHINE: the measurements pass, and the tests match the\n"
   "acceptance criteria / goal the work order carries.\n"
   "no human key per piece — the human's key is at the goal\n"
   "gate, and the escalation contract holds: a failing piece\n"
   "is the overseer's problem until it is a blocker no agent\n"
   "role can answer.",
 },

 "Prove the whole · Goal gate": {
  "in":
   "every piece landed, plus EVERYTHING declared upstream:\n"
   "the work order, the design package, the product\n"
   "measurements. this gate is where the declarations all\n"
   "come home to be checked.",
  "grounding":
   "COLD, by design: the reviewing eyes see ONLY the work\n"
   "order and the change — no build context, no session\n"
   "memory. the builder's own context is what blinds it;\n"
   "the flaw class this catches is a gap in the DECLARED\n"
   "TRUTH itself ('never contacts your server' — no check\n"
   "could fail, because nothing declared it). those gaps\n"
   "live at assembly, not per piece — which is why cold\n"
   "eyes run once per goal + on demand for risky pieces,\n"
   "never routinely per piece.",
  "out":
   "conformance PER LAYER, never one verdict: code · logic ·\n"
   "architecture · pixel vs the approved design · the\n"
   "product measurements from stage 1.\n\n"
   "and the verdicts can BLOCK. the rung-wide property:\n"
   "every gate here refuses from OUTSIDE the model —\n"
   "advisory output is not a check. (today: 0 CI workflows,\n"
   "0 pre-commit hooks, every repo. every gate in the\n"
   "system is a model choosing to comply.)",
  "acceptance":
   "MACHINE: every declared layer conforms, per layer.\n\n"
   "HUMAN — the EXPERT-USER pass: Tony uses the output\n"
   "itself. the app feature, the performance, the document,\n"
   "the diagram — whatever the output finally is, checked\n"
   "as the expert user, not as a reader of reports.\n"
   "(Tony, 2026-08-03: 'im checking it as the expert user.')\n\n"
   "this is GOAL ACHIEVED — the report the escalation\n"
   "contract promised. the human re-enters here, and\n"
   "nowhere earlier short of an unanswerable blocker.",
 },

 "Drive to done  (/goal + /loop)": {
  "in":
   "a cut release with its DONE condition — every piece\n"
   "carrying its own check, measurements declared, risks\n"
   "qualified. entered through the GATES: work enters at\n"
   "the LOWEST rung whose declared inputs all exist;\n"
   "missing inputs push work UP, never through.\n\n"
   "the one licensed bypass is a SPIKE — declared up\n"
   "front, cheap, built for a kill-or-keep decision.\n"
   "'just build it' is the anti-pattern for MVP work; a\n"
   "spike that wants to become real re-enters via the gates.",
  "grounding":
   "the work order and the declared artifacts — nothing\n"
   "else exists to read, because the RUNG-WIDE PROPERTY\n"
   "holds: state lives in the declared artifacts, never in\n"
   "the session. anything worth keeping is written the\n"
   "moment it exists. a session may die at any instant —\n"
   "the loss is bounded to the in-flight piece, redone\n"
   "from its spec. sessions end BETWEEN pieces: the cut\n"
   "is chosen, not suffered.",
  "out":
   "next unblocked item → build and prove → repeat,\n"
   "unattended. each piece runs BUILD's machinery on\n"
   "exactly its slice (two-tier access) and commits as it\n"
   "verifies. the driver holds nothing, so it cuts and\n"
   "resumes fresh between pieces whenever conditions\n"
   "degrade — cutting costs nothing; cut liberally, even\n"
   "per piece. (no degradation detector needed: the\n"
   "missing signal dissolved rather than found.)",
  "acceptance":
   "MACHINE: the loop stops at exactly two points — GOAL\n"
   "ACHIEVED (hands to Prove the whole · Goal gate), or a\n"
   "HUMAN-LEVEL blocker once the role ladder is exhausted:\n"
   "every question answered at the lowest role with the\n"
   "knowledge AND the authority, escalated only on genuine\n"
   "inability. while an answer waits on the human, nothing\n"
   "is built the answer could invalidate — park vs stop is\n"
   "the driving role's call.\n\n"
   "PRECONDITION: MUST NOT run at all where nothing can\n"
   "refuse (today: 0 CI, 0 hooks, every repo).",
 },
}


# Movement 7 — what gets built, and in what order.
# Tony's call, with the spike added: the routing bet is untested, so it gets
# tested rather than decided.
SEQUENCE = [
 ("MVP", "#e03131", [
   ("Route to the altitude",
    "the keystone — three gaps stay unreachable without it"),
   ("Agree the shape — now in Design the solution",
    "sensei A3 story format, drawn in the whiteboard grammar"),
   ("Refuse bad work (CI) — now the BUILD-wide property",
    "the only item that changes what is POSSIBLE, not just likely"),
 ]),
 ("SPIKE — not a decision", "#e03131", [
   ("Route ONE dead skill, cheaply",
    "the routing bet is untested. wire one, watch whether it gets used."),
   ("Kill or keep on evidence",
    "beats route-vs-rip as a binary — neither side has evidence yet"),
 ]),
 ("v1", "#1e1e1e", [
   ("Hold product truth + its read path",
    "the artifact is worthless without retrieval — measured, not feared"),
   ("Decide what proves it — now in Design the solution",
    "test bias by layer; contract tests where client meets server"),
   ("Choose what matters next",
    "rank by consequence — the vacuum conductor filled with session-fit"),
   ("Drive to done  (/goal + /loop)",
    "REQUIRES CI FIRST — a loop with nothing able to refuse compounds errors"),
   ("Design the interface — now in Design the solution",
    "PRE-LOOP. approved design is what the loop builds to; nothing starts without it"),
   ("Verify against what we said — in Prove the whole",
    "the loop's hand-back. machine: code/logic/arch/pixel. human: expert-user pass"),
 ]),
 ("SOMEDAY", "#1e1e1e", [
   ("Review unanchored — now in Prove the whole", "real, but it needs the rungs above it first"),
   ("Measurement collection", "nothing counts today; premature until something does"),
   ("Rip what survives the spike", "post-approval only — evidence first"),
 ]),
]

# First-cut requirements. Deliberately shallow — one MUST per function, enough
# to expose relationships between them, not enough to be a spec. Draft for
# Tony to correct; anything marked (?) is me guessing rather than reading.
REQUIREMENTS = [
 ("PRODUCT", [
  ("Frame the intent",
   "MUST state why this exists in terms checkable by someone outside the build,\nand be reachable by the design rung without asking a question"),
  ("Test viability",
   "MUST qualify every candidate-fatal risk with EVIDENCE — a test or an\nanalysis — and record impact and likelihood SEPARATELY, never multiplied.\n"
   "FATAL = impact >= the value framing declared, at any likelihood.\n"
   "MUST leave every risk in one state: countermeasure (permanent or\nTEMPORARY, carrying its return condition), accepted, accepted unknown\n"
   "(by whom, when, why not gathered), or fatal.\nMUST NOT let an UNQUALIFIED risk reach the next stage — a named, unsized\n"
   "risk reads as managed, which is the failure mode this exists to stop."),
  ("Hold product truth  — CUT 2026-08-03",
   "CUT. the code is the truth for mechanism and sequencing; a parallel\ndocument is a second source that drifts. the one measured failure behind\n"
   "this function was RETRIEVAL, not absence — the document existed.\nwhat survives goes elsewhere: retrieval is the 'reachable' clause of\n"
   "Where the work is written down; intent and value are already produced\nby Frame the intent.\n"
   "RETURN CONDITION: a question arises that the code cannot answer."),
  ("Slice a release · Set the goal",
   "a release is a GROUPING, not a time axis — time may be attached later, or\nnever. ordering and scheduling are separable.\n"
   "MUST respect dependencies as HARD constraints, and MUST cap the slice at\nwhat a user can absorb at once — a release can be too big even when\n"
   "everything in it is finished.\nMUST consume the qualified risks from Test viability rather than\nre-assessing them.\n"
   "The DONE condition MUST be ASSEMBLED from upstream declarations, never\nauthored at the end: every item is a conformance check against something\n"
   "already declared. MUST NOT contain an item nothing declared — it cannot\nbe checked, so it passes by assertion."),
  ("Choose what matters next",
   "MUST present candidates on two constant axes, both about OUTCOME:\nCONSEQUENCE (what it costs us not to do it) and VALUE (what we gain).\n"
   "MUST NOT use EFFORT as an axis — an input measure beside outcome measures\nmakes the grid incoherent and flatters cheap work.\n"
   "MUST name, per item, WHAT WE LOSE by not choosing it — a ranked list shows\nwhat you picked and never what you gave up.\n"
   "MUST be RENDERED, with the same structure per item and a clear ask. the\nfailure is not bad ranking, it is items that cannot be weighed: no diagram,\n"
   "no structure, no ask.\nMUST separate items BLOCKED on a dependency — they are not candidates at\n"
   "any consequence.\nMUST NOT rank by what fits the session about to run."),
 ]),
 ("DESIGN", [
  ("Design the solution",
   "MUST produce ONE package: detailed specs, architecture plans, testing\nstrategy — and diagrams for as many aspects as we can. agreed in\ndiagrams, not prose.\n"
   "MUST propose at least two approaches with trade-offs before one is\nchosen — options on constant axes, costs marked, bets named, resolved\nin ONE message, not a sequence of clarifications.\n"
   "MUST be approved before any build starts, on TWO KEYS: every aspect\ndrawn and nothing left to annotate · every stage-1 measurement has a\nNAMED ANSWER in the package. the measuring itself is post-build.\n"
   "MUST live at docs/design/<slug> — living, undated, same slug as the\nproduct doc. GO writes a dated gate record and hands to CONTRACT,\nnever to a plan-writing skill.\n"
   "MUST state test bias per layer, and name every seam needing a\ncontract test.\n"
   "(?) MUST output interface values a machine can check — tokens, hex,\nspacing, states"),
 ]),
 ("CONTRACT", [
  ("Write the contract · Size and assign",
   "MUST be implementable by a builder that never saw the reasoning;\nevery piece carries its own check.\n"
   "MUST tier access: the overseer holds ALL upstream truth; a builder\ngets the exact spec for their piece plus related materials, NO MORE.\n"
   "MUST size and assign AFTER the piece is written, never before.\n"
   "MUST NOT need human approval — provided every piece is measurable\nagainst an upstream declaration. an unmeasurable piece cannot ride\n"
   "through on assertion: it is a push-back to design.\n"
   "MUST escalate to the human only a BLOCKER no agent role can answer;\notherwise the next report is goal achieved."),
 ]),
 ("BUILD", [
  ("Build a piece · Prove it",
   "MUST measure each piece against ALL RELEVANT specs and measurements —\nits own criteria plus everything its change touches, relevance scoped\n"
   "by the overseer — and tests MUST match the acceptance criteria / goal.\ncollateral is covered by 'relevant': damage beside the piece shows up."),
  ("Prove the whole · Goal gate",
   "MUST run cold eyes over the whole change before 'goal achieved' is\ndeclared — seeing ONLY the work order and the change, no build context;\n"
   "verdict CAN BLOCK. also on-demand for risky pieces. the flaw class is\ngaps in the DECLARED TRUTH, which live at assembly, not per piece.\n"
   "MUST check every declared layer — code, logic, architecture, pixel vs\nthe approved design, product measurements — conformance per layer,\n"
   "never one verdict.\n"
   "MUST end with the EXPERT-USER pass: the human uses the output itself —\napp feature, performance, document, diagram, whatever it finally is.\n"
   "RUNG-WIDE PROPERTY: every gate here MUST block from outside the model.\nadvisory output is not a check. (today: 0 CI, 0 hooks, every repo)"),
 ]),
 ("SESSION", [
  ("Open / close · Keep tempo · Hold state\n— became the RUNG-WIDE PROPERTY 2026-08-04",
   "state lives in the DECLARED ARTIFACTS, never in the session. anything\nworth keeping is written the moment it exists. a session may die at any\ninstant — the loss is bounded to the in-flight piece, redone from its\nspec. sessions end BETWEEN pieces: the cut is chosen, not suffered.\ntoday's close-out-deferred capture is the loss window this forbids."),
  ("Route to the altitude\n— dissolved into the ENTRY GATES 2026-08-04",
   "work enters at the LOWEST rung whose declared inputs all exist; missing\ninputs push work UP, never through — the gates in series ARE the routing.\nnothing passes a gate on assertion. the one licensed bypass is a SPIKE:\ndeclared up front, cheap, built for a kill-or-keep decision. 'just build\nit' is the anti-pattern for MVP work; a spike that wants to become real\nre-enters via the gates."),
  ("Drive to done  (/goal + /loop)",
   "MUST stop at exactly two points: GOAL ACHIEVED, or a HUMAN-LEVEL\nblocker once the role ladder is exhausted — every question answered at\nthe lowest role with the knowledge AND the authority; the human hears\nonly what no agent role can decide.\nMUST NOT build anything a pending human answer could invalidate.\nMUST NOT run at all where nothing can refuse."),
  ("Keep context optimal (inside the loop)\n— dissolved by construction 2026-08-04",
   "each piece runs on exactly its slice (two-tier access); the driver\nrestarts between pieces at zero cost (the property). when cutting costs\nnothing, no degradation detector is needed — cut liberally, even per\npiece. the missing quality signal dissolved rather than found."),
 ]),
 ("CROSS-CUTTING", [
  ("How we talk to each other",
   "MUST be one question, drilled, carrying the findings it depends on.\n(?) MUST be agreed in diagrams, not prose — constant axes, colour marking\ncost only, bets named and discharged by name, containment over arrows,\nan altitude shift between movements.\n(?) MUST round-trip: the diagram goes out, annotations come back as\ninput, preserved across regeneration.\n(?) MUST pick a story format before drawing — proposal / compare-contrast\n(current → new → what changes) / roadmap / illumination.\n(?) needs an enforcement point — five written statements did not bind"),
  ("Do we have what we need? (entry gate)",
   "MUST check the declared inputs of the rung about to start, and MUST push\nback naming what is missing rather than proceeding on assumption.\nMUST call 'Show where we are' rather than render a view of its own"),
  ("Show where we are",
   "MUST be invocable at any time, and MUST be produced at every phase-gate\nclose. MUST render have / need / progress for ONE rung AND for the whole\nboard. Never prose.\n(?) the gate-close copy is the artifact of record for that gate — dated,\nkept, diffable against the next one"),
  ("Size work to a model",
   "(?) every function that dispatches work MUST declare the model tier and\nthe effort it needs, and why. sized AFTER the work is specified, never\nbefore. MUST NOT default to the top tier for difficulty alone"),
  ("Where the work is written down",
   "every function's output MUST have exactly one home, and its name MUST be\nderivable without looking it up — know the subject, know the filename.\n"
   "MUST date records of EVENTS, and MUST NOT date living documents.\nthe test: would rewriting this tomorrow be CORRECT, or would it be\n"
   "FALSIFYING the record? correct -> living, no date, git history is the\narchive. falsifying -> a record, dated, never rewritten again.\n"
   "MUST state the git/vault split — git: machine-read, diffable, travels\nwith code. vault: human-read, assumes no prior context. never both.\n"
   "MUST carry route and stage in front matter, so that route-specific\nacceptance is machine-checkable rather than a human reading for it.\n"
   "(?) MUST be reachable — an artifact nothing routes to is lost, not\nstored. naming solves findability, NOT reachability. still open: the\n"
   "6 Jul design doc that held 1 Aug's answer was perfectly well named."),
  ("What we ruled out, and why",
   "MUST be its OWN artifact, reviewable in one pass — inside each solution doc,\n'what have we already ruled out?' cannot be answered without reading all\n"
   "of them.\nMUST record the CONCEPT, not the code: what was tried or considered, why\nit was eliminated, the evidence (a test OR an analysis — the same thing,\n"
   "differing in cost), and the condition that would bring it back.\nMUST be read in GROUNDING by every function that proposes anything. that\n"
   "is what stops a dead option being re-proposed, and it is why this is not\na graveyard but an input.\n"
   "MUST be captured as a BYPRODUCT of work already happening — a failed\nverify IS the record. an artifact needing discipline to maintain goes\n"
   "stale, and a stale 'already tried' list is worse than none.\nMUST NOT record slips. the filter is: was it ever a candidate?"),
  ("Stay in control of external tools",
   "MUST name what is NOT being adopted before the tool is invoked"),
 ]),
]

# Tooling catalogue. For each tool we actually use: who calls it, what that
# caller requires, and whether it is met. The point is improve-or-replace —
# a tool can be excellent for one caller and wrong for another.
TOOLING = [
 ("switch", "you, crossing a boundary",
  "survive going cold — full context restored, nothing re-derived",
  "MEETS. 20x/day, the one thing that holds"),
 ("switch", "the LOOP, keeping context healthy",
  "cut on BOTH: (1) token headroom — measurable, cheap.\n(2) quality degrading or drifting from intent — bites\nharder, and has no signal at all today",
  "UNKNOWN. 'low' exists but was built for\ntoken budget, not context hygiene. (2) has\nno signal — nearest seed is v0.68's\n'say how you caught your own mistake'"),
 ("conductor", "you, working one session",
  "orient, plan, execute with evidence, hold scope",
  "MEETS, at the contract rung and below"),
 ("conductor", "the LOOP, running one item",
  "take an item, build it, verify, commit — without re-planning\nor re-asking what it is",
  "UNKNOWN. every session starts from orient\nand a plan gate. a loop step should not."),
 ("kivna", "you, reading later",
  "vault readable by someone with no prior context",
  "MEETS. write-only from the flow"),
 ("tend", "you, setting up or fixing drift",
  "converge a repo to current conventions, change nothing silently",
  "MEETS. never commits, by design"),
 ("trim", "you, when artifacts pile up",
  "archive what is done",
  "DYING. exists because of two other\nproblems, not its own"),
 ("skriv", "you, writing prose",
  "text that does not read as generated",
  "MEETS. used near-daily"),
 ("pair", "you, wanting rapid back-and-forth",
  "reasoning kept internal, one speech-bubble question, interrupt early",
  "MEETS via hook. one-time toggle, not invoked per session"),
 ("superpowers\nbrainstorming", "the design rung",
  "approaches, architecture, boundaries — WITHOUT its waterfall,\nits menus, its worktree assumption or its handoff target",
  "PARTIAL. gives the capability, then\ncaptures the plan phase and routes to\nwriting-plans. never returns."),
 ("sensei story", "agreeing a shape",
  "A3 narrative structure — proposal, compare/contrast, roadmap",
  "PROVEN, ELSEWHERE. extensively used in\n~/toyota-sensei and other projects.\n"
  "never run inside Kerd — so the bet is\nTRANSFER, not the method."),
 ("/loop", "driving to done",
  "run until the goal is met or the hand-back point is reached",
  "UNTESTED. MUST NOT run where\nnothing can refuse"),
 ("excalidraw\n+ clipboard", "agreeing a shape, both directions",
  "diagram out, annotations back in as input, preserved across\nregeneration — no install, no lock-in",
  "MEETS. proven both ways in one round\ntrip. caveat: one-directional on the file\n— regenerating overwrites hand edits"),
 ("diagram generator\n(tools/diagram)", "showing where we are",
  "render have / need / progress, for one rung and for the whole\nboard, on demand and at every gate close",
  "PARTIAL. renders the map and the\nrequirements; renders no progress state\nand nothing invokes it"),
]
