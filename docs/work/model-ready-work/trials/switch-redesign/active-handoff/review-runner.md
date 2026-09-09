## Active-handoff rehearsal review

**Read:** `active-handoff/run.py`, `method.md`, `test_run.py`; adapter `skills/switch/scripts/{codex_roll,handoff,roll}.py` and `skills/conductor/scripts/ask.py`. No execution.

### Blockers

**1. Observer is stricter than the adapter on optional event fields (run.py:79, 83).** It requires exact `turnId`/`threadId` on `item/completed` and `turn/completed`, and depends on the `turn/started` notification to set `self.turn`/`self.thread`. `codex_roll.py:258-261` deliberately tolerates absent ids (`not in {None, sid}`) and can establish the turn from the `turn/start` response alone. If the host omits those fields, the observer raises *inside* `receive`, the exception propagates into `_run`'s `except BaseException`, and cleanup stops the worker — an optional protocol field becomes the disclosed source-loss path, after the work exists but before any save.

**2. Nothing prevents or detects a source-worker commit.** `publish` guards the index and working tree, then takes `rev-parse HEAD` as-is and pushes `HEAD:refs/heads/<branch>` (handoff.py:58-73). The source sandbox is `workspace-write`; a worker `git commit` is pushed and restored by the destination. `saved["commit"]`'s parent is never compared to the controller's initial commit, so method.md:22 ("the controller alone creates the fixture, commits named files, pushes") is not enforced by this driver.

**3. Saved-place integrity is unchecked after the destination run.** `Roller` compares `place.read_bytes() != place_before` (roll.py:266). run.py:127 re-reads only `agreement.md`/`example.json`; `after` is validated against the in-memory `before`. A destination edit of `handoff.json` — which its own prompt forbids (run.py:116) — is undetected.

**4. Reply-count rules diverge.** run.py:84 demands exactly one non-commentary message; codex_roll.py:302 permits a steer-corrected second. With the default 0.65 fraction and no test trigger, a context-triggered steer aborts the source turn into the same loss path. Symmetrically, run.py:124 validates only `dst["reply"]`, where Roller chains every `checkpoint_candidates` entry — an intermediate candidate erasing evidence is never examined.

**5. Late-abort surface.** Any stray file the source leaves trips `publish`'s unassigned-changes guard (handoff.py:60-64) at the same post-work point; no `.gitignore` is established.

### Limits

I ran nothing. The five fixtures exercise only `require_release` and always patch `roll.group_gone`, so the real liveness check, the observer, the save/shutdown ordering and the preservation checks have no coverage here — the fixtures cannot support any ordering conclusion. I make no claim about the running model-worker trial. I did not fetch the App Server doc cited at method.md:42 (no network); the retained-source gap is disclosed there and I treat it as open, not passing.

## Controller disposition

The live run used run-observed.py (preserved verbatim), not the later corrected run.py. It received the required event IDs and exactly one final candidate per worker, with no context trigger. Its observed ordering is evidence for that supported happy path, not all event variants.

Accepted and corrected for future runs: detect worker Git commits, compare the destination saved-place bytes, validate every destination checkpoint candidate, and ignore generated Python cache files in the disposable fixture. Eight controller-run admission/preservation tests pass. These corrections have not been claimed as a new live replay.

Retained as explicit limits: missing IDs or multiple source replies conservatively abort this narrow observer; the actual adapter has broader compatibility. Any abort still reaches the documented cleanup/retained-source gap. Unexpected source files continue to refuse rather than being silently included. A production lifecycle API must address these paths before automatic To is accepted.

Post-run checks of the observed run: destination's original clone reflog is 243bd9e7a844595fc33337fd31c91db799f43729; the saved source revision has exactly that parent, and source history contains only initialization and the controller's handoff commit. Destination HEAD still equals the saved revision. Git diff of handoff.json, agreement.md and example.json against HEAD is empty. These are retrospective controller checks, not checks performed by the original driver.

