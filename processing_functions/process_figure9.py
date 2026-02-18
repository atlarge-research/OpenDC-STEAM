# %%

import pandas as pd 
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

workload = "surf"

df_setups = pd.read_csv(f"{base_folder}/utils/{workload}_setups.csv")

df_trace = pd.read_parquet(f"{base_folder}/workload_traces/{workload}/tasks.parquet")
task_durations = df_trace[["id", "duration"]]

task_durations["id"] = task_durations["id"].astype(int)

# %%

def getPeakPower(df_powerSource):
    return df_powerSource["energy_usage"].max() / 3600 / 1000

def getUniqueTasks(df_task, df_trace):

    df_task_unique = df_task.drop_duplicates(subset=["task_id"], keep="last", inplace=False).reset_index()
    
    min_submission_time = df_task_unique["submission_time"].min()
    df_task_unique["submission_time"] = df_task_unique["submission_time"] - min_submission_time

    df_task_unique["duration_simulation"] = df_task_unique.finish_time - df_task_unique.submission_time
    df_task_unique_merged = df_task_unique.merge(df_trace, left_on="task_id", right_on="id").reset_index(drop=True)
    df_task_unique_merged
    df_task_unique_merged["delay"] = df_task_unique_merged["duration_simulation"] - df_task_unique_merged["duration"]

    return df_task_unique_merged

def getPowerStats(setup):
    name = setup["name"]
    NoH = setup["NoH"]
    battery = setup["battery"]
    allocationType = setup["allocationType"]
    failures = setup["failures"]
    
    df_powerSource = pd.read_parquet(f"{base_folder}/output/surf_detailed/{NoH}/{battery}/{allocationType}/raw-output/0/seed=0/powerSource.parquet")
    
    peak_power = getPeakPower(df_powerSource)
    total_energy = df_powerSource["energy_usage"].sum() / 3_600_000 / 1000
    
    return peak_power, total_energy

def getTaskDelays(setup):
    name = setup["name"]
    NoH = setup["NoH"]
    battery = setup["battery"]
    allocationType = setup["allocationType"]
    failures = setup["failures"]
    
    df_task = pd.read_parquet(f"{base_folder}/output/surf_detailed/{NoH}/{battery}/{allocationType}/raw-output/0/seed=0/task.parquet")
    
    # task_delay = df_task["scheduling_delay"].mean() / 1000 / 60 / 60
    
    df_unique_tasks = getUniqueTasks(df_task, task_durations)
    task_delay = df_unique_tasks["delay"].mean() / 1000 / 60 / 60  # Convert to hours
    
    return task_delay

df_powerSources = {}
df_tasks = {}

peak_powers = {}
total_energies = {}
task_delays = {}

for index, setup in df_setups.iterrows():
    name = setup["name"]
    print(f"Processing {name}...")
    
    NoH = setup["NoH"]
    battery = setup["battery"]
    allocationType = setup["allocationType"]
    failures = setup["failures"]
    
    peak_power, total_energy = getPowerStats(setup)
    
    peak_powers[name] = peak_power
    total_energies[name] = total_energy
    
    task_delays[name] = getTaskDelays(setup)
    
    
# %% Writing results to CSV files

with open(f"{base_folder}/results/{workload}_peak_powers.csv", "w") as f:
    f.write("Name,Peak Power (kW)\n")
    for name, peak_power in peak_powers.items():
        f.write(f"{name},{peak_power}\n")
        
with open(f"{base_folder}/results/{workload}_total_energies.csv", "w") as f:
    f.write("Name,Total Energy (kWh)\n")
    for name, total_energy in total_energies.items():
        f.write(f"{name},{total_energy}\n")

with open(f"{base_folder}/results/{workload}_task_delays.csv", "w") as f:
    f.write("Name,Task Delay (hours)\n")
    for name, task_delay in task_delays.items():
        f.write(f"{name},{task_delay}\n")

# %%
