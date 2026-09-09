# Ordinary Out/In: observed candidate-only pickup

Adoption gap 4 in [the current list](../consolidation.md#current-adoption-list--corrected-2026-09-09)
asks for an ordinary save followed by a fresh-session pickup on real work. This
records the first half actually observed, with its cost limits stated rather than
implied. It does not reopen the accepted Switch trial and adds no new trial pack.

## What ran

2026-09-09, from 09:28 EDT. A fresh Claude session in the real Kerd repository was
asked to perform Switch In from the candidate skill only, entering at
consolidation's **Pickup after local closeout**. Installed Kerd Switch was not
invoked, so this is candidate-only behavior on a real project — unlike the 09:00
sitting, which picked up through installed Kerd Switch and said so.

## Observed result

Restoration succeeded. The session recovered the work's purpose, the standing
prohibitions (Seinn is evidence only; the parked schema-split session stays parked;
completed trials are not repeated; no install or publish), the untracked files to
leave alone, the open adoption gaps and the absence of any active build or pending
approval. Nothing was invented to fill a gap, and no numeric budget was fabricated.

The pickup also caught what the record could not tell it: the saved position and
next action had been overtaken by the same day's 09:00 boundary commit, which was
committed and pushed but recorded only in the dated session account. Three living
pointers — consolidation's pickup section, CONTEXT.md and TODO.md — still said the
pack was uncommitted and not on GitHub. Reconciliation was done against Git and
dated evidence, including a read-only `ls-remote` that verified `origin/main`.

## Cost, and what stays unmeasured

Actual input-token cost is **unmeasured**. The host exposes no token readout to the
session, so no claim is made against the trial's 8,000-token and 5%-of-context
targets; neither a pass nor a fail is evidenced here.

What can be counted is bytes read: 63,359 across seven selections, of which 15,237
were the candidate skill's own instructions. A crude four-bytes-per-token proxy puts
that near 15,800 tokens. *[Corrected 2026-09-09: an earlier draft of this record
called that "over budget". A byte conversion is not a token measurement, and being
twice the target on a proxy is grounds for concern, not a measured failure. The
result stays unmeasured in both directions.]* The concern is real enough to act on
— the causes below are worth removing either way — but it is not a verdict.

The overrun has a named cause. The reading set consolidation named came to roughly
20KB. Reconciling the stale pointer forced the 27,894-byte session account, most of
which is an exhaustive 300-path list of the files in the boundary commit — a list
`git show --name-only` reproduces on demand. Stale pointers, and inventories copied
into memory, are what cost this pickup its budget.

## Finding, now addressed: the default verified save could not run here

`handoff.py save --push` is Out's default for an authorized commit-and-push. On
this repository it refuses, correctly:

```
{"status": "blocked", "error": "Unassigned changes need a decision: ...
 live-control/output/__pycache__/*.pyc, kerd-laptop-result.patch"}
```

The index was left untouched. Two untracked `.pyc` files that a reviewed-output
override un-ignores, and the root patch the user instructed be left untracked,
are unassigned work by the helper's rule, and it will not commit around them.
So a scoped boundary in this repository takes the disclosed manual route, which
kept the same three protections: an empty index checked before staging, the file
list named explicitly and compared against the staged set, and the remote branch
checked to carry the exact saved commit before any remote-success claim.

The producer settled the design the same day: files a project has explicitly kept
local are preserved leftovers, not blockers to unrelated work. `save`, `pickup` and
`prepare` now take `--preserve` with exact project-relative paths. A save commits
only its named files and reports acknowledged paths as local only, not saved. A
pickup proceeds past them, and stops untouched if the incoming revision carries one
of those paths, because that collision is a real decision. Unacknowledged changes
still stop both. The acknowledgement is project-local and exact — no pattern, no
ignore entry, no deletion, no stash — and a path that is tracked or missing is
refused, so it cannot quietly hide real work or a typo. Kerd's own acknowledged
paths are named in [consolidation's pickup section](../consolidation.md#pickup-after-local-closeout)
rather than in a new config file.

## What this does and does not establish

Established: a candidate-only Switch In restored a real project from a real save,
and surfaced rather than swallowed a contradiction in its own start point.

Not established: a single end-to-end candidate cycle. The Out that preceded this
was local-only, and an intervening sitting used installed Kerd Switch, so save and
pickup were not one candidate-driven pair. The continuation and visibility gaps are
untouched by this observation. Context cost remains unmeasured.

## Countermeasures taken, and what would falsify them

1. Switch's Out guidance now requires the living handoff to describe the sitting
   that is ending, to keep the pre-save revision distinct from the next action, to
   say which of prepared/committed/remote-verified it reached, and never to embed
   its own resulting commit ID in a file inside that commit.
   [Guidance](../skills/switch/references/in-out.md).
2. `handoff.py pickup` and `prepare` report `overtaken_revisions`: full commit IDs
   a loaded record names that are already in the checkout's history. *[Corrected
   2026-09-09: this is a diagnostic hint, not a staleness test. An older hash is
   ordinary — records cite history and state the position observed before their own
   save. The defect here was an obsolete next action, which no hash can show.]* It
   reports and never refuses; unknown IDs, such as another project's HEAD, stay
   unreported.
3. Preserved local files, above.
4. Regression checks cover the hinted record, the foreign and current IDs, the
   prepared packet, preservation through a save, an unacknowledged change that
   still blocks, a pickup proceeding past leftovers, and an incoming-path
   collision. The Switch script suite is 198 tests, passing.

Expectation: the next handoff written under the corrected Out will not name an
action its own sitting completed, and a pickup loading a record with an older
revision will hint rather than assert.

Replayed against the real case, the second half holds. Running the check over
consolidation.md exactly as it stood at the stale pickup, against the corrected
`HEAD`, reports `d223510451a91ded0eedfeeba95d048d7100b920` — the very revision
whose next action had already been done. The same check over the corrected record
reports nothing. That is a replay of the actual record, not a fixture.

Both halves then ran on this repository for real. The helper that had refused this
boundary saved it, with the three acknowledged paths reported local only and left
untracked on disk. A following pickup of the corrected record returned
`record_loaded` past those same leftovers, listing them and raising no hint. So the
save side, the pickup side and the quiet-on-a-good-record case are observed here,
not only in fixtures.

Still unobserved: a handoff written from scratch under the corrected Out, the hint
reaching a reader inside a real In, and the collision rule firing against a real
remote rather than a temporary one. The next sitting tests the first two. A handoff
that again outlives its own next action falsifies this work.
