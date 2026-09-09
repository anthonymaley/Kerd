# Independent Claude review — clean replay

Requested and observed model: claude-opus-5; requested effort high. Read-only
artifact inspection on 2026-09-07. Controller separately executed all 13 tests
successfully. No blocking findings. This archived repeat-experiment output does
not replace the earlier independently reviewed status tool adopted in the skill.

## Verdict per measure

**M1 — Met.** `roll_status.py:45-70` resolves via `git rev-parse --show-toplevel` and `--absolute-git-dir`; the only subprocess invocation in the file is that `rev-parse` query (`roll_status.py:48`). No write path exists — no `open(...,"w")`, `mkdir`, or fallback record. Clone-style (`test_roll_status.py:83`, asserts `.git` is a dir) and worktree-style (`:98`, asserts `.git` is a file) are both covered, and `:110` snapshots mode/mtime_ns/sha256 across the repo.

**M2 — Met.** All seven states are present in `KNOWN_STATES` (`:16-24`) and exercised in `:146`. Review wording is "awaiting independent assessment, not accepted" (`:20`). Unknown/missing/invalid → `StatusError` → stderr + exit 1 (`:171-173`), with no completion inferred from file count or command success anywhere.

**M3 — Met.** `history_lines` (`:122-138`) prints count, last status, and trigger observation only. An unrecognized historical status collapses to `"unknown"` (`:128`) rather than being echoed — tested at `:173-181`. `saw_trigger`/`all_reported` (`:130-132`) correctly distinguishes `no` from `unknown` when the optional field is absent; `:183` covers that. `session_id`/`request_id` are never read; `:95-96` asserts non-leakage.

**M4 — Met.** `safe_text` (`:36-42`) strips CSI/OSC first, then maps remaining `Cc`/`Cf` to spaces — so a lone `\x1b`, `\x00`, and newline injection into the panel are all neutralized (`:192` confirms the intent). Type validation is explicit (`:90-119`). The broad `except Exception` (`:174`) plus `errors="strict"` decoding caught as `UnicodeError` (`:56`, `:78`) closes the traceback paths. Output is a text panel with the scoped-exit note (`:151`).

**M5 — Adequate as written.** Tests are stdlib-only, subprocess-isolated, and use `tempfile` repos exclusively; negative cases, untouched-data, leakage, and honest review/unknown states are all present. USAGE gives the exact invocation and states the read-only limits and the meaning of exit 0.

## Blocker

None supported by the code I read.

Two scoped, non-blocking observations:

1. `roll_status.py:67` uses `--absolute-git-dir` (Git ≥ 2.13). USAGE states no minimum Git version. Smallest correction: one sentence in `USAGE.md` noting the requirement. Not a measure failure.
2. `test_roll_status.py:110` verifies data-untouched only for the clone case; the worktree case has no equivalent snapshot. Smallest correction: call `self.snapshot(self.base)` around `run_status(worktree)` in `test_worktree_style_git_file_uses_private_worktree_git_dir`. Coverage nit, not an M1 gap.

## Limitations

I did not execute the suite, so every statement above is test *adequacy* by reading, not evidence that `python3 -m unittest -v test_roll_status.py` passes — that remains the controller's execution. I read only the four named files; I did not open `place.json`, other trial copies, or any `.git/roll` content. Git-version and platform-specific behavior (permission-denied reads, non-UTF-8 paths) is reasoned from the source, untested here.
