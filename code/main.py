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
		json_obj = json.load(fp)

	sectors = {}
	primary_energies = {}
	energy = {}



	sectors = build_model(json_obj["sectors"])

	for energy in json_obj["primaryenergies"]:
		energy_name = json_obj["primaryenergies"][energy]["name"]
		primary_energies[energy_name] = 0

	return sectors

def build_model(obj):
	sectors = {}
	for sector in obj:
		sector_name = obj[sector]["name"]
		sectors[sector_name] = Sector(sector_name)

		for input_name in obj[sector]["inputs"]:
			input = obj[sector]["inputs"][input_name]
			energy = Energy(input["name"], sectors[sector_name	], energy=input["energy"]*100/input["efficiency"])
			sectors[sector_name].add_energy(input["name"], energy)
			add_outputs(input, energy)

	return sectors

def add_outputs(obj, parent):
	sector = parent.sector
	if "inputs" in obj:
		for input_name in obj["inputs"]:
			json_input = obj["inputs"][input_name]
			input = None
			if json_input["name"] in sector.energies:
				input = sector.energies[json_input["name"]]
			else:
				input = Energy(json_input["name"], sector)
				sector.energies[json_input["name"]] = input
			input.add_output(parent.name, quota=json_input["quota"], efficiency=json_input["efficiency"])
			add_outputs(json_input, input)
if __name__ == "__main__":
	main()
