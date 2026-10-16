class Mustache:
    """A class to represent a mustache"""

    def __init__(self):
        self._color = "black"
        self._allowed_colors = ["black", "brown", "blonde", "red", "white"]

    def get_color(self):
        return self.color

    def color_mustache(self, color):
        if color not in self._allowed_colors:
            raise ValueError("What an absurd color for a mustache!")

        self.color = color
