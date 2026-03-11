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

df_base_surf = pd.read_csv(f"{base_folder}/results/surf_aggregated.csv")
df_base_surf["battery_capacity"] = df_base_surf.battery.apply(lambda x: int(x.split("_")[0]))

df_base_marconi = pd.read_csv(f"{base_folder}/results/marconi_aggregated.csv")
df_base_marconi["battery_capacity"] = df_base_marconi.battery.apply(lambda x: int(x.split("_")[0]))

df_base_borg = pd.read_csv(f"{base_folder}/results/borg_aggregated.csv")
df_base_borg["battery_capacity"] = df_base_borg.battery.apply(lambda x: int(x.split("_")[0]))


# %% Get the correct rows Surf

df_surf = df_base_surf[df_base_surf["failures"] == "no"].reset_index(drop=True)

df_surf_277 = df_surf[df_surf["NoH"] == 277]
df_surf_default = df_surf_277[df_surf_277["allocationType"] == "normal"]
df_surf_default = df_surf_default[df_surf_default["battery_capacity"] == 0]

df_surf_HS = df_surf[df_surf["NoH"] >= 200]
df_surf_HS = df_surf_HS[df_surf_HS["battery_capacity"] == 0]
df_surf_HS = df_surf_HS[df_surf_HS["allocationType"] == "normal"]

df_surf_BAT = df_surf_277[df_surf_277["allocationType"] == "normal"]

df_surf_TS = df_surf_277[df_surf_277["allocationType"] == "shifting"]
df_surf_TS = df_surf_TS[df_surf_TS["battery_capacity"] == 0]

df_surf_TS_BAT = df_surf_277[df_surf_277["allocationType"] == "shifting"]

df_surf_TS_HS = df_surf[df_surf["NoH"] >= 200]
df_surf_TS_HS = df_surf_TS_HS[df_surf_TS_HS["battery_capacity"] == 0]
df_surf_TS_HS = df_surf_TS_HS[df_surf_TS_HS["allocationType"] == "shifting"]


df_surf_HS_BAT = df_surf[df_surf["NoH"] >= 200]
df_surf_HS_BAT = df_surf_HS_BAT[df_surf_HS_BAT["allocationType"] == "normal"]

df_surf_TS_HS_BAT = df_surf[df_surf["NoH"] >= 200]
df_surf_TS_HS_BAT = df_surf_TS_HS_BAT[df_surf_TS_HS_BAT["allocationType"] == "shifting"]

# %% Get the correct rows Marconi

df_marconi = df_base_marconi[df_base_marconi["failures"] == "no"].reset_index(drop=True)

df_marconi_972 = df_marconi[df_marconi["NoH"] == 972]
df_marconi_default = df_marconi_972[df_marconi_972["allocationType"] == "normal"]
df_marconi_default = df_marconi_default[df_marconi_default["battery_capacity"] == 0]

df_marconi_HS = df_marconi[df_marconi["NoH"] >= 750]
df_marconi_HS = df_marconi_HS[df_marconi_HS["battery_capacity"] == 0]
df_marconi_HS = df_marconi_HS[df_marconi_HS["allocationType"] == "normal"]

df_marconi_BAT = df_marconi_972[df_marconi_972["allocationType"] == "normal"]

df_marconi_TS = df_marconi_972[df_marconi_972["allocationType"] == "shifting"]
df_marconi_TS = df_marconi_TS[df_marconi_TS["battery_capacity"] == 0]


df_marconi_TS_BAT = df_marconi_972[df_marconi_972["allocationType"] == "shifting"]


df_marconi_TS_HS = df_marconi[df_marconi["NoH"] >= 750]
df_marconi_TS_HS = df_marconi_TS_HS[df_marconi_TS_HS["battery_capacity"] == 0]
df_marconi_TS_HS = df_marconi_TS_HS[df_marconi_TS_HS["allocationType"] == "shifting"]


df_marconi_HS_BAT = df_marconi[df_marconi["NoH"] >= 750]
df_marconi_HS_BAT = df_marconi_HS_BAT[df_marconi_HS_BAT["allocationType"] == "normal"]

df_marconi_TS_HS_BAT = df_marconi[df_marconi["NoH"] >= 750]
df_marconi_TS_HS_BAT = df_marconi_TS_HS_BAT[df_marconi_TS_HS_BAT["allocationType"] == "shifting"]


# %% Get the correct rows Borg

df_borg = df_base_borg[df_base_borg["failures"] == "no"].reset_index(drop=True)

df_borg_1534 = df_borg[df_borg["NoH"] == 1534]
df_borg_default = df_borg_1534[df_borg_1534["allocationType"] == "normal"]
df_borg_default = df_borg_default[df_borg_default["battery_capacity"] == 0]

