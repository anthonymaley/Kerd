# Requirements — prior art

**Law 4 step 1: assess and learn from industry standards, leading approaches,
emerging approaches.** Commissioned 2026-08-14 after Tony stopped the requirement
shape draft with *"dont just take 'he asked for them' as fact that is the best
way… lets not invernt fire to make meal, lets turn on the stove to cook one."*

Three researchers, each barred from reading this repo so none could be anchored
by what we had drafted. Briefs were widened mid-flight after Tony's correction
that the question set itself was a cage: *"dont limit the research to mapping ID
schemas, status names etc to how we think — lets see how they manage
requirements and then decide what we do from there. maybe we are missing
something."*

**Status: findings only. No decision has been taken.** Steps 2–5 of Law 4
(decide what fits · adopt or be inspired · design for gaps · build the gaps)
have not run.

---

## The premise was wrong, and that is the headline

We assumed a requirement is **a record with fields**. Across both completed
territories, that is a *minority* position.

| System | What a requirement actually is |
|---|---|
| Doorstop | an object in a database — one YAML file per item, filename = ID |
| StrictDoc | a node in a **document** with a typed grammar |
| Sphinx-Needs | an **annotation embedded in prose** — the document is primary |
| OpenFastTrace | **nothing it owns** — a graph of tagged fragments across markdown, source, XML. OFT owns only the *link topology* |
| Reqflow | text in documents it **cannot write and does not structurally parse** — regexes scrape IDs from `.docx`/`.pdf` |
| ADR | a **decision**, past tense, immutable, rationale-bearing |
| RFC / PEP | an entry ticket to a **process** |
| BDD | a **behaviour illustrated by an executable example** |
| Jira / Linear | a unit of **assignable work** |

Every documented failure of trackers-as-requirements traces to that last
mismatch.

---

## The document-versus-database trilemma

Every corner bleeds, and each project's densest bug cluster is the cost of its
choice.

- **Database** (Doorstop) — files are unordered, so document order must be
  re-encoded as a `level:` attribute. That reinvention is its worst bug cluster:
  issues 246, 219, 229, 706, all reorder/level defects.
- **Document** (StrictDoc) — keeps narrative order, pays with no incremental
  rebuild: *"With a project tree of 100 documents with 100-400 nodes each, the
  page start takes 10 seconds"* (issue 2428).
- **Graph** (OpenFastTrace) — refuses to own the container, escapes both, and
  pays by having **no reviewable narrative at all**.

**Performance is a universal wall**, and always the same cause — full rebuild
from the filesystem. Doorstop issue 430: *"the stateless command line tool…
has to load everything from the file system in each invocation"* and *"not
written with performance as a goal"*; strains near 2000 items. Sphinx-Needs
issue 1082: a 130 MB `needs.json` for a project *"still in incubation phase"*.

---

## IDs

**The scale lesson, stated by the modern-practice researcher:** *opaque +
sequential + never reused is the only scheme that survives. Every scheme that
encoded meaning in the identifier eventually had the meaning change.*

- `ADR-0001`, `PEP 8`, `RFC 2119` — sequential, permanent, deliberately opaque.
  The number never encodes a claim that can go stale.
- **Jira `PROJ-123`** — project-scoped, and the prefix is the bug: renaming a
  project key rewrites every issue key; moving an issue between projects
  reassigns it.
- **Linear `ENG-123`** — scoped to the **team**, not the project, so work moves
  between projects without losing identity. A deliberate correction of Jira.
- **OpenFastTrace `req~login.backoff~1`** — type, dotted name, **revision as
  part of the identity**.
- **Doorstop `REQ001`** — tool-assigned `max(number)+1`; the ID *is* the
  filename; numbers can be reused after deletion (issue 84).
- **Sphinx-Needs** — auto-ID is a **hash of the title**, so renaming the title
  silently changes the ID.
- **StrictDoc** — no format enforced; renaming a UID while preserving inbound
  links has been an open issue since 2023 (1360).

---

## Status — no convergence on values, total convergence on structure

**The values disagree completely:**

- **OpenFastTrace** — a real validated enum: `APPROVED`, `PROPOSED`, `DRAFT`,
  `REJECTED`. Unknown values throw. Default `APPROVED`.
- **StrictDoc** — `STATUS` is a free string. A `'Draft' | 'Active' | 'Deleted'`
  rule exists in `grammar.py` and is **never wired into parsing** — dead code.
- **Sphinx-Needs** — validation **off by default**; populate `needs_statuses`
  and an unknown value halts the build. No shipped defaults.
- **Doorstop** — **no status field at all.** Booleans only: `active`,
  `derived`, `normative`. Its position: fingerprints and links already encode
  what a lifecycle would say, so a status field is bookkeeping that drifts.
