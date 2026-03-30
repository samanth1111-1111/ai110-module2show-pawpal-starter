from pawpal_system import Owner, Pet, Task, Schedule

# --- Create Owner ---
owner = Owner(name="Samantha", contact_info="samantha@email.com")

# --- Create Pets ---
buddy = Pet(name="Buddy", age=3, breed="Golden Retriever", medical_info="No known allergies")
luna  = Pet(name="Luna",  age=5, breed="Siamese Cat",      medical_info="Lactose intolerant")

# --- Create Tasks added OUT OF ORDER intentionally ---
playtime     = Task(title="Playtime",       duration=20, priority="Low",    time="19:00")
evening_walk = Task(title="Evening Walk",   duration=30, priority="Medium", time="18:00", recurrence="daily")
grooming     = Task(title="Brush Luna",     duration=15, priority="Medium", time="14:00")
vet_meds     = Task(title="Give Luna Meds", duration=5,  priority="High",   time="09:00", recurrence="daily")
luna_walk    = Task(title="Luna's Walk",    duration=20, priority="Low",    time="18:10")  # cross-pet conflict: overlaps evening_walk (Buddy)
vet_checkup  = Task(title="Vet Checkup",    duration=30, priority="High",   time="09:00")  # exact same time as vet_meds (Luna) — same-pet conflict
feeding      = Task(title="Feed Buddy",     duration=10, priority="High",   time="07:20", recurrence="daily")  # same-pet conflict: overlaps morning_walk (Buddy)
morning_walk = Task(title="Morning Walk",   duration=30, priority="High",   time="07:00", recurrence="daily")

# --- Assign Tasks to Pets (also out of order) ---
buddy.add_task(playtime)
buddy.add_task(evening_walk)
buddy.add_task(feeding)
buddy.add_task(morning_walk)

luna.add_task(grooming)
luna.add_task(vet_meds)
luna.add_task(luna_walk)
luna.add_task(vet_checkup)

# Mark one task complete to demonstrate status filtering
grooming.mark_complete()

# --- Register Pets with Owner ---
owner.add_pet(buddy)
owner.add_pet(luna)

# --- Build Schedule ---
schedule = Schedule(owner)
schedule.generate_daily_plan()

W = 57

# --- 1. Raw insertion order (unsorted) ---
print("=" * W)
print("  UNSORTED (insertion order)")
print("=" * W)
all_tasks = owner.get_all_tasks()
for i, t in enumerate(all_tasks, 1):
    print(f"  {i}. [{t.time}]  {t.title:<20}  {t.priority:<6} | {t.status}")
print("=" * W)

# --- 2. sort_by_time() ---
print("\n" + "=" * W)
print("  SORTED BY TIME  (sort_by_time)")
print("=" * W)
for i, t in enumerate(schedule.sort_by_time(), 1):
    recur = f"[{t.recurrence}]" if t.recurrence else ""
    print(f"  {i}. [{t.time}]  {t.title:<20}  {t.priority:<6} | {t.status} {recur}")
print("=" * W)

# --- 3. filter_by_pet ---
print("\n" + "=" * W)
print("  FILTER: Buddy's tasks only  (filter_by_pet)")
print("=" * W)
for t in schedule.filter_by_pet("Buddy"):
    print(f"    [{t.time}]  {t.title:<20}  {t.status}")
print("=" * W)

# --- 4. filter_by_status ---
print("\n" + "=" * W)
print("  FILTER: Pending tasks only  (filter_by_status)")
print("=" * W)
for t in schedule.filter_by_status("Pending"):
    print(f"    [{t.time}]  {t.title:<20}  {t.status}")
print("=" * W)

print("\n" + "=" * W)
print("  FILTER: Completed tasks only  (filter_by_status)")
print("=" * W)
for t in schedule.filter_by_status("Completed"):
    print(f"    [{t.time}]  {t.title:<20}  {t.status}")
print("=" * W)

# --- 5. filter_tasks (combined) ---
print("\n" + "=" * W)
print("  FILTER: Luna's Pending tasks  (filter_tasks combined)")
print("=" * W)
for t in schedule.filter_tasks(pet_name="Luna", status="Pending"):
    print(f"    [{t.time}]  {t.title:<20}  {t.status}")
print("=" * W)

# --- 6. Conflict detection ---
print("\n" + "=" * W)
print("  CONFLICT CHECK  (conflict_warnings)")
print("=" * W)
warnings = schedule.conflict_warnings()
if warnings:
    for msg in warnings:
        print(f"  {msg}")
else:
    print("  No conflicts detected.")
print("=" * W)

# --- 7. complete_task: auto-schedule next occurrence for recurring tasks ---
print("\n" + "=" * W)
print("  RECURRING TASK COMPLETION  (complete_task)")
print("=" * W)

for task in [morning_walk, vet_meds]:
    next_task = schedule.complete_task(task)
    print(f"  Completed : '{task.title}'  status={task.status}")
    if next_task:
        print(f"  Scheduled : '{next_task.title}'  @ {next_task.time}"
              f"  ({next_task.recurrence})  status={next_task.status}")
    print()

# Completing a non-recurring task should NOT create a new instance
next_task = schedule.complete_task(playtime)
print(f"  Completed : '{playtime.title}'  status={playtime.status}")
print(f"  Next task created: {next_task}  (None expected — not recurring)")
print("=" * W)

# Regenerate plan to include the newly added recurring tasks
schedule.generate_daily_plan()
print("\n" + "=" * W)
print("  UPDATED PLAN after completions")
print("=" * W)
for i, t in enumerate(schedule.view_plan(), 1):
    recur = f"[{t.recurrence}]" if t.recurrence else ""
    print(f"  {i}. [{t.time}]  {t.title:<20}  {t.priority:<6} | {t.status} {recur}")
print("=" * W)
