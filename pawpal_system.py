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
        pass

    def update_task(self, title=None, duration=None, priority=None, time=None):
        pass

    def is_overdue(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    age: int
    breed: str
    medical_info: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def view_tasks(self):
        pass

    def update_info(self, new_info: str):
        pass


class Owner:
    def __init__(self, name: str, contact_info: str):
        self.name = name
        self.contact_info = contact_info
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, pet: Pet):
        pass

    def view_all_pets(self):
        pass


class Schedule:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []
        self.daily_plan: list[Task] = []

    def generate_daily_plan(self):
        pass

    def view_plan(self):
        pass

    def explain_plan(self):
        pass
