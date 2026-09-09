# Switch To entry and exact pickup

2026-09-07. This slice improves normal skill routing and the destination command.
It does **not** connect an ordinary interactive skill invocation to a live source
controller, exit an existing user host, or complete an end-to-end device handoff.

## Executable correction

The earlier managed destination check compared the returned commit after calling
prepare. A newer remote could therefore advance the checkout before the mismatch
was reported. Strengthening the existing test reproduced that failure: an error
was raised, but HEAD had changed.

The shared pickup/prepare helper now accepts an optional exact Git revision;
the CLI exposes it as `--commit`. It compares the fetched branch revision before
fast-forwarding and merges the checked commit, not a later replacement FETCH_HEAD.
ManagedTo supplies its verified saved revision automatically. Ordinary latest-state
In retains its existing behavior when no exact revision is supplied.

Wrong revision: no working-file or HEAD update and no record reported restored.
Git fetch metadata can change; this is not claimed as a write-free network check.
No reset, force checkout, new fingerprint, approval record, CI or hook was added.

Seven new regressions cover exact success, mismatch without record loading or
checkout update, local mismatch, invalid commit expressions, CLI invocation,
changed FETCH_HEAD and edits during record reading. The strengthened ManagedTo
regression verifies its destination stays unchanged. The first test for replacing
FETCH_HEAD used an unsupported pseudoref update; corrected to a real second local
fetch, which exercises the intended race without modifying product behavior.

Final verification: all 170 Switch tests pass in both the pack and isolated
candidate mirror; both skill structure validations pass. The updated process
view was rendered and visually inspected at desktop and narrow widths. Live
Seinn and installed Kerd remain unchanged; the user's pre-existing TODO edit
was preserved. No root repository commit or push was performed.

## Independent skill behavior

Three fresh Codex evaluators received the candidate skill and separate disposable
scenarios, not the expected verdicts. No installed skills, network or real devices
were involved. [Fixture setup](prepare.py) is reproducible in an empty directory.
Observed folder: `/tmp/kerd-to-entry.WNCzX5`.

| Scenario | Observed action | Controller check |
|---|---|---|
| Reconnect to the same SSH/tmux session | Explained same-session continuation; no Git, edits, session launch or exit | Original HEAD and unsaved draft preserved |
| Ordinary interactive source; no host-exit control | Updated the precise work record, committed/pushed only its assigned files to the local bare origin, reported release pending | Clean source; local/remote both 7186a201a29df12157dc2dbfce597b1705aeba5b; no speaker notes or destination work |
| Destination given an exact handoff revision | Used candidate prepare; newer remote refused; no continuation | HEAD stayed 893aa31d5eea6786a536860a64a5a995beacabea, clean files; remote was b0b4f62a0a1f9de2a9eb99c206a6decfc246ba0f |

The destination evaluator initially omitted the global `--project` argument,
corrected that invocation and then encountered the intended revision refusal.
The guide now includes a complete command shape. The interactive evaluator's
portable instruction was accurate but verbose and quote-formatted; the guide now
asks for a compact summary plus a copyable plain-text block. These final presentation
clarifications have not been represented as another independent live replay.

The fixture's supplied session/connection facts are simulated inputs, not verified
Studio/laptop lifecycle evidence. Human source-exit confirmation in the fallback
is not automatic To support. The small Python controller still needs a real
connection from the normal Conductor/Switch call; a saved marker or PID cannot
reconstruct its live owner object. That is the next integration work, not something
these routing results satisfy.
