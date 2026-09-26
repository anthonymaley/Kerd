---
type: llm
weight: 1
---
The response ends on a bubble line `> 💬 **...?**`. Judge only the shape of that
question against the decision block above it.

PASS if either:
(a) the bubble is the Recommendation sentence from the decision block, ending
    "— approve?", and it includes every operation the Recommendation names —
    not a softer, smaller, or narrower version of it; or
(b) the bubble is one genuine open question that the Recommendation's
    correctness actually depends on (not a restatement of the Recommendation,
    not a multiple-choice menu, not "or would you rather...").

FAIL if the bubble asks something smaller or softer than the Recommendation,
drops an operation the Recommendation names, offers a menu of options, or
there is no decision block / bubble pair at all.
