# Category disposition — Kerd

Which of the twenty categories this project owes requirements in. Without this,
an empty category cannot be told from a missing one, so "empty" is not a signal
at all.

`applies` takes no reason. **`n/a` requires one** — the same asymmetry the risk
ledger enforces on `accepted` and the rigor design on a waiver: the cheap state
is the one that must be argued for.

This file is the evidence for the producer's gate **`G1` — "Requirement
disposition declared"**, which every project type in
`docs/product/requirements-project-type-templates.md` requires unless it marks
the gate `n/a`.

> **DRAFTED BY THE MODEL, NOT YET KEYED — 2026-08-08.** The design says this
> file is the producer's, written at opt-in. Every `n/a` reason below is mine
> and reversible; several are genuine judgment calls rather than obvious facts,
> and they are flagged. Read the reasons, not the verdicts.

| Code | Category | Disposition | Reason |
|---|---|---|---|
| BUS | Business | applies | Kerd has success criteria and a stated purpose; that no `BUS` requirement is filed yet is a gap, not an exemption |
| STA | Stakeholder | applies | it has users beyond its producer, and one named contributor |
| USR | User | applies | personas and workflows exist — the producer, and a consuming project's developer |
| PRD | Product | applies | filled |
| FUN | Functional | applies | filled |
| NFR | Non-functional | applies | filled |
| UX | UX/UI | applies | filled — eight requirements, all from 2026-08-08 |
| TECH | Technical | applies | filled |
| INT | Integration | applies | **judgment call** — Kerd integrates with Claude Code's hook and skill surfaces, with git, and optionally with an Obsidian vault. No `INT` requirement is filed, which makes this a gap |
| DATA | Data | applies | it writes and reads durable files, and has retention rules (immutable session logs, overwritten state) |
| SEC | Security | applies | **corrected 2026-08-08 — the earlier `n/a` was falsified by code.** `hooks/session-start.sh:12` `cd`s into `$CLAUDE_PROJECT_DIR` and `:21` runs `git fetch --dry-run` against that repository's own declared remote, on every session, auto-loaded for all users by `hooks/hooks.json` (v0.96.0 — the harness registers it the moment the plugin is enabled, so the exposure is now universal, not opt-in). That is shipped code making an outbound network call inside a repo the operator may not have written. No authentication, credentials or user data are still true; "no network service" was not. No `SEC` requirement is filed, which makes this a gap |
| PRIV | Privacy | applies | **judgment call, reversed from an earlier draft** — the vault's do-not-save markers *are* a privacy control, and session logs capture the producer's words verbatim |
| CMP | Regulatory / Compliance | n/a | no regulated domain, no certification sought, no records-retention obligation imposed by any external body |
| ANA | Analytics / Measurement | n/a | no telemetry, no event collection, no experimentation framework. **Note the near-miss**: Kerd measures itself extensively, but those are stage-1 measurements against declared targets, which live in design packages rather than as analytics requirements |
| OPS | Operational | applies | filled |
| SUP | Support | applies | README, playbook and skill text are support surfaces; no `SUP` requirement is filed, which is a gap |
| TST | Testing / Validation | applies | filled |
| REL | Release | applies | a release checklist exists and is CI-enforced; no `REL` requirement is filed, which is a gap |
| DOC | Documentation | applies | living design docs, dated gate records and a playbook, with rules about which is which |
| POST | Post-Launch | applies | **the identified hole** — `docs/design/funnel-steps.md` leaves the Live stage empty because no source for its steps could be found, and Live *is* post-launch. This category is that stage's missing vocabulary |

**Eleven of the eighteen `applies` categories are unfilled** — `BUS`, `STA`, `USR`, `INT`, `DATA`, `SEC`, `PRIV`, `SUP`, `REL`, `DOC` and `POST`, which is now visible rather
than invisible — the whole point of declaring the disposition. Before this file existed, all ten looked identical to `SEC` being empty, and
only the two `n/a` rows are correct.
