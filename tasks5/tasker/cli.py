import argparse
from pathlib import Path
from typing import Optional

from .storage import TaskStore


def _print_task(t):
    print(f"[{t.id}] {t.title}")
    if t.description:
        print(f"    {t.description}")
    print(f"    created: {t.created_at}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasker", description="Simple task manager")
    parser.add_argument("--data", default="./.tasker/tasks.json", help="Path to JSON data file")

    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a new task")
    add.add_argument("title")
    add.add_argument("--description", "-d", default=None)

    listp = sub.add_parser("list", help="List tasks")

    search = sub.add_parser("search", help="Search tasks")
    search.add_argument("query")

    return parser


def main(argv: Optional[list] = None):
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TaskStore(args.data)

    if args.cmd == "add":
        t = store.add(args.title, args.description)
        print("Added:")
        _print_task(t)
    elif args.cmd == "list":
        for t in store.list():
            _print_task(t)
    elif args.cmd == "search":
        for t in store.search(args.query):
            _print_task(t)


if __name__ == "__main__":
    main()
