# Risk state split — migration review worksheet

Generated 2026-09-03 by the risk-state-split contract spec, Step 1, from the live tree: 21 records, 84 rows; 79 unrecorded severities and 1 ambiguous treatment for producer review.

The producer keys every empty `Key` cell, in batches by record. Legal keys — Severity: `fatal` | `non-fatal`; Treatment: `countermeasure - permanent` | `countermeasure - temporary` | `accepted` | `accepted unknown`. This file commits WITH the migration (the archaeology rule: a reviewed value stays distinguishable from a stated one, forever).

## conductor-boundary.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Two copies of the boundary flow drift apart: conductor's close-out re-describes switch-out and the descriptions diverge over releases | boundaries silently differ by entry path — the exact failure class the single-serializer rule closed in code | the v0.83.0 goal block: two routing documents carried stale boundary claims the edit map missed; prompt-layer drift is the system's best-evidenced failure | fatal |
| 2 | Severity | A second boundary run after conductor already closed (user habit: `/kerd:switch out` after close) | one no-op commit attempt on a clean tree | switch-out on a clean tree reports clean and commits nothing beyond an empty-state check; observed behaviour of the flow | non-fatal |
| 3 | Severity | Pull discipline blurs: conductor running the boundary starts to look like license to pull | mid-task file changes under in-flight work — the reason pull was boundary-only | v0.67.0 rationale unchanged; switch-IN owns pull and is untouched by this slice | non-fatal |
| 4 | Severity | Next-pick suggestions harden into auto-execution (scope creep toward the loop nobody asked for) | producer key eroded — the pick is Tony's by design (choose-what-matters) | Tony 2026-08-06: "suggest when a task completes without building a loop or hook"; the 2026-08-02 loop guard stands for execution even though its CI precondition flipped | non-fatal |

## funnel-driver.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Editing conductor breaks the only working instance of half the system's functions | the daily working protocol goes down in three repos at once with no fallback, and the damage is invisible until a session tries to plan | conductor-role.md transition rule 4 states it directly: breaking it breaks the only working instance of half the system's functions; ~/leru holds 6 spec files written under this protocol | fatal |
| 2 | Severity | The four role names invert under use — Composer is assigned to the human while the spec-writing agent is the Orchestrator | the driver's whole job is coordinating these roles, and instructions written in names that swap under reading will be misread by the model exactly as they were by their author | Tony: "I used orchestrator when I meant conductor... including the composer who writes the specs"; conductor-role.md's own ladder avoids "composer" entirely and names Tony as himself | non-fatal |
| 3 | Severity | A driver that reads the funnel but obliges nothing leaves the machinery unwalked | the whole item delivers a better-informed skill and zero behaviour change, which is the failure this repo has already shipped twice | matrix.py audit reports clean with 0 matrices; docs/gates/ holds no record for switch-fidelity | fatal |
| 4 | Severity | Prompt-layer instruction is not a call — a skill telling the model to run gate.py is advice it can skip | funnel awareness reads as a guarantee in the skill text while being a suggestion in practice, and in consuming repos the tool does not exist at all | CONTEXT.md 2026-08-06: the refusal surface is Kerd's own and prompt-layer-only in consuming projects is the intended contract; grep of skills/ for tool invocations returns zero | fatal |
| 5 | Severity | The queued funnel rename silently rewrites the authority model | the role ladder becomes a role funnel by accident and the seat diagram changes meaning without a decision | funnel-steps.md queues the cross-cutting rename; conductor-role.md lines 9, 12 and 52 use the words for the seat, not the stage | non-fatal |
| 6 | Severity | Two spec clauses cannot be built as written — two-tier access is undefined and the unattended tempo is gated behind an undefined stage | a build either stalls at those rows or invents a meaning, and an invented meaning silently becomes the standard | two-tier access appears in no file but conductor-role.md:49; funnel-steps.md leaves Live deliberately empty | non-fatal |

