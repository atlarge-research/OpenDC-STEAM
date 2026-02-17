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
