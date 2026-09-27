# What our task evidence supports

Summary first prepared 2026-09-08; the delegated-jobs section below was added
2026-09-27. These are bounded observations, not a model ranking,
proof of optimal effort, or a requirement to repeat benchmarks before each job.
Model choice still needs the current task, available tools and account access.

| Work observed | Useful evidence | Limit |
| --- | --- | --- |
| Claude Fable 5 drafted a model-help guide; Codex GPT-5.6 Terra reviewed it | A real draft, source-based review and applied corrections | Not evidence for Fable 5.1; no model comparison; medium effort requested |
| GPT-5.6 Terra inspected the corrected guide through the CLI bridge | Read-only file inspection and supported findings, with no file changes observed | Codex model identity was not emitted; medium effort requested, not observed |
| GPT-5.6 Sol managed work across a local handoff; Claude Opus 5 assessed it | Work continued from a saved checkpoint; independent review plus separately executed tests | High effort requested; no optimal-effort claim; the local trial alone did not prove a device transfer |

Original records remain in the Kerd development pack, relative to
`docs/work/model-ready-work/`:

- `trials/integrated-delivery/contribution-notes.md`
- `trials/integrated-delivery/final-file-check.md`
- `trials/switch-redesign/live-control/results.md`

Those historical records and their linked artifacts are intentionally not shipped
with the skill. This summary preserves their limits without importing private
transport metadata, temporary-machine paths or a development archive into every
project. Consult the originals when auditing these observations. A consumer's
new job evidence belongs in that consumer's work record, not in this catalogue.

## Delegated jobs, 2026-09-20 to 2026-09-27

Summary prepared 2026-09-27 from 359 native Claude dispatches in Kerd's own
development and two other projects using Kerd. Outcomes are readers' judgments of
what followed each return; the requested model was checked against the observed
one on about 16 jobs, all matching. No job ran the same brief on two models, so
none of this ranks one model above another.

| Work observed | Useful evidence | Limit |
| --- | --- | --- |
| Fable 5.1 (high) reviewing releases, standing in for the other-provider reviewer | Found real, applied problems in each of 15 reviews in one project; none reversed | Only as stand-in; no same-diff comparison with the Codex reviewer |
| Opus 5.5 (high, xhigh) composing scores and design checks | Caught real reasoning errors in designs; usually needed one fix round before use | Five jobs ended on an account session limit, not a quality signal |
| Fable 5.1 (high) composing design drafts | Usually needed a fix round; one built on rulings the brief failed to supersede | Different work from the Opus scores above; not comparable |
| Opus 5.5 and Sonnet 5 players | Most returns accepted as-is; failures traced to gaps in the brief | Twice a player disclosed skipping test-first and was accepted without comment, now a finding by rule |
| Sonnet 5 (high, medium) readers and wording passes | Accurate and scoped; honest "nothing to fix" results | One false "not present" claim and one sweep that missed what a later review found |

The prompt profiles' clauses remain `evaluation: pending`: briefs followed the
profiles' structure, but no job compared a brief with and without a clause.
