# Release-closeout — design

Slice 1 of `docs/product/release-closeout.md`: the repo-surface pass,
wired into conductor. Canvas: `docs/design/release-closeout.excalidraw`
(generator: `tools/diagram/gen_release_closeout.py`).

## The mechanism

**The trigger is the version-field diff — CI's own release definition,
reused.** A conductor task whose work commit changes the three
`"version"` fields (R1's set) IS a release; at close-out, before the
boundary step, conductor runs the release close-out pass. One
definition of "release", shared with the machine layer; no second
heuristic.

**The pass is two invokes and a charter — the invoke pattern's third
and fourth uses.** Conductor calls `/kerd:tend` for the structural
drift check and `/kerd:slainte` for the narrative pass; slainte's pass
calls skriv's one-shot audit on any prose it writes. Nothing
re-describes anything: tend and slainte stay the definitions of their
own checks, conductor holds trigger wires only — the same
single-definition law v0.84.0 established for the boundary.

**The charter split — CI owns mechanical, the pass owns narrative.**
Slainte's dormant `release` area already specced the judgment layer
(its rule 7, cross-doc claim verification, is the narrative-truth
sweep this frame wants) — and its rules 1, 2 and 5 now duplicate what
CI refuses mechanically (R1 version sync, R2/R3 description sync and
namespace). The re-founding prunes the duplicated rules to a one-line
"CI owns" pointer and keeps what no machine rule covers: skill-count
claims, frontmatter/directory name drift, marketplace URL, hook
template currency, and the whole rule-7 family (README claims vs
SKILL.md behaviour, What's New honesty, playbook truth, state-contract
table vs actual behaviour).

**Fixes are work commits, and restraint is reported.** The pass edits
what is drift, under the caller's verification gate (diff read, blast
radius, staged by name, skriv on prose). Anything judged
deliberate-not-drift is *named in the report as left untouched* — the
killer risk's countermeasure is visible restraint, not a second gate.

