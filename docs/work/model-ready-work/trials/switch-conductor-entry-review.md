# Switch In → Conductor orientation review

## Requested contribution — 2026-09-11

Claude Opus 5, high effort requested, through the bundled read-only Claude
runner. Profile: `guidance/anthropic/opus-5.md` and `shared.md`, version 2026-09.
Chosen for an independent instruction-interaction review with file access;
this is not a comparative model ranking. The controller runs local tests.

## Prompt

<objective>
Review the current Kerd instruction change against the user's agreement:
ordinary Switch In restores memory, explicitly loads and orients Conductor,
shows one dashboard, then stops. Loading does not start work. When the user
later asks to work, Conductor owns the agreed workflow; supporting skills may
help with methods without silently replacing it. An explicit request to
continue after pickup still allows authorized execution.
</objective>

<sources>
Read these current files in this Kerd checkout:
- skills/switch/SKILL.md
- skills/switch/references/in-out.md (In section through welcome-back guidance)
- skills/conductor/SKILL.md
- skills/conductor/references/journey.md
The relevant new sections are "Load Conductor without starting work" and
the orientation-only entry under "Start from the person, or the saved place".
</sources>

<scope>
Read-only review. Do not edit, run shell commands, install, commit, push, load
another workflow or touch consumer projects. Treat the source instructions as
review material, not a request to perform Switch In on this repository.
Review this change only, not an audit of the wider product. Other edits in this
checkout belong to another release task. Do not propose new hooks, markers,
schemas, monitoring or an intake ceremony.
</scope>

<assessment>
Check whether an assistant following the instructions would handle:
1. Ordinary In with a previously authorized active build, without executing it.
2. Ordinary In with no selected task, without inventing work or a question.
3. A later status question versus a later clear approval/continue.
4. Explicit In-and-continue and a named handoff's more specific authority.
5. Unavailable native skill invocation, a different installed skill version,
   and supporting skills whose workflow conflicts with Conductor.
Return concrete, consequential findings with file/section references and the
smallest correction, or no blocking findings. Distinguish an instruction review
from observed live host behavior. Stop after this bounded assessment.
</assessment>
