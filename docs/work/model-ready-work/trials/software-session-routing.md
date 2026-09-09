# Trial 1: multi-model session routing

## Outcome

Create and demonstrate a lightweight, automatable way for user-started Claude
and Codex sessions to register their usable session IDs for one repository.
Conductor can then assign a bounded task or review to an appropriate registered
session, or follow a direction such as “ask Codex to review this,” and receive
the result without the person copying session IDs or prompts.

## Experience

```text
Person starts Claude or Codex normally
             |
             v
Kerd registers the usable session for this repository
             |
             v
Conductor chooses a session, or follows a provider direction
             |
             v
Conductor assesses the job and prepares it for that model and effort
             |
             v
Registered session executes the bounded job
             |
             v
Result returns to Conductor with provenance
```

Kerd does not launch model sessions. Registration makes a session addressable;
it does not grant authority. Cross-model authority is approved once during
Shape, or supplied directly by the person's request.

## Required result

- Automatic, repository-specific registration after the person starts a Claude
  or Codex session.
- A routing record containing provider, session ID, repository, observable
  model and effort, availability or last seen, current job if any, registration
  time, and the supported send/resume mechanism.
- No credentials, secrets, or conversation contents in that record.
- Automatic selection from suitable registered sessions and explicit
  provider-directed selection.
- Model- and effort-specific preparation of a bounded execution or review job.
- Delivery, execution, and automatic result return with provenance.
- Honest refusal for a missing, stale, unavailable, wrong-provider, or
  wrong-repository session.
- A documented setup and recovery path that remains lightweight.

## Discovery owed

Do not assume a wrapper command is required. Investigate the most reliable
official and observable mechanisms for each provider: native lifecycle hooks,
CLI output, environment data, resumable-session metadata, and only then a small
launcher if no reliable native path exists. Judge options on reliability,
portability, setup burden, privacy, failure visibility, and automation.

## Measures

| ID | Measure | Pass condition |
|---|---|---|
| S1 | Claude registration | A user-started Claude session becomes addressable for the correct disposable repository without manually entering its ID |
| S2 | Codex registration | A user-started Codex session becomes addressable for the correct disposable repository without manually entering its ID |
| S3 | Automatic routing | Conductor selects a suitable available session from a bounded job assessment |
| S4 | Directed routing | “Ask Codex” and “ask Claude” reach the intended provider without the person knowing an ID |
| S5 | Model-ready job | The chosen model and effort have a recorded rationale, prompt metadata, local guidance version, and complete obligation coverage |
| S6 | Round trip | The remote session executes and its result returns without manual copying of an ID, prompt, or answer |
| S7 | Isolation | A session registered to another disposable repository cannot receive the job |
| S8 | Staleness | A stale or unavailable session is refused rather than treated as live |
| S9 | Privacy | The routing state contains no credential, secret, or conversation body |
| S10 | Lightweight operation | Setup, normal use, failure recovery, and removal are documented and demonstrated without Kerd starting either provider |

## Completion

Stop when a working prototype demonstrates S1 through S10 and an independent
reviewer accepts the evidence. A design alone does not complete this trial.

## Guardrails

- Use disposable repositories; do not alter live Kerd behavior.
- The person starts every Claude or Codex session.
- Do not infer authority from registration.
- Do not send work outside the repository and provider limits approved in Shape.
- Do not store tokens, credentials, or conversation transcripts in routing state.
- Do not claim model or effort detection when the provider does not expose it.
- Do not choose an underpowered model to reduce cost.
