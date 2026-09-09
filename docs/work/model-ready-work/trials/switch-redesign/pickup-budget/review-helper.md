## Prepared-pickup review — findings

**Files read (read-only):**
- `.../switch/scripts/handoff.py`
- `.../switch/scripts/tests/test_handoff.py`
- `.../switch/references/in-out.md`

### Supported defects

**1. Locale-dependent decoding of "raw" sources — medium.** `handoff.py:96`, `:141`, `:149` use `Path.read_text()` with no `encoding=`, so decoding follows the process locale. Under a non-UTF-8 single-byte locale, UTF-8 records decode without error into mojibake and are handed to the fresh reader labelled as the raw source — silent corruption, not a refusal. The same function then does `len(content.encode())` (`handoff.py:100`), which is UTF-8, so `bytes` and the decode disagree whenever they differ. The test at `test_handoff.py:209` writes `café` via `write_text()`, so both sides share the same locale and the mismatch cannot surface in the suite. Countermeasure: pass `encoding="utf-8"` on every read and on the byte count; I expect the CLI to then fail loudly on genuinely non-UTF-8 records instead of corrupting them.

**2. CRLF is normalized before it reaches `named_section` — low.** `read_text()` applies universal newlines, so a CRLF file arrives as LF. `test_section_ends_at_parent_heading_and_preserves_line_endings` (`test_handoff.py:269-272`) feeds CRLF directly to `named_section` and asserts preservation — a property the `prepare()` pipeline cannot deliver, since no caller-reachable path passes CRLF through. Either read with `newline=""` or drop the preservation claim; today the test asserts more than the feature does.

**3. The concurrency guard is untested — medium (coverage, not behavior).** `handoff.py:150-153` is the newest and subtlest logic: re-check branch, cleanliness and HEAD after reading sources. No test exercises it. `test_prepare_rejects_dirty_tree_wrong_branch_and_missing_extra_source` (`:246-248`) dirties the tree *before* `prepare()`, so the refusal comes from `pickup()`'s early check at `handoff.py:83`. The post-read guard has no confirming observation.

**4. Gitignored files pass as sources — low.** `relative_file` accepts any existing non-symlink file; untracked files are otherwise caught because `git status --porcelain` refuses them, but ignored files are invisible to that check. Such a file is packaged next to a commit hash under the note "Caller-selected saved records" (`handoff.py:156`) while existing at no commit.

No defects found in `named_section`'s fence/heading logic, the exactly-once rule, the `--section` argparse wiring, or the traversal/symlink reuse.

### Limits

Static reading only; I ran nothing. The 26 handoff and 139 Switch passes are the controller's, not mine — findings 1–2 are reasoned from the code, tested by neither of us. I did not review save/pickup for redesign, and treated the exact-ATX, fenced-exclusion parser scope as given.

## Controller disposition

All four findings accepted. Reads now specify UTF-8 and preserve line endings; prepared sources must be tracked. New tests exercise the real CRLF/UTF-8 pipeline, invalid decoding, ignored sources and a concurrent edit during source reading. The corrected helper emits an identical packet on the Seinn fixture. This is an optimistic changed-state check, not an atomic snapshot or security boundary.

