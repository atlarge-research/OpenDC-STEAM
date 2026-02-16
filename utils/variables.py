import json 

import pandas as pd

base_folder = "/home/dante-niewenhuis/Documents/Papers/STEAM-github"

utils_path = f"{base_folder}/utils"

with open(f"{utils_path}/thresholds.json", "r") as rf:
    thresholds_dict = json.load(rf)

region_codes = sorted(list(thresholds_dict.keys()))

battery_capacities_dict = {}
NoH_dict = {}

battery_capacities_dict["surf"] = sorted([0] + list(range(10, 50, 10)) + list(range(200, 400, 20)) + list(range(400, 1000, 100)))
NoH_dict["surf"] = sorted(list(range(25, 500, 25)) + [277])

battery_capacities_dict["marconi"] = sorted([0, 25] + list(range(8000, 14000, 2000)))
NoH_dict["marconi"] = sorted(list(range(200, 1000, 50)) + [972] + list(range(1000, 1600, 100)))

battery_capacities_dict["borg"] = sorted([0, 25] + list(range(8000, 14000, 2000)))
NoH_dict["borg"] = sorted(list(range(800, 1500, 100)) + [1534] + list(range(1500, 2000, 200)))

code_to_region = {}

with open(f"{utils_path}/code_to_region.csv", "r") as rf:
    for line in rf.readlines()[1:]:
        line = line.strip()

        index = line.index(",")

        code_to_region[line[:index]] = line[index+1:]

carbon_trace_stats = pd.read_csv(f"{utils_path}/carbon_traces_stats.csv")
