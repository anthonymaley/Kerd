# Connecting the work loop · implementation record

## Purpose and authority

Continue build step 2 of the agreed lightweight Conductor design after the user
accepted the session-routing MVP and asked to keep going without “next” prompts.
Work stays in this pack and the isolated candidate. No installed skill changes,
plugin repin, commit, push, publication or global configuration changes.

## What was connected

The accepted transport is now bundled at skills/conductor/scripts/ask.py.
Its initial implementation was byte-identical to the accepted trial snapshot;
the 31 tests traveled with it, with only their source-path layout adjusted.
The trial remains historical acceptance evidence. Maintain new candidate changes
in this pack and copy tested snapshots into the isolated candidate; do not patch
two independent live implementations or copy private trial state.

Conductor loads model-jobs.md when delegating, reads the actual applicable model
guidance, writes the real bounded prompt and invokes the packaged runner against
the current project. The existing work record links results and contributions.
No JSON work-envelope gate or older compiler manifest becomes a usage dependency.

## Observed results · 2026-09-05

| Desired result | Actual evidence |
|---|---|
| The connection travels with the candidate | Original 31 tests passed from the packaged location; three portability checks added. Final suite: 34 passed in 31.928s. No project script copy required. |
| Prepared jobs yield a useful, reviewed result | Independent controller read local model guidance, sent a Claude drafting job, obtained a fresh Codex review, corrected supported findings and saved the completed guide without another approval turn. |
| Read-only Codex can inspect actual files | Candidate wording corrected after the first review needed pasted snapshots. A fresh live run used rg and nl/sed to inspect actual files and verify the final corrections. |
| Switch saves the exact place | Separate save and fresh-pickup agents preserved the unresolved success question and proposed answer. No invented agreement, full build, commit, push, CI, hook or old mode mutation. |
| The work is understandable visually | The connected-loop drawing rendered and was visually inspected at actual 1000px and emulated 390px viewports; no horizontal overflow. Mobile reflows rather than shrinking the desktop drawing. |

The three additional transport tests cover project-subdirectory resolution,
a .git file pointing at separate metadata, and invocation from outside the
consumer project. The .git-file test is not a full linked-worktree lifecycle
test. The runner retains its documented POSIX and abrupt-termination limits.

Useful artifacts, all kept in this pack:

- [The working-loop drawing](../diagrams/working-loop.html).
- [The actual guide](integrated-delivery/using-model-help.md).
- [Claude prompt](integrated-delivery/draft-prompt.md),
  [Codex prompt](integrated-delivery/review-prompt.md),
  [model/effort/profile notes](integrated-delivery/contribution-notes.md).
- [Independent findings and corrections](integrated-delivery/review-result.md).
- [Final on-disk check and telemetry](integrated-delivery/final-file-check.md).
- [Switch save/pickup evidence](integrated-delivery/switch-check.md).

The first guide review's source snapshots and 2026-09 profiles are preserved
as the basis actually used. The later read-only change was verified separately,
not retrospectively credited to that review. The OpenAI family profile's new
2026-09-05 revision removes the old cheapest-tier instruction; the earlier
profile is archived. This implements the user's suitability-first decision,
not a measured claim about a model's superiority. Account/model defaults stayed
untouched. Requested and provider-observed model identity remain distinct.

## What these results do not prove

Prompt-layer judgment is not an unbypassable permission mechanism. The actual
prompts retained this job's outcome, sources, success, authority and completion
condition; that is one semantic inspection, not a universal guarantee.
The final-file run reported 56,128 input tokens including cached and inherited
native context. That is not the short prompt's size or evidence of efficiency.
No speed/cost/quality baseline or effort sweep ran. The unused older compiler
is not a dependency or proof of integrated prompt quality.

Fresh first-use user comprehension, full cross-machine continuity, behavior on
all failure/resource paths and Windows support remain unproved. This is real
bounded delivery evidence, not completion of every acceptance condition in
the broad rework spec. The candidate requires no CI/hooks; other installed
Kerd skills have not yet been migrated.

## Now

The candidate delivery connection and local save/pickup slice are built and
checked. No jobs remain active. The [current entry](../candidate-entry.md)
loads this candidate explicitly. Live adoption, other legacy-skill cleanup and
the complete real-user first-use trial remain separate work. Nothing was
committed, pushed, installed, repinned or published.

Final consistency check: all three candidate skills pass format validation;
the Conductor/Switch and guidance snapshots match their maintained pack source.
The 84 local links checked across 18 current entry/spec/skill/view files resolve.
The original Kerd tracked tree and index remain unchanged. These are consistency
checks, not extra workflow gates or a claim that user comprehension passed.

The [subsequent experience checks](experience-checks.md) exercised more entry
and recovery cases and made two small instruction corrections. They did not
change the transport or supersede the remaining real-user evidence gap above.
