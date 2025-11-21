import json
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so pytest can import the local package
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from tasker.storage import TaskStore


def test_add_and_list(tmp_path: Path):
    data = tmp_path / "tasks.json"
    store = TaskStore(str(data))

    t1 = store.add("Buy milk", "2 liters")
    t2 = store.add("Call Alice", None)

    all_tasks = store.list()
    assert len(all_tasks) == 2
    titles = [t.title for t in all_tasks]
    assert "Buy milk" in titles and "Call Alice" in titles


def test_search(tmp_path: Path):
    data = tmp_path / "tasks.json"
    store = TaskStore(str(data))
    store.add("Fix bug", "null pointer in parser")
    store.add("Write docs", "usage examples")

    res = store.search("bug")
    assert len(res) == 1
    assert res[0].title == "Fix bug"

    res2 = store.search("usage")
    assert len(res2) == 1
    assert res2[0].title == "Write docs"
