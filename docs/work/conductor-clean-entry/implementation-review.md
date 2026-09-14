# Candidate implementation review

Shareable request, not private transport framing. Established Claude partner,
existing model and effort retained. Opus 5/shared Claude profile as in review.md.

<objective>
Review the completed local clean-entry changes. Anthony also reinforced that
Conductor should not perform all substantial work itself: useful independent
jobs must be assigned, not merely considered, with justified inline exceptions.
Codex is the sole editor and will hold these files stable during your review.
No commit, push, release, install, binding change or new job from you.
</objective>

<sources>
git diff -- README.md skills/switch/SKILL.md skills/switch/references/in-out.md
skills/conductor/SKILL.md skills/conductor/references/execution.md
skills/conductor/references/journey.md skills/conductor/references/understanding.md
Also docs/work/conductor-clean-entry/{work.md,scenarios.md}.
Original dumps remain the baseline; your native transcript additions in the work
record are attributed as your reports, not Codex's independent verifications.
</sources>

<review>
Check the moved arrival rules for lost meaning/contradictory callers, direct and
redirected entry (workflow approval versus operations), practical delegation at
research/diagnosis entry, and preservation of managed ownership/continuation.
Your requested entry instruction is carried in Switch's actual invocation
example, not only in Conductor. TEAM must come from Agent, not project history;
legacy recorded collaboration is not being called fictitious.
Conductor can make bounded local orientation reads when the stage is not known,
but an already-scoped approval gets the entry frame before substantive tool calls.
Do not require a guessed stage/split before the necessary local orientation.
Give consequential findings with path/line and a minimal correction. Distinguish
rules from observed compliance; assess the scenario boundaries without claiming
live operational replay. Source/renderer tests don't prove model behavior.
Switch 379 tests pass. Release/audit gates clean apart from existing trace gap;
version remains 0.123.0 because this is unreleased, not a release-ready claim.
</review>
