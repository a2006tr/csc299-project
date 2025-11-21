def inc(n: int) -> int:
    return n + 1
from pathlib import Path
import argparse
import json
import sys

TASKS_LOCATIONS = [
    Path(__file__).parent / "tasks.json",
    Path(__file__).parent.parent / "tasks.json",
    Path(__file__).resolve().parents[2] / "data" / "tasks.json",  # project-root/data/tasks.json
    Path.cwd() / "data" / "tasks.json",                           # working-dir/data/tasks.json
]

def find_tasks_file():
    # Prefer the project data/tasks.json when present (or create it there).
    data_path = Path(__file__).resolve().parents[2] / "data" / "tasks.json"
    # If a data/tasks.json exists use it
    if data_path.exists():
        return data_path
    # Otherwise fall back to any other existing candidate
    for p in TASKS_LOCATIONS:
        if p.exists():
            return p
    # If none exist, ensure the data directory and initialize the file there
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text("[]", encoding="utf-8")
    return data_path

def load_tasks():
    p = find_tasks_file()
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in {p}: {e}")

def save_tasks(tasks):
    p = find_tasks_file()
    p.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")
    return p

def cmd_add(args):
    # Add a task and write it to the selected tasks.json (prefer data/tasks.json)
    tasks = load_tasks()
    max_id = max((t.get("id", 0) for t in tasks), default=0)
    task_id = max_id + 1
    title = getattr(args, "title", None)
    description = getattr(args, "description", "") or ""
    task = {"id": task_id, "title": title, "description": description}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task}")
    return 0

def cmd_list(args):
    tasks = load_tasks()
    print(json.dumps(tasks, indent=2))
    return 0

def matches(task, query, field, exact):
    if field == "id":
        try:
            qnum = int(query)
        except ValueError:
            return False
        return task.get("id") == qnum
    def s(x): return (x or "").lower()
    q = str(query).lower()
    if field == "title":
        return (task.get("title") == query) if exact else q in s(task.get("title"))
    if field == "description":
        return (task.get("description") == query) if exact else q in s(task.get("description"))
    # all
    combined = f"{task.get('title','')} {task.get('description','')}".lower()
    return (combined == q) if exact else q in combined

def cmd_search(args):
    tasks = load_tasks()
    results = [t for t in tasks if matches(t, args.query, args.field, args.exact)]
    if not results:
        print("No tasks found.")
        return 0
    print(json.dumps(results, indent=2))
    return 0

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="python -m simple_task_cli.cli")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title")
    p_add.add_argument("description", nargs="?")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.set_defaults(func=cmd_list)

    p_search = sub.add_parser("search", help="Search tasks")
    p_search.add_argument("-q", "--query", required=True, help="Query string")
    p_search.add_argument("-f", "--field", choices=["title", "description", "id", "all"], default="all")
    p_search.add_argument("--exact", action="store_true", help="Exact match")
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
