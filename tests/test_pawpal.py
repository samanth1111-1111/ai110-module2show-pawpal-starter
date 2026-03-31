import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import patch
from datetime import datetime

from pawpal_system import Task, Pet, Owner, Schedule


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_owner_with_pets():
    """Return a Schedule pre-loaded with Buddy (2 tasks) and Luna (2 tasks)."""
    owner = Owner(name="Sam", contact_info="sam@email.com")
    buddy = Pet(name="Buddy", age=3, breed="Golden Retriever", medical_info="None")
    luna  = Pet(name="Luna",  age=5, breed="Siamese Cat",      medical_info="None")

    buddy.add_task(Task(title="Morning Walk", duration=30, priority="High",   time="07:00", recurrence="daily"))
    buddy.add_task(Task(title="Evening Walk", duration=30, priority="Medium", time="18:00"))

    luna.add_task(Task(title="Give Luna Meds", duration=5,  priority="High",   time="09:00", recurrence="daily"))
    luna.add_task(Task(title="Brush Luna",     duration=15, priority="Medium", time="14:00"))

    owner.add_pet(buddy)
    owner.add_pet(luna)
    return Schedule(owner), buddy, luna


# ---------------------------------------------------------------------------
# Task: mark_complete
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task(title="Feed Dog", duration=10, priority="High", time="08:00")
    assert task.status == "Pending"
    task.mark_complete()
    assert task.status == "Completed"


# ---------------------------------------------------------------------------
# Task: is_overdue
# ---------------------------------------------------------------------------

def test_is_overdue_no_time_returns_false():
    task = Task(title="Checkup", duration=30, priority="High")
    assert task.is_overdue() is False


def test_is_overdue_completed_returns_false():
    task = Task(title="Walk", duration=20, priority="High", time="07:00")
    task.mark_complete()
    assert task.is_overdue() is False


def test_is_overdue_past_time_returns_true():
    task = Task(title="Walk", duration=20, priority="High", time="07:00")
    future_now = datetime(2025, 1, 1, 10, 0, 0)  # 10:00, well after 07:00
    with patch("pawpal_system.datetime") as mock_dt:
        mock_dt.now.return_value = future_now
        assert task.is_overdue() is True


def test_is_overdue_future_time_returns_false():
    task = Task(title="Walk", duration=20, priority="High", time="23:00")
    early_now = datetime(2025, 1, 1, 6, 0, 0)  # 06:00, before 23:00
    with patch("pawpal_system.datetime") as mock_dt:
        mock_dt.now.return_value = early_now
        assert task.is_overdue() is False


# ---------------------------------------------------------------------------
# Task: next_occurrence / next_task
# ---------------------------------------------------------------------------

def test_next_occurrence_none_when_no_recurrence():
    task = Task(title="Walk", duration=20, priority="High", time="07:00")
    assert task.next_occurrence() is None


def test_next_occurrence_none_when_no_time():
    task = Task(title="Walk", duration=20, priority="High", recurrence="daily")
    assert task.next_occurrence() is None


def test_next_occurrence_daily_advances_when_past():
    task = Task(title="Walk", duration=20, priority="High", time="07:00", recurrence="daily")
    # Simulate current time at 08:00 — candidate 07:00 has already passed
    now = datetime(2025, 1, 1, 8, 0, 0)
    with patch("pawpal_system.datetime") as mock_dt:
        mock_dt.now.return_value = now
        result = task.next_occurrence()
    assert result.day == 2  # advanced to next day
    assert result.hour == 7


def test_next_occurrence_weekly_advances_when_past():
    task = Task(title="Walk", duration=20, priority="High", time="07:00", recurrence="weekly")
    now = datetime(2025, 1, 1, 8, 0, 0)
    with patch("pawpal_system.datetime") as mock_dt:
        mock_dt.now.return_value = now
        result = task.next_occurrence()
    assert result.day == 8  # advanced by 7 days


