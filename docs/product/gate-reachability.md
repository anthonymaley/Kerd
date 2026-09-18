---
route: new
stage: ready-to-release
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

**Reframed 2026-09-18: Conductor, not Drive.** Conductor replaced Drive
(`docs/decisions.md`, 2026-09-18 13:08). Conductor's rewrite had also stopped it
calling the checks, so the frame's four invocations no longer exist as written;
two remain, both in Drive, which is being removed. The value is unchanged: a user
in their own repository gets a real answer about where their work stands, with no
path typed. Winning now reads: **Conductor, run from a repository that is not
Kerd, asks that project which step a piece of work is on, names missing
groundwork before moving on, and reads nothing of Kerd's own tree.**

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
- docs/decisions.md — the 2026-08-06 prompt-layer-only decision whose "the tool is absent" premise this item falsifies, and the 2026-08-27 ruling that version bumps are for real skill-behaviour changes, which this is.
- TODO.md — the `gate.py --root` row narrowed on 2026-08-14 to "the hooks and skills that invoke the tools still assume the Kerd tree", which is exactly this item.
- docs/playbook.md — the cold-eyes trap recording that `tools/design/matrix.py` still resolves through `kit.ROOT`, the same class of defect one tool over.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Risk evidence | Severity | Treatment | Countermeasure | Treatment evidence | Review trigger |
|---|---|---|---|---|---|---|---|---|---|
| Incorrect path or root handling makes a tool operate on the wrong repository — reporting against Kerd's tree while the user believes it is theirs, or the reverse | yes | A gate that lies. The user is told their repo's rung when the tool read Kerd's: a false pass at any rung, or a refusal citing files that are not theirs. **Measured read-only for the four in-scope calls** — `gate.py` contains no write calls and `kit.py`'s only non-selftest write is the seal path (`kit.py:670`), which this item does not wire — so the impact is a false verdict, never data loss. Against this item's declared value it is still the worst outcome available: reachability that lies is worse than reachability absent | Medium-high without the countermeasure. Two distinct roots are live at once — the plugin root locating the tool, the target root locating the data — and conflating them is the single easiest error in the change | Measured 2026-09-02: `gate.py`'s own resolver already walks OUT of a git worktree into the parent repo (`_walk_up_for_git` tests `isdir('.git')`, false when `.git` is a worktree file), and the defect has fired once — a review subagent's call bound to the live tree and reverted in-flight work. Read-only status verified by grep across `gate.py` and `kit.py`, not assumed | fatal | countermeasure - permanent | **Classified fatal on the producer's ruling, 2026-09-02: impact >= declared value, and a gate reading the wrong repository defeats this item's entire declared value.** His reasoning is the transferable half — *"the countermeasure being cheap and permanent affects treatment, not impact classification. Using it to avoid fatal would make the state depend on how inconvenient the parser's consequence is."* The treatment, unchanged and still real: every wired invocation passes `--root` explicitly, ambient resolution is never relied on, and two fixtures run in opposite directions — a foreign-repo call reports the foreign repo's state, and no foreign-target call ever returns a Kerd-rooted answer. **Viability refuses until the policy conflict this exposes is resolved as its own decision** (CONTEXT.md `## Open Questions`, 2026-09-02); it is not reinterpreted here to keep the critical path moving | skills/conductor/scripts/tests/test_step_check.py — --root fixtures in both directions, per the 2026-09-02 treatment ruling: from inside Kerd against a separate project (never answered from Kerd) and from inside that project against Kerd (never answered from the project); each fails when --root is dropped (negative controls run 2026-09-18). Released in 0.137.0/0.137.1 | Fires the moment any *writing* subcommand (`seal`) is wired into a skill invocation — the risk changes class from false report to data change, and this row must be re-qualified before that lands |
| `${CLAUDE_PLUGIN_ROOT}` may not be reliably available inside skill-invoked shell commands, so the canonical invocation cannot be written as designed | no | The four edits cannot be written as designed. The fallback is a path the user supplies by hand, which is the acceptance criterion inverted — "without manually supplied paths" is the thing being bought | Answered 2026-09-18. Low, for skill text: the placeholder resolves where it is written in a skill's main instructions. Certain, for a reference file or a shell variable: it does not resolve there | Measured 2026-09-02: `${CLAUDE_PLUGIN_ROOT}` appears in skill text **zero** times across all ten skills; its only proven use anywhere in the plugin is `hooks/hooks.json`; **measured 2026-09-18**, one headless run of a throwaway plugin (`claude -p --plugin-dir`): in `SKILL.md` text it arrived as the install path; in the skill's `references/` file it stayed literal; as a shell variable it was unset. Consistent with the plugins reference: "Skill and agent content: anywhere the placeholder appears"; "They aren't present in the environment of commands Claude runs through the Bash tool" | fatal | countermeasure - permanent | Write the plugin path only in a skill's main instructions (`SKILL.md`), never in a reference file or as a shell variable; the invocation passes the target repository explicitly | skills/conductor/scripts/tests/test_step_check.py — the fixture runs the command exactly as written in Conductor's SKILL.md, placeholder filled as Claude Code fills skill text, and it resolves; the placeholder appears nowhere under references/. Released in 0.137.0 | Fires if Claude Code changes where plugin placeholders resolve, or if the invocation is moved into a reference file |
| The four edits land and the skills still degrade silently, because nothing checks that an invocation resolved — a failed command and an absent one look identical in prose | no | A later regression reintroducing the defect would be invisible. The skills would fall back to prose exactly as they do today, and nothing on disk would catch it on any subsequent change | High over time. Nothing checks that a skill's invocation resolved, which is this repo's standing finding that skill text cannot enforce on itself | Measured: today's failure mode IS silence — the bare relative path yields *No such file*, the skill continues in prose, and nothing is recorded | non-fatal | countermeasure - temporary | The foreign-repo fixture is the check: it asserts the project's step and its named gap are surfaced (`enters at:` and the `need:` line), so a regression to prose fails the fixture instead of passing quietly. Reworded 2026-09-18 from "asserts a real refusal": the agreed scope names the gap and offers it rather than refusing. Temporary because a fixture proves the wiring at build time and not at use time |  | Fires if the fixture is removed or made non-blocking, or when automatic hook/CI enforcement is taken as its own product decision |
| Fixing the four gate calls while `progress.py` and `fidelity.py` stay Kerd-pinned leaves a consuming repo half-served, with a working route and no board | no | A consuming repo can walk the rungs but cannot see position. Switch-in there recovers the narrative and not the location — the half of the session handoff the standing decision says the three files carry worst | Certain. This is the deliberate scope boundary, not a risk of failure | Measured 2026-09-02: `progress.py` accepts no `--root` (passing one prints usage and exits 2); `fidelity.py:50` pins `ROOT` to the tool's own file path, so inside a plugin cache it audits the cache | non-fatal | accepted | None in this item, deliberately. The deferral is explicit in the producer's scope ruling and is what keeps the prerequisite proportionate |  | Fires when the diagnostic pilot reaches its first session boundary and needs a board, or at the pilot's findings — whichever comes first |

## Scope

The smallest valuable increment, agreed by Anthony 2026-09-18 13:15 ("yes") against
`docs/work/gate-reachability/scope.html`: **Conductor, in the user's own project,
knows which step a piece of work is on and does not move past missing groundwork
silently.**

In scope:

- Conductor asks the user's project where a piece of work stands when it picks the
  work up, and before it starts a build, reading that project's records and never
  Kerd's.
- When groundwork for the next step is missing, Conductor names what is missing and
  offers to do it. The person can still choose to go ahead; that choice is recorded
  in the work record, never taken silently. This replaces a flat refusal inside a
  conversation, by the producer's decision.
- No path typed: the plugin locates its own checks from Conductor's main
  instructions (row 2's treatment).
- A foreign-repo fixture: one pass and one named gap, from a repository that is not
  Kerd, proving neither reads Kerd's own files (row 1's treatment).
- Release metadata.

Deliberately excluded:

- Drive: replaced by Conductor; removing the skill is its own later release.
- `progress.py`, `fidelity.py`, hooks and CI automation (the producer's 2026-09-02
  scope ruling, unchanged).
- Small standalone fixes: Conductor keeps them direct, with no step check.

Rigor level: mvp
