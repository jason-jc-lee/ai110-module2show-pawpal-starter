"""
main.py
CLI demo script to verify PawPal+ backend logic (pawpal_system.py) works correctly.
Run with: python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(title: str, tasks: list[Task]) -> None:
    """Print a list of tasks in a readable, formatted way."""
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("  (no tasks)")
        return
    for task in tasks:
        window = task.preferred_time_window or "anytime"
        status = "✔" if task.is_complete else " "
        print(
            f"  [{status}] {window:>12} — {task.name} "
            f"({task.duration_minutes} min) [priority: {task.priority}] "
            f"(pet: {task.pet_name})"
        )


def main() -> None:
    # Create an owner
    owner = Owner(name="Jamie", contact_info="jamie@example.com")

    # Create two pets
    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby", age=5)

    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    # Add tasks with different times/priorities to each pet
    biscuit.add_task(Task(
        name="Morning walk", category="walk", duration_minutes=30,
        priority="high", preferred_time_window="08:00",
    ))
    biscuit.add_task(Task(
        name="Feeding", category="feeding", duration_minutes=10,
        priority="high", preferred_time_window="09:00",
    ))
    whiskers.add_task(Task(
        name="Litter box cleaning", category="grooming", duration_minutes=5,
        priority="medium", preferred_time_window="10:00",
    ))
    whiskers.add_task(Task(
        name="Evening feeding", category="feeding", duration_minutes=10,
        priority="high", preferred_time_window="18:00", is_recurring=True,
        recurrence_pattern="daily",
    ))

    scheduler = Scheduler(day_start="07:00", day_end="21:00")

    # Full prioritized plan across all pets
    full_plan = scheduler.generate_plan(owner)
    print_schedule("Today's Schedule (All Tasks, by priority)", full_plan)

    # A plan constrained to 40 available minutes
    limited_plan = scheduler.generate_plan(owner, available_minutes=40)
    print_schedule("Today's Schedule (Limited to 40 minutes)", limited_plan)

    # Show recurring tasks
    recurring = scheduler.expand_recurring_tasks(owner.get_all_tasks())
    print_schedule("Recurring Tasks", recurring)

    # Demonstrate marking a task complete
    full_plan[0].mark_complete()
    print(f"\nMarked '{full_plan[0].name}' as complete.")
    print_schedule("Today's Schedule (after completing first task)", full_plan)


if __name__ == "__main__":
    main()
