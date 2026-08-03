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
   "ACHIEVED: a named risk was tested and survived\nGAP: risks carried forward, never named"),

  ("Hold product truth", "", "GAP",
   "shipped changes from build,\nrelease slices",
   "living, user-side: what the\nproduct does today",
   "ACHIEVED: doc matches the running app\nGAP: 6 Jul design doc held 1 Aug's answer, unread"),

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
  ("Shape the solution", "superpowers\nbrainstorming", "external",
   "intent, constraints, and the real\nterrain — actual code, not summaries",
   "approaches with trade-offs,\nchosen architecture, boundaries",
   "ACHIEVED: the contract never re-derives design\nGAP: 3of3 reached outside Kerd to find this"),

  ("Agree the shape", "", "GAP",
   "options on constant axes,\ncosts marked, bets named",
   "an approved shape — a sensei A3\nstory, drawn, with bets discharged",
   "ACHIEVED: one message resolved the decision\nGAP: 3 rounds produced no decision (dinner-tonight)"),

  ("Decide what proves it", "", "GAP",
   "the chosen shape + where the\nrisk actually sits",
   "test strategy: heavy on business logic,\nbehaviour-level on UI, contract at seams",
   "ACHIEVED: a contract test caught a breaking change\nGAP: movie-catalog-client-contract.md enforces nothing"),

  ("Design the interface\ninitial → final → APPROVED", "", "GAP",
   "product truth + the intent —\nwhat someone needs to do here",
   "what the user sees and does: screens,\nstates, gestures, copy. Approved BEFORE\nany build starts — this gates the loop",
   "ACHIEVED: the build had an approved design to\nbuild TO  GAP: dinner-tonight's came from a Claude\ndesign spec produced entirely outside Kerd"),
 ]),

 ("CONTRACT", [
  ("Write the contract ·\nSize and assign", "conductor", "ok",
   "the approved shape + terrain\nfetched for the orchestrator",
   "spec file: per-step tags, sized\nmodel + effort, verify commands",
   "ACHIEVED: a delegated step passed on first return\nWATCH: keep/delegate ratio — 50/50 means tags are early"),
 ]),

 ("BUILD", [
  ("Execute a unit ·\nProve it worked", "conductor", "ok",
   "one spec slice — scope, files,\nsignatures, the why, verify",
   "the change + evidence: command\noutput, diff, collateral checked",
   "ACHIEVED: collateral check caught an unintended edit\nGAP: 'my deletion range swallowed three helpers'"),

  ("Review unanchored", "", "GAP",
   "the spec and the diff — nothing\nelse. no session context",
   "what is missing, what does not\nmatch what was agreed",
   "ACHIEVED: it finds what the in-loop review missed\nGAP: 'never contacts your server' needed Tony to push"),

  ("Refuse bad work", "", "GAP",
   "the commit or the branch",
   "pass, or blocked — outside the\nmodel, not a choice to comply",
   "ACHIEVED: a bad change was blocked, not discussed\nGAP: 0 CI workflows, 0 pre-commit hooks, every repo"),

  ("Verify against what we said\n(half machine, half human)", "", "GAP",
   "the running thing + EVERYTHING declared\nupstream: product measurements, the\napproved design, architecture, the contract",
   "conformance per layer — code, logic,\narchitecture, PIXEL-PERFECT UI vs design,\nthen: did we meet the product measurements",
   "ACHIEVED: shipped EXACTLY what was specified, proven\nagainst the measurements set at the start\nGAP: 'NOT YET EYEBALLED' — nothing checks conformance"),
 ]),

 ("SESSION", [
  ("Open / close · Keep tempo ·\nHold state", "switch, conductor", "ok",
   "repo state + the last session's\nhandoff",
   "restored context, work committed as\nit verifies, a cold-readable handoff",
   "ACHIEVED: next session picked up cold, no re-derivation\nWATCH: switch runs 20x/day — the one thing that holds"),

  ("Route to the altitude", "", "GAP",
   "the request, before any work\nis sized",
   "which rung to enter at, and\nwhich function runs first",
   "ACHIEVED: a session started at the right rung\nGAP: sherpa is an orphan; nothing references it"),

  ("Drive to done  (/goal + /loop)", "", "GAP",
   "a cut release with its DONE condition,\nplans, tests — everything in place",
   "next unblocked item → run → check goal →\nrepeat. AND when to cut a session and\nstart fresh to keep conditions good",
   "ACHIEVED: a release reached done without being\ndriven by hand  GAP: nothing detects a degraded\nsession; conductor says restart, nothing says when"),
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
}


# Movement 7 — what gets built, and in what order.
# Tony's call, with the spike added: the routing bet is untested, so it gets
# tested rather than decided.
SEQUENCE = [
 ("MVP", "#e03131", [
   ("Route to the altitude",
    "the keystone — three gaps stay unreachable without it"),
   ("Agree the shape",
    "sensei A3 story format, drawn in the whiteboard grammar"),
   ("Refuse bad work (CI)",
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
   ("Decide what proves it",
    "test bias by layer; contract tests where client meets server"),
   ("Choose what matters next",
    "rank by consequence — the vacuum conductor filled with session-fit"),
   ("Drive to done  (/goal + /loop)",
    "REQUIRES CI FIRST — a loop with nothing able to refuse compounds errors"),
   ("Design the interface → approved",
    "PRE-LOOP. approved design is what the loop builds to; nothing starts without it"),
   ("Verify against what we said",
    "the loop's hand-back. machine: code/logic/arch/pixel. human: product intent"),
 ]),
 ("SOMEDAY", "#1e1e1e", [
   ("Review unanchored", "real, but it needs the rungs above it first"),
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
   "MUST name the assumption that kills it, and record which risks were tested\nversus carried forward — carried is fine, silent is not"),
  ("Hold product truth",
   "MUST be diffable against the running app, and MUST be read when work\ntouches its area. Unread means it does not exist."),
  ("Slice a release · Set the goal",
   "MUST state a DONE condition specific enough to terminate a loop"),
  ("Choose what matters next",
   "MUST rank by consequence and show the reasoning.\nMUST NOT rank by what fits the session about to run."),
 ]),
 ("DESIGN", [
  ("Shape the solution",
   "MUST produce at least two approaches with trade-offs before one is chosen"),
  ("Agree the shape",
   "MUST present options on constant axes, costs marked, bets named —\nand resolve in ONE message, not a sequence of clarifications"),
  ("Decide what proves it",
   "MUST state test bias per layer, and name every seam needing a contract test"),
  ("Design the interface → approved",
   "MUST be approved before any build starts.\n(?) MUST output values a machine can check — tokens, hex, spacing, states"),
 ]),
 ("CONTRACT", [
  ("Write the contract · Size and assign",
   "MUST be implementable by a model that never saw the reasoning.\nTags assigned AFTER the step body is written, never before."),
 ]),
 ("BUILD", [
  ("Execute a unit · Prove it worked",
   "MUST produce evidence, and MUST check collateral — what changed that\nshould not have, not just whether the intended change landed"),
  ("Review unanchored",
   "MUST see only the spec and the diff. No session context, ever."),
  ("Refuse bad work",
   "MUST be able to block, from outside the model.\nAdvisory output does not satisfy this."),
  ("Verify against what we said",
   "MUST check every declared layer — code, logic, architecture, pixel, product\nmeasurements — and report conformance per layer, not one verdict"),
 ]),
 ("SESSION", [
  ("Open / close · Keep tempo · Hold state",
   "MUST survive going cold — the next session picks up without re-deriving"),
  ("Route to the altitude",
   "MUST decide before the work is sized, not after"),
  ("Drive to done  (/goal + /loop)",
   "MUST stop at the stated hand-back point.\nMUST NOT run at all where nothing can refuse."),
  ("Keep context optimal (inside the loop)",
   "MUST cut on token headroom AND on quality degrading or drifting from\nintent. (?) the second has no signal — self-correction rate is the\nnearest proxy we have, and it was added for another reason"),
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
