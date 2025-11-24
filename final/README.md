# Homework Calendar / Tracker CLI

This small CLI stores assignments (tasks) with due dates in a JSON file and
supports adding, listing, searching, and marking tasks as done.

Quick start
1. Make sure you're in the project root (where this README and `pyproject.toml` live):

   ```bash
   cd /path/to/project/final1
   ```

2. Add an assignment (interactive due date):

   ```bash
   python -m tasks3 add "Homework 1" "Chapter 1 problems"
   # you'll be prompted: Due date (YYYY-MM-DD):
   ```

3. Add non-interactively with `--due`:

   ```bash
   python -m tasks3 add "Homework 2" "Read chapter 2" --due 2025-11-30
   ```

4. List tasks (grouped and sorted by due date):

   ```bash
   python -m tasks3 list
   ```

5. Search (by title, description, id, or date):

   ```bash
   python -m tasks3 search -q home -f title
   python -m tasks3 search -q 2025-11-30 -f date
   ```

6. Mark a task done (removes it):

   ```bash
   python -m tasks3 done 1
   ```

Notes
- Tasks are stored in a `tasks.json` file under project `data/tasks.json` when
  present, or in a fallback location as defined by the module.
- Dates must be provided in `YYYY-MM-DD` format.

Running tests

The project includes pytest tests. Run them from the project root like this:

```bash
python3 -m pytest -q
```

If you want improvements (flexible date parsing, due-soon filters, nicer output), I can add them.
