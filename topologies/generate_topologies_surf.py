# %%

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

topology_folder = f"{base_folder}/topologies"

from utils.variables import thresholds_dict, battery_capacities_dict, NoH_dict, region_codes

from topologies.generate_topology import generate_topology

# %%

workload = "surf"

battery_capacities = battery_capacities_dict[workload]
NoHList = NoH_dict[workload]

for NoH in NoHList:
    for region_code in region_codes:
        for battery_capacity in battery_capacities:
            generate_topology(workload, NoH, battery_capacity, region_code, thresholds_dict[region_code]["mean"])
# %%
# Generate topologies for charging speed simulations required for figure 7b

charging_speeds = [0, 10, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 3000, 6000]

for charging_speed in charging_speeds:
    for region_code in region_codes:
        generate_topology(workload, 277, 320, region_code, thresholds_dict[region_code]["mean"], charging_speed=charging_speed)
# %%
