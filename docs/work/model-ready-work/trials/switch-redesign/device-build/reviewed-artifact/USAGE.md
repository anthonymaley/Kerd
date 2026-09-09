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

For a report-friendly summary that can be pasted into a written work report
without copying any source body, request Markdown:

```sh
python3 pickup_preview.py example.json --format markdown
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

Markdown output is a heading, a state table, a source table, and the closing
line, so it can be pasted into a written report:

```text
# Prepared pickup preview

| Field | Value |
| --- | --- |
| Branch | "kerd-switch-trial-20260906" |
| Revision | "2302c2a3f92fb1c094b23b3c83eb67b9d79b8a83" |
| Working tree at check | clean |
| Synchronization | local-only (not synchronized) |
| Selected sources | 2 |
| Total source text | 9100 UTF-8 bytes |

| # | File | Selection | UTF-8 bytes |
| --- | --- | --- | --- |
| 1 | "CONTEXT&#46;md" | "complete file" | 7156 |
| 2 | "TODO&#46;md" | "## Now (including child sections)" | 1944 |

Prepared does not mean restored or accepted.
```

The state table always carries the same six rows, in that order. The source
table has one row per selected source, in packet order, and keeps its header
row even when no source was selected. Markdown contains no source content, no
note prose, no private session-ID fields and no unknown extra fields. The note
is dropped on purpose: it is free prose written for a reader, not safe metadata
for a report.

Recorded labels — branch, revision, file and selection — go through one
inert-cell convention. It is documented here because a Markdown table is a
structural format, so an unescaped label could change the table rather than
appear in it:

1. Control characters, formatting characters, lone surrogates and literal
   backslashes first become the same visible escapes the text format uses
   (`\u001B`, `\U000E0001`, `\\`), rendered through step 2 as `&#92;u001B` and
   so on. A newline therefore cannot open a second row. `@` additionally becomes
   the visible escape `\u0040`, so email addresses do not become automatic links.
   Literal backslash-u text stays distinguishable because its backslash was doubled.
2. The characters `&`, `<`, `>`, `|`, `` ` ``, `\`, `*`, `_`, `[`, `]`, `~`, `:`, `.` and
   `"` then become decimal character references: `&#38;`, `&#60;`, `&#62;`,
   `&#124;`, `&#96;`, `&#92;`, `&#42;`, `&#95;`, `&#91;`, `&#93;`, `&#126;` and
   `&#58;`, `&#46;` and `&#34;`. Colons and periods prevent bare URL/domain
   autolinking while displaying normally after rendering. A table parser splits a row into cells on the raw pipe character
   before it decodes any reference, so `&#124;` cannot add a cell. In the tested
   rendering, references do not open code spans, emphasis, links or raw HTML. `&` is in the
   set so that a label containing a literal reference cannot forge one.
3. The result is wrapped in quotation marks. Since a quotation mark inside a
   label became `&#34;`, the wrapping marks are the only unescaped quotation
   marks in a cell, and show exactly where the recorded label begins and ends.

`#` is deliberately left readable. A heading is a block construct and cannot
begin inside a table cell, so escaping it would cost legibility on labels such
as `## Now (including child sections)` without removing a risk.

Limits of the Markdown claim. The laptop reported manual checks with pandoc's GFM
reader and Python-Markdown's tables extension, but did not supply their exact
fixtures or HTML. Independent review found a missing case: bare URLs and email
addresses could still become links. After correction, the controller rendered a
retained synthetic fixture through GitHub's Markdown API in gfm mode, without a
repository context: two tables, nine rows and no active elements inside cells.
The fixture, returned HTML and method are retained in the trial's review pack.
This is out-of-band evidence, not a network dependency of the stdlib test suite.
The corrected version has not been rerun through the laptop's two renderers.
No guarantee is made for arbitrary renderer plugins, repository-context reference
linking or consumers that treat the Markdown as HTML directly. Text and JSON
formats preserve their existing display behaviour; the extra email display escape
applies only to Markdown.

The command validates the required packet shape before producing a successful
preview. Invalid JSON, a missing file, missing or malformed fields, a status
other than `pickup_prepared`, or non-Boolean state flags produce an error on
standard error and exit status 2, with no successful output on standard output.
An unsupported `--format` value also exits with status 2 and prints a usage
error on standard error, on the Markdown route as on the other two. Library
callers can use `summarize(packet)` for text, `summarize_json(packet)` for JSON
or `summarize_markdown(packet)` for Markdown; each returns a string and raises
`ValueError` for invalid input.

The preview does not restore or accept a pickup, verify current repository or
remote state, resume a session, or grant execution authority. No output format
includes source content, private session-ID fields, or unknown extra fields.
JSON and Markdown both omit the optional note; JSON further omits the closing
explanation, so its metadata alone is not proof of restoration, acceptance or
execution authority. Markdown keeps that closing line and states the recorded
state in its table, so a pasted report cannot quietly imply that a prepared
pickup was restored or accepted.
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

Markdown reuses the text convention, then adds its email display escape and
character references. Consequently an email's `@` is visibly escaped only in
Markdown; text and JSON retain their existing representations.

Run the test suite with:

```sh
python3 -m unittest -v
```
