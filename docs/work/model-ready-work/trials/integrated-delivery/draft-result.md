# Claude drafting result

Request: model-help-draft-1
Status: completed
Requested/observed model: claude-fable-5 / claude-fable-5
Requested effort: medium
Provider exit: 0

## Provider reply

Draft complete — written but not yet independently assessed.

**File:** `/private/tmp/kerd-job-integration.gKNK7m/docs/work/model-help/using-model-help.md` (same path as the `/tmp/...` alias in the brief; macOS `/tmp` is `/private/tmp`).

**Sources used:** `SKILL.md`, `references/execution.md`, `references/model-jobs.md`, and a targeted read of `ask.py`'s status handling (to confirm "completed means a reply arrived, not that it passed," background waiting, and honest uncertainty reporting).

**What the guide covers, mapped to the agreement:**
- When to ask for review, input, or building, with the rule that a review request authorizes only that review (from model-jobs.md).
- What Conductor handles: model choice with no silent substitution, brief-writing, giving reviewers the original agreement rather than the builder's summary, sending and collecting results — all without command syntax, session IDs, or model settings.
- What the person sees: stage plus current activity (e.g. "Deliver · independent review running"), background work with updates, and inspection of artifacts before claiming success.
- Findings: corrections within existing authority without a fresh "okay," rerun checks, reassessment, and the three-failed-corrections reassessment rule from execution.md.
- Examples: a software one (builder edits agreed files, a different model reviews and changes nothing) and a business one (drafting a pricing section is an editing job; the proposal reviewer reports findings only). Both keep review and editing authority distinct.
- Limits: boundaries are instructions not sandboxes (hence inspection), some checks like running tests may need another route, no publication/commits/purchases/installs implied, existing charges apply.

**Limitations, per the sources:**
- The claim that helpers "can't run tests" is stated in the sources specifically for Claude workers via the bundled runner ("file tools, not Bash"); I generalized it softly as "some checks may need Conductor or another route" to stay accurate across routes.
- The guide omits the runner's failure/cancellation states (`interrupted`, `resolve`, blocked reuse) beyond "Conductor says so plainly" — deliberate, since the audience is nontechnical, but a reviewer may judge that too thin.
- No numeric claims were introduced; the only number is the three-corrections reassessment rule, which comes directly from execution.md.
