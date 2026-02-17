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

df_base_surf = pd.read_csv(f"{base_folder}/results/surf/surf_aggregated.csv")
df_base_surf["battery_capacity"] = df_base_surf.battery.apply(lambda x: int(x.split("_")[0]))

# %% Get the correct rows

df_surf = df_base_surf[df_base_surf["NoH"] == 277]
df_surf = df_surf[df_surf["allocationType"] == "normal"]
df_surf = df_surf[df_surf["failures"] == "no"]

# %% Get the reduction numbers

def getCarbonReduction(df):
    df["battery_carbon"] = df["embodied_carbon_battery"] + df["carbon_emission"]


    carbon_reduction = []

    capacities = sorted(df["battery_capacity"].unique())

    for name, group in df.groupby("carbon_trace"):

        group = group.sort_values("battery_capacity").reset_index()
        base_carbon = group[group["battery_capacity"] == 0]["battery_carbon"].values[0]

        carbon_reduction_ = (base_carbon - group["battery_carbon"]) / base_carbon * 100


        min_carbon = group.iloc[1:]["battery_carbon"].min()

        # carbon_reduction.append([name] + carbon_reduction_.to_numpy().tolist())

        carbon_reduction.append([name, (base_carbon - min_carbon) / base_carbon * 100])

    # return pd.DataFrame(carbon_reduction, columns=["region"] + capacities)
    return pd.DataFrame(carbon_reduction, columns=["region", "total_carbon_reduction"])


default_embodied_cost = 100
def getDistribution(df, new_carbon_cost):
    df_new = df.copy()

    ratio = new_carbon_cost / default_embodied_cost

    df_new["embodied_carbon_battery"] = df_new["embodied_carbon_battery"] * ratio

    df_reduction = getCarbonReduction(df_new)

    df_bad = df_reduction[df_reduction["total_carbon_reduction"] < 0]
    df_mid = df_reduction[(df_reduction["total_carbon_reduction"] >= 0) & (df_reduction["total_carbon_reduction"] <= 5)]
    df_good = df_reduction[df_reduction["total_carbon_reduction"] > 5] 

    bad_percentage = len(df_bad) / len(df_reduction) * 100
    mid_percentage = len(df_mid) / len(df_reduction) * 100
    good_percentage = len(df_good) / len(df_reduction) * 100

    return [new_carbon_cost, bad_percentage, mid_percentage, good_percentage]

# %%

embodied_costs = range(30, 250, 5)

bad_percentages = []
med_percentages = []
good_percentages = []

for embodied_cost in embodied_costs:
    cost, bad_percentage, mid_percentage, good_percentage = getDistribution(df_surf, embodied_cost)

    bad_percentages.append(bad_percentage)
    med_percentages.append(mid_percentage) 
    good_percentages.append(good_percentage)

bad_percentages = np.array(bad_percentages)
med_percentages = np.array(med_percentages)
good_percentages = np.array(good_percentages)

# %%

plt.figure(figsize=(6,4))

fill_good = plt.fill_between(embodied_costs, bad_percentages + med_percentages, 100, hatch="-", label="High")
fill_med = plt.fill_between(embodied_costs, bad_percentages, bad_percentages + med_percentages, hatch='\\', label="Low")
fill_bad = plt.fill_between(embodied_costs, 0, bad_percentages, hatch="//", label="Negative")

fill_bad.set_facecolor("indianred")
fill_med.set_facecolor("gold")
fill_good.set_facecolor("forestgreen")


plt.plot(embodied_costs, bad_percentages, color="gray")
plt.plot(embodied_costs, bad_percentages + med_percentages, color="gray")


plt.axvline(x=100, color="black", linestyle="--")

fontsize= 16

plt.annotate("Experimental setup:\n100 kgCO2/kWh", (95, 150), ha="left", va="top", 
             fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'))


plt.legend(title="$\\bf{Effectiveness}$", title_fontsize=fontsize, framealpha=1, fontsize=fontsize)

plt.xlabel("Embodied carbon cost [kgCO2/kWh]", fontsize=fontsize)
plt.ylabel("Percentage [%]", fontsize=fontsize)

plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)

plt.tight_layout()
plt.savefig(f"{base_folder}/figures/figure_8.pdf", bbox_inches='tight')
