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

def get_experiment_info(folder):
    
    result_list = []

    with open(f"{folder}/trackr.json", "r") as rf:
        trackr = json.load(rf)
        
    for i, experiment_info in enumerate(trackr):
        workload = Path(experiment_info["workload"]["pathToFile"]).stem

        topology = experiment_info["topology"]["pathToFile"]

        NoH = topology.split("/")[2]
        battery = topology.split("/")[3]

        battery_capacity = battery.split("_")[0]
        battery_speed = battery.split("_")[1]
        battery_embodied_rate = battery.split("_")[2]
        
        battery = f"{battery_capacity}_{battery_speed}"

        carbon_trace = topology.split("/")[4].split(".")[0]

        allocationPolicy = experiment_info["allocationPolicy"]

        if allocationPolicy["type"] == "prefab":
            allocationType = "normal"
        else:
            allocationType = "shifting"
            
        if "failureModel" in experiment_info:
            failure_model = experiment_info["failureModel"]
            
            if "startPoint" in failure_model:
                failures = failure_model["startPoint"]
            else:
                failures = 0.0
        else:
            failures = "no"
            
        results = aggregateResults(f"{folder}/raw-output/{i}/seed=0", workload, NoH, carbon_trace)
        
        result_list.append([workload,NoH,battery,battery_capacity,battery_speed,battery_embodied_rate,allocationType,carbon_trace,failures,results["runtime"],results["energy_usage"],results["scheduler_delay"],results["SLA_violations"],results["carbon_emission"],results["embodied_carbon_host"],results["embodied_carbon_battery"],results["total_carbon"]])

    return result_list

# %%

def find_folders_with_trackr_json(root_dir):
    root = Path(root_dir)
    return [
        str(path.parent)
        for path in root.rglob("trackr.json")
    ]

def process_experiment_output(experiment_name):
    print(f"Processing output for experiment: {experiment_name}")

    folder = f"{base_folder}/output/{experiment_name}"
    
    folders = find_folders_with_trackr_json(folder)
    print(f"Found {len(folders)} simulations to process.")

    results = []

    for i, folder in enumerate(folders):
        print(f"Processing folder {i+1}/{len(folders)}: {folder}")

        results += get_experiment_info(folder)

    df = pd.DataFrame(results, columns=["workload", "NoH", "battery", "battery_capacity", "battery_speed", "battery_embodied_rate", "allocationType", "carbon_trace", 
                                        "failures", "runtime", "energy_usage", "scheduler_delay", 
                                        "SLA_violations", "carbon_emission", "embodied_carbon_host", 
                                        "embodied_carbon_battery", "total_carbon"],
                    )

    dtypes = {"workload": str, "NoH": int, "battery": str, "battery_capacity": int, "battery_speed": int, 
            "battery_embodied_rate": float, "allocationType": "category", "carbon_trace": "category", "failures": "category", "runtime": float, 
            "energy_usage": float, "scheduler_delay": float, "SLA_violations": float, "carbon_emission": float, 
            "embodied_carbon_host": float, "embodied_carbon_battery": float, "total_carbon": float}

    df = df.astype(dtypes)

    df.to_csv(f"{base_folder}/results/{experiment_name}_aggregated.csv", index=False)
