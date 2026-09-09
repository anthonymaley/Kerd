## Assessment: pickup preview vs. agreement.md (M1–M5)

**No blocking findings.** The three deliverables meet M1–M5 as written. Four scoped gaps, ordered by weight:

**1. Missing-field validation is unexercised (M4/M2 evidence gap).**
`test_pickup_preview.py:132-158` covers *wrong-typed* and *empty* fields, but no case omits a required key. The `f"{owner}.{name} is required"` branch (`pickup_preview.py:23-24`) and the `name not in mapping` half of `_boolean` (`pickup_preview.py:33`) are never reached. M2 requires that missing fields "cannot look successful"; the code appears correct by reading, but the claim rests on inspection, not test evidence. Adding `packet()` variants with `branch`/`sources`/`clean_at_check` popped would close this.

**2. Astral-plane escape is malformed and ambiguous (M3, minor).**
`pickup_preview.py:44-45` emits `\u` with an 8-digit width for codepoints above U+FFFF (Cf includes e.g. U+1D173 musical format controls). Result: `\u0001D173`, which is not a valid Python/JSON escape and reads ambiguously as `\u0001` + `D173`. Python convention is `\U0001D173`. Terminal safety still holds — the character is neutralized — so this is display correctness, not a safety hole. Untested: no test supplies a non-BMP format character.

**3. Escaping is not injective (M3, minor).**
A label containing the literal text `\u001B` renders identically to a real escaped ESC (`pickup_preview.py:38-48`). A reader cannot distinguish them. Doubling backslashes would fix it; nothing in the agreement requires it.

**4. CLI error text echoes the argv path unescaped (M3-adjacent, minor).**
`pickup_preview.py:134-136` prints `OSError`, whose string embeds the supplied filename. A path containing control characters reaches the terminal unneutralized. Packet-derived error messages interpolate only field names and indices — no packet values leak — so the leak surface is limited to the caller's own argument. M3 scopes neutralization to *labels*, so this is outside the stated requirement.

**M5 / USAGE:** invocation, output, and limits are accurate against the code; limits at `USAGE.md:38-43` correctly disclaim restore/accept, live-state verification, and token/fingerprint semantics.

**Limits of this review:**
- I did not execute anything. Byte counts in `USAGE.md:24-26` (7156 / 1944 / 9100) and every test outcome are unverified by me.
- I cannot confirm `example.json` or `agreement.md` are byte-identical to what was supplied; I have no baseline to diff against.
- Assessed files: the four named plus `example.json`, all under `/tmp/kerd-active-handoff.8OXsok/destination/`.

## Controller disposition

No blocking artifact finding. Controller reran all 10 worker tests in both destination and copied output. Source/destination agreement and example match their committed originals; those are controller checks, not peer execution.

Missing top-level fields now have a supplemental controller test, iterating all six required fields. Existing worker tests already exercised missing nested source fields. A second supplemental test probes the reported error-path concern with ESC, newline and bidi controls: Python's OSError filename representation escapes them; no raw controls or extra lines are emitted on this host. Do not present that static concern as a reproduced defect.

The non-BMP escape notation and literal-backslash ambiguity remain minor display limitations, not terminal-execution vulnerabilities or unmet requirements. The observed deliverable is retained unchanged; no production adoption or universal secret-redaction claim is made. The preview deliberately displays caller-supplied labels and optional note, so those fields must themselves be suitable for display.

