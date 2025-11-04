# Simple Task CLI

A small command-line task manager in Python. Commands: `add`, `list`, `search`. Tasks are stored as JSON objects in a `tasks.json` file.

## Run (development)

From the project root (the directory containing the `simple-task-cli` package):

```bash
# use local source without installing
PYTHONPATH=simple-task-cli/src python -m simple_task_cli.cli <command> [options]
```

Or run the module directly:

```bash
python simple-task-cli/src/simple_task_cli/cli.py <command> [options]
```

Install editable so `python -m` works without PYTHONPATH:

```bash
cd simple-task-cli
pip install -e .
# then from project root:
python -m simple_task_cli.cli <command> [options]
```

## Commands

All examples assume running via `PYTHONPATH=... python -m simple_task_cli.cli`.

1) add — create a new task
```
python -m simple_task_cli.cli add "<title>" "[description]"
```
- title: required
- description: optional (use quotes if contains spaces)
- Example:
  ```
  python -m simple_task_cli.cli add "Buy milk" "2 liters"
  ```
- Output: prints the added task (JSON-like dict). The CLI assigns an incremental numeric `id`.

2) list — show all tasks
```
python -m simple_task_cli.cli list
```
- Prints the entire tasks array (pretty-printed JSON).
- Example output:
  ```json
  [
    {"id": 1, "title": "Buy milk", "description": "2 liters"},
    {"id": 2, "title": "Write report", "description": ""}
  ]
  ```

3) search — find tasks by query
```
python -m simple_task_cli.cli search -q <query> [-f FIELD] [--exact]
```
Options:
- `-q`, `--query` (required): search string or id value
- `-f`, `--field`: one of `title`, `description`, `id`, `all` (default: `all`)
  - `title` — search task titles
  - `description` — search task descriptions
  - `id` — numeric id match (use `--exact` for exact numeric matches)
  - `all` — title + description combined
- `--exact`: perform exact (full-string or numeric) match instead of substring search

Examples:
- substring search across title + description:
  ```
  python -m simple_task_cli.cli search -q test
  ```
- search only titles (case-insensitive substring):
  ```
  python -m simple_task_cli.cli search -q "buy" -f title
  ```
- search by id (exact numeric match):
  ```
  python -m simple_task_cli.cli search -q 1 -f id --exact
  ```
Output: pretty-printed JSON array of matches or `No tasks found.` if none match.

## tasks.json location and initialization

The CLI prefers a `data/tasks.json` in the project root first, then falls back to package-local locations. If no file exists the CLI will create `simple-task-cli/data/tasks.json` initialized to `[]`.

To manually initialize:
```bash
# from project root
mkdir -p simple-task-cli/data
echo '[]' > simple-task-cli/data/tasks.json
```
Or to place `tasks.json` at project root:
```bash
mkdir -p data
echo '[]' > data/tasks.json
```

## Help / exit codes
- Show help:
  ```
  PYTHONPATH=simple-task-cli/src python -m simple_task_cli.cli -h
  PYTHONPATH=simple-task-cli/src python -m simple_task_cli.cli search -h
  ```
- Exit codes:
  - `0` — success
  - non-zero — error (invalid JSON, missing args, etc.)

## Notes
- The CLI writes updates to whichever `tasks.json` it resolves (see locations above). Ensure you point the CLI at the intended file if you maintain multiple copies.
- If you have an unused Node helper in the repo, it is safe to remove or archive it if you only use the Python CLI.