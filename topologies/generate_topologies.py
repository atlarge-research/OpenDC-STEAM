# %%

import json
import os
import sys

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

topology_folder = f"{base_folder}/topologies"

def generate_hosts(workload: str, NoH: int):
    if workload == "surf":
        return [
            {
                "name": "H01",
                "cpu":
                {
                    "coreCount": 16,
                    "coreSpeed": 2100
                },
                "memory": {
                    "memorySize": 100000
                },
                "powerModel": {
                    "modelType": "sqrt",
                    "power": 400.0,
                    "idlePower": 32.0,
                    "maxPower": 180.0
                },
                "count": NoH
            }
        ]
    if workload == "marconi":
        return [
            {
                "name": "H01",
                "cpu": {
                    "coreCount": 48,
                    "coreSpeed": 2100
                },
                "accel":
                {
                    "coreCount": 23040,
                    "coreSpeed": 1
                },
                "memory": {
                    "memorySize": 100000
                },
                "powerModel": {
                    "modelType": "sqrt",
                    "power": 400.0,
                    "idlePower": 150.0,
                    "maxPower": 350.0
                },
                "accelPowerModel": {
                    "modelType": "linear",
                    "power": 400.0,
                    "idlePower": 200.0,
                    "maxPower": 1000.0
                },
                "count": NoH
            }
        ]
    if workload == "borg":
        return [
            {
                "name": "H01",
                "cpu":
                {
                    "coreCount": 48,
                    "coreSpeed": 2100
                },
                "memory": {
                    "memorySize": 100000
                },
                "powerModel": {
                    "modelType": "sqrt",
                    "power": 400.0,
                    "idlePower": 200.0,
                    "maxPower": 530.0
                },
                "count": NoH
            } 
        ]

def generate_topologies(workload: str, NoH: int, battery_capacity: float, carbon_trace: str, 
                           starting_CI: float, charging_speed: int = 1000, embodied_carbon_cost: float = 100.0):
    data = {
        "clusters":
        [
            {
                "name": "C01",
                "hosts" :
                [
                    generate_hosts(workload, NoH)
                ],
                "powerSource": {
                    "carbonTracePath": f"carbon_traces/{carbon_trace}_2021-2024.parquet"
                }
            }
        ],
    }

    if starting_CI > 0:
        data["clusters"][0]["battery"] = {
                    "capacity": battery_capacity,
                    "chargingSpeed": charging_speed*battery_capacity,
                    "embodiedCarbon": embodied_carbon_cost*battery_capacity,
                    "expectedLifetime": 10,
                    "batteryPolicy": {
                        "type": "runningMeanPlus",
                        "startingThreshold": starting_CI,
                        "windowSize": 168
                    }
                }

    # If no output folder is provided, use the default one based on the parameters
    output_folder = f"{topology_folder}/{workload}/{NoH}/{battery_capacity}_{charging_speed}_{embodied_carbon_cost}"
        
    if not os.path.exists(f"{output_folder}"):
        os.makedirs(f"{output_folder}")

    with open(f'{output_folder}/{carbon_trace}.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)