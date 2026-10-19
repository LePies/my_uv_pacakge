from my_uv_pacakge.mustache import Mustache as Mustache


def main() -> None:
    print("Hello from my-uv-pacakge!")

__all__ = [
    "Mustache",
    "barber"
]

def __getattr__(name):
    if name == "barber":
        from importlib import import_module

        return import_module("my_uv_pacakge.subpackages.barber")

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__ + ["barber"])
