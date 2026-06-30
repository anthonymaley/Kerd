# Validate Methods Toolkit — 2026-06-29

The deeper design session the mode/lifecycle redesign flagged as "the hardest,
least-specified part of the dial" (`2026-06-28-mode-lifecycle-redesign.md`,
Stage 2). This specs how sherpa's **Validate** stage decides *what to validate*,
*how*, and *when it's done* — so training Validate into the sherpa skill becomes a
normal slice.

Designed in partner-mode whiteboard (one decision at a time), same as the rest of
the dial. Decisions below are co-signed with Tony (2026-06-29).

## The principle — risk-driven, not menu-driven

Validate is **not a fixed battery of analyses you run on every idea.** That's the
waterfall drift. It's the JIT logic applied to the worth-it question:

> Find the idea's **killer assumption** — the thing that, if false, kills it — and
> run the **cheapest test of that one thing**. Survive it, move to the next-riskiest.
> Stop when the fatal risks are cleared and a build pathway is clear.

The method falls *out of* the risk. You never pick a method first; you find what's
most likely to be fatal and reach for the cheapest tool that tests it.

This keeps the stage's decision-style JIT (drill the riskiest thing, decide, gate)
while the rigor rises vs. Explore (real research/evidence, not a throwaway spike).

## The risk taxonomy (five categories)

The menu you pick the killer from, and the keys in the risk→method map. Each names
a distinct **failure mode** — *how* the idea dies — which is the point of the
taxonomy.

| Risk | "The thing that kills it" | Cheapest tests |
|---|---|---|
| **Demand** | Nobody actually wants or uses it. | exists-check, talk to target users, light market test (landing page / waitlist / preorder) |
| **Feasibility** | It can't be built, or can't be made to work. | technical spike (= reuse Explore's), prototype, theory check |
| **Economics** | The numbers don't work; it's not worth it. | ROI / cost model, back-of-envelope |
| **Differentiation** | It already exists, or there's no reason it's us. | exists-check, competitor scan |
| **Access** | We can't reach the users, or we're not allowed. | channel/distribution check, legal/compliance scan |

Notes:
- **Demand and Differentiation share tooling** (exists-check, competitor scan) but
  stay separate — they kill for different reasons (nobody wants it vs. someone
  already nailed it). Naming the failure mode is the value.
- The list is a **floor, not a cage** — if an idea has a killer that doesn't fit
  these five, name it and test it. The taxonomy speeds the common cases; it doesn't
  forbid the uncommon one.

## The method map — how to run each (cheaply)

The second half of the toolkit. Each method is run JIT — smallest version that
gives signal, not an exhaustive study.

- **exists-check** — search whether it already exists (products, prior art, OSS).
  Often the *first* test because it's the cheapest and can kill Demand AND
  Differentiation at once.
- **competitor scan** — who's doing this, how well, where the gaps are.
- **talk to target users** — a handful of real conversations; the cheapest true
  demand signal.
- **market test** — a lightweight demand probe that costs the *user* something
  (a click, an email, a preorder): landing page, waitlist, fake-door.
- **technical spike** — build the single riskiest technical bit. This is literally
  Explore's spike, reused here to retire a Feasibility risk.
- **prototype** — a rougher functional slice when a spike isn't enough.
- **theory check** — reason/research whether the approach is sound (docs, papers,
  an expert). For when the risk is conceptual, not buildable-yet.
- **ROI / cost model** — back-of-envelope economics: what it costs to build/run vs.
  what it returns. Kills or clears Economics.
- **channel/distribution check** — is there a real path to reach the users at all.
- **legal/compliance scan** — are we allowed; what regulation/licensing applies.

## The Validate loop

1. **Surface the risks.** Read the Explore handoff (vision + how-it-works +
   requirements). Enumerate "what has to be true for this to succeed," mapping each
   to a risk category. Then **drill the user once**: "of these, which scares you
   most / is least certain?" — human judgment + the handoff together rank the list.
2. **Rank by `most likely to kill × least certain`.** The top of that list is the
   killer assumption. (High-impact-but-certain isn't where the risk is; low-impact
   doesn't gate the build.)
3. **Test the top risk, cheapest method first** (from the map). Run it JIT — enough
   signal to decide, no more.
4. **Branch on the result:**
   - **Survives** → cross it off, drop to the next-riskiest. Re-evaluate the exit
     bar.
   - **Fails** → it's a kill-or-pivot signal. **Jump back to Explore** (sherpa's
     core move) to reshape the idea, or kill it. A failed validation is the stage
     doing its job, not a setback.
5. **Graduate when the exit bar is met** (below).

## Exit bar — when Validate is done

Graduate to Plan when **all three** hold:

1. The **killer assumption(s) have been tested and survived.**
2. There's a **clear pathway to build** — you know the route, not just that it's
   wanted.
3. The **remaining risks are acceptable to carry into Build** — known, non-fatal,
   and cheaper to resolve by *building* than by more validating.

Clause 3 is the JIT release valve: you clear the *fatal* risks and a build path,
and carry the rest. You do **not** clear every risk.

**Tripwire (drift signal):** validating a risk that's cheaper to just *build past*
is over-cooking — the waterfall drift. If the next test costs more than building the
thing would teach you, stop validating and graduate.

## Produces → Plan (handoff)

Write into `kivna/sherpa.md`'s Stage log:
- the **validated pathway** (the route to build that's expected to succeed),
- the **evidence** behind it (which killer risks were tested, by which method, what
  the signal was — with the claim-discipline tags: "tested, not yet proven" vs.
  cited),
- the **carried risks** (named non-fatal risks Plan/Build should stay aware of).

## Training it into sherpa (the next slice)

Replace the Validate stub in `skills/sherpa/SKILL.md` with: the risk-driven
principle, the five-category taxonomy table, the method map (compressed), the loop,
the exit bar + tripwire, and the handoff — matching the shape of the already-trained
Explore/Plan/Build/Launch sections. Reuses Explore's spike for the technical-spike
method. Ships as a MINOR (v0.49.0), completing the lifecycle. After that: Phase 3
(rename `dian`→`conductor`, `dial`→`sherpa`; retire folded modes).
