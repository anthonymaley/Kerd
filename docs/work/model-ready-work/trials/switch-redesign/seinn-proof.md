# Seinn: useful pickup and GitHub round trip

Status: selected restoration and Git transport tested locally; the supplied
laptop result also supports second-device memory restoration. Automatic source
exit, active-build transfer and measured low-context pickup remain unproved.

## What actually changed

The live Seinn checkout stayed clean at
19b7a98a778b88dedab52c91bd662e6ac4b7843d. An isolated clone and dedicated branch
`kerd-switch-trial-20260906` received only CONTEXT.md, TODO.md, their verbatim
archives and a changes record. No product code or dated session log was changed.
Original archives were compared byte-for-byte with live originals before publishing.

The helper committed those five named files as
ef4dc42f13630c76da2ad2c1eaf43509e210e862 and pushed to the dedicated GitHub branch.
It verified remote HEAD. A second clean clone fetched that branch from GitHub;
the pickup helper verified the expected branch, synchronized safely and loaded
the same current context. Both current CONTEXT and TODO compare byte-for-byte
between source and destination. Source exit explicitly remained false.

This exercised a real remote, but both clones were on this machine. It did not
transfer an active Conductor build: Seinn's saved state correctly says nothing
is in flight. Active continuation was separately exercised by the Roll fixture.
Do not combine those two results into a claim that an active build crossed devices.

## Memory result

The entry CONTEXT is now 7,156 bytes, versus 388,097 bytes before. That is a smaller
entrypoint, not a token count or a complete pickup cost. The historical context
is still reachable, unchanged. TODO is 27,964 bytes, versus 30,465 before.

Seven resolved or absorbed narratives left the active TODO: require-phone
duplicate, listener investigation, Docker trial, VAAPI fix, Docker permissions
proposal, browser-claim verification and the redundant sudo complaint. Applicable
lessons remain in current context or linked decisions. Both original files remain
recoverable in `docs/work/switch-trial/archive/` on the trial branch.

Independent source review found no unjustified removal. It requested corrections
to the old entitlement “in flight” label, an index of still-unresolved archived
questions, an overbroad journal-evidence prohibition and a source hash presented as
current. Those four corrections are included in the published trial.

## Selected fresh-reader test

A fresh Claude session received [these twelve questions](review-seinn-pickup.md),
without their answer key. Controller comparison with the source review found the
required facts and restrictions in all twelve answers: no active build; completed
rollout but no Build-exit ruling; notification obligation without sending authority;
unanswered TV behavior; discriminating playback evidence; migration fields still
open; no live probes; add_shares and privacy choices; settled product decisions;
wrong-target cause still unknown; and peer/dependency boundaries.

This is not a held-out completeness test: the author of the condensed memory had
seen the selected questions. The reader used five whole files (current CONTEXT,
TODO, latest daily log, Sherpa and the trial changes), not just the entrypoint.
It ran before the four final source-review corrections. Those corrections retain
the tested facts, but this is not a fresh-reader run on the exact final commit.

The reader appropriately declined to act outside trial authority, but ended with
an unnecessary question about the eventual notification. No user answer is needed
for this memory trial; it stays outside scope. Its minor claim about archive sizes
also conflated a section size with the TODO archive; source sizes above are the
controller's measurements, not that claim. Do not adopt the returned prose blindly.

Key Decisions and Operational State have not been comprehensively revalidated.
The source archive remains essential for future feature-specific retrieval. The
test checks selected restoration, not lossless memory for every possible task.

## Actual laptop pickup — result supplied 2026-09-07

The user supplied the completed retry from Anthony's MacBook Pro (Mac16,1),
reporting local execution rather than SSH to the Studio. The trial checkout was
/Users/anthonymaley/seinn-test, origin git@github.com:anthonymaley/seinn.git,
branch kerd-switch-trial-20260906, HEAD
2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83. It reported matching live remote HEAD
and a clean working tree including untracked-file inspection. That is the prepared
retry revision, unlike the first attempt at main's 19b7a98.

The returned position matches the saved handoff: rollout complete 4/4; last-sitting
build 339 and agent 2.3.1 observations, not new device probes; no active build;
Build-exit ruling still absent; the Krutho notification owed but not authorized
by this trial; and the TV failure/queue behavior awaiting the producer's choice.
The result retained operational restrictions and reported no readiness checks,
builds, source changes, deployments or external messages during pickup.

Assessment: successful bounded second-device memory restoration on the supplied
evidence. This controller did not inspect the laptop or the seven shell commands;
machine identity, exact reads and absence of side effects are reported evidence,
not independently observed telemetry. There was no active Seinn build to transfer.
The source controller session remained open. No automatic To pass is awarded.

Reported complete reads: device-handoff.md, CONTEXT.md, changes.md and .gitignore.
TODO was read selectively (Now/Owed and nearby rows), not in full. Neither the
historical context archive nor the daily log was needed for this bounded pickup.
The model explicitly left the 8,000-token / 5% target unassessed; no usable
input-token/context reading was supplied. Smaller retrieval alone is not a pass.

Setup caveat: the destination folder already contained hook-created .remember/,
so the model used init/fetch/checkout rather than a clone into an empty directory.
It initially asked an unnecessary question about excluding that folder, then
corrected its assertion after finding the folder's own ignore file. No exclusion
change was reported. This does not establish a clean, hook-free startup experience
or justify automatically hiding session-created files in future projects.

No repeat of this same read-only laptop check is needed. Further proof should
address the remaining measures, not repeat successful position restoration.

## Still needed

- Actual Switch-added input-token and usable-context measurements, including
  all necessary retrieval. The agreed 8,000-token / 5% target is unassessed.
- Supported source-session release/exit and destination ownership, with a genuine
  active-work handoff. Git save and local locks alone do not provide that behavior.
- Final user review before live installation or replacing Seinn main's memory.
