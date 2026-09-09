# MVP run 001 — matched diagnostic

Run date: 2026-09-04. Rubric frozen before either model executed:
`../diagnose-broken-gate-rubric.md`.

## Integrity

- Envelope SHA-256, both variants:
  `77b4010443ab29be09ace1ff8be5ea249079a3382728b5e2f6260b8f5dfdfe28`
- Claude prompt: `anthropic-opus-5@2026-09`, effort `high`, 195 words,
  prompt SHA-256
  `c774621cf48f0545813356d09fb226dd0ea4107d93d7700a40d8e554d2841b9c`.
- OpenAI prompt: `openai-gpt-5-6@2026-09`, `gpt-5.6-sol`, effort
  `medium`, 201 words, prompt SHA-256
  `dfde0a66c6ce8ba654930b4e6c811d477683e57e5aec4123253f0ad9f78a4a20`.
- Fixture SHA-1 before and after both runs:
  `76bba7f385242e20d3e8c3b18a3f2cd9a42706f3`.
- Both ran with read-only permissions and no session persistence. Project
  customizations were disabled for the model run where the CLI exposed that
  control. Neither run changed a file.

## Blind-score result

| Variant | S1 defects | S2 probes | S3 files changed | Mandatory outcome |
|---|---:|---:|---:|---|
| Claude Opus 5, high | 3/3 | 2/3 | 0 | **NOT MET** |
| GPT-5.6 Sol, medium | 3/3 | 3/3 | 0 | **MET** |

### Claude adjudication

Claude correctly found and cited all three causes:

1. `return raw.strip()` does not lowercase severity.
2. `if severity and severity not in LEGAL` silently accepts an empty severity.
3. `return problems[:1]` hides simultaneous failures.

It correctly predicted P1 and P3 before and after correction. For P2 it
proposed merely removing the truthiness guard, producing
`illegal severity: ` after correction. The frozen rubric requires the explicit
result `severity empty`, because the declared correction reports emptiness
before legality checks. S2 therefore scores 2/3; semantic proximity is not used
to edit the rubric after seeing the output.

Claude attempted one Bash-based in-memory probe. The read-only run allowed only
Read and Grep, so the harness denied it. Claude disclosed the denial, hand-traced
the fixture, and completed the report. Reported CLI telemetry:

- API duration: 61.125 seconds; wall time: 61.04 seconds.
- Total cost: USD 0.242735.
- Model output tokens: 4,711, including 2,332 thinking tokens.
- Cache creation input: 9,915; cache-read input: 48,536; direct input: 6.
- Three turns and one permission denial.

The large input/cache numbers are harness overhead, not the 195-word compiled
task prompt. Future comparisons must record task prompt and harness prefix
separately.

### OpenAI adjudication

GPT-5.6 Sol correctly found and cited the same three causes. It proposed an
explicit empty-severity branch, then predicted every frozen before/after result
exactly, including `severity empty` for P2 and both simultaneous findings for
P3. It changed no file.

Reported CLI telemetry:

- Wall time: 44.24 seconds.
- Tokens used: 5,139 (the CLI did not split input, cached input, reasoning, and
  output in the captured text result).
- One shell tool call, used to number the fixture and inspect worktree status.
- The read-only sandbox caused Git to warn that it could not create an Xcode
  cache file; the inspection still returned and the task completed.

## What this proves

This run proves the mechanical MVP end to end:

- one frozen requirement compiled into materially different model-native
  prompts;
- both prompts preserved the identical requirement digest;
- both exact model IDs resolved from local guidance without a web lookup;
- both models could act on the prompt with read-only repository tools;
- the frozen rubric distinguished a close answer from a passing answer;
- model and effort choice changed result, latency, tool behavior, and telemetry.

It does **not** prove GPT-5.6 is generally better, that the adapters beat current
Conductor, or that either clause set caused the result. One task, unequal effort,
different harnesses, and one run per condition cannot support those claims.

## Next experiment

Run the current Conductor baseline and neutral-envelope condition on this same
task, then repeat all four conditions at least three times. Keep model, effort,
tool permissions, and harness prefix as comparable as the products allow. Only
after outcome parity should time or token savings decide a winner. Then ablate
one adapter clause at a time.

