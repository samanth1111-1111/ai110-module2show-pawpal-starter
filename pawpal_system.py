from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    duration: int                  # in minutes
    priority: str                  # "High", "Medium", "Low"
    time: Optional[str] = None     # optional scheduled time, e.g. "08:00"
    status: str = "Pending"        # "Pending" or "Completed"

    def mark_complete(self):
        """Mark this task as Completed."""
        self.status = "Completed"
        pass

    def update_task(self, title=None, duration=None, priority=None, time=None):
        """Update one or more task fields; only provided values are changed."""
        if title is not None:
            self.title = title
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if time is not None:
            self.time = time
        pass

    def is_overdue(self) -> bool:
        """Return True if the task's scheduled time has passed and it is not yet completed."""
        from datetime import datetime
        if self.time is None or self.status == "Completed":
            return False
        task_hour, task_minute = map(int, self.time.split(":"))
        now = datetime.now()
        task_time = now.replace(hour=task_hour, minute=task_minute, second=0, microsecond=0)
        return now > task_time
        pass


@dataclass
class Pet:
    name: str
    age: int
    breed: str
    medical_info: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a Task to this pet's task list."""
        self.tasks.append(task)
        pass

    def remove_task(self, task: Task):
        """Remove a Task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)
        pass

    def view_tasks(self):
        """Return the list of tasks assigned to this pet."""
        return self.tasks
        pass

    def update_info(self, new_info: str):
        """Update the pet's medical information."""
        self.medical_info = new_info
        pass


class Owner:
    def __init__(self, name: str, contact_info: str):
        self.name = name
        self.contact_info = contact_info
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a Pet to this owner's pet list if not already present."""
        if pet not in self.pets:
            self.pets.append(pet)
        pass

    def remove_pet(self, pet: Pet):
        """Remove a Pet from this owner's pet list."""
        if pet in self.pets:
            self.pets.remove(pet)
        pass

    def view_all_pets(self):
        """Return the list of all pets belonging to this owner."""
        return self.pets
        pass

    def get_all_tasks(self) -> list[Task]:
        """Collect and return all tasks across every pet owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks
        pass


class Schedule:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []
        self.daily_plan: list[Task] = []

    def generate_daily_plan(self):
        """Sort all owner tasks by priority and store them in daily_plan."""
        tasks = self.owner.get_all_tasks()
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        self.daily_plan = sorted(tasks, key = lambda t: priority_order.get(t.priority, 4))
        pass

    def view_plan(self):
        """Return the ordered daily plan."""
        return self.daily_plan
        pass

    def explain_plan(self):
        """Return a string explaining the ordering logic used for the daily plan."""
        return "Tasks are order by priority (High -> Medium -> Low)."
        pass
