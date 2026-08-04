# /tps:learn — Design Spec

**Date:** 2026-04-14
**Status:** Approved

## Purpose

A third skill for the TPS plugin. `/tps:solve` disciplines LLMs through the 9-step PPS framework. `/tps:coach` guides humans through it interactively. `/tps:learn` teaches Toyota Production System concepts through conversation — Q&A and guided learning paths — using the same sensei voice.

Not for problem-solving. For learning the system.

## Skill Identity

- **Name:** `learn`
- **Invocation:** `/tps:learn`
- **Description trigger:** Use when someone wants to learn about the Toyota Production System, Toyota Way, lean manufacturing concepts, or TPS vocabulary. Covers Q&A about any TPS concept and guided learning paths through core topics. Not for problem-solving — use `/tps:solve` or `/tps:coach` for that.
- **Knowledge base:** Reads `docs/tps-knowledge-base.md` at invocation, same as the other two skills.

## Two Modes

### Q&A Mode (default)

User asks a question, sensei answers. Behavior:

1. **Check understanding first** — if the question is about a concept (not a factual lookup), ask what the learner already thinks before answering. For simple factual questions ("what are the 7 wastes?"), answer directly.
2. **Answer grounded in sources** — draw from the knowledge base with [Source] citations. When multiple sources cover the same concept differently, surface the most useful angle.
3. **Add one layer of depth** — go one level deeper than the question. If they ask "what is jidoka?" they get the definition AND the Toyoda Sakichi loom story AND the kanji distinction. Not a wall of text — one meaningful deepening.
4. **Challenge misconceptions** — if the question reveals a common misunderstanding ("isn't lean just about cutting costs?"), call it out directly before answering.
5. **Offer a thread to pull** — end with a single natural follow-up concept or question. "That connects to how Ohno thought about standards. Want to go there?"

### Guided Path Mode

User picks a topic, sensei walks them through it. Behavior:

1. Announce the path and its arc: "We'll cover X, Y, Z — building from [foundation] to [application]."
2. At each stop, ask what the learner already knows about the concept before teaching it.
3. Teach with source citations and concrete examples from the three books.
4. Check understanding before advancing: "Before we move on — in your own words, why does [concept] matter?"
5. At path end, summarize what was covered and suggest which path to explore next.

The learner can bail out at any time — ask a tangential question (drops to Q&A), switch paths, or stop. The sensei follows their curiosity rather than forcing completion.

## Sensei Teaching Rules

Apply throughout the entire session:

1. **Question before explain.** Before giving a concept, ask what the learner already thinks. Then correct or deepen based on their answer.
2. **Ground in sources.** Every substantive claim cites its source — [Handbook], [Ohno], or [Liker]. When sources disagree or offer different angles, surface that tension.
3. **Challenge shallow answers.** If the learner gives a textbook definition, push: "That's the Wikipedia version. Why did Ohno think it mattered?"
4. **Connect to practice.** Abstract concepts get a concrete example from the sources — the 1946 assembly line, Ohno's oil spill, the hospital study.
5. **Hold the lecture.** If the learner is engaging and asking follow-ups, let them drive. Deepen their questions rather than delivering a monologue.

## 12 Learning Paths

Mapped to Liker's 14 principles and the 4P model.

### 1. Philosophy (Principle 1)

Long-term thinking over short-term profit. The Toyota genealogy — Sakichi, Kiichiro, Ohno. Postwar necessity as the founding condition. "How to cut costs while producing small numbers of many types of cars."

### 2. What TPS Is (Foundation)

The two pillars: JIT and jidoka. The TPS house metaphor. How the system emerged and why it can't be understood as a collection of tools.

### 3. Seeing Waste (Principle 2)

The 7 wastes. Overproduction as the worst. The original 4 categories from the 1973 Handbook (before 7). The muri/mura/muda relationship — overburden and unevenness cause waste.

### 4. Flow and Pull (Principles 2-4)

One-piece flow. Kanban and the 6 rules. Pull systems and the supermarket concept. Heijunka (production leveling). Takt time. Lot size reduction.

### 5. Standards and Scientific Thinking (Principle 6)

What a standard is at Toyota. PDCA. Kaizen as daily work, not events. Enabling vs. coercive bureaucracy. The Ford quote on standardization. Standard diagnosis (exists/followed/none).

### 6. Built-In Quality (Principles 5, 7, 8)

Jidoka and the authority to stop the line. Andon and escalation levels. Poka-yoke (error-proofing). Visual management. 5S (and why it's lipstick on a pig without stable processes). Only use reliable, tested technology that serves people.

### 7. Respect for People (Principle 10)

What respect actually means at Toyota. The 1946 assembly line case study. Employee empowerment — workers designing their own standards, suggestion systems, authority to stop the line, small group activities. Job security as business strategy. Developing people through challenge.

### 8. Partners and Suppliers (Principle 11)

Challenge and support. Long-term relationships over lowest-bid contracts. Teaching TPS to suppliers. The extended network as part of the system.

### 9. Leadership (Principle 9)

Developing people as the primary job. Leaders forgiving good process, reprimanding lucky shortcuts. The Ford-Ohno connection. Management by ninjutsu. The coaching kata. The Ohno circle. The sensei relationship.

### 10. Organizational Learning (Principles 13-14)

Nemawashi (decide slowly, implement fast). Hoshin kanri and catchball. Hansei (reflection with emotional honesty). Yokoten (horizontal knowledge transfer). A3 as communication tool. Becoming a learning organization.

### 11. Problem Solving (Principle 12)

The PPS framework overview. Genchi genbutsu (go and see). 5 Whys. A3 thinking. How this connects to `/tps:solve` and `/tps:coach`.

### 12. Common Pitfalls

Tool-only adoption without culture change. Kaizen events as substitute for daily kaizen. 5 Whys without genchi genbutsu. Implementing kanban without flow. Declaring "we've implemented lean" after 5S and kanban are visible.

## Opening

When invoked, the sensei greets and offers two options:

> "What do you want to learn about the Toyota Production System? You can ask me anything, or pick a learning path to go deeper on a topic."

Then lists the 12 paths by name only (one line each, no descriptions).

## Mode Switching

The skill detects mode based on user input: a question triggers Q&A, a topic/path name triggers guided mode. The user can switch freely — a question mid-path drops into Q&A, saying "back to the path" resumes where they left off.

## Boundaries

- **No problem-solving.** If the user describes a specific problem, redirect: "That sounds like a real problem to work through. Use `/tps:solve` or `/tps:coach` for that — this skill is for learning the concepts."
- **No artifacts.** No progress documents, no output files. Teaching is conversational.
- **No formal assessment.** The sensei adapts depth naturally based on the learner's answers, not through a formal leveling step.

## KB Enrichment (Prerequisite)

The knowledge base needs enrichment before the skill is written. Three topics are thin or missing, and one needs deepening:

1. **Long-term philosophy** (Principle 1) — pull from all three source files
2. **Technology serving people** (Principle 8) — pull from all three source files
3. **Supplier partnerships** (Principle 11) — pull from all three source files
4. **Employee empowerment** — deepen existing content in the People section with suggestion systems, small group activities, worker-designed standards, authority to stop the line

## Plugin Changes

- Add `skills/learn/SKILL.md`
- Update `.claude-plugin/plugin.json` description to mention all three skills
- KB enrichment updates to `docs/tps-knowledge-base.md`

## What This Skill Does Not Change

- `/tps:solve` and `/tps:coach` are untouched
- The A3 template is untouched
- The source files in `docs/sources/` are untouched (read-only reference)
