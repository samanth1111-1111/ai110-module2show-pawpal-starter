# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The scheduling engine goes beyond a simple to-do list with several algorithmic features:

- **Priority-aware daily plan** — `generate_daily_plan` sorts tasks by scheduled time first, then breaks ties by priority (High → Medium → Low), so the most important tasks always surface at the right moment.
- **Conflict detection** — `find_conflicts` uses an interval-overlap algorithm to identify any two tasks whose time windows collide, across pets or within the same pet.
- **Recurring tasks** — Tasks marked `"daily"` or `"weekly"` automatically generate the next pending instance when completed via `complete_task`, keeping the schedule self-maintaining.
- **Flexible filtering** — `filter_tasks` lets you slice the task list by pet name, status, or both combined in a single call.
- **Overdue detection** — `is_overdue` compares each task's scheduled time against the current wall clock so stale pending tasks are easy to surface.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
