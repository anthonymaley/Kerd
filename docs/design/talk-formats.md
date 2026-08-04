# Talk formats — the system's communication library

Living design doc (undated by the naming rule; git history is the archive).
Owner: **How we talk to each other** (function 19). Source: the nine A3
story layouts in `Sensei Input/story layout visuals/`, extracted from the
sensei skill per post-walk decision 1. The reference exemplar for any
one-page decision document is the 2013 API Gateway proposal
(`Sensei Input/example diagrams/API Gateway Proposal Paper.pdf`): current
drawn · ideal drawn · numbered pains · target · scored evaluation · costs ·
roadmap — one page.

## The tier rule

Weight decides the instrument, and the test is **who reads it, and when**:

| Tier | Instrument | Test |
|---|---|---|
| Everyday | a layout drawn on the whiteboard, in the moment | for the human in *this* conversation |
| Large story | `/sensei:story` — full A3 built progressively | an audience reads it cold, or it persists as a record |
| Problem | `/sensei:work` — point of cause, 5 whys | a problem that survived a few attempts |

## The formats

Each format keeps its own **used-when trigger** — the layouts carry these
natively, which makes format choice a route match, not a taste call.

| # | Format | Used when | Sections |
|---|---|---|---|
| 1 | **Proposal** | proposing to improve the condition — reducing problems or gaining benefits not currently available | Current Situation & Background → Problems & Cause → Proposal & Benefits |
| 2 | **Compare & Contrast** | showing a situation now versus after some change | Current Situation → New Situation |
| 3 | **Correcting Discrepancy from Standard** | the current situation differs from an established standard; countermeasure activity is in order | Current Situation → Standard & Discrepancy → Countermeasure |
| 4 | **Develop the Roadmap** | trends identified and analysed; a strategic direction decided | Trends & Analysis → Strategic Direction (Roadmap) |
| 5 | **Illumination of the Unknown** | sharing information by starting from what the reader knows | Known → Unknown |
| 6 | **Educate to the Detail** | teaching detail that needs the bigger picture first | Simplest → Medium → Detail |
| 7 | **Education / Satisfaction** | educating on a series of related topics | Intro · Purpose · Background → Points 1..N → Conclusion · Summary · Benefits |
| 8 | **Problem Solving A3** | a perceived business/engineering problem (via `/sensei:work`) | Happy path → As-is (GAP, measured) → Point of cause (TARGET) → Root cause (5 whys / fishbone) → Countermeasure & plan (results, measured) → Check / Monitor / Prevent / Share |

(A ninth file, `Proposal@2x-2`, is a variant of format 1 — one format, two
renderings.)

## System mappings — which moment uses which format

| System moment | Format |
|---|---|
| A DECISION question to the human (what · why it matters · the gap · what we win · what we lose) | **Proposal** — the five fields map onto its sections: what = current situation · why + gap = problems & cause · win/lose = proposal & benefits, **with the loss named** |
| "Say it in the user's terms" (now → the change → what it means) | **Compare & Contrast** |
| A conformance FAILURE report (a check found the built thing differing from a declaration) | **Correcting Discrepancy from Standard** — current vs the DECLARATION → discrepancy → countermeasure |
| Slicing a release, the MVP sequence, strategic direction | **Develop the Roadmap** |
| Educating the human on something new | **Illumination of the Unknown** (new territory) or **Educate to the Detail** (deep territory) |
| A multi-topic report (e.g. a gate-close summary spanning areas) | **Education / Satisfaction** |
| A problem that survived attempts | **Problem Solving A3**, via `/sensei:work` |
| An idea brief / one-page proposal artifact | **Proposal**, held to the API Gateway exemplar's bar |

## Rendering rules

- Everyday renders happen in the whiteboard grammar: containment over
  arrows (arrows only where sequence IS the point), colour marks cost
  (red), the human's input (green), deltas (blue), constant axes on any
  comparison.
- The evaluation matrix (see `docs/design/design-instrument.md`) is the
  scoring half of format 1/2 when options are compared.
- The diagram toolkit (`tools/diagram/kit.py`) grows layout helpers per
  format — a build item, not a precondition; until then formats are drawn
  by convention.

## Conformance

A communication claiming a format MUST carry that format's sections — a
machine can check section presence. The enforcement point rides the refusal
property (a talk rule that cannot bind from outside the model is advisory);
until an instance exists, this is convention.
