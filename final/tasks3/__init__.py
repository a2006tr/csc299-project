"""Top-level package shim for tests.

This module imports the actual implementation from src/tasks3/__init__.py so that
`import tasks3` works when running tests from the project root.
"""
from pathlib import Path
import importlib.util
import sys

pkg_path = Path(__file__).parent.parent / "src" / "tasks3" / "__init__.py"
spec = importlib.util.spec_from_file_location("tasks3", str(pkg_path))
module = importlib.util.module_from_spec(spec)
sys.modules["tasks3"] = module
spec.loader.exec_module(module)

# Re-export public names
for name in dir(module):
    if not name.startswith("__"):
        globals()[name] = getattr(module, name)
