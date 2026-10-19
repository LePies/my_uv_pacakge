import importlib
import sys

from my_uv_pacakge.mustache import Mustache as Mustache

__all__ = ['Mustache', 'barber', 'opt']

# --- subpackage aliases (managed by dev/new_subpackage.py) ---

for _name, _module in {'barber': 'barber', 'opt': 'opt'}.items():
    _mod = importlib.import_module(f"my_uv_pacakge.{_module}")
    sys.modules[f"my_uv_pacakge.{_name}"] = _mod
    globals()[_name] = _mod

# --- end managed block ---
