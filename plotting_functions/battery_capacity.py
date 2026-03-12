# %%

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

# %%

df_base_surf = pd.read_csv(f"{base_folder}/results/surf_aggregated.csv")
df_base_surf["battery_capacity"] = df_base_surf.battery.apply(lambda x: int(x.split("_")[0]))

df_base_marconi = pd.read_csv(f"{base_folder}/results/marconi_aggregated.csv")
df_base_marconi["battery_capacity"] = df_base_marconi.battery.apply(lambda x: int(x.split("_")[0]))

df_base_borg = pd.read_csv(f"{base_folder}/results/borg_aggregated.csv")
df_base_borg["battery_capacity"] = df_base_borg.battery.apply(lambda x: int(x.split("_")[0]))

# %% Get the correct rows

df_surf = df_base_surf[df_base_surf["NoH"] == 277]
df_surf = df_surf[df_surf["allocationType"] == "normal"]
df_surf = df_surf[df_surf["failures"] == "no"]

df_marconi = df_base_marconi[df_base_marconi["NoH"] == 972]
df_marconi = df_marconi[df_marconi["allocationType"] == "normal"]
df_marconi = df_marconi[df_marconi["failures"] == "no"]

df_borg = df_base_borg[df_base_borg["NoH"] == 1534]
df_borg = df_borg[df_borg["allocationType"] == "normal"]
df_borg = df_borg[df_borg["failures"] == "no"]

# %% Get the reduction numbers

def getCarbonReduction(df):

    res = []

    capacities = sorted(df["battery_capacity"].unique())

    for name, group in df.groupby("carbon_trace"):

        group = group.sort_values("battery_capacity").reset_index()
        default_operational_carbon = group[group["battery_capacity"] == 0]["carbon_emission"].values[0]
        default_total_carbon = group[group["battery_capacity"] == 0]["total_carbon"].values[0]

        operational_carbon_reduction = (default_operational_carbon - group["carbon_emission"]) / default_operational_carbon * 100
        embodied_carbon_increase = (group["embodied_carbon_battery"]) / default_total_carbon * 100
        total_carbon_reduction = (default_total_carbon - group["total_carbon"]) / default_total_carbon * 100


        max_reduction = total_carbon_reduction.max()

        res.append([name, max_reduction] + operational_carbon_reduction.to_numpy().tolist() + 
                   embodied_carbon_increase.to_numpy().tolist() + 
                   total_carbon_reduction.to_numpy().tolist())

        # carbon_reduction.append([name, (base_carbon - max_reduction) / base_carbon * 100])

    return pd.DataFrame(res, columns=["region", "max_reduction"] + 
                        [f"{x}_operational" for x in capacities]+
                        [f"{x}_embodied" for x in capacities]+
                        [f"{x}_battery" for x in capacities])
    # return pd.DataFrame(carbon_reduction, columns=["region", "total_carbon_reduction"])

df_reduction_surf = getCarbonReduction(df_surf)
df_reduction_marconi = getCarbonReduction(df_marconi)
df_reduction_borg = getCarbonReduction(df_borg)

# %%

operational_reductions = []
embodied_reductions = []
battery_reductions = []
capacities = sorted(df_surf["battery_capacity"].unique().tolist())

df_surf_filtered = df_reduction_surf[df_reduction_surf["max_reduction"] > 1]

for capacity in capacities:
    series_operational = df_surf_filtered[f"{capacity}_operational"]
    series_embodied = df_surf_filtered[f"{capacity}_embodied"]
    series_battery = df_surf_filtered[f"{capacity}_battery"]

    operational_reductions.append([series_operational.mean()])
    embodied_reductions.append([-series_embodied.mean()])
    battery_reductions.append([series_battery.mean()])

# %%

fig, ax = plt.subplots(figsize=(6, 4))

tick_fontsize = 15
legend_fontsize = 16
label_fontsize = 16
axis_fontsize = 16

linewidth = 3
ax.plot(capacities, operational_reductions, label="Operational Carbon", color="goldenrod", linestyle="--", linewidth=linewidth)
ax.plot(capacities, embodied_reductions, label="Embodied Carbon", color="maroon", linestyle=":", linewidth=linewidth)
ax.plot(capacities, battery_reductions, label="Total Carbon", color="mediumpurple", linewidth=linewidth)

best_capacity = capacities[np.argmax(battery_reductions)]
plt.axvline(x=best_capacity, color="green", linestyle="--")
plt.annotate(f"Best Capacity: {best_capacity}", (best_capacity+10, -2.5), ha='left', va="bottom", 
             fontsize=label_fontsize, color="green")

plt.legend(loc="upper right", fontsize=legend_fontsize, 
           labelspacing=0, borderpad=0.2,bbox_to_anchor=(1, 0.85))
plt.xlabel("Battery Capacity [kWh]", fontsize=axis_fontsize)
plt.ylabel("Carbon Reduction [%]", fontsize=axis_fontsize)
# plt.ylabel("")

# ax.yaxis.set_label_coords(-0.08, 0.35)


plt.xticks(fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)

plt.savefig(f"{base_folder}/figures/battery_capacity.pdf", dpi=300, bbox_inches='tight')

# %%
