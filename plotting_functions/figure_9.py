# %%

import matplotlib.pyplot as plt
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

def getPeakPower(df_powerSource):
    return df_powerSource["energy_usage"].max() / 3600 / 1000

def getUniqueTasks(df_task, df_trace):

    df_task_unique = df_task.drop_duplicates(subset=["task_id"], keep="last", inplace=False).reset_index()

    df_task_unique["duration_simulation"] = df_task_unique.finish_time - df_task_unique.submission_time
    df_task_unique_merged = df_task_unique.merge(df_trace, left_on="task_id", right_on="id").reset_index(drop=True)
    df_task_unique_merged
    df_task_unique_merged["delay"] = df_task_unique_merged["duration_simulation"] - df_task_unique_merged["duration"]

    return df_task_unique_merged


workload = "surf"


# %% reading the data from CSV files

peak_powers = {}
task_delays = {}
total_energies = {}

with open(f"{base_folder}/results/{workload}/peak_powers.csv", "r") as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        name, peak_power = line.strip().split(",")
        peak_powers[name] = float(peak_power)

with open(f"{base_folder}/results/{workload}/task_delays.csv", "r") as f:
    for i, line in enumerate(f):
        if i == 0:
            continue
        name, task_delay = line.strip().split(",")
        task_delays[name] = float(task_delay)

with open(f"{base_folder}/results/{workload}/total_energies.csv", "r") as f:
    total_energies = {}
    for i, line in enumerate(f):
        if i == 0:
            continue
        name, total_energy = line.strip().split(",")
        total_energies[name] = float(total_energy)

# %%

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 3), sharex=True, gridspec_kw={"hspace": 0.1}, constrained_layout=False)

fontsize = 14

keys = ["normal", "HS", "TS", "B", "TS\n+B", "TS\n+HS", "HS\n+B", "TS+HS\n+B "]

ax1.bar(keys, peak_powers.values(), color="cornflowerblue", edgecolor="black")
ax2.bar(keys, task_delays.values(), color="cornflowerblue", edgecolor="black")
ax3.bar(keys, total_energies.values(), color="cornflowerblue", edgecolor="black")


bbox_props = dict(boxstyle="square,pad=0.4", edgecolor="black", facecolor="gainsboro")
ax1.annotate("A", xy=(0.95, 0.88), xycoords='axes fraction', ha='left', va='top', fontsize=12, fontweight='bold', bbox=bbox_props)
ax2.annotate("B", xy=(0.95, 0.88), xycoords='axes fraction', ha='left', va='top', fontsize=12, fontweight='bold', bbox=bbox_props)  
ax3.annotate("C", xy=(0.95, 0.88), xycoords='axes fraction', ha='left', va='top', fontsize=12, fontweight='bold', bbox=bbox_props)

bbox_props = dict(boxstyle="square,pad=0.4", edgecolor="black", facecolor="white")
ax1.annotate("HS: Hardware Scaling\nTS: Temporal Shifting\nB: Battery", 
             xy=(0.03, 0.88), xycoords='axes fraction', ha='left', va='top', fontsize=10, bbox=bbox_props)

if workload == "surf":
    ax3.set_ylim(45, 60)
    
if workload == "marconi":
    ax3.set_ylim(400, 500)
    
if workload == "borg":
    ax3.set_ylim(300, 550)

ax1.tick_params(axis='y', labelsize=11)  # Increase the size of the y-axis labels
ax2.tick_params(axis='y', labelsize=11)  # Increase the size of the labels
ax3.tick_params(axis='y', labelsize=11)  # Increase the size of the labels

if workload == "surf":
    ax3.set_yticks([45, 50, 55])

if workload == "marconi":
    ax3.set_yticks([400, 450, 500])
    
if workload == "borg":
    ax3.set_yticks([300, 425, 550])
    
plt.xticks(fontsize=fontsize)  # Increase the size of the labels
plt.savefig(f"{base_folder}/figures/figure_9.pdf", dpi=300, bbox_inches="tight")

# %%
