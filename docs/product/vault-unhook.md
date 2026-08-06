---
route: new
stage: building
---

# Vault-unhook — the boundary stops paying for pages nobody reads

## Value

Born from the switch/kivna workhorse interview (2026-08-06, Tony +
two other users): the vault has **zero readers** — no human opens
Obsidian (all three users, by their own account), and no machine reads
it (write-only from the session flow by design since the split). Yet
every full switch-out writes it automatically — Status.md overwritten,
domain files updated — real tokens at every boundary, part of the exact
bill that pushed one user into session limits *mid-switch-out*, the
worst place to die. The insurance the vault represents ("I'm not losing
the history") is already delivered twice over: `kivna/sessions/`
immutable full-fidelity logs, and git history of every pruned
CONTEXT.md.

Value, in units:

- **Automatic vault writes per boundary: 1 → 0.** Switch-out stops
  calling the vault save; the boundary's token cost drops by the
  vault-save share for every user, on every project, at every
  boundary.
- **The capability survives on demand: unchanged.** `/kerd:kivna save`
  still performs the full write when invoked deliberately — the
  Obsidian export becomes a choice, not a toll.
- **The killer feature untouched: byte-for-byte.** Switch-in reads the
  same three files in the same flow; nothing about "fresh session,
  switch in, one second ago" changes.

Named honestly, the loss: **the vault stops tracking the project
automatically.** Status.md goes stale unless someone asks for a save —
the insurance shifts from always-current to current-when-refreshed.
Anyone who *does* start reading the vault will find it dated to the
last deliberate save.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Silent knowledge loss: something is captured only by the vault path today and dies with the auto-save | yes | long-term knowledge value eroded — the thing switch exists to protect | low-medium — most vault content duplicates repo records | analysis 2026-08-06: Status.md mirrors CONTEXT.md + the latest log; Weekly and domain files re-curate CONTEXT Key Decisions; `people/` files and human-curated domain prose are the genuine vault-only residue — and the on-demand save keeps that path fully writable | countermeasure - permanent | the design carries a coverage table naming every vault artifact's fate (duplicated-in-repo · vault-only-kept-via-on-demand); do-not-save markers unchanged; nothing is deleted from the vault — only the automatic write stops | |
| The loved insurance rots silently: an unused-but-valued capability degrades trust when someone finally visits and finds it months stale | no | the "I'm not losing history" comfort inverts on first stale visit | medium — nobody visits today, which is exactly how staleness accumulates | the interview itself: the vault's value to Tony is its existence, not its freshness; cross-project awareness ("you use that approach in X") was checked and comes from the memory layer (MEMORY.md + episodic search), never the vault — nothing reads the vault in-session by design | accepted | | a real retrieval need — including a cross-project one — hits the vault and finds it stale: re-argue (candidates then: a weekly scheduled save, or save-on-release) |
| Boundary behavior change surprises the other users mid-habit | no | one confused boundary, quickly learned | low — the change removes a step they never see output from | same usage pattern across users (interview); the completion banner will name the change the first time | countermeasure - permanent | switch-out's banner notes "vault not written (on-demand since v0.83.0) — run /kerd:kivna save if you want the Obsidian export" for the first releases | |

## Release slice

Rigor level: mvp

Smallest valuable slice — **slice 1: the vault becomes opt-in
everywhere**: switch-out's vault step is removed from full mode (the
modifier table collapses — full and light become identical on the
vault axis); the reflection step's "flag for vault" language re-points
at CONTEXT.md; `/kerd:kivna save` is untouched and documented as the
deliberate export; **tend's vault-integration check softens — an
absent vault is a legitimate opt-out (info line), a present vault
still gets its spine checked** (Tony's call, 2026-08-06: "add that
project by project as needed, not by default" — without this, tend
would nag every opt-out project toward pages nobody reads); README
switch + kivna + tend sections and both SKILL.md files updated
together; MINOR version bump. The capability list keeps "knowledge
management" — kivna still owns it, on demand.

Deliberately excluded, named:

- **The kivna verdict** — whether import/export/scaffold earn their
  place is its own evidence-checked Backlog item (the same
  zero-usage smell, but no license without archaeology).
- **Boundary auto-sizing** (light/low dying as user-facing modifiers;
  switch sizes its own boundary) — Backlog, separate slice.
- **The cycle automation** (`switch out → clear → in` as one act) —
  Backlog High, its own frame; killer feasibility question first.
- **Any vault deletion** — nothing in `~/eolas/vault/` is touched,
  ever, by this slice.

## Grounding

- skills/switch/SKILL.md — the boundary flow this slice edits
- skills/kivna/SKILL.md — the save path that becomes on-demand-only
- skills/tend/SKILL.md — Category 3's missing-vault nag softens (added at design when the tend amendment joined the slice; grounding healed same sitting)
- docs/vault-spec.md — the vault contract the coverage table is checked against
- kivna/sessions/2026-08-06.md — the interview record this frame's evidence cites
- CONTEXT.md — standing decisions bind: the three-file read set, state-in-declared-artifacts
