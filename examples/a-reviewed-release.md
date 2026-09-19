# A reviewed release

Kerd 0.134.0, released 2026-09-17. It was written by a Claude session and read by Codex, a
second AI that did not write it, before it was pushed. Codex raised five findings across
two rounds. All five were accepted. Two of them changed the rule that was the whole point
of the release.

This is that release as its own records describe it.

## What was built

The owner supplied two versions of the same diagram card. One was written in
implementation terms: function calls, line numbers, type names. The other said the same
thing in product language: what works today, what does not, which part owns the gap, and
what the fix costs. He asked for the difference to be written into Kerd's Visuals skill
as a contract correction, and said explicitly that he did not want a new governance
protocol for it.

The first proposal came back at seven bullets. Most of it was already there:

> The proposal arrived at seven bullets. **Five were already contracted** in
> `skills/visuals/SKILL.md`; "Technical architecture is a deeper view when useful, not the
> default vocabulary" alone covered three plus the entire deep-dive exception.

Two clauses were new. An expansion test, meaning you strip every symbol, path, line
number and type name out of a rendered diagram and the main relationship must still read
to someone who has never opened the source. And visible identity, meaning the project or
repository name is readable inside the picture, not only in the filename or the HTML
title.

At the point it went to review, the work record says: "731 tests green, `gate.py release`
clean."

## What the second AI found

Round one, three findings, all accepted and fixed before the push.

The first is the one worth reading, because the rule it hit was the rule the release
existed to add:

> **High — the expansion test had no passing situation for a whole class of view.**
> As first written it required every view to show "what changes, and what that
> costs". A factual current-state, architecture or audience view has neither. That
> is the 0.133.0 defect — a rule so absolute no legitimate case satisfies it —
> reintroduced in the release whose own record names that defect, by the session
> that had corrected it four hours earlier.

The second: the exception for Kerd's own bundled starter diagram was written as "the
bundled starter patterns carry no project and are the exception", which reads as though
anything made from a starter is exempt, and the same file tells the model to start from
that asset. Narrowed to the untouched asset alone.

The third was mechanical. The README's What's New heading still said v0.133.2 while three
manifests said 0.134.0.

Codex also caught the record claiming the release had shipped before the release action
had run. "Shipped" became "Prepared for 0.134.0".

Then the fix for the first finding was re-reviewed, and it had the same shape as the
problem it fixed.

> **Medium — the three-way split I introduced as the fix for finding 1 created a
> self-classification judgment**, which is the 0.132.0 defect in a new place. A
> future-state architecture is both an architecture view and a proposal, and the
> author could select the lighter "factual … architecture" branch while depicting
> change.

Codex's replacement wording was taken: content decides which test a view takes, never the
title or the diagram type. Any view that depicts or recommends a change takes the fuller
test; a view limited to present facts takes the general one alone.

The fifth finding was that the new README entry both overstated and narrowed the rule at
once, demanding "what it costs" without the qualification the skill carried, and saying
every view names its project where the rule permits project, product or repository.
Corrected.

## What changed because of it

The expansion test was split into a general invariant that applies to every view plus a
four-part test scoped to solution, proposal and correction views, with cost qualified by
"where a cost or boundary exists". The acceptance statement in the work record had the
same gap and was corrected with it, which the record notes "would have passed a view the
skill rejected". The starter exception was narrowed. The branch rule was replaced with
Codex's version. The README entry and heading were fixed.

The session's own summary of the two rounds:

> **Two review rounds, five findings, three of them the same defect class.** The first
> draft reintroduced it; the fix for that reintroduction introduced it again one level
> up. Both were caught by review, neither by any static check — 731 tests and a clean
> gate were green at every one of those points.

And, from the session log:

> The governing rule has never needed changing — **a rule needs a test it can fail and a
> situation it can pass** catches all five unchanged. What changes nothing is more
> rule-writing; what has caught every instance is an independent reader.

## What stayed unproved

The release shipped with its central claim untested in use, and said so at the close:

> **0.134.0's two clauses have not been measured on real diagram output** — they are
> producer checks at review, and nothing has exercised them yet.

The work record says the same thing in its acceptance section: "Both are producer checks
at review, not gates." No test enforces them. The record gives a reason for that too, that
a check could have been written to grep for the identity rule, and that this would be a
new enforcement surface for a rule with no violation history.

Two commits, pushed, CI green on the tip. The record does not claim the rule works. It
claims the rule was read by someone who did not write it, twice, and fixed twice before
it went out.