**The config dies; targets derive.** `.slainte` (the hand-kept target
list — currently pointing at a CHANGELOG dead since 0.14.0) is
deleted. The pass derives its surface from the repo: README.md
(sections + What's New), CLAUDE.md, docs/playbook.md,
docs/state-contract.md, the capability lists, and any `docs/design/`
living doc the release's diff touched. The on-demand area audits
(docs/code/site/deps/playbook) survive config-less, deriving targets
the same way.

## Edit map

From the design-time concept sweep (read-only · reports · never fixes ·
`.slainte` · audit targets · health-audit phrasings — swept across
skills/, docs/state-contract.md, docs/playbook.md, README.md,
CLAUDE.md, docs/design/; each surviving section then read whole, per
the playbook's newest gotcha).

**skills/slainte/SKILL.md — re-founded (the largest edit)**

1. Frontmatter description: "Read-only audit that reports issues
   without fixing them" → triggered release close-out pass + on-demand
   audit; fixes drift under the caller's verification gate.
2. Identity paragraph (line 10): "Read-only … Does not fix anything.
   That's the user's call." → the pass fixes drift and reports what it
   deliberately left; on-demand audits report-only unless the caller
   asks for fixes.
3. `## Config` section + `.slainte` format + the two config commands
   (`add`, no-arg config display) — deleted whole; replaced by a
   `## Targets` paragraph: derived from the repo, listed explicitly.
4. New `## The release pass` section: trigger (version-field diff, by
   its caller conductor), the charter split (CI-owns pointer line
   naming R1–R3/AU1–6; the kept judgment checks), fix discipline
   (work commit under the gate, skriv audit on prose, restraint
   reported), output shape (the severity table stays).
5. The `release` area: rules 1, 2, 5 pruned to the CI-owns pointer;
   rules 3, 4, 6, 8 and rule 7's family kept (renumbered); rule 7's
   vault item keeps its v0.83.0 informational-only note.
6. Area audits: `.slainte` registration language removed; targets
   derived per area.

**skills/tend/SKILL.md — 5 sites, `.slainte` dies**

7. Required-files list: `.slainte` row removed.
8. Scaffold: the `.slainte` template block removed (tend stops
   creating it).
9. Deprecated-patterns list: add `.slainte` ("removed in v0.85.0 —
   targets derive from the repo; offer deletion"); the `.sotu` row's
   rename target note updated to "(both since removed)".
10. Stale-file exception list: `.slainte` dropped from the config
    extensions example.
11. The example report's required-files line: `.slainte` removed.

**skills/conductor/SKILL.md — the two trigger wires**

12. Orient gains the bare-repo wire (one paragraph in the cold/warm
    path area): no Kerd structure detected (no CONTEXT.md, no TODO.md,
    no kivna/) → offer `/kerd:tend` setup before planning.
13. Close-out gains the release wire as step 6, before the boundary
    step (which renumbers 6→7): if this session's work commits changed
    the plugin version fields, run the release close-out pass — invoke
    `/kerd:tend` (drift check) and `/kerd:slainte` (narrative pass with
    fixes); the pass's edits are work commits under the verification
    gate. One instruction each, zero re-description; the
    `[conductor: closed]` marker stays after the boundary.

**docs/state-contract.md — 2 rows**

14. "Structural audit and fix | tend | Slainte reports content issues
    but doesn't fix structure" → tend keeps structure; slainte fixes
    *content* drift under the caller's gate.
15. "Content audit (read-only) | slainte | Slainte never modifies
    files, only reports" → "Content audit and fix | slainte —
    triggered at release by conductor, on demand otherwise | fixes
    drift under the caller's verification gate; reports what it
    leaves".

**README.md — 2 edits + What's New**

16. Slainte section (~line 134): rewritten — triggered at release,
    fixes with restraint reported, config gone, areas derived;
    tend section untouched except any `.slainte` mention if present.
17. What's New v0.85.0 entry (Compare & Contrast voice), cap at five
    (drop v0.80.0), trailing line bumped.

**docs/playbook.md — 1 line**

18. Role line: "slainte: project health audits (docs, code, site,
    deps, playbook)" → "slainte: the release close-out pass (triggered
    by conductor at version bumps; fixes doc drift under the gate) +
    on-demand health audits".

**tools/diagram/gen_kerd_map.py + the map — 1 line + regen**

19. Slainte one-liner "read-only health audit: … reports, never fixes"
    → "release close-out pass: triggered at version bumps, fixes doc
    drift, restraint reported"; regenerate
    `docs/design/kerd-map.{excalidraw,svg}`.

**Repo root — the config's grave**

20. `git rm .slainte` — nothing replaces it.

**.claude-plugin — version bump**

21. 0.84.0 → 0.85.0 in the three fields (MINOR). Capability lists:
    "project audits" wording reviewed at design time — it still
    describes the on-demand audits and the pass; unchanged.

## Stage-1 measurements — named answers

- **Config dead**: `.slainte` absent from the tree (`git ls-files
  .slainte` prints nothing); `grep -c '\.slainte'
  skills/slainte/SKILL.md` prints `0`; tend's count = the
  deprecated-pattern rows only (exact count derived at contract time).
- **Read-only identity dead**: `grep -c 'Read-only audit\|Does not fix
  anything\|never modifies files, only reports'` over
  `skills/slainte/SKILL.md` and `docs/state-contract.md` prints `0`
  in each.
- **The wires exist, once each**: conductor greps for the release-pass
  step and the bare-repo offer ≥ 1 each; conductor contains no slainte
  check descriptions (single-definition law — heading-text grep = 0).
- **The charter split is written**: slainte greps — CI-owns pointer
  ≥ 1; `Version sync` as a kept rule = 0.
- **skriv wire present**: `grep -c 'skriv' skills/slainte/SKILL.md`
  ≥ 1 (the pass charter names the audit).
- **Map regenerated**: `gen_kerd_map.py` contains the new one-liner;
  the committed map pair is regenerated in the same commit.

## Out of scope, named

- External/declared surfaces (websites, SDK docs, portals,
  marketplace listings beyond this repo's files) — slice 2.
- Any CI graduation (What's-New-untouched refusal etc.) — behind the
  accepted-risk review trigger.
- The kivna scaffold verdict — Backlog archaeology, untouched.
- skills/skriv/SKILL.md — untouched (verdict keep; it is called, not
  changed).
- Switch — untouched entirely; the pass runs before the boundary, and
  the boundary contract is v0.84.0's.
