# %%

import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

# %%

def getCarbonReduction(df):
    
    res = []

    positive_regions = []
    
    for name, group in df.groupby("carbon_trace"):
        
        base_carbon = group[group["battery_capacity"] == 0]["total_carbon"].values[0]

        group["carbon_reduction"] = (base_carbon - group["total_carbon"]) / base_carbon * 100

        res.append(group)
        
        max_reduction = group["carbon_reduction"].max()
        
        if max_reduction > 0:
            positive_regions.append(name)
    
    df = pd.concat(res, ignore_index=True)

    df = df[df["battery_capacity"] != 0]
    
    df = df[df["carbon_trace"].isin(positive_regions)].reset_index(drop=True)
    
    return  df

df_res = pd.read_csv(f"/home/dante-niewenhuis/Documents/Papers/STEAM-github/results/surf_charging_speed_aggregated.csv")

# %%

df_res = getCarbonReduction(df_res)

# %%

charging_speeds = list(sorted(df_res["battery_speed"].unique()))

mins = []
means = []
maxs = []

for speed in sorted(charging_speeds):
    df_speed = df_res[df_res["battery_speed"] == speed]
    means.append(df_speed["carbon_reduction"].mean())
    mins.append(df_speed["carbon_reduction"].quantile(0.25))
    maxs.append(df_speed["carbon_reduction"].quantile(0.75))


mins = np.array(mins)
means = np.array(means)
maxs = np.array(maxs)

# %%

performance_thresh = 95 

means = np.array(means)
distance = (means.max() - means) / means.max() * 100
performance_line = charging_speeds[np.where(distance < 100-performance_thresh)[0][0]]

# %%

plt.figure(figsize=(6, 4))

bax = brokenaxes(xlims=((0, 1.2), (2.800, 3.200), (5.800, 6.010)), wspace=.1)  

linewidth = 3.5
bax.plot(np.array(charging_speeds)/1000, maxs, label = "3rd quartile", color="goldenrod", linestyle="--", linewidth=linewidth)
bax.plot(np.array(charging_speeds)/1000, means, label= "mean", color="mediumpurple", linestyle="-", linewidth=linewidth)
bax.plot(np.array(charging_speeds)/1000, mins, label="1st quartile", color="maroon", linestyle=":", linewidth=linewidth)

bax.axvline(x=performance_line/1000, color='green', linestyle='--', linewidth=2)
bax.axvline(x=3.000, color='gray', linestyle='--', linewidth=2)
bax.axvline(x=6.000, color='black', linestyle='--', linewidth=2)

text_hoffset = 0.02
text_voffset = -1.5
label_fontsize = 16
axis_fontsize = 20
tick_fontsize = 15
legend_fontsize = 16

bax.annotate(f'{performance_thresh}%\nPerformance:\n{performance_line/1000}kW/kWh', 
             xy=(performance_line/1000+text_hoffset, text_voffset), fontsize=label_fontsize,
             textcoords='data', ha='left', va='bottom', color='green')

bax.annotate('Tesla Super\nCharger:\n3kW/kWh', xy=(3.000 - text_hoffset, text_voffset+3.7), 
             textcoords='data', ha='right', va='bottom', color='gray', fontsize=label_fontsize)

bax.annotate('Facebook\nDC charger:\n6kW/kWh', xy=(6.000 - text_hoffset, text_voffset), 
             textcoords='data', ha='right', va='bottom', color='black', fontsize=label_fontsize)

bax.legend(bbox_to_anchor=(0.45, 0.96), loc='upper left', fontsize=legend_fontsize, labelspacing=0, borderpad=0.2)

plt.ylim([None, None])

bax.set_xlabel("Charging Speed [kW/kWh]", labelpad=30,fontsize=axis_fontsize)
bax.set_ylabel("Carbon Reduction [%]", labelpad=30, fontsize=axis_fontsize)
# bax.set_ylabel("")

bax.axs[0].set_xticks(np.arange(0, 1.2, 0.5))
bax.axs[0].tick_params(axis='x', labelsize=tick_fontsize)
bax.axs[1].set_xticks([3])
bax.axs[1].tick_params(axis='x', labelsize=tick_fontsize)
bax.axs[2].set_xticks([6])
bax.axs[2].tick_params(axis='x', labelsize=tick_fontsize)

bax.axs[0].tick_params(axis='y', labelsize=tick_fontsize)

plt.savefig(f"{base_folder}/figures/battery_charging.pdf", dpi=300, bbox_inches='tight')

# %%
