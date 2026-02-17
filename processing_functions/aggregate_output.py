# %%

import pandas as pd
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

topology_folder = f"{base_folder}/topologies"

from utils.variables import region_codes

def getUniqueTasks(df_task, task_durations):
    df_task_unique = df_task.drop_duplicates(subset=["task_id"], keep="last", inplace=False).reset_index()
    
    df_task_unique["duration_simulation"] = df_task_unique.finish_time - df_task_unique.submission_time
    df_task_unique_merged = df_task_unique.merge(task_durations, left_on="task_id", right_on="id").reset_index(drop=True)
    df_task_unique_merged["delay"] = df_task_unique_merged["duration_simulation"] - df_task_unique_merged["duration"]
    df_task_unique_merged["SLA_matched"] = df_task_unique_merged["delay"] < SLA_time
    
    return df_task_unique_merged

df_trace_dict = {}
df_trace_dict["surf"] = pd.read_parquet(f"{base_folder}/workload_traces/surf/tasks.parquet")[["id", "duration"]]
df_trace_dict["marconi"] = pd.read_parquet(f"{base_folder}/workload_traces/marconi/tasks.parquet")[["id", "duration"]]
df_trace_dict["borg"] = pd.read_parquet(f"{base_folder}/workload_traces/borg/tasks.parquet")[["id", "duration"]]
    
SLA_time = 1000 * 60 * 60 * 24
def handleTasks(result_folder, workload):
    if os.path.exists(f"{result_folder}/task.parquet"):
        df_task = pd.read_parquet(f"{result_folder}/task.parquet")
        df_task["total_delay"] = df_task.scheduling_delay + df_task.checkpoint_delay + df_task.failure_delay

        scheduler_delay = df_task.total_delay.mean()
        
        SLA_matched = scheduler_delay < SLA_time
        SLA_violations = 100 - SLA_matched.mean()*100
        
        return scheduler_delay, SLA_violations
    
    else:
        return -9999, -9999


host_lifecycle = 1000 * 60 * 60 * 24 * 365 * 5

host_carbon_dict = {}

host_carbon_dict["surf"] = 1022 * 1000
host_carbon_dict["marconi"] =  3542 * 1000
host_carbon_dict["borg"] = 2250 * 1000

def handleHosts(workload, runtime, NoH):
    host_carbon = host_carbon_dict[workload]
    
    total_carbon_host = NoH * host_carbon

    host_portion =  runtime / host_lifecycle

    embodied_carbon_host = total_carbon_host * host_portion

    return embodied_carbon_host

df_carbon_traces = {}

for region_code in region_codes:
    df_carbon_traces[region_code] = pd.read_parquet(f"{base_folder}/carbon_traces/{region_code}_2021-2024.parquet")

workload_starts = {}
workload_starts["surf"] = pd.to_datetime("2024-03-01T00:00:00")
workload_starts["marconi"] = pd.to_datetime("2024-03-01T00:00:00")
workload_starts["borg"] = pd.to_datetime("2024-03-01T00:00:00")

workload_ends = {}
workload_ends["surf"] = pd.to_datetime('2024-07-02 20:57:18')
workload_ends["marconi"] = pd.to_datetime('2024-03-30 18:15:22')
workload_ends["borg"] = pd.to_datetime('2024-04-01 00:11:41')


def get_mean_CI(workload, region_code):
    df_carbon_trace = df_carbon_traces[region_code]

    workload_start = workload_starts[workload]
    workload_end = workload_ends[workload]

    filtered_trace = df_carbon_trace[(df_carbon_trace["timestamp"] >= workload_start) & (df_carbon_trace["timestamp"] <= workload_end)]
    
    return filtered_trace["carbon_intensity"].mean()

def get_remaining_charge(df):
    if (len(df) == 0):

        return 0

    return df.iloc[-1].charge

def get_remaining_carbon(df, workload, region_code):
    
    remaining_charge = get_remaining_charge(df)

    mean_CI = get_mean_CI(workload, region_code)

    return remaining_charge / 3600000 * mean_CI

# The idle power of each host
idle_power_dict = {}
idle_power_dict["surf"] = 32
idle_power_dict["marconi"] = 350
idle_power_dict["borg"] = 200 

def calculateExcessCarbon(workload, NoH, runtime, region_code):
    idle_power = int(NoH) * idle_power_dict[workload]

    max_time = pd.to_datetime(runtime, unit="ms")
    min_time = workload_ends[workload]
    
    runtime_diff = max_time - min_time

    if runtime_diff.total_seconds() < 0:
        return 0

    # idle energy in kWh
    idle_energy = (runtime_diff.total_seconds() * idle_power) / 3_600_000

    df_carbon_trace = df_carbon_traces[region_code]
    
    df_carbon_trace_rows = df_carbon_trace[(df_carbon_trace["timestamp"] >= min_time) & (df_carbon_trace["timestamp"] <= max_time)]
    
    if len(df_carbon_trace_rows) == 0:
        return 0

    CI = df_carbon_trace_rows["carbon_intensity"].mean()
    return idle_energy * CI

def aggregateResults(folder, workload, NoH, carbon_trace):
    
    df_powerSource = pd.read_parquet(f"{folder}/powerSource.parquet")
    df_battery = pd.read_parquet(f"{folder}/battery.parquet")

    energy_usage = df_powerSource.energy_usage.sum()
    operational_carbon = df_powerSource.carbon_emission.sum()

    excessCarbon = calculateExcessCarbon(workload, int(NoH), df_powerSource.timestamp_absolute.max(), carbon_trace)
    
    operational_carbon -= excessCarbon

    if (len(df_battery) > 0):
        remaining_carbon = get_remaining_carbon(df_battery, workload, carbon_trace)
        operational_carbon -= remaining_carbon

    embodied_carbon_battery = df_battery.embodied_carbon_emission.sum()
    runtime = df_powerSource.timestamp.max()

    scheduler_delay, SLA_violations = handleTasks(folder, workload)
    embodied_carbon_host = handleHosts(workload, runtime, int(NoH))

    total_carbon = operational_carbon + embodied_carbon_host + embodied_carbon_battery

    return [runtime, energy_usage, scheduler_delay, SLA_violations, operational_carbon,
              embodied_carbon_host, embodied_carbon_battery, total_carbon]
