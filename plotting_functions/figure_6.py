# %%

import pandas as pd 
import numpy as np

import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
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
df_surf["battery_carbon"] = df_surf["embodied_carbon_battery"] + df_surf["carbon_emission"]


df_marconi = df_base_marconi[df_base_marconi["NoH"] == 972]
df_marconi = df_marconi[df_marconi["allocationType"] == "normal"]
df_marconi = df_marconi[df_marconi["failures"] == "no"]
df_marconi["battery_carbon"] = df_marconi["embodied_carbon_battery"] + df_marconi["carbon_emission"]


df_borg = df_base_borg[df_base_borg["NoH"] == 1534]
df_borg = df_borg[df_borg["allocationType"] == "normal"]
df_borg = df_borg[df_borg["failures"] == "no"]
df_borg["battery_carbon"] = df_borg["embodied_carbon_battery"] + df_borg["carbon_emission"]


# %% Get the reduction numbers

def getCarbonReduction(df):

    carbon_reduction = []

    capacities = sorted(df["battery_capacity"].unique())

    for name, group in df.groupby("carbon_trace"):

        group = group.sort_values("battery_capacity").reset_index()
        base_carbon = group[group["battery_capacity"] == 0]["total_carbon"].values[0]

        carbon_reduction_ = (base_carbon - group["total_carbon"]) / base_carbon * 100


        min_carbon = group.iloc[1:]["total_carbon"].min()

        # carbon_reduction.append([name] + carbon_reduction_.to_numpy().tolist())

        carbon_reduction.append([name, (base_carbon - min_carbon) / base_carbon * 100])

    # return pd.DataFrame(carbon_reduction, columns=["region"] + capacities)
    return pd.DataFrame(carbon_reduction, columns=["region", "total_carbon_reduction"])

df_reduction_surf = getCarbonReduction(df_surf)
df_reduction_marconi = getCarbonReduction(df_marconi)
df_reduction_borg = getCarbonReduction(df_borg)

# %%

df_reduction_surf_good = df_reduction_surf[df_reduction_surf["total_carbon_reduction"] > 5]
df_reduction_surf_med = df_reduction_surf[(df_reduction_surf["total_carbon_reduction"] >= 0) & (df_reduction_surf["total_carbon_reduction"] <= 5)]
df_reduction_surf_bad = df_reduction_surf[df_reduction_surf["total_carbon_reduction"] < 0]

df_reduction_marconi_good = df_reduction_marconi[df_reduction_marconi["total_carbon_reduction"] > 5]
df_reduction_marconi_med = df_reduction_marconi[(df_reduction_marconi["total_carbon_reduction"] >= 0) & (df_reduction_marconi["total_carbon_reduction"] <= 5)]
df_reduction_marconi_bad = df_reduction_marconi[df_reduction_marconi["total_carbon_reduction"] < 0]

df_reduction_borg_good = df_reduction_borg[df_reduction_borg["total_carbon_reduction"] > 5]
df_reduction_borg_med = df_reduction_borg[(df_reduction_borg["total_carbon_reduction"] >= 0) & (df_reduction_borg["total_carbon_reduction"] <= 5)]
df_reduction_borg_bad = df_reduction_borg[df_reduction_borg["total_carbon_reduction"] < 0]

# %%

df_reduction_surf.loc[df_reduction_surf["total_carbon_reduction"] < 0, "total_carbon_reduction"] = -0.01
df_reduction_marconi.loc[df_reduction_marconi["total_carbon_reduction"] < 0, "total_carbon_reduction"] = -0.01
df_reduction_borg.loc[df_reduction_borg["total_carbon_reduction"] < 0, "total_carbon_reduction"] = -0.01

# %%

fig, axs = plt.subplots(3, 1, sharex=True, figsize=(6, 4), gridspec_kw = {'wspace':0, 'hspace':0.1})
plt.subplots_adjust(hspace=0)

label_fontsize = 17
tick_fontsize = 12

num_bins = 12

# Define common bins
common_bins = np.linspace(min(0, df_reduction_marconi.total_carbon_reduction.min(), df_reduction_borg.total_carbon_reduction.min()), 
                          max(0, df_reduction_marconi.total_carbon_reduction.max(), df_reduction_borg.total_carbon_reduction.max()), num_bins-1)


common_bins = np.array([-common_bins[1]] + list(common_bins))

common_bins[1] = 0

norm_neg = mcolors.Normalize(vmin=common_bins.min(), vmax=0)
norm_pos = mcolors.Normalize(vmin=0, vmax=common_bins.max())

# Create a custom color map from blue to green
colors = ["mediumseagreen", "mediumseagreen"]  # darkgreen to Green
n_bins = 100  # Number of bins in the color map
cmap_name = 'green'
cm_g = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

def addHist(df, ax, title):
    n, bins, patches = ax.hist(df.total_carbon_reduction, bins=common_bins, edgecolor='black', linewidth=0.5, weights=np.ones(len(df)) / len(df) * 100)
    ax.set_ylabel('Percentage [%]', fontsize=label_fontsize)
    # Add title with a small gray box behind it
    bbox_props = dict(boxstyle="square,pad=0.4", edgecolor="black", facecolor="gainsboro")
    ax.annotate(title, xy=(0.97, 0.85), xycoords='axes fraction', ha='right', va='top', fontsize=12, fontweight='bold', bbox=bbox_props)
    ax.axvline(df.total_carbon_reduction.mean(), color='black', linestyle='--')
    ax.annotate(f'Mean reduction:\n{df.total_carbon_reduction.mean():.2f}%', xy=(df.total_carbon_reduction.mean() + 1, ax.get_ylim()[1] - 2),
                ha='left', va='top', fontsize=11)
    
    for i in range(len(patches)):
        if (bins[i] < 0):
            patches[i].set_facecolor("firebrick")
            patches[i].set_hatch('//')
            
            continue

        patches[i].set_facecolor(cm_g(int(norm_pos(bins[i]) * n_bins)))

addHist(df_reduction_surf, axs[0], "Surf")
addHist(df_reduction_marconi, axs[1], "Marconi")

# Remove xticks for the top and middle plots
axs[0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
addHist(df_reduction_borg, axs[2], "Borg")

# Remove y-axis labels for the middle and bottom plots
axs[0].set_ylabel('')
axs[2].set_ylabel('')
plt.xlabel("Max total carbon reduction [%]", fontsize=label_fontsize)
plt.xticks(fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)
plt.tight_layout()
plt.savefig(f"{base_folder}/figures/figure_6.pdf", bbox_inches='tight')

# %%
