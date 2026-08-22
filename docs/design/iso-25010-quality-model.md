# ISO/IEC 25010:2023 — the product quality model, as the register will cite it

The reference `R-0011`'s quality column stands on. Supplied by the producer
2026-08-22 and corroborated against Sonar's explainer
(sonarsource.com/resources/library/iso-iec-25010-explained/) line for line,
and against the two secondary sources the spike's product player read (arc42's
2023 changelog, Pacific Cert's guide) on every headline change.

**Evidence tier: corroborated secondary — four sources agreeing, none of them
the ISO text.** Every ISO mirror refused the fetch. If the ISO text is ever
read and differs, this file is corrected and the correction dated; nothing
built on it is assumed right by having been written first.

## Product quality — nine characteristics

| # | Characteristic | Sub-characteristics | Changed in 2023 |
|---|---|---|---|
| 1 | **Functional suitability** — provides functions that meet stated and implied needs | completeness · correctness · appropriateness | — |
| 2 | **Performance efficiency** — performance relative to resources used | time behaviour · resource utilization · capacity | — |
| 3 | **Compatibility** — coexists and exchanges information with other systems | co-existence · interoperability | — |
| 4 | **Interaction capability** — ease with which users can interact with it | appropriateness recognizability · learnability · operability · user error protection · user engagement · inclusivity · user assistance · self-descriptiveness | was *Usability*. New: user engagement, inclusivity (replaces *accessibility*), user assistance, self-descriptiveness. Dropped: *user interface aesthetics* |
| 5 | **Reliability** — performs specified functions under specified conditions for a specified period | faultlessness · availability · fault tolerance · recoverability | *maturity* → faultlessness |
| 6 | **Security** — protects information against unauthorised access or modification | confidentiality · integrity · non-repudiation · accountability · authenticity · resistance | New: resistance — sustains operation under attack |
| 7 | **Maintainability** — ease with which it can be modified | modularity · reusability · analysability · modifiability · testability | — |
| 8 | **Flexibility** — adapts to changes in requirements, contexts or environments | adaptability · scalability · installability · replaceability | was *Portability*. New: scalability |
| 9 | **Safety** — avoids states that endanger life, health, property or environment | operational constraint · risk identification · fail safe · hazard warning · safe integration | Entirely new |

## Quality in use — five characteristics

How the product performs for a user in a real context. Some sources place this
in ISO/IEC 25019:2023 rather than 25010; the concepts are the same either way.

effectiveness · efficiency · satisfaction (usefulness, trust, pleasure,
comfort) · freedom from risk · context coverage

## The rest of the SQuaRE family, for when a second pass wants them

25000 guide to the series · 25012 data quality · 25019 quality in use ·
25020/22/23/24 measurement · **25040/41 evaluation process** (surfaced by the
spike as the closer fit for what `tools/design/` does) · 25030 quality
requirements.

## How Kerd uses it — the adaptation, not the adoption

The spike's finding (`docs/design/standards-grounding-findings.md`): the
evaluation matrix had already split "quality" into four or five of these
characteristics under its own names. So the column is **defined** by this
list, never **replaced** by it — an evaluation declares which characteristics
are relevant, consults the list before writing the mark, and writes one mark.
`R-0012` and `R-0033` bind a cell to a few words; nine columns would fail them.
