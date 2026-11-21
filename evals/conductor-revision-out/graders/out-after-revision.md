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
Find the FIRST Skill call in the trace that starts Switch Out. PASS if a successful
change to the brief (event 1) comes before that first Out start. FAIL if the brief was
never successfully changed, if every change to it failed or errored, if Out was never
started through the Skill tool, or if any Out start (the first or any other) comes
before the first successful change to the brief. A Skill call that starts some other
skill or action (for example switch in) is not an Out start.
