from Energy import Sector, Energy
from sys import argv, exit
from copy import copy
import json

def main():
	'''if len(argv) < 2:
		print("Usage: 'python3 %s <json-file>' json-file containing data about the system." % argv[0])
		exit(1)
	'''
	with open("system-data.json", "r") as fp:
		obj = json.load(fp)

	(primaryenergies, energies, sectors) = build_model(obj)
	return sectors
	
def build_model(obj):
	sectors = {}
	energies = {}
	primaryenergies = {}
	
	for energy_id in obj["primary_energies"]:
		energy_obj = obj["primary_energies"][energy_id]
		energy = Energy(energy_id, energy_obj["name"])
		primaryenergies[energy_id] = energy
		energies[energy_id] = energy
		
		add_inputs(obj, energy_id, energy_obj, energies)
	
	for energy_id in obj["energies"]:
		energy_obj = obj["energies"][energy_id]
		if not energy_id in energies:
			energies[energy_id] = Energy(energy_id, obj["energies"][energy_id]["name"])
		add_inputs(obj, energy_id, energy_obj, energies)
		add_sectors(obj, energy_id, energy_obj, sectors, energies)
	
	return (primaryenergies, energies, sectors)


def add_inputs(obj, id, energy_obj, energies):
	if "energies" in energy_obj:
		for energy_id in energy_obj["energies"]:
			if not energy_id in energies:
				energies[energy_id] = Energy(energy_id, obj["energies"][energy_id]["name"])
			efficiency = energy_obj["energies"][energy_id]["efficiency"]
			quota = energy_obj["energies"][energy_id]["quota"]
			energies[energy_id].add_input(id, energies[id], efficiency, quota)
			energies[id].add_subenergy(energy_id, energies[energy_id], efficiency, quota)

def add_sectors(obj, id, energy_obj, sectors, energies):
	if "sectors" in energy_obj:
		for sector_id in energy_obj["sectors"]:
			if not sector_id in sectors:
				sectors[sector_id] = Sector(sector_id, obj["sectors"][sector_id]["name"])
			efficiency = energy_obj["sectors"][sector_id]["efficiency"]
			amount = energy_obj["sectors"][sector_id]["amount"]
			sectors[sector_id].add_energy(id, energies[id])
			energies[id].add_sector(sector_id, sectors[sector_id], efficiency, amount)

if __name__ == "__main__":
	main()
