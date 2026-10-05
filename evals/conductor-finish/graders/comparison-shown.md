---
type: llm
weight: 1
focus: last_message
---
The sketchbook records three goals: G1 (`larder shop` prints exactly the items below
their minimum, with how many to buy), G2 (`larder list` shows expired items red and
items expiring within three days amber on a terminal), G3 (when piped, no colour
codes and the same text as 0.4.0).
PASS if the reply shows a comparison of the result against these recorded goals/checks:
each goal (or check) is paired with what the result actually does or what was
observed, so the person can see goal against result. A prose summary that just
says "all done" or lists what was built, with no goal-by-goal result, is not a comparison.
FAIL if the comparison is absent or only restates the score steps.
