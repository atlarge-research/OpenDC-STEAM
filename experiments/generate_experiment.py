# %%

import json
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

experiment_folder = f"{base_folder}/experiments"
bash_folder = f"{base_folder}/bash_scripts"

def getAllocationPolicy(shifting):
    if shifting:
        return {
            "type": "timeshift",
            "filters": [
                {
                    "type": "Compute"
                },
                {
                    "type": "VCpu",
                    "allocationRatio": 1.0
                },
                {
                    "type": "Ram",
                    "allocationRatio": 1.5
                }
            ],
            "weighers": [
                {
                    "type": "Ram",
                    "multiplier": 1.0
                }
            ],
            "forecast": True,
            "taskStopper": {
                "forecastThreshold": 0.4
            }
        }
    else:
        return {
            "type": "prefab",
            "policyName": "TaskNumMemorizing"
        }
        
def generateExportModel(files_to_export, exportInterval = 3600 * 24 * 365, printFrequency = 1):
    return {
        "exportInterval": exportInterval,
        "printFrequency": printFrequency,
        "filesToExport": files_to_export,
        "computeExportConfig": {
            "hostExportColumns": ["power_draw", "energy_usage", "cpu_usage", "cpu_utilization", "embodied_carbon"],
            "serviceExportColumns": ["tasks_total", "tasks_pending", "tasks_active", "tasks_completed", "tasks_terminated", "hosts_up"],
            "taskExportColumns": [
                    "submission_time",
                    "schedule_time",
                    "finish_time",
                    "task_state",
                    "scheduling_delay",
                    "checkpoint_delay",
                    "failure_delay"
                ],
            "powerSourceExportColumns": [
                "power_draw",
                "energy_usage",
                "carbon_intensity",
                "carbon_emission"
            ],
            "batteryExportColumns": [
                "power_draw",
                "energy_usage",
                "embodied_carbon_emission",
                "charge"
            ]
        }
    }
        
def generateExperiment(workload: str, NoH: int, battery: str, carbon_regions: str, shifting: bool=False, failures:bool = False, 
                       files_to_export: list[str] = ["service", "powerSource", "battery", "host", "task"], 
                       output_folder: str=None, output_addition: str="", exportInterval: int = 3600 * 24 * 365, 
                       printFrequency: int = 1, embodied_carbon_cost: float=100, startPoint: float=None, experiment_name: str=None):
    
    if shifting:
        name = f"{NoH}/{battery}/shifting{output_addition}"
    else:
        name = f"{NoH}/{battery}/normal{output_addition}"
    
    if experiment_name is not None:
        name = experiment_name
    
    data = {
        "outputFolder": f"output/{experiment_name}",
        "name": f"{workload}/{NoH}/{battery}",
        "topologies": [{"pathToFile": f"topologies/{workload}/{NoH}/{battery}_{embodied_carbon_cost}/{region_code}.json"} for region_code in carbon_regions],
        "workloads": [{
            "pathToFile": f"workload_traces/{workload}",
            "type": "ComputeWorkload",
            "submissionTime": "2024-03-01T00:00:00"
        }],
        "allocationPolicies": [
            getAllocationPolicy(shifting=shifting)
        ],
        "exportModels": [
            generateExportModel(files_to_export, exportInterval, printFrequency)
        ]
    }
    
    if failures:    
        data["maxNumFailures"] = [1000]

        if startPoint is None:
            data["failureModels"] = [{ 
                "type": "trace-based", 
                "pathToFile": f"failure_traces/FB_Msgr_user_reported.parquet",
                "startPoint": i / 10
            } for i in range(10)]
            data["name"] = f"{NoH}/{battery}/failure{output_addition}"
        else:
            data["failureModels"] = [{ 
                "type": "trace-based", 
                "pathToFile": f"failure_traces/FB_Msgr_user_reported.parquet",
                "startPoint": startPoint / 10
            }]
            data["name"] = f"{NoH}/{battery}/failure{startPoint}{output_addition}"

        data["checkpointModels"] = [
            {
                "checkpointInterval": 36000000,
                "checkpointDuration": 60000,
                "checkpointIntervalScaling": 1.0
            }
        ]
    
    if output_folder is None:
        output_folder = f"{experiment_folder}/"
    
    output_folder = f"{output_folder}{workload}/{NoH}/{battery}_{embodied_carbon_cost}"
    
    if not os.path.exists(f"{output_folder}"):
        os.makedirs(f"{output_folder}")

    if failures:
        if startPoint is None:
            with open(f"{output_folder}/failure{output_addition}.json", 'w') as f:
                json.dump(data, f, indent=4)
        else:
            with open(f"{output_folder}/failure{startPoint}{output_addition}.json", 'w') as f:
                json.dump(data, f, indent=4)
        return

    if shifting:
        with open(f"{output_folder}/shifting{output_addition}.json", 'w') as f:
            json.dump(data, f, indent=4)
    else:
        with open(f"{output_folder}/normal{output_addition}.json", 'w') as f:
            json.dump(data, f, indent=4)