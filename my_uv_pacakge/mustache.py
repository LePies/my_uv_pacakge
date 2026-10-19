class Mustache:
    """A class to represent a mustache"""

    def __init__(self):
        self._color = "black"
        self._allowed_colors = ["black", "brown", "blonde", "red", "white"]
        self._mustache_lengt = 10

    def get_mustache_length(self):
        if self._mustache_lengt > 10:
            print("This mustache is too long!, Get it trimmed")
        elif self._mustache_lengt < 5:
            print("This mustache is too short!")
        else:
            print("This mustache is just right!")

        return self._mustache_lengt

    def grow_mustaceh(self):
        self._mustache_lengt += 1

    def get_color(self):
        return self._color

    def color_mustache(self, color):
        if color not in self._allowed_colors:
            raise ValueError("What an absurd color for a mustache!")

        self._color = color
