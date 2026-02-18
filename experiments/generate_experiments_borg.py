# %%

import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

from utils.variables import battery_capacities_dict, NoH_dict, region_codes

from experiments.generate_experiment import generateExperiment

workload = "borg"

experiment_folder = f"{base_folder}/experiments/{workload}"

capacities = battery_capacities_dict[workload]
NoHList = NoH_dict[workload]

# %%
# Experiment files to run all combinations of NoH, batterie and shifting required for figure 6, 9, 10, and 11

battery_capacities = battery_capacities_dict[workload]
NoHList = NoH_dict[workload]

for NoH in NoHList:
    for battery_capacity in battery_capacities:
        generateExperiment(workload, NoH, f"{battery_capacity}_1000", region_codes, exportInterval=99999999999, printFrequency=24*6, files_to_export=["host", "service", "powerSource", "battery"])
        generateExperiment(workload, NoH, f"{battery_capacity}_1000", region_codes, shifting=True, exportInterval=99999999999, printFrequency=24*6, files_to_export=["host", "service", "powerSource", "battery"])

# %%
# Scaling experiments required for figure 5

for NoH in NoHList:
    generateExperiment(workload, NoH, "0_1000", ["US-NY-NYIS"], failures=True, exportInterval=99999999999, printFrequency=24*6, output_folder=f"{experiment_folder}/{workload}_scaling/", experiment_name=f"borg_scaling")
    generateExperiment(workload, NoH, "0_1000", ["US-NY-NYIS"], exportInterval=99999999999, printFrequency=24*6, output_folder=f"{experiment_folder}/{workload}_scaling/", experiment_name=f"borg_scaling")
