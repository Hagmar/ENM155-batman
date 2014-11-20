class Sector:
    def __init__(self, name):
        self.name = name
        self.energies = {}

    def add_energy(self, name, energy):
        self.energies[name] = energy

    def value(self):
        return sum([self.energies[e].value() for e in self.energies])

class Energy:
    def __init__(self, name, energy=0, quota=0, efficiency=0):
        self.name = name
        self.sectors = {}
        self.inputs = {}
        self.energy = energy
        self.quota = quota
        self.efficiency = efficiency

    def add_input(self, name, energy=0, quota=0, efficiency=0):
        self.inputs[name] = Energy(name, energy, quota, efficiency)

    def add_sector(self, name):
        self.sectors[name] = Sector(name)
        self.sectors[name].add_energy(self.name, self)

    def value(self, sector=None):
        if sector:
            return self.sectors[sector].value()
        else:
            return (sum([self.inputs[i].value() for i in self.inputs]) + self.energy) * self.quota / self.efficiency

