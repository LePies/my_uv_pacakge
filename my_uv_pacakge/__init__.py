from subpackages.barber import barber

from my_uv_pacakge.mustache import Mustache as Mustache


def main() -> None:
    print("Hello from my-uv-pacakge!")

__all__ = [
    "Mustache",
    "barber"
]
