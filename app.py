import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant that helps you build a
daily schedule of care tasks for your pet, based on priority, time, and conflicts.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()
st.subheader("Owner & Pet Setup")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# --- Manage application "memory" with st.session_state ---
# Only create the Owner/Pet objects once, the first time this info is set.
# On every later rerun, reuse what's already stored instead of recreating it.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(st.session_state.pet)

owner = st.session_state.owner
pet = st.session_state.pet

# Keep the stored owner/pet name and species in sync if the user edits the fields
owner.name = owner_name
pet.name = pet_name
pet.species = species

st.divider()
st.markdown("### Tasks")
st.caption("Add tasks for this pet. They'll feed into the scheduler below.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    time_window = st.text_input("Time (HH:MM, optional)", value="", placeholder="08:00")

recurring_col1, recurring_col2 = st.columns(2)
with recurring_col1:
    is_recurring = st.checkbox("Recurring task?")
with recurring_col2:
    recurrence_pattern = st.selectbox(
        "Repeats", ["daily", "weekly"], disabled=not is_recurring
    )

# --- Wire the "Add task" button to real backend logic ---
if st.button("Add task"):
    new_task = Task(
        name=task_title,
        category="general",
        duration_minutes=int(duration),
        priority=priority,
        preferred_time_window=time_window.strip() or None,
        is_recurring=is_recurring,
        recurrence_pattern=recurrence_pattern if is_recurring else None,
    )
    pet.add_task(new_task)  # Pet.add_task() handles storing it and tagging pet_name

st.divider()
st.subheader("Today's Schedule")
st.caption(
    "Powered by Scheduler: sorts tasks, filters by status, and flags time conflicts."
)

scheduler = Scheduler()
all_tasks = owner.get_all_tasks()

if not all_tasks:
    st.info("No tasks yet. Add one above.")
else:
    sort_choice = st.radio("Sort by", ["Priority", "Time"], horizontal=True)
    show_completed = st.checkbox("Show completed tasks", value=True)

    # --- Use Scheduler.filter_tasks() to respect the "show completed" toggle ---
    visible_tasks = (
        all_tasks if show_completed else scheduler.filter_tasks(all_tasks, is_complete=False)
    )

    # --- Use Scheduler.sort_by_priority() / sort_by_time() based on the user's choice ---
    if sort_choice == "Priority":
        ordered_tasks = scheduler.sort_by_priority(visible_tasks)
    else:
        ordered_tasks = scheduler.sort_by_time(visible_tasks)

    # --- Surface Scheduler.detect_time_conflicts() as a prominent warning ---
    conflicts = scheduler.detect_time_conflicts(all_tasks)
    if conflicts:
        st.warning(
            "⚠️ Scheduling conflicts detected:\n\n" + "\n\n".join(f"- {c}" for c in conflicts)
        )
    else:
        st.success("✅ No scheduling conflicts detected.")

    if ordered_tasks:
        st.table(
            [
                {
                    "time": t.preferred_time_window or "anytime",
                    "title": t.name,
                    "duration_minutes": t.duration_minutes,
                    "priority": t.priority,
                    "pet": t.pet_name,
                    "recurring": t.recurrence_pattern or "-",
                    "done": "✔" if t.is_complete else "",
                }
                for t in ordered_tasks
            ]
        )
    else:
        st.info("No tasks match the current filter.")

    st.markdown("#### Mark a task complete")
    task_names = [t.name for t in visible_tasks if not t.is_complete]
    if task_names:
        chosen = st.selectbox("Task to complete", task_names)
        if st.button("Mark complete"):
            task_to_complete = next(t for t in visible_tasks if t.name == chosen)
            # --- Use Pet.mark_complete_and_advance() so recurring tasks auto-renew ---
            next_task = pet.mark_complete_and_advance(task_to_complete)
            if next_task:
                st.success(
                    f"Marked '{chosen}' complete. Next occurrence auto-scheduled "
                    f"for {next_task.due_date}."
                )
            else:
                st.success(f"Marked '{chosen}' complete.")
    else:
        st.caption("All visible tasks are already complete.")

st.divider()
st.subheader("Build a Time-Budgeted Plan")
st.caption("Generates a prioritized plan that fits within a limited time budget.")

available_minutes = st.number_input(
    "Time budget for today (minutes, optional)", min_value=0, max_value=1440, value=0,
    help="Leave at 0 for no time limit."
)

if st.button("Generate schedule"):
    budget = available_minutes if available_minutes > 0 else None
    plan = scheduler.generate_plan(owner, available_minutes=budget)

    if not plan:
        st.warning("No tasks to schedule yet. Add some tasks above first.")
    else:
        st.success("Here's today's plan:")
        for task in plan:
            window = task.preferred_time_window or "anytime"
            st.markdown(
                f"- **{window}** — {task.name} ({task.duration_minutes} min, "
                f"priority: {task.priority}) — for {task.pet_name}"
            )
