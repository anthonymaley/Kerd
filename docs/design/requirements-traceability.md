# Requirements traceability — slice 1 design

> **STATUS 2026-08-08: the MECHANISM is decided; the rest of the design is
> still BLOCKED.** The build-vs-adopt evaluation below is complete and is the
> repo's first evaluation matrix. It settles which mechanism holds the
> register. The design sections *after* the matrix are the 2026-08-07 package
> that was blocked at cold eyes — 19 findings across eight themes, plus roughly
> fifteen more found on 2026-08-08 by a five-reader terrain pass. They have not
> yet been reworked. **No design GO record may be written against this version.**
>
> Resolved since the block, and recorded here so they are not re-argued:
>
> - **Theme 2** (where the promotion beat sits) — answered by the producer:
>   capture is continuous and free, a durable statement lands as `proposed` the
>   moment it is said; ruling it `final` or `dropped` happens later, on the
>   board. Two beats, not one.
> - **Theme 1** (the killer risk has no countermeasure) — reshaped by the same
>   answer: the machine's role is to **detect that the first beat did not run**,
>   not to perform it. It warns and requires an explicit approval to continue.
>   Its firing frequency is the process-health measurement.
> - **Theme 7** (do dispositions share a table with rigor classes) — dead. The
>   producer's `requirements-project-type-templates.md` settles it from a third
>   direction: `G1` makes disposition a universal gate and the floors are a
>   matrix by project type.
> - **Theme 8** (no dependency field) — subsumed into the row rework, and
>   **not** closed by adopting the producer's universal row, which has no
>   Dependency field either.

Frame: `docs/product/requirements-traceability.md`. Slice 1 only: a durable
input becomes an addressable requirement, in the user's own repo, and the
machinery can read it there.

---

# The mechanism — build or adopt

The producer proposed five external tools on 2026-08-07/08 and set the goal
*"perform requirements management and traceability eval."* All five were
investigated against the repo, most of them installed and run hands-on in
throwaway virtual environments rather than read off a README. Every finding was
adversarially refuted before it was allowed to count.

**The criteria below were declared at 23:52 on 2026-08-07, before any tool
evidence landed.** That ordering is the whole point of the format's file order,
and the draft carrying the timestamp is the record. Had the criteria been
written after StrictDoc's write-back UI was demonstrated, weighting that
capability heavily would have felt obvious and the matrix would have been
rigged in a way no later reader could detect.

**Twenty-three criteria: twelve M, eleven D.** *Effort to build is deliberately
absent* — the 2026-08-03 standing decision that effort is an input measure, and
putting it beside outcome measures makes the grid incoherent and flatters cheap
work. **`Due date` replaced it** (`TST-003`, 2026-08-08): *can it meet the plan
in time* is an outcome measured against a declared bar, which is a legitimate
axis rather than the tiebreaker effort was demoted to. Its target records that
no plan artifact exists to test against — the same missing release-grouping
artifact that `Release grouping` and `TECH-006` both hit.

Three criteria are the producer's own words, 2026-08-07 23:41: *"needs to be git
repo and claude code friendly per project and not scatter arifacts, needs to be
the same files"* — filed as `TECH-007`, `NFR-004`, `TECH-008`, all `final`.

**The matrix is marks-only.** Twelve of twenty-three criteria are M, and a `×`
on an M kills an option regardless of any score, so the marks decide this before
arithmetic could — the standard's own rule, *"marks always, scores when the
stakes are real"*.

**The mark set and its rules are `PRD-008` … `PRD-012` and `UX-001` … `UX-006`**,
stated by the producer on 2026-08-08 and captured as requirements rather than
left in conversation — including the ruling that decides many cells here:
**building the missing piece ourselves is a legal countermeasure**, marked `△-`,
with its cost carried by the summary columns rather than hidden in the mark.

## Criteria

