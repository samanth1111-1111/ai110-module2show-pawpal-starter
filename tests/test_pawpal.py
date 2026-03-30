import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(title="Feed Dog", duration=10, priority="High", time="08:00")
    assert task.status == "Pending"
    task.mark_complete()
    assert task.status == "Completed"


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", age=3, breed="Golden Retriever", medical_info="None")
    task = Task(title="Morning Walk", duration=30, priority="High", time="07:00")
    assert len(pet.tasks) == 0
    pet.tasks.append(task)
    assert len(pet.tasks) == 1
