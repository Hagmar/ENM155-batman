class Sector:
	def __init__(self, name):
		self.name = name
		self.energies = {}

	def add_energy(self, name, energy):
		self.energies[name] = energy

	def value(self):
		return sum([self.energies[e].value() for e in self.energies])

class Edge:
	def __init__(self, dest, quota=100.0, efficiency=100.0):
		self.destination = dest
		self.quota = quota
		self.efficiency = efficiency

	def __eq__(x, y):
		return x.destination == y.destination

	def __hash__(self):
		return self.destination.__hash__()

class Energy:
	def __init__(self, name, sector, energy=0):
		self.name = name
		self.sector = sector
		self.energy = energy
		self.outputs = []

	def add_output(self, name, quota, efficiency):
		if name in self.sector.energies:
			energy = self.sector.energies[name]
			edge = Edge(energy,quota,efficiency)
			if not edge in self.outputs:
				self.outputs.append(edge)
			return energy
		else:
			new_energy = Energy(name, self.sector)
			self.sector.energies[name] = new_energy
			edge = Edge(self.sector.energies[name],quota,efficiency)
			self.outputs.append(edge)
			return new_energy

	def value(self, sector=None):
		value = self.energy
		for edge in self.outputs:
			value += edge.destination.value()*edge.quota/edge.efficiency
		return value