| Criterion | Group | Target / Minimum | Category | Weight |
|---|---|---|---|---|
| The same files | fit | the register IS the project's own committed files — no parallel store, no export-only copy | M | 3 |
| No artifact scatter | fit | requirements live in one declared location; generated output is absent or gitignorable without loss | M | 3 |
| Git-repo native | fit | plain text, meaningful line-level diffs, no binary, no server needed to read it | M | 3 |
| Claude Code friendly | fit | a model reads and WRITES a requirement with Read/Edit alone, no tool invocation in the capture path | M | 3 |
| Belongs to the consuming project | fit | the register lives in the user's repo and Kerd holds none of its own | M | 3 |
| Human-readable with no tooling | readability | a person opening the raw file in git understands a requirement without installing anything | M | 2 |
| Machine-readable by stdlib | readability | a stdlib-only Python script parses the register with the tool NOT installed | M | 2 |
| Installable at all | cost | installs on the developer's own platform via one documented command — not "how much", but "can you get it at all" | M | 3 |
| The producer's ID format | expressiveness | `<CODE>-<NNN>` across all twenty codes, including the two-letter `UX-001` | M | 2 |
| The twenty-category taxonomy | expressiveness | discipline categories as a first-class field, extensible, not invented per project | M | 2 |
| The five-state lifecycle | expressiveness | proposed / qualified / final / superseded / dropped as a closed, validated set | M | 2 |
| Refusal from outside the model | doctrine | a malformed or incomplete register fails a run — not a warning a model may ignore | M | 3 |
| Requirement-to-requirement dependency | expressiveness | one requirement declares its dependency on another ID, and a dangling link is refused | D | 2 |
| Category disposition | expressiveness | all twenty categories declared `applies` or `n/a`-with-reason; an omission is refused | D | 2 |
| Forward trace to code and tests | expressiveness | a requirement links to the commit or test that satisfies it | D | 1 |
| Release grouping | destination | requirements group into named releases as a first-class artifact | D | 1 |
| Generated human view | destination | an HTML view derived from the files, not hand-built | D | 1 |
| Write-back editing | destination | a human changes a requirement's state from the view and it lands in the files | D | 1 |
| Maintenance and survival | cost | actively maintained, or so simple that abandonment costs nothing | D | 2 |
| Added dependency burden | cost | what the option adds BEYOND what the project already needs, weighed against the share of value it buys — an ecosystem-normal install is not a burden; a whole new runtime bought for a fraction of the value is | D | 3 |
| Cost | summary | MONEY. Free to use: no licence fee, no subscription, no per-seat charge — "cant expect anyone to pay to use" | M | 3 |
| Quality | summary | solves the whole need rather than a part of it | D | 3 |
| Due date | summary | usable in the next working session — NO plan artifact exists to test against, so this is the only declared horizon | D | 2 |
| Rating | verdict | the option a producer would pick with everything weighed | D | 3 |

## Options

| Option | Description | Architecture overview |
|---|---|---|
| Build | A markdown register in the consuming project, checked by two new rules on the existing gate audit | docs/design/reqtools-build.svg |
| StrictDoc | Apache-2.0 Python requirements tool; `.sdoc` files, HTML/JSON/Excel/ReqIF export, and a local web UI that writes back to source | docs/design/reqtools-strictdoc.svg |
| Doorstop | LGPLv3 Python tool storing one YAML-or-markdown file per requirement in a linked document tree | docs/design/reqtools-doorstop.svg |
| SphinxNeeds | MIT Sphinx extension defining requirements as directives inside prose documents, with filtering and reporting | docs/design/reqtools-sphinxneeds.svg |
| OpenFastTrace | GPL-3.0 Java requirement tracer reading markdown specifications and linking them to annotated code | docs/design/reqtools-openfasttrace.svg |
| Reqflow | GPLv2+ C++ tracer that finds requirements by regex inside existing documents and reports coverage | docs/design/reqtools-reqflow.svg |

## Evaluation matrix

