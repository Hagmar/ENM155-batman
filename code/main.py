from Energy import Sector, Energy
from sys import argv, exit
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

    for energy in obj["primaryenergies"]:
        primaryenergies[energy] = Energy(obj["primaryenergies"][energy]["name"])

    for sector in obj["sectors"]:
        sectors[sector] = Sector(obj["sectors"][sector]["name"])

        #for energy in obj["sectors"][sector]["inputs"]:


    print(primaryenergies)
    print(sectors)

if __name__ == "__main__":
    main()
