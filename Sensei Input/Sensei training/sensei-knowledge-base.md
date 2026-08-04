# TPS Knowledge Base

Curated synthesis for the TPS coaching skills. Organized by concept, drawing from three canonical sources:

- **Handbook**: 1973 TPS Handbook, Toyota OMCD internal training manual
- **Ohno**: "Toyota Production System: Beyond Large-Scale Production" by Taiichi Ohno (1978)
- **Liker**: "The Toyota Way" by Jeffrey Liker (2nd ed., 2021)
- **Platt**: TMMNA Pocketmod by Tim Platt (1998-2001), Toyota internal training material
- **Japanese**: Original Japanese source texts and nuance analysis (docs/sources/japanese-analysis/)

Citations appear as [Source] when the origin matters for coaching context.

---

## 1. What TPS Is

The Toyota Production System is a way of thinking about production that Toyota built over 30 years, starting in the late 1940s. It was not designed in a conference room. It emerged from necessity: Japan after the war had low volume and high variety. The American approach of mass production didn't apply.

Ohno framed the founding question: "How to cut costs while producing small numbers of many types of cars." He refused to believe the productivity gap between Japanese and American workers was physical: "Could an American really exert ten times more physical effort? Surely, Japanese people were wasting something." [Ohno]

That observation became the seed. The gap was waste, not effort.

### The Two Pillars

TPS rests on two pillars [all three sources agree]:

1. **Just-in-Time (JIT)**: The right parts reach the assembly line at the time they are needed and only in the amount needed. Attributed to Toyoda Kiichiro.

2. **Autonomation (Jidoka)**: Automation with a human touch. Machines detect abnormalities and stop themselves. Originated from Toyoda Sakichi's auto-activated loom. The kanji 自働化 includes the human radical, while plain automation 自動化 does not. [Handbook]

Ohno used a baseball analogy: autonomation is the individual skill of each player; JIT is the teamwork that coordinates the whole team. [Ohno]

### The TPS House

The canonical visual representation [Liker]:

```
┌─────────────────────────────────────────────────────┐
│  ROOF: Highest Quality, Lowest Cost, Shortest       │
│        Lead Time, Best Safety, High Morale          │
├──────────────────────┬──────────────────────────────┤
│   LEFT PILLAR        │   RIGHT PILLAR               │
│   Just-in-Time       │   Jidoka                     │
│   (Kiichiro Toyoda)  │   (Sakichi Toyoda)           │
│  - One-piece flow    │  - Stop and fix              │
│  - Takt time         │  - Andon                     │
│  - Pull/kanban       │  - Poka-yoke                 │
│                      │  - In-station quality        │
├──────────────────────┴──────────────────────────────┤
│  CENTER: Flexible, Capable, Motivated People        │
│          Continuously Improving                     │
├─────────────────────────────────────────────────────┤
│  FOUNDATION: Operational Stability                  │
│  Heijunka, Standardized Work, Visual Management     │
└─────────────────────────────────────────────────────┘
```

The roof goals are achievable only when both pillars stand and the foundation is solid. "Implementing lean tools" without the foundation fails because you install parts of a pillar without anything holding it up.

### Long-Term Philosophy

The organization exists for a purpose beyond profit. Long-term survival and value creation are the mission; profit is a byproduct and an input, not the goal. [Liker]

Long-term thinking does not mean slow thinking. It means not sacrificing the future for the quarter. [Liker]

**Concrete evidence — Great Recession 2008–2009**: Toyota lost $4B in FY2009, its first loss since 1950. Two plants (Indiana and Texas) saw sales drop more than 40%. Response: zero regular employee layoffs. Plants shut for three months of intensive kaizen training. Team members alternated between production and improvement work each half-shift. Managers took voluntary pay cuts. Workers took every other Friday unpaid. The shutdown was used to relocate lines and reprogram robots. [Liker]

A team leader's assessment: "The difference between Toyota and the other companies is that instead of forcing us to go on unemployment, they are investing in us, allowing us to sharpen our minds." [Liker]

**Ohno's patience with kanban**: The supermarket concept took shape in 1953. Kanban was not established company-wide until 1962 — nine years. Ohno's explanation: "Although it sounds like a long time, I think it was natural because we were breaking in totally new concepts." Cooperating firms learned by visiting Toyota and watching directly; the system could not be understood without seeing it in action. [Ohno]

The pattern — develop people, accept slow rollout of fundamentally new concepts, absorb short-term costs to protect long-term capability — is not incidental to TPS. It is the operating system underneath every tool.

### The Mission: 徹底的なムダの排除

Ohno's signature phrase for the purpose of TPS: 「徹底的なムダの排除」(tettei-teki na muda no haijo). Typically rendered as "thorough elimination of waste." More faithful: "elimination of waste, penetrated to the very bottom." The word 徹底的 contains 徹 (penetrate) + 底 (bottom). English "thorough" is a mild intensifier. Japanese 徹底的 is almost religious: no half-measures, no exceptions, no tolerance. Every kaizen activity, every 5 Whys session, every standardized-work revision serves this one objective. [Ohno, Japanese]

### Cost Reduction Is the Goal

Efficiency is not pursued for its own sake. The conventional formula, "selling price = profit + actual cost," is backwards. The market sets the price. Profit comes only from reducing cost. [Ohno]

The handbook is blunt: "We do not do just anything because it is profitable. Instead we must go for the plan that we believed to be the most profitable among all the other profitable options." [Handbook]

### Toyota's Priority Hierarchy

1. Safety
2. Quality
3. Volume
4. Profit-making

[Liker, attributed to Akio Toyoda during Covid-19]

---

## 2. Scientific Thinking and Observation

### The Epistemological Commitment

TPS demands a specific way of knowing things. Three characteristics of practical scientific thinking [Liker, via Mike Rother]:

1. Acknowledging our comprehension is always incomplete and possibly wrong.
2. Assuming answers will be found by test rather than just deliberation.
3. Appreciating that differences between prediction and actuality are a useful source of learning.

The contrast is how most people respond to problems: assume they already understand reality, neglect to test assumptions, and view failed predictions as personal failures.

The biological reality: our brains evolved for fast, pattern-matching thinking. TPS is a system of practices that forces slow, deliberate thinking to become habitual through practice. [Liker, citing Kahneman]

### Genchi Genbutsu (Go and See)

"The actual place and actual thing." Go directly to the source to find facts. Make decisions based on observed reality, not reports or theory. [All three sources]

The handbook: "The actual situation is the starting point. Investigate root cause. Develop countermeasure. Facts at the workplace are more accurate than data or reports." [Handbook]

Ohno: "The production plant is manufacturing's major source of information. Stand on the production floor all day and watch — you will eventually discover what has to be done. I cannot emphasize this too much." [Ohno]

John Shook clarified for the digital age: "Genchi genbutsu means grasping the real situation. How you get facts and grasp the situation is actually secondary. It doesn't mean you must always literally go and see. It means confirm what's really happening." [Liker]