| Criterion | Build | StrictDoc | Doorstop | SphinxNeeds | OpenFastTrace | Reqflow |
|---|---|---|---|---|---|---|
| The same files | ○ | ○ | △- — its own tree, not your docs | △- — 14 docs need rewriting | ○ | ○ |
| No artifact scatter | ○ | ○ | △- — ~65 files across 20 dirs | △+ — gitignore the build output | ○+ — writes nothing by default | ○ |
| Git-repo native | ○ | ○ | ○ | ○ | ○ | ○ |
| Claude Code friendly | ○ | ○ | △ — the UID is the filename | ○- — directive syntax is fiddly | ○ | △- — the format is ours |
| Belongs to the consuming project | △ — gate.py --root not landed | ○ | ○ | ○ | ○ | ○ |
| Human-readable with no tooling | ○ | ○ | ○ | ○ | ○ | ○ |
| Machine-readable by stdlib | ◎ | △+ — a .sdoc parser is ours | ○ | ○ | ○ | △- — our parser, not the tool |
| Installable at all | ○ | ○ | ○ | ○ | △- — install a JVM first | × — no macOS build exists |
| The producer's ID format | ○ | ○ | △+ — needs -s - at creation | ○ | △- — tilde grammar, second ID | ○ |
| The twenty-category taxonomy | △+ — codes hardcoded in kit.py | ○ | △- — unvalidated, our checker | ○ | △- — unvalidated free tags | △- — the field is ours |
| The five-state lifecycle | ◎ | ○ | △- — BANANA passed, our checker | ○ | △- — closed four, state in tags | △- — the field is ours |
| Refusal from outside the model | △- — no CI outside Kerd | ○ | ○- — structure yes, values no | ○ | ○ | △- — our checker, not the tool |
| Requirement-to-requirement dependency | △+ — field absent from the row | ○ | ○- — UID links, tier-shaped | ○+ — typed links, dangling caught | △ — Depends is inert | △- — our field, our check |
| Category disposition | ○ | △+ — our completeness check | △- — custom attr, our check | △- — our completeness check | △- — no field, separate file | △- — wholly ours |
| Forward trace to code and tests | △- — requirement-to-code unbuilt | ○ | △- — no source-file link | △- — code convention is ours | ◎ | ○ |
| Release grouping | △- — board unbuilt, own slice | △- — custom field, board is ours | △- — no concept, our board | △- — no release object | △- — no concept, we build it | △- — grouping is ours |
| Generated human view | △+ — no register view yet | ◎ | ○+ — publish built in | ◎ | ○ | △+ — CSV only, we render |
| Write-back editing | △- — never built here | ◎ | △- — server read-only | △- — static HTML only | △- — no UI at all | △- — report-only, one-way |
| Maintenance and survival | ◎ | ○ | ○- — recent, one maintainer | ○+ — active at 8.3.0 | ○ | ○- — dead, register survives |
| Added dependency burden | ◎ | △- — 87 packages onto existing Python | △ — 15 packages onto existing Python | △- — packages plus a build pipeline | × — a whole new runtime, for tracing only | × — new toolchain, and uninstallable |
| Cost | ○ | ○ | ○ | ○ | ○ | ○ |
| Quality | △- — four asked-for gaps | △- — three pieces still ours | △- — no validation or board | △- — board and write-back ours | △- — tracer only, register ours | △- — almost everything is ours |
| Due date | ○- — --root and rework first | △+ — install plus a reader | △+ — script the tree layout | △- — greenfield now, rewrite later | △- — JVM plus a register build | △- — a toolchain first |
| Rating | ○ | △- — only if 373 MB is bearable | △- — the format survives, not the tool | △- — heavy shell, good model | △- — only if a runtime is allowed | △- — cannot install on macOS |

## Preferred solution

Build — the register is a markdown file in the consuming project's own git
repo, and it is the only option that satisfies *the same files* by construction
rather than by policy.

**Five of six options are dead on at least one M criterion.** Build is the only
living option, and it carries two `×` — both on D criteria in the *destination*
group, both real losses named below.

**Say plainly which criterion decides this, because one does.** *Install burden
on consuming projects*, M, target "nothing beyond Python 3 stdlib", kills all
five external options on its own: StrictDoc 87 distributions / 373 MB, Doorstop
15 / 28 MB, Sphinx-Needs 30 / 118 MB, OpenFastTrace a Java 17 runtime, Reqflow
an autotools compile against a Homebrew formula Homebrew itself marks
unmaintained. Every one of those lands on **every consuming project**, because
`TECH-001` puts the state in the user's repo, so the tool must run there.

**And say what changes if the producer relaxes that target**, because that is
his call and not the model's. Relax install burden from M to D and StrictDoc
becomes a living option with a genuine case: verified write-back, ReqIF and
Excel export, and a validator that refuses. It would still lose *the same files*
to Build and it would still have no release board — but it would be a real
comparison rather than an elimination. The target was declared before the
evidence; changing it after is the producer's prerogative and nobody else's.

**Two independent findings survived the eliminations and belong in the build:**

