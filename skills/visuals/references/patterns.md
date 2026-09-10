# Pick by meaning, not by stage

Kerd adaptation of selected diagram-design patterns; not the complete upstream
catalogue. Read the section that fits the relationship. No rung mapping or type
approval is required.

## Parts and connections

Use for “what are we building?” Show distinct capabilities or actors, grouped
by ownership or meaningful boundary. Connections show what passes between them,
not decoration. A service offering can show buyer, service, delivery team and
result; it need not be forced into frontend/backend/database terminology.
Keep implementation tools out of the first view unless they affect the decision.

## Scope by containment

Use for “what belongs inside this?” Nested regions mean broader-to-narrower
scope, not process order. Siblings belong at the same level. Label boundaries
clearly and leave space between levels. An external reviewer may act on the work
without belonging inside the same trust boundary; do not conflate the two.

## Responsibility flow

Use for “who does what, and where does it pass to someone else?” Give each
person/team/role a labelled lane. Put an action in its owner's lane; arrows
crossing lanes are handoffs. Empty space is acceptable—do not invent equal
amounts of work for every actor. The selected model is not automatically a
software service, and the user is not a frontend.

## Decisions and sequence

Use a flowchart for action order with branches. Rounded ends mark start/result;
rectangles are actions; diamonds are real decisions with labelled exits. A
return arrow means an actual retry or correction, not decorative circularity.
Keep the main path obvious. Do not draw every internal check as a user approval.

For one straight sequence, omit diamonds. The worked review-flow example is
this simpler case: request → prepare → review → findings. It demonstrates a
target experience, not an implemented session transport.

## Detail without overload

Start with the smallest view that explains the decision. Add a second view for
an important branch, ownership detail or technical mechanism when requested or
needed for a sound decision. A hidden detail is not allowed to reverse the
meaning of the overview. Use a table or short paragraph when no relationship
benefits from being drawn.
