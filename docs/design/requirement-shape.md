# What a requirement looks like

**Status: DRAFTED BY THE MODEL — AWAITING TONY'S REVIEW AND APPROVAL.** Blocking.
Nothing may be built against this shape until he has worked through it.

**Why this exists:** Tony stopped the view spike on 2026-08-14 with *"wait have
we even agreed what a requirment looks like? how can we spike"*. A view is a
projection of a shape, and rendering one before the shape is agreed would have
made whichever shape it used the de facto answer.

**Sources — nothing here is invented from taste.** `docs/kerd-goals.md`
(approved), `docs/kerd-interview.md` (source of truth), and his interface list
of 2026-08-14 08:16. Each field below names what put it there.

---

## The fields

| # | Field | What it holds | Why it exists |
|---|---|---|---|
| 1 | **Reference** | A short human-sayable ID | *"Reference numbers"* — he asked for them, and IDs are what let a requirement be spoken about ("that fails B4") |
| 2 | **Statement** | What must be true, in one or two sentences | The requirement itself |
| 3 | **Status** | `DRAFT` · `ACCEPTED` · `FINAL v1.0` · `v1.2` … | His words, 08:23: *"status is DRAFT, ACCEPTED, FINAL V1.0, V1.2 kind of status"* |
| 4 | **Traces to** | The goal or law it serves | Law 2 as applied to requirements: one that traces to nothing does not belong |
| 5 | **Depends on** | Other requirements this one needs | *"no simple way for me to see the requirments and their dependencies"* |
| 6 | **Source words** | His verbatim quote where his words carry it | G7 — *"never sumarize memories or requirments or achievements"* |
| 7 | **Notes & comments** | His comments for the model to pick up; notes recorded around the requirement | *"to add comments perhaps for you to pick up or to record notes around the requirments"* |
| 8 | **Attachments** | Links, images | *"add links or images perhaps as input"* |
| 9 | **History** | What changed, when, and why | Law 2 — every change lands somewhere; and his change-impact want |

## Status, as he defined it

A requirement's status is about **its own maturity and version**, not about how
far the work has got. Read as a progression:

- **`DRAFT`** — being written or worked on. Not agreed. Costs nothing to change.
- **`ACCEPTED`** — he has agreed it. Changing it now is a change to an
  agreement, which is Law 2 territory.
- **`FINAL v1.0`** — locked into a version. This is the state a build is
  measured against.
- **`v1.2`** — a later version of the same requirement. The requirement did not
  die; it moved forward, and the earlier version stays in History.

**Why versions rather than a `superseded` state:** his change-of-mind
requirement — *"change requirement x and the impact can be measured and
planned"* — needs the old and new to be comparable, and needs the change to be
schedulable (*"does this go to the next release, the next version?"*). A version
number does both; a `superseded` flag does neither.

## What status is NOT

Where a requirement has got to in the work — designed, built, tested, launched —
**is not status**. That is derivable from what the requirement is linked to: if
a design cites it, it is designed; if a test cites it, it is tested. Storing it
as a field would mean maintaining by hand a fact the links already carry, and it
would be the first thing to go stale.

*This is a model inference from his answer, not something he said. Flagged.*

---

## Straw-man — Law 3 applied to this draft

**Where I am least confident: `ACCEPTED` versus `FINAL v1.0`.** I have described
them as distinct states — agreed, then locked to a version — but he listed them
in one breath and may mean one thing. If a requirement is accepted, is it not
final? The distinction I have drawn is that acceptance is his agreement and
finalisation is its assignment to a release. **That may be an invention.**

**Field 9 (History) has no shape.** I have said a requirement carries history
without saying what an entry looks like. Under Law 2, every change to an
accepted requirement lands here — so this field carries the entire anti-drift
guarantee and it is currently a word.

**Fields 7 and 8 may not belong on the requirement.** Comments, notes, links and
images are *working material around* a requirement rather than part of it. Putting
them in the record means the record grows without the requirement changing, and
that a requirement's version could churn on a comment. They may belong beside it.

**Nothing here says who may change what.** `DRAFT` is presumably the model's to
edit freely; `ACCEPTED` presumably needs him. That is unstated, and it is the
rule that makes the status field mean anything.

**Nine fields may be too many.** His standard is *"i dont mind robust, i just
mind overhead and overwork"*. Every field is grounded, but grounded is not the
same as necessary, and a nine-field record is a nine-field record to fill in.

**The omission pass** — walking his words forward rather than auditing what is
here: I find no requirement content in the interview or goals that these fields
cannot hold. **But I cannot check the one that matters** — whether this shape
survives contact with the twenty-category schema and five link roles in
`docs/requirements/catalog.md`, because that comparison has not been run.

## Not yet done, deliberately

- **Compared against `docs/requirements/catalog.md`** — the pre-reset schema
  (twenty categories, five states, five link roles, hash-approved statements).
  The agreed method is to draft fresh, then compare non-destructively and keep
  what survives on merit. This draft is the fresh half; the comparison is owed.
- **Categories or tags.** The old schema carries a twenty-category taxonomy with
  a primary-plus-tags rule. Nothing in the reset material asks for categories, so
  none are proposed here rather than inherited.
- **Link roles beyond `depends on` and `traces to`.** The old schema has five.
  Only the two he named are here.