- **Doorstop's markdown itemformat** — YAML frontmatter plus a prose body, with
  text and metadata in one file. A stdlib script parsed every field with PyYAML
  *not installed*. That is exactly `TECH-005`'s "read quickly by a person and
  directly by a tool", and it can be implemented without adopting Doorstop.
- **OpenFastTrace's tag convention** — `# [impl->dsn~some-item~1]` is a plain
  comment in Python or shell. *Writing* a tag costs nothing; only *checking* one
  needs the JVM. Kerd can adopt the convention and write a stdlib checker,
  which is the forward-trace half of slice 2 at no dependency cost.

## Proposal and next steps

1. **Build AU7 and AU8 on the existing audit**, on the AU5/AU6 precedent — no
   new CI step. The prototype against the real `kit.py` was 117 non-blank
   non-comment lines plus 11 fixtures, passing first run, including the
   dependency column and two-letter IDs.
2. **Land `gate.py --root` first.** It is a hard dependency, not a follow-up:
   `tools/gates/kit.py:24` derives `ROOT` from the tool file's own path, so a
   consuming project would audit the plugin cache. See the countermeasure below
   — the *script*-location half is undesigned and is the real work.
3. **Adopt the frontmatter-plus-body item shape** for the register's rows and
   the `<CODE>-<NNN>` ID format with the regex widened to `^[A-Z]{2,4}-\d{3}$`,
   which accepts all twenty codes exactly and nothing longer.
4. **Keep ReqIF and `.sdoc` as export targets, never as storage.** If a
   consuming project ever needs interchange, generating it from a markdown
   register is a rendering problem; storing in a tool's format to get it is a
   dependency problem.
5. **The release board is not in this slice**, and after this evaluation we know
   something new about it: no tool on the market that met the other criteria has
   a release-grouping concept either. StrictDoc's own authors use GitHub
   milestones. Building it is not us declining an easy win.

## Risks and countermeasures required

**The killer risk is untouched by this decision, and that is the point of
recording it here.** *Requirements are recorded but the promotion beat is
skipped under time pressure* is unaffected by which mechanism holds the
register — no external tool supplies the countermeasure either. It scores
identically across all six options and must not be charged to Build.

Three risks are specific to the preferred option:

- **The refusal does not travel.** Build's `△` on *refusal from outside the
  model* is the standing decision that Kerd's CI audits Kerd, and a consuming
  project gets the skills' judgment rather than the machine's refusal. Every
  external option scored `○` here. This is the one criterion where adopting
  would genuinely have bought something.
- **The forward trace is built and never exercised.** The `Piece:` trailer
  shipped at v0.91.0 and zero commits have carried one.
- **No write-back and no board, today.** Both are `×`, both are real capability
  the producer asked for, and both are deferred rather than dismissed.

A row is required for every △ on a **MANDATORY** criterion — the marks that
would otherwise have been `×` and killed the option. There are 21. The other 43
triangles sit on DESIRABLE criteria, where the few-word reason in the cell is
the whole statement; the rule was narrowed on 2026-08-08 because demanding
prose for all 64 buries the table in exactly the reading `UX-006` says a table
exists to avoid.

## Countermeasures


