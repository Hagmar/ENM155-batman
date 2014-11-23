class Sector:
	def __init__(self, id, name):
		self.name = name
		self.id = id
		self.energies = {}

	def add_energy(self, id, energy):
		self.energies[id] = energy

	def value(self):
		return sum([self.energies[e].value(self.id) for e in self.energies])

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

	def value(self, id=None):
		if id:
			(sum_used, sum_created) = self.sum_value_energy(self, id)
			return (sum_used, sum_created)
		else:
			return 0
	
	def sum_value_energy(self, energy, id):
		sum_used = 0
		sum_created = 0
		for subenergy_id in energy.subenergies:
			link = energy.subenergies[subenergy_id]
			if subenergy_id == id:
				sum_created += link[0].energy * link[2]
				sum_used += sum_created / link[1]
			else:
				(used_temp, created_temp) = self.sum_value_energy(link[0], id)
				created_temp = created_temp * link[2]
				used_temp = used_temp * link[2] / link[1]
				sum_created += created_temp
				sum_used += used_temp
				
		(sum_used, sum_created) = self.sum_value_sector(energy, id, sum_used, sum_created)
		
		return (sum_used, sum_created)
	
	def sum_value_sector(self, energy, id, sum_used, sum_created):
		for sector_id in energy.sectors:
			link = energy.sectors[sector_id]
			if sector_id == id:
				sum_created += link[2]
				sum_used += sum_created / link[1]
		return (sum_used, sum_created)