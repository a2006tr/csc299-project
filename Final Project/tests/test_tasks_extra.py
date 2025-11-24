import json
from final import load_tasks, save_tasks, matches, main


def test_add_with_due_and_done(tmp_path, monkeypatch):
    fake_file = tmp_path / "tasks.json"
    monkeypatch.setattr("final.find_tasks_file", lambda: fake_file)

    # Add a task non-interactively using --due
    rc = main(["add", "HW1", "Chapter 1", "--due", "2025-11-30"])
    assert rc == 0

    tasks = load_tasks()
    assert len(tasks) == 1
    t = tasks[0]
    assert t["title"] == "HW1"
    assert t["due_date"] == "2025-11-30"

    # Search by date
    rc = main(["search", "-q", "2025-11-30", "-f", "date"]) or 0
    # search prints results but returns 0

    # Mark done
    rc = main(["done", str(t["id"])])
    assert rc == 0
    assert load_tasks() == []