- **PEP** — Draft, Active, Accepted, Provisional, Deferred, Rejected, Withdrawn,
  Final, Superseded.
- **ADR (Nygard)** — proposed, accepted, deprecated, superseded.
- **Jira** — Open → In Progress → Resolved → Closed (+ Reopened).
- **Linear** — Backlog, Todo, In Progress, Done, Canceled.

**The structural convergence is the finding:** every tracker family
independently arrived at a **category layer of three to six buckets beneath
arbitrarily many display names**. Jira rolls every status into To do / In
progress / Done; Linear into six types. Names vary per team; the categories do
not.

**The verdict on half-enforcement, verbatim from the docs-as-code researcher:**

> The two tools that added a status field made it unenforced, which is the worst
> of both worlds: it looks like a contract and isn't one.

### Accepted versus Final — the question Tony asked, answered

In PEP practice these are **genuinely different states**: **Accepted** means
approved but not yet shipped; **Final** means implemented and released.
Standards-track PEPs maintain both. Informational and Process PEPs use **Active**
instead and never reach Final.

**The rule that falls out: keep two states only when implementation can lag
approval.** And the consequence is directly measured — **ADRs collapse the two
(no ADR status distinguishes "decided" from "actually built"), and that collapse
is precisely their documented drift failure.**

---

## Versioning and supersession — four live models

1. **Revision inside the identity** (OpenFastTrace). A child writes
   `Covers: req~login~2`; bumping the parent to `~3` mechanically invalidates
   every stale link. Human-declared: the guide says explicitly *don't* bump for
   cosmetic edits. Cannot detect an unbumped change — pure discipline.
2. **Content fingerprint** (Doorstop). `Item.stamp()` hashes
   `[uid, text, ref, references, links]` → SHA-256 → base64. Mismatch =
   *"unreviewed changes"*; re-approve with `doorstop review`. `active`,
   `derived`, `normative`, `level`, `header` are **deliberately excluded** so
   metadata edits do not nag. **The configurability is the sophisticated part —
   "what counts as a material change" is a project decision**, set in
   `.doorstop.yml`.
