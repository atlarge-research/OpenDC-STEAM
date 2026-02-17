# %%

from pathlib import Path
import pandas as pd 

import json

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

from processing_functions.aggregate_output import aggregateResults

# %%

folder = "/home/dante-niewenhuis/Documents/Papers/STEAM-github/output/surf"

def find_folders_with_trackr_json(root_dir):
    root = Path(root_dir)
    return [
        str(path.parent)
        for path in root.rglob("trackr.json")
    ]

# Example usage
folders = find_folders_with_trackr_json(folder)
print(folders)

# %%

def get_experiment_info(folder):

    with open(f"{folder}/trackr.json", "r") as rf:
        trackr = json.load(rf)
        
    for i, experiment_info in enumerate(trackr):
        print(experiment_info)

        workload = Path(experiment_info["workload"]["pathToFile"]).stem

        topology = experiment_info["topology"]["pathToFile"]

        NoH = topology.split("/")[2]
        battery = topology.split("/")[3]

        battery_capacity = battery.split("_")[0]
        battery_speed = battery.split("_")[1]

        carbon_trace = topology.split("/")[4].split(".")[0]

        allocationPolicy = experiment_info["allocationPolicy"]

        if allocationPolicy == "prefab":
            allocationType = "Normal"
        else:
            allocationType = "Shifting"
            
        if "failureModel" in experiment_info:
            failure_model = experiment_info["failureModel"]
            
            failures = failure_model["startPoint"]
        else:
            failures = "no"
            
        print(workload,NoH,battery,allocationType,carbon_trace,failures)
        
        results = aggregateResults(f"{folder}/raw-output/{i}/seed=0", workload, NoH, carbon_trace)
        
        print(results)

# %%

get_experiment_info(folders[0])

# for folder in folders:
#     get_experiment_info(folder)

# %%
