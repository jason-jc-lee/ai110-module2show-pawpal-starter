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

    # Add two tasks out of order and at a clashing time, to test sorting + conflicts
    biscuit.add_task(Task(
        name="Playtime", category="enrichment", duration_minutes=15,
        priority="low", preferred_time_window="07:30",
    ))
    whiskers.add_task(Task(
        name="Vet check-in call", category="meds", duration_minutes=10,
        priority="medium", preferred_time_window="09:00",  # same time as Feeding
    ))

    scheduler = Scheduler(day_start="07:00", day_end="21:00")

    # Full prioritized plan across all pets
    full_plan = scheduler.generate_plan(owner)
    print_schedule("Today's Schedule (All Tasks, by priority)", full_plan)

    # A plan constrained to 40 available minutes
    limited_plan = scheduler.generate_plan(owner, available_minutes=40)
    print_schedule("Today's Schedule (Limited to 40 minutes)", limited_plan)

    # --- Phase 4: sorting by time (tasks were added out of order above) ---
    all_tasks = owner.get_all_tasks()
    by_time = scheduler.sort_by_time(all_tasks)
    print_schedule("Today's Schedule (sorted by time)", by_time)

    # --- Phase 4: filtering by pet and by completion status ---
    biscuit_tasks = scheduler.filter_tasks(all_tasks, pet_name="Biscuit")
    print_schedule("Filtered: Biscuit's tasks only", biscuit_tasks)

    incomplete_tasks = scheduler.filter_tasks(all_tasks, is_complete=False)
    print_schedule("Filtered: Incomplete tasks only", incomplete_tasks)

    # --- Phase 4: conflict detection (Feeding and Vet check-in both at 09:00) ---
    warnings = scheduler.detect_time_conflicts(all_tasks)
    print("\nConflict Check")
    print("--------------")
    if warnings:
        for w in warnings:
            print(f"  {w}")
    else:
        print("  No conflicts found.")

    # Show recurring tasks
    recurring = scheduler.expand_recurring_tasks(owner.get_all_tasks())
    print_schedule("Recurring Tasks", recurring)

    # Demonstrate marking a task complete
    full_plan[0].mark_complete()
    print(f"\nMarked '{full_plan[0].name}' as complete.")
    print_schedule("Today's Schedule (after completing first task)", full_plan)

    # --- Phase 4: recurring task auto-advance on completion ---
    evening_feeding = next(t for t in whiskers.get_tasks() if t.name == "Evening feeding")
    next_occurrence = whiskers.mark_complete_and_advance(evening_feeding)
    print(f"\nMarked '{evening_feeding.name}' complete (recurring: {evening_feeding.recurrence_pattern}).")
    if next_occurrence:
        print(f"Auto-created next occurrence: due {next_occurrence.due_date} "
              f"(is_complete={next_occurrence.is_complete})")
    print_schedule("Whiskers' tasks (after recurring advance)", whiskers.get_tasks())


if __name__ == "__main__":
    main()