3. **New record plus pointer** (PEP `Superseded-By:`, MADR *"superseded by
   ADR-0123"*). Preserves history; creates chains a reader must walk to find
   current truth.
4. **Amend for minor, new record for substantial** (Rust RFCs). Pragmatic, and
   it hands the minor/substantial line to human judgement.

**Notably**, the largest public ADR collection concedes *"in practice,
mutability has worked better for our teams"* — immutability is a convention
followed partially at best.

**The disagreement between (1) and (2) is about who decides materiality:** the
human, who forgets to declare it, or the machine, which cries wolf on typos.

---

## Links — the strongest convergence in the survey

**All five docs-as-code tools store links in exactly one direction and derive
the reverse.** Nobody stores both ends. The reason is mechanical: two ends means
two files to keep consistent and a merge conflict per link.

Dangling links are a **fatal validation error surfaced in CI with a non-zero
exit** — also unanimous.

Vocabulary: OFT `Covers:` / `Depends:` / `Needs:`; StrictDoc `Parent` / `Child` /
`File` with optional `ROLE`/`REVERSE_ROLE`; Sphinx-Needs `links` /
`parent_needs`; Doorstop `links` only.

**OFT ships the richest link-state vocabulary anyone has**: `COVERS`,
`PREDATED`, `OUTDATED`, `AMBIGUOUS`, `UNWANTED`, `ORPHANED`, `COVERED_SHALLOW`,
`COVERED_UNWANTED`, `COVERED_PREDATED`, `COVERED_OUTDATED`, `DUPLICATE`.

**Doorstop stores the parent's fingerprint inside the link**, giving two
independent staleness signals — *"suspect link"* (the parent changed) separate
from *"unreviewed changes"* (this item changed).

---

## Mechanisms our question set had no slot for

The most valuable output of widening the brief.

1. **`Needs:`** (OFT) — a requirement declares **which artifact types must cover
   it** (`Needs: arch, utest`). Coverage completeness becomes *computed* rather
   than asserted.
2. **Typed layers with deep coverage** (OFT) — `req→arch→dsn→impl/utest`.
   Shallow coverage with uncovered descendants is still a defect. Plus
   **forwarding** to deliberately skip a layer.
3. **`derived: true`** (Doorstop) — *"this has no parent, on purpose"*,
   exempting the item from must-link-upward validation. **Directly relevant to
   our 46 unparented requirements, which we have been treating wholly as a
   defect.**
4. **`normative: false`** (Doorstop) — explanatory prose living inside the
   database, exempt from link rules.
5. **`MID`** (StrictDoc) — a **machine identifier separate from the human ID**.
   Without it the tool *"cannot reliably determine whether a node has been
   modified or relocated"*. **Day-one trap: adopt it late and diff fidelity is
   permanently degraded.**
6. **Link roles as data**, and `File` relations anchoring a requirement to a
   code region by `LINE_RANGE` / `FUNCTION` / `CLASS`.
7. **Per-document grammar** (StrictDoc) — the schema is declared *inside the
   document it governs*, not globally.
8. **Query language over embedded annotations** (Sphinx-Needs `needtable`,
   `needflow`, `needfilter`) — prose treated as a queryable database. Plus
   `needservice`, pulling needs live from Jira/GitHub.
9. **`need_part`** — sub-requirements addressable within one requirement.
10. **ID reservation for concurrent authoring** (`doorstop-server`).
11. **Soft delete** (`active: false`) rather than removal.
12. **Rejection as a durable, first-class artifact** (RFC/PEP) — called by the
    researcher *"the single most underrated feature in the whole territory."*
13. **The shepherd / delegate role structure** and a **bounded comment window**
    (Rust's Final Comment Period: ten days, with a disposition of
    merge/close/postpone).
14. **An ADR's real payload is Context, not Decision.** The decision is usually
    visible in the code; the reasoning and the rejected alternatives are not.
15. **`/speckit.clarify`** — force ambiguity to be *named and resolved* before
    implementation rather than silently guessed. Named the highest-leverage
    AI-specific practice found.

---

## Approval fatigue — measured, and it is the sharpest finding for us

Tony named false approval as the central failure (G4) from intuition. It has
been measured.

**"Habituation at the Gate"** (Yu et al., arXiv 2606.22721, June 2026).
Longitudinal within-reviewer analysis: **400 repeat reviewers, 11,429 reviews,
seven months**, AIDev dataset.

- Approval of AI-agent code rose **30.1% → 36.8%** (p < 10⁻⁶)
- Inline comment volume **fell 22%** (p = 0.0014)
- Review latency **rose 3.5×**

Authors' interpretation: *"reflexive habituation under growing workload rather
than rational trust calibration alone."* **Reviewers take longer to get to it
and look less hard when they do — and it gets worse over time, not better.**

**Intercom, from production:** humans default to *"rubber-stamping. Glancing at
a diff, skimming the description, clicking approve"*, and *"human review is not
a guarantee of safety. It never was."* **Their countermeasures are structural,
never exhortative:** the agent **refuses to approve large or complex changes**
(forcing small diffs), every approval is labelled, logged and queryable, and the
shipping engineer stays accountable.

Lineage: Bainbridge, *Ironies of Automation* (1983); Goddard, Roudsari & Wyatt
(JAMIA 2012) on automation bias; Franklin et al. (DeepMind, 2025) *AI Agent
Traps*. The operative claim: oversight collapses when *"approval requests arrive
faster than a human can read them."*

**Calibration, recorded because the researcher volunteered it:** a snippet
claiming oversight intervention success of *"9 to 26% across every oversight
strategy tested"* could not be located or verified. **Do not use it.**

**What this does to our design:** our answer to false approval is currently
presentational — borders, brevity, visuals. The evidence says presentation does
not create scrutiny. The fix is structural: cap what one gate may contain, log
every approval, and require the human to produce *something* rather than a
keystroke.

---

## The warning aimed straight at us

**Adzic's ten-year Specification by Example survey:** only **12%** of teams keep
requirements as text files in version control. **57%** use Jira as primary
documentation. Most teams **abandoned living documentation**.

The researcher's framing: *"this territory has already tried the thing you're
probably about to build, and mostly failed at it for reasons that were social,
not technical."*

### That framing does not survive Tony's reading of it — 2026-08-14 08:43

> what Adzic doesnt say is that the 12% might be the most productive and the 57%
> might not actually know the requirments that are lost to complexity

**The survey measures ADOPTION, not OUTCOME, and the two were quietly conflated
— by the researcher and then by the model relaying it.** "Most teams abandoned
living documentation" is a fact about what teams *did*. It is not evidence about
whether it *worked*, and the numbers are compatible with two opposite readings:

- **The researcher's reading:** the practice failed socially, so most teams
  dropped it.
- **Tony's reading:** the 12% who kept it may be the teams for whom it worked —
  and the 57% on Jira **cannot report the requirements they lost**, because a
  requirement lost to tool complexity leaves no trace in the tool that lost it.

**Nothing in the statistic distinguishes these**, and the second reading has a
structural argument behind it: **the failure is invisible from inside the
population being surveyed.** Asking teams whether they are missing requirements
they do not know about cannot return a number.

This is the same shape as the false-approval failure the same research
documents — the person best placed to report the problem is the one the problem
prevents from seeing it.

**What would actually settle it:** outcome data, not adoption data. None was
found.

**Calibration note, recorded because it is a repeat:** the model passed this
finding on as *"the warning aimed straight at us"* without testing the
inference. A researcher's conclusion is evidence about the researcher's
reasoning, not a fact. The standing guidance is not to take agent output at face
value; this is the second time in two days it was taken at face value and the
producer caught it.

## Jira is ruled out — Tony, 2026-08-14 08:43

> jira is overkill to imo, and not easy to work with, too complex, and cost
> prohibitive, puts dependency on users projects

Four grounds, and the last is the decisive one: **it puts a dependency on the
user's project.** Under Law 1 (Kerd installs into someone else's repo and
operates inside its boundaries), anything Kerd requires is a cost imposed on
every consuming project — the same arithmetic that ruled against StrictDoc's
87 distributions and 373 MB. A commercial, hosted, per-seat dependency is
strictly worse on that axis than a library.

