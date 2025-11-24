"""Compatibility shim so `import final` works for simple imports.

This loads the implementation from src/final/__init__.py and inserts it into
sys.modules as `final`.
"""
from pathlib import Path
import importlib.util
import sys

pkg_path = Path(__file__).parent / "src" / "final" / "__init__.py"
spec = importlib.util.spec_from_file_location("final", str(pkg_path))
module = importlib.util.module_from_spec(spec)
sys.modules["final"] = module
spec.loader.exec_module(module)

from types import SimpleNamespace
_ns = SimpleNamespace(**{k: getattr(module, k) for k in dir(module) if not k.startswith("__")})
for _k in dir(_ns):
    globals()[_k] = getattr(_ns, _k)
