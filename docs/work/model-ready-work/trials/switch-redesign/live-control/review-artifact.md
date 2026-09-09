I'm dispatched as a subagent reviewer, so I skipped skill invocation and went straight to the artifacts. Read-only: I ran no tests, no shell, no git commands.

## Files read

`agreement.md`, `pickup_preview.py`, `test_pickup_preview.py`, `USAGE.md`, `example.json`, plus `place.json` (the builder's claim, read so I could check it rather than accept it).

## Verdict

**No blocker found against M1–M4.** The privacy core (M3) is sound by construction, not by filtering: `_validated_summary` (`pickup_preview.py:99-107`) builds a fresh dict of six named keys and each source entry is a fresh dict of three keys (`:85-91`), so content, note, and unknown input fields cannot reach either output path regardless of input shape. That is the strongest single property in the change, and it is the one M3 needed.

Five gaps below, none of which I judge to block acceptance. One of them (E1) is an evidence limit that only the controller can close.

---

### F1 — Lone surrogates round-trip in text but produce non-interoperable JSON — Medium

`_terminal_safe` deliberately escapes category `Cs` (`pickup_preview.py:44`), and `test_surrogate_label_is_visible_and_utf8_encodable` (`test_pickup_preview.py:159-163`) locks that in for text. The JSON path has no equivalent. `_utf8_size` (`:55-59`) guards surrogates only for `content`; `branch`, `commit`, `file`, `selection` are passed raw to `json.dumps(..., ensure_ascii=True)` (`:152`).

Reproducible input — a packet file containing the literal escape:

```json
{"status":"pickup_prepared","branch":"label\ud800","commit":"abc123",
 "clean_at_check":true,"synchronized":false,"sources":[]}
```

`json.load` accepts that escape and yields a lone-surrogate `str`. `--format json` then exits 0 and prints `{"branch": "label\ud800", ...}`. Asymmetry worth naming: the same surrogate inside `content` exits 2, and in text output it renders safely as `\uD800`.

Whether this is a defect depends on the consumer. Python's `json.loads` accepts it. My understanding — from training data, not verified against a spec fetch in this session — is that RFC 8259 §8.2 leaves unpaired surrogates as non-interoperable and that strict parsers such as Rust's `serde_json` reject them, while Go's `encoding/json` substitutes U+FFFD. For a feature whose stated purpose is "a caller can use its summary without scraping terminal text," a non-Python caller is the expected consumer, so I'd treat this as worth a decision rather than worth ignoring. M2 says "JSON parses into the documented metadata" — it does, under Python. I am not claiming M2 fails.

### F2 — M3's malformed-input evidence is thinner on the JSON route than on the text route — Low

The malformed-packet battery (`test_pickup_preview.py:165-184`, twelve cases) runs only through `summarize`. `summarize_json` is exercised against exactly one invalid input, and only via the CLI (`:309-320`, `branch=""`). The syntax-error path (`:328-337`) and the missing-file path (`:339-345`) are text-only.

Risk is low, because the format branch happens after `json.load` and both formats share `_validated_summary` (`:174`). But M3 is the seeded prior failure and M4 asks the tests to *prove* the route; as written, a future regression that skipped validation inside `summarize_json` would be caught only by the single `branch=""` case.

### F3 — `revision` is not covered by the round-trip test — Low

`test_labels_round_trip_without_terminal_escaping` (`:224-241`) asserts byte-exact recovery for `branch`, `file` and `selection`, but not `revision`. USAGE.md:48 correspondingly promises originality only for "`file` and `selection`", though `branch` and `revision` have the same property in code. M2 names "labels" generally. Code path is identical, so this is a coverage/doc gap, not a suspected bug.

### F4 — Python floor claimed but not exercised — Low

USAGE.md:5 states "requires Python 3.10 or newer". The only build evidence in the tree is `__pycache__/pickup_preview.cpython-314.pyc` and `__pycache__/test_pickup_preview.cpython-314.pyc`, i.e. the suite ran under CPython 3.14. Reading the source I see nothing needing >3.10 at runtime — PEP 585/604 annotations are deferred by `from __future__ import annotations` in both files (`pickup_preview.py:4`, `test_pickup_preview.py:3`), and `subprocess.CompletedProcess[str]` at `test_pickup_preview.py:280` is likewise a deferred annotation. So the claim is plausible but untested. Downgrade the wording or test the floor; either is fine.

### F5 — JSON drops the note and the "prepared ≠ accepted" trailer — Low, informational

Text output carries the note and the closing `Prepared does not mean restored or accepted.` (`:143-145`). JSON carries neither; `summarize_json` discards the validated note (`:151`). USAGE.md:65 documents the note omission, not the trailer.

This cuts both ways and I am not recommending a change: the note is caller-authored free prose, so dropping it is the privacy-safe default, and the agreement neither requires nor forbids it. But in `example.json:19` the note is precisely where "no execution authority is granted by this packet" lives, so a machine consumer sees no field conveying that. Adding one would widen the feature, which the agreement forbids — so this is a documentation call for the controller, not a defect.

`★ Insight ─────────────────────────────────────`
The design choice that makes M3 hold is allowlist-by-construction rather than denylist-by-filtering. Contrast the two failure modes: a filter that strips `content` fails open when a packet gains a new sensitive key; a rebuilt dict fails closed. That is why `test_content_note_and_unknown_fields_are_absent` can assert `set(output) == {...}` — the test checks the *shape*, not a list of known secrets, so it catches leaks nobody anticipated.

The second notable choice is that `_terminal_safe` is applied only at render time, never during validation. That is what lets one validator serve two formats with genuinely different escaping requirements — terminal safety for humans, JSON syntax for parsers — without either contaminating the other. F1 is the one seam where that separation is incomplete.
`─────────────────────────────────────────────────`

---

## Checks I could do statically, and their results

- **Test count**: 19 test methods (10 + 3 + 6 across the three classes), matching `place.json`'s "Ran 19 tests". Consistent.
- **Seeded history preserved**: `place.json:10-12` still carries `"M3": 1`. Consistent with the agreement's requirement.
- **Authority**: the session-start git snapshot lists only `USAGE.md`, `pickup_preview.py`, `test_pickup_preview.py` and `place.json` as modified. `agreement.md`, `example.json` and `.gitignore` are unmodified there. This is from the snapshot supplied to me, not a live check I ran.
- **Error messages carry no packet values** (`:16`, `:24`, `:28`, `:34`, `:68`) — only field names and integer indices. Content cannot leak via stderr on the failure path.
- **USAGE escaping spec matches code**: the 4-vs-8 hex-digit rule and uppercase hex at USAGE.md:66-72 match `_terminal_safe` (`:44-49`). Surrogates being BMP correctly fall in the 4-digit branch.

## Evidence limits

**E1 is the one that matters.** I can see only the working-tree copy of `test_pickup_preview.py`. M1 requires that *existing* tests still pass — but a suite whose existing assertions were rewritten or weakened would look identical to me. Nothing in the code suggests that happened; I simply have no way to distinguish the two. Reading git objects would need shell, which I don't have.

Beyond E1: I executed nothing, so every "passes" in `place.json` is unconfirmed by me, including the 7156 / 1944 / 9100 byte counts in USAGE.md:31-33 and `test_pickup_preview.py:306`. F1's parser-rejection claim is training-data, unfetched.

## Tests the controller should run to settle this

1. `git diff HEAD -- test_pickup_preview.py` — settles E1 and M1 directly. Read-only.
2. `python3 -m unittest -v` — confirms the 19/19 claim.
3. F1 repro: write the surrogate packet above to a temp file, run `--format json`, and feed stdout to a strict non-Python parser. Settles whether F1 is real or academic.
4. F2 closure, if wanted: run the existing malformed battery through `summarize_json` as well as `summarize`, and add the truncated-JSON case under `--format json`.

One question, and it's E1: **can you produce the diff of `test_pickup_preview.py` against HEAD?** Until I see it, M1 is builder-asserted rather than independently assessed, and that is the only measure I cannot reach from the files alone.
