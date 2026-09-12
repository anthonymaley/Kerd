# Fable review of the Switch Out lean-start slice (0.111.0) — 2026-09-11

Second read-only Fable subagent review of the day, on the uncommitted 0.111.0
working tree at `f8aff95`: the "Leave a lean start point" step, the `measure`
helper, and the first-run migration of Kerd's own memory. The earlier review of
the four skills is [the 0.110.0 review](2026-09-11-fable-skill-review.md).

## Findings, as ranked by the reviewer, with dispositions

1. **OVERCLAIM** — the recorded measurement (20,170 bytes) was 1,704 bytes stale
   against a fresh `measure` run, and the "before" size named the wrong revision
   (216,309 is 0.110.0; 0.110.1 was 216,391). **Fixed:** the reading is now taken
   as the last edit before the save, iterated to a fixed point because the pasted
   digits change the file; the before-size cites 0.110.1.
2. **CONTRACT GAP** — three kept rulings had no entry in `docs/decisions.md`
   (the two made tonight, and DEAD SOLUTIONS, which lives inside another entry).
   **Fixed:** two entries added at the top with index lines; the DEAD SOLUTIONS
   ruling names the entry it lives in.
3. **CONTRADICTION** — README "On cheap boundaries" still said CONTEXT.md is
   pruned at acceptance-record landings. **Fixed.**
4. **CONTRADICTION** — the TODO contract named two homes for a closed row and
   its verdict list lacked `dead`. **Fixed:** completed work is recorded in the
   session log and the archived row; `dead` added; owner/reader blocks and
   cross-skill rows added for the two new files.
5. **LOSS** — four things from the old `## Now` survived nowhere in the pickup
   set: the `ask.py` proof criterion, the vault bridge's queued requests, the
   narrowing of the stashes row, the consolidation-list note. **Fixed:** all four
   restored (NOW bullet, CONTEXT Where We Are, the Backlog row itself).
6. **CLARITY** — the first NOW bullet was "run the next switch in", not actionable
   inside the session it opens. **Fixed:** it is now the Conductor-session proof.
7. **OVERCLAIM** — "six bare slash references prefixed" was seven edits, one a
   rewrite, three inside quoted evidence. **Fixed:** the note says so.
8. **REPRODUCED DEFECT** — `measure` triple-counted a repeated source.
   **Fixed, tested:** a repeated file or section is refused.
9. **CONTRACT GAP** — the acknowledged local-only path was not in current-state
   memory, and two stray `.pyc` files escaped the ignore rules, so the boundary
   save would refuse. **Fixed:** the exact path is named in CONTEXT.md; the
   `__pycache__` was deleted (generated output, nothing tracked).
10. **CLARITY** — three launch-sequence rulings had no bearing on the named next
    work, and the vault-bridge ruling was missing. **Fixed:** the preamble says
    why the three are held; the vault-bridge ruling is inline.
11. **STALE REFERENCE** — "exactly three files" survived in the state contract
    and `fidelity.py`. **Fixed** in the contract ("the pickup set the last Out
    named — by default exactly those three"); `fidelity.py` left as is, it checks
    the default set.
12. **COVERAGE GAP** — no CLI test, no duplicate test. **Fixed:** both added.

Nothing to report from the reviewer: release checklist, dead links, migration
fidelity of the two Backlog rows and the retained position (byte-identical), 153
of 156 decision entries byte-identical and the index matching every entry.

## Helper probe table, as run by the reviewer

Twenty-one `measure` cases in a temp repo: missing file, absent or duplicated
heading, empty section, heading without `#`, Latin-1, CRLF, zero-byte, symlink,
`../` and absolute paths, a directory, an untracked file, a repeated source,
`--target` 0 / -3 / abc / 1, a non-repo project. Every failure exited 2 with a
JSON error except `--target abc` (argparse usage, like the other subcommands)
and an absolute path outside the project (raw ValueError text). Unit suite 281
tests OK before the fixes; 283 after.

## What the reviewer did not review

The 0.110.1 dispositions; the verdicts of the 73 Backlog rows left open;
`roll.py` and `managed_to.py`; hooks tests; whether kivna or lorg read
`## Key Decisions` (inferred no impact from the contract).
