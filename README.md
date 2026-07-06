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

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest


# Run with coverage:
pytest --cov
```


Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()`, `Scheduler.sort_by_time()` | Sorts by priority (high→low) or by HH:MM time; untimed tasks sort last |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_time_conflicts()` | Flags exact time-slot matches, returns warning strings instead of crashing |
| Recurring tasks | `Task.get_next_occurrence()`, `Pet.mark_complete_and_advance()` | Auto-creates the next occurrence (+1 day or +7 days via `timedelta`) when a recurring task is completed |
## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
