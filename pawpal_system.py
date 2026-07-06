"""
pawpal_system.py
Logic layer for PawPal+.

Classes: Owner, Pet, Task, Scheduler
This is a skeleton generated from diagrams/uml_draft.mmd — attributes and
method stubs only, no scheduling logic implemented yet.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    name: str
    category: str  # e.g. "walk", "feeding", "meds", "enrichment", "grooming"
    duration_minutes: int
    priority: str  # e.g. "high", "medium", "low"
    pet_name: Optional[str] = None  # back-reference so a task can be identified on its own
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # e.g. "daily", "weekly"
    preferred_time_window: Optional[str] = None  # e.g. "morning", "08:00-09:00"


@dataclass
class Pet:
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        raise NotImplementedError

    def get_tasks(self) -> List[Task]:
        """Return this pet's tasks."""
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    contact_info: Optional[str] = None
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        raise NotImplementedError

    def get_pets(self) -> List[Pet]:
        """Return this owner's pets."""
        raise NotImplementedError


class Scheduler:
    def __init__(self, day_start: str = "07:00", day_end: str = "21:00"):
        self.day_start = day_start
        self.day_end = day_end

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (and likely duration as a tiebreaker)."""
        raise NotImplementedError

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Identify tasks that overlap in time or exceed the available window."""
        raise NotImplementedError

    def expand_recurring_tasks(self, tasks: List[Task]) -> List[Task]:
        """Turn recurring task definitions into concrete daily instances."""
        raise NotImplementedError

    def generate_plan(self, pet: Pet) -> List[Task]:
        """Produce an ordered daily plan for a pet's tasks given constraints."""
        raise NotImplementedError
