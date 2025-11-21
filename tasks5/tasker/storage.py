import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


@dataclass
class Task:
    id: int
    title: str
    description: Optional[str]
    created_at: str


class TaskStore:
    """Simple JSON-backed task store.

    Responsibilities:
    - persist tasks to a JSON file
    - provide add/list/search operations
    """

    def __init__(self, path: str):
        self.path = Path(path)
        self._ensure_file()

    def _ensure_file(self):
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps({"tasks": []}, indent=2))

    def _read(self) -> List[dict]:
        data = json.loads(self.path.read_text())
        return data.get("tasks", [])

    def _write(self, tasks: List[dict]):
        self.path.write_text(json.dumps({"tasks": tasks}, indent=2))

    def list(self) -> List[Task]:
        raw = self._read()
        return [Task(**r) for r in raw]

    def add(self, title: str, description: Optional[str] = None) -> Task:
        tasks = self._read()
        next_id = max((t.get("id", 0) for t in tasks), default=0) + 1
        t = Task(
            id=next_id,
            title=title,
            description=description,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        tasks.append(asdict(t))
        self._write(tasks)
        return t

    def search(self, q: str) -> List[Task]:
        q_lower = q.lower()
        return [t for t in self.list() if q_lower in t.title.lower() or (t.description and q_lower in t.description.lower())]
