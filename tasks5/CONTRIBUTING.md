Contributing
============

Welcome — thank you for contributing. This document explains how to set up a dev environment, run tests, and follow our standards when opening PRs.

Developer setup
---------------
1. Clone and change directory:

```bash
git clone <repo_url>
cd /path/to/repo/tasks5
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the package in editable mode and dev deps:

```bash
python -m pip install -e .
python -m pip install -r requirements.txt
```

Running tests
-------------
Run the test suite with:

```bash
pytest -q
```

Quick linting and formatting
----------------------------
- We recommend using a formatter and linter (e.g., Black, ruff). Add them to your editor or run them manually.

PR checklist
------------
Before requesting review, ensure the following (adapted from the project constitution):

- Does the change have a clear purpose and matching issue/description?
- Are new functions small and single-purpose?
- Are types and linting passing locally and in CI?
- Are there tests for the new logic, and do they run fast and deterministically?
- Were UX changes reviewed and accompanied by screenshots or a short demo?
- Are edge cases and error states handled with clear messages?
- Was accessibility considered where applicable?

Small PR guidance
------------------
- Keep PRs focused and small (<400 lines) when possible.
- For larger changes, open a design ADR or RFC and request an initial design review before implementation.

How to file a good issue or PR
-----------------------------
- Title: concise summary
- Description: what changed, why, and how to test manually
- Include: screenshots (UI), sample commands, or a short video/gif when helpful

Code of conduct
---------------
Be respectful and collaborative. If you need mediation, contact the repository owners.

Questions
---------
Open an issue or ask on the project channel. We'll help you get unblocked.
