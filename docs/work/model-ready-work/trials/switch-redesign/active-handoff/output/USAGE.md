# Prepared pickup preview

`pickup_preview.py` shows the recorded identity and size of a prepared pickup
without printing the selected source bodies. It uses only the Python standard
library and requires Python 3.10 or newer.

Run it with one pickup packet JSON file:

```sh
python3 pickup_preview.py example.json
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

The command validates the required packet shape before producing a successful
preview. Invalid JSON, a missing file, missing or malformed fields, a status
other than `pickup_prepared`, or non-Boolean state flags produce an error on
standard error and a nonzero exit status. Library callers can use
`summarize(packet)`; it returns the preview string and raises `ValueError` for
invalid input.

The preview does not restore or accept a pickup, verify current repository or
remote state, resume a session, or grant execution authority. Source content,
private session-ID fields, and unknown extra fields are not displayed. Labels
and the optional note are shown with terminal control and formatting characters
escaped. Byte counts describe the UTF-8 encoding of the supplied source strings;
they are not token counts, file sizes checked from disk, or content fingerprints.

Run the test suite with:

```sh
python3 -m unittest -v
```
