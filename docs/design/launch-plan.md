# Launch plan — five outcomes and the path to a real user

**The definition of done (Tony, 2026-09-02):** Kerd is done when a real user
drives a real work item, in their own repository, frame to acceptance, unaided.
Progress is reported against **five outcomes**, never as a percentage —
`91.6%` and `1 of 7` are retired from launch reporting. Full rationale in
CONTEXT.md `## Key Decisions` (2026-09-02).

**The dated record:** `docs/plans/2026-09-02-launch-plan.html` — the decision's
visual, drafted 2026-09-02, recovered into the repo 2026-09-03 from the private
artifact (`https://claude.ai/code/artifact/e26d07b8-437d-4db7-a427-186e614bcf49`).
That render is immutable; this file is the living home.

## The five outcomes

| # | Outcome | What proves it | Status (hand-kept, as of 2026-09-03) |
|---|---|---|---|
| 1 | External execution proven | A throwaway repo routes, passes, audits and **refuses** with no Kerd tree present, driven through the skills rather than by hand | Partial: gate engine externally proven; skill invocation wiring missing |
| 2 | Diagnostic real-product run | A findings document; **PARTIAL is a valid outcome** | Not started; subject chosen (`agent-request`) |
| 3 | Pilot-derived minimum capability built | Every item traces to a line in the outcome-2 findings | Waiting on outcome 2; deliberately unsized until it returns |
| 4 | Clean independent pilot passed | Acceptance reached unaided — **the launch criterion** | Not started |
| 5 | Release completed | Release checks green; known limits documented where a user meets them | Not started |

**Launch: 0 of 5.**

## The critical path

1. Complete `risk-state-split` — the ledger vocabulary migration
   (viability and scope keyed 2026-09-03; design → build → release remain).
2. Re-qualify and complete `gate-reachability` — the four skill invocations
   and foreign-repo fixtures; scope already stated by the producer.
3. Release and refresh the plugin cache.
4. Create the separate `agent-request` repository — never inside Kerd.
5. Run the diagnostic pilot without editing Kerd.
6. Build only what the pilot proves necessary (outcome 3).
7. Run the clean independent pilot (outcome 4 — the criterion).
8. Release when that pilot reaches acceptance without undocumented manual work.

## Binding rules

- **The pilot may not begin before the machinery is reachable** — otherwise it
  measures plumbing rather than product.
- **Kerd is frozen during any pilot run** — breaks are recorded, never
  repaired mid-run, or the instrument becomes a demo.
- **The first pilot is an instrument, not evidence.** It may fail, it may need
  manual intervention, and its output is a findings list. Only the clean pilot
  is the criterion.
- **Outcome 3 stays unsized until outcome 2 returns** — sizing it from
  inspection is how the project previously reached "92% complete" without
  meeting a user.

**Declared limit:** the Status column is hand-kept — no machine derives it.
It is updated at each outcome transition, and its "as of" date says how stale
it may be.