## gate-reachability.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 2 | Severity | `${CLAUDE_PLUGIN_ROOT}` may not be reliably available inside skill-invoked shell commands, so the canonical invocation cannot be written as designed | The four edits cannot be written as designed. The fallback is a path the user supplies by hand, which is the acceptance criterion inverted — "without manually supplied paths" is the thing being bought | Measured 2026-09-02: `${CLAUDE_PLUGIN_ROOT}` appears in skill text **zero** times across all ten skills; its only proven use anywhere in the plugin is `hooks/hooks.json` | fatal |
| 3 | Severity | The four edits land and the skills still degrade silently, because nothing checks that an invocation resolved — a failed command and an absent one look identical in prose | A later regression reintroducing the defect would be invisible. The skills would fall back to prose exactly as they do today, and nothing on disk would catch it on any subsequent change | Measured: today's failure mode IS silence — the bare relative path yields *No such file*, the skill continues in prose, and nothing is recorded | non-fatal |
| 4 | Severity | Fixing the four gate calls while `progress.py` and `fidelity.py` stay Kerd-pinned leaves a consuming repo half-served, with a working route and no board | A consuming repo can walk the rungs but cannot see position. Switch-in there recovers the narrative and not the location — the half of the session handoff the standing decision says the three files carry worst | Measured 2026-09-02: `progress.py` accepts no `--root` (passing one prints usage and exits 2); `fidelity.py:50` pins `ROOT` to the tool's own file path, so inside a plugin cache it audits the cache | non-fatal |

## gate-visuals.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | A visual is approved without being read — the rubber-stamp failure, at picture speed | an agreed drawing nobody looked at becomes declared truth, and every later comparison is against a fiction | the register's own answer to false approval is presentational, named as an accepted residue on 2026-08-13 | fatal |
| 2 | Severity | Prescribing one visual per gate makes a gate unpassable for work that genuinely has no such picture | a rung blocks on ceremony | design already allows a declaration-driven set rather than a fixed one | non-fatal |
| 3 | Severity | Redrawing from the built side is only strong for two aspects | the comparison is partial and could read as complete | measured in the table above | non-fatal |

## grounding-was-read.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Hollow stamping: a receipt written without attention degrades the receipts check to ceremony — a green "grounding read" light that means nothing | the receipts half's value inverted; trust in the gate erodes | analysis 2026-08-05: no mechanical check can prove comprehension; what is provable — retrieval, exact content version, freshness, presence at gate | non-fatal |
| 2 | Severity | Declaration rot: grounding lists go stale as artifacts move or rename — the audit red-lights legitimate work, or authors stop declaring grounding to avoid friction | reachability value decays; the gate breeds resentment instead of discipline | the repo's own history: renames deferred precisely because references break | non-fatal |
| 3 | Severity | Comprehension-proof creep: slice 2's receipt design grows quizzes, summaries, or attention checks | rigor-rises-ceremony-low violated; the flow cost balloons past the value | the temptation is visible already — this frame had to argue itself out of it | non-fatal |
| 4 | Severity | Resolution is looser than declared: an absolute path resolves without touching the repo, and a directory resolves where the design says file | a grounding line can pass while guaranteeing nothing inside the tree | cold-eyes goal review 2026-08-05: probes showed an absolute ref and a directory ref both resolve clean | non-fatal |

## hooks-autoload.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Auto-load doesn't actually fire on this machine — the docs are right in principle but the harness build here behaves differently | the whole fix is inert: hooks silently absent everywhere instead of silently broken | claude-code-guide confirmed from live docs but flagged "tested but not yet verified" empirically; no fresh-session observation yet | fatal |
| 2 | Severity | Stripping a consumer repo's manual entries before its cache repins to the version shipping hooks.json leaves that repo with no hooks in the gap | brief window with no Kerd hooks in that repo — identical to today, where the pinned path is already dead | the eleven repos already point at pruned versions, so their manual hooks are already non-functional; stripping loses nothing working | non-fatal |
| 3 | Severity | Cutting stop.sh removes the only live surfacing of the conductor phase-stamp to the human at turn-end | the stamp is still written to the marker and read into CONTEXT.md; only the free turn-end echo is lost | `state-contract.md:89`, `time-awareness.md:28` — stop.sh echoes the whole conductor line | non-fatal |
| 3 | Treatment | Cutting stop.sh removes the only live surfacing of the conductor phase-stamp to the human at turn-end | the stamp is still written to the marker and read into CONTEXT.md; only the free turn-end echo is lost | `state-contract.md:89`, `time-awareness.md:28` — stop.sh echoes the whole conductor line | accepted |

