"""Proxy module so `import tasks3` works during tests.

This loads the actual package implementation from src/tasks3/__init__.py
and inserts it into sys.modules as `tasks3`.
"""
from pathlib import Path
import importlib.util
import sys

pkg_path = Path(__file__).parent / "src" / "tasks3" / "__init__.py"
spec = importlib.util.spec_from_file_location("tasks3", str(pkg_path))
module = importlib.util.module_from_spec(spec)
sys.modules["tasks3"] = module
spec.loader.exec_module(module)

# Re-export symbols at module level
from types import SimpleNamespace
_ns = SimpleNamespace(**{k: getattr(module, k) for k in dir(module) if not k.startswith("__")})
for _k in dir(_ns):
    globals()[_k] = getattr(_ns, _k)
