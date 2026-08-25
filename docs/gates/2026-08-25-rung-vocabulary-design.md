---
route: new
stage: designed
---

# Design GO — rung-vocabulary, 2026-08-25

**Clock:** 2026-08-25 10:30 EDT

Design approved — Tony's key, 2026-08-25 morning sitting. Package:
`docs/design/rung-vocabulary.md` with two drawings beside it, both resealed at
this gate: `the-ladder` (`fp:e2e788033798`) and `rungs-and-artifacts`
(`fp:8daab36a9d76`).

**The GO waited on a correction the producer made to a drawing he had already
sealed.** Two days earlier both views were sealed and the item sat at design.
Reading them again, he stopped the session: *"scope, that is not a risk ledger.
its where we lock in what we want, what features etc... that will go into design
and then loop."* `tools/gates/kit.py` confirmed the mismatch — `kit.py:627` gates
the scope rung on `## Risk ledger` while `kit.py:643` gates the **design** rung
on `## Release slice`, so the machine checked *risk* where scope belonged and
checked the commitment one rung late. Both seals were broken and remade.

**What the GO covers — the four things design settles:**

1. **Acceptance creates READY-TO-RELEASE, and the wording must stop implying
   finality.** His ruling: the producer is not declaring the work *"done forever"*
   or *"released"*; they are declaring it **fit to release**. So: `stage:` is
   `ready-to-release`, the record is `docs/gates/<date>-<slug>-acceptance.md`,
   the required section is **`## Release condition`** — not `## Done condition` —
   and prose says *"accepted as ready for release"*, never *"done"*.
2. **The `stage:` values, one per gate:** `framed`, `viable`, `scoped`,
   `designed`, `handed-off`, `looping`, `ready-to-release`. Four change; two of
   the four (`contracted`, `building`) touch nothing, being legal values no work
   record has ever used. The migration is eight files.
3. **`loop` stays `loop`.** `learn` refused — no evidence arrived, and `learn`
   names a hoped-for side effect rather than the mechanism, which is the class of
   name the currency rule was written against.
4. **Ready-to-release becomes DERIVED, not declared.** `STAGES` already ends in
   `done` and six work records declare it, but `route()` never reads `stage:` at
   all — so doneness was typed by a human and derived from nothing, at the one
   position where the iron rule matters most. `route()` gains a terminal case:
   when every rung's inputs exist, including the acceptance record, it reports
   `ready-to-release` rather than naming the last rung again.

**The frame's headline claim is struck.** *"This restructure changes no
machinery"* was true of the `build`/`goal`/`loop` fold it was written about and
false of the item — `## Release slice` moves a gate and is renamed `## Scope`,
and viability gains a check it has never had. Struck in place with its
replacement named, per Law 4.

**The session's own fix was refuted before it landed, and that is the most
useful thing this gate produced.** Asked where the risk ledger belonged, the
model's instinct was viability. An independent top-tier call was made
specifically to refute it and did, on fetched evidence: Stage-Gate puts the named
risk assessment in Stage 2 alongside product definition; PRINCE2 creates the Risk
Register at initiation alongside the scope; ISO/IEC/IEEE 29148 carries no risk
section at all. **You cannot qualify the risks of an undefined thing.** So risk is
checked twice at two depths in one section — viability wants killer risks
**named**, scope wants **every row qualified**. Evidence tiers are stated rather
than smoothed: 24748 was reached only as far as its official preview.

**The machine key is met at three of five, and the two gaps are declared rather
than invented.** Two of the frame's stage-1 measurements — *rung names readable
across all six work types* and *rung names a newcomer can search* — are judgments
no checker can make. They are recorded as unmeasurable rather than given a number
written after the fact.

**A visible regression is declared here rather than discovered on the board:**
five work records carry `## Value` and no risk ledger. They report
`enters at: slice` today and will report `enters at: viability` once killer
risks are required. That is the truth arriving, not a defect.

**Four factual errors were found auditing the drawings against the code** — an
overclaim that the Value check tests units (it tests existence), an omitted
`## Done condition` requirement, a wrong verdict calling `contract → handoff`
cheap when the word is a generator filename and a rung key in three more, and new
and moved checks being visually indistinguishable from existing ones. All four
came from reading `kit.py` line by line after the producer asked whether the
descriptions were correct.

Hands to CONTRACT.

---

## Amendment — 2026-08-25, at the contract rung

**Clock:** 2026-08-25 10:51 EDT

**The declared regression above is wrong and is corrected here rather than
rewritten above.** The record said *"five work records carry `## Value` and no
risk ledger. They report `enters at: slice` today and will report
`enters at: viability`."* The composer checked it against the tree while writing
the contract spec, and it is wrong three ways:

- **Four such records exist, not five.** The design listed four names and asserted
  five, absorbing the shortfall in the phrase *"and one more"*. There is no fifth.
- **Three of the four are `route: spike`** — `diagram-toolkit`,
  `requirements-view`, `standards-grounding` — and a spike bypasses the ladder
  entirely, so they cannot regress.
- **The one that can move is `requirements-project-type-templates`, and it does
  not move where the record said.** It reports `enters at: viability` **today**,
  not `slice`, and will report **`frame`** — because `enters_at` names the
  deepest *passing* rung, not the next rung to do. The original sentence read the
  field backwards.

**The true declared regression is one record, viability → frame.** Every other
ledger on disk already names at least one killer risk, so nothing else moves. No
exemption is added.

**A second error, same class:** the design package cited a function `stage_ahead`
in `tools/gates/kit.py` as the check that refuses a declared stage without its
artifacts. **No such function exists.** The mechanism is the AU2 audit rule whose
message reads *"stage ahead of its artifacts"* — a phantom symbol invented
because the message reads like a function name. It passed `## Grounding` because
AU5 resolves file *paths* and never symbols inside a line.

**One finding returned by the composer is itself wrong, recorded so nobody
"corrects" a correct number.** It reported the design's *"19 uses of `handoff`
across `skills/`"* as drifted to 15. Measured: `grep -roni 'handoff' skills/`
returns **19**, exactly as written. 15 is the count for
`skills/switch/SKILL.md` alone. The conductor made the mirror-image mistake an
hour earlier — a case-sensitive grep returning 16 — and nearly reported the frame
as wrong on the same number.

**Why this is appended rather than fixed in place:** gate records are immutable by
contract. A record that quietly grew correct would leave nothing to learn from,
and the failure here — a count asserted ahead of the list supporting it, with the
shortfall hidden by a vague phrase — is the same class as the four phantom
dependencies of 2026-08-14. It reached an immutable record, which is exactly how
far it should be visible.
