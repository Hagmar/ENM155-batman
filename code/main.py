from Energy import Sector, Energy
from sys import argv, exit
from copy import copy
import json

def main():
    if len(argv) < 2:
        print("Usage: 'python3 %s <json-file>' json-file containing data about the system." % argv[0])
        exit(1)

    with open(argv[1], "r") as fp:
        obj = json.load(fp)

    sectors = {}
    energies = {}
    primaryenergies = {}
    energy = {}

    for energy in obj["primaryenergies"]:
        primaryenergies[energy] = Energy(obj["primaryenergies"][energy]["name"])

    energies = copy(primaryenergies)

    for sector in obj["sectors"]:
        pass
        sectors[sector] = Sector(obj["sectors"][sector]["name"])

        for energy in obj["sectors"][sector]["inputs"]:
            energies[energy].add_input()


    print(energies)
    #print(sectors)

if __name__ == "__main__":
    main()