def test_next_task_returns_pending_copy():
    task = Task(title="Walk", duration=20, priority="High", time="07:00", recurrence="daily")
    now = datetime(2025, 1, 1, 8, 0, 0)
    with patch("pawpal_system.datetime") as mock_dt:
        mock_dt.now.return_value = now
        next_t = task.next_task()
    assert next_t is not None
    assert next_t.status == "Pending"
    assert next_t.title == task.title
    assert next_t.recurrence == "daily"


def test_next_task_none_for_non_recurring():
    task = Task(title="Vet", duration=30, priority="High", time="09:00")
    assert task.next_task() is None


# ---------------------------------------------------------------------------
# Pet: add / remove tasks
# ---------------------------------------------------------------------------

def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", age=3, breed="Golden Retriever", medical_info="None")
    task = Task(title="Morning Walk", duration=30, priority="High", time="07:00")
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_remove_task_decreases_pet_task_count():
    pet = Pet(name="Buddy", age=3, breed="Golden Retriever", medical_info="None")
    task = Task(title="Morning Walk", duration=30, priority="High", time="07:00")
    pet.add_task(task)
    pet.remove_task(task)
    assert len(pet.tasks) == 0


def test_remove_task_not_in_list_does_not_raise():
    pet = Pet(name="Buddy", age=3, breed="Golden Retriever", medical_info="None")
    task = Task(title="Ghost Task", duration=5, priority="Low")
    pet.remove_task(task)  # should not raise


# ---------------------------------------------------------------------------
# Schedule: sorting
# ---------------------------------------------------------------------------

def test_sort_by_time_untimed_tasks_go_last():
    schedule, buddy, _ = make_owner_with_pets()
    buddy.add_task(Task(title="No Time Task", duration=10, priority="High"))
    result = schedule.sort_by_time()
    assert result[-1].time is None


def test_generate_daily_plan_priority_tiebreaker():
    owner = Owner(name="Sam", contact_info="x")
    pet = Pet(name="Buddy", age=2, breed="Lab", medical_info="None")
    high = Task(title="High Task",   duration=10, priority="High",   time="09:00")
    low  = Task(title="Low Task",    duration=10, priority="Low",    time="09:00")
    med  = Task(title="Medium Task", duration=10, priority="Medium", time="09:00")
    pet.add_task(low)
    pet.add_task(med)
    pet.add_task(high)
    owner.add_pet(pet)
    schedule = Schedule(owner)
    schedule.generate_daily_plan()
    plan = schedule.view_plan()
    assert plan[0].priority == "High"
    assert plan[1].priority == "Medium"
    assert plan[2].priority == "Low"


def test_generate_daily_plan_unknown_priority_sorts_last():
    owner = Owner(name="Sam", contact_info="x")
    pet = Pet(name="Buddy", age=2, breed="Lab", medical_info="None")
    pet.add_task(Task(title="Low",     duration=10, priority="Low",      time="09:00"))
    pet.add_task(Task(title="Unknown", duration=10, priority="Critical", time="09:00"))
    owner.add_pet(pet)
    schedule = Schedule(owner)
    schedule.generate_daily_plan()
    plan = schedule.view_plan()
    assert plan[-1].priority == "Critical"


# ---------------------------------------------------------------------------
# Schedule: filtering
# ---------------------------------------------------------------------------

def test_filter_by_pet_case_insensitive():
    schedule, _, _ = make_owner_with_pets()
    assert schedule.filter_by_pet("buddy") == schedule.filter_by_pet("Buddy")


def test_filter_by_pet_unknown_name_returns_empty():
    schedule, _, _ = make_owner_with_pets()
    assert schedule.filter_by_pet("Fido") == []


def test_filter_by_status_pending_excludes_completed():
    schedule, buddy, _ = make_owner_with_pets()
    buddy.tasks[0].mark_complete()
    pending = schedule.filter_by_status("Pending")
    assert all(t.status == "Pending" for t in pending)


def test_filter_tasks_combined_pet_and_status():
    schedule, _, luna = make_owner_with_pets()
    luna.tasks[0].mark_complete()
    result = schedule.filter_tasks(pet_name="Luna", status="Pending")
    assert all(t.status == "Pending" for t in result)
    # All returned tasks must belong to Luna
    assert all(t in luna.tasks for t in result)


