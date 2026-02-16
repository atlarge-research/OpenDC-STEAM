# %%

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

from utils.variables import thresholds_dict, battery_capacities_dict, NoH_dict, region_codes

from topologies.generate_topologies import generate_topologies

# %%

workload = "borg"

capacities = battery_capacities_dict[workload]
NoHList = NoH_dict[workload]

for NoH in NoHList:
    for region_code in region_codes:
        for capacity in capacities:
            generate_topologies(workload, NoH, capacity, region_code, thresholds_dict[region_code]["mean"] )

# %%
