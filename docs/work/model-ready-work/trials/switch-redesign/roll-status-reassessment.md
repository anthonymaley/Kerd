# Independent Claude reassessment — 2026-09-07

Requested and observed model: claude-opus-5; requested effort high. Read-only review.
Controller separately ran all 13 tests successfully. The assessment below is
artifact inspection, not reviewer-executed tests. The remaining stdout pipe/encoding
suggestion is outside the agreed scope and is not silently claimed fixed.

## Verdict per measure

**M1 — read-only, Git-resolved paths: met.**
`roll_status.py:52-70` runs exactly one external command shape, `git -C <project> rev-parse <option>`, with `stdin=DEVNULL` and `check=False`; a repo-wide grep for `write|open(|mkdir|remove|unlink|rename|Popen|shutil` in the module returns only `subprocess.run` at :54. There is no filesystem write path in the module at all, so "never writes a fallback record" holds structurally, not just by test. Root and private dir both come from Git (`--show-toplevel`, `--absolute-git-dir`, :73-77), so clones and linked worktrees resolve identically. Coverage: `test_roll_status.py:79-92` (clone-style `.git` dir, invoked from a nested subdirectory, byte-snapshot equality) and `:94-114` (linked worktree, asserts `.git` is a *file* at :103 and writes the fixture into the worktree's private dir at :104-105, snapshot over the whole base at :106/:114).

**M2 — current state and next action: met.**
All seven required states are present with friendly text (`:17-25`); `review` is labelled "awaiting independent assessment (not accepted)" (:21). Unknown current status, non-string status, missing/empty `next_action`, non-object record, and unparseable JSON all raise `StatusError` → stderr + exit 1 (`:98-107`, `:185-196`). Nothing in the module derives state from file counts or command success. `test_roll_status.py:116-132` covers all seven; `:249-255` confirms `status: "complete"` is still nonzero and does not print "passed".

**M3 — history summary, post-correction: met.**
`history_lines` (:139-161) reports `len(history)`, last returned status, and trigger observation. The tolerance change is implemented at :146: `shown_last = last_status if last_status in KNOWN_STATES else "unknown"` — an unfamiliar string maps to the literal `"unknown"` and the raw string is never printed. Type strictness is retained at :120-124 (non-string, non-null `status` still errors) and :130-134 (`context_readings` accepts `None` or list, rejects anything else). `context_trigger` remains `None`-or-dict only (:125-129). Regression tests: `:185-195` asserts exit 0, a valid current panel, `Last returned status: unknown`, **and** `assertNotIn("future-runtime-status", ...)`; `:197-214` asserts `context_readings: null` yields exit 0 with `observed: no`. The negative side is still pinned at `:270-276` (`context_readings: {}` and `status: ["continue"]` both error).

**M4 — safe output: met.**
Two-stage sanitisation at `:39-49`: the regex (:29-32) strips whole CSI/OSC/two-char escapes, then every remaining Unicode `C*`/`Zl`/`Zp` character becomes a space. All 14 `StatusError` messages (grep above) are constant literals — no record content, path, or exception text is interpolated into stderr, so private error fields cannot leak through the failure path either. Output is a text panel, not a JSON dump (:164-174), with the "does not mean the work passed" line at :172. Exit 0 only on a fully validated known state.

**M5 — tests and USAGE: met.**
13 test methods, all fixtures under `tempfile.TemporaryDirectory` (:43-52), invoked exactly as the agreement documents (`USAGE.md:32-36`). Negative cases (:240-295), untouched-data snapshots (:92, :114, :247), native-ID/private-error non-leakage (:161-162), and honest review/unknown states are all present. `USAGE.md:18-21` was updated to describe the two new tolerances without overclaiming.

`★ Insight ─────────────────────────────────────`
- The sentinel in `history_lines:148` (`item.get("context_trigger", "missing")`) is safe *only because* `validate_record:125-129` rejects string `context_trigger`. A record can never contain the literal `"missing"` in that slot, so "absent" and "recorded as the word missing" can't be confused. That's a validation-enforced invariant, and it's the kind of coupling worth a comment — it breaks silently if the type check is ever loosened.
- The tolerance change is safe against injection precisely because it maps unfamiliar input to a *program literal* rather than echoing it. Had `:146` printed `last_status` directly, the new leniency would have opened an unsanitised saved-string path to stdout, since `safe_text` is not applied there. The test at `:195` locks that in.
`─────────────────────────────────────────────────`

## Blocking findings

None. I found no supported blocking defect, and no regression from either correction.

## Non-blocking observation (one)

`roll_status.py:195` — `print(panel)` sits outside the `try`. A `BrokenPipeError` (e.g. `roll_status.py --project . | head -1`) or a `UnicodeEncodeError` (non-ASCII repo path under an ASCII stdout encoding) would emit a traceback. This is outside M4's stated scope, which covers "malformed input or read/Git errors", and the panel content itself is already control-safe — so I am not raising it as a failure. Minimal correction if the controller wants it closed: move `print(panel)` inside the existing `try` with an added `except OSError` returning 1. I did not make this change; authority here is read-only.

## Limitations

- I did not execute `python3 -m unittest -v test_roll_status.py`. My M5 verdict is an inspection of the assertions' *adequacy and correctness*, not evidence that they pass; the controller's run is the empirical check. Per the provisional-tagging default, treat M1–M5 above as "reviewed against artifacts, pending the controller's test execution".
- I did not read this trial's `.git/roll` or `.git/cross-llm`, per the agreement and this request's constraints; I read only the four deliverable-related files plus `place.json`/`recovery-place.json`, which were supplied as context.
- Runtime claims I could not verify independently — that live history emits only `continue`/`review`/`blocked`, and that the bounded route emits `context_readings: null` — are taken from the controller's statement. My review confirms the code and tests match *those* stated facts; it does not confirm the facts themselves.
- Git-version behaviour of `--absolute-git-dir` (added in Git 2.13) is from training data and unverified here; no doc fetch was permitted.

Files reviewed: `[isolated project]/agreement.md`, `roll_status.py`, `test_roll_status.py`, `USAGE.md`, `place.json`, `recovery-place.json`.
