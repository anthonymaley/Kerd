## E1/M1 disposition: **closed. No contradiction found in the supplied evidence.**

### What the controller executed (I ran nothing)

- 13 legacy tests via `check_legacy.py` against the new module and CLI — reported all passing.
- The current 19-test suite after the test/docs-only follow-ups — reported passing.

I did not execute either. Everything below is from reading.

### Checks I performed by reading

**1. Legacy suite shape matches the reported count.** `failed-save/output/test_pickup_preview.py` defines 10 `SummarizeTests` methods (`:39`–`:191`) and 3 `CliTests` methods (`:204`, `:214`, `:225`) = 13. Consistent with "13 tests passed".

**2. Assertion-by-assertion comparison — no legacy assertion was deleted, weakened, or altered.** Lines 1–179 of the current file are identical to legacy 1–179, including the full 12-case `bad_packets` list. The only four differences, all in the strengthening direction:

| Legacy | Current | Direction |
|---|---|---|
| `:181-184` battery runs through `summarize` only | `:181-185` loops `(summarize, summarize_json)` | stronger |
| `:195` `run_cli(self, path)` | `:284` `run_cli(self, path, *arguments)` | equivalent for zero args (`:286` builds the same argv) |
| `:204-212` `test_cli_success` | `:293-304` same 6 assertions, preceded by an explicit `--format text` ≡ default equality check (`:295-297`) | stronger, nothing removed |
| `:220`/`:228` `assertNotEqual(returncode, 0)` | `:342`/`:351` `assertEqual(returncode, 2)`, each looped over both formats | strictly stronger (2 ≠ 0 entails the legacy assertion) |

This is the check E1 was blocking on. The current suite contains every legacy assertion verbatim or in a stronger form, so M1's "existing tests remain passing" is not resting on a rewritten suite.

**3. The loader does not make the 13-test pass vacuous.** `check_legacy.py:13` inserts the artifact root on `sys.path` *before* `exec_module` at `:17`, so legacy `:12`'s `from pickup_preview import summarize` binds the new module. `:19` rebinds `module.ROOT`/`module.PROGRAM`; both are read as module globals at call time (`run_cli` at legacy `:197`, `test_cli_success` at `:205`), so the rebinding takes effect and the subprocess runs the new `pickup_preview.py` with no `--format` argument — exactly the default-text route M1 covers. The module executes under the name `unchanged_legacy_tests`, so legacy `:234`'s `__main__` guard does not fire a second in-process run. `:14`'s `parents[1] / "failed-save/output/..."` resolves to the same file I read.

**4. "Product code did not change" holds.** I re-read `pickup_preview.py` (184 lines) and compared against the copy I reviewed in request 1 — identical, including `summarize_json` at `:149-152` and `_utf8_size` at `:55-59`. I read this file outside the named set because the legacy-run result only transfers to the artifact under review if the module is unchanged; that was the one supplied claim I could not check any other way.

**5. Follow-up claims map to real lines.** Both-format malformed input and missing file: `:339-345`, `:348-354`, plus the library battery at `:182`. Explicit text route: `:295-297`. Revision round trip: `:227`, `:243`. Tested-Python wording: `USAGE.md:5-6` now states 3.14 was tested and the minimum-version runtime was not exercised. Metadata-only semantics: `USAGE.md:69-70`. Lone-surrogate scope: `USAGE.md:52-55`, which describes the behavior I found by reading — labels preserved as escapes, content required to encode, no cross-parser guarantee.

### Two independent lines agree

The legacy run shows the new artifact satisfies the old assertions; the textual comparison shows the current suite still carries those assertions. Either alone would leave a hole (a passing legacy run says nothing about whether the shipped suite kept them; a textual match says nothing about whether they still pass). Together they close M1.

### Residual limits

- I executed nothing; both pass results remain controller-reported.
- The legacy CLI tests read `ROOT / "example.json"` from the artifact root. Its being unmodified comes from the session-start git snapshot, not a live check I ran.
- `test_booleans_must_be_actual_booleans` (`:187-192`) is still `summarize`-only — unchanged from legacy, so not a weakening, and it exercises the same shared validator.
- F1 is disclosed rather than fixed, which is the correct disposition given the no-widening constraint; the 3.10 floor is likewise now disclosed as untested rather than asserted.

Files read: the two supplied paths, plus current `test_pickup_preview.py`, `USAGE.md` and `pickup_preview.py`.
