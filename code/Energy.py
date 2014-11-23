class Sector:
	def __init__(self, id, name):
		self.name = name
		self.id = id
		self.energies = {}

	def add_energy(self, id, energy):
		self.energies[id] = energy

	def value(self):
		return sum([e.value(self.id) for e in self.energies])

class Energy:
	def __init__(self, id, name, energy=0):
		self.name = name
		self.id = id
		self.energy = energy
		self.sectors = {}
		self.inputs = {}
		self.subenergies = {}

	def add_input(self, id, energy, efficiency, quota):
		self.inputs[id] = (energy, efficiency, quota)
	
	def add_subenergy(self, id, subenergy, efficiency, quota):
		self.subenergies[id] = (subenergy, efficiency, quota)
		
	def add_sector(self, id, sector, efficiency, amount):
		self.sectors[id] = (sector, efficiency, amount)

	'''def value(self, sector=None):
		if sector:
			return self.sectors[sector].value()
		else:
			return self.energy * self.efficiency
	'''