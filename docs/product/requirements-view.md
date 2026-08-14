---
route: spike
stage: framed
---

# Requirements view — two spikes

> ⛔ **BLOCKED BEFORE IT RAN — 2026-08-14 08:2x.** Tony: *"wait have we even
> agreed what a requirment looks like? how can we spike"*. He is right and the
> frame below was written too early. **A view is a projection of a shape, and the
> shape is not agreed.** Spike A would render the pre-reset register schema —
> the one the reset put under review. Spike B needs "a Kerd-shaped document",
> and Kerd-shaped is exactly what is undecided. Either spike would have made
> whichever shape it used the de facto answer, because the view would be built
> around it.
>
> **Prerequisite: agree what a requirement is** — its fields, its states, its
> links, what carries a comment, what carries a dependency. Much of that is
> already determined by the approved goals and by his own interface list below;
> it needs drafting and agreeing, not inventing.
>
> Nothing below is wrong, and it is kept intact. It is out of sequence.

## Value

Tony's objection, 2026-08-13 evening, and its correction the following morning.
He rejected a markdown file as the way requirements are worked on — **but not
the storage, and not the BUILD verdict**. His words, 2026-08-14 08:16:

> i objected to a simple markdown file last night because there was no simple
> way for me to see the requirments and their dependencies, i would expect a
> html view at least for me to interact with and edit the text, see its status
> (for each requirment) and to add comments perhaps for you to pick up or to
> record notes around the requirments, add links or images perhaps as input ? a
> ingle huge markdown for me to interact with is not the answer. However, im not
> going to declare how we store that data, it could be a markdown file that you
> manage and create.

**This separates the interface from the storage, and that is what dissolves the
deadlock.** The 08-08 evaluation (`docs/design/requirements-traceability.md`)
chose BUILD over StrictDoc and lost only two things doing it — a **generated
view** and **verified write-back** — recorded in that file as *"both capabilities
the producer asked for and Build does not have"*. Those two are precisely what he
is asking for now. So the open question is not which tool holds the data. It is
**whether we can supply the view without the dependency**: StrictDoc costs 87
distributions and 373 MB in *every consuming project*, which is what it lost on.

The evaluation wrote its own reversal condition to be checked rather than
re-argued — *"if a rendered view and write-back editing are wanted sooner than we
would build them… this decision should be re-opened rather than inherited."*
**That condition has fired.** These spikes check it.

**Winning:** we know, from having used both, whether the view is ours to build or
StrictDoc's to lend — and we know what a good one looks like, because we used a
working one before designing ours.

## What the view must do — his list, and the yardstick both spikes are judged by

1. See the requirements **and their dependencies** — not a single huge markdown.
2. Interact with and **edit the text**.
3. See **status per requirement**.
4. Add **comments** — either for the model to pick up, or as notes recorded
   around a requirement.
5. Add **links or images** as input.

**Write-back, staged.** Tony, 08:20: *"ideally directly to reduce overhead for
many requirments but we can start with a paste option while we build the proess
and ui out if you want as a first step"*. Direct write-back is the target because
it is what makes many requirements affordable to work on. A paste-back loop is
the accepted first step while the process and UI are built.

## The two spikes

Run in parallel — they answer different questions and neither blocks the other.
Spike B also gives Spike A a target to aim at rather than an invented one.

### Spike A — can we produce the view ourselves?

- **Question:** can a generated HTML view over markdown we own deliver all five
  capabilities above, with paste-back editing, without a third-party runtime
  dependency?
- **Method:** generate a view from the existing register; use it as he would.
- **Kill criteria — any one ends it:** dependencies cannot be shown legibly; the
  paste-back loop costs more than editing the markdown directly; or it cannot be
  built without a dependency of its own.
- **Kept if it passes:** the generator. **Kept if it fails:** the finding, and
  StrictDoc's case strengthens by exactly that much.

### Spike B — DEMOTED to conditional, 2026-08-14 08:22

Tony: *"i thought we jsut agreed to build - so no need to spike strcit dc?"* He
is right, and the model under-read the reversal condition. It says a view is
wanted *"sooner than **we would build them**"* — **conditional on our own build
speed**, not on wanting a view at all. BUILD's reasons for winning are unchanged
(373 MB per consuming project, adds a dependency without removing the work, an
unconstrained free-string status field).

**So Spike B is downstream of Spike A, not parallel to it.** It runs only if
Spike A shows the view is slow or impossible to build ourselves. Until then
StrictDoc stays where the 08-08 evaluation left it: a genuine runner-up, not
adopted.

*(Both spikes were Tony's own proposal at 08:16 — "im also open to doing two
spikes"; the sequencing error was the model's.)*

### Spike B (held) — is StrictDoc's interface worth 373 MB?

- **Question:** what does a good requirements interface actually look and feel
  like, and does StrictDoc's write-back UI deliver the five capabilities?
- **Method:** install in a throwaway venv, load a Kerd-shaped document, use the
  UI hands-on. Never installed into this repo's environment.
- **Kill criteria:** if the UI does not deliver what he wants, the dependency
  question is moot and Spike A is the only road.
- **Kept either way:** the interaction patterns worth copying. Even if StrictDoc
  is not adopted, a working reference beats designing a view from imagination.

## Kill-or-keep

Declared before either spike runs, so the answer is read off rather than argued
afterwards. A spike with no kill criterion becomes a build nobody chose.

**Spike A is KILLED if any of these hold:**

- Dependencies between requirements cannot be shown legibly in the view.
- The paste-back loop costs more effort than editing the markdown directly —
  measured against his own standard, *"i just mind overhead and overwork"*.
- It cannot be built without acquiring a runtime dependency of its own, which
  would forfeit the only margin Build holds over StrictDoc.

**Spike A is KEPT if** all five capabilities work over markdown we own, with
paste-back, and no new dependency. What is kept is the generator; it then
re-enters the ladder as normal work rather than shipping from the spike.

**Spike B is KILLED if** the StrictDoc UI does not deliver the five
capabilities — in which case the 373 MB question is moot and Spike A is the only
road.

**Spike B is KEPT — regardless of the adoption verdict — as** the interaction
patterns worth copying. A working reference beats designing a view from
imagination, and Tony has already named the value of learning from a tool
without adopting it: *"superpowers does some great things… so we can learn from
it."*

**If both are killed**, the finding is that the view is harder than either of us
thinks, and that is itself the answer the re-opened evaluation needs.

**Neither spike may ship.** Whatever survives re-enters the ladder normally; the
bypass covers the spike only.

## Deliberately not in these spikes

- **Choosing the storage format.** He explicitly declined to declare it.
- **Re-running the full 6 × 24 evaluation.** These spikes feed it; they do not
  replace it. The decision is re-opened, not yet re-taken.
- **Building the real view.** A spike that ships is not a spike. Whatever
  survives re-enters the ladder normally — the bypass covers the spike only.
- **The build-vs-adopt decision on Kerd itself** (interview Q4), which is a
  different question from this one and stays open.
