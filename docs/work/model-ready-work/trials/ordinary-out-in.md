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
that near 15,800 tokens. That is an estimate, not a measurement, and it is well above
the target's proxy equivalent — so treat this pickup as over budget pending real
instrumentation, not as an unknown that might have passed.

The overrun has a named cause. The reading set consolidation named came to roughly
20KB. Reconciling the stale pointer forced the 27,894-byte session account, most of
which is an exhaustive 300-path list of the files in the boundary commit — a list
`git show --name-only` reproduces on demand. Stale pointers, and inventories copied
into memory, are what cost this pickup its budget.

## Finding: the default verified save cannot run here

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

This is a limitation to weigh, not a defect to patch here: relaxing the rule
would let a save sweep in work nobody assigned. Whether the helper should learn
"leave these paths alone" is an open design question, unowned as of this record.

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
2. `handoff.py pickup` and `prepare` now report `overtaken_revisions`: full commit
   IDs a loaded record names that the checkout already contains. It reports and
   does not refuse; unknown IDs, such as another project's HEAD, stay unreported.
3. Three regression checks cover the stale-handoff case, the foreign/current-ID
   case and the prepared packet. The whole Switch script suite is 193 tests, passing.

Expectation: the next handoff written under the corrected Out will not name an
action its own sitting completed, and a pickup loading an overtaken record will
report it before acting.

Replayed against the real case, the second half holds. Running the check over
consolidation.md exactly as it stood at the stale pickup, against the corrected
`HEAD`, reports `d223510451a91ded0eedfeeba95d048d7100b920` — the very revision
whose next action had already been done. The same check over the corrected record
reports nothing. That is a replay of the actual record, not a fixture, and not yet
a live pickup: `handoff.py pickup` refuses on this repository while the instructed
untracked files sit in the tree ("Local changes exist"), which is the same
limitation the save side hit.

Still unobserved: a handoff written from scratch under the corrected Out, and the
signal reaching a reader inside a real In. The next sitting tests both. A quiet
signal on a genuinely stale record, or a handoff that again outlives its own next
action, falsifies this.