Recorded as a **ruled-out option with its reasons**, so the decision is
reachable rather than re-argued.

Related documented failures:

- **ADRs quietly abandoned** after a few enthusiastic months. *A stale decision
  log is worse than no log, because it gives false confidence.*
- **Drift between ADR and code** — accepted decision, divergent implementation,
  no superseding record.
- **BDD reduced to test syntax** — North's own talk is titled *"BDD Is Not About
  Testing."*
- **Trackers as the map** — Jira *"implicitly teaches everyone to ignore the
  larger vision while focusing on details… There is no whole."* Patton on flat
  backlogs: *"a bag of context-free mulch."* Shape Up's chapter heading is
  literally *"No backlogs."*
- **Linear's answer to rot was not discipline** — they shipped auto-close and
  auto-archive **on by default**.

---

## Where discussion goes

**Universally, discussion lives outside the record and dies there.** PEP
mandates a `Discussions-To:` header; Rust discussion sits in the PR thread and
Zulip. What survives is a *link*, not the argument.

**MADR is the exception** — it compresses the debate into the record itself via
**Decision Drivers, Considered Options, Pros and Cons of the Options,
Confirmation.**

Among the tools: OFT has `Comment:` and `Rationale:`; StrictDoc has repeatable
`COMMENT` fields; Doorstop and Sphinx-Needs have none and defer to pull
requests. **Nobody built threaded discussion.**

---

## The collaboration round-trip

**Everyone treats the source file as the only writable surface and the view as
disposable.** Doorstop's published output is explicitly *"not intended to be
imported into Doorstop."*

**StrictDoc alone writes back** — `strictdoc server`, port 5111, edits land in
`.sdoc` files — and its own maintainers state it *"is not yet hardened against
unsafe use"* and that deploying it as a shared server is *"impractical."* It
**refuses real-time collaboration by design**: *"StrictDoc shall not implement
the real-time editing capability."* A known defect: moving a field in the GUI
silently rewrites it as multiline.

Whether StrictDoc's write-back patches or regenerates whole files is
**undocumented and unverified**.

---

## The researchers' own recommendations

Recorded as *their* opinions, not decisions.

1. **Two artifact types, not one** — a decision record (immutable,
   rationale-bearing, ADR-shaped) and an executable acceptance criterion. **Do
   not build one schema trying to be both.**
2. **Opaque sequential IDs**, never reused, never re-scoped; Linear's
   team-scoping over Jira's project-scoping.
3. **Steal PEP's Accepted-versus-Final split** — the specific mechanism that
   catches the drift ADRs suffer from.
4. **Steal the process, not the template, from RFC/PEP** — named proposer, named
   decider, bounded comment window, and **rejection as a recorded outcome**.
5. **Make approval active and structural** — cap gate size, log approvals,
   require the human to produce something.
6. **Steal `/speckit.clarify`** — ambiguity named and resolved, never guessed.
7. **Don't build a backlog** — accumulated unreviewed intent is a liability.
8. From the tools: take the one-directional link with derived reverse (free,
   unanimous); take Doorstop's narrow-field fingerprint *or* OFT's
   revision-in-ID; take OFT's `Needs:` for computable coverage — **and either
   enforce a status enum or do not ship the field.**

---

## Where ADRs sit in the flow — an observation, NOT a proposal

**Tony, 2026-08-14 08:36:** *"ADR is the requirement in detail when approved."*

**Clarified by him minutes later, and the clarification matters:** *"im not
saying use ADR btw, just noting that ADRs come post requirement approval in
process flow, not saying we need to use them."*

**So this is a sequencing observation about where ADRs fall relative to
requirement approval. It is not a design position, it does not propose adopting
ADRs, and it does not reject the researchers' two-artifact recommendation.**

*Correction recorded: the model first wrote this up as a ruling that rejected
recommendation 1. That was an over-read — the same failure as the C4 "approval"
over-read the previous day, where a single word was inflated into a claim the
producer had not made. Twice in two days, and both times he caught it by reading
what was written rather than either model catching it. **Treat any sentence that
turns one of his observations into a position as suspect until he confirms it.***