**TPS relevance**: Step 1 (What Is Happening) and Step 4 (Point of Cause) both depend on direct observation. A description built from secondhand reports will point the 5 Whys at the wrong target.

### The Ohno Circle

Ohno's training device: he drew a circle on the shop floor and had students stand in it for hours, sometimes all day, observing. No explanation given. The teaching: develop the discipline of sustained observation without preconceptions. The gemba contains more information than any report. The student must figure out what to look for. [Liker, Ohno]

### Observation Discipline

The handbook warns about three problems with observation [Handbook]:

1. Bias from experience
2. Superficial observation
3. Insufficient time observing

"Stay there and keep observing for about half a day." And: "Observe without any bias, as if you were a blank piece of paper." [Handbook]

---

## 3. Standards

### What Standards Are

Standard work is the current best-known way of performing work at the rate of customer demand. It forms the baseline for kaizen. [All three sources]

The handbook: "Standard work is alive, it is always incomplete and always has tasks that can be improved." [Handbook]

Ohno: "Standards are something to set up yourself." Not developed by IE technicians, but by the leader on the floor. [Ohno]

Ford, quoted by both Ohno and Liker: "If you think of standardization as the best you know today, but which is to be improved tomorrow — you get somewhere. But if you think of standards as confining, then progress stops."

The handbook is sharp about accountability: "A supervisor at a workplace where the standard work has not been revised regularly, has proved themselves to be an incapable leader." [Handbook]

### Three Elements of Standard Work

All three sources agree on these [Handbook, Ohno, Liker]:

1. **Cycle time**: Time allowed to complete one piece or unit, derived from customer demand.
2. **Work sequence**: The order of operations a worker performs.
3. **Standard inventory (WIP)**: The minimum in-process inventory needed to keep the process running.

If any one is missing, standard work is not complete.

### The Standard Diagnosis

When any defect or deviation is found, the first question is always: "Was standardized work followed?" [Liker, Handbook]

- If no: correct behavior. This is a training or compliance problem.
- If yes and defects still occur: modify standardized work. The standard is wrong.

This question determines whether you have a people problem or a system problem. Most organizations default to "people problem." Toyota defaults to "system problem." [Liker]

**TPS relevance**: Step 2 (What Should Happen) surfaces the standard. The diagnosis determines how the problem flows through Steps 4 and 5. Three outcomes matter:
1. No standard exists. (This is a finding, not a failure.)
2. Standard exists but is not followed.
3. Standard followed but still failed.

### Workers Own Their Standards

Toyota turned classical industrial engineering on its head. Work groups design and continuously improve their own work. "We gave the stopwatch to the work groups." [Liker]

