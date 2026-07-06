import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant that helps you build a
daily schedule of care tasks for your pet, based on priority and time constraints.
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

# --- Step 2: Manage application "memory" with st.session_state ---
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

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# --- Step 3: Wire the "Add task" button to real backend logic ---
if st.button("Add task"):
    new_task = Task(
        name=task_title,
        category="general",
        duration_minutes=int(duration),
        priority=priority,
    )
    pet.add_task(new_task)  # Pet.add_task() handles storing it and tagging pet_name

if pet.get_tasks():
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": t.name,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "pet": t.pet_name,
            }
            for t in pet.get_tasks()
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()
st.subheader("Build Schedule")
st.caption("Generates a prioritized plan using the Scheduler class from pawpal_system.py.")

available_minutes = st.number_input(
    "Time budget for today (minutes, optional)", min_value=0, max_value=1440, value=0,
    help="Leave at 0 for no time limit."
)

if st.button("Generate schedule"):
    scheduler = Scheduler()
    budget = available_minutes if available_minutes > 0 else None
    plan = scheduler.generate_plan(owner, available_minutes=budget)

    if not plan:
        st.warning("No tasks to schedule yet. Add some tasks above first.")
    else:
        st.success("Here's today's plan:")
        for task in plan:
            st.markdown(
                f"- **{task.name}** ({task.duration_minutes} min, priority: {task.priority}) "
                f"— for {task.pet_name}"
            )
