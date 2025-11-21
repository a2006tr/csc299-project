import json
from tasks3 import load_tasks, save_tasks, matches


def test_save_and_load_round_trip(tmp_path, monkeypatch):
    """Ensure save_tasks() writes JSON and load_tasks() reads it correctly."""
    
    # Use a temporary tasks file (prevent writing into your real project)
    fake_file = tmp_path / "tasks.json"

    # Force find_tasks_file() to return our temporary file
    monkeypatch.setattr("tasks3.find_tasks_file", lambda: fake_file)

    tasks = [{"id": 1, "title": "test", "description": "abc"}]
    
    save_tasks(tasks)
    loaded = load_tasks()

    assert loaded == tasks


def test_matches_title_partial():
    """matches() should match substring in title when not exact."""
    task = {"id": 1, "title": "Finish homework", "description": ""}
    assert matches(task, "home", "title", exact=False)
    assert not matches(task, "xyz", "title", exact=False)


def test_matches_exact_description():
    """Exact match on description should only match full string."""
    task = {"id": 2, "title": "Task", "description": "hello world"}
    assert matches(task, "hello world", "description", exact=True)
    assert not matches(task, "hello", "description", exact=True)

