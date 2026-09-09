# Returned independent Claude assessment

Model: claude-opus-5, high effort; read-only. Controller ran 11 tests separately.
The runtime appends history only after a validated returned state (continue,
review or blocked); this answers the reviewer's final question without asking
an unnecessary user question. B1's future/unknown history tolerance is a useful
bounded correction; current runtime does not emit the proposed complete status.
The controller also found real nullable context_readings in non-observed-route
history; the view should tolerate that unavailable optional field.

I read the agreement and all three deliverables in full. No files were modified; I ran nothing.

## Verdict

**Conditional pass with one blocking finding.** The implementation is genuinely careful — no write path exists anywhere in `roll_status.py`, error strings are all literals (so no private content can leak through exception text), and the panel/exit-code honesty language required by M2/M4 is present verbatim. One over-strict validation rule can suppress the entire panel on a plausible real record, and that is what I'd hold the handoff on.

`★ Insight ─────────────────────────────────────`
The strongest privacy property here isn't the ID filtering — it's that every `StatusError` carries a **fixed literal** message (`roll_status.py:65-94`) and `main` prints `{exc}` rather than chaining a traceback. Interpolating `exc` from an underlying `OSError`/`JSONDecodeError` is the usual way private paths and file content leak into stderr; this code structurally cannot.
The second is that validation is separated from rendering (`validate_record` → `make_panel`), so by the time anything is formatted, `status` and every historical status are already constrained to a closed vocabulary. That's why the unsanitized `shown_last` on line 145 is not a control-character hole — but it's also the source of the blocker below.
`─────────────────────────────────────────────────`

## Blocking

**B1 — An unrecognized *historical* status aborts the whole command.**
- Location: `roll_status.py:120-124` (`prior_status ... not in KNOWN_STATES` → raise), consumed at `roll_status.py:164`.
- Reproducing input: `<git-dir>/roll/run.json` = `{"status": "review", "next_action": "Await independent assessment.", "history": [{"status": "complete", "context_trigger": null}]}`
- Expected from reading the code: exit 1, stdout empty, stderr `Roll status unavailable: The Roll status record has invalid history.` The valid current state and next action are never shown.
- Affected measures: **M3** primarily — it defines history entries as carrying `status`/`context_trigger`/`context_readings` and directs "label unknown rather than inventing values," not "refuse to render." Knock-on to **M2**, whose obligation to display a friendly current status and exact next action for `review` is defeated by an unrelated old history entry. M2's closed vocabulary is written about the record's *current* status; the code applies it retroactively to every history item.
- Note the test suite itself uses `"complete"` as its exemplar of a status outside the vocabulary (`test_roll_status.py:219`), and separately asserts the "unknown" labelling path for a *missing* status (`:173-177`) — the missing case degrades gracefully, the unexpected-value case does not. That asymmetry is the defect.
- Source: code reasoning only. I did not execute this; `test_roll_status.py:243` covers `status: ["continue"]` (wrong *type*) but no test covers an unexpected status *string*, so the suite passing would not contradict me.

## Nonblocking (three)

1. `roll_status.py:157` labels `len(history)` as "Completed workers". If the ledger appends an entry when a worker starts, the count overstates. I can't settle this — ledger append semantics are runtime evidence the controller owns, not artifact quality.
2. `roll_status.py:141` — for `history: []` the "Context-triggered Roll observed" line disappears entirely rather than reading `no`/`unknown`. Defensible, but the M3 field silently vanishes.
3. `test_roll_status.py` inherits the ambient environment and global gitconfig. `commit.gpgsign=true`, a global `core.hooksPath`, or a set `GIT_DIR` would break `:100` or skew `--absolute-git-dir` resolution. Affects test reproducibility, not the deliverable's behaviour.

## What I checked and found sound

M1: no write call of any kind exists — only `read_text` and `git rev-parse --show-toplevel` / `--absolute-git-dir`; `test_roll_status.py:34-39` snapshots via `rglob`, which in pathlib **does** include `.git`, so the untouched assertions are real. M4: the ANSI regex plus the `unicodedata` category-`C` sweep leaves no residual escape — an unterminated OSC falls through to the two-char `\x1b[@-_]` form (`]` = 0x5D is in range) and an 8-bit `\x9d` is caught as `Cc`. All seven M2 states are present with "not accepted" wording on `review`. USAGE covers invocation, both `.git` shapes, and the exit-0 caveat, satisfying M5's documentation clause.

## Limitations

Read-only inspection of four files only. I executed nothing — no test run, no `roll_status.py` invocation — so every behavioural statement above, including B1's output, is derived from reading control flow. I did not read `.git/roll` or `.git/cross-llm`, and I did not open `place.json`. Nothing here speaks to Roll lifecycle, context cost, source exit, or absence of compaction.

One question, and it decides B1: **when a Roll worker finishes and its entry is appended to `history`, what values can that entry's `status` take** — is it drawn from exactly the seven current-state names, or from a separate worker-return vocabulary?

