import sys

# alias my_uv_pacakge.barber -> my_uv_pacakge.subpackages.barber
import my_uv_pacakge.subpackages.barber.barber as _barber
from my_uv_pacakge.mustache import Mustache as Mustache

sys.modules["my_uv_pacakge.barber"] = _barber
barber = _barber

__all__ = ["Mustache", "barber"]