def test_filter_tasks_no_args_returns_all():
    schedule, buddy, luna = make_owner_with_pets()
    all_tasks = schedule.filter_tasks()
    assert len(all_tasks) == len(buddy.tasks) + len(luna.tasks)


# ---------------------------------------------------------------------------
# Schedule: conflict detection
# ---------------------------------------------------------------------------

def test_find_conflicts_overlapping_tasks():
    owner = Owner(name="Sam", contact_info="x")
    pet = Pet(name="Buddy", age=2, breed="Lab", medical_info="None")
    a = Task(title="Walk",    duration=30, priority="High", time="07:00")
    b = Task(title="Feed",    duration=20, priority="High", time="07:20")  # starts inside a
    pet.add_task(a)
    pet.add_task(b)
    owner.add_pet(pet)
    conflicts = Schedule(owner).find_conflicts()
    assert (a, b) in conflicts


def test_find_conflicts_adjacent_tasks_no_conflict():
    owner = Owner(name="Sam", contact_info="x")
    pet = Pet(name="Buddy", age=2, breed="Lab", medical_info="None")
    a = Task(title="Walk", duration=30, priority="High", time="07:00")  # ends 07:30
    b = Task(title="Feed", duration=10, priority="High", time="07:30")  # starts 07:30
    pet.add_task(a)
    pet.add_task(b)
    owner.add_pet(pet)
    conflicts = Schedule(owner).find_conflicts()
    assert conflicts == []


def test_find_conflicts_untimed_tasks_ignored():
    owner = Owner(name="Sam", contact_info="x")
    pet = Pet(name="Buddy", age=2, breed="Lab", medical_info="None")
    pet.add_task(Task(title="No Time A", duration=30, priority="High"))
    pet.add_task(Task(title="No Time B", duration=30, priority="High"))
    owner.add_pet(pet)
    assert Schedule(owner).find_conflicts() == []


def test_find_conflicts_cross_pet():
    owner = Owner(name="Sam", contact_info="x")
    buddy = Pet(name="Buddy", age=2, breed="Lab",    medical_info="None")
    luna  = Pet(name="Luna",  age=3, breed="Siamese", medical_info="None")
    a = Task(title="Buddy Walk", duration=30, priority="High", time="18:00")
    b = Task(title="Luna Walk",  duration=20, priority="Low",  time="18:10")  # overlaps a
    buddy.add_task(a)
    luna.add_task(b)
    owner.add_pet(buddy)
    owner.add_pet(luna)
    conflicts = Schedule(owner).find_conflicts()
    assert (a, b) in conflicts


# ---------------------------------------------------------------------------
# Schedule: complete_task
# ---------------------------------------------------------------------------

def test_complete_task_marks_done():
    schedule, buddy, _ = make_owner_with_pets()
    task = buddy.tasks[1]  # Evening Walk — non-recurring
    schedule.complete_task(task)
    assert task.status == "Completed"


def test_complete_task_non_recurring_returns_none():
    schedule, buddy, _ = make_owner_with_pets()
    task = buddy.tasks[1]  # Evening Walk — no recurrence
    result = schedule.complete_task(task)
    assert result is None


def test_complete_task_recurring_adds_to_correct_pet():
    schedule, buddy, luna = make_owner_with_pets()
    now = datetime(2025, 1, 1, 8, 0, 0)
    with patch("pawpal_system.datetime") as mock_dt:
        mock_dt.now.return_value = now
        next_t = schedule.complete_task(buddy.tasks[0])  # Morning Walk — daily
    assert next_t in buddy.tasks
    assert next_t not in luna.tasks


def test_complete_task_recurring_new_task_is_pending():
    schedule, buddy, _ = make_owner_with_pets()
    now = datetime(2025, 1, 1, 8, 0, 0)
    with patch("pawpal_system.datetime") as mock_dt:
        mock_dt.now.return_value = now
        next_t = schedule.complete_task(buddy.tasks[0])
    assert next_t.status == "Pending"
