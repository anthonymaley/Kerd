# Prepared pickup preview

`pickup_preview.py` shows the recorded identity and size of a prepared pickup
without printing the selected source bodies. It uses only the Python standard
library and uses Python 3.10+ syntax. This trial was tested on Python 3.14;
the minimum-version runtime has not been exercised.

Run it with one pickup packet JSON file:

```sh
python3 pickup_preview.py example.json
```

Text is the default output format. For a machine-readable summary, request
JSON explicitly:

```sh
python3 pickup_preview.py example.json --format json
```

The preview reports the recorded branch and revision, whether the working tree
was clean at the check, whether the packet was synchronized or local-only, each
selected file and section, and the source text sizes in UTF-8 bytes. For example:

```text
Prepared pickup preview
Branch: kerd-switch-trial-20260906
Revision: 2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83
Working tree at check: clean
Synchronization: local-only (not synchronized)
Selected sources: 2 sources
  1. CONTEXT.md — complete file — 7156 UTF-8 bytes
  2. TODO.md — ## Now (including child sections) — 1944 UTF-8 bytes
Total source text: 9100 UTF-8 bytes
Note: Caller-selected saved records, not fresh operational verification. Selection completeness and restored meaning still need assessment. No session is resumed and no execution authority is granted by this packet.
Prepared does not mean restored or accepted.
```

JSON output is one object with exactly these fields:

- `branch`: the recorded branch string.
- `revision`: the recorded `commit` string.
- `clean_at_check`: the recorded Boolean working-tree flag.
- `synchronized`: the recorded Boolean synchronization flag.
- `selected_sources`: an array in packet order. Each entry contains only
  `file`, `selection`, and `utf8_bytes`.
- `total_utf8_bytes`: the sum of all selected-source `utf8_bytes` values.

The `branch`, `revision`, `file` and `selection` values are the original strings. JSON syntax escapes
controls and backslashes as needed, and parsing the JSON restores the original
labels; the terminal-safe text-display convention described below is not
embedded in JSON data. This trial verifies decoding with Python's JSON parser,
not every consumer. Label validation does not reject lone-surrogate strings;
such a label is preserved as an escape, unlike source content, which must encode
as valid UTF-8. No cross-parser guarantee is claimed for those labels.

The command validates the required packet shape before producing a successful
preview. Invalid JSON, a missing file, missing or malformed fields, a status
other than `pickup_prepared`, or non-Boolean state flags produce an error on
standard error and exit status 2, with no successful output on standard output.
An unsupported `--format` value also exits with status 2 and prints a usage
error on standard error. Library callers can use `summarize(packet)` for text or
`summarize_json(packet)` for JSON; each returns a string and raises `ValueError`
for invalid input.

The preview does not restore or accept a pickup, verify current repository or
remote state, resume a session, or grant execution authority. Neither output
format includes source content, private session-ID fields, or unknown extra
fields. JSON also omits the optional note and text-only closing explanation;
its metadata alone is not proof of restoration, acceptance or execution authority.
In text output, labels and the
optional note use an unambiguous terminal-safe display convention:
literal backslashes are doubled, BMP control/formatting characters and lone surrogates use a
lowercase `u` and four hexadecimal digits (for example, `\u001B`), and non-BMP
control and formatting characters use an uppercase `U` and eight hexadecimal
digits (for example, `\U000E0001`). Thus literal text such as `\u001B` is shown
as `\\u001B`, distinct from an actual escape control character shown as
`\u001B`. Hexadecimal letters are uppercase, while normal readable Unicode such
as `café`, `計画`, and `🌍` remains readable. Byte counts describe the UTF-8
encoding of the supplied source strings; they are not token counts, file sizes
checked from disk, or content fingerprints.

Run the test suite with:

```sh
python3 -m unittest -v
```