**The questions below therefore apply to any model that merges the two — they
are open design questions, not objections to a proposal nobody made:**

- **Immutability.** An ADR is conventionally frozen once accepted, and the whole
  Groundhog-Day defence rests on that. A requirement that continues to version
  (`FINAL v1.0` → `v1.2`) is by definition not frozen. Either the ADR half gives
  up immutability, or a version bump mints a new record.
- **The rejected options.** An ADR's real payload is **Context** — the reasoning
  and what was ruled out. A requirement statement has no natural home for that.
  Under his model it must arrive at approval time and persist.
- **The verification half.** BDD's lesson is that a requirement and its test can
  be the same artifact. An ADR cannot be executed. If the requirement-in-detail
  is ADR-shaped, what carries the acceptance criterion?

None of these refute him; all three are unanswered by the position as stated.

---

# Standards and enterprise tools

ISO/IEC/IEEE 29148, IEEE 830, ReqIF, OSLC RM, DOORS Classic and Next, Jama,
Polarion, INCOSE GtWR.

**Blocked sources, named rather than softened:** `incose.org` returned **403**
for both GtWR summary sheets; `ibm.com/support` returned **403** for the DOORS
absolute-number page; the Springer *Requirements Anti-Patterns* chapter is
paywalled. Claims resting on those are marked below.

## No standard in this territory defines requirement status — the REVIEW has the lifecycle

**This is the strongest finding in the section, and it is a negative one.**

- **29148** — "Status" does not appear in the §5.2.8 attribute list at all. The
  only mention is that the Owner *"reports the status of the requirement."*
- **ReqIF** — none. **OSLC** — none.
- **Jama** — item workflow is configurable, not shipped.
- **Polarion / DOORS Next** — both ship a lifecycle for the **review object**,
  not the requirement. DOORS Next, verbatim: `Draft > In Progress > Reviewed >
  Finalized`, plus `Paused` and `Overdue`, with roles **Approver / Reviewer /
  Optional reviewer**.

**Two independent vendors converged on the same shape: the requirement has no
mandated state machine; the review does. Approval is modelled as an event
happening *to* a requirement, not a field *on* it.**

*Approved and baselined are distinct.* 29148 §3.1.3 defines a baseline as a
*"formally approved version of a configuration item… formally designated and
fixed at a specific time"*, and names four: Functional (requirements),
Allocated, Developmental, Product.

## The mandatory minimum is one field, or zero

| Source | Mandatory fields on a requirement |
|---|---|
| **OSLC RM 2.1** | **Exactly one** — `dcterms:title`. Everything else is Zero-or-one or Zero-or-many, *including* `identifier`. |
| **ReqIF** | **None.** `SpecObject` declares "Attributes: No attributes." All domain fields are user-defined. |
| **ISO 29148** | **None mandated.** §5.2.8.2 is headed "**Examples of** requirements attributes". |

**There is no documented mandatory minimum attribute set anywhere in this
territory, and the most modern spec converged on one field.** Our own draft
carries nine.

## IDs — the verified doctrine

**ISO 29148 §5.2.8.2, verbatim:**

> "Each requirement should be uniquely identified… **Once assigned, the
> identification is unique — it is never changed (even if the identified
> requirement changes) nor is it reused (even if the identified requirement is
> deleted).**"

Immutable, never reused, and the stated reason is tracing. The standard is
deliberately agnostic on meaningful-versus-opaque.

**ReqIF** defends immutability even against tool incompatibility: where a tool
cannot handle the identifier it attaches an `AlternativeID` rather than mutating
it. **OSLC**: identity is the resource URI.

**Universal convergence: every system separates a stable identity from a display
position.** DOORS keeps three — section number (renumbers freely), absolute
number, object identifier. *Whether DOORS' absolute number is editable or reused
after purge is unverified — the IBM page answering it returned 403.*

## Version number is a VOLATILITY SENSOR

29148 lists Version Number as a per-requirement attribute and gives a second
reason beyond bookkeeping:

> "to provide an indication of the **volatility** of the requirement. A
> requirement that has a lot of change could indicate a problem or risk to the
> project."

**A requirement that keeps changing is a risk signal about the project, not just
a record that moved.** Jama versions on any *field value* change; Polarion has no
per-item counter (every save is a repository revision); ReqIF has no version at
all, only `lastChange`.

## Links — the OSLC convergence set

The most recent and most cross-vendor-negotiated answer available. Seven inverse
pairs plus four one-way, all Zero-or-many:

| Paired | One-way |
|---|---|
| `elaboratedBy` / `elaborates` | `validatedBy` |
| `specifiedBy` / `specifies` | `implementedBy` |
| `decomposedBy` / `decomposes` | `affectedBy` |
| `satisfiedBy` / `satisfies` | `trackedBy` |
| `constrainedBy` / `constrains` | |

