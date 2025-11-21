Running the Tasker prototype
============================

Prerequisites
-------------
- Python 3.8+
- pip (for installing test/development deps) — optional if you run with `python -m` directly

Quick install (recommended for development)
-----------------------------------------
1. From the project root:

```bash
cd /Users/arturo/Desktop/project3/tasks5
python -m pip install -e .
```

2. After install you can use the `tasker` console script:

```bash
tasker --data ./.tasker/tasks.json add "Buy milk" --description "2 liters"
tasker --data ./.tasker/tasks.json list
tasker --data ./.tasker/tasks.json search milk
```

Run without installing
----------------------
If you prefer not to install, use the module runner:

```bash
python -m tasker.cli --data ./.tasker/tasks.json add "Buy milk" --description "2 liters"
python -m tasker.cli --data ./.tasker/tasks.json list
```

Notes on the `--data` option
----------------------------
- The default in the CLI is `./.tasker/tasks.json`. The directory will be created automatically when adding tasks.
- You can point `--data` to any writable path.

Running tests
-------------
1. Install test deps:

```bash
python -m pip install -r requirements.txt
```

2. Run pytest:

```bash
pytest -q
```

Development tips and troubleshooting
----------------------------------
- If tests fail with `ModuleNotFoundError: No module named 'tasker'`, install the package in editable mode (`pip install -e .`) or run tests using the repo root on `PYTHONPATH`:

```bash
PYTHONPATH=. pytest -q
```

- The tests currently add the repo root to `sys.path` as a quick compatibility measure during development; prefer installing the package to avoid that.
- To remove a deprecation warning about `datetime.utcnow()`, the project already uses timezone-aware timestamps (`datetime.now(timezone.utc)`) in `tasker/storage.py`.

Next improvements (suggested)
---------------------------
- Add GitHub Actions workflow to run tests on PRs and main branch.
- Add more unit tests (CLI behavior, edge-case persistence).
- Add type checking (mypy) and a linter (ruff/flake8) in CI.
