class Sector:
	def __init__(self, name):
		self.name = name
		self.energies = {}

	def add_energy(self, name, energy):
		self.energies[name] = energy

	def value(self):
		return sum([self.energies[e].value() for e in self.energies])

class Energy:
	def __init__(self, name, energy=0, quota=1.0, efficiency=1.0):
		self.name = name
		self.sectors = {}
		self.inputs = {}
		self.energy = energy
		self.quota = quota
		self.efficiency = efficiency

	def add_input(self, name, quota, efficiency):
		new_energy = Energy(name, self.energy*quota/efficiency, quota, efficiency)
		self.inputs[name] = new_energy
		return new_energy
	
	def add_existing_input(self, energy):
		energy.energy = self.energy*energy.quota/energy.efficiency
		self.inputs[energy.name] = energy

	def add_sector(self, sector):
		#self.sectors[name] = Sector(name)
		self.sectors[name] = sector
		self.sectors[name].add_energy(self.name, self)

	def value(self, sector=None):
		if sector:
			return self.sectors[sector].value()
		else:
			return self.energy * self.efficiency

