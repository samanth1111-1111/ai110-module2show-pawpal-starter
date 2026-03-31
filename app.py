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
    pet_rows = [{"🐾 Name": p.name, "Breed": p.breed, "Age": p.age, "Medical Info": p.medical_info} for p in owner.pets]
    st.dataframe(pet_rows, use_container_width=True, hide_index=True)
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
        with col3:
            recurrence = st.selectbox("Recurrence", ["None", "daily", "weekly"])
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        if task_title.strip():
            new_task = Task(
                title=task_title.strip(),
                duration=int(duration),
                priority=priority,
                time=task_time.strip() or None,
                recurrence=None if recurrence == "None" else recurrence,
            )
            pet_options[selected_pet].add_task(new_task)  # Pet.add_task() appends to pet.tasks
            st.success(f"Task '{new_task.title}' added to {selected_pet}!")
        else:
            st.error("Please enter a task title.")

    # --- Filter controls using Schedule.filter_tasks() and Schedule.sort_by_time() ---
    schedule = Schedule(owner=owner)

    st.markdown("#### Filter Tasks")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_pet = st.selectbox(
            "Filter by pet", ["All"] + [p.name for p in owner.pets], key="filter_pet"
        )
    with col_f2:
        filter_status = st.selectbox(
            "Filter by status", ["All", "Pending", "Completed"], key="filter_status"
        )

    filtered_set = set(schedule.filter_tasks(
        pet_name=None if filter_pet == "All" else filter_pet,
        status=None if filter_status == "All" else filter_status,
    ))

    sorted_tasks = [t for t in schedule.sort_by_time() if t in filtered_set]

    if sorted_tasks:
        priority_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        task_rows = [{
            "Task": t.title,
            "⏰ Time": t.time or "anytime",
            "Priority": f"{priority_icon.get(t.priority, '')} {t.priority}",
            "Duration (min)": t.duration,
            "Recurrence": t.recurrence or "—",
            "Status": t.status,
            "Overdue": "⚠️ Yes" if t.is_overdue() else "✅ No",
        } for t in sorted_tasks]
        st.dataframe(task_rows, use_container_width=True, hide_index=True)

        overdue_tasks = [t for t in sorted_tasks if t.is_overdue()]
        if overdue_tasks:
            st.warning(f"⚠️ {len(overdue_tasks)} task(s) are overdue: {', '.join(t.title for t in overdue_tasks)}")
        else:
            st.success("All tasks are on schedule.")
    else:
        st.info("No tasks match the current filter.")

    # --- Mark task complete using Schedule.complete_task() ---
    all_pending = [t for t in owner.get_all_tasks() if t.status == "Pending"]
    if all_pending:
        st.markdown("#### Mark a Task Complete")
        task_labels = {f"{t.title} ({t.time or 'anytime'})": t for t in all_pending}
        chosen_label = st.selectbox("Select task to complete", list(task_labels.keys()), key="complete_select")
        if st.button("Mark Complete"):
            follow_up = schedule.complete_task(task_labels[chosen_label])
            st.success(f"'{task_labels[chosen_label].title}' marked complete.")
            if follow_up:
                st.info(f"Next recurring occurrence scheduled at: {follow_up.time}")
            st.rerun()

else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates a sorted daily plan and checks for scheduling conflicts.")

if st.button("Generate schedule"):
    schedule = Schedule(owner=owner)
    schedule.generate_daily_plan()       # Schedule.generate_daily_plan() sorts tasks by time then priority
    plan = schedule.view_plan()          # Schedule.view_plan() returns the ordered list

    if plan:
        st.markdown(f"**Today's Schedule for {owner.name}**")
        priority_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        for i, task in enumerate(plan, 1):
            time_label = task.time if task.time else "anytime"
            label = (
                f"**{i}. {task.title}** &nbsp;|&nbsp; "
                f"{priority_icon.get(task.priority, '')} {task.priority} priority &nbsp;|&nbsp; "
                f"⏰ {time_label} &nbsp;|&nbsp; {task.duration} min &nbsp;|&nbsp; `{task.status}`"
            )
            if task.is_overdue():
                st.error(f"⚠️ {label}  ← *overdue*", icon="⚠️")
            elif task.status == "Completed":
                st.success(label, icon="✅")
            else:
                st.info(label, icon="📋")
        st.caption(schedule.explain_plan())

        # --- Conflict detection using Schedule.find_conflicts() ---
        conflicts = schedule.find_conflicts()
        st.divider()
        if conflicts:
            st.warning(f"⚠️ {len(conflicts)} scheduling conflict(s) detected:")
            for a, b in conflicts:
                st.error(
                    f"**{a.title}** ({a.time}, {a.duration} min) overlaps with "
                    f"**{b.title}** ({b.time}, {b.duration} min)",
                    icon="🚫",
                )
        else:
            st.success("✅ No scheduling conflicts found.", icon="✅")
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