## inline-composer.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | A composer call on every small task becomes ceremony, so users abandon conductor for inline work and it leaves fewer artifacts than it does today | worse than the status quo: today inline work leaves no score but still runs under conductor's verification gate; an abandoned conductor loses the gate too | measured: conductor's own text created the lean path for this reason; v0.96.0 and v0.98.0 both chose it | fatal |
| 2 | Severity | Top-tier capacity runs out, so inline work blocks on an unavailable composer | inline work stalls, or silently degrades to a worse score without the producer knowing | conductor already specifies the fallback: write the score as conductor and say so explicitly at the gate | non-fatal |
| 3 | Severity | The score satisfies the contract rung but not the design rung, so inline work still cannot reach goal and the board still misreports it | a composer call is paid for and the board is unchanged — the visible symptom that motivated the investigation survives | measured this session: `gate.py route model-effort-advisory` reports every frame/viability/slice/design input present and still demands `docs/design/<slug>.md` plus a design GO record before contract | non-fatal |
| 4 | Severity | The score is written but nothing checks it was written, so the rule decays into advice | inline work drifts back to no score, invisibly | `OPS-001`, and the measured history of prompt-layer gates in this repo | non-fatal |

## model-effort-advisory.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | The model cannot reliably know the session's current model or effort, so the advisory asserts a wrong current state and advises from it | advice built on a false premise — e.g. telling a session already on Opus to "switch down to Opus", or missing a Fable session entirely | this very session — the prompt says Opus 4.8, the session has run on Fable since 13:26; effort was never visible | fatal |
| 2 | Severity | The advisory beat becomes a nag — every session opens with a model interrogation | friction at orient; users skip conductor | the existing advisory already carries a skip rule ("skip the gate only when the work is trivially small") | non-fatal |
| 3 | Severity | Advising down mid-flow loses session context on the switch | none — `/model` preserves the conversation | this session switched Opus → Fable mid-conversation with full context carried; the risk is empty on the evidence | non-fatal |

## progress-html.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | A third surface that lies: the HTML drifts from the model while the canvas pair stays current — the view Tony actually reads becomes the one nothing checks | the piece's whole value inverted: a trusted-looking page misstates position | the staleness refuser shipped v0.78.0: single-serializer + byte-compare + depth-1 convergence proven on the real tree and in CI ×3 | fatal |
| 2 | Severity | Dashboard-itis: "interactive" creeps into controls, live refresh, a server, things that mutate | scope balloons; the read-only trust story breaks | tonight's conversation already reached for "interact" | non-fatal |
| 3 | Severity | Self-contained constraint fails: interactivity needs something a bare `file://` page can't do | page needs serving or external deps — friction returns | the model is already JSON (`--json` seams on both tools); embed + vanilla JS is standard, no fetch needed when data is inlined | non-fatal |

## push-wiring.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Self-reference loop: the refresh commit changes what the next render shows, so a strict staleness rule or auto-push never converges and every ship deadlocks | all ships blocked — full declared value lost and the ship flow with it | 2026-08-04 probes: re-render after the trailer commit modified both files (depth-1 drift); two consecutive renders byte-identical (md5 pair) — render-only commits carry no `Piece:` trailer, so divergence stops at depth 1 | fatal |
| 2 | Severity | Moving the push into CI needs write-back permission and races concurrent pushes | render commits from CI could conflict with local work or fail silently on token scope | `.github/workflows/gate.yml` carries no `permissions:` block and no push step today; untested | non-fatal |
| 3 | Severity | The staleness gate changes conductor's work-commit flow: a trailer commit can no longer push alone — its render refresh must ride the same push | per-piece pushes become a two-commit pair; forgetting reds the tip at CI, cost is one extra local round | this session's flow: 874c93e (trailers) pushed before 8318029 (render) — under the gate that first push would go red | non-fatal |
| 4 | Severity | True prevention not built: a lying render can land on main and sit red until fixed — detection after the fact, not refusal before landing | cost bounded by reaction time to a loud red check; nothing is silent | goal-gate cold review 2026-08-04: main unprotected, CI on direct pushes is post-hoc by construction | non-fatal |

