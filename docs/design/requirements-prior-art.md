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

## Still outstanding

The **standards and enterprise tools** researcher (ISO/IEC/IEEE 29148, IEEE 830,
ReqIF, DOORS, Jama, Polarion) has not yet reported. Its territory is the one
most likely to change the status and attribute picture again.
