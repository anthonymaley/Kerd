# Independent Claude review after automatic Roll — 2026-09-07

Requested/observed model: claude-opus-5; requested effort high. Controller separately
ran all 13 tests successfully (2.580 seconds). This artifact set is archived trial
output, not a replacement for the earlier reviewed script adopted in the skill.
Final native-helper cleanup required controller assistance in this run; the real
mid-build fresh-worker transition did not. Neither is hidden by the quality verdict.

Conductor answer to the reviewer's question: actual roll.py appends history only
after successful provider cleanup and validated saved-state readback, not on start.
No user question is needed. Other suggestions do not block the agreed measures.

## Verdict

All four artifacts are present and, **by reading the code (not by executing it)**, the three deliverables satisfy M1–M5 as written. **No blocking findings.**

I did not run `roll_status.py` or the test suite; every claim below is static reasoning over the source. The controller's separate execution is what would promote this from "reads as correct" to "tested".

---

## Evidence per measure

**M1 — read-only, Git-resolved locations** — `roll_status.py:65-88` issues a single `git -C <project> rev-parse --show-toplevel --absolute-git-dir`, which resolves both the worktree root and the *actual* private dir in one read-only call. `--absolute-git-dir` is what makes the linked-worktree case work: it returns `<main>/.git/worktrees/<name>`, not the shared `.git`. The only filesystem access anywhere is `record_path.open("r")` (`:94`). No fetch/checkout/merge/stage/script-exec path exists. Covered by `test_roll_status.py:51` (`.git` directory) and `:60` (`.git` file — asserts `(worktree/".git").is_file()` at `:84` and `"worktrees" in str(private_record)` at `:89`).

**M2 — seven states, honest review, honest failure** — `KNOWN_STATES` (`:16-45`) covers all seven; `review` reads "awaiting independent assessment; it has not been accepted" (`:31`). `validate_current` (`:108-121`) rejects missing/non-string status, unknown status, and missing/empty/undisplayable `next_action`, each via `RecordError` → exit 2 (`:212-214`). There is no "complete"/"done" state and nothing derives state from file counts or from the command's own success. `test_roll_status.py:206` pins the important negative: a saved status of `"complete"` exits nonzero rather than being treated as success.

**M3 — history summary without leakage** — `history_summary` (`:124-177`) emits exactly three derived scalars: `len(history)`, a label looked up in `KNOWN_STATES`, and a Yes/No/Unknown. No entry field is ever printed. Absent `context_trigger` on any entry sets `context_known = False` → `"Unknown"` (`:145-146`, `:174-175`), which is the "label unknown rather than inventing" behaviour M3 asks for. Missing `history` key → `"Unknown (history not recorded)"` (`:127`). The quality disclaimer is in the panel itself (`:195`). Leakage is negatively tested at `test_roll_status.py:141-142` against synthetic `session_id` / `request_id` / `error` values, and `:153` asserts an unrecognised historical status string is not echoed.

**M4 — safe output** — `safe_text` (`:58-62`) strips CSI/OSC via regex, then removes *every* remaining Unicode category-`C` codepoint. That second pass is the real guarantee: an unmatched escape form (DCS `\x1bP…`, charset `\x1b(B`, single-byte C1 `\x9b`) still loses its `ESC`/C1 byte and degrades to inert literal text, and it also removes `Cf` bidi overrides and `Cs` lone surrogates that `json.load` can produce. Every dynamic string reaching stdout — `next_action` and the project path — passes through it; everything else is a hardcoded literal. All `RecordError` messages are fixed strings, so no `JSONDecodeError` text or private content reaches stderr, and git's own stderr is `DEVNULL`'d (`:79`). Exit 0 is reachable only through a fully successful `render`.

**M5 — tests and docs** — `python3 -m unittest -v test_roll_status.py` matches the file's location and shape; fixtures are `tempfile.TemporaryDirectory` + `git init` only, with synthetic values for all private fields. Negative cases: missing record, invalid JSON, unknown status, eight type-invalid records, non-Git directory. Data-untouched check at `:172-187` compares bytes + `st_mtime_ns` and asserts no fallback record. USAGE.md states invocation, both `.git` shapes, and the two limits that matter — exit 0 means "read, not passed" (`USAGE.md:20-22`) and identifiers/raw history are never shown (`:24-26`).

`★ Insight ─────────────────────────────────────`
- `render` builds the entire panel string *before* `main` prints it (`:180-197`, `:211-216`). That ordering is what makes a mid-render `RecordError` — e.g. a bad history entry discovered after the status line is composed — emit *no* partial panel. Validation that raises during formatting is only safe if formatting is separated from output.
- Layering a regex escape-stripper over a `unicodedata.category(c).startswith("C")` sweep is the right shape: the regex preserves readability for the common CSI/OSC case, the category sweep is the completeness backstop. A regex alone would have left `\x1bP` and `\x9b` live.
`─────────────────────────────────────────────────`

---

## Nonblocking suggestions

1. **`Completed workers` counts all history entries** (`:177`, `str(len(history))`). If the live ledger appends an entry when a worker *starts* rather than when it returns, the label overstates during `status: running`. I could not check — the agreement forbids reading this trial's real `.git/roll/run.json`.
2. **M1's "clone-style" case is exercised via `git init`, not `git clone`** (`test_roll_status.py:19`). Structurally identical (`.git` as a directory), so the substance is covered; only the literal wording differs.
3. **USAGE claims `--project` accepts "any directory inside its Git worktree"** (`USAGE.md:6-7`); the code supports this via `--show-toplevel`, but no test passes a subdirectory. Documented behaviour without coverage.
4. **`context_readings` is type-validated but never used** (`:154-157`). Defensible under M4's "validate expected JSON types", but a reader may look for the output it feeds and find none.
5. **The em dash in `Current: … — …`** (`:189`) is the one non-ASCII byte on the success path; under a non-UTF-8 stdout encoding `print` would raise outside the `RecordError` handler. Outside M4's scope (that clause covers malformed-input and read/Git errors), so noted only.

---

## Limitations

Read-only inspection of the four files plus a directory listing. I did not execute the command or the suite, did not read `.git/roll/run.json` or `.git/cross-llm/*` (agreement.md:50-52), and did not consult the builder's account. Artifact quality here says nothing about Roll lifecycle, context cost, source exit, or absence of compaction — those need the controller's runtime evidence. One incidental observation from the listing: the only non-deliverable byproduct in the worktree is `__pycache__/test_roll_status.cpython-314.pyc`, consistent with the suite having been imported under Python 3.14; it carries no information about pass/fail.

One question, since it is the only item that could turn a nonblocking note into a blocking one: does the live ledger append a history entry when a worker *starts*, or only when it *returns*?
