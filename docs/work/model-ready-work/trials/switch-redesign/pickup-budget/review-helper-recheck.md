## Recheck — prepared pickup corrections

**Resolved.**

1. **UTF-8** — `source_text()` (`handoff.py:81-84`) opens with `encoding="utf-8"`; used at `:102`, `:150`, `:158`. Locale no longer decides. Invalid bytes raise `UnicodeDecodeError`, a `ValueError` subclass, so `main:200` catches it and returns blocked/exit 2 instead of mojibake. `bytes` at `:106` now encodes the same UTF-8 it decoded.

2. **Line endings** — `newline=""` disables universal-newline translation, so CRLF reaches `named_section`, whose `rstrip("\r\n")` and `splitlines(keepends=True)` already handled it. `test_handoff.py:251` exercises the full pipeline, so the preservation claim at `:311` is now backed end-to-end rather than only at the function boundary.

3. **Tracked sources** — `git ls-files --error-unmatch` at `:145`, `:149`, `:156` covers record, `--file` and `--section` alike; `test_handoff.py:266` checks all three against a gitignored file with a clean tree.

4. **Concurrency** — `test_handoff.py:278` patches `named_section` to dirty the tree mid-read and asserts "Project changed"; the guard at `:161` is exercised. Its second disjunct (`rev-parse HEAD != loaded["commit"]`) remains untested — the status branch fires first.

**One narrow new gap (low).** `ls-files --error-unmatch -- <path>` treats the path as a pathspec, so glob characters in a filename can match a *different* tracked file and pass the tracked check. Reachable only for a gitignored file whose name contains `*`, `?` or `[`; untracked non-ignored files are already stopped by the clean check. A `:(literal)` prefix would close it.

**Limits.** Static reading only; I ran nothing. The 143 passes and the identical before/after Seinn packet are the controller's evidence, not mine. Scope held to these four corrections.

## Controller disposition

The literal-path finding was accepted and corrected using Git's literal pathspec. A new test rejects an ignored question-mark filename that could otherwise match a different tracked file, then verifies the same literal name works when actually tracked. A second new test exercises a clean concurrent commit, covering the HEAD-change branch. All 145 Switch tests pass after these corrections. This final narrow correction is controller-tested, not claimed as a further peer review.