| Option | Criterion | Countermeasure | Type | Confidence | Return condition |
|---|---|---|---|---|---|
| Build | Belongs to the consuming project | `gate.py --root <path>`, defaulting to `kit.ROOT`; the library already takes `root` everywhere, so only the CLI entry point pins it | permanent | medium — the parameterisation is proven by the selftest passing temp trees, but the SCRIPT-location half is undesigned: `${CLAUDE_PLUGIN_ROOT}` expands nowhere in this repo and `$CLAUDE_PROJECT_DIR` measured unset | |
| Build | The twenty-category taxonomy | move the twenty codes out of `kit.py` into the project's own `categories.md`, so a consuming project extends rather than inherits a hardcode | permanent | high — the disposition file already has to exist and already lists all twenty | |
| Build | Refusal from outside the model | ship the checker in `tools/` and give it an entry point a consuming project's own CI can invoke | temporary | low — Kerd's CI audits Kerd; a consuming project gets the skills' judgment, not the machine's refusal, and every external option scores ○ here | the first consuming project that runs the audit against itself |
| StrictDoc | Machine-readable by stdlib | write a stdlib parser for `.sdoc` rather than using the JSON export, which requires the tool to run | permanent | medium — the format is regular enough to parse, but this is work the adoption was meant to avoid | |
| Doorstop | The same files | accept the `reqs/**/` tree as the register's declared home; it cannot annotate `docs/product/<slug>.md` at all | permanent | low — a parallel layout by design, and the tool's whole merge story depends on it | |
| Doorstop | No artifact scatter | flatten to one document per category rather than per item, trading merge-friendliness for file count | permanent | low — file-per-item is HOW it earns clean diffs; the evidence states the scatter cannot be configured away | |
| Doorstop | Claude Code friendly | give the model the filename convention and the per-document `.doorstop.yml` so capture is a Write to a computable path | permanent | medium — the UID IS the filename, so the model must compute the next free number before writing | |
| Doorstop | The producer's ID format | pass `-s -` at every document creation; the default separator is empty and yields `UX001` | permanent | high — verified hands-on, `FUN-001` and `UX-001` both produced verbatim | |
| Doorstop | The twenty-category taxonomy | model the categories as documents under one synthetic root, since a second root is rejected, and validate the set with our own checker | permanent | low — the tree is single-rooted by design and a flat taxonomy is not expressible natively | |
| Doorstop | The five-state lifecycle | validate the state field with our own checker, because Doorstop validates no custom attribute values | permanent | high — `state: BANANA_NOT_A_LIFECYCLE_STATE` passed its strictest run, so the gap is measured and the fix is ours | |
| SphinxNeeds | The same files | rewrite the fourteen product docs into directive syntax | permanent | low — the decisive test found ZERO needs in the real docs, and `needs.json` is a build artifact, i.e. a derived second copy | |
| SphinxNeeds | No artifact scatter | gitignore `_build/` and publish the HTML from CI rather than committing it | permanent | medium — works, but the shareable artifact then needs hosting that does not exist | |
| OpenFastTrace | Installable at all | install a system JVM; Java 17 is a common machine-level dependency | temporary | low — no JVM exists on this machine, and a consuming project cannot be assumed to have one | the first consuming project confirmed to carry a JVM already |
| OpenFastTrace | The producer's ID format | keep `<CODE>-<NNN>` in the register we own and carry OFT's `artifacttype~name~revision` as a second, derived ID for tracing only | permanent | low — two ID namespaces is exactly the confusion the register exists to remove | |
| OpenFastTrace | The twenty-category taxonomy | put the category in free-form `Tags:`, since artifact types are tracing-hierarchy levels rather than a taxonomy, and validate it ourselves | permanent | low — tags are unvalidated free text, so the taxonomy would be enforced only by our own checker | |
| OpenFastTrace | The five-state lifecycle | hold the five states in our register and map only the four OFT understands | permanent | low — the closed set is the vendor's and has no documented extension point | |
| Reqflow | Claude Code friendly | author requirements in our own markdown and let reqflow regex-match them | permanent | low — reqflow contributes nothing to authoring; the format would be entirely ours | |
| Reqflow | Machine-readable by stdlib | parse our own markdown with stdlib and use reqflow only for coverage reports | permanent | low — its only structured export is a two-column CSV, produced by a binary that will not install here | |
| Reqflow | The twenty-category taxonomy | carry the category in our own field; reqflow has no schema at all | permanent | low — a requirement is whatever a PCRE regex matched | |
| Reqflow | The five-state lifecycle | carry the state in our own field; the tool's only status is `U` for uncovered | permanent | low — same absence of schema | |
| Reqflow | Refusal from outside the model | run our own checker; reqflow cannot run on macOS at all | permanent | low — the refusal would come from the part we wrote, not from the option being evaluated | |

## The design package — BLOCKED, not yet reworked

Everything below this line is the 2026-08-07 18:56 package. It was written
before the mechanism was settled and before the producer supplied
`requirements-project-type-templates.md` at 20:56. It is retained verbatim so
the rework is a visible diff rather than a replacement, and so the findings
against it stay reachable.

