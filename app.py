import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule

# Check if the owner already exists in session_state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Samantha", contact_info="samantha@email.com")

# Access the owner anywhere in the app
owner = st.session_state.owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name    = st.text_input("Pet name", placeholder="e.g. Buddy")
    pet_age     = st.number_input("Age", min_value=0, max_value=30, value=1)
    pet_breed   = st.text_input("Breed", placeholder="e.g. Golden Retriever")
    pet_medical = st.text_input("Medical info", placeholder="e.g. No known allergies")
    submitted_pet = st.form_submit_button("Add Pet")

if submitted_pet:
    if pet_name.strip():
        new_pet = Pet(name=pet_name.strip(), age=pet_age,
                      breed=pet_breed.strip(), medical_info=pet_medical.strip())
        owner.add_pet(new_pet)   # Owner.add_pet() stores the pet on the owner
        st.success(f"{new_pet.name} added!")
    else:
        st.error("Please enter a pet name.")

if owner.pets:
    st.markdown("**Your Pets:**")
    for p in owner.pets:
        st.write(f"- {p.name} ({p.breed}, age {p.age})")
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Assign tasks to a pet. Each task is stored on the pet via Pet.add_task().")

if owner.pets:
    with st.form("add_task_form"):
        pet_options   = {p.name: p for p in owner.pets}
        selected_pet  = st.selectbox("Assign to pet", list(pet_options.keys()))
        task_title    = st.text_input("Task title", placeholder="e.g. Morning walk")
        task_time     = st.text_input("Scheduled time (HH:MM)", placeholder="e.g. 08:00")
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        if task_title.strip():
            new_task = Task(title=task_title.strip(), duration=int(duration),
                            priority=priority, time=task_time.strip() or None)
            pet_options[selected_pet].add_task(new_task)  # Pet.add_task() appends to pet.tasks
            st.success(f"Task '{new_task.title}' added to {selected_pet}!")
        else:
            st.error("Please enter a task title.")

    for p in owner.pets:
        if p.tasks:
            st.markdown(f"**{p.name}'s tasks:**")
            st.table([{"title": t.title, "time": t.time or "anytime",
                       "priority": t.priority, "duration": t.duration,
                       "status": t.status} for t in p.tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    schedule = Schedule(owner=owner)
    schedule.generate_daily_plan()       # Schedule.generate_daily_plan() sorts tasks by priority
    plan = schedule.view_plan()          # Schedule.view_plan() returns the ordered list

    if plan:
        st.markdown(f"**Today's Schedule for {owner.name}**")
        for i, task in enumerate(plan, 1):
            time_label = task.time if task.time else "anytime"
            st.markdown(
                f"{i}. **{task.title}** — {task.priority} priority | "
                f"{task.duration} min | ⏰ {time_label} | `{task.status}`"
            )
        st.caption(schedule.explain_plan())
    else:
        st.warning("No tasks found. Add pets and tasks first.")
        st.markdown(
            """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
