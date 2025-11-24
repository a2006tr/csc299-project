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
   python -m final add "Homework 1" "Chapter 1 problems"
   # you'll be prompted: Due date (YYYY-MM-DD):
   ```

3. Add non-interactively with `--due`:

   ```bash
   python -m final add "Homework 2" "Read chapter 2" --due 2025-11-30
   ```

4. List tasks (grouped and sorted by due date):

   ```bash
   python -m final list
   ```

5. Search (by title, description, id, or date):

   ```bash
   python -m final search -q home -f title
   python -m final search -q 2025-11-30 -f date
   ```

6. Mark a task done (removes it):

   ```bash
   python -m final done 1
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

AI features
-----------

This project includes optional AI-powered helpers. They are disabled by default
and only run when the OpenAI SDK is installed and the environment variable
`OPENAI_API_KEY` is set.

Install and configure

1. Install the OpenAI SDK used by the project (example package name):

    ```bash
    pip install openai
    ```

2. Export your API key:

    ```bash
    export OPENAI_API_KEY="sk-..."
    ```

Summarize descriptions when adding

Add a task and ask the CLI to summarize the long description into a short
phrase that will be stored as the `summary` field on the task:

```bash
python -m final add "Homework 3" "Long paragraph describing the assignment" --due 2025-12-01 --summarize
```

If the API is configured the CLI will print the AI-produced summary and store
it on the task; otherwise it will print an error message and continue.

Process files in a folder with AI

The `ai-process` command sends each text file in a folder to the AI model and
writes the assistant's returned content to a `done/` subfolder inside the
input folder, preserving the original filenames. This is useful for asking the
model to rewrite, annotate, or otherwise improve homework files.

Usage:

```bash
python -m final ai-process path/to/homework_folder
```

Project example
---------------

This repository contains a sample assignments folder at the project root:

- Relative path: `assignments/`
- Absolute path: `/Users/arturo/Desktop/project3/final1/assignments`

The command below will process files placed in that folder and write outputs
to `assignments/done/` (created if missing):

```bash
python -m final ai-process assignments
```

Behavior and safety notes
- AI calls are performed lazily to avoid requiring the SDK when running tests or
   using non-AI features.
- The model and prompt are conservative (low temperature and token limits) but
   you should review any generated outputs before using them.
- If you want a dry-run mode, retry/backoff, or mocked tests for AI, I can add
   them.
