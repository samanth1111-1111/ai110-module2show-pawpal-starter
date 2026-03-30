from pawpal_system import Owner, Pet, Task

# --- Create Owner ---
owner = Owner(name="Samantha", contact_info="samantha@email.com")

# --- Create Pets ---
buddy = Pet(name="Buddy", age=3, breed="Golden Retriever", medical_info="No known allergies")
luna  = Pet(name="Luna",  age=5, breed="Siamese Cat",      medical_info="Lactose intolerant")

# --- Create Tasks ---
morning_walk = Task(title="Morning Walk",    duration=30, priority="High",   time="07:00")
feeding      = Task(title="Feed Buddy",      duration=10, priority="High",   time="08:00")
vet_meds     = Task(title="Give Luna Meds",  duration=5,  priority="High",   time="09:00")
grooming     = Task(title="Brush Luna",      duration=15, priority="Medium", time="14:00")
evening_walk = Task(title="Evening Walk",    duration=30, priority="Medium", time="18:00")
playtime     = Task(title="Playtime",        duration=20, priority="Low",    time="19:00")

# --- Assign Tasks to Pets ---
buddy.tasks.append(morning_walk)
buddy.tasks.append(feeding)
buddy.tasks.append(evening_walk)
buddy.tasks.append(playtime)

luna.tasks.append(vet_meds)
luna.tasks.append(grooming)

# --- Register Pets with Owner ---
owner.pets.append(buddy)
owner.pets.append(luna)

# --- Build and Print Today's Schedule ---
all_tasks = [task for pet in owner.pets for task in pet.tasks]
sorted_tasks = sorted(all_tasks, key=lambda t: (t.time or "99:99", t.duration))

print("=" * 45)
print(f"  Today's Schedule for {owner.name}")
print("=" * 45)
for i, task in enumerate(sorted_tasks, 1):
    print(
        f"  {i}. [{task.time}]  {task.title:<20}"
        f"  {task.priority:<6} priority  |  {task.duration} min  |  {task.status}"
    )
print("=" * 45)