**Polarion makes the inverse mandatory** — "ID, Name, and **Opposite Name** are
required." That constraint forces you to say what a link means *from both ends*,
which is where sloppy link semantics get caught.

**ReqIF is the outlier:** `SpecRelation` has source, target, type — and **no
predefined types whatsoever.**

**The minimum set everyone reaches independently: parent/child (decomposition),
satisfied-by (implementation), verified-by (test), and a weak catch-all
"relates to".**

## The language linter — highest value-per-effort in the territory

29148 §5.2.7 is **normative and mechanically checkable**. Avoid: superlatives ·
subjective language ("user friendly", "easy to use") · vague pronouns ("it",
"this") · ambiguous adverbs ("significant", "minimal") · ambiguous logic
("and/or") · open-ended terms ("provide support", "but not limited to") ·
comparatives · loopholes ("if possible", "as appropriate") · totality terms
("all", "always", "never") · incomplete references.

And §5.2.4 on modal verbs: **'shall' is binding · 'will' is context · 'should'
is a goal and is NOT a requirement · 'may' is permission · avoid 'must' entirely
(misread as binding) · avoid passive voice.**

Femmer et al. built exactly this as "Requirements Smells" and report **59%
average precision at 82% average recall** (arXiv:1611.08847).

**The researcher's verdict: a greppable word list catching real defects, with no
process, no roles and no tool. It runs on prose in a file.**

## Mechanisms our frame had no slot for

- **TBD / TBS / TBR as first-class closable markers.** 29148: the set *"cannot
  be considered complete until all the TBx designated requirements have been
  resolved."* **A tracked hole is a mechanism, not a smell** — and "no TBx open"
  is a release gate.
- **Rationale as the sanctioned home for excluded design.** 29148: *"All
  assumptions made regarding a requirement **shall** be documented and validated
  in one of the requirement's attributes (e.g., rationale)."*
- **Set-level quality as a separate class from row-level quality** — nine
  characteristics for a requirement (§5.2.5), five for the *set* (§5.2.6).
  Quality is a property of the collection, checked once, not a question asked of
  every row.
- **Two independent ranking dimensions** (IEEE 830 §4.3.5): degree of
  **stability** and degree of **necessity** (Essential / Conditional /
  Optional). **Priority is not one number.**
- **Tailoring as a delete-only operation.** 29148 Annex C: you may delete
  sections; you may not modify them. *"Tailoring is not permitted if a claim of
  'full conformance' is to be made."*
- **Attribute-level declaration of semantic significance** — DOORS' "Affect
  change dates" flag, set on the *attribute definition*, so the schema author
  declares which fields are load-bearing before any automation runs.
- **The link graph as a measurement instrument** — volatility, change rate,
  *"percentage of parents without children"*, *"average number of child
  requirements per parent — an indicator of design complexity"*, TBx closure
  progress.
- **SysML v2 models a requirement as a constraint**, not as text with attributes.
- **29148's primary artifact is a document with a mandated table of contents**,
  not a database. Conformance is to an outline; attributes are one clause,
  explicitly "examples of".

## Named anti-patterns

- **Requirements creep** — 29148 twice: *"excessive uncontrolled changes can
  result in 'requirements creep' that can result in cost overruns, schedule
  delays, design errors, buyer dissatisfaction or even cancellation."*
- **Design inside the requirement** — *"including design solutions in the
  requirements creates the risk that potential design solutions could be
  overlooked or eliminated."*
- **Duplication without cross-reference** — IEEE 830 §4.3.7: *"the same
  requirement should not appear in more than one place… a requirement may be
  altered in only one of the places where it appears."*
- **Suspect-link noise is treated by every vendor as *the* defect.** Jama makes
  triggers per-field; DOORS gates on "Affect change dates" and ships "suspect
  profiles"; IBM holds patents on suspicion management. **If every edit marks
  everything suspect, the flag gets discarded.**
- **Silent trace decay** — *"traces degrade silently as requirements, code, and
  tests evolve independently."*

## Steal / refuse — the researcher's list

**Steal:** the immutable-never-reused ID rule as 29148 states it, machine-minted,
with identity always separated from display position · **the §5.2.7 language
linter** · rationale as a required companion field (*the only attribute that
answers "can we delete this yet?"*) · the four-link minimum with **named
inverses** · declare which fields are load-bearing · TBx as a closable marker
with "none open" as a release gate · set-level characteristics as a review
checklist asked once · tailoring-by-deletion.

**Refuse:** a configurable workflow engine · per-requirement version counters
(git versions the file — but *keep the volatility signal*, derived from
`git log`) · automated suspect-link propagation (steal the declaration, refuse
the graph-walker) · the five-document information-item set · separate review
objects with their own lifecycles, e-signatures, baselines-as-artifacts · **a
large attribute set** (flagged by the researcher as their own opinion, resting
on the mandatory-minimum trio rather than on INCOSE authority).