df_borg_HS = df_borg[df_borg["NoH"] >= 900]
df_borg_HS = df_borg_HS[df_borg_HS["battery_capacity"] == 0]
df_borg_HS = df_borg_HS[df_borg_HS["allocationType"] == "normal"]

df_borg_BAT = df_borg_1534[df_borg_1534["allocationType"] == "normal"]

df_borg_TS = df_borg_1534[df_borg_1534["allocationType"] == "shifting"]
df_borg_TS = df_borg_TS[df_borg_TS["battery_capacity"] == 0]


df_borg_TS_BAT = df_borg_1534[df_borg_1534["allocationType"] == "shifting"]


df_borg_TS_HS = df_borg[df_borg["NoH"] >= 900]
df_borg_TS_HS = df_borg_TS_HS[df_borg_TS_HS["battery_capacity"] == 0]
df_borg_TS_HS = df_borg_TS_HS[df_borg_TS_HS["allocationType"] == "shifting"]


df_borg_HS_BAT = df_borg[df_borg["NoH"] >= 900]
df_borg_HS_BAT = df_borg_HS_BAT[df_borg_HS_BAT["allocationType"] == "normal"]

df_borg_TS_HS_BAT = df_borg[df_borg["NoH"] >= 900]
df_borg_TS_HS_BAT = df_borg_TS_HS_BAT[df_borg_TS_HS_BAT["allocationType"] == "shifting"]

# %% Get the reduction numbers

def getCarbonReduction(df, df_default):

    carbon_reduction = []

    for name, group in df.groupby("carbon_trace"):

        # group = group.sort_values("battery_capacity").reset_index()
        base_carbon = df_default[df_default["carbon_trace"] == name]["total_carbon"].values[0]

        min_carbon = group["total_carbon"].min()
        
        min_row = group[group["total_carbon"] == min_carbon]
        
        optimal_capacity = min_row["battery_capacity"].values[0]

        carbon_reduction.append([name, (base_carbon - min_carbon) / base_carbon * 100, optimal_capacity])

    return pd.DataFrame(carbon_reduction, columns=["region", "total_carbon_reduction", "optimal_capacity"])

df_reduction_surf_TS = getCarbonReduction(df_surf_TS, df_surf_default)
df_reduction_surf_HS = getCarbonReduction(df_surf_HS, df_surf_default)
df_reduction_surf_BAT = getCarbonReduction(df_surf_BAT, df_surf_default)

df_reduction_surf_TS_HS = getCarbonReduction(df_surf_TS_HS, df_surf_default)
df_reduction_surf_TS_BAT = getCarbonReduction(df_surf_TS_BAT, df_surf_default)
df_reduction_surf_HS_BAT = getCarbonReduction(df_surf_HS_BAT, df_surf_default)
df_reduction_surf_TS_HS_BAT = getCarbonReduction(df_surf_TS_HS_BAT, df_surf_default)

df_reduction_marconi_TS = getCarbonReduction(df_marconi_TS, df_marconi_default)
df_reduction_marconi_HS = getCarbonReduction(df_marconi_HS, df_marconi_default)
df_reduction_marconi_BAT = getCarbonReduction(df_marconi_BAT, df_marconi_default)

df_reduction_marconi_TS_HS = getCarbonReduction(df_marconi_TS_HS, df_marconi_default)
df_reduction_marconi_TS_BAT = getCarbonReduction(df_marconi_TS_BAT, df_marconi_default)
df_reduction_marconi_HS_BAT = getCarbonReduction(df_marconi_HS_BAT, df_marconi_default)
df_reduction_marconi_TS_HS_BAT = getCarbonReduction(df_marconi_TS_HS_BAT, df_marconi_default)

df_reduction_borg_TS = getCarbonReduction(df_borg_TS, df_borg_default)
df_reduction_borg_HS = getCarbonReduction(df_borg_HS, df_borg_default)
df_reduction_borg_BAT = getCarbonReduction(df_borg_BAT, df_borg_default)

df_reduction_borg_TS_HS = getCarbonReduction(df_borg_TS_HS, df_borg_default)
df_reduction_borg_TS_BAT = getCarbonReduction(df_borg_TS_BAT, df_borg_default)
df_reduction_borg_HS_BAT = getCarbonReduction(df_borg_HS_BAT, df_borg_default)
df_reduction_borg_TS_HS_BAT = getCarbonReduction(df_borg_TS_HS_BAT, df_borg_default)

# %%

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex="col", sharey=True, figsize=(7, 8), gridspec_kw = {'wspace':0.1, 'hspace':0}, constrained_layout=True)
bbox_props = dict(boxstyle="square,pad=0.4", edgecolor="black", facecolor="gainsboro")

widths = 0.8
axis_fontsize = 20
tick_fontsize = 17
legend_fontsize = 16
label_fontsize = 16

