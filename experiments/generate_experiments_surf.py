# %%

import pandas as pd
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

from utils.variables import battery_capacities_dict, NoH_dict, region_codes

from experiments.generate_experiment import generateExperiment

workload = "surf"
experiment_folder = f"{base_folder}/experiments"

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
    generateExperiment(workload, NoH, "0_1000", ["NL"], exportInterval=99999999999, printFrequency=24*6)
    generateExperiment(workload, NoH, "0_1000", ["NL"], failures=True, exportInterval=99999999999, printFrequency=24*6)

# %%
# Charging speed experiment required for figure 7a

charging_speeds = [10, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 3000, 6000]


for charging_speed in charging_speeds:
    generateExperiment(workload, 277, f"320_{charging_speed}", region_codes, 
                           exportInterval=99999999999, printFrequency=24*6, 
                           output_folder=f"{experiment_folder}/{workload}_charging_speed/", 
                           export_folder=f"output/surf_charging_speed", files_to_export=["host", "service", "powerSource", "battery"])


for region_code in region_codes:
    generateExperiment(workload, 277, f"0_1000", [region_code], 
                        exportInterval=99999999999, printFrequency=24*6, 
                        output_folder=f"{experiment_folder}/{workload}_charging_speed/", 
                        export_folder=f"output/surf_charging_speed/", files_to_export=["host", "service", "powerSource", "battery"])


# %%
# More detailed simulations required for figure 9
# These experiments have a higher export frequency required for metrics such as power draw spike

df_setups = pd.read_csv(f"{base_folder}/utils/surf_setups.csv")

for i, setup in df_setups.iterrows():    
    workload = setup["workload"]
    NoH = setup["NoH"]
    battery = setup["battery"]
    allocationType = setup["allocationType"]
    
    if allocationType == "shifting":
        shifting = True
    else:
        shifting = False
    
    generateExperiment(workload, NoH, battery, ["NL"], shifting=shifting, 
                       exportInterval=3600, printFrequency=24*6, 
                       output_folder=f"{experiment_folder}/{workload}_detailed/",
                       export_folder=f"output/surf_detailed")
    
# %%
