---
name: spike
description: "Throw multiple ideas at the wall to learn what works. Directional but exploratory — no plan, no decomposition. Captures wins AND losses with evidence; commits cleanly so working solutions are extractable for the real build. Use when uncertainty is high, tries are cheap, and a plan would be premature."
category: development
core_skills:
  - kerd:switch
  - kerd:kivna
discover_keywords:
  - "spike"
  - "prototype"
  - "throw at the wall"
  - "see what sticks"
  - "try a bunch"
  - "experiment"
  - "validate"
  - "explore"
  - "rapid"
---

## Setup

- [ ] `/kerd:switch` in light -- minimal session open, no smoke test
- [ ] Extract the bigger idea -- read CLAUDE.md, CONTEXT.md (`## Where We Are`), TODO.md (`## Now`), and any `docs/research/` files. State the bigger idea in one line for confirmation. Do NOT decompose into tasks. The direction is the constraint; the spike is the surface area.
- [ ] Pre-flight inventory -- in one pass, ask the user for everything that will otherwise get trickled in mid-spike: accounts/credentials available vs not, sample inputs (URLs, files, API keys), hardware/environment state, scope limits ("today: prove X. Out of scope: Y, Z."). Capture in CONTEXT.md (`## Where We Are` for environment state, `## Open Questions` for unresolved inputs). Skipping this multiplies friction by 5–10x because each missing input becomes a stop-and-ask round.
- [ ] Empirical primitive first -- name the cheap, fast, ground-truth probe for this domain (e.g. AASA fetch for tvOS deep-links, `curl` for APIs, sample-data fetch for analytics, canary deploy for infrastructure). Run it once across the entire surface BEFORE generating any try matrix. This replaces guessing with observation. Skip ONLY if no such primitive exists for the domain — and say so explicitly.
- [ ] Identify or create the captured-evidence file -- look for `docs/research/[topic]-spec.md` or equivalent. If one exists, append to it. If not, propose a path and create on first capture, not upfront.

## Try

- [ ] Generate the try matrix -- batch hard. For hardware/long-loop tests, default to N+1 variants over what was asked. Add the obvious next variants without asking. The round-trip is the bottleneck.
- [ ] Ship the build -- the user runs the tests on real hardware, real users, real environment. Do not simulate when the real test loop is the whole point.
- [ ] Verify each variant before tagging it ✓ -- "I added it" never equals "it works." Test the just-added variant in the same loop iteration. Never batch verification to close-out. The most expensive bugs (Infuse `&name=` parameter not working, "Prime was working no?" regression after URL change) come from tagging-then-deferring-verification.
- [ ] Record results immediately as they come in:
  - **Wins** → captured-evidence file with: what worked, what variant, when verified, what evidence
  - **Provisional losses** → captured-evidence file's "provisional decline" zone — NOT promoted to canonical "decline" until the loss survives EITHER (a) one configuration change (e.g. adding `LSApplicationQueriesSchemes`) OR (b) one explicit user push-back round. Each provisional entry must list "what would change my mind" and "what I have not yet tried."
  - Promote provisional → canonical only after the survival test. Closure-bias is the default failure mode of spike work; this gate is the structural fix for it.
  - Both wins and losses must cite specific session moments. Do not infer outcomes from theory.
- [ ] **Strong-language gate (claim-formation).** Before tagging anything with "verified", "definitively", "impossible", "always", "never", "private mechanism", "service-policy", "closed", "decline", or equivalents: require ≥3 confirming observations OR a documented source citation in the spec file. Without those, use "tested but not yet verified" / "the evidence I have suggests" / "from training data; may be wrong". This is the global CLAUDE.md Claim Discipline applied to spike's specific vocabulary — same structural gate, named here so it triggers at the moment of writing the spec entry.
- [ ] When external research is needed (docs, AASA, community sources, SDK availability), try ≥3 alternate URLs/search angles before declaring docs unavailable. WebFetch failure ≠ stop. Specifically: don't fall back to general-knowledge guessing about external systems — the assistant's training-data confidence is precisely the wrong tool for spike work. Each external claim must carry a "verified by [URL/doc]" tag, OR be downgraded to "from training data; may be outdated".
- [ ] **Tripwires (immediate flag during Try, not deferred to close-out).** Stop and re-examine immediately if any of these occur:
  - A "✓ verified" tag is about to be written on something not empirically retested in this loop iteration → flag and downgrade
  - Strong-language vocabulary used without citation → flag and downgrade
  - Architectural claim made from 1-2 negative observations without alternate-explanation enumeration → flag and scope it ("tested with X, Y; W and Z untried")
- [ ] Trim the matrix as findings stabilize -- when a variant graduates to confirmed-win or canonical-loss, remove it from the active try surface at the next loop iteration. The captured-evidence file retains the full record; the running matrix is for unknowns only. Don't wait for the user to say "remove broken ones."
- [ ] Loop back to "Generate the try matrix" with what was learned. Continue until either (a) enough wins to graduate, (b) enough canonical losses to redirect, or (c) the user calls wrap-up.

## Close

- [ ] **Self-audit against baseline.** Count strong-language claims in the spec file vs. citations supporting them. Baseline (3of3 spike, 2026-04-25): ~33-42% confident-wrong rate per investigation, 4/5 user-detected. Target: <10% confident-wrong, 0 ungated platform claims, 0 "verified" tags without retest. Record the count in the session log so we can measure whether spike-mode's gates actually grip across sessions.
- [ ] Removed-from-backlog log -- ask "what did we learn we don't need?" Append disproven hypotheses to a Removed/Disproven section. Spike work generates as much value from disproven assumptions as from confirmed ones, but only if recorded.
- [ ] Commit graduation -- review the spike's working code. For each output, classify explicitly: `keep-as-is` (production-ready), `extract-and-promote` (move into real code), or `discard` (was a try, not a keeper). Make the decision visible before committing.
- [ ] Clean commits -- each confirmed-working solution gets its own commit with evidence in the message (e.g. "spike: Peacock iOS-share URL works, verified on Apple TV 4K 2026-04-25"). Disproven attempts get committed separately as "spike: confirmed [X] declines, evidence in [file]" so they're discoverable but not mistaken for working code.
- [ ] `/kerd:kivna` save -- update vault if the spike produced strategically-significant findings. Skip if outcomes are purely tactical.
- [ ] `/kerd:switch` out -- close session
