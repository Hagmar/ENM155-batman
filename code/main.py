#-*- encoding: utf-8 -*-
from Energy import Sector, Energy
from sys import argv, exit
from copy import copy
import json
import argparse

def main():
	parser = argparse.ArgumentParser(description=u"Modellering av Sveriges energiförbrukning")
	parser.add_argument("-t", "--total",action="store_true", dest="total", help=u"Visa totala energiförbrukningen för Sverige")
	parser.add_argument("-s", "--sectors",action="store_true", dest="sectors", help=u"Visa alla sektorer")
	parser.add_argument("-p", "--primary-energies",action="store_true", dest="primary", help=u"Visa alla primära energier")
	parser.add_argument("-e", "--energies",action="store_true", dest="energies", help=u"Visa alla energier")
	parser.add_argument("-v", "--value", metavar=("from_id", "to_id"),dest="values", type=str,nargs='*', help=u"Visa hur mycket energi utav energitypen 'from_id' som används till energitypen eller sektorn 'to_id'. Visar även hur mycket energi man får ut i sekundärenergin eller sektorn efter alla energiomvandlingar och förluster. Anger man inte 'to_id' så tolkas detta som alla sektorer")
	parser.add_argument("-f", "--file", dest="file", default="system-data.json", help=u"Visa alla sektorer")
	args = parser.parse_args()

	try:
		with open(args.file, "r") as fp:
			obj = json.load(fp)
	except:
		print u"File does not exist or does not contain valid json data."
		exit()

	(primaryenergies, energies, sectors) = build_model(obj)
	id_to_name = {}
	for e in energies:
		id_to_name[energies[e].id] = energies[e].name
	for s in sectors:
		id_to_name[sectors[s].id] = sectors[s].name

	calculate_energies(energies, sectors)

	if args.total:
		total = 0
		print(u"Sveriges energiförbrukning: ")
		for e in primaryenergies.values():
			total += e.energy
			print(u'{:20}{:10.4f} TWh'.format(e.name, e.energy))
		print(u"\n{:20}{:10.4f} TWh".format("Total energi", total))
	elif args.sectors:
		for s in sectors.values():
			print u"{:16} id: {:15}".format(s.name, s.id)

	elif args.primary:
		print('\n'.join([p.name for p in primaryenergies.values()]))
	elif args.energies:
		for e in energies.values():
			print u"{:16} id: {:15}".format(e.name, e.id)
	elif args.values:
		# Check for invalid energies or sectors
		for value in args.values:
			if not (value in energies or value in sectors):
				print u"\"{:s}\" är inte en giltig energityp eller sektor.".format(value)
				exit()
		length = (len(args.values))
		output = ""
		if length == 1:
			source_energy = 0
			for p in primaryenergies.values():
				source_energy += p.value(args.values[0])[0]
			if args.values[0] in energies:
			# Checking value for an energy
				(used, created) = energies[args.values[0]].value()

				if source_energy != 0:
					output += u"{:0.4f} TWh från alla primärenergier används för att framställa {:s}\n".format(source_energy, id_to_name[args.values[0]])
				output += u"{:0.4f} TWh av energin från {:s} går till alla sektorer.\n".format(used, energies[args.values[0]].name)
				output += u"Med detta så får man ut {:0.3f} TWh till alla sektorer.".format(created)
			else:
			# Checking value for a sector
				used = source_energy
				created = sectors[args.values[0]].value()
				output += u"{:0.4f} TWh från alla primärenergier används för att framställa energi till {:s} sektorn\n".format(source_energy, id_to_name[args.values[0]])
				output += u"Detta förser sektorn med {:0.4f} TWh energi.".format(created)
		elif length == 2:
			(used, created) = energies[args.values[0]].value(args.values[1])
			output += u"{:0.4f} TWh av energin från {:s} går till {:s}.\n".format(used, energies[args.values[0]].name, id_to_name[args.values[1]])
			output += u"Med detta så får man ut {:0.3f} TWh till {:s}.".format(created, id_to_name[args.values[1]])
		if used == 0:
			print("Parametrarna gav inget resultat")
			exit()
		print output
	else:
		parser.print_help()
	return primaryenergies, energies, sectors
	
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
			sectors[sector_id].energy += amount
			energies[id].add_sector(sector_id, sectors[sector_id], efficiency, amount)

def calculate_energies(energies, sectors):
	for sector_id in sectors:
		sector = sectors[sector_id]
		for energy_id in sector.energies:
			energy = energies[energy_id]
			energy_sector_link = energy.sectors[sector_id]
			amount = energy_sector_link[2]/energy_sector_link[1]
			increase_energy(energy, amount, energies)

def increase_energy(energy, amount, energies):
	energy.energy += amount
	for input_id in energy.inputs:
		input = energies[input_id]
		link = energy.inputs[input.id]
		efficiency = link[1]
		amount_temp = amount * link[2] / efficiency
		increase_energy(input, amount_temp, energies)

if __name__ == "__main__":
	main()
