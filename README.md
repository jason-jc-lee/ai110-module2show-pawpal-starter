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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
Today's Schedule (All Tasks, by priority)
-----------------------------------------
  [ ]        09:00 — Feeding (10 min) [priority: high] (pet: Biscuit)
  [ ]        18:00 — Evening feeding (10 min) [priority: high] (pet: Whiskers)
  [ ]        08:00 — Morning walk (30 min) [priority: high] (pet: Biscuit)
  [ ]        10:00 — Litter box cleaning (5 min) [priority: medium] (pet: Whiskers)

Today's Schedule (Limited to 40 minutes)
----------------------------------------
  [ ]        09:00 — Feeding (10 min) [priority: high] (pet: Biscuit)
  [ ]        18:00 — Evening feeding (10 min) [priority: high] (pet: Whiskers)
  [ ]        10:00 — Litter box cleaning (5 min) [priority: medium] (pet: Whiskers)

Recurring Tasks
---------------
  [ ]        18:00 — Evening feeding (10 min) [priority: high] (pet: Whiskers)

Marked 'Feeding' as complete.

Today's Schedule (after completing first task)
----------------------------------------------
  [✔]        09:00 — Feeding (10 min) [priority: high] (pet: Biscuit)
  [ ]        18:00 — Evening feeding (10 min) [priority: high] (pet: Whiskers)
  [ ]        08:00 — Morning walk (30 min) [priority: high] (pet: Biscuit)
  [ ]        10:00 — Litter box cleaning (5 min) [priority: medium] (pet: Whiskers)
  
```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
## Testing PawPal+

Run the test suite with:

```
python -m pytest
```

This test suite covers:
- Task completion status changes
- Task counts when adding tasks to a pet
- Priority and time sorting
- Recurring task advancing on completion, and that non-recurring tasks don't create follow-ups
- Conflict detection for duplicate time slots, and preventing false positives
- Pets with zero tasks producing an empty plan without errors

Sample output:

```
=================================== test session starts ====================================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0
rootdir: /Users/jason/Downloads/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 11 items

tests/test_pawpal.py ...........                                                      [100%]

==================================== 11 passed in 0.03s =====================================
```

**Confidence Level:** (4/5 stars): The logic seems to be covered by tests, but overlapping-duration conflicts and multi-week recurrence haven't been tested yet.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()`, `Scheduler.sort_by_time()` | Sorts by priority (high→low) or by HH:MM time; untimed tasks sort last |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_time_conflicts()` | Flags exact time-slot matches, returns warning strings instead of crashing |
| Recurring tasks | `Task.get_next_occurrence()`, `Pet.mark_complete_and_advance()` | Auto-creates the next occurrence (+1 day or +7 days via `timedelta`) when a recurring task is completed |
## ✨ Features

- **Owner and pet management** - track multiple pets per owner, each with their own task list
- **Task tracking** — name, category, duration, priority, optional time slot, and completion status
- **Priority-based sorting** — Scheduler.sort_by_priority() orders tasks from high to low
- **Time-based sorting** — Scheduler.sort_by_time() orders tasks chronologically
- **Filtering** — Scheduler.filter_tasks()` filters by pet name and completion status
- **Conflict warnings** — Scheduler.detect_time_conflicts() flags tasks scheduled at the same time, without crashing 
- **Daily/weekly recurrence** — Pet.mark_complete_and_advance() automatically creates the next occurrence of a recurring task 
- **Time-budgeted planning** — Scheduler.generate_plan() builds a plan that fits within a limited number of available minutes

## 📸 Demo Walkthrough

**Main UI features:**
- Enter owner and pet info (persists across the session)
- Add tasks with a title, duration, priority, optional time, and optional recurrence
- View today's schedule sorted by priority or time, with completed tasks optionally hidden
- See conflict warnings automatically if two tasks share a time slot
- Mark tasks complete so recurring tasks automatically re-occur for their next date
- Generate a plan that includes as many tasks as fit in the available minutes

**Example Process:**
1. Enter an owner name and add a pet (i.e "Mochi," a dog)
2. Add a task: "Morning walk," 20 minutes, high priority, 08:00
3. Add a second task: "Grooming," 10 minutes, medium priority, also at 08:00 (a conflict warning appears)
4. Toggle to sort by time to see the tasks in chronological order
5. Mark "Morning walk" complete, then set a task as "Recurring: daily" to see a new occurrence get auto-scheduled for tomorrow
6. Set a 30-minute time budget and click "Generate schedule" to see only the highest-priority tasks that fit

**Key Scheduler behaviors shown:** priority sorting, time sorting, filtering by completion status, conflict detection, and recurring task.

**Sample CLI output** (from running `python main.py`):

```
Today's Schedule (All Tasks, by priority)
-----------------------------------------
  [ ]        09:00 — Feeding (10 min) [priority: high] (pet: Biscuit)
  [ ]        18:00 — Evening feeding (10 min) [priority: high] (pet: Whiskers)
  [ ]        08:00 — Morning walk (30 min) [priority: high] (pet: Biscuit)
  [ ]        10:00 — Litter box cleaning (5 min) [priority: medium] (pet: Whiskers)
  [ ]        09:00 — Vet check-in call (10 min) [priority: medium] (pet: Whiskers)
  [ ]        07:30 — Playtime (15 min) [priority: low] (pet: Biscuit)

Conflict Check
--------------
  ⚠️ Conflict at 09:00: 'Vet check-in call' (Whiskers) overlaps with 'Feeding' (Biscuit)

Marked 'Evening feeding' complete (recurring: daily).
Auto-created next occurrence: due 2026-07-07 (is_complete=False)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
