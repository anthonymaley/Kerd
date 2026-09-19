# Work: rehearsal, the score, the concert — Conductor's route to a performed build

## Direction
For Anthony, and any Kerd user running real projects. Conductor's turn-by-turn
work (with peer review and Switch In/Out) is the **rehearsal** and stays as it is.
Rehearsal covers, in any order: the idea and why, feasibility and whether it is
worth it, goals and constraints, the design. When the person is **ready**,
Conductor guides them to the **composer**, which writes the **score**; the
**concert** performs it (agents loop to the score, context windows roll) and
returns a **result** checked against the goals. Other agents and models help and
review throughout; the person can always see where they are; pictures throughout.
View: [rehearsal-concert.html](rehearsal-concert.html) (proposed until agreed)

## Success and proof
Proposed, not agreed: on a real project (3of3 or apple-music), one piece of work
goes rehearsal → ready → score → concert → result without falling back to turn by
turn during the concert. Anthony: "when we are ready we go to concert to execute
perfectly."

## Boundaries and decisions
- Must: the organic route is not lost. Anthony, 2026-09-18: "right now conductor is
  really working for organic peer turn by turn and agent peer review, switch in/out
  etc. so dont want to lose that."
- Must: no strict process. "we need to let the AI work and people react."
- Must: keep the protocol simple. "lets not overcomplicate the protocol to make it
  work, needs to feel like playing music not building an LLM."
- Must: agents and visuals run through the whole process. Anthony, 22:22: "agents,
  visuals all super important throughout the process no matter if its rehearsal or
  concert time."
- Open: what the launch plan's pilot becomes. The `agent-request` subject overlaps
  `/kerd:agent` and was set aside in conversation; no ruling recorded yet.
Time/resources: none stated.
Stopping point: shaping only so far. No Kerd skill change is authorized.

## Agreement
Direction agreed in conversation 2026-09-18 22:21: "yes that diagram is good but we
need to fold in some of the goals in rehearsal then (idea, feasibility, constraints,
goals, design) then when ready we are guided to composer for the score > then to
concert for execute (loop, rolling etc) subagents used throughout etc but yes this
is the simple high level process we need." Build not yet requested or approved.

## Decisions and changes
- 2026-09-18 22:25 — Anthony approved drafting, with two corrections: Ready can be
  prompted by Conductor ("i think we are ready! or we need this to be ready"), and
  "rehearsal cant be gates or ladders, it needs to be organic and free flowing, and
  conductors job is to guide and interview and prompt to get what we need to be ready
  for concert. not a strict protocol process."
- 2026-09-18 22:29 — Anthony ruled the 3of3 and apple-music counts out as evidence:
  both are long-running projects with large backlogs that predate Conductor. Analysis
  drawn from them was dropped from this record and the view. He kept the
  recommendation it led to: Switch Out keeps the rehearsal notes, Switch In shows
  where each piece of work stands, Conductor guides and prompts Ready.
- 2026-09-18 22:16 — Anthony reframed two parallel routes as one sequence: "organic
  route is dress rehearsal, and the structured route is the concert."

- 2026-09-18 22:36 — Fresh Claude review (Opus 5, high effort, observed) returned
  eight wording findings; rehearsal and Ready wording found sound.
- 2026-09-18 22:56 — Anthony's rulings on the findings: (1) the composer can be used
  at any time, to write a score in rehearsal or check a complex piece, and the score
  is written as we go; (2) "always be delivering. always. Concert is implementation
  to a spec to a goal vs incremental work"; (3) the goals and spec set in rehearsal
  and codified in the score decide whether the goal is met "before we can leave loop";
  (4) Conductor keeps and owns a notebook and refers to it; Switch Out can add to it,
  "but he owns it"; (5) do not complicate: visuals and agents work the same in
  rehearsal and concert, visuals at key points and for agreement "all the time" and
  in concert also capture what is built and progress; agents "anytime we can, and
  especially in concert, fan out as many agents as we can with their own part of the
  score"; (6–8) agreed, with plain English, product-level wording in every visual and
  exchange. The notebook is the existing work record; `docs/playbook.md` is a
  different, project-wide file and keeps its name.

- 2026-09-18 22:58 — Named the **sketchbook** (Anthony: "notebook - seems off - is there
  a musical term we can use?"; agreed "okay"). It is the existing work record under a
  musical name; nothing moves on disk.

- 2026-09-18 23:06 — Second fresh review (Opus 5, high) returned ten findings on the
  revised draft; all applied as wording. One is a product limit, not wording: the
  rolling route runs one player at a time, so a concert cannot yet fan out and roll
  at once. The draft now says so plainly. Open for a later release.

- 2026-09-18 23:15 — Anthony corrected the 23:06 "product limit": rolling happens at
  the Conductor level between batches. Fan out a batch, wait for every return,
  assess the context window, then continue or do a rolling Switch Out and In and start
  the next batch. It is not one agent over many rolls. And Conductor, though not
  independent, still checks each player's claim against the spec. The 23:06 entry's
  limit applies only to the unattended managed driver. Draft reworded to match.

## Now
Stage: Shape
Current activity: draft revised to the 22:56 rulings; uncommitted.
Pending question: see the session; not yet answered at this save.
Next action: on Anthony's go, draft the smallest Conductor change (rehearsal notes +
the Ready moment that hands to the composer). Codex `codex-tui` reviews at the
checkpoint and before push.
