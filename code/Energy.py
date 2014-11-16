class Sector:
    def __init__(self, name):
        self.name = name
        self.energy_distribution = []

    def distribution(self, value, energy):
        self.energy_distribution.append((energy, value))


class Energy:
    def __init__(self, name):
        self.name = name
