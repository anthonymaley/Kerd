---
type: llm
weight: 1
focus: trace
---
The trace is one turn of a session asked to revise launch-brief.md with the product
team's answers. Check the order of two events:
1. A successful change to launch-brief.md: an Edit or Write tool call on that file
   (whatever the path's spelling, absolute or relative, and whatever the order of the
   call's fields) whose tool result is not an error and shows the file was changed.
2. A Skill tool call that starts Switch Out: the skill is switch (kerd:switch) and its
   arguments start Out ("out"), made by the session itself, not in reply to the person
   asking for it.
PASS if event 1 happens and is followed later in the trace by event 2. FAIL if the
brief was never successfully changed, if every change to it failed or errored, if Out
was never started through the Skill tool, if Out started before the brief was changed,
or if the Skill call starts some other skill or action (for example switch in).
