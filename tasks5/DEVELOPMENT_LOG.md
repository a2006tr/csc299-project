Development log — Trials, errors, and fixes
=========================================

This log records the main steps, problems, and fixes while building the `tasker` prototype.

1) Initial scaffold
--------------------
- Created `tasker` package with `storage.py` and `cli.py` and added a simple `Task` dataclass.
- Wrote `tests/test_storage.py` to validate `add`, `list`, and `search` behavior.

Problems found and actions
--------------------------

- ModuleImportError in pytest
  - Symptom: pytest failed to import `tasker`: "ModuleNotFoundError: No module named 'tasker'" during test collection.
  - Root cause: Tests ran without package installed and Python path didn't include the repository root.
  - Fixes:
    1. Short-term: Inserted repo root into `sys.path` in `tests/test_storage.py` to allow importing the local package during test runs.
    2. Long-term: Added `pyproject.toml` so the project can be installed in editable mode (`pip install -e .`) which is the preferred developer workflow.

- Missing pip/pytest in environment
  - Symptom: In this environment, running `pip` and `pytest` initially returned "command not found".
  - Root cause: The execution environment used by the agent didn't have package management tools available.
  - Fix: Tests were executed using the environment provided by the user's machine when the commands were run there; instructions were added in `INSTRUCTIONS.md` to install deps locally.

- Deprecation warning for datetime.utcnow()
  - Symptom: pytest reported DeprecationWarning recommending timezone-aware datetimes.
  - Fix: Replaced `datetime.utcnow().isoformat()` with `datetime.now(timezone.utc).isoformat()` in `tasker/storage.py`.

- IndentationError after a quick edit
  - Symptom: After modifying `storage.py` to use timezone-aware timestamps, an indentation error was introduced in the `add` method causing test collection failure.
  - Fix: Corrected indentation and formatted `Task` instantiation across multiple lines for clarity.

2) Packaging and convenience
---------------------------
- Added `pyproject.toml` with setuptools backend and a `tasker` console script entry.
- Added `requirements.txt`, `README.md`, `INSTRUCTIONS.md`, and this `DEVELOPMENT_LOG.md` to document the project and developer steps.

3) Test results
---------------
- After fixes, the test suite passes locally: 2 passed, no warnings.

Suggestions for future work
--------------------------
- Replace `sys.path` manipulation in tests with editable install or pytest config.
- Add unit tests for CLI parsing and boundary cases (invalid data path, corrupted JSON file).
- Add CI (GitHub Actions) to run tests and linting automatically on PRs.
- Consider adding serialization validation (schema) to avoid corrupt JSON states.

Notes
-----
- This log is intentionally concise yet concrete. It captures actionable steps and recommended next tasks for maintainers.