This is the distinction between coercive bureaucracy (Taylorist) and enabling bureaucracy (Toyota). Standards developed by workers in a continuous effort to improve are empowering. Standards imposed by experts are alienating. [Liker, citing Paul Adler's NUMMI study]

### Standard Work Tools

The handbook details specific artifacts [Handbook]:

- **Part-specific capacity chart**: Records process order, machine number, basic time, tools, processing capacity.
- **Standard work combination chart**: Visual showing work sequence and time relationships between manual work (solid line), automatic feed (dotted line), and walking (wavy line).
- **Standard work chart**: A3-size paper showing machine placement, work sequence, standard WIP, cycle time, safety and quality check points. Displayed visually so the supervisor's guidance becomes visible.
- **Job breakdown sheet**: Important steps, key points (success/failure, safety, making work easier), and reasons why.

---

## 4. Waste

### The Capacity Equation

All three sources share the same foundational equation:

```
Current Capacity = Useful Work + Waste
```

True efficiency means minimizing waste, not maximizing output. [Handbook, Ohno]

### The Original Four Types (1973)

The handbook lists four categories of unnecessary activity, predating the commonly cited seven [Handbook]:

1. Overproduction
2. Waiting time
3. Transport
4. Processing itself

"These four categories were further expanded and subdivided into what is commonly referred to today as '7 Wastes'. The objective of defining them was to make it easier for people to see where improvements needed to be made." [Handbook]

### The Seven Wastes (Ohno)

Ohno's list, in his ordering (which encodes priority) [Ohno, Japanese]:

1. **つくりすぎのムダ** (overproduction): the parent of all other wastes. It hides the other six.
2. **手待ちのムダ** (waiting)
3. **運搬のムダ** (transport/conveyance)
4. **加工そのもののムダ** (the waste of processing itself): not "are we doing too much of it" but "is this step necessary at all?" A challenge to the step's existence, not its dosage. [Japanese]
5. **在庫のムダ** (inventory)
6. **動作のムダ** (wasted motion): specifically the bodily motions of the worker. Distinct from 運搬 (transport of materials). [Japanese]
7. **不良をつくるムダ** (making defectives): the Japanese points at the act of producing them, placing responsibility on the process. "Defects" sounds like an outcome; 不良をつくる sounds like something the process is doing. [Japanese]

Overproduction is first and is the worst. It generates all the others. [Ohno, Handbook, Liker]

Liker adds an eighth: unused employee creativity.

### The Three Ms

Toyota's internal ordering is Muri, Mura, Muda because that is the causal chain. Most English lean literature reverses this to Muda first because waste grabs Western management attention. [Handbook, Liker, Japanese]

- **Muri (ムリ)** (overburden): Pushing people, equipment, or processes beyond their capacity. Also means "unreasonable" or "impossible." Applies to everything, not just operator fatigue. This is the cause.
- **Mura (ムラ)** (unevenness): Variance in quality, volume, work content, or time intervals. 標準 (hyōjun, standard) is the opposite of mura. This is why standardized work is TPS's answer to mura.
- **Muda (ムダ)** (waste): Non-value-added activity. The 7 wastes. This is the symptom.

The causal chain: "If you impose overburden (muri), unevenness (mura) arises, and in turn that becomes the origin of waste (muda)." Waste is where you notice the disease, but you treat it at the source. [Japanese]

On the shop floor, the three are sometimes collapsed into the portmanteau ダラリ (da-ra-ri), a slouching, unproductive sound. Being ダラリ is bad. [Japanese]

"Muda is viewed as something that can be worked on by the frontline work group, but overburden and unevenness are the responsibility of management." [Liker]

### Making Waste Visible

The handbook's key method: all four types of waste should be converted into visible waiting time, the easiest form to spot and countermeasure. Methods [Handbook]:

- Make operators follow standard work thoroughly.
- Restrict overproduction using kanban.
- Specify workspace on conveyor.

### The Overstock Cascade

The handbook traces a vicious cycle that starts with excess inventory [Handbook]: Excess inventory leads to needing a warehouse, which needs people, which needs forklifts, which needs management, which leads to rust and damage, which needs repair, which needs computers, which creates a perceived capacity shortage, which triggers capital investment, which creates even more inventory. This is why overproduction is the worst waste.

### Work Classification

Three categories [Handbook, Ohno]:

- **(A) Waste**: Eliminate immediately.
- **(B) Non-value-added work**: Must be done under current conditions but is waste. Change conditions to eliminate.
- **(C) Value-added work**: Processing that changes shape or character of the product.

The proportion of value-adding work is "surprisingly low." [Handbook]

The critical distinction from Ohno: "Moving is not necessarily working. Working means actually advancing the process." [Ohno]

### Work Redistribution

Do NOT spread surplus time evenly across workers. [Handbook]

Bad example: 4 workers each at 0.85 capacity. Waste is invisible.

Correct approach: Fill 3 workers to 1.0 and leave person 4 at 0.4 (visible surplus), then eliminate the 0.4 through improvement.

Equal redistribution hides the waste and creates psychological resistance to future improvement.

### True Efficiency vs. Apparent Efficiency

10 people making 100 items, improved to make 120. If demand is still 100, making 120 is "apparent increase." Costs go up. True efficiency: 8 people making 100 items. [Handbook, Ohno]

Two ways to increase efficiency: increase output or reduce workers. Most supervisors choose increasing output (easier). Toyota chooses reducing workers (harder, but the only method that reduces cost when demand is flat or falling). [Handbook]

Ohno: "Few people in the world can raise productivity when production quantities decrease." [Ohno]

**TPS relevance**: Steps 3 (AS IS) and 4 (Point of Cause) depend on understanding what waste looks like in the specific process. The work classification helps identify which category the waste falls into, which determines the countermeasure approach at Step 6.

---

## 5. Problem Solving

### 5 Whys

Toyota's root-cause analysis method. Ask "Why?" iteratively, moving from symptom to root cause. [All three sources]

Ohno's canonical example [Ohno]:

1. Why did the machine stop? A fuse blew from an overload.
2. Why was there an overload? The bearing was not sufficiently lubricated.
3. Why was it not lubricated sufficiently? The lubrication pump was not pumping sufficiently.
4. Why was it not pumping sufficiently? The shaft was worn and rattling.
5. Why was the shaft worn out? There was no strainer attached and metal scrap got in.

The handbook offers a parallel example [Handbook]:

1. Machine stops. Why? Switch broken.
2. Switch broken. Why? Oil in switch case.
3. Oil in switch case. Why? Leaking lubricant pipe joint.
4. Leaking pipe joint. Why? Pipe runs through switch case.
5. Pipe runs through switch case. Why?

"5W = 1H" (Five Whys equal One How). The answer to the fifth why becomes the countermeasure. [Handbook]

Critical nuances:

- **"Five" is not literal.** The number is an anchor to push past the premature answer, not a target. Ohno's point: one or two whys rarely reach the real cause. "Ask until you stop hitting symptoms." [Liker, Japanese]
- **なぜ (naze, why) is a soft, curious word.** The practice is taught as 自問自答 (jimon-jitō, "asking yourself and answering yourself"), an introspective discipline, not an interrogation of a subordinate. Many English implementations turn 5 Whys into a blame cascade because they miss this framing. [Japanese]
- **真因 (shin'in, true cause) vs 原因 (gen'in, cause).** Japanese distinguishes between any cause and the true cause. The kanji 真 means "truth." The 5 Whys output is not just "a cause" but the true one. Lesser causes are falsehoods masquerading as explanations. English "root cause" is close but 真因 is morally stronger. [Japanese]
- **5 Whys degenerates into 5 Whos when people are defensive.** Creating a psychologically safe environment is a prerequisite. The investigation focuses on system failure, never individual failure. [Liker]
- **5 Whys without genchi genbutsu produces false root causes.** Asking "Why?" in a conference room, without observing the actual phenomenon, consistently produces plausible but wrong answers. [Liker]

**TPS relevance**: Step 5 (Root Cause Analysis) applies 5 Whys to the Point of Cause identified in Step 4. The precision of Step 4 determines whether the 5 Whys hit a real root cause or wander into speculation.

### PDCA (Plan-Do-Check-Act)

The cornerstone of scientific thinking at Toyota, derived from Deming. [Liker]

Two versions exist. The false version is project management in disguise [Liker]:

| Aspect | False PDCA | True PDCA |
|--------|-----------|-----------|
| Plan | Commit to a known solution | Set direction and form hypotheses |
| Do | Implement the solution | Run experiments |
| Check | Confirm the solution worked | Compare prediction to actual: what did we learn? |
| Act | Broadly deploy | Refine and set next target condition |

The tell: when "Check" is used only to confirm success (not to learn from failed predictions), the organization is using PDCA as theater.

Ohno: "Things do not go as planned. It is not being obsessed with just moving anything as planned, it is better to take advantage of the effect of natural adjustment." [Ohno via Handbook]

**TPS relevance**: The entire 9-step framework is a PDCA cycle. Steps 0-4 are Plan (understand the problem). Steps 5-6 are Do (develop and test countermeasure). Step 7 is Check (monitor results). Steps 8-9 are Act (standardize and spread).

### A3 Thinking

An 11x17-inch single-page document that tells a complete story. But the document is not the point. The A3 is an artifact for making thinking visible so a coach can teach. [Liker]

John Shook: "We would rewrite A3s 10 times or more. We would write and revise them, tear them up and start over, discuss them and curse them, all as ways of clarifying our own thinking, learning from others, informing and teaching others." [Liker]

All good A3s have PDCA built in: current condition, gap, target, hypotheses, experiments, and learning.

Why paper matters: "If plans are hidden in a password-protected database, genchi genbutsu of planning cannot happen." The physical visibility of information at the gemba triggers questions. [Liker]

### Countermeasures, Not Solutions

"There are no solutions, only countermeasures." A countermeasure is a hypothesis that might reduce the gap. Proven countermeasures become standards, "the best we know today until we find a better one." [Liker]

The word choice is deliberate. "Solution" implies finality and certainty. "Countermeasure" preserves the scientific stance: we are testing, not declaring.

### The Problem-Solving Stack

How problems are actually handled at Toyota, from seconds to years [Liker]:

**Level 1 (seconds to minutes)**: Team member sees deviation, pulls andon cord. Team leader responds within 10-20 seconds. Contain or stop line segment.

**Level 2 (same shift)**: Team leader examines andon pulls, selects most frequent. First question: was standardized work followed? Countermeasure applied by tomorrow morning. (Ohno's rule: no problem should wait longer than tomorrow morning.)

**Level 3 (days to weeks)**: Systematic root cause analysis. 5 Whys, Pareto charts, cause-and-effect diagrams, genchi genbutsu, A3 report.

**Level 4 (weeks to months)**: PDCA/kaizen cycles. Plan, experiment, check, standardize and spread via yokoten.

**Level 5 (months to years)**: Strategic problem solving through hoshin kanri. Goals cascaded through catchball.

### TBP: Toyota Business Practices (8-Step)

Introduced by Fujio Cho to give people a framework for developing scientific thinking through practice on real problems. [Liker]

1. **問題の明確化 (Clarify the Problem)**: Grasp current condition. Define ideal condition. No root cause analysis yet.
2. **問題の層別と問題点の特定 (Break Down and Pinpoint)**: Go to the gemba. Move from the broad problem (問題, mondai) to the specific problem-point (問題点, mondaiten). Japanese has two words where English has one. Step 2's whole purpose is this move from broad to narrow. [Japanese]
3. **目標の設定 (Set the Target)**: Specific value and deadline for the prioritized sub-problem.
4. **真因の追究 (Pursue the True Cause)**: Go to the gemba. 真因 (shin'in) means the true cause, not just any cause. Investigate based on actual facts through 5 Whys.
5. **対策立案 (Formulate Countermeasures)**: Consider all stakeholders and risks. Multiple countermeasures possible.
6. **対策の実行 (Execute Countermeasures)**: Implementation is an experiment. Watch for unintended consequences.
7. **効果の確認 (Verify the Effect)**: Did the countermeasure achieve the target? Was the process sound?
8. **標準化と横展開 (Standardize and Deploy Horizontally)**: New processes become the standard. 横展開 (yokotenkai) is active deployment, not passive sharing. 横 (horizontal) + 展開 (deploy/unfold): take the solution and lay it out across the organization. Missing either half (standardize OR deploy) means the gain decays. [Japanese]

TBP is iterative, not linear. After addressing sub-problem 1, revisit the current condition, select the next sub-problem, continue. The steps are not a checklist but a discipline for not fooling yourself. [Japanese]

**TPS relevance**: The 9-step TPS framework maps closely to TBP. Steps 0-3 correspond to TBP Steps 1-3. Step 4 (Point of Cause) adds precision that TBP Step 4 assumes. Steps 5-9 correspond to TBP Steps 4-8.

---

## 6. Flow, Pull, and Leveling

### One-Piece Flow

Flow value to each customer, ideally one by one, without stagnation. One-piece flow is a vision to struggle toward, not a tool to implement once. [Liker]

The primary benefit is not efficiency. It forces problems to the surface so people must solve them and grow. It is deliberately "a bad system that will break." [Liker]

The math that explains why: Batch and queue with 4 processes at 90% uptime = 90% output (buffers hide inefficiency). One-piece flow: 90% x 90% x 90% x 90% = 65.6% output unless every problem is solved. Toyota's 97% operational ratio is achieved not by preventing problems but by solving them continuously. [Liker]

### Establishing Flow

At the Koromo plant in 1947, Ohno rearranged machines in processing sequence. Workers resisted the shift to "one operator, many machines." Ohno was patient and did not press for drastic changes. [Ohno]

The handbook traces the evolution of machine placement [Handbook]:

1. Single placement: 1 person per machine, lots of waiting.
2. Type-specific placement: 2 machines per person, L-shape. Creates "birdcage" isolated islands and overproduction.
3. Process-order placement: machines in production sequence, minimal walking, one-piece flow.
4. Flow production system: straight line, walking is part of the job, fractional workers combined across lines.

### Kanban

A scheduling signal for JIT production. The later process goes to the earlier process to pick up what is needed. [All three sources]

The supermarket idea (1953): Ohno got the idea from American supermarkets. The customer gets what is needed, at the time needed, in the amount needed. The store restocks only what has been taken. [Ohno]

Six rules of kanban [Handbook, Ohno]:

1. Don't send defective products to the next process.
2. The following process comes to pick up.
3. Only produce the amount picked up.
4. Do production leveling.
5. Kanban is a means of fine tuning.
6. Stabilize and rationalize the production process.

"Introducing kanban without actually practicing these rules will bring neither the control expected of kanban nor the cost reduction. A half-hearted introduction of kanban brings a hundred harms and not a single gain." [Handbook]

**Critical context**: It took from 1953 to 1962 for Toyota to establish kanban company-wide. "Although it sounds like a long time, I think it was natural because we were breaking in totally new concepts." [Ohno]

Flow must be established before kanban. Kanban cannot be bolted onto a broken process. [Ohno]

The kanban paradox [Liker]: TPS experts get irritated when people rave about kanban. Kanban is organized waste. The real purpose is to eliminate the kanban: reduce inventory to expose and solve problems, approaching one-piece flow. "Flow where you can, pull where you must." (Rother)

### Takt Time

```
Takt Time = Operating time available per day / Required number of products per day
```

Common error: calculating from equipment capacity or available labor instead of from customer demand. [Handbook]

Everything should produce at takt rate. Going faster = overproduction. Going slower = bottleneck. [Liker]

### Heijunka (Production Leveling)

Leveling production by both volume and product mix over a fixed period. Never assemble the same model in a batch at final assembly. Mix models in sequence. [Liker, Ohno]

Ohno's concrete example: Corona and Carina models flowed alternately on the same line. For 10,000 Coronas per month: 250 sedans + 125 hardtops + 125 wagons daily, sequenced as sedan, hardtop, sedan, wagon. Never in batches. [Ohno]

Without leveling, the whole system destabilizes. Heijunka is the foundation that enables everything above it in the TPS house. [Liker]

### Setup Time Reduction

What made small lot sizes economically viable [Ohno]:

- 1940s: 2-3 hours
- 1950s: under 1 hour, then 15 minutes
- Late 1960s: 3 minutes

---

## 7. People and Respect

### Respect for People as Foundation

The handbook: "Labor reduction aims mainly the elimination of unnecessary activity, and it does not mean labor intensification or speeding up." [Handbook]

"There is nothing more demoralizing for people who are offering their precious energy and time to the company and are forced to waste it. Concentrating their efforts into work that is useful is the beginning of respect for people." [Handbook]

### The 1946 Assembly Line Case Study

September to December 1946 [Handbook]:

- Takt increased from 16.6 to 18.2 vehicles/hour.
- 120-150 minutes of line stops per shift.
- Team went to production floor, applied roughly 100 improvements centered on worker difficulties.
- Line stops dropped to 20-30 minutes.
- Complaints about "labor intensification" completely disappeared.
- 80% of improvements came from the people themselves.

This is the clearest proof that TPS is respect for people in practice, not just in principle. Mutual trust starts with participation in improvement activities.

### Labor Saving vs. People Saving

The handbook makes a critical distinction [Handbook]:

- **Labor saving**: Reducing effort (may save 0.1 or 0.5 of a worker).
- **People saving**: Reorganizing so one fewer worker is needed.
- **Reducing the number of workers**: Actually removing the person from the line.

0.9 person saving doesn't reduce a person. Only the last two produce real cost reduction. [Handbook, Ohno]

### When Reducing People

"Reduce the best personnel first." Removing poor performers leads to morale decline. Removing best performers gets active cooperation from others because they get reassigned to improvement work. [Handbook]

### Job Security as Business Strategy

Without job security, team members will not surface problems (fear of looking incompetent), will not participate in kaizen (fear of working themselves out of a job), and will not trust leadership's stated intentions. [Liker]

Toyota's job security is not charity. The knowledge, skills, and problem-solving capability of long-tenured, secure team members cannot be purchased in the market. It can only be grown. [Liker]

### Employee Empowerment

**Team structure**: Four team members per Team Leader (TL). Four TLs per Group Leader (GL). The GL is the first management level; they run their area like a small business — responsible for HR, training, performance review, safety, kaizen, and hoshin kanri inputs. The GL can perform any job on the line. [Liker]

**Authority to stop the line**: Any team member can pull the andon cord when they see a deviation from standard. This is not just permission — it is an expectation. A team member who never pulls the cord is not seen as efficient; they are seen as not paying attention. (See Section 9 for the full andon sequence.)

**The suggestion system**: Georgetown Toyota generated approximately 80,000 suggestions per year, with 99% implemented. The volume is not the result of financial incentives. It is the result of intrinsic motivation — meaningful work, recognition by peers and leaders, and the small-group structure that makes each idea visible and actionable. Research on creative performance (Duncker candle experiment) shows that pay-per-idea programs undermine the intrinsic motivation that drives genuine kaizen. Toyota relies on recognition, not cash bonuses. [Liker]

**Quality circles**: Offline team activities — often after hours — where intact work groups solve quality, productivity, or safety problems using a simplified 6-step process: (1) theme selection, (2) current condition analysis, (3) target setting, (4) root cause analysis, (5) countermeasure implementation, (6) standardize and evaluate. Projects run six months. Led by the team leader; coached by the group leader. Best projects are presented regionally and globally. The result is that every Toyota team member has direct experience with structured problem solving, not just the engineers. [Liker]

**Workers design their own standards**: The enabling bureaucracy principle (Section 3, Standards) applies directly here. Standards that workers develop through their own continuous improvement efforts are empowering. Standards that are designed by industrial engineers and imposed on workers are alienating. Toyota's kaizen structure ensures team members are the authors of their own standard work, not recipients of it. [Liker, Adler NUMMI study]

This connects directly to the 1946 case study earlier in this section: 80% of improvements came from the people themselves. Empowerment is not a program. It is the structural outcome of job security, team-level authority, and a suggestion system that responds to every idea.

### The Toyota Way 2001 (Five Values)

Toyota's internal philosophy document (the "Green Book"), two pillars with five values. The English rendering of the pillar names loses meaning. [Liker, Japanese]

**Pillar 1: 知恵と改善 (Chie to Kaizen)** is rendered in English as "Continuous Improvement." The Japanese says "Wisdom and Kaizen." 知恵 (chie, wisdom) is the faculty that powers improvement. You can have improvement without wisdom (brute optimization); the Japanese insists the two are joined. The English pillar name conflates the pillar with one of its sub-values (改善), erasing wisdom entirely. [Japanese]

**Pillar 2: 人間性尊重 (Ningen-sei Sonchō)** is rendered as "Respect for People." 人間性 means "humanity / human-ness / human nature," not just "people." The object of respect is what makes people human: their capacity to think, grow, take responsibility. [Japanese]

The five values under these pillars [Liker, Japanese]:

1. **チャレンジ (Challenge)**: "Standing on a long-term perspective, we take on the challenge of realizing our dreams with courage and creative force." The Japanese uses active verbs (挑戦する, to challenge) and 力 (force/power). English flattens this into a static quality. [Japanese]
2. **改善 (Kaizen)**: "Forever pursuing evolution and innovation, we work on improvement without pause." The kanji is 改 (alter) + 善 (good/virtue), literally "changing toward the good." It carries moral weight. English "improvement" is neutral optimization. The Japanese also pairs 進化 (evolution, gradual) with 革新 (innovation, radical) as a productive paradox. [Japanese]
3. **現地現物 (Genchi Genbutsu)**: "Through genchi genbutsu we discern the essence, swiftly agree and decide, and execute with full force." English renders this as "go and see," which captures only the first half. The Japanese insists on observation in service of fast, decisive, hard-executed action. 見極める means "see through to the very end," a penetrating observation, not a leisurely walkabout. [Japanese]
4. **チームワーク (Teamwork)**: "We develop people and concentrate the strength of individuals." 育成 (ikusei) is the verb used for raising children or growing plants. People are grown, not "developed" in the HR sense. 結集 (kesshū) means to concentrate forces into a single point. Teamwork in Japanese-Toyota is 育成 + 結集: grow each person, then focus their forces. [Japanese]
5. **尊重 (Respect)**: "Respecting others, making the effort to understand each other, fulfilling our responsibilities, and building mutual trust." The verb 果たす (hatasu) means to carry through to completion. Responsibility is not something you accept; it is something you complete. [Japanese]

### The Coaching Relationship

A Toyota sensei is not a consultant, lecturer, or expert who provides answers. The sensei [Liker]:

- Goes to the gemba and observes without speaking, then asks challenging questions.
- Does NOT give the answer. Creates conditions for the student to discover it.
- Pushes back on A3s. Marks them up, sends them back.
- Sets impossible-seeming challenges that force creative experimentation.
- Creates discomfort deliberately. "Try something and do it now." (Ohno)
- Explains the criticism after the fact, not during it.

### The Coaching Kata (5 Questions)

Five questions a coach asks at every coaching cycle [Liker, via Rother]:

1. What is the target condition?
2. What is the actual condition now?
3. What obstacles are preventing you from reaching the target condition? Which one are you addressing now?
4. What is your next step (experiment)? What do you expect?
5. How quickly can we go and see what we have learned from taking that step?

These are not just coaching questions. They are the architecture of a scientific-thinking conversation.

**TPS relevance**: The /sensei:coach skill models this dynamic. The sensei draws out the human's thinking at each step rather than providing it.

### The Supervisor's Circle

From the handbook, the supervisor's improvement cycle [Handbook]:

Standardization -> finding abnormality -> investigation of the cause -> improvement -> standardization

"If they cannot recognize what is abnormal, they are not suitable to be a supervisor." [Handbook]

"A supervisor who cannot say 'stop the line,' as well as a supervisor whose line has stopped 2 or 3 times for the same reason both get an 'F.'" [Handbook]

"The best supervisor is one who can do the standardization and promote improvement so that the line can work at its best performance even without them." [Handbook]

---

## 8. Partners and Suppliers

Suppliers are extensions of the production system, not external vendors. Toyota challenges them with high standards, invests in their capability, and expects mutual improvement — but never extraction.

**The governing principle**: "Achievement of business performance by the parent company through bullying suppliers is totally alien to the spirit of the Toyota Production System." — Taiichi Ohno [Ohno]

**Value chain hierarchy** [Liker]: Fair commercial relations form the foundation. Above that: stable processes, enabling systems, mutual learning. Skipping lower levels makes upper levels impossible. This sequence determines whether the partnership produces results.

**Target cost system** [Liker]: Toyota provides first-tier suppliers a maximum allowed cost. Supplier designs to hit that target. Post-launch, Toyota requests annual price reductions — assuming kaizen will continually reduce cost. This structure assumes a partnership, not adversarial negotiation.

**The Aisin Fire (1997)** [Liker]: A sole-source p-valve factory burned. Two hundred suppliers self-organized within two days and restarted production without a central coordinator. This was possible only because Toyota had spent decades building deep mutual trust and shared TPS knowledge across the supply base. Toyota's internal conclusion: not to abandon JIT, but to avoid concentrating critical sole-source parts in a single location.

**Jishuken (voluntary study groups)** [Liker]: Started 1977 by Toyota's OMCD. Groups of 4–7 suppliers organized by geography or part type. TPS trainers rotate across member companies on 3–4 month radical transformation projects — not incremental improvement. Representatives visit each other's plants and make recommendations. Called "voluntary"; Toyota expects participation from core suppliers.

**How cooperating firms originally learned kanban** [Ohno]: Kanban was adopted company-wide at Toyota in 1962 after nine years of internal development. Suppliers learned by visiting Toyota and watching the system operate directly. "They would have had difficulty understanding the system without seeing it in action."

**TSSC** [Liker]: Toyota Production System Support Center (originally Toyota Supplier Support Center, founded 1992). Teaches TPS using model-line transformation. In 25 years served 320+ organizations, including non-Toyota manufacturers. Average outcomes: 75% inventory reduction, 124% productivity improvement.

---

## 9. Visual Management and Quality

### Andon

Line-stop indicator using lights: green (normal), yellow (attention needed), red (stopped). Makes the status of the production line visible at a glance. [All three sources]

The system works like this at Toyota [Liker]:

1. Team member sees deviation from standard, pulls andon cord. Yellow light.
2. Line continues moving (allows finish of current unit).
3. Team leader has 10-20 seconds to respond.
4. Team leader can fix it, cancel the stop, or allow line to stop.
5. If line stops, workstation turns red. Only the line segment stops, not the entire plant.

The Cho Paradox: "If you are not shutting down the assembly plant, it means that you have no problems. All manufacturing plants have problems. So you must be hiding your problems." [Liker]

"A line which does not stop is either perfectly good or extremely bad." [Handbook]

### Poka-Yoke (Error-Proofing)

Creative devices making errors nearly impossible. The handbook lists six categories (A-F) covering operational errors, product problems, incomplete work, and preceding process defects. [Handbook]

Additional error-proofing methods: signs (visual), jigs (won't accept wrong products), autonomation (stop on problem). [Handbook]

Each poka-yoke device has its own standard maintenance form: what problem it addresses, what alarm sounds, what action to take, how to confirm the device is working, and how to quality-check if it breaks down. [Liker]

Without confirming the device works, you have false confidence.

### Technology Serves People (Principle 8)

Technology serves people and processes, not the reverse. Automate only what is already a well-understood, stable manual process. Never automate a process you don't deeply understand manually first. [Liker]

Mitsuru Kawai's four skills required before automating [Liker]:

1. Develop manual skills — workers must be able to perform the work by hand
2. Apply kaizen to the manual process — improve it before encoding it in machine
3. Automate the improved manual process — not the original, waste-laden version
4. Apply kaizen to the automated process — automation does not end improvement

"I believe that the more automation advances, the more the ability of the people using it will be put to the test. Machines cannot improve unless people do, too." — Akio Toyoda [Liker]

The principle, not the technology, is what matters. When a manager spec'd an expensive electronic andon system, a Toyota mentor drove him to a hardware store and bought red, yellow, and green flags. Said: "Andon." The system only works when people understand the importance of surfacing problems and have a problem-solving process to follow. [Liker]

The TPS Basic Learning Line illustrates this concretely: Kawai used a manual transmission assembly line with no electricity as the training environment for deep TPS development. Students improve the manual line through kaizen, then carry those insights to automated processes. Learning must be earned through the manual work first. [Liker]

### 4-S / 5S

The original system was 4-S [Handbook]:

1. Seiri (Sort)
2. Seiton (Organize)
3. Seisou (Clean)
4. Seiketsu (Standardize)

Later consultants added Shitsuke (Sustain), "complicating the original program until the tool becomes an independent program, without understanding why it was useful in the first place." [Handbook]

Toyota actually uses 4S. They drop Sustain: "assumed; without sustaining, why bother?" [Liker]

"5S is lipstick on a pig" if applied to a mass production system without stable processes. 5S should support smooth flow to takt, not organize waste neatly. [Liker]

### Quality Built into the Process

"Every single person is responsible. The following process is the customer. 100% inspection is built into the process, not performed by separate inspectors." [Handbook]

If a defect is found in the following process [Handbook]:

1. Immediately contact preceding process.
2. Stop production.
3. Investigate root cause.
4. Implement countermeasures.

"The goal of the inspector: not just pass/fail, but responsible for workplace analysis of why failure occurred, determine cause, stop reoccurrence. The inspector must be a teacher." [Handbook]

### The Conveyor Safety Example

A sign says "Turn off switch before climbing onto conveyor." But when the conveyor runs at 80%, maintenance says it can wait, and production pressure exists. Will the worker really follow the rule? The blame goes to the person, but the real reason is incomplete automation. This is a system failure, not a behavior failure. [Handbook]

**TPS relevance**: This example illustrates why Step 5 (Root Cause) must pursue systemic causes, not blame individuals. If the 5 Whys stop at "the worker didn't follow the rule," you have a symptom dressed up as a root cause.

---

## 10. Leadership

### Developing People Is the Primary Job

Toyota leaders measure their success by the scientific thinking capability of their direct reports, not by the problems they personally solve. [Liker]

"Before we build cars, we build people." [Liker]

The most important and most difficult behavior: resisting the impulse to give the answer. [Liker]

### Leaders Forgive Sound Process, Reprimand Lucky Shortcuts

"Management will forgive a decision that does not work out as expected if the process used was a good one. A decision that by chance works out well, but was based on a shortcut process, is more likely to lead to a reprimand." [Liker]

This single behavioral norm creates the conditions for genuine scientific thinking. If people are rewarded for quick results regardless of method, they will always shortcut.

### The Ford Connection

Ohno spent significant time analyzing Henry Ford's original work. He believed Ford was a natural rationalist and that Ford's successors misinterpreted his true intention. [Ohno]

Ford's successors kept large lot sizes in upstream processes: "They ended up with the concept 'the larger the lot size, the better.' This builds a dam, so to speak, and stops the flow." [Ohno]

Ohno believed: "If the American king of cars were still alive, he would be headed in the same direction as Toyota." [Ohno]

Ford on standards (quoted by Ohno): "One has to go rather slowly on fixing standards... There is the standardizing which marks inertia, and the standardizing which marks progress." [Ohno]

Ford on the purpose of industry: "The true end of industry is to liberate mind and body from the drudgery of existence by filling the world with well-made, low-priced products." [Ohno]

### Management by Ninjutsu

"Management should be done not by arithmetic but by ninjutsu." [Ohno]

The Corolla story: 80 workers were making 5,000 engines. The boss said 10,000 units would need 160 workers. Ohno's response: "In grade school I was taught that two times eight equals sixteen. After all these years, do you think I should learn that from you?" 100 workers ended up making over 10,000 units. Linear scaling is lazy thinking. [Ohno]

### Hoshin Kanri

Management system keeping the entire organization aligned and focused. Both a planning tool and a process for developing people through coaching. [Liker]

Not target cascading. The critical thinking discipline is: "What do I need to work on to help my boss achieve their targets?" This is causal decomposition, not proportional target splitting. [Liker]

Catchball: the give-and-take exchange of targets and ideas between organizational levels. An ongoing coaching process, not just a planning meeting. [Liker]

### The Genealogy

Toyoda Sakichi spent an entire day watching his grandmother's loom. From this came the philosophy: "Find a subject to think about, stare at an object until a hole is almost bored through it, and find out its essential nature." His auto-activated loom took 25 years from conception to completion. [Ohno]

Toyoda Kiichiro articulated the founding principle in 1933: "We shall learn production techniques from the American method of mass production. But we will not copy it as is. We shall use our own research and creativity to develop a production method that suits our own country's situation." [Ohno]

The search for Japanese originality, for adapting rather than copying, flows directly into TPS.

---

## 11. Common Pitfalls

What non-Toyota organizations get wrong, drawn primarily from Liker with supporting context from the handbook and Ohno.

### Treating TPS as a Toolkit

Organizations implement 5S, kanban, and kaizen events as discrete projects. Each tool produces some local improvement. No learning occurs. Tools wither after the project team leaves.

Ohno: "If we write it down, we kill it." TPS is a living system of thinking. Tools are expressions of that thinking. Separating the tool from the thinking produces an empty form. [Liker]

### 5 Whys Without Genchi Genbutsu

Asking "Why?" in a conference room, without going to observe the actual phenomenon, consistently produces plausible but false root causes. The countermeasure doesn't work, and people become cynical about root cause analysis. [Liker]

The blue baby hospital case: an intelligent team "knew" the cause before going to look and was wrong on every count. Going to gemba with blank minds revealed: wrong sensors (adult sensors on babies), an administrator turning off all alarms, and no follow-up protocol. Inexpensive process changes fixed the problem. No new computer system needed. [Liker]

### Implementing Standards Without Engaging Workers

Experts design the one best way, supervisors enforce, workers comply. This is Taylorism, not Toyota. It produces resistance, workarounds, and static procedures. [Liker]

### Kaizen Events as a Substitute for Daily Kaizen

Three-day or five-day kaizen workshops produce burst improvement followed by gradual regression. The daily discipline of standardized work, visual management, PDCA, and team leader involvement doesn't exist to sustain the gains. Toyota's kaizen is not an event. It is the daily scientific way people work. [Liker]

### Technology Before Process Understanding

"Americans tend to think that buying expensive new technology is a good way to solve problems. Toyota prefers to first use people and processes to solve problems, then supplement its people with technology later." [Liker]

The handbook frames the sequence of improvement: (1) People improvement, (2) Process improvement, (3) Equipment improvement, (4) Design improvement. Work improvement before equipment improvement, always. Three reasons: equipment costs money and might not be needed, equipment improvement is irreversible, and equipment in a workplace without good work improvement will likely fail. [Handbook]

### Stopping When Tools Are in Place

Many organizations declare "we've implemented lean" when kanban is running and 5S is visible. This is the beginning, not the end.

The retired lean sensei's answer when asked "are we world class?": "I do not know. I was not here yesterday." [Liker]

---

## 12. Key Vocabulary

Essential terms for TPS coaching. Not an exhaustive glossary but the concepts that matter at each step.

**Andon**: Signal device for problems. Green = normal, yellow = attention, red = stopped. The Check mechanism of TPS-wide PDCA. [All sources]

**Autonomation (自働化, Jidoka)**: Machine intelligence to detect abnormalities and stop. Second pillar of TPS. Ohno deliberately wrote the compound as 自働化 (with 働, containing the person radical 亻) to distinguish it from plain automation 自動化 (with 動, no person radical). The character itself carries the thesis: a machine that truly works contains a trace of human intelligence, specifically the intelligence to stop itself when something is wrong. The kanji is a mnemonic that no English word can replicate. Many lean adopters implement "automation" without the halt-on-abnormality principle and then wonder why they do not get Toyota's quality. [All sources, Japanese]

**Catchball**: Give-and-take exchange of targets between organizational levels in hoshin planning. [Liker]

**Countermeasure**: A hypothesis that might reduce the gap. Not a "solution." Proven countermeasures become standards. [Liker]

**Gemba/Genba**: "The real place." Where value-added work happens. Go there. [All sources]

**Genchi Genbutsu (現地現物)**: "The actual place and actual thing." The English "go and see" captures only the first half. The full Japanese value statement: "Through genchi genbutsu we discern the essence (本質を見極める, to see through to the very end), swiftly agree and decide, and execute with full force." Observation in service of fast, decisive action, not a leisurely walkabout. [All sources, Japanese]

**Hansei**: "Being honest about your own weaknesses." Reflection with emotional acknowledgment, a future plan, and sincere commitment. Not just a meeting format. [Liker]

**Heijunka**: Production leveling by volume and mix. Foundation of the TPS house. [All sources]

**Hoshin Kanri**: Policy deployment. Organizational alignment through cascaded goals and coaching, not just target-setting. [Liker]

**JIT (ジャスト・イン・タイム)**: 「必要なものを、必要なときに、必要なだけ」. "What is needed, when it is needed, only as much as is needed." The Japanese repeats 必要 (hitsuyō, necessary) three times as a drumbeat. The particle だけ (dake, only/just) means nothing beyond that. Any more than necessary is, definitionally, waste. First pillar of TPS. [All sources, Japanese]

**Kaizen (改善)**: The kanji is 改 (alter/revise) + 善 (good/virtue), literally "changing toward the good." It carries moral weight: you are not optimizing a number, you are reforming toward virtue. The daily scientific way people work toward goals, not an event. [All sources, Japanese]

**Kanban**: Scheduling signal for JIT production. Authorizes replenishment of what was consumed. [All sources]

**Kata**: Practice pattern to develop skill. Improvement Kata (4-step) and Coaching Kata (5-question). [Liker]

**Muri/Mura/Muda (ムリ・ムラ・ムダ)**: Toyota's internal order is Muri first because it encodes causation: overburden causes unevenness, unevenness causes waste. English reverses this to Muda first. See Section 4 for full treatment. [Handbook, Liker, Japanese]

**Nemawashi**: "Going around the roots." Building consensus through cross-organizational communication before formal decisions. Toyota's operational method has 8 components organized in two phases — Relationships (Be Personable, Build Partnerships, Be Proactive, Build Pyramid) then Communication (Be Provider, Begin with Peers, Break for Preview, Bare Prospects). The key principle: start with peers, spiral up through layers, return to lower levels if needed. Benefits: no surprises, collective knowledge, give and take. A decision reached through nemawashi takes longer to plan but executes at the speed of full commitment. [Liker, Platt]

**PDCA**: Plan-Do-Check-Act. Scientific thinking cycle. The compass, not the GPS. [All sources]

**Poka-Yoke**: Error-proofing devices making mistakes nearly impossible. [Handbook, Liker]

**Standard Work**: Current best-known way to perform work at customer demand rate. The baseline for kaizen. Three elements: cycle time, work sequence, standard inventory. [All sources]

**Takt Time**: Rate of customer demand. Available work time divided by units required. The pacing mechanism of JIT. [All sources]

**TBP (Toyota Business Practices)**: Cho's 8-step problem-solving developmental framework. [Liker]

**Yokoten (横展開)**: 横 (horizontal) + 展開 (deploy/unfold). Active deployment, not passive sharing. "Share best practices" is the weak English version. 横展開 is an imperative: take the solution and lay it out across the organization. Not "copy exactly" but go see, learn, and adapt to local problems. [Liker, Japanese]

---

## 13. Key Quotes for Coaching

Organized by the moments they matter most in TPS coaching.

### On Going to See (Steps 1, 3, 4)

"The actual situation is the starting point. Facts at the workplace are more accurate than data or reports." [Handbook]

"Stand on the production floor all day and watch — you will eventually discover what has to be done." [Ohno]

"If the problem is known, it is relatively easy to implement countermeasures. The hard part is finding out what the real problem is." [Handbook]

### On Standards (Step 2)

"If there is no standard, there can be no improvement." [Ohno]

"Standard work is alive, it is always incomplete and always has tasks that can be improved." [Handbook]

"If you think of standardization as the best you know today, but which is to be improved tomorrow — you get somewhere." [Ford, via Ohno and Liker]

### On Root Cause (Step 5)

"By asking why five times and answering it each time, we can get to the real cause of the problem." [Ohno]

"Observe without any bias, as if you were a blank piece of paper." [Handbook]

"Underneath the 'cause' of a problem, the real cause is hidden. We must dig up the real cause by asking why, why, why, why, why." [Ohno]

### On Countermeasures (Step 6)

"There are no solutions, only countermeasures." [Liker]

"For every problem, we must have a specific countermeasure. A vague statement that waste should be eliminated will not convince anybody." [Ohno]

"Take countermeasures for every single failure — even if a failure occurs only once in 1,000." [Handbook]

### On Checking and Prevention (Steps 7, 8)

"Improvement is finished only when intended results are obtained." [Handbook]

"A supervisor whose line has stopped 2 or 3 times for the same reason gets an 'F.'" [Handbook]

"If defects persist, either standard work is not being followed, or there is a defect in machinery, equipment, or tools." [Handbook]

### On Sharing (Step 9)

Yokoten: "Horizontal and peer-to-peer, with the expectation that people go see for themselves and learn how another area did kaizen and then improve on those kaizen ideas. It is not 'copy exactly.'" [Liker, via Norval]

### On the Mindset

"Necessity is the mother of invention." [Ohno]

"Do not be afraid of stopping the line. Instead of fearing line stops, you should consider them as the springboard for further improvement." [Handbook]

"The slower but consistent tortoise causes less waste and is much more desirable than the speedy hare." [Ohno]

"The most important thing we have learned is the importance of implementation — actually getting out there and doing it." [Liker, via Fujio Cho]

"TPS is built on the scientific way of thinking... How do I respond to this problem? Not a toolbox." [Liker, via Ohba]

## 14. A3 as Communication Tool

The A3 is not only a problem-solving format. At Toyota, the A3 is used for any communication that needs to be clear, compressed, and reviewable. The discipline of one page forces the author to understand their own thinking well enough to compress it. [Platt]

### The 7 Story Types

Toyota uses 7 story types for A3 communication, organized into two categories:

**Information Stories** (telling a story to inform):
1. **Educate to the Details** — Simple overview → Medium detail → Full detail. Start with the big picture, drill into specifics.
2. **Illumination of the Unknown** — Known → Unknown. Anchor new information to what the audience already understands.
3. **Compare & Contrast** — Current Situation → New Situation. Show what changed or will change.
7. **Education / Satisfaction** — Introduction → Topics → Conclusion. Educate on a series of related topics.

**Recommendation Stories** (telling a story to get agreement):
4. **Standard Toyota Proposal** — Situation → Problems & Cause → Proposal & Benefits. Show the problem before proposing the solution.
5. **Correcting Discrepancy from Standard** — Current Situation → Standard & Gap → Countermeasures. A known standard is not being followed.
6. **Develop the Roadmap** — Trends & Analysis → Strategic Direction. Propose direction based on identified trends.

These are separate from problem-solving (the 9-step framework). Problem-solving is investigation — you don't know the answer when you start. Story types are communication — you know what you want to say and the A3 structures how you say it. [Platt]

### The 5-Step Story Creation Process

1. **Select the outline** — pick the story type that fits what you're communicating
2. **Fill each box** — 3-7 key bullet points per section, developed at the level of your intended audience
3. **Test against the Rock Solid principles** — if it fails any test, compress further
4. **Illustrate** — add charts or pictures where they help, keep them simple
5. **Nemawashi and refine** — review with others, adjust, repeat

### Rock Solid Principles

Four tests for whether a story is ready. If it fails any one, it needs more work:
- If it's too much to handwrite, you have too much
- The audience should know why they're reading this
- Someone with no context (a grandparent) should be able to follow it
- You should be able to tell the story in a 3-minute elevator ride

These tests enforce the A3 constraint: one page is not a limitation, it is the discipline that produces clarity. [Platt]

### Nemawashi as Method

The 8 components of operational nemawashi:

**Relationships (1-4):**
1. **Be Personable** — be part of the organization, say hello, speak to people in the halls
2. **Build Partnerships** — build personal relationships with a select few, converse regularly on work and personal topics
3. **Be Proactive** — identify the key stakeholders for specific activities before you need them
4. **Build Pyramid** — understand the formal hierarchy and the informal organization, know who has established relationships

**Communication (5-8):**
5. **Be Provider** — stay in touch with key stakeholders, keep them informed of progress, share information
6. **Begin with Peers** — when building consensus, start with peers and spiral up through the layers; return to a lower level if necessary
7. **Break for Preview** — have preliminary informal discussions, hand sketch the concept and story
8. **Bare Prospects** — outline for informal discussions: review the history, identify previous reviewers, relay current thoughts, ask questions, get feedback, adjust, repeat with others

Benefits: no surprises, collective knowledge, give and take, each person is a person not an enemy. [Platt]

---

*Synthesized from three canonical sources. See docs/sources/ for full extractions and docs/sources/sources-index.md for source details and unique contributions.*
