# appended as a separate module — imported by the main generator
FUNCTIONS = [
 ("PRODUCT", [
  ("Frame the intent",     "why this exists, what it must do — high level, enough to inform the rung below", "sherpa Explore", "unused"),
  ("Test viability",       "demand · economics · differentiation · access · feasibility. cheapest test first", "interrogate / sherpa Validate", "unused"),
  ("Hold product truth",   "living, user-side: what the product does today. overwritten, never dated", "", "GAP"),
  ("Slice a release",      "MVP / v1 / v1.2 — what is in, what is deferred, and why", "sherpa Launch", "unused"),
 ]),
 ("DESIGN", [
  ("Shape the solution",   "approaches, architecture, components, boundaries — how the thing is built", "superpowers brainstorming", "external"),
  ("Agree the shape",      "options on constant axes, costs marked, bets named, approved before build", "", "GAP"),
 ]),
 ("CONTRACT", [
  ("Write the contract",   "exact files, signatures, the why, a verify command with expected output", "conductor · orchestrator", "ok"),
  ("Size and assign",      "keep vs delegate, model and effort per step, approved at the gate", "conductor · tags", "ok"),
 ]),
 ("BUILD", [
  ("Execute a unit",       "one step, from the contract, by a model that never saw the reasoning", "conductor · players", "ok"),
  ("Prove it worked",      "run the check, read it, and check for collateral — what changed that shouldn't", "conductor · verify gate", "ok"),
  ("Review unanchored",    "fresh context, given only spec + diff: what is missing, what does not match", "", "GAP"),
  ("Refuse bad work",      "automated, outside the model, able to block. the only thing that can say no", "", "GAP"),
 ]),
 ("SESSION", [
  ("Open / close a session","context in, state out, boundary commits, handoff that survives going cold", "switch", "ok"),
  ("Keep tempo",           "scope held, 3-fix limit, claim discipline, work committed as it verifies", "conductor", "ok"),
  ("Hold project state",   "what is true / what is next / what happened — one file each", "CONTEXT · TODO · sessions", "ok"),
  ("Route to the altitude","decide what kind of work this is, and enter at the right rung", "", "GAP"),
 ]),
 ("SUPPORT", [
  ("Converge structure",   "setup a repo, detect drift, fix gaps against current conventions", "tend", "ok"),
  ("Hold human knowledge", "readable by someone with no prior context. one write per session", "kivna", "ok"),
  ("Write in a human voice","prose that does not read as generated", "skriv", "ok"),
  ("Keep artifacts lean",  "archive what is done — dies once TODO closure holds", "trim", "dying"),
 ]),
]
