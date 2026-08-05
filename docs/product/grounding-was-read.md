---
route: new
stage: done
---

# Grounding-was-read — lost becomes a red light

## Value

Born as the entry gate's declared second job (deferred in A8 of the
entry-gates spec) and the closing move of the walk's reachability rule:
an artifact is reachable when at least one function's grounding names
it, gate-enforced. The measured failure behind it: the 6 July design
doc that held 1 August's answer — well-named, on disk, unread; nothing
in the system could even detect that it had been skipped.

Value, in units:

- **Lost is a checkable state** — today: no mechanism can detect an
  unreachable or vanished grounding artifact; target: a work item's
  declared grounding is machine-readable data, and **a broken
  grounding reference at a pushed tip goes red within one CI run,
  never silent** — detection at the tip, the same calibrated wording
  push-wiring settled on. *(Amended at the goal gate, 2026-08-05: the
  original "0 broken references at any pushed tip" was unenforceable —
  no branch protection, CI runs post-landing — and non-discriminating:
  declaring is optional, so an empty repo scores 0 trivially. The
  guarantee is per declared section.)*
- **Grounding gets skipped silently** — today: inputs arrive on their
  own, but the background reading (standing decisions, the living
  design docs of what the work touches) is exactly what gets skipped
  under pressure, and skipping leaves no trace; target (slice 2):
  a rung passes its gate only when every declared grounding artifact
  carries a fresh read-receipt. **0 rungs passed with missing or stale
  receipts.**

The honest limit, declared up front: a receipt can prove **retrieval
at an exact content version** — the file was read by the stamping tool,
at that moment, at that content — never *comprehension*. The check's
claim is retrieval-at-version, the same declared-simplification class
as "goal counts checked boxes" and detection-at-tip.

Named honestly: **slice 1 does not cure the 6 July instance** — that
doc resolved fine on disk and went unread, which is the second
target's (deferred) business. Slice 1's own win is the sibling
failure — the artifact that moved, vanished, or was never reachable —
plus the declaration substrate without which no receipt could ever
know what to check.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Hollow stamping: a receipt written without attention degrades the receipts check to ceremony — a green "grounding read" light that means nothing | yes | the receipts half's value inverted; trust in the gate erodes | medium — models under pressure to succeed stamp; rushed humans too | analysis 2026-08-05: no mechanical check can prove comprehension; what is provable — retrieval, exact content version, freshness, presence at gate | countermeasure - permanent | The check's claim is declared as retrieval-at-version, never understanding; receipts are stamped by a tool that itself reads the file and records content identity; a receipt goes stale the moment its artifact changes; receipts land in slice 2 so slice 1 carries no hollow-stamp surface at all | |
| Declaration rot: grounding lists go stale as artifacts move or rename — the audit red-lights legitimate work, or authors stop declaring grounding to avoid friction | no | reachability value decays; the gate breeds resentment instead of discipline | medium — docs have already moved once (the vault move, the date-split renames deferred) | the repo's own history: renames deferred precisely because references break | countermeasure - permanent | the reachability audit runs in CI, so rot is caught at the push that causes it with the fix named — never discovered archaeologically | |
| Comprehension-proof creep: slice 2's receipt design grows quizzes, summaries, or attention checks | no | rigor-rises-ceremony-low violated; the flow cost balloons past the value | low | the temptation is visible already — this frame had to argue itself out of it | accepted | | if any receipt design proposes a check beyond presence + freshness, this row must be re-argued before it ships |
| Resolution is looser than declared: an absolute path resolves without touching the repo, and a directory resolves where the design says file | no | a grounding line can pass while guaranteeing nothing inside the tree | low — repo docs have no reason to carry absolute or directory refs | cold-eyes goal review 2026-08-05: probes showed an absolute ref and a directory ref both resolve clean | accepted | | the first real grounding line that is not a plain relative file path re-argues this row |

## Release slice

Smallest valuable slice — **slice 1: declarations + the reachability
audit** (Tony's call, 2026-08-05): a work item's grounding becomes
machine-readable data in its own product doc — the `## Grounding`
section, per-item, as the design settled after finding A8's sketched
gate-table slot never existed *(amended at the goal gate: this
paragraph originally still promised that dead landing site)* — and a
CI audit rule proves every declared grounding reference resolves on
disk — a broken reference is a refusal naming the file and the
reference. The slice's
win: **"lost" is a checkable state for the first time**, and it cannot
be hollow — resolution is pure mechanics.

Deliberately excluded, named:

- **Read-receipts at gates** — slice 2, carrying the hollow-stamping
  ledger row and the retrieval-not-comprehension claim; its receipt
  shape rides the `mark_reviewed` precedent (reading as an explicit,
  dated, content-anchored act).
- **Any comprehension proof** — never, per the ledger's third row.

The design rung's hard question, named now rather than discovered
there: **declaration granularity** — static per-rung grounding classes
(authorable once, coarse; cannot name "the living design docs of what
this work touches", which varies per work item) versus per-work-item
grounding lists (precise; authored every time, so they carry their own
rot and ceremony risk). The design conversation owns the choice; the
slice commits only to machine-readable declarations and a resolving
audit, whichever shape wins.

## Grounding

- docs/design/grounding-was-read.md — the design this slice implements; AU5's semantics are measured against it
- tools/gates/kit.py — the harness AU5 lands in
- docs/gates/*-grounding-was-read-design.md — the design GO record that admitted this build
- CONTEXT.md — standing decisions bind the implementation
