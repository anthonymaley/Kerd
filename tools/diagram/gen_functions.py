# Function map. Working functions are merged; gaps stay separate — the things
# that work do not need decomposing, the things missing do.
# Fields: name, today, status, inputs, outputs, measurement

FUNCTIONS = [
 ("PRODUCT", [
  ("Frame the intent", "sherpa Explore", "unused",
   "a spark, a problem noticed,\na complaint from someone using it",
   "why this exists + what it must do,\nhigh level, enough to inform design",
   "can design proceed without guessing?\nintent questions asked later"),

  ("Test viability", "interrogate /\nsherpa Validate", "unused",
   "the framed intent +\nits killer assumption",
   "fatal risks cleared, or the idea\nreshaped or killed",
   "which risks tested vs carried\nforward; kill rate"),

  ("Hold product truth", "", "GAP",
   "shipped changes from build,\nrelease slices",
   "living, user-side: what the\nproduct does today",
   "drift vs the running app;\nhow often it is actually read"),

  ("Slice a release", "sherpa Launch", "unused",
   "product truth + intent +\nwhat is already built",
   "MVP / v1 / v1.2 — what is in,\nwhat is deferred, and why",
   "scope held vs crept;\ndeferred items that came back"),
 ]),

 ("DESIGN", [
  ("Shape the solution", "superpowers\nbrainstorming", "external",
   "intent, constraints, and the real\nterrain — actual code, not summaries",
   "approaches with trade-offs,\nchosen architecture, boundaries",
   "how often the contract re-derives\ndesign; rework from a wrong shape"),

  ("Agree the shape", "", "GAP",
   "options on constant axes,\ncosts marked, bets named",
   "an approved shape, with its\nbets discharged by name",
   "decisions per gate — did one\nmessage resolve it? reversals after"),
 ]),

 ("CONTRACT", [
  ("Write the contract ·\nSize and assign", "conductor", "ok",
   "the approved shape + terrain\nfetched for the orchestrator",
   "spec file: per-step tags, sized\nmodel + effort, verify commands",
   "keep/delegate ratio; steps failing\nacceptance on first return"),
 ]),

 ("BUILD", [
  ("Execute a unit ·\nProve it worked", "conductor", "ok",
   "one spec slice — scope, files,\nsignatures, the why, verify",
   "the change + evidence: command\noutput, diff, collateral checked",
   "first-pass acceptance rate;\n3-fix escalations per session"),

  ("Review unanchored", "", "GAP",
   "the spec and the diff — nothing\nelse. no session context",
   "what is missing, what does not\nmatch what was agreed",
   "findings the in-loop review missed\n— the whole reason it exists"),

  ("Refuse bad work", "", "GAP",
   "the commit or the branch",
   "pass, or blocked — outside the\nmodel, not a choice to comply",
   "escapes: bad changes that passed;\nblocks that were real"),
 ]),

 ("SESSION", [
  ("Open / close · Keep tempo ·\nHold state", "switch, conductor", "ok",
   "repo state + the last session's\nhandoff",
   "restored context, work committed as\nit verifies, a cold-readable handoff",
   "cold-pickup success — did the next\nsession re-derive? tree clean at boundary"),

  ("Route to the altitude", "", "GAP",
   "the request, before any work\nis sized",
   "which rung to enter at, and\nwhich function runs first",
   "sessions started at the wrong rung;\nskills reached vs left orphaned"),
 ]),

 ("SUPPORT", [
  ("Converge · Human knowledge ·\nHuman voice", "tend, kivna, skriv", "ok",
   "the repo, the session, the prose",
   "conventions applied, vault updated,\ntext that does not read as generated",
   "drift found per run; vault readable\nby someone with no prior context"),

  ("Keep artifacts lean", "trim", "dying",
   "completed feature docs,\nstale TODO items",
   "archived — and eventually nothing,\nonce TODO closure holds",
   "doc count trend; age of the\noldest open TODO item"),
 ]),
]
