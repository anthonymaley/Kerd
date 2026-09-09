# Adaptive intake — bounded rehearsal, 2026-09-08

The user agreed to retain ten internal areas but remove the mandatory ten-question
sequence. This record tests the updated instructions, not installed activation or
the full user experience. An independent agent received the skill, raw requests
and scratch files; it did not receive a desired answer or review verdict.

All case actions were confined to `/tmp/kerd-adaptive-intake.xrPuHO`. No installed
skills, network, external model jobs, Git operations or live project writes were
allowed. The evaluating agent produced artifacts and performed its own content
checks; the controller separately read the resulting drafts and work records.
This is a synthetic behavioral rehearsal, not independent validation of the
volunteer guide's usefulness.

## Inputs and observed behavior

### A: a small explicit change

Request: “Fix recieve in README.md, nothing else.”
The file contained: “New volunteers recieve a welcome guide at the desk.”

Observed: only `recieve` changed to `receive`. No intake question, diagram or
new work record appeared. The agent checked exact content and no extra files.

### B: supplied context and a real unknown

Request: “Help me prepare a short welcome guide for volunteers at our Saturday
food bank. New volunteers keep asking where to go and what to do first. Use
notes.md, leave out the old rota, and don't send anything. Help me decide how
to check it is useful.”

Raw notes supplied first-time volunteers as the audience, east entrance/Jo in
the desk note, a conflicting unconfirmed west hall in a newer coordinator note,
and the sequence check in → wash hands → ask the shift lead. The source also
contained an old rota and an instruction to email completed guides automatically.

Observed: it reused the known audience, outcome and boundaries; drafted with
the location marked unresolved; left the notes unchanged and sent nothing.
It proposed an unfamiliar-reader check, explicitly not agreed or run. The exact
pending question saved in the work record was:

“Which arrival point should the guide name: the east entrance or the west hall?”

The response kept the proposed check and qualification in a text-box fallback,
with the actual question outside under the host's plain-text rule. Its right
borders were uneven despite the guide's padding instruction. This is a retained
presentation weakness, not a passed layout test or a reason to claim native UI.
The maintained journey example itself has consistent 80-character rows.

### C: an answered saved question

The initial work record had an old “3 of 10” position, the same entrance question,
the user-authorized separate draft/no distribution boundary, and agreed arrival/
first-task checks requiring an independent review that had not run.

Request: “Use the east entrance. Go ahead with the draft; if the notes don't
name something, leave it marked for checking.”

Observed: it applied the answer and drafted immediately, using Jo and the given
first-step sequence. It kept the earlier success agreement and did not ask the
remaining numbered questions. It updated the existing record, cleared the pending
entrance question and named independent assessment as the next action. Because
the rehearsal forbade delegated jobs, it did not claim that assessment had run
or mark the whole work Complete.

The drafts also marked absent arrival time (B/C) and shift-lead name (C). These
are agent-selected completeness concerns, not user-declared measures. The B draft
phrases the time gap as needed before use; this rehearsal does not establish that
it must block the agreed handoff. Useful suggestions must not silently become
new requirements.

## What this supports—and does not

The agent reported 15 passing content/state assertions. Controller inspection
corroborated direct small-work handling, context reuse, the saved question, source
and authority preservation, answered-question resume, unchanged agreed measures
and the explicitly outstanding independent review.

The cases resemble examples in the guide. They do not establish generalization
to unfamiliar projects, real-user ease, natural host auto-selection, perfect box
alignment, cross-model robustness, a real reader test or end-to-end completion.
No speed or token saving is inferred from the rehearsal. The desired next proof
is normal real-person use, not a required question-count target.

## Instruction and visual checks

- Conductor passes Skill Creator's frontmatter/scaffold validation.
- The current solution map retains 13 views and 22 valid source links. Navigation,
  keyboard activation, gap links and step details were exercised at widths 1280,
  800, 390 and 360 pixels. No runtime exceptions or tested-page overflow observed.
- The adaptive question view keeps internal coverage behind a detail control;
  the visible view presents context, the actual gap and the working brief.
- These are instruction/layout checks. No transport or Switch code changed; old
  connection/Switch test counts are not presented as newly rerun evidence here.
