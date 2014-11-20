class Sector:
    def __init__(self, name):
        self.name = name

class Energy:
    def __init__(self, name, energy=None, quota=None, efficiency=None):
        self.name = name
        self.sectors = {}
        self.inputs = {}
        self.energy = energy
        self.quota = quota
        self.efficiency = efficiency

    def add_input(self, name, energy=None, quota=None, efficiency=None):
        self.inputs[name] = Energy(name, energy, quota, efficiency)

    def add_sector(self, name):
        self.sectors[name] = Energy(name)

    def value(self, sector=None):
        if sector:
            return self.sectors[sector].value()
        else:
            return sum([i.value() for i in self.inputs])

