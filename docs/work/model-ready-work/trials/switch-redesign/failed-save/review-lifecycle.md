# Independent lifecycle review

2026-09-07, independent Codex reviewer `held_source_review`; read-only inspection
of codex_roll.py, managed_to.py and relevant callers/tests. No live Git/model job
or artifact quality claim was requested from this reviewer.

Two concrete findings were reproduced:

1. Identical repeated checkpoint candidates were rejected as an unchanged loop,
   unlike ordinary Roller. Corrected: skip identical candidates, validate every
   changed candidate against cumulative state, and refuse unchanged overall work.
2. Unexpected activity during a held-source inspection was rejected once but could
   be forgotten by a later idle reading. Corrected: latch held_uncertain, keep the
   source and lock owned, and refuse successful handoff. Explicit abandonment
   remains distinct from successful release.

New regression cases cover both. Independent recheck: both corrected, all 86
Codex lifecycle tests pass, duplicate-candidate save/release ordering independently
checked with mocks. No further directly consequential issue found. The reviewer
did not run the Git-writing ManagedTo fixtures; the controller runs those in
disposable repositories. This is not a claim that every possible lifecycle or
host failure has been proved.
