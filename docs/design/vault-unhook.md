# Vault-unhook — the vault becomes opt-in everywhere

Living design doc. Owner: the `vault-unhook` work item
(`docs/product/vault-unhook.md`), release slice 1. Grounded on the
repo's current skill sources (switch unchanged since v0.75.0 — the
in-cache copy matched; kivna, tend, and the vault spec read in full at
this rung). Routed here by `gate.py route` — enters at design.

## What it does

Removes the automatic vault write from the session boundary and every
nag toward creating one, without touching the deliberate path. After
this slice: switch neither reads nor writes the vault in any mode —
its surviving vault mentions are the deliberate-path pointer and the
conditional banner line *(goal-gate amendment 2026-08-06: the original
"nor mentions" claim overstated)*; tend treats a vault-less project as
a legitimate opt-out; `/kerd:kivna save` is the deliberate way vault
pages get written (lorg's report copy is the one automatic exception,
per the coverage table). Nothing in any existing vault is deleted or
moved. The switch-IN path is not edited at all — the killer feature is
out of bounds by construction.

*Goal-gate amendment, 2026-08-06 — the edit map below was incomplete
as designed:* cold eyes found the two documents that actually route
the boundary behaviour missing from it — `skills/conductor/SKILL.md`
(four boundary-vault claims, including the close-out handoff
instruction) and `docs/state-contract.md` (the ownership contract,
four rows) — plus six lesser declared-truth sites (playbook gotcha,
"only writer" overclaims, the kerd-map generator label,
conductor-role.md, slainte's lag tolerance). All amended in the
goal-gate commit. The cross-cutting grep the playbook has always
demanded is now a named design-rung obligation for any slice touching
a system-wide behaviour. The shipped README edits were nine (steps
6+7 of the contract, the expansion declared there), tend's were four.

## The coverage table — every vault artifact's fate

The killer risk's countermeasure: nothing dies silently. Inventory from
`docs/vault-spec.md` + the live Kerd vault:

| Vault artifact | Written by | Fate after unhook |
|---|---|---|
| `[Name] Status.md` (spine) | kivna save | duplicated-in-repo (CONTEXT.md `## Where We Are` + the newest session log); refreshed only on deliberate save |
| `[Name] Weekly.md` (spine) | kivna save | re-curation of repo records (session logs, Key Decisions); refreshed on deliberate save |
| `[Name].md` MOC (spine) | kivna scaffold/save | static index; updated on deliberate save when files are added |
| Domain files (Architecture Decisions, Playbook, Positioning, Usage/Install guides) | kivna save step 4 | human-curated re-statements of repo decisions; vault-only prose kept via deliberate save |
| `people/` shared directory | human + kivna wikilinks | **vault-only — the genuine residue**; untouched by this slice, writable via deliberate save, linked per the spec |
| Client/engagement/research slots | human + kivna save | vault-only where they exist; deliberate save |
| Lorg report vault copy | lorg | unchanged here (lorg is under its own review) |

Nothing is deleted; the automatic *writer* stops, the files stay.

## The edit map — four files, one principle

**A. `skills/switch/SKILL.md`** (the bulk):

1. Frontmatter `description`: drop `vault` from the session-state
   commit list; "skip vault and reflection" → "skip reflection".
2. Intro: "The session-state commit is CONTEXT.md, TODO.md, the
   session log, and vault files" → drop "and vault files".
3. Usage line for `out light`: "(skip vault, reflection, progress
   tracking)" → "(skip reflection, progress tracking)".
4. Modifier table: delete the "Vault update" row.
5. The under-table note becomes: the vault is neither read nor
   written by switch in any mode — it is kivna's, on demand.
6. **Step 4 "Update the vault": deleted; steps 5–8 renumber to 4–7.**
   (Decision below.)
7. Reflection step: "flag for the appropriate vault file … written
   during the `/kerd:kivna save` step" → "record in CONTEXT.md Key
   Decisions; a project that keeps a vault updates it on demand via
   `/kerd:kivna save`".
8. Triage step: drop "vault files" from the session-files list (they
   were never committable here — the vault is a separate tree).
