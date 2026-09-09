# Clear, safe labels in a pickup preview

Improve the supplied preview without changing its packet format or other behavior.
People must distinguish a literal backslash-u label from an actual escaped control
character. Non-BMP controls must use valid eight-digit `\U` notation; BMP controls
use four-digit `\u` notation. Keep normal readable Unicode readable.

Deliver only changes to pickup_preview.py, test_pickup_preview.py and USAGE.md.
M1: unambiguous literal-backslash versus control output, including non-BMP controls.
M2: existing privacy, validation and CLI behavior remains covered and passing.
M3: focused new tests and usage explain the actual escaping convention.

Source does the implementation and pauses BEFORE adding tests or updating usage.
Destination completes those and corrects supported issues. This deliberate split
exercises a useful unfinished handoff, not a claim about natural context pressure.
Controller alone writes place.json and performs Git operations. Do not modify
agreement.md, example.json, place.json or .gitignore. No network, Git writes,
background work, delegation, native history or files outside this disposable repo.

Return JSON: status continue/review/blocked, next_action, memory, cumulative
evidence (relative files), failures (preserve supplied counts), pending_jobs.
Review means ready for assessment, not accepted. No fabricated test evidence.
The reply must be valid JSON: literal backslashes in string values need JSON
escaping. Prefer plain-language descriptions of escaping in the saved memory.
