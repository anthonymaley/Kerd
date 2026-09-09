# Example model-ready briefs

This page shows the same job prepared for different model types. The outcome,
proof, boundaries, and stopping point never change. Only the presentation and
recommended effort change.

## The person's work brief

```yaml
outcome: Find why the gate reports the wrong repository root.
deliverable:
  - A diagnosis naming the faulty line and the smallest safe correction.
success_measures:
  - S1: The actual cause is identified from the supplied fixture.
  - S2: The correction preserves worktree and plugin use cases.
  - S3: Every claim points to observable evidence.
proof:
  - File-and-line references for the cause.
  - A command or fixture that reproduces the failure.
context:
  - mvp/fixtures/broken_gate.py
boundaries:
  - Diagnose only; do not edit files.
  - Do not inspect an expected-answer file.
decision_rights:
  model_may_decide:
    - Investigation method and commands.
  person_decides:
    - Whether to implement the correction.
open_questions:
  - Does root discovery stop at the nearest worktree or continue to a parent?
done_when:
  - S1 through S3 are answered, or a blocker is shown with evidence.
```

## Claude Opus type — difficult, high-consequence work

Recommended starting effort: high; test xhigh for deep agentic work.

```xml
<role>You are investigating a repository fault and returning an evidence-backed diagnosis.</role>
<outcome>Find why the gate reports the wrong repository root.</outcome>
<deliverables>
  <item>Name the faulty line and the smallest safe correction.</item>
</deliverables>
<success>
  <measure id="S1">Identify the actual cause from the supplied fixture.</measure>
  <measure id="S2">Preserve worktree and plugin use cases.</measure>
  <measure id="S3">Support every claim with observable evidence.</measure>
</success>
<boundaries>
  <rule>Diagnose only; do not edit files.</rule>
  <rule>Do not inspect an expected-answer file.</rule>
</boundaries>
<context>mvp/fixtures/broken_gate.py</context>
<task>Choose the most effective investigation method. Return file-and-line
evidence and a reproducing command. Stop when S1-S3 are answered or an
evidenced blocker prevents an answer.</task>
```

Why this form: direct instructions and labelled sections make mixed material
easy to distinguish. It leaves the investigation method open.

## Claude Sonnet type — capable everyday work

Recommended starting effort: medium or high, selected from task results.

Use the same structure as the Opus brief, but keep supporting context tighter.
Add a short example only when the required output shape has previously been
misread. Do not add extra procedures merely because the model is less costly.

## Claude Fable type — fast, bounded work

Recommended starting effort: low or medium for narrow tasks; raise it when
evidence shows quality falls.

```xml
<outcome>Find why the supplied gate fixture reports the wrong root.</outcome>
<success>S1 cause identified; S2 both use cases preserved; S3 claims evidenced.</success>
<boundaries>Read only. Do not inspect expected answers.</boundaries>
<input>mvp/fixtures/broken_gate.py</input>
<return>Cause with file/line evidence, smallest safe correction, reproduction command.</return>
```

Why this form: the work is tightly bounded and the return shape is explicit.
If the task requires broad retrieval, the effort level or model choice should
change instead of burying the model in reminders.

## OpenAI Sol type — difficult reasoning and agentic work

Recommended starting effort: medium or high; test xhigh only where results
justify the added time and cost.

```markdown
# Outcome
Find why the gate reports the wrong repository root.

# Success and proof
- S1: identify the actual cause from the supplied fixture.
- S2: ensure the proposed correction preserves worktree and plugin use cases.
- S3: support every claim with file/line evidence and a reproducing command.

# Boundaries and decisions
- Diagnose only; do not edit files or inspect expected answers.
- Choose the investigation method and commands.
- The person decides whether to implement the correction.

# Stop condition
Stop when S1-S3 are answered or an evidenced blocker prevents an answer.

# Context
mvp/fixtures/broken_gate.py
```

Why this form: it leads with the outcome, makes proof and stopping explicit,
and avoids prescribing reasoning steps. Effort is set in model configuration,
not by telling the model to “think harder” in the brief.

## OpenAI Terra type — balanced everyday work

Recommended starting effort: medium.

Use the same outcome-first structure as Sol. Keep the context narrowly scoped
and state the exact deliverable. Add a checklist only when the task itself has
several mandatory parts, not as generic process ceremony.

## OpenAI Luna type — quick, well-bounded work

Recommended starting effort: low or medium.

```markdown
Outcome: diagnose why `mvp/fixtures/broken_gate.py` reports the wrong root.

Return: cause with file/line evidence, the smallest safe correction, and one
reproduction command. Preserve worktree and plugin behavior. Read only; do not
inspect expected answers. Stop after S1-S3 are evidenced or a blocker is proven.
```

Why this form: it minimizes preparation overhead for a narrow job while
preserving every obligation. If the coverage check cannot map an obligation,
this compact version is refused rather than executed.

## What is actually different

| Model type | Main change | What never changes |
|---|---|---|
| Claude Opus | Labelled boundaries and room for deep autonomous work | outcome, measures, proof, boundaries |
| Claude Sonnet | Tight context and optional shape example | outcome, measures, proof, boundaries |
| Claude Fable | Compact brief and explicit return shape | outcome, measures, proof, boundaries |
| OpenAI Sol | Outcome-first sections and explicit stop condition | outcome, measures, proof, boundaries |
| OpenAI Terra | Balanced context and only task-required checklists | outcome, measures, proof, boundaries |
| OpenAI Luna | Minimal direct form for narrow work | outcome, measures, proof, boundaries |

These are starting profiles. The evaluation loop decides which differences
remain; provider documentation alone does not make them permanent.

