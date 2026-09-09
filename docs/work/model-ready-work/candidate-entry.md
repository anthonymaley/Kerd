# Start here — use the current candidate

This is the isolated Conductor, Visuals and Switch candidate—not a replacement
for installed Kerd. Start it in the **project where the work belongs**. No CI,
custom hooks, plugin installation or new repository is needed just to try it.

The maintained candidate is the `skills/` directory beside this page, together
with its sibling `guidance/` directory. Use it directly; the separate candidate
clone is a checked mirror, not another source of instructions. Keep that relative
layout if copying the pack. Do not install the legacy plugin from the mirror.

A [portable three-skill bundle](packaging/START.md) is now prepared for controlled
adoption. Claude can load it for one session with `--plugin-dir`, without a global
install; Codex's documented fallback here is explicit file loading. The bundle's
README explains scope, remaining instruction conflicts and the way back. See
[current package evidence](consolidation.md#portable-package--2026-09-08).

For new work or to continue a saved package, open your project's session and paste:

```text
Read /Users/anthonymaley/development/product/kerd/docs/work/model-ready-work/skills/conductor/SKILL.md and use that candidate in this project. Begin, or continue the current saved work.
```

Fresh work uses the supplied description, or a light opener if none exists.
Conductor reuses project context, suggests a working brief and asks only important
gaps; the ten coverage areas are internal, not ten confirmation turns. Small,
clear authorized changes run directly. When the skill is available to a host,
natural requests such as “build an app” or “create a guide” can select it; the
candidate paste is the fallback until deliberate host discovery (including
Claude's session-local plugin route) is confirmed.
Existing work resumes its question or authorized
action. A completed work package stays complete; give a new outcome when you
want new work. The original session-routing-03 trial is already accepted.

You can say “ask Claude to review this” or “ask Codex for input.” The candidate
prepares and runs an appropriate bounded contribution when that route and
authority are available. Its bundled CLI connection uses already-authenticated
accounts, Python, Git and macOS/Linux support. Conductor checks the chosen route
and offers to set up missing tools with your approval; you complete provider
sign-in. It handles session IDs, requests and results, not you. It won't silently
install tools, change your chosen model, or pretend missing review evidence exists.
The connection creates workers and resumes its registered aliases; it does not
automatically connect to an already-open terminal you name.
Native delegation is another route when available and appropriate.
You do not need to choose the staff for every job. Conductor uses the local
[model suitability guide](guidance/model-choice.md), required tools and relevant
results, then briefly explains its model/effort choice. It preserves requested
models and the agreed quality; no provider gets a default preference and an
unknown capability stays unknown. This is evidence-led selection, not a proved
automatic ranking.
An ordinary standalone review or status request does not start the guided
interview. Question presentation follows the host's supported controls; where
textual numbered choices are forbidden, the candidate uses a simple confirmation
instead of displaying controls the host does not permit.

That path is this Studio's location, not a requirement for other machines. On a
different machine, substitute the local pack location. The work itself belongs
in your current project. You do not need to move a native conversation or copy
private session IDs.

## Diagrams without a setup chore

For diagrams, the bundled Visuals skill already includes a diagram-design
adaptation: no extra diagram install is needed. Full upstream diagram-design
and Archify are optional complementary tools. When useful or requested,
Visuals explains the benefit and offers approved setup, with the built-in view
as a fallback. [Tool sources and assessment](visual-tools-assessment.md).

## Save, resume or move the work


Explicitly load this pack's Switch, then state the action in ordinary language:

```text
Read /Users/anthonymaley/development/product/kerd/docs/work/model-ready-work/skills/switch/SKILL.md and save this session locally.
```

| Say what you need | What Switch does |
| --- | --- |
| Resume the saved work — In | Restores relevant memory and continues the saved authorized action. Synchronizes Git when requested/authorized. |
| Close this sitting — Out | Records work, tidies evidenced completions and prepares the next sitting; commits/pushes under the agreed Git authority. |
| Continue this work on my laptop — To | Saves the exact mid-work position to the agreed GitHub branch and supplies a named destination pickup. It is not full closeout. |
| Continue the build in fresh context — Roll | Preserves the agreement and actual progress across fresh managed workers, where the execution route supports it. |

A local-only save stays local. Failed synchronization is visible. To never claims
that a Git push started a remote model; you open the destination session. Roll
controls workers it owns, not any arbitrary terminal you already have open.
Your existing host permissions and instruction hierarchy still apply. If a legacy
project instruction conflicts, the candidate reports that conflict rather than
silently changing your setup.

## What is ready to try

Guided understanding, visual agreement, prepared Claude/Codex contributions,
independent review and continuation have been exercised in bounded trials. The
[Studio → laptop result](trials/switch-redesign/device-build/results.md) includes
returned artifacts and a corrected, independently reviewed result. The refreshed
conversation still needs a real-person end-to-end check; this is not a released
replacement for installed Kerd. [Current consolidation](consolidation.md).

[See the working loop](diagrams/working-loop.html) ·
[Read the real model-produced guide](trials/integrated-delivery/using-model-help.md) ·
[Evidence and limits](trials/integrated-delivery.md)

Live adoption and migration of other Kerd skills remain separate, unfinished work.
Trying these three skills does not change global instructions, hooks, CI, installed
Kerd or existing approvals. Existing project CI can be used as evidence; it is
not required to use the candidate.
