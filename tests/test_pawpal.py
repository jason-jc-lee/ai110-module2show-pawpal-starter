"""
tests/test_pawpal.py
Quick tests for PawPal+ core logic.
"""

import sys
import os
from datetime import timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task's is_complete flag to True."""
    task = Task(name="Walk", category="walk", duration_minutes=20, priority="high")
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count by one."""
    pet = Pet(name="Biscuit", species="Dog")
    assert pet.task_count() == 0
    pet.add_task(Task(name="Feeding", category="feeding", duration_minutes=10, priority="high"))
    assert pet.task_count() == 1


def test_scheduler_sorts_by_priority():
    """The scheduler should place high priority tasks before low priority ones."""
    scheduler = Scheduler()
    low = Task(name="Grooming", category="grooming", duration_minutes=15, priority="low")
    high = Task(name="Meds", category="meds", duration_minutes=5, priority="high")
    sorted_tasks = scheduler.sort_by_priority([low, high])
    assert sorted_tasks[0] is high
    assert sorted_tasks[1] is low


def test_owner_get_all_tasks_across_pets():
    """Owner.get_all_tasks() should combine tasks from every pet it owns."""
    owner = Owner(name="Jamie")
    dog = Pet(name="Biscuit", species="Dog")
    cat = Pet(name="Whiskers", species="Cat")
    dog.add_task(Task(name="Walk", category="walk", duration_minutes=30, priority="high"))
    cat.add_task(Task(name="Litter", category="grooming", duration_minutes=5, priority="medium"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 2


# --- Phase 5: additional tests ---

def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should return tasks earliest-to-latest, regardless of input order."""
    scheduler = Scheduler()
    late = Task(name="Evening feeding", category="feeding", duration_minutes=10,
                priority="high", preferred_time_window="18:00")
    early = Task(name="Morning walk", category="walk", duration_minutes=30,
                 priority="high", preferred_time_window="08:00")
    middle = Task(name="Lunch", category="feeding", duration_minutes=10,
                  priority="medium", preferred_time_window="12:00")

    sorted_tasks = scheduler.sort_by_time([late, early, middle])

    assert [t.name for t in sorted_tasks] == ["Morning walk", "Lunch", "Evening feeding"]


def test_sort_by_time_pushes_untimed_tasks_to_end():
    """Edge case: a task with no preferred_time_window should sort after all timed tasks."""
    scheduler = Scheduler()
    timed = Task(name="Walk", category="walk", duration_minutes=20,
                 priority="high", preferred_time_window="08:00")
    untimed = Task(name="Playtime", category="enrichment", duration_minutes=15, priority="low")

    sorted_tasks = scheduler.sort_by_time([untimed, timed])

    assert sorted_tasks[0] is timed
    assert sorted_tasks[1] is untimed


def test_recurring_daily_task_creates_next_day_occurrence():
    """Marking a daily recurring task complete should auto-create a new task due 1 day later."""
    pet = Pet(name="Whiskers", species="Cat")
    task = Task(name="Evening feeding", category="feeding", duration_minutes=10,
                priority="high", is_recurring=True, recurrence_pattern="daily")
    pet.add_task(task)

    next_task = pet.mark_complete_and_advance(task)

    assert task.is_complete is True
    assert next_task is not None
    assert next_task.is_complete is False
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert pet.task_count() == 2  # original + the newly created next occurrence


def test_non_recurring_task_does_not_create_next_occurrence():
    """Edge case: completing a non-recurring task should not create a follow-up task."""
    pet = Pet(name="Biscuit", species="Dog")
    task = Task(name="Vet visit", category="meds", duration_minutes=30, priority="high")
    pet.add_task(task)

    next_task = pet.mark_complete_and_advance(task)

    assert next_task is None
    assert pet.task_count() == 1  # no new task added


def test_detect_time_conflicts_flags_duplicate_times():
    """The scheduler should flag two tasks scheduled at the exact same time."""
    scheduler = Scheduler()
    task_a = Task(name="Feeding", category="feeding", duration_minutes=10,
                  priority="high", preferred_time_window="09:00", pet_name="Biscuit")
    task_b = Task(name="Vet check-in call", category="meds", duration_minutes=10,
                  priority="medium", preferred_time_window="09:00", pet_name="Whiskers")

    warnings = scheduler.detect_time_conflicts([task_a, task_b])

    assert len(warnings) == 1
    assert "09:00" in warnings[0]


def test_detect_time_conflicts_returns_empty_for_no_overlap():
    """Edge case: tasks at different times should not be flagged as conflicts."""
    scheduler = Scheduler()
    task_a = Task(name="Feeding", category="feeding", duration_minutes=10,
                  priority="high", preferred_time_window="09:00")
    task_b = Task(name="Walk", category="walk", duration_minutes=20,
                  priority="high", preferred_time_window="10:00")

    warnings = scheduler.detect_time_conflicts([task_a, task_b])

    assert warnings == []


def test_pet_with_no_tasks_returns_empty_schedule():
    """Edge case: a pet with no tasks should produce an empty plan, not an error."""
    owner = Owner(name="Jamie")
    empty_pet = Pet(name="Ghost", species="Dog")
    owner.add_pet(empty_pet)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)

    assert plan == []
