"""
tests/test_pawpal.py
Quick tests for PawPal+ core logic.
"""

import sys
import os

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
