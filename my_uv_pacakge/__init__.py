"""Core package: mustaches plus dynamically aliased subpackages."""

import sys

from my_uv_pacakge.mustache import Mustache as Mustache

__all__ = ["Mustache", "barber", "opt"]

# --- subpackage aliases (managed by dev/new_subpackage.py) ---

import my_uv_pacakge.subpackages.barber as _barber
import my_uv_pacakge.subpackages.opt as _opt

sys.modules["my_uv_pacakge.barber"] = _barber
barber = _barber
sys.modules["my_uv_pacakge.opt"] = _opt
opt = _opt

# --- end managed block ---


def main() -> None:
    """Entry point for the my-uv-pacakge console script."""
    print("Hello from my_uv_pacakge!")
