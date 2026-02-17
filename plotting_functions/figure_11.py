# %%

import pandas as pd 
import matplotlib.pyplot as plt
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

# %%

df_base_surf = pd.read_csv(f"{base_folder}/output/surf_aggregated.csv")
df_base_surf["battery_capacity"] = df_base_surf.battery.apply(lambda x: int(x.split("_")[0]))

df_base_marconi = pd.read_csv(f"{base_folder}/output/marconi_aggregated.csv")
df_base_marconi["battery_capacity"] = df_base_marconi.battery.apply(lambda x: int(x.split("_")[0]))

df_base_borg = pd.read_csv(f"{base_folder}/output/borg_aggregated.csv")
df_base_borg["battery_capacity"] = df_base_borg.battery.apply(lambda x: int(x.split("_")[0]))

# %% Get the correct rows

df_surf = df_base_surf[df_base_surf["failures"] == "no"].reset_index(drop=True)
df_surf["battery_carbon"] = df_surf["embodied_carbon_battery"] + df_surf["carbon_emission"]

df_surf_277 = df_surf[df_surf["NoH"] == 277]
df_surf_BAT = df_surf_277[df_surf_277["allocationType"] == "normal"]
df_surf_TS_BAT = df_surf_277[df_surf_277["allocationType"] == "shifting"]

df_surf_HS_BAT = df_surf[df_surf["allocationType"] == "normal"]
df_surf_HS_BAT = df_surf_HS_BAT[df_surf_HS_BAT["NoH"] >= 200]

df_surf_TS_HS_BAT = df_surf[df_surf["NoH"] >= 200]

# %%

df_marconi = df_base_marconi[df_base_marconi["NoH"] == 972]
df_marconi["battery_carbon"] = df_marconi["embodied_carbon_battery"] + df_marconi["carbon_emission"]
df_marconi = df_marconi[df_marconi["failures"] == "no"]
df_marconi_normal = df_marconi[df_marconi["allocationType"] == "normal"]
df_marconi_shifted = df_marconi[df_marconi["allocationType"] == "shifting"]

df_borg = df_base_borg[df_base_borg["NoH"] == 1534]
df_borg = df_borg[df_borg["failures"] == "no"]
df_borg["battery_carbon"] = df_borg["embodied_carbon_battery"] + df_borg["carbon_emission"]
df_borg_normal = df_borg[df_borg["allocationType"] == "normal"]

# %% Get the reduction numbers

def getCarbonReduction(df):

    carbon_reduction = []

    capacities = sorted(df["battery_capacity"].unique())

    for name, group in df.groupby("carbon_trace"):

        group = group.sort_values("battery_capacity").reset_index()
        base_carbon = group[group["battery_capacity"] == 0]["total_carbon"].values[0]

        carbon_reduction_ = (base_carbon - group["total_carbon"]) / base_carbon * 100

        min_carbon = group.iloc[1:]["total_carbon"].min()
        
        min_row = group[group["total_carbon"] == min_carbon]
        
        optimal_capacity = min_row["battery_capacity"].values[0]

        # carbon_reduction.append([name] + carbon_reduction_.to_numpy().tolist())

        carbon_reduction.append([name, (base_carbon - min_carbon) / base_carbon * 100, optimal_capacity])

    # return pd.DataFrame(carbon_reduction, columns=["region"] + capacities)
    return pd.DataFrame(carbon_reduction, columns=["region", "total_carbon_reduction", "optimal_capacity"])

df_reduction_surf_BAT = getCarbonReduction(df_surf_BAT)
df_reduction_surf_TS_BAT = getCarbonReduction(df_surf_TS_BAT)
df_reduction_surf_HS_BAT = getCarbonReduction(df_surf_HS_BAT)
df_reduction_surf_TS_HS_BAT = getCarbonReduction(df_surf_TS_HS_BAT)

# %%

optimal_capacities_BAT =df_reduction_surf_BAT[df_reduction_surf_BAT["total_carbon_reduction"] > 0.5]["optimal_capacity"]
optimal_capacities_TS_BAT = df_reduction_surf_TS_BAT[df_reduction_surf_BAT["total_carbon_reduction"] > 0.5]["optimal_capacity"]
optimal_capacities_HS_BAT = df_reduction_surf_TS_BAT[df_reduction_surf_BAT["total_carbon_reduction"] > 0.5]["optimal_capacity"]
optimal_capacities_TS_HS_BAT = df_reduction_surf_TS_HS_BAT[df_reduction_surf_BAT["total_carbon_reduction"] > 0.5]["optimal_capacity"]

# %%

plt.figure(figsize=(8, 2))

bp = plt.boxplot(
    [
        optimal_capacities_BAT,
        optimal_capacities_TS_BAT,
        optimal_capacities_HS_BAT,
        optimal_capacities_TS_HS_BAT,
    ][::-1],
    tick_labels=[
        "B",
        "B+TS",
        "B+HS",
        "B+TS+HS",
    ][::-1],
    showmeans=True,
    # showfliers=False,
    whis=3,
    meanline=False,
    boxprops=dict(color="black", facecolor="mediumseagreen"),
    medianprops=dict(color="white"),
    meanprops=dict(marker="o", markerfacecolor="white", markeredgecolor="black"),
    vert=False,
    patch_artist=True,
    widths=0.7  # Reduce the space between boxes by adjusting the width
)
    
plt.yticks(fontsize=17)
plt.xticks(fontsize=15)
plt.xlabel("Optimal capacity [kWh]", fontsize=17)
plt.tight_layout()

plt.savefig(f"{base_folder}/figures/figure_11.pdf", dpi=300)
