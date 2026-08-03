# TODO

## Now

- **Agree the 18 first-cut requirements, one at a time.** They're in movement 9 of `docs/plans/2026-08-02-product-to-build.excalidraw`. Sequencing is Tony's: requirements → agree → *then* HOW and WHAT, which dictates what happens to the five scattered communication statements and to every other function. Two are marked `(?)` because they're drafted rather than read, and are where to start: *Design the interface MUST output machine-checkable values* (would constrain how Tony designs), and *How we talk to each other needs an enforcement point* (that's a solution smuggled into a requirement).
- **Do NOT use `/kerd:capturerequirements` for this** — Tony's explicit instruction. It's under review, and its dated-snapshot output shape is the thing we suspect is wrong.
- **Nothing gets ripped until the design is approved.**
- **v0.66–v0.68 are installed and still have never run.** First real conductor session should watch: does the orchestrator subagent reliably write-and-summarise; does after-the-body tagging shrink `[keep]` (prediction: mostly delegate, one or two review steps); does a `[keep]` diff-review catch collateral a verify command misses. Tony is out of Fable credits, so the first run will exercise the unavailable-orchestrator fallback rather than the happy path.

## Backlog

- **The SPIKE** (movement 7): route ONE dead skill cheaply and watch whether it gets used. Beats route-vs-rip as a binary — neither side has evidence. Candidate: `capturerequirements`, as the cheapest to wire with the cleanest signal.
- **CI on `~/3of3`** — the highest-consequence item on the board and the least Kerd-shaped. 0 workflows, 0 pre-commit hooks, every repo; build-green has already proven untrustworthy there.
- Repin remaining repos to the current cache version: `leru`, `krutho-strategy`, `krutho-founders` are all still on `kerd/0.65.0` — alive today, one GC from breaking silently. `~/3of3` was repinned to 0.68.0 this session. `obair` has no Kerd pin at all (deliberate, or drift — unchecked).
- Hook version staleness check in `/kerd:tend` — four occurrences now; the manual sweep only ever fixes the repo you happen to be looking at.
- Guard switch-in step 3 smoke test against context bloat (delegate the build/test run; absorb a verdict, never a full log). A spec for this was produced as the orchestrator mechanic test and is in the scratchpad, not the repo.
- Decide whether switch should commit the vault repo (contract vs behaviour disagree — see CONTEXT.md).
- `CHANGELOG.md` is stale at 0.14.0 while the repo is at 0.68.0, and it's absent from the CLAUDE.md release checklist. Revive it or delete it.
- Surface model-tiered delegation in the two plugin capability-list descriptions, or leave "session discipline" to subsume it. Open since v0.64.0; still unanswered.
- Dogfood sherpa on `~/Bree` — now contingent on the design pass, since sherpa may be routed, reshaped or ripped.
- Mode reconciliation deferred until that same decision; clean krutho-strategy's stray `sessions-of-record/`.
- skriv voice profile: wiring held pending non-founder-genre samples.
- Stale Kerd.md MOC version field (says 0.31.0) — update per release or remove (lean remove).
- Consider promoting the refined question-formation rule from the pair hook into global `~/.claude/CLAUDE.md`. Note: this is one of the five statements the design pass found don't bind, so it may be superseded by whatever the requirements agreement decides.
