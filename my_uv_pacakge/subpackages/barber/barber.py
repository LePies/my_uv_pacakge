import my_uv_pacakge as muv


class Barber:
    def __init__(self, name, age, salary):
        self.name = name

        self.age = age
        self.salary = salary

    def trim_mustache(self, mustahce: muv.Mustache):
        mustahce._mustache_lengt -= 5
        print(f"mustache lenthg is now {mustahce.get_mustache_length()}")