**The sharpest strategic point in the whole survey:**

> OSLC — the most recent and most industry-negotiated spec in this territory —
> concluded that a requirement is a **URI, a title, and typed links**. Everything
> else is local. That is the evidence-backed floor. 29148's language criteria are
> the quality bar you apply to the title's prose. **The register is the cheap
> part; the linter and the link semantics are where the value is.**

---

---

# Agent skills and AI-vendor practice

superpowers read **from source on disk** rather than recalled, plus Claude Code,
GitHub Spec Kit, AWS Kiro, OpenAI, Windsurf and Devin.

*(A note on provenance: the harness flagged this researcher's output as
instruction-shaped because it quoted Claude Code's `bypassPermissions` mode name.
Benign — a quotation inside a finding, treated as data.)*

## superpowers, end to end

Source: `~/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.6/skills/`
(a newer 6.2.0 also present).

**Pipeline:** `using-superpowers` → `brainstorming` → `writing-plans` →
`subagent-driven-development` *or* `executing-plans` →
`finishing-a-development-branch`, with `test-driven-development` and
`verification-before-completion` binding throughout.

**Two artifacts on disk, both committed: a spec and a plan. There is NO
requirements file.** Intent goes conversation → design doc → plan. The spec has
**no template** (shipped ones use ad-hoc headings: Motivation, Architecture,
What Changes / What Stays the Same, What This Drops, Testing). The plan *is*
templated: mandatory Goal / Architecture / Tech Stack header, a File Map, then
`### Task N` blocks with Files and checkbox steps that are literally the TDD
cycle.

**6.2.0 is drifting toward requirements**: it adds `## Global Constraints` —
*"The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules… Every task's requirements implicitly include this
section"* — and per-task `**Interfaces:** Consumes / Produces`.

**Three human gates, all conversational, NONE RECORDED.** A `<HARD-GATE>` in
brainstorming: *"Do NOT invoke any implementation skill, write any code… until
you have presented a design and the user has approved it. This applies to EVERY
project regardless of perceived simplicity"* — with an anti-rationalization
section: *"'Simple' projects are where unexamined assumptions cause the most
wasted work."* Then section-by-section design approval, then a written-spec gate.
**The human reads and says yes. The approval leaves no artifact — only the git
commit.**

**The real rigor is agent-to-agent, not human-to-agent.** Per task: implementer
→ **spec-compliance reviewer** → **code-quality reviewer**, each in a
fix-and-re-review loop. The spec reviewer is adversarial *by instruction*:

> "The implementer finished suspiciously quickly. Their report may be
> incomplete, inaccurate, or optimistic… DO NOT: Take their word… DO: Compare
> actual implementation to requirements line by line… Look for extra features
> they didn't mention."

Implementers must report `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`,
and the controller must act — *"**Never** ignore an escalation or force the same
model to retry without changes."* Escalation is destigmatized: *"It is always OK
to stop and say 'this is too hard for me.' Bad work is worse than no work."*

**Verification, verbatim:** *"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION
EVIDENCE"* · *"Claiming work is complete without verification is dishonesty, not
efficiency"*. Its table demands a **line-by-line checklist** for "requirements
met", states that **"tests passing" is explicitly insufficient**, and requires
**"VCS diff shows changes"** rather than the agent's own report.

**Deliberate absences worth noting:** plan self-review is *not* delegated
(*"a checklist you run yourself — not a subagent dispatch"*) — yet a shipped
design doc specifies exactly such a reviewer, designed then dropped. Plan
placeholders are **failures**: *"'TBD', 'TODO', 'implement later'… 'Add
appropriate error handling'"*. And agreement theatre is banned outright:
*"NEVER: 'You're absolutely right!'… 'Great point!' (performative)"*.

## What this territory does that requirements management never would

- **Instruction as behavioural countermeasure.** Rules written against *the
  agent's own rationalizations* — excuse→reality tables (*"I'm confident |
  Confidence ≠ evidence"*), hard gates, "Iron Law". Rules for a mind that will
  try to talk itself out of them, not for a process.
- **The reviewer is instructed to distrust**, and it is cheap enough to run per
  task.
- **Context isolation as quality control** — *"They should never inherit your
  session's context or history — you construct exactly what they need."*
- **Cost-tiering the gate** — cheap model for mechanical work, most capable
  model for architecture and review.
- **PROGRAMMABLE APPROVAL.** Claude Code hooks return
  `{"permissionDecision": "allow"|"deny"|"ask", "permissionDecisionReason": …}`
  on `PreToolUse`; `Stop`, `SubagentStop`, `TaskCompleted` are blocking events
  too. **Approval becomes executable policy rather than a request** — which is
  the structural countermeasure the habituation research says is required.
