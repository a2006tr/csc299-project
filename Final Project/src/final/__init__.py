def inc(n: int) -> int:
    return n + 1

from pathlib import Path
import argparse
import json
import sys
import os
import re
from datetime import date

TASKS_LOCATIONS = [
    Path(__file__).parent / "tasks.json",
    Path(__file__).parent.parent / "tasks.json",
    Path(__file__).resolve().parents[2] / "data" / "tasks.json",
    Path.cwd() / "data" / "tasks.json",
]


def find_tasks_file():
    data_path = Path(__file__).resolve().parents[2] / "data" / "tasks.json"
    if data_path.exists():
        return data_path
    for p in TASKS_LOCATIONS:
        if p.exists():
            return p
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text("[]", encoding="utf-8")
    return data_path


def load_tasks():
    p = find_tasks_file()
    if not p.exists():
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


def summarize_task(description: str) -> str:
    # Lazy import so environments without the SDK can still import this module
    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError("OpenAI SDK not available. Install the 'openai' package to use AI features.") from e

    if not ("OPENAI_API_KEY" in os.environ):
        raise RuntimeError("OPENAI_API_KEY not set; cannot call OpenAI API.")

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You summarize tasks as very short phrases, 15 words or less. "
                    "Output only the bare summary with no extra commentary."
                ),
            },
            {"role": "user", "content": "Summarize the following task description as a very short phrase:\n\n" + description},
        ],
        max_tokens=32,
        temperature=0.2,
    )
    try:
        return response.choices[0].message.content.strip()
    except Exception:
        raise RuntimeError("Unexpected response from OpenAI API")


def process_file_content_with_ai(content: str, filename: str | None = None) -> str:
    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError("OpenAI SDK not available. Install the 'openai' package to use AI features.") from e

    if not ("OPENAI_API_KEY" in os.environ):
        raise RuntimeError("OPENAI_API_KEY not set; cannot call OpenAI API.")

    client = OpenAI()
    system_msg = (
        "You are an assistant that helps produce a clear, finished version of a "
        "student's homework file. Return only the revised file content (no extra "
        "explanatory text). If the file contains code, return runnable code where "
        "possible."
    )
    user_msg = f"Process and improve the following file content. Return only the new file contents (no commentary):\n\n{content}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
        max_tokens=1600,
        temperature=0.2,
    )
    try:
        return response.choices[0].message.content
    except Exception:
        raise RuntimeError("Unexpected response from OpenAI API")


def cmd_add(args):
    tasks = load_tasks()
    max_id = max((t.get("id", 0) for t in tasks), default=0)
    task_id = max_id + 1
    title = getattr(args, "title", None)
    description = getattr(args, "description", "") or ""
    due = getattr(args, "due", None)
    if due:
        try:
            date.fromisoformat(due)
        except ValueError:
            print("Invalid date format for --due. Use YYYY-MM-DD.")
            return 1
    else:
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
                _d = date.fromisoformat(s)
                due = s
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
    task = {"id": task_id, "title": title, "description": description, "due_date": due}
    # Optionally summarize via AI
    if getattr(args, "summarize", False) and description:
        try:
            summary = summarize_task(description)
            task["summary"] = summary
            print(f"AI summary: {summary}")
        except Exception as e:
            print(f"AI summarization failed: {e}")
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task}")
    return 0


def cmd_list(args):
    tasks = load_tasks()
    groups = {}
    no_date = []
    for t in tasks:
        d = t.get("due_date")
        if not d:
            no_date.append(t)
        else:
            groups.setdefault(d, []).append(t)

    def parse_key(k):
        try:
            return date.fromisoformat(k)
        except Exception:
            return date.max

    for d in sorted(groups.keys(), key=parse_key):
        print(d)
        for t in sorted(groups[d], key=lambda x: x.get("id")):
            desc = t.get("summary") or t.get("description") or ""
            print(f"- [{t.get('id')}] {t.get('title')} : {desc}")
        print()

    if no_date:
        print("No due date:")
        for t in no_date:
            desc = t.get("summary") or t.get("description") or ""
            print(f"- [{t.get('id')}] {t.get('title')} : {desc}")
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
        return (task.get("due_date") == query) if exact else q in s(task.get("due_date"))
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


def cmd_ai_process(args):
    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"Not a folder: {folder}")
        return 1
    done_dir = folder / "done"
    done_dir.mkdir(exist_ok=True)
    files = [p for p in folder.iterdir() if p.is_file()]
    if not files:
        print("No files to process in folder.")
        return 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            print(f"Skipping binary or unreadable file: {f.name}")
            continue
        try:
            out = process_file_content_with_ai(text, filename=f.name)
        except RuntimeError as e:
            print(f"AI processing failed: {e}")
            return 2
        out_path = done_dir / f.name
        out_path.write_text(out, encoding="utf-8")
        print(f"Wrote: {out_path}")
    return 0


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="python -m final")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title")
    p_add.add_argument("description", nargs="?")
    p_add.add_argument("--due", help="Due date in YYYY-MM-DD (optional)")
    p_add.add_argument("--summarize", action="store_true", help="Use AI to summarize the description into a short phrase and store it as `summary`")
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
    p_ai = sub.add_parser("ai-process", help="Process all files in a folder with AI and write outputs to a 'done' subfolder")
    p_ai.add_argument("folder", help="Path to folder containing files to process")
    p_ai.set_defaults(func=cmd_ai_process)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
