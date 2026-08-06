---
route: new
stage: done
---

# Release-closeout — every release checks its own story, and fixes it

## Value

Born from the skriv/slainte/tend review (2026-08-06/07, Tony's keys in
the interview): slainte's logic is good and its usage is zero for one
reason — nobody is prompted; it waits to be remembered, and memory is
exactly what the machinery exists to replace. Meanwhile every release
already has a close moment (the version-bump work commit inside a
conductor session) where the whole doc surface should be checked — and
today only the mechanical subset is (CI's release sweep R1–R3, AU1–6;
byte-sync and reference resolution, never narrative truth). The
judgment layer — does the README still describe what shipped? is
What's New honest? does the playbook's architecture list match? — runs
never. Cold eyes keeps proving the cost: five goal gates, five layer-4
blocks, all of them stale-narrative gaps found *after* shipping.

Value, in units:

- **Doc-surface passes per release: 0 → 1.** A release-shipping task
  (the diff bumps the version) or a feature-closing one (a goal
  record lands) triggers the close-out pass by contract — prompted by
  the machinery, never by memory.
- **slainte fixes instead of reporting.** Findings become edits,
  applied under conductor's verification gate as a normal work commit
  (diff read, blast radius reviewed) — "reports, never fixes" dies as
  slainte's identity.
- **tend runs at the two moments it's needed**: conductor's orient on
  a repo with no Kerd structure offers tend's setup; a release re-runs
  tend's drift check alongside the doc pass.
- **The layer-4 tail shrinks.** The class cold eyes blocks (documents
  narrating dead behaviour) gets a per-release sweep instead of
  waiting for the next goal gate.

Named honestly, the losses and limits: **slainte stops being read-only**
— an audit that edits can edit wrongly; the countermeasure is the same
gate every work commit passes, not a new safety net. **The trigger is
prompt-layer** — conductor's text fires the pass; nothing refuses a
session that skips it (the mechanical subset stays CI's; a CI rule for
"version bumped but What's New untouched" is a plausible future
graduation, not this slice). External surfaces (websites, SDK docs,
portals, marketplace listings beyond this repo's files) need a
declared-surfaces mechanism — slice 2, not tonight.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| The fix mode edits away something a human wrote deliberately — an audit with hands rewrites voice, nuance, or a decision it misread as drift | yes | trust in the pass dies on the first bad edit; docs regress silently | medium — narrative judgment is exactly where models overreach | five layer-4 blocks show models also *miss* narrative drift; the inverse error (overcorrecting) is untested | countermeasure - permanent | fixes are work commits under conductor's verification gate: diff read in full, blast radius reviewed, staged by name; anything judged deliberate-not-drift is reported, not edited — the pass's report names what it chose not to touch | |
| The pass duplicates CI and rots into noise (checks what R1–R3/AU1–6 already refuse) | no | wasted tokens per release; findings ignored | medium | the .slainte config already targets CHANGELOG.md, dead since 0.14.0 — stale target lists rot | countermeasure - permanent | the pass's charter names its layer: narrative truth only — anything machine-checkable belongs in CI and gets a Backlog row instead of a slainte check; the target list derives from the repo (README, playbook, capability lists, What's New, docs/design living docs), not a hand-kept config | |
| Prompt-layer trigger silently skipped (the conductor text isn't honored some session) | no | one release ships unchecked — today's status quo, not a regression | medium | the invoke-is-literal precedent held on first run (v0.84.0); prompt-layer instructions in this repo are honored but unenforced | accepted | | a release demonstrably ships with the pass skipped: graduate the cheapest subset to a CI rule (e.g. version-bump-without-What's-New refusal) |
| Release moment misdetected (version bump absent from a release-shaped change, or present in a non-release edit) | no | a pass fires needlessly or misses once | low — the three-field bump is the release definition here (R1) | CLAUDE.md release checklist + gate release rules define release = version bump | countermeasure - permanent | release detection is the version-field diff, same definition CI uses — one release definition; the goal-record clause (goal-rung amendment, Tony's key) adds a completion firing moment, not a second release heuristic | |

## Release slice

Rigor level: mvp

Smallest valuable slice — **slice 1: the repo-surface pass, wired into
conductor**: slainte's SKILL.md re-founded as the release close-out
pass — triggered, not remembered: when a conductor task's diff bumps
the plugin version — or, per the goal-rung amendment (Tony's key), the
session lands a goal record — the close-out (before running the
boundary) executes the pass: tend's drift check plus a narrative-truth sweep of
the repo's own surfaces (README sections + What's New, playbook
architecture/role lines, capability lists, living docs/design docs
touched by the release), fixing what is drift and reporting what it
deliberately left (judgment findings only — the mechanical layer stays
CI's); fixes ship as a normal work commit under the verification gate **and
pass skriv's one-shot audit first — machine-written prose on
user-facing surfaces honors the voice rules automatically** (Tony's
key 2026-08-07: skriv wired in where prose happens, never a
session-wide toggle — code and technical text stay out of skriv's
scope by its own charter); conductor's orient gains the bare-repo
wire (no Kerd structure → offer tend's setup); `.slainte`'s hand-kept target list dies (targets
derive from the repo); standalone `/kerd:slainte` and `/kerd:tend`
stay invocable on demand; README + state-contract + kerd-map updated
together; MINOR version bump.

Deliberately excluded, named:

- **External/declared surfaces** (websites, SDK docs, developer
  portals, marketplace listings beyond this repo's files) — slice 2,
  behind a declared-surfaces mechanism.
- **Any CI graduation** (e.g. What's-New-untouched refusal) — named
  in the accepted-risk row's review trigger, not built here.
- **The kivna scaffold verdict** — its archaeology stays a Backlog
  item; tend's bare-repo wire offers what tend already does today.
- **skriv edits** — reviewed, verdict keep; its SKILL.md is untouched.
  The pass *calls* skriv's existing one-shot audit on the prose it
  writes — a caller wire, not a skriv change (the invoke pattern,
  third use).

## Grounding

- skills/slainte/SKILL.md — the skill being re-founded
- skills/tend/SKILL.md — the drift check the pass runs; the setup the orient wire offers
- skills/conductor/SKILL.md — the two trigger sites (orient, close-out)
- CLAUDE.md — the release checklist defining the release moment
- tools/gates/README.md — the mechanical layer the pass must not duplicate
- kivna/sessions/2026-08-06.md — the review interview and the three briefs, this frame's evidence