- **Authority as a formal ladder** (OpenAI Model Spec): Root → System →
  Developer → User → Guideline, *"instructions with higher authority override
  those with lower authority"*, and when two root principles conflict *"the
  model should default to inaction."*

**What this territory LACKS, and it is exactly our subject:** requirement
identity (superpowers, Claude Code plan mode and Cursor have **no IDs and no
trace from a shipped line back to the ask** — coverage is "skim the spec, can
you point to a task?", by eye, once) · **no recorded approval** (no who, when,
or what; no diff-since-approval) · no change control · no status on a
requirement · no non-functional vocabulary.

## Vendors

**Claude Code plan mode** — the plan is **conversational, never written to
disk**; approval is a menu. *(Note: `bypassPermissions` disables plan mode's
blocks entirely.)*

**GitHub Spec Kit — the only one with real traceability.** Its spec template
mandates `## User Scenarios & Testing` with prioritised user stories
(`### User Story 1 … (Priority: P1)`, `**Why this priority**`, `**Independent
Test**`, Given/When/Then), `## Requirements` as `- **FR-001**: System MUST …`,
and `## Success Criteria` as `- **SC-001**`. Tasks carry `[ID] [P?] [Story]` —
`T012 [P] [US1]` — **linking every task back to a numbered story.**

Three mechanisms worth stealing outright:

- **`[NEEDS CLARIFICATION: auth method not specified - email/password, SSO,
  OAuth?]` — and it is CAPPED**: *"LIMIT: Maximum 3 [NEEDS CLARIFICATION]
  markers total"*. A bounded ambiguity budget, not an open TODO list.
- **Machine gates rather than human ones** — a generated
  `checklists/requirements.md` the agent self-validates against *"until all
  items pass (max 3 iterations)"*; `/analyze` is *"STRICTLY READ-ONLY"*.
- **`## Constitution Check`** — *"GATE: Must pass before Phase 0 research.
  Re-check after Phase 1 design"* — and conflicts *"require adjustment of the
  spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring."*

Its refusals: no tech stack in the spec, success criteria must be
*"technology-agnostic"*, and tests are *"OPTIONAL - only include them if
explicitly requested"*.

**AWS Kiro — the only hard human loop.** `.kiro/specs/` holds `requirements.md`
in **EARS** syntax (*"WHEN [condition] THE SYSTEM SHALL [behavior]"*),
`design.md`, and `tasks.md`, with **explicit approval checkpoints between
requirements→design and design→tasks**. Its "Quick Spec" mode deliberately
bypasses them.

**OpenAI** — `AGENTS.md` is standing context, not a spec: no IDs, no acceptance
criteria. Codex's approval axis is permissions, not specs.

**Windsurf / Devin** — plans are **persistent markdown**, `@`-mentionable to
resume, human-editable; a larger model revises the plan while the session model
acts, and *"you will be notified when this happens so that you can review."*

---

## Still outstanding

- **The release-and-roadmap question is unanswered by all three reports.** How a
  requirement is linked to a release, a version, or a roadmap; whether release
  membership is stored on the requirement or on the release; what happens to a
  requirement that slips; and whether anything models a roadmap as distinct from
  a release. Asked of the standards researcher; not yet returned. This is the
  open TODO row *"the release-planning artifact"* and Tony's standing position
  that **a release is a grouping, not a time axis**.
- **Agent skills and vendor practice** — superpowers read from source on disk,
  plus Anthropic, OpenAI and GitHub Spec Kit. Dispatched, not yet returned.

## Verification status — carried from the researchers, not smoothed

**Verified from primary text:** ISO 29148 (full standard), IEEE 830, ReqIF v1.2
(OMG), OSLC RM 2.1 (OASIS), SysML v2 review document, Femmer et al., and the
OpenFastTrace / Doorstop / StrictDoc / Sphinx-Needs source files and grammars.

**Verified from vendor docs:** Jama, Polarion, and DOORS' three-way ID,
delete-then-purge semantics, "Affect change dates", baseline sets, review
lifecycle, partial system attributes.

**Practitioner secondary source only:** DOORS Next link-type names.

**Blocked (403), named rather than softened:** DOORS absolute-number editability
and reuse (ibm.com/support); INCOSE GtWR summary sheets (incose.org).

**Unverified — treat as training data:** the GtWR attributes appendix; INCOSE
rule *numbers* (version-dependent: v3.1 has 41 rules, v4 has 42, so v3.1 R41 ≠
v4 R41 — the rule *names* are reliable, the numbers must not be cited untagged);
DOORS Created By / Last Modified By / Last Modified On.

**Paywalled:** the Springer *Requirements Anti-Patterns* chapter.

**Explicitly retracted by a researcher:** a claim of *"9 to 26% oversight
intervention success across every oversight strategy tested"* could not be
located or verified. **Do not use it.**
