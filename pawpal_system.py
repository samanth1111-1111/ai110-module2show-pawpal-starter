from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta


@dataclass
class Task:
    title: str
    duration: int                      # in minutes
    priority: str                      # "High", "Medium", "Low"
    time: Optional[str] = None         # optional scheduled time, e.g. "08:00"
    status: str = "Pending"            # "Pending" or "Completed"
    recurrence: Optional[str] = None   # None, "daily", or "weekly"

    def mark_complete(self):
        """Mark this task as Completed."""
        self.status = "Completed"

    def next_task(self) -> Optional["Task"]:
        """If this task recurs, return a new Pending Task for the next occurrence. Otherwise None.

        Delegates date calculation to ``next_occurrence``. The returned task copies
        all fields from the current task (title, duration, priority, recurrence) but
        uses the next scheduled time and starts with status ``"Pending"``.

        Returns:
            Task: A fresh Task instance scheduled for the next occurrence, or ``None``
                if this task has no recurrence or no scheduled time.
        """
        next_dt = self.next_occurrence()
        if next_dt is None:
            return None
        return Task(
            title=self.title,
            duration=self.duration,
            priority=self.priority,
            time=next_dt.strftime("%H:%M"),
            recurrence=self.recurrence,
        )

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
        """Return True if the task's scheduled time has passed and it is not yet completed.

        Compares the task's ``HH:MM`` time against the current wall-clock time using
        today's date. Tasks without a scheduled time or that are already ``"Completed"``
        are never considered overdue.

        Returns:
            bool: ``True`` when the task is ``"Pending"``, has a scheduled time, and
                the current moment is strictly after that time today; ``False`` otherwise.
        """
        if self.time is None or self.status == "Completed":
            return False
        task_hour, task_minute = map(int, self.time.split(":"))
        now = datetime.now()
        task_time = now.replace(hour=task_hour, minute=task_minute, second=0, microsecond=0)
        return now > task_time

    def next_occurrence(self) -> Optional[datetime]:
        """Return the next scheduled datetime for a recurring task, or None if not recurring.

        Starts from a candidate datetime equal to today at the task's ``HH:MM`` time.
        If that moment has already passed, it advances the candidate by one day
        (``"daily"``) or one week (``"weekly"``). Tasks with no time or no recurrence
        return ``None``.

        Returns:
            datetime | None: The next future datetime at which this task should run,
                or ``None`` if the task is not recurring or has no scheduled time.
        """
        if self.time is None or self.recurrence is None:
            return None
        task_hour, task_minute = map(int, self.time.split(":"))
        now = datetime.now()
        candidate = now.replace(hour=task_hour, minute=task_minute, second=0, microsecond=0)
        if self.recurrence == "daily":
            if candidate <= now:
                candidate += timedelta(days=1)
        elif self.recurrence == "weekly":
            if candidate <= now:
                candidate += timedelta(weeks=1)
        return candidate


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
        """Sort all owner tasks by time (primary) then priority (tiebreaker).

        Collects every task from every pet owned by ``self.owner`` and sorts them
        using a two-key tuple: ``(scheduled_time, priority_rank)``. Tasks without a
        scheduled time sort after all timed tasks (sentinel value ``"99:99"``).
        Priority rank maps ``"High"`` → 1, ``"Medium"`` → 2, ``"Low"`` → 3; unknown
        priorities sort last (rank 4). The result is stored in ``self.daily_plan``.
        """
        tasks = self.owner.get_all_tasks()
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        self.daily_plan = sorted(
            tasks,
            key=lambda t: (t.time or "99:99", priority_order.get(t.priority, 4))
        )

    def sort_by_time(self) -> list[Task]:
        """Return all owner tasks sorted by scheduled time. Tasks with no time go last."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda t: t.time or "99:99"
        )

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks belonging to the pet with the given name."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return list(pet.tasks)
        return []

    def filter_by_status(self, status: str) -> list[Task]:
        """Return all tasks across all pets matching the given status ('Pending'/'Completed')."""
        return [t for t in self.owner.get_all_tasks() if t.status.lower() == status.lower()]

    def filter_tasks(self, pet_name: Optional[str] = None, status: Optional[str] = None) -> list[Task]:
        """Return tasks filtered by pet name, status, or both combined.

        When ``pet_name`` is given, only tasks belonging to the matching pet are
        considered (case-insensitive). When ``status`` is given, only tasks whose
        ``status`` matches (case-insensitive) are kept. Both filters can be applied
        together; if neither is provided, all tasks across all pets are returned.

        Args:
            pet_name: Name of the pet to filter by, or ``None`` to include all pets.
            status: Task status to filter by (e.g. ``"Pending"`` or ``"Completed"``),
                or ``None`` to include all statuses.

        Returns:
            list[Task]: Tasks satisfying all supplied filter criteria.

        Examples:
            filter_tasks(pet_name="Buddy")             # all of Buddy's tasks
            filter_tasks(status="Pending")             # all pending tasks
            filter_tasks(pet_name="Buddy", status="Pending")  # Buddy's pending tasks only
        """
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for pet in self.owner.pets
                     if pet.name.lower() == pet_name.lower()
                     for t in pet.tasks]
        if status is not None:
            tasks = [t for t in tasks if t.status.lower() == status.lower()]
        return tasks

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete. If it recurs, add a new Pending instance for the next occurrence.

        Sets ``task.status`` to ``"Completed"`` via ``Task.mark_complete``, then calls
        ``Task.next_task`` to compute the next scheduled occurrence. If a next occurrence
        exists, the new task is appended to whichever pet already owns the completed task
        so that it appears in future plan generations.

        Args:
            task: The task to mark as completed. Must already belong to one of the
                owner's pets for the follow-up task to be attached correctly.

        Returns:
            Task | None: The newly created follow-up ``Task`` (status ``"Pending"``) if
                the completed task was recurring, or ``None`` if it was a one-off task.
        """
        task.mark_complete()

        next_task = task.next_task()
        if next_task is None:
            return None

        # Attach the new task to whichever pet owns the completed task
        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.add_task(next_task)
                break

        return next_task

    def find_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose time windows overlap.

        Converts each timed task's ``HH:MM`` start time to total minutes since
        midnight, then checks every unique pair using the standard interval-overlap
        condition: two intervals [a_start, a_end) and [b_start, b_end) overlap when
        ``a_start < b_end and b_start < a_end``. Tasks without a scheduled time are
        excluded from conflict detection.

        Returns:
            list[tuple[Task, Task]]: Every unordered pair ``(a, b)`` of tasks whose
                time windows overlap. Returns an empty list when there are no conflicts.
        """
        timed = [t for t in self.owner.get_all_tasks() if t.time is not None]
        conflicts = []
        for i in range(len(timed)):
            for j in range(i + 1, len(timed)):
                a, b = timed[i], timed[j]
                a_hour, a_min = map(int, a.time.split(":"))
                b_hour, b_min = map(int, b.time.split(":"))
                a_start = a_hour * 60 + a_min
                b_start = b_hour * 60 + b_min
                a_end = a_start + a.duration
                b_end = b_start + b.duration
                if a_start < b_end and b_start < a_end:
                    conflicts.append((a, b))
        return conflicts

    def view_plan(self):
        """Return the ordered daily plan."""
        return self.daily_plan

    def explain_plan(self):
        """Return a string explaining the ordering logic used for the daily plan."""
        return "Tasks are sorted by scheduled time, with priority as a tiebreaker (High -> Medium -> Low)."
