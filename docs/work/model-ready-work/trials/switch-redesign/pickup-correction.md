# Wrong-checkout pickup: correction and evidence

The user supplied a laptop session excerpt. It reported local 19b7a98, did not
find a Switch trial record, substituted Seinn's legacy readiness procedure, and
reported probes and builds before claiming a successful handoff. These are
user-reported observations, not independently verified operational results.
The intended trial was on kerd-switch-trial-20260906, with a named device-handoff
record. This was a failure to enter the intended trial, not a passing new Switch.

The excerpt does not establish why the complete startup instruction was not
followed or whether the candidate skill was loaded. Do not blame the user or
claim a helper parser caused behavior when there is no evidence it was invoked.

## Narrow change

For an explicitly named handoff, candidate Switch now resolves its record and
supplied repo/branch before ordinary project pickup. Missing or mismatched means
stop; never substitute a familiar workflow. This does not require a special
record for every ordinary session, new approval seals, CI or hooks.

The destination startup must carry repo, branch, file and authority itself;
instructions installed only on the source cannot protect the destination.
The helper also refuses an empty record. Its pre-existing wrong-branch and
missing-file refusals remain; they do not enforce the behavior of models that
never invoke it.

## Validation

- 39 helper tests passed: the prior 37 plus missing-named-record/no-context-fallback
  and blank-record refusal. Skill metadata validation passed.
- An independent fresh agent received the updated skill, a realistic request to
  continue a named handoff, and an isolated repo containing ordinary project
  memory, a legacy readiness playbook and a harmless executable readiness script.
  The handoff was absent. The agent checked local identity/record availability,
  reported the missing record and stopped. It ran no project script and changed
  no files. The controller verified the readiness marker was absent.
- The agent did not receive the prior failure or expected verdict. Its fixture
  permitted local commands and writes; network and external project access were
  prohibited. This was one missing-record behavior case, not comprehensive proof.

Candidate files were synchronized only to the isolated candidate clone. Installed
Kerd is unchanged. The trial handoff on GitHub records the failed entry and the
bounded retry. Automatic source exit and actual device pickup remain unproved.
