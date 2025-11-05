# Simple Task CLI

A small command-line task manager in Python. The project provides two primary commands: `add` and `list`. Tasks are stored as JSON objects in a `tasks.json` file.

## Run (development)

From the project root (the directory containing the `simple-task-cli` package) you can run the CLI using the local `src` tree without installing:

```bash
# use local source without installing
PYTHONPATH=simple-task-cli/src python -m simple_task_cli.cli <command> [options]
```

Or run the module file directly (not recommended for normal use):

```bash
python simple-task-cli/src/simple_task_cli/cli.py <command> [options]
```

Install editable so `python -m` works without setting `PYTHONPATH`:

```bash
cd simple-task-cli
python -m pip install -e .
# then from project root:
python -m simple_task_cli.cli <command> [options]
```

## Commands

All examples below assume running via `PYTHONPATH=simple-task-cli/src python -m simple_task_cli.cli` unless you installed the package.

1) add — create a new task
```bash
python -m simple_task_cli.cli add "<title>" "<description>"
```
- `title`: required (use quotes if it contains spaces)
- `description`: optional (use quotes if it contains spaces)

Example:
```bash
python -m simple_task_cli.cli add "Buy milk" "2 liters"
```

On success the CLI prints the added task, for example:
```
Task added: {'id': 1, 'title': 'Buy milk', 'description': '2 liters'}
```

2) list — show all tasks
```bash
python -m simple_task_cli.cli list
```

This prints each task on a separate line, for example:
```
ID: 1, Title: Buy milk, Description: 2 liters
ID: 2, Title: Write report, Description:
```

## tasks.json location and initialization

The CLI resolves `tasks.json` in this order:
1. `data/tasks.json` in the project root (preferred)
2. `simple-task-cli/data/tasks.json` inside the package
3. If none exists the CLI will create `simple-task-cli/data/tasks.json` initialized to `[]`.

To manually initialize an empty `tasks.json` in the package data folder:
```bash
# from project root
mkdir -p simple-task-cli/data
echo '[]' > simple-task-cli/data/tasks.json
```

Or to place `tasks.json` at the project root:
```bash
mkdir -p data
echo '[]' > data/tasks.json
```

## Help

Show help for the CLI:
```bash
PYTHONPATH=simple-task-cli/src python -m simple_task_cli.cli -h
```

If you installed the package editable:
```bash
python -m simple_task_cli.cli -h
```

## Notes

- Use `PYTHONPATH` while developing, or install editable with `pip install -e` for convenience.
- The CLI writes updates to whichever `tasks.json` it resolves; make sure you edit or check the correct file if you maintain multiple copies.