bp = ax1.boxplot(
    [
        df_reduction_surf_HS["total_carbon_reduction"],
        df_reduction_surf_TS["total_carbon_reduction"],
        df_reduction_surf_BAT["total_carbon_reduction"],
        df_reduction_surf_TS_HS["total_carbon_reduction"],
        df_reduction_surf_TS_BAT["total_carbon_reduction"],
        df_reduction_surf_HS_BAT["total_carbon_reduction"],
        df_reduction_surf_TS_HS_BAT["total_carbon_reduction"],
    ][::-1],
    tick_labels=[
        "HS",
        "TS",
        "B",
        "TS+HS",
        "TS+B",
        "HS+B",
        "TS+HS+B",
    ][::-1],
    showmeans=True,
    showfliers=False,
    whis=3,
    meanline=False,
    boxprops=dict(color="black", facecolor="mediumseagreen"),
    medianprops=dict(color="white"),
    meanprops=dict(marker="o", markerfacecolor="white", markeredgecolor="black"),
    vert=False,
    patch_artist=True,
    widths=widths  # Reduce the space between boxes by adjusting the width
)

ax1.annotate("Surf", xy=(0.96, 0.9), xycoords='axes fraction', ha='right', va='top', fontsize=label_fontsize, fontweight='bold', bbox=bbox_props)

bp = ax2.boxplot(
    [
        df_reduction_marconi_HS["total_carbon_reduction"],
        df_reduction_marconi_TS["total_carbon_reduction"],
        df_reduction_marconi_BAT["total_carbon_reduction"],
        df_reduction_marconi_TS_HS["total_carbon_reduction"],
        df_reduction_marconi_TS_BAT["total_carbon_reduction"],
        df_reduction_marconi_HS_BAT["total_carbon_reduction"],
        df_reduction_marconi_TS_HS_BAT["total_carbon_reduction"],
    ][::-1],
    tick_labels=[
        "HS",
        "TS",
        "B",
        "TS+HS",
        "TS+B",
        "HS+B",
        "TS+HS+B",
    ][::-1],
    showmeans=True,
    showfliers=False,
    whis=3,
    meanline=False,
    boxprops=dict(color="black", facecolor="mediumseagreen"),
    medianprops=dict(color="white"),
    meanprops=dict(marker="o", markerfacecolor="white", markeredgecolor="black"),
    vert=False,
    patch_artist=True,
    widths=widths  # Reduce the space between boxes by adjusting the width
)

ax2.annotate("Marconi", xy=(0.96, 0.9), xycoords='axes fraction', ha='right', va='top', fontsize=label_fontsize, fontweight='bold', bbox=bbox_props)


bp = ax3.boxplot(
    [
        df_reduction_borg_HS["total_carbon_reduction"],
        df_reduction_borg_TS["total_carbon_reduction"],
        df_reduction_borg_BAT["total_carbon_reduction"],
        df_reduction_borg_TS_HS["total_carbon_reduction"],
        df_reduction_borg_TS_BAT["total_carbon_reduction"],
        df_reduction_borg_HS_BAT["total_carbon_reduction"],
        df_reduction_borg_TS_HS_BAT["total_carbon_reduction"],
    ][::-1],
    tick_labels=[
        "HS",
        "TS",
        "B",
        "TS+HS",
        "TS+B",
        "HS+B",
        "TS+HS+B",
    ][::-1],
    showmeans=True,
    showfliers=False,
    whis=3,
    meanline=False,
    boxprops=dict(color="black", facecolor="mediumseagreen"),
    medianprops=dict(color="white"),
    meanprops=dict(marker="o", markerfacecolor="white", markeredgecolor="black"),
    vert=False,
    patch_artist=True,
    widths=widths  # Reduce the space between boxes by adjusting the width
)

ax3.annotate("Borg", xy=(0.96, 0.9), xycoords='axes fraction', ha='right', va='top', fontsize=label_fontsize, fontweight='bold', bbox=bbox_props)

ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

tick_labels=[
        "HS",
        "TS",
        "B",
        "TS+HS",
        "TS+B",
        "HS+B",
        "TS+HS+B",
    ][::-1]

for ax in (ax1, ax2, ax3):
    ax.tick_params(axis='x', labelsize=tick_fontsize)
    ax.tick_params(axis='y', labelsize=tick_fontsize)
    
    lbl = ax.get_yticklabels()
    for label in lbl:
        label.set_linespacing(0.7)
    
ax3.set_xlabel("Total Carbon Reduction [%]", fontsize=axis_fontsize)

plt.savefig(f"{base_folder}/figures/combined_techniques.pdf", bbox_inches='tight', dpi=300)

# plt.savefig(f"{base_folder}/figures/combined_techniques.png", bbox_inches='tight', dpi=300)


# %%
