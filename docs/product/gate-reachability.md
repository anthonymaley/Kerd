---
route: new
stage: framed
---

# Drive and conductor cannot reach the gate machinery outside Kerd

## Value

Tony's frame statement, in his words (2026-09-02 evening):

> Users in consuming repos cannot reach Kerd's gate machinery through Drive or
> conductor.

**Measured, not asserted.** All four gate invocations use a bare relative path —
`skills/drive/SKILL.md:39` and `:76`, `skills/conductor/SKILL.md:90` and `:150`
— so outside this tree they resolve to nothing and the skill degrades to prose
**silently**. `${CLAUDE_PLUGIN_ROOT}` appears in skill text zero times; its only
proven use is `hooks/hooks.json`.

**The engine is not the problem, and this is the finding that sizes the item.**
Tested 2026-09-02 against a disposable git repository holding one work record
and nothing else:

```
gate.py check widget scope     --root <foreign>  → exit 1   REFUSES
gate.py check widget viability --root <foreign>  → exit 0   passes
gate.py audit                  --root <foreign>  → exit 0   runs
gate.py route widget           --root <foreign>  → full seven-rung table
```

So **machine refusal already travels** with no code change. What is missing is
the wiring that invokes it. This falsifies the premise of the 2026-08-06
standing decision as written — *"in a consuming project the tool is absent so
the instruction resolves to nothing."* The tools are **not absent**; they ship
in the plugin cache. They are unreachable.

**Why this item exists now, and what it is subordinate to.** It is the smallest
prerequisite to starting the diagnostic pilot — the first real work item driven
end to end in someone else's repository. Until it lands, a pilot measures the
plumbing rather than the product. It is a prerequisite, not the milestone.

**Winning, in units.** `/kerd:drive` and `/kerd:conductor`, run from a
repository that is not Kerd, invoke the gate with **no manually supplied path**
and surface a **real refusal**.

**The producer's ceremony ruling, recorded verbatim because it is the first live
test of the proportionality dial** (2026-09-02):

> Use route: new, Rigor level: mvp. Do not call it a spike: it changes shipped
> behavior, so a spike route would misrepresent implementation as research.

His declared route through the ladder, rung by rung — quoted so no later sitting
inflates it:

> - **Frame:** users in consuming repos cannot reach Kerd's gate machinery
>   through Drive or conductor.
> - **Viability:** one killer risk — incorrect path/root handling could operate
>   on the wrong repository.
> - **Scope:** only the four gate invocations, focused foreign-repo fixtures, and
>   required release metadata. Explicitly defer progress.py, fidelity.py, hooks,
>   and CI automation.
> - **Design:** one concise keyed decision defining the canonical plugin-root plus
>   target-root invocation. No broad design package.
> - **Handoff:** the first real use of inline-composer — a short spec for the four
>   edits and verification.
> - **Loop:** implement and test both success and refusal from a foreign
>   repository.
> - **Acceptance:** `/kerd:drive` and conductor invoke the gate without manually
>   supplied paths and surface a real refusal.

> Every rung remains real, but none needs to become a large document.

**On nesting a spike**, his boundary: one is justified *only* if execution
uncovers a genuine unknown that must be answered before implementation — the
named candidate being whether `${CLAUDE_PLUGIN_ROOT}` is reliably available
inside skill-invoked shell commands. *"Test that narrowly and return the finding
to the MVP; don't convert the whole item into a spike."*

**The ledger below is named, not qualified.** The frame gate's floor is
presence; every row is refused at the scope gate until it carries Evidence, a
legal State and a countermeasure. Left standing rather than filled with a
plausible disposition, per the 2026-08-31 ruling.

## Grounding

- skills/drive/SKILL.md — the two gate invocations at lines 39 and 76, both bare relative paths; the frame-gate question set is the one rung that already asks something.
- skills/conductor/SKILL.md — the two gate invocations at lines 90 and 150, the pre-flight inventory being where a foreign repo first meets the gates; and line 165, which declares the design and work-handoff stages unowned.
- tools/gates/gate.py — the `--root` resolver whose CLI half shipped 2026-08-14 and which this item proves works against a foreign repo; also `_walk_up_for_git`, the site of the worktree escape defect this item's killer risk generalises.
- hooks/hooks.json — the only place in the plugin where `${CLAUDE_PLUGIN_ROOT}` is proven to resolve at runtime, and therefore the precedent the invocation idiom is built on.
- CONTEXT.md — the 2026-08-06 prompt-layer-only decision whose "the tool is absent" premise this item falsifies, and the 2026-08-27 ruling that version bumps are for real skill-behaviour changes, which this is.
- TODO.md — the `gate.py --root` row narrowed on 2026-08-14 to "the hooks and skills that invoke the tools still assume the Kerd tree", which is exactly this item.
- docs/playbook.md — the cold-eyes trap recording that `tools/design/matrix.py` still resolves through `kit.ROOT`, the same class of defect one tool over.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Incorrect path or root handling makes a tool operate on the wrong repository — reading, auditing or writing against Kerd's tree while the user believes it is theirs, or the reverse | yes |  |  |  |  |  |  |
| `${CLAUDE_PLUGIN_ROOT}` may not be reliably available inside skill-invoked shell commands, so the canonical invocation cannot be written as designed | no |  |  |  |  |  |  |
| The four edits land and the skills still degrade silently, because nothing checks that an invocation resolved — a failed command and an absent one look identical in prose | no |  |  |  |  |  |  |
| Fixing the four gate calls while `progress.py` and `fidelity.py` stay Kerd-pinned leaves a consuming repo half-served, with a working route and no board | no |  |  |  |  |  |  |
