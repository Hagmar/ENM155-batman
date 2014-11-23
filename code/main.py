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

	sectors = {}
	energies = {}
	primaryenergies = {}
	energy = {}

	for energy in obj["primaryenergies"]:
		primaryenergies[energy] = Energy(obj["primaryenergies"][energy]["name"])

	energies = copy(primaryenergies)
	sectors = build_model(obj)
	return sectors
	#for energy in obj["sectors"][sector]["inputs"]:
	#	energies[energy].add_input()
	
	#print(energies)
	#print(sectors)

def build_model(obj):
	sectors = {}
	for sector in obj["sectors"]:
		sectors[sector] = Sector(obj["sectors"][sector]["name"])
		
		for input_name in obj["sectors"][sector]["inputs"]:
			input = obj["sectors"][sector]["inputs"][input_name]
			energy = Energy(input["name"], energy=input["energy"], efficiency=input["efficiency"])
			sectors[sector].add_energy(input["name"], energy)
			add_inputs(input, energy)
	
	return sectors

def add_inputs(obj, parent):
	if "inputs" in obj:
		for input_name in obj["inputs"]:
			input = obj["inputs"][input_name]
			new_energy = parent.add_input(input["name"], quota=input["quota"], efficiency=input["efficiency"])
			add_inputs(input, new_energy)

if __name__ == "__main__":
	main()
