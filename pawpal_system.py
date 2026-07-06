"""
pawpal_system.py
Logic layer for PawPal+.

Classes: Task, Pet, Owner, Scheduler
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""

    name: str
    category: str  # e.g. "walk", "feeding", "meds", "enrichment", "grooming"
    duration_minutes: int
    priority: str  # e.g. "high", "medium", "low"
    pet_name: Optional[str] = None  # back-reference so a task can be identified on its own
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # e.g. "daily", "weekly"
    preferred_time_window: Optional[str] = None  # e.g. "08:00" in HH:MM format
    is_complete: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.is_complete = False

    def get_next_occurrence(self) -> Optional["Task"]:
        """Return a new Task instance for the next occurrence if this task is recurring.

        Daily tasks advance by 1 day, weekly tasks by 7 days, using timedelta.
        Returns None if the task isn't recurring.
        """
        if not self.is_recurring or not self.recurrence_pattern:
            return None

        if self.recurrence_pattern == "daily":
            next_due = self.due_date + timedelta(days=1)
        elif self.recurrence_pattern == "weekly":
            next_due = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            name=self.name,
            category=self.category,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            pet_name=self.pet_name,
            is_recurring=self.is_recurring,
            recurrence_pattern=self.recurrence_pattern,
            preferred_time_window=self.preferred_time_window,
            is_complete=False,
            due_date=next_due,
        )


@dataclass
class Pet:
    """Stores a pet's profile and its list of care tasks."""

    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list, tagging it with this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's tasks."""
        return self.tasks

    def task_count(self) -> int:
        """Return how many tasks this pet currently has."""
        return len(self.tasks)

    def mark_complete_and_advance(self, task: Task) -> Optional[Task]:
        """Mark a task complete, and if it's recurring, automatically add the next occurrence.

        Returns the newly created next-occurrence Task, or None if the task doesn't recur.
        """
        task.mark_complete()
        next_task = task.get_next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    contact_info: Optional[str] = None
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return this owner's pets."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'brain' that retrieves, organizes, and manages tasks across pets."""

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, day_start: str = "07:00", day_end: str = "21:00"):
        """Set up a scheduler with a bounded daily time window."""
        self.day_start = day_start
        self.day_end = day_end

    def get_tasks_for_owner(self, owner: Owner) -> List[Task]:
        """Retrieve all tasks across every pet belonging to the given owner."""
        return owner.get_all_tasks()

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (high first), then by shorter duration as a tiebreaker."""
        return sorted(
            tasks,
            key=lambda t: (self.PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes),
        )

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Return tasks that share the same preferred_time_window (a simple overlap check)."""
        seen = {}
        conflicts = []
        for task in tasks:
            window = task.preferred_time_window
            if not window:
                continue
            if window in seen:
                conflicts.append(task)
                conflicts.append(seen[window])
            else:
                seen[window] = task
        # de-duplicate while preserving order
        unique_conflicts = []
        for t in conflicts:
            if t not in unique_conflicts:
                unique_conflicts.append(t)
        return unique_conflicts

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their preferred_time_window ('HH:MM' string), earliest first.

        Tasks with no time set are pushed to the end.
        """
        return sorted(
            tasks,
            key=lambda t: (t.preferred_time_window is None, t.preferred_time_window or ""),
        )

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        is_complete: Optional[bool] = None,
    ) -> List[Task]:
        """Filter tasks by pet name and/or completion status.

        Any filter left as None is ignored (not applied).
        """
        result = tasks
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        if is_complete is not None:
            result = [t for t in result if t.is_complete == is_complete]
        return result

    def detect_time_conflicts(self, tasks: List[Task]) -> List[str]:
        """Lightweight conflict check: return warning strings for tasks sharing an exact time slot.

        This does not crash the program — it just returns human-readable warnings for the
        caller (e.g. main.py) to print or log. Only exact HH:MM matches are flagged; true
        overlapping durations are not checked (see reflection.md for this tradeoff).
        """
        warnings: List[str] = []
        seen: dict = {}
        for task in tasks:
            slot = task.preferred_time_window
            if not slot:
                continue
            if slot in seen:
                other = seen[slot]
                warnings.append(
                    f"⚠️ Conflict at {slot}: '{task.name}' ({task.pet_name}) "
                    f"overlaps with '{other.name}' ({other.pet_name})"
                )
            else:
                seen[slot] = task
        return warnings

    def expand_recurring_tasks(self, tasks: List[Task]) -> List[Task]:
        """Return only the tasks that are marked recurring (placeholder for future date logic)."""
        return [t for t in tasks if t.is_recurring]

    def generate_plan(self, owner: Owner, available_minutes: Optional[int] = None) -> List[Task]:
        """Build a prioritized daily plan across all of an owner's pets.

        If available_minutes is given, tasks are filtered out once the time budget runs out.
        """
        tasks = self.get_tasks_for_owner(owner)
        sorted_tasks = self.sort_by_priority(tasks)

        if available_minutes is None:
            return sorted_tasks

        plan = []
        time_used = 0
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= available_minutes:
                plan.append(task)
                time_used += task.duration_minutes
        return plan