**The alignment artifact for this design is the producer's taxonomy and chain,
not a drawing** (Tony, 2026-08-07: *"i gave you the drawing in text form there,
the categories etc - i approve the drawing not needed"*). Both are in the
frame's `## Value`, enumerable and pointed-at row by row. The standing rule is
that alignment needs a shared structure; a drawing is its usual form, not its
only one.

## What it does

A project opts in by declaring a **register** in its own repo. The register
holds one row per requirement: a stable ID, its category, the requirement in
the producer's words, and exactly one state. Alongside it, the project declares
a **disposition** for each of the twenty categories — `applies`, or `n/a` with a
named reason — so an empty category can be told from a missing one.

Nothing is derived. The register is written by the promotion beat and read by
everything downstream. That is deliberate: this is the one artifact in the
system whose content cannot be derived from disk, because human input leaves no
trace until someone writes it down.

## The three artifacts

All three live in the **user's project**, never in Kerd. Kerd's own copies exist
because Kerd is built with Kerd.

| Artifact | Path | Kind | Written by |
|---|---|---|---|
| The register | `docs/requirements/register.md` | living, overwritten in place | the promotion beat |
| The category disposition | `docs/requirements/categories.md` | living, rarely changed | the producer, at opt-in |
| The catalog (shipped default) | the skill's own text | immutable, ships with Kerd | nobody — it is the standard |

`docs/requirements/` is a new directory and the only structural addition.

> **Finding not yet acted on (2026-08-08):** `docs/requirements/` is the exact
> output path of `capturerequirements`, the skill cut at v0.73.0 — cut partly
> *because* that path produced dated snapshots that violated the date-split
> rule. The standing rule is that dead solutions stay dead unless a named return
> condition fires. The rework owes that named condition, or a different path.

### The register row

```
| ID | Category | Requirement | State | Source |
|---|---|---|---|---|
| NFR-001 | Non-functional | The boundary records everything agreed; efficiency is a tiebreaker, never a reason to record less | final | 2026-08-07 session |
```

> **Superseded 2026-08-08.** The producer's `## Universal requirement row`
> (`docs/product/requirements-project-type-templates.md:162`) fixes fifteen
> fields, of which this row carries five. The ten it lacks are Project Type,
> Subtype, Title, Priority, Owner, Acceptance Criteria, Verification Method,
> Trace Links, Evidence, and Decision / Launch Gate. It is written as a block of
> `Field:` lines, not a table row. Neither document has a Dependency field, so
> adopting the universal row wholesale still does not close theme 8.

- **ID** — `<CODE>-<NNN>`, zero-padded to three. Stable for the life of the
  project; never renumbered, never reused. A superseded requirement keeps its
  ID and changes state.
- **Category** — one of the twenty codes, and its disposition must be `applies`.
- **Requirement** — the producer's words. Compressed for the row, never
  paraphrased into the model's vocabulary.
- **State** — exactly one of a closed set (below).
- **Source** — where it came from, so the full wording is reachable.

### The states

Borrowed wholesale from the risk ledger, which has run since v0.72.0 and is
machine-checked today. Tony's shape: *"any request should be qualified and if
its durable we should make it a requirement, might go through stages to be
final."*

| State | Meaning |
|---|---|
| `proposed` | captured, not yet qualified — the holding state |
| `qualified` | judged durable, wording agreed, not yet signed |
| `final` | the producer's key is on it; it is a requirement |
| `superseded` | replaced by another ID, which is named |
| `dropped` | deliberately abandoned, with a reason |

`proposed` and `qualified` exist because Tony named stages explicitly. Without
them the register would force a request to be either final or absent, which is
the same all-or-nothing failure prose has.

### The category disposition

One row per category, all twenty present, none omittable:

```
| Code | Disposition | Reason |
|---|---|---|
| SEC | n/a | no security surface — a local CLI plugin with no auth, no network, no user data |
| FUN | applies | |
```

`n/a` **requires** a reason; `applies` takes none. Same asymmetry the risk
ledger already enforces on `accepted`, and for the same purpose: the cheap
state is the one that must be argued for.

## The promotion beat

> **Superseded 2026-08-07 late.** The producer split this into two beats:
> capture on the fly as `proposed`, rule to `final` or `dropped` later on the
> board. The single beat below rides conductor's task framing, which fires only
> for new work and only where entry gates exist — so it would have caught none
> of the session's forty-three requirements, which is the evidence the frame's
> own gap 2 records. The paragraph below is retained as the record of what was
> wrong, not as the design.

Where a request becomes a requirement. This is the killer risk's countermeasure
and the only part of the design that spends producer attention.

**It sits inside the framing conversation, not beside it.** Conductor's task
framing already produces `docs/product/<slug>.md` with the producer's key on
`## Value` (v0.94.0). Promotion rides that same beat rather than adding a second
sign-off.

> **False premise, confirmed 2026-08-08.** The original sentence here claimed
> `FUN-001` "deleted the plan gate this same day". It did not: `FUN-001` is a
> decision in state `final` whose execution is deliberately blocked, and the
> plan gate is still unconditional in four places in `skills/conductor/SKILL.md`
> (:173, :215, :218, :246). The no-second-sign-off argument stands on the
> standing decision, not on an executed precedent.

The sequence, from Tony's words:

1. **A request arrives** — in conversation, as it always does.
2. **Qualify it.** Is it durable, or is it about this task only? Durable means
   it constrains future work. `/kerd:interrogate` does exactly this shape for
   risks already.
3. **If durable, draft a row** — proposed state, category assigned, the
   producer's wording preserved.
4. **The producer's key moves it to final.** Read back before writing, as
   `## Value` already requires.

## The aiming fix

`tools/gates/kit.py:24` derives `ROOT` from the tool file's own path. Run from a
consuming project, that resolves to the plugin cache rather than the project.

> **Half-refuted 2026-08-08.** The claim below that "every hook uses
> `${CLAUDE_PLUGIN_ROOT}` to find its script … shipping since v0.19.0" is
> imprecise in three ways, and the token is expanded **nowhere in this repo
> today** — there is no `hooks/hooks.json`, only a template that `tend` rewrites
> into a literal absolute path. `$CLAUDE_PROJECT_DIR` also measured **unset** in
> the tool environment. The *state* half should use
> `git rev-parse --show-toplevel 2>/dev/null || pwd`. The *script* half — how a
> consuming repo locates `gate.py` at all — remains undesigned and is the real
> work in this section.

The change is a CLI argument, not a refactor. `kit.py:22-24`'s own comment says
why: *"The CLI passes ROOT; selftest passes a temp tree instead — every function
below takes `root` as a parameter for exactly that reason."* The library is
already parameterised. Only `gate.py`'s entry point pins it.

- `gate.py` gains `--root <path>`, defaulting to `kit.ROOT` so every existing
  invocation is byte-identical in behaviour.
- Skill text that instructs a tool run passes the project directory.

## Edit map — four files

> **Incomplete, confirmed 2026-08-08.** `tools/gates/README.md` is the AU law's
> declared home, states "the six rules" and "AU1–AU6", and is absent here. At
> least five further places declare the same count and would go stale on
> AU7/AU8, including `skills/slainte/SKILL.md`, two sites in `README.md`,
> `kit.py`'s docstring, and two diagram generators whose strings are baked into
> committed `.svg` artifacts. The heading's own count is therefore wrong.

| File | Change | Why |
|---|---|---|
| `tools/gates/gate.py` | add `--root <path>`, default `kit.ROOT`; thread to every subcommand | the aiming fix; without it the checks below cannot run in a consuming repo |
| `tools/gates/kit.py` | add `REQUIREMENT_STATES`, `CATEGORY_CODES`, and a register/disposition parser + checker | the legal sets and the refusal, beside the ones they resemble |
| `skills/conductor/SKILL.md` | the promotion beat inside task framing | where a request becomes a requirement |
| `README.md` | the capability, and What's New | a user-facing capability must be described in the user's terms |

## The checks

Two, both inside `gate.py audit` (AU7, AU8). **CI gains no step** — they ride
the existing audit, following the AU5 and AU6 precedent.

- **AU7 — the register is well-formed.** Every row has five columns; every ID
  matches `^[A-Z]{3,4}-\d{3}$` and is unique; every state is in the legal set;
  every `superseded` row names its replacement and that ID exists; every
  category code is real and its disposition is `applies`.
- **AU8 — the disposition is complete.** All twenty categories present, each
  `applies` or `n/a`, and every `n/a` carries a non-empty reason.

> **Defect, confirmed twice.** `^[A-Z]{3,4}-\d{3}$` rejects `UX-001` — a shipped
> category code and the frame's own worked example. Checked against all twenty
> codes: the minimum length is 2 (`UX` alone) and the maximum is 4 (`TECH`,
> `DATA`, `PRIV`, `POST`), so the smallest correct fix is
> `^[A-Z]{2,4}-\d{3}$`. Kerd files zero UX requirements, so its own dogfood
> register could never catch this — the thin-dogfood risk biting inside the
> design written under it.

**A project with no `docs/requirements/` is silent, not red.** Declaring is
opting in — the grounding-was-read precedent (2026-08-05), where retrofits were
refused because they manufacture hollow declarations.

> **Contradiction, found 2026-08-08.** The producer's `G1` — "Requirement
> disposition declared" — is a **universal gate** in his own scheme, required by
> every project type unless that type marks it `n/a`. Opt-in and universal
> cannot both hold. The rework must decide which projects are in scope for the
> gate.

## Named answers — the stage-1 measurements

| Measurement (frame, Value) | Target | Named answer |
|---|---|---|
| Durable inputs recorded as addressable rows, not prose | 0 → the session's own count | Kerd's register is seeded at build with the requirements the 2026-08-07 session produced (frame gap 2), which is the first real content and the only honest one available. Verified by `gate.py audit` passing AU7 over a non-empty register. **Limit, named:** this measures that the beat ran once, not that it keeps running; the second is prompt-layer and unmeasurable from disk. |
| Categories whose applicability is undeclared | all 20 → 0 | AU8 refuses any disposition file missing a category or carrying a reasonless `n/a`. Asserted by fixture: a disposition with 19 rows must fail, and one with 20 where `SEC`'s reason is empty must fail. |
| The machinery can audit a project that is not Kerd | no → yes | `gate.py --root <tmpdir> audit` run against a temp tree containing a register, asserting it reports that tree's rows and not Kerd's. This is the existing selftest pattern — `kit` functions already take `root`, and the selftest already passes temp trees. |
| A requirement is answerable by ID | not answerable → answerable from one file | `gate.py` reports a named ID's row, or refuses if absent. Asserted by fixture on `NFR-001`. **Limit, named:** slice 1 answers *what the requirement is*, not *what satisfies it* — the forward wiring to measurements and pieces is slice 2. |
| Existing behaviour unchanged for repos that do not opt in | byte-identical | `gate.py audit` with no `docs/requirements/` present produces the same output as today, asserted by the existing selftest cases passing unmodified, plus this repo's own audit before the register is seeded. |

> **Gap, found 2026-08-08.** The fourth measurement names a capability — report
> a named ID's row — that no row of the edit map builds. The design's own
> two-key GO rule requires every stage-1 measurement to have a named answer *in
> the package*, so that rule is unmet even setting the eight blocking themes
> aside.

## Testing strategy

New fixtures in the existing selftest harness, which is where the legal-set
checks already live: a well-formed register and disposition (pass); a duplicate
ID; a malformed ID; an illegal state; a `superseded` row naming a missing ID; a
requirement in a category dispositioned `n/a`; a 19-row disposition; a reasonless
`n/a`. Plus one `--root` case asserting a temp tree is audited rather than Kerd.

The rigor level is `mvp` and this is its honest disposition:

- **Measured** — the five rows above, all diff- or fixture-scoped.
- **Waived by name** — that the promotion beat is actually *used* in later
  sessions. No harness can observe a conversation, and a model choosing to
  comply is not a check. The observation is the first session after ship that
  produces a durable requirement; recorded in that session's log. This is the
  killer risk's residue and it is stated rather than designed away.

## Out of scope, named

- **The forward wiring** — requirement → measurement → piece. Slice 2. Building
  both halves at once means neither gets a real test.
- **Project-type templates and per-level floors.** ~~The same object as
  `rigor-level` slice 2, designed and unbuilt. Two mechanisms declaring what a
  project owes would disagree.~~ **Reason void as of 2026-08-07 20:56** — the
  producer supplied the mechanism, so there are no longer two peers that could
  disagree, and `Rigor level` becomes derived from project type. The exclusion
  may still stand for slice size; it must be re-argued on that ground.
- **Any retrofit of the twenty existing slugs.** Manufactures requirements
  nobody stated. (Note: there are **13** product docs, not 20; 22 slugs exist on
  the board and 9 have no product doc.)
- **The top and bottom of the chain** — Business Goal, Stakeholder Need,
  Post-Launch Metric. Recorded in frame gap 6; slice 1 builds only the link
  where the break is.
- **Release planning.** This makes it expressible; building it is its own work.
- **Rendering the register on the journey page.** The page should render
  something that exists.
