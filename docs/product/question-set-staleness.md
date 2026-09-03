---
route: new
stage: framed
---

# A derived question set knows when it has gone stale

## Value

Tony's requirement, in his words (2026-09-02 evening, stated at the frame gate
the previous boundary deliberately deferred to keep the value statement his):

> It must prevent me from trusting a question set that looks current but was
> derived from rules the repository has since changed. I should not enter a
> producer conversation with obsolete questions, omit a newly required judgment,
> or tell you a rung is adequately examined when the set no longer represents its
> gate. If that happens, the stale set creates false confidence and pushes the
> defect into later work, where correction costs more. It must also prevent the
> opposite failure: invalidating sets for unrelated edits so frequently that
> freshness becomes noise and people learn to ignore or bypass it.

**The value is stated in two directions, and both are load-bearing.** A
mechanism that only catches staleness is trivially satisfiable by invalidating
everything always; a mechanism that only avoids noise is satisfiable by never
firing. Neither half alone is the requirement.

**What winning looks like, in units — his words, same sitting:**

> Six weeks from now, it is working if three observable things are true:
>
> - Every change to a rule or standing decision actually used by a question set
>   makes that set stale before its next use.
> - Unrelated edits do not invalidate it.
> - A newly relevant decision that was never among the original sources is
>   discovered at the scheduled review before the set is relied on again.
>
> I would want fixtures proving both directions — relevant changes refuse,
> irrelevant changes remain valid — and six weeks of use with zero stale sets
> used and zero invalidations people had to dismiss as noise.

So the measurements this item is answerable to are: **fixtures covering both
directions**, and over six weeks of real use, **zero stale sets used** and
**zero invalidations dismissed as noise**. The third condition — discovery of a
relevant decision that was never a named source — is what makes the scheduled
review a separate mechanism rather than a fallback on the first.

**The mechanism this frame exists to build was already ruled** (CONTEXT.md,
2026-09-02): the exact gate demands and standing decisions a set was derived
from, named individually · a derivation fingerprint over those named sources ·
a refusal condition, so any named source changing marks the set stale before
its next use · a periodic Law 4 review trigger for discovering relevant sources
that were never named. Both alternatives were refused by name — re-deriving on
every invocation *"wastes work without solving the harder problem: an unlisted
new decision would remain invisible"*, and a date-only review trigger *"is also
too weak."*

**Why this comes before the five remaining question sets.** The spike proved a
viability set derives — five of six questions traced to a machine-enforced
refusal in `kit.py`, cited by line — and proved the harder thing: derivation is
backward-looking. Writing five more artifacts that go stale silently, with
nothing able to catch it, builds the defect this item exists to prevent, five
times over.

**The ledger below is named, not qualified, and the empty cells are
deliberate.** The frame gate's floor is presence: a killer risk named, with no
sizing and no evidence, because the risks of a thing not yet scoped cannot be
qualified against a commitment that does not exist. Every row will be refused at
the scope gate until it carries Evidence, a legal State, and a countermeasure.
That refusal is correct and is left standing rather than papered over with a
plausible disposition — per the 2026-08-31 ruling that `unqualified` is workflow
incompleteness, not a durable risk state.

## Grounding

- docs/design/question-set-derivation-findings.md — the spike's verdict (PARTIAL), the candidate viability set with its per-question citations, and the recommended-but-unbuilt mechanism this item frames.
- docs/product/question-set-derivation.md — the spike's own frame and its declared kill-or-keep, including the criterion reported as searched-and-not-found rather than satisfied.
- CONTEXT.md — the 2026-09-02 ruling on source-bound invalidation versus re-derivation per use; the suspect-link-stamp decision this is same-family with (a stored reference proves existence, never sameness); the 2026-09-01 approval-fingerprint ruling that one versioned mechanism is preferred over a second recipe; and the measured count of dormant review triggers that nothing fires.
- tools/gates/kit.py — the refusals a derived question actually binds to (`parse_ledger` and `LEDGER_COLUMNS`), and `req_statement_hash` at line 1191, the one hashing recipe that exists on disk today.
- tools/gates/README.md — the rung exit/entry rule (line 42) the whole derivation rests on: a rung's exit is the next rung's entry.
- docs/work/question-sets/software-change.md — the only question set on disk, and the shape a derived set would have to carry its named sources in.
- tools/reqview/fingerprint.py — the second live implementation of a hashing recipe, and the standing warning that nothing tests it against the Python one.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Invalidation fires on edits that do not change any cited rule, so freshness reads as noise and people learn to dismiss or bypass it — leaving a mechanism that still claims to protect while being routed around | yes |  |  |  |  |  |  |
| The scheduled discovery review is a human beat with no forcing function, so the half of the mechanism that catches unlisted new decisions never runs — and the third success condition is delivered by nothing | yes |  |  |  |  |  |  |
| A standing decision is a prose bullet in a file with no stable anchor, so there may be nothing addressable to fingerprint at the granularity the value statement requires | no |  |  |  |  |  |  |
| The refusal is prompt-layer, so a set can be used while stale by a model that simply proceeds — the repo's standing finding that skill text cannot enforce on itself | no |  |  |  |  |  |  |
