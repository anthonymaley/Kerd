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

  ("Approve what shipped\n(final UI/UX, per release)", "", "GAP",
   "the built thing, running —\nnot a diff, not a green build",
   "seen and approved, or sent back.\nthe release's terminal condition",
   "ACHIEVED: a release was approved on what was seen\nGAP: 'NOT YET EYEBALLED' · 'four builds passed, which\non this project has historically meant very little'"),
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

  ("Design the interface\n(initial)", "", "GAP",
   "product truth + the intent —\nwhat someone needs to do here",
   "what the user sees and does:\nscreens, states, gestures, copy",
   "ACHIEVED: the build had a design to build TO\nGAP: dinner-tonight's came from outside Kerd entirely"),
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
   ("Design the interface (initial)",
    "the build needs something to build TO — dinner-tonight's came from outside"),
   ("Approve what shipped (final UI/UX)",
    "the loop's terminal condition — where it must stop and hand back to you"),
 ]),
 ("SOMEDAY", "#1e1e1e", [
   ("Review unanchored", "real, but it needs the rungs above it first"),
   ("Measurement collection", "nothing counts today; premature until something does"),
   ("Rip what survives the spike", "post-approval only — evidence first"),
 ]),
]