9. Completion banner: when `kivna/vault.json` exists, append one
   line: `vault not written (on-demand since v0.83.0) — /kerd:kivna
   save for the Obsidian export`. Conditional on the config file,
   permanent (harmless, and it is the ledger's third-row
   countermeasure).
10. Fallback Behavior: delete the "no vault found → suggest scaffold"
    paragraph — absence is now legitimate, not a gap.
11. Light-mode note: "vault and reflection skipped" → "reflection
    skipped".

**B. `skills/kivna/SKILL.md`** (deliberately minimal): one sentence
added to the save command's intro — save is deliberate and on-demand;
switch no longer calls it at the boundary (v0.83.0); a vault is exactly
as fresh as its last save. Everything else stands: the skill already
frames save around natural breakpoints, and scaffold's interview flow
is untouched (invoking kivna IS the opt-in).

**C. `skills/tend/SKILL.md`**: Category 3's missing-vault path changes
from a ⚠ current-vs-proposed table to one info line — "no vault
configured — opt-in via /kerd:kivna scaffold when this project wants a
knowledge base" — never a failing/warning state. A present vault keeps
every existing check (spine, symlinks, naming, MOC links, session-
history ban). Category 2's required-files example drops `vault.json`.

**D. `docs/vault-spec.md`**: the Ownership section gains the opt-in
sentence (a project without a vault is not in violation; tend flags
drift only where a vault exists) and the rollout note is updated.

**Plus:** README (switch para's vault sentence; kivna section's "same
save mechanic switch uses at the boundary" dies; How They Fit's
day-to-day paragraph drops the automatic `/kerd:kivna save` call); version
0.83.0 in the three fields; capability lists unchanged ("knowledge
management" still true, on demand).

## The decision — delete-and-renumber vs tombstone step

Marks (light tier — not close):

| Criterion | delete + renumber | keep a tombstone "step 4 (removed)" |
|---|---|---|
| The skill reads clean to a new user (M) | ○ | × a numbered hole documents history, not behavior |
| External step-number references survive | △ one playbook gotcha cites "step 5" — a dated incident record, left as archaeology | ○ |
| Diff size | △ larger, mechanical | ○ |

**Delete + renumber wins.** Living docs describe what is, git history
archives what was.

## Named answers — the stage-1 measurements

| Measurement (product doc, Value) | Target | Named answer |
|---|---|---|
| Automatic vault writes per boundary | 1 → 0 | the step's deletion, verified at build by diff scope + `grep -c "kivna save" skills/switch/SKILL.md` landing at exactly the two deliberate-path pointers (reflection re-point + banner line). Honest limit, named: skill text is prompt-layer — no runtime refuser can observe a session's tool calls; the machinery's writ stops at what is on disk. |
| The on-demand path | unchanged | kivna SKILL.md diff = one added sentence, zero removals — asserted by diff read at build (step 5-class collateral check). |
| The killer feature | byte-for-byte | zero diff hunks inside the `## Switch In` section of switch SKILL.md — asserted by diff read at build; any hunk in that range is a build refusal. |

## Testing strategy

No new CI machinery — this slice edits skill text, and the tools can
only check what lands on disk. The proof obligations run at build and
land in the goal record: the three diff-scoped assertions above, the
full local suite (unchanged — no tool edits), and the release sweep
(R1–R3: three version fields, byte-identical capability lists, no bare
skill references introduced). The rigor level is `mvp` and this section
is its honest disposition: measured = the three diff assertions +
release sweep; waived-by-name = runtime observation of a live boundary
(no harness for it; the first real switch-out after ship is the
observation, recorded in the next session log).

## Out of scope, named

- **Boundary auto-sizing** (light/low die as user-facing modifiers) —
  Backlog, its own slice; this slice deliberately leaves the modifier
  table's shape alone apart from the vault row.
- **The cycle automation** — Backlog High, its own frame.
- **The kivna verdict** (import/export/scaffold archaeology) — Backlog;
  this design's minimal kivna touch is deliberate so that review meets
  an unmodified surface.
- **Any vault deletion or migration** — never in this slice.
- **Weekly scheduled saves / save-on-release** — only if the
  stale-insurance review trigger ever fires.
