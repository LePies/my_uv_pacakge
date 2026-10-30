"""Implementation of the barber subpackage."""

import my_uv_pacakge as muv


class Barber:
    """Represents a barber who trims mustaches."""

    def __init__(self, name: str, age: int, salary: int) -> None:
        """Initialize the barber.

        Args:
            name: The barber's name.
            age: The barber's age.
            salary: The barber's salary.
        """
        self.name = name
        self.age = age
        self.salary = salary

    def trim_mustache(self, mustache: muv.Mustache) -> int:
        """Trim a mustache by the default amount and report the new length.

        Args:
            mustache: The mustache to trim.

        Returns:
            The mustache's new length.
        """
        new_length = mustache.trim()
        print(f"mustache length is now {new_length}")
        return new_length


__all__ = ["Barber"]
