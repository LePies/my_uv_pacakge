"""Mustache model: color, length, and growth."""

DEFAULT_COLOR = "black"
ALLOWED_COLORS = ["black", "brown", "blonde", "red", "white"]
DEFAULT_LENGTH = 10
MIN_LENGTH = 5
MAX_LENGTH = 10


class Mustache:
    """Represents a mustache with a color and a length."""

    def __init__(self) -> None:
        self._color = DEFAULT_COLOR
        self._mustache_length = DEFAULT_LENGTH

    @property
    def color(self) -> str:
        """Return the current mustache color."""
        return self._color

    @property
    def mustache_length(self) -> int:
        """Return the current mustache length."""
        return self._mustache_length

    def get_mustache_length(self) -> int:
        """Print whether the length is too long, too short, or just right.

        Returns:
            The current mustache length.
        """
        if self._mustache_length > MAX_LENGTH:
            print("This mustache is too long!, Get it trimmed")
        elif self._mustache_length < MIN_LENGTH:
            print("This mustache is too short!")
        else:
            print("This mustache is just right!")

        return self._mustache_length

    def grow_mustache(self) -> None:
        """Increase the mustache length by one."""
        self._mustache_length += 1

    def trim(self, amount: int = 5) -> int:
        """Shorten the mustache by the given amount, clamped at zero.

        Args:
            amount: How much length to remove. Defaults to 5.

        Returns:
            The new mustache length.
        """
        self._mustache_length = max(0, self._mustache_length - amount)
        return self._mustache_length

    def get_color(self) -> str:
        """Return the current mustache color."""
        return self._color

    def color_mustache(self, color: str) -> None:
        """Set the mustache color.

        Args:
            color: The new color; must be one of ALLOWED_COLORS.

        Raises:
            ValueError: If the color is not allowed.
        """
        if color not in ALLOWED_COLORS:
            raise ValueError("What an absurd color for a mustache!")

        self._color = color


__all__ = [
    "ALLOWED_COLORS",
    "DEFAULT_COLOR",
    "DEFAULT_LENGTH",
    "MAX_LENGTH",
    "MIN_LENGTH",
    "Mustache",
]
