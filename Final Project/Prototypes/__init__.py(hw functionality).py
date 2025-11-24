def inc(n: int) -> int:
    return n + 1

from pathlib import Path
import argparse
import json
import sys
from datetime import date

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
    if not p.exists():
        # initialize empty tasks file
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("[]", encoding="utf-8")
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
    # Use provided due date if passed via CLI; otherwise prompt interactively.
    due = getattr(args, "due", None)
    if due:
        try:
            date.fromisoformat(due)
        except ValueError:
            print("Invalid date format for --due. Use YYYY-MM-DD.")
            return 1
    else:
        # Prompt for a due date (ISO YYYY-MM-DD). Keep asking until a valid date is
        # provided so tasks are associated with specific dates.
        while True:
            try:
                s = input("Due date (YYYY-MM-DD): ").strip()
            except EOFError:
                print("No due date provided; cancelling add.")
                return 1
            if not s:
                print("Please enter a due date in YYYY-MM-DD format.")
                continue
            try:
                # Validate ISO format
                _d = date.fromisoformat(s)
                due = s
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
    task = {"id": task_id, "title": title, "description": description, "due_date": due}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task}")
    return 0

def cmd_list(args):
    tasks = load_tasks()
    # Group tasks by due date (ISO string). Tasks without due_date go last.
    groups = {}
    no_date = []
    for t in tasks:
        d = t.get("due_date")
        if not d:
            no_date.append(t)
        else:
            groups.setdefault(d, []).append(t)

    # Sort dates ascending (closest first)
    def parse_key(k):
        try:
            return date.fromisoformat(k)
        except Exception:
            return date.max

    for d in sorted(groups.keys(), key=parse_key):
        print(d)
        for t in sorted(groups[d], key=lambda x: x.get("id")):
            print(f"- [{t.get('id')}] {t.get('title')} : {t.get('description')}")
        print()

    if no_date:
        print("No due date:")
        for t in no_date:
            print(f"- [{t.get('id')}] {t.get('title')} : {t.get('description')}")
    return 0
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
    if field == "date" or field == "due_date":
        # exact match compares whole date string; otherwise substring
        return (task.get("due_date") == query) if exact else q in s(task.get("due_date"))
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

def cmd_done(args):
    tasks = load_tasks()
    try:
        remove_id = int(args.id)
    except ValueError:
        print("Invalid id")
        return 1
    new = [t for t in tasks if t.get("id") != remove_id]
    if len(new) == len(tasks):
        print(f"No task with id {remove_id}")
        return 1
    save_tasks(new)
    print(f"Removed task {remove_id}")
    return 0

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="python -m simple_task_cli.cli")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title")
    p_add.add_argument("description", nargs="?")
    p_add.add_argument("--due", help="Due date in YYYY-MM-DD (optional)")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.set_defaults(func=cmd_list)

    p_search = sub.add_parser("search", help="Search tasks")
    p_search.add_argument("-q", "--query", required=True, help="Query string")
    p_search.add_argument("-f", "--field", choices=["title", "description", "id", "all", "date", "due_date"], default="all")
    p_search.add_argument("--exact", action="store_true", help="Exact match")
    p_search.set_defaults(func=cmd_search)

    p_done = sub.add_parser("done", help="Mark task done and remove it")
    p_done.add_argument("id", help="ID of task to remove")
    p_done.set_defaults(func=cmd_done)

    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