## release-closeout.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | The fix mode edits away something a human wrote deliberately — an audit with hands rewrites voice, nuance, or a decision it misread as drift | trust in the pass dies on the first bad edit; docs regress silently | five layer-4 blocks show models also *miss* narrative drift; the inverse error (overcorrecting) is untested | fatal |
| 2 | Severity | The pass duplicates CI and rots into noise (checks what R1–R3/AU1–6 already refuse) | wasted tokens per release; findings ignored | the .slainte config already targets CHANGELOG.md, dead since 0.14.0 — stale target lists rot | non-fatal |
| 3 | Severity | Prompt-layer trigger silently skipped (the conductor text isn't honored some session) | one release ships unchecked — today's status quo, not a regression | the invoke-is-literal precedent held on first run (v0.84.0); prompt-layer instructions in this repo are honored but unenforced | non-fatal |
| 4 | Severity | Release moment misdetected (version bump absent from a release-shaped change, or present in a non-release edit) | a pass fires needlessly or misses once | CLAUDE.md release checklist + gate release rules define release = version bump | non-fatal |

## requirements-success-measurement.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | The process is too long or too much friction for the user, and not obvious enough what is happening — no visibility of state, progress and measurements (A5) | the capability is skipped or waived every time, so 0 of 52 stays 0 of 52 while the machinery reads as complete — the "shipped an instrument nobody was obliged to use" failure, measured twice in this repo. This is the WHOLE of the declared value, not a fraction of it, which is what makes the row killer rather than merely serious | `docs/product/funnel-driver.md` gap 8; `rigor-level` slice 2 (per-level floors) specced 2026-08-05 and never built; `grep -i floor tools/gates/*.py` returns nothing | fatal |
| 2 | Severity | It touches conductor and superpowers (A6), and the umbrella rule forbids requiring conductor to change | any design that needs conductor to carry a measurement step re-opens the retired killer risk of `funnel-driver`. Below the declared value: it costs the umbrella rule, not the 0-of-52 outcome — which is why this row is not killer | the rule at `docs/design/funnel-driver.md` — *Drive may CALL conductor, never REQUIRE it to change* | non-fatal |

## requirements-traceability.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Requirements are recorded but the promotion beat is skipped under time pressure, so the register holds the easy requirements and loses the contested ones — which are the valuable ones | the capability is delivered and the loss it exists to stop continues, now with a register that looks complete; worse than absent because it reads as coverage | gap 2: forty-three requirements produced across one session and its follow-on and zero promoted, in a session explicitly about this problem | fatal |
| 2 | Severity | Retrofitting IDs onto finished work manufactures requirements nobody ever stated | fabricated traceability passes its own check and cannot be told apart from the real thing, which destroys the register's only value | the grounding-was-read precedent (2026-08-05) refused retrofits for exactly this reason and made declaring the act of opting in | fatal |
| 3 | Severity | The machinery cannot aim at a consuming project, so the capability degrades to a naming convention nobody checks | traceability is asserted and unenforced in every repo that is not Kerd, which is every repo the capability is for | gap 5: kit.py:24 derives ROOT from the tool's own path; gate.py has no argument parser; the cache ships tools/ so the code is present and merely misaimed | fatal |
| 4 | Severity | The machine can check an ID is present and mapped; it cannot check the mapping is true — a piece naming a requirement it does not build passes green | the check certifies structure and gets read as certifying substance, so a requirement gap survives a green run | the same declared limit already carried by AU5 (resolution is not comprehension) and fidelity.py (reachability is not comprehension) | non-fatal |
| 5 | Severity | The producer authors requirement IDs and the model authors everything downstream, so filing drifts toward what is convenient to build rather than what was asked for | the vocabulary stops meaning what the producer meant, which destroys "speak in IDs that mean something" | the v0.92.0 rename shows the failure is real (names ratified at v0.66.0 came back describing the opposite roles), but that scheme was authored in-session, which this one is not | fatal |
| 6 | Severity | Kerd exercises about a quarter of its own taxonomy, so the capability ships tested against a narrow slice of what it claims to cover | filing rules for UX, INT, SEC, PRIV and CMP requirements are unexercised at ship; a consuming project meets those bugs first | gap 2: filing this session's forty-three requirements put twelve in PRD and left thirteen of the twenty categories empty | non-fatal |
| 7 | Severity | The `Piece:` trailer, the code end of the chain, has never once been written | the forward trace stops at the contract and "requirement to code" is unproven | zero trailers across the 40 commits since v0.91.0, explainable by no contract-run work in that window | non-fatal |

## rigor-level.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Hollow waiving: waived-by-name is the cheapest state, so a model or rushed human waives everything — the table goes green and the level means nothing (an "MVP" that is a spike in substance) | the forcing function's value inverted — a declared level certifies rigor that was never applied; worse than today's silence because it looks checked | analysis 2026-08-05: the state machinery cannot distinguish a considered waiver from a reflex one; what is checkable — a waiver names its reason and review trigger (the accepted-state pattern), and the catalog can declare per-level floors: classes a level cannot waive | fatal |
| 2 | Severity | Catalog is thin or wrong: expansions derive from the catalog, so a class the catalog never names is never asked anywhere — the silence gap reappears one level up | class coverage capped by catalog quality; the gap moves rather than closes | analysis 2026-08-05: the catalog is a living doc, so each discovered miss is one amendment that upgrades every future slice at once — centralised, versus today where the miss recurs silently per slice | non-fatal |
| 3 | Severity | Ceremony creep: the disposition table grows until declaring a level costs more than the judgment it forces — spikes route around the ladder | rigor-rises-ceremony-low violated; adoption dies at the cheap end | analysis 2026-08-05: spike cost is bounded by design at one declared line + zero deviations | non-fatal |

## risk-state-split.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | A half-migrated vocabulary — the checker demanding the new shape while any record still carries the old, or the reverse — makes every work item's ledger fail to parse at once, disabling the whole board in a single commit | Every item's route degrades at once: the parser refuses in both directions (exact-header match), the board cannot derive truthfully, CI goes red at the next push, and nothing advances until the tree converges. No data loss — the parsers only read | Measured 2026-09-03: 21 records carry `## Risk ledger`; exact-header refusal at `kit.py:457-459`; `parse_ledger` consumed at `:740`/`:795` inside the rung checks the board derives from (`:965`); CI runs the gates on every push | fatal |
| 2 | Severity | Hollow treatment — the new Treatment field reads as protection merely because it is populated, so an unproven fix wears the same clothes as a proven one; a treatment is not proven merely because its field is populated | The Treatment half of the declared value silently defeated for any affected row; worst case, a fatal-severity risk advances as treated. A false green, no data loss | Today's machine checks content only for non-emptiness (`kit.py:492`) — it cannot distinguish a proven treatment from an asserted one; the 2026-09-02 incident is recorded in CONTEXT.md | non-fatal |

## rung-vocabulary.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | A half-done rename turns the board red and blocks every push | CI refuses on `progress.py stale` and on front-matter validation; nobody can ship anything until it is finished | the ladder is pinned in exactly two places — `kit.py:34` `RUNGS` and `kit.py:91` `GATE_RECORD_RE` — but `stage:` values live in 20 work records and the board derives from disk | fatal |
| 2 | Severity | `handoff` collides with switch's session handoff, inside our own vocabulary | a newcomer reading bare `handoff` cannot tell whether a session or a work item is being handed over — the exact confusion this item exists to remove, and an inside collision cannot be disambiguated by context the way an outside one can | 15 uses in `skills/switch/SKILL.md`, 19 across `skills/`, 17 across `docs/design/` and the gates README | non-fatal |
| 3 | Severity | `spec` was rejected as the contract replacement because it collides on filenames | `docs/gates/<date>-<slug>-spec.md` and `docs/plans/<date>-<slug>-spec.md` would differ only by folder | `kit.py:682` and `kit.py:711` glob `docs/plans/*-<slug>-spec.md`; `GATE_RECORD_RE` would have matched the same basename shape | non-fatal |
| 4 | Severity | The grounding section cannot cite an external source | Law 4 obliges learning from standards, and the section that records what was read refuses every URL — so the reading is recorded in prose the machine cannot check | `gate.py audit` refused both URLs in this file's own grounding on first write, 2026-08-23 | non-fatal |
| 5 | Severity | Renaming `goal` breaks 7 immutable gate records | history becomes unreadable to the parser, or gets rewritten — and gate records are immutable by contract | `ls docs/gates/` — 17 records, 10 `design` and 7 `goal`; no other rung has ever been recorded | fatal |
| 6 | Severity | `RUNGS` goes from eight entries to seven, and the router walks it | `route()` returns the deepest rung whose cumulative inputs exist; collapsing two rungs into one container changes what every slug reports, including the 20 already on the board | `kit.py:34` defines `RUNGS` as a flat list and `route()` iterates it; the board derives every position from that call | fatal |
| 7 | Severity | ~~Nothing marks an item done once `acceptance` is the last position~~ **ANSWERED 2026-08-25: the terminal state is READY TO RELEASE, not done** — the producer's ruling, *"not done, but 'ready to release'"*, because the work loops after release so `done` names nothing. The literal `stage:` value stays open for design. | today the last rung is `loop`, so a finished item reports `enters at: loop` forever; with `acceptance` last the same ambiguity moves rather than resolving | `route()` returns the deepest rung whose inputs exist, and there is no rung beyond the last one to enter | non-fatal |
| 8 | Severity | This is vocabulary churn dressed as work | a sitting spent on words while `funnel-driver` sits at contract for a fourth day | the item was raised precisely to block that spec | non-fatal |

## shared-memory.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | The views get built over empty sources — seven of the ten render blank because the state they display is never captured | the whole item delivers nothing: a wall of empty pages is worse than no wall, because it looks like coverage and reports clean forever | measured 2026-08-07: matrix audit reports 0 matrices; 0 ruled-out artifacts against a 2026-08-03 decision; no release grouping artifact; no issues list; no architecture diagram among 23 generators | fatal |
| 2 | Severity | Capture stays discipline-dependent — a model must choose to record human input, and the model least likely to record it is one already drifting | the root cause is untouched and every view decays to stale, which returns Tony to checking and reminding, the exact failure this item exists to remove | switch-fidelity's root-cause section, confirmed first-party by Tony 2026-08-07: "all of the x's are where I see the problem regularly, I drive input and direction and we revisit next session" | fatal |
| 3 | Severity | The human view and the machine view drift apart and become two sources of truth | Tony reads a wall that contradicts the repo, which is worse than no wall — he would be making decisions on stale state without knowing it | gap 9 of switch-fidelity, measured at the release pass of 2026-08-06 | fatal |
| 4 | Severity | Drag-and-drop requires a write path from a browser into the repo, which nothing here has ever needed | either the board is read-only and Tony edits it by speaking, or a new and unproven mechanism enters the system | Tony 2026-08-07: "how we move things we can analyse and discuss, but we need a visual to see the overview" | non-fatal |
| 5 | Severity | The reference-design exemption becomes a silent skip and the matrix stays empty | gap 5 persists behind a rule that now looks satisfied, which is worse than an unmet rule because it reports clean | rigor-level's killer risk, 2026-08-05: waived-by-name is the cheapest state and is therefore the licensed habit | non-fatal |

## switch-fidelity.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Pruning to fix accretion introduces erosion — a short session's close overwrites CONTEXT.md and drops an agreed point recorded by an earlier, deeper session | a lost agreed point IS the failure this work exists to remove, so impact equals the declared value — fatal by impact alone if left without a countermeasure | gaps 3-5: git history of CONTEXT.md shows monotonic growth 5,074 to 54,566 bytes and 12 to 59 decisions, one 183-byte dip in five months; no rule requires a new version to be a superset minus superseded | fatal |
| 2 | Severity | Reading more at pickup fills the window faster, forcing more boundaries — each boundary is itself a fidelity risk | more switches per unit of work, compounding every other risk here | measured 2026-08-07: Key Decisions is 88% of CONTEXT.md; the newest session log is 1,005 lines | non-fatal |
| 3 | Severity | The fidelity property stays unfalsifiable — no check exists that a pickup restored what the close recorded, so every countermeasure here ships unverified | the work cannot be proven to have worked; regressions stay invisible exactly as they are today | analysis 2026-08-07: switch has no post-pickup verification step in any mode; the only evidence of continuity is that sessions feel continuous | non-fatal |
| 4 | Severity | "Read in full" instructions get silently bounded by the reader when the target is large | the pickup reads less than specified and reports it as complete, which is indistinguishable from a faithful read | gap 2: at this session's own pickup the model read lines 856-1005 of a 1,005-line log and reported doing so | fatal |

## time-awareness.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | The model writes a plausible time instead of running `date` — the birth failure | false times land in immutable records (worse than no time) and poison the calibration base | the "midnight" self-date; the "late-evening" heading written at midday (kivna/sessions/2026-08-06.md, correction note) | fatal |
| 2 | Severity | Retrofitted timestamps manufacture history | false records at any depth, silently plausible | the grounding precedent: declaring is opting in; a reconstructed value cannot be honest | fatal |
| 3 | Severity | The statusline renders for the human only — the model never sees it | the model stays clock-blind in prose unless it runs `date` itself | Tony's own framing: "the model doesn't see the statusline" | non-fatal |
| 4 | Severity | Clock-line presence unenforced in new records | a new gate record ships without its Clock line, silently | AU rules check shape, not a record's birth date — old records legitimately lack the line | non-fatal |

## vault-unhook.md

| Row | Field | Risk | Impact | Risk evidence | Key |
|---|---|---|---|---|---|
| 1 | Severity | Silent knowledge loss: something is captured only by the vault path today and dies with the auto-save | long-term knowledge value eroded — the thing switch exists to protect | analysis 2026-08-06: Status.md mirrors CONTEXT.md + the latest log; Weekly and domain files re-curate CONTEXT Key Decisions; `people/` files and human-curated domain prose are the genuine vault-only residue — and the on-demand save keeps that path fully writable | non-fatal |
| 2 | Severity | The loved insurance rots silently: an unused-but-valued capability degrades trust when someone finally visits and finds it months stale | the "I'm not losing history" comfort inverts on first stale visit | the interview itself: the vault's value to Tony is its existence, not its freshness; cross-project awareness ("you use that approach in X") was checked and comes from the memory layer (MEMORY.md + episodic search), never the vault — nothing reads the vault in-session by design | non-fatal |
| 3 | Severity | Boundary behavior change surprises the other users mid-habit | one confused boundary, quickly learned | same usage pattern across users (interview); the completion banner will name the change the first time | non-fatal |


## Treatment evidence review — fatal rows

Extension ruled by the producer, 2026-09-03 (option 2): for each
fatal-keyed row, the composer proposes a Treatment-evidence citation that
resolves against the live tree and evidences that row's countermeasure
specifically — or proposes EMPTY with the reason, so a real gap stays
visible instead of hiding inside migration-created noise. The producer
keys the final cell: `empty` (the cell stays empty and the item refuses
honestly), or the citation text that lands verbatim — his edit of a
proposal is welcome and his key is what lands. `gate-reachability.md`
row 1 is excluded: its planned form was ruled 2026-09-02. Every proposed
path below was verified to exist on 2026-09-03.

| Record | Row | Proposed Treatment evidence | Key |
|---|---|---|---|
| conductor-boundary.md | 1 | skills/switch/SKILL.md — the one canonical switch-out definition; conductor's close-out invokes it rather than copying | skills/switch/SKILL.md — the one canonical switch-out definition; conductor's close-out invokes it rather than copying |
| funnel-driver.md | 1 | skills/drive/SKILL.md — the umbrella contract: drive hands each sitting to /kerd:conductor without changing it, so there is no conductor edit to get wrong | skills/drive/SKILL.md — the umbrella contract: drive hands each sitting to /kerd:conductor without changing it, so there is no conductor edit to get wrong |
| funnel-driver.md | 3 | skills/drive/SKILL.md — drive reads the rung from gate.py and is refused by the frame gate until the question set closes: the instrument paired with its obligation | skills/drive/SKILL.md — drive reads the rung from gate.py and is refused by the frame gate until the question set closes: the instrument paired with its obligation |
| funnel-driver.md | 4 | EMPTY — treatment is accepted; a fatal row cannot stand accepted, so the row refuses honestly pending re-treatment | empty |
| gate-reachability.md | 2 | EMPTY — treatment is accepted unknown; the nested-spike measurement has not run | empty |
| gate-visuals.md | 1 | EMPTY — no countermeasure exists (the cell says none yet, the producer's own ruling) | empty |
| hooks-autoload.md | 1 | EMPTY — the fresh-session check is the item's own unbuilt done-condition; no observation recorded | empty |
| inline-composer.md | 1 | docs/design/inline-composer.md — one artifact type sized by content: a short score is legal and answers a small change | planned — the short-score route built and shipped as the design specifies · docs/design/inline-composer.md |
| model-effort-advisory.md | 1 | skills/conductor/SKILL.md — belief plus confirmation, never detection: the advisory states its belief and gates on the confirmed pair | skills/conductor/SKILL.md — belief plus confirmation, never detection: the advisory states its belief and gates on the confirmed pair |
| progress-html.md | 1 | tools/diagram/progress_kit.py — one write path emits the excalidraw/svg/html trio; the stale byte-compare covers all three | tools/diagram/progress_kit.py — one write path emits the excalidraw/svg/html trio; the stale byte-compare covers all three |
| push-wiring.md | 1 | tools/diagram/progress.py — the stale byte-compare; render commits carry no trailer, so every pushed HEAD converges | tools/diagram/progress.py — the stale byte-compare; render commits carry no trailer, so every pushed HEAD converges |
| release-closeout.md | 1 | skills/slainte/SKILL.md — fix discipline: fixes are work commits under the caller's verification gate, and deliberate-not-drift is named as left untouched | skills/slainte/SKILL.md — fix discipline: fixes are work commits under the caller's verification gate, and deliberate-not-drift is named as left untouched |
| requirements-success-measurement.md | 1 | EMPTY — the measurable-success-condition machinery is mid-flight in its own spec; only the rigor declaration is shipped | empty |
| requirements-traceability.md | 1 | docs/requirements/categories.md — the opt-in disposition file the register gate reads: declared categories are refused-into, silence stays silent | docs/requirements/categories.md — the opt-in disposition file the register gate reads: declared categories are refused-into, silence stays silent |
| requirements-traceability.md | 2 | docs/design/requirements-traceability.md — the ruled-out entry: any retrofit of the twenty existing slugs manufactures requirements; forward-only by construction | planned — the forward-only register with retrofit refused, built as the design rules · docs/design/requirements-traceability.md |
| requirements-traceability.md | 3 | tools/gates/kit.py — every function takes root as a parameter; aiming at a consuming project is an argument, not a refactor | empty |
| requirements-traceability.md | 5 | docs/requirements/categories.md — the twenty fixed categories with producer-keyed dispositions; extension only by a producer-named row | docs/requirements/categories.md — the twenty fixed categories with producer-keyed dispositions; extension only by a producer-named row |
| rigor-level.md | 1 | EMPTY — the waiver catalog and per-level floors are this item's own unbuilt machinery | empty |
| risk-state-split.md | 1 | tools/gates/kit.py — fixtures T64–T69: old-only refused, mixed refused, fully-migrated accepted, landing in the migration commit itself | tools/gates/kit.py — fixtures T64–T69: old-only refused, mixed refused, fully-migrated accepted, landing in the migration commit itself |
| rung-vocabulary.md | 1 | docs/gates/2026-08-27-rung-vocabulary-acceptance.md — the acceptance record of the landed rename: atomic, no audit can observe a half-state | docs/gates/2026-08-27-rung-vocabulary-acceptance.md — the acceptance record of the landed rename: atomic, no audit can observe a half-state |
| rung-vocabulary.md | 5 | tools/gates/kit.py — STAGE_ALIASES: retired names read forever, written never; no file on disk renamed | tools/gates/kit.py — STAGE_ALIASES: retired names read forever, written never; no file on disk renamed |
| rung-vocabulary.md | 6 | tools/gates/kit.py — the loop rung's entry and exit carry the folded build/goal checks unchanged; T45 pins the seven-rung ladder | tools/gates/kit.py — the loop rung's entry and exit carry the folded build/goal checks unchanged; T45 pins the seven-rung ladder |
| shared-memory.md | 1 | EMPTY — the slice-order discipline lives in the record's own Scope; no external artifact evidences it yet | empty |
| shared-memory.md | 2 | EMPTY — capture-as-gated-artifact is unbuilt; the gate does not exist | empty |
| shared-memory.md | 3 | EMPTY — the derived, CI-refused pages are unbuilt beyond slice 1's journey head | empty |
| switch-fidelity.md | 1 | skills/switch/SKILL.md — pruning is event-licensed: CONTEXT.md append-only between an acceptance record landing and an explicit agreed drop, so a short session structurally cannot prune | skills/switch/SKILL.md — pruning is event-licensed: CONTEXT.md append-only between an acceptance record landing and an explicit agreed drop, so a short session structurally cannot prune |
| switch-fidelity.md | 4 | EMPTY — treatment is accepted unknown with no countermeasure stated | empty |
| time-awareness.md | 1 | docs/state-contract.md — the same-turn rule, defined once: a time is written only from a machine source produced in the same turn | docs/state-contract.md — the same-turn rule, defined once: a time is written only from a machine source produced in the same turn |
| time-awareness.md | 2 | docs/design/time-awareness.md — new records only: a backfilled time is manufactured history | docs/design/time-awareness.md — new records only: a backfilled time is manufactured history |
