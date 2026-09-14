# Urgent-risk correction: final release review

Established Claude partner; retain native model and effort. Applicable local
profile: Opus 5, 2026-09; exact effort unverified. This is a shareable brief;
Agent retains the full framed request privately.

<objective>
Anthony answered “yes” to Codex's explicit “Shall I release this fix?” after
the two local reviews. Codex owns the sole 0.122.1 publication. Please review
the final release surfaces read-only; do not release in parallel.
</objective>

<sources>
The current diff of .claude-plugin/plugin.json, .claude-plugin/marketplace.json,
README.md, skills/switch/SKILL.md and docs/work/switch-arrival-team/work.md.
The Out guide and both earlier urgent-risk briefs remain in this diff; the
implementation you already cleared is unchanged. Patch version 0.122.1 fixes
the intended urgent-risk retention, with no new schema, runtime or In change.
</sources>

<review>
Check the three version fields, release-note accuracy and scope, trigger
description and work-record status. Report consequential remaining problems
with a path and minimal correction, or state ready for release subject to the
test/CI results. No need to re-read consumer transcripts or repeat the fixture.
Codex is running the full Switch, Agent, Conductor, packaging and hook suites
and the entry-gate checks, and will append their actual results before saving.
</review>

<boundaries>
Read-only: no edits, staging, commits, pushes, installs, bindings, consumer
checks or new jobs. Installed plugins and the local root patch stay untouched.
The queued-human-message exception is not part of this correction. Reply once;
Codex retrieves the complete response through Agent.
</boundaries>
