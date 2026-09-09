# Model-ready work — working demonstration

An isolated implementation of the [design](../design.md). It prepares one
model-neutral work brief as a neutral, Claude, or OpenAI execution prompt
without changing the requirement being evaluated.

The MVP is deliberately isolated from Kerd's live skills. It proves five things:

1. A work brief can be validated before model selection.
2. Exact model IDs resolve to local, versioned profiles without web access.
3. Different model families receive different prompt structure and effort
   configuration while preserving the same task obligations.
4. Every preparation emits a coverage report mapping each required work-brief
   field to the generated prompt.
5. Preparation is deterministic and can be tested without calling a model.

## Run it

```bash
python3 docs/work/model-ready-work/mvp/compiler.py selftest
python3 docs/work/model-ready-work/mvp/compiler.py profiles
python3 docs/work/model-ready-work/mvp/compiler.py compile \
  docs/work/model-ready-work/mvp/examples/foreign-repo-gate.json \
  --model claude-opus-5 --effort high \
  --out /tmp/prompt-run
```

The prepare command (currently named `compile` in this prototype) writes:

- `prompt.txt` — model-specific execution prompt;
- `manifest.json` — work-brief fingerprint, guidance version, configuration,
  coverage mappings, prompt metrics, and source provenance.

Use `--model neutral` for the baseline. The compiler performs no network call
and does not execute the resulting prompt.

## MVP boundary

- JSON is used instead of introducing a YAML dependency.
- Profiles cover current Kerd candidates: Claude Opus 5, Sonnet 5, Fable 5.1;
  OpenAI GPT-5.6 Sol, Terra, and Luna.
- Local profiles are concise interpretations with official source URLs and
  Kerd-owned rendering rules; vendor documentation is not mirrored.
- Dispatch recommendation, token-provider accounting, real model execution,
  independent review, and one-instruction-at-a-time guidance tests belong to
  the full pilot.
