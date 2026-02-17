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

def getResult(df_base, workload, NoH, allocationType, carbon_trace, battery):
    df = df_base[df_base["workload"] == workload]
    df = df[df["NoH"] == NoH]
    df = df[df["allocationType"] == allocationType]
    df = df[df["carbon_trace"] == carbon_trace]
    df = df[df["battery"] == battery]
    return df.reset_index()

def getDefaultSurf(df_base):
    return getResult(df_base, "surf", 277, "normal", "NL", "0_1000")

def getDefaultMarconi(df_base):
    return getResult(df_base, "marconi", 972, "normal", "IT", "0_1000")

# %% Get results SURF

df_base_surf = pd.read_csv(f"{base_folder}/results/surf/surf_aggregated.csv")
df_base_surf["total_carbon"] = df_base_surf["carbon_emission"] + df_base_surf["embodied_carbon_host"] + df_base_surf["embodied_carbon_battery"]

df_surf = df_base_surf[df_base_surf["carbon_trace"] == "NL"]
df_surf = df_surf[df_surf["battery"] == "0_1000"]
df_surf = df_surf[df_surf["allocationType"] == "normal"]
df_surf = df_surf[df_surf["SLA_violations"] > -9999]

df_surf_normal = df_surf[df_surf["failures"] == "no"].sort_values(by=["NoH"]).reset_index()
df_surf_failures = df_surf[df_surf["failures"] != "no"].sort_values(by=["NoH"]).reset_index()

df_surf_failures_mean = df_surf_failures.groupby("NoH")[["carbon_emission", "embodied_carbon_host", "total_carbon", "SLA_violations"]].mean().reset_index()

# %% Get results marconi

df_base_marconi = pd.read_csv(f"{base_folder}/results/marconi/marconi_aggregated.csv")
df_base_marconi["total_carbon"] = df_base_marconi["carbon_emission"] + df_base_marconi["embodied_carbon_host"] + df_base_marconi["embodied_carbon_battery"]

df_marconi = df_base_marconi[df_base_marconi["carbon_trace"] == "IT"]
df_marconi = df_marconi[df_marconi["battery"] == "0_1000"]
df_marconi = df_marconi[df_marconi["allocationType"] == "normal"]

df_marconi = df_marconi[df_marconi["SLA_violations"] > -9999]

df_marconi_normal = df_marconi[df_marconi["failures"] == "no"].sort_values(by=["NoH"]).reset_index()
df_marconi_failures = df_marconi[df_marconi["failures"] != "no"].sort_values(by=["NoH"]).reset_index()

df_marconi_failures_mean = df_marconi_failures.groupby("NoH")[["carbon_emission", "embodied_carbon_host", "total_carbon", "SLA_violations"]].mean().reset_index()

# %% Get results marconi

df_base_borg = pd.read_csv(f"{base_folder}/results/borg/borg_aggregated.csv")
df_base_borg["total_carbon"] = df_base_borg["carbon_emission"] + df_base_borg["embodied_carbon_host"] + df_base_borg["embodied_carbon_battery"]

df_borg = df_base_borg[df_base_borg["carbon_trace"] == "US-NY-NYIS"]
df_borg = df_borg[df_borg["battery"] == "0_1000"]
df_borg = df_borg[df_borg["allocationType"] == "normal"]

df_borg_normal = df_borg[df_borg["failures"] == "no"].sort_values(by=["NoH"]).reset_index()
df_borg_failures = df_borg[df_borg["failures"] != "no"].sort_values(by=["NoH"]).reset_index()

df_borg_failures_mean = df_borg_failures.groupby("NoH")[["carbon_emission", "embodied_carbon_host", "total_carbon", "SLA_violations"]].mean().reset_index()

# %%

surf_upper = 350
surf_lower = 25
df_surf_normal = df_surf_normal[(df_surf_normal["NoH"] >= surf_lower) & (df_surf_normal["NoH"] <= surf_upper)]
df_surf_failures_mean = df_surf_failures_mean[(df_surf_failures_mean["NoH"] >= surf_lower) & (df_surf_failures_mean["NoH"] <= surf_upper)]

marconi_upper = 1250
marconi_lower = 0
df_marconi_normal = df_marconi_normal[(df_marconi_normal["NoH"] >= marconi_lower) & (df_marconi_normal["NoH"] <= marconi_upper)]
df_marconi_failures_mean = df_marconi_failures_mean[(df_marconi_failures_mean["NoH"] >= marconi_lower) & (df_marconi_failures_mean["NoH"] <= marconi_upper)]

borg_upper = 2000
borg_lower = 0
df_borg_normal = df_borg_normal[(df_borg_normal["NoH"] >= borg_lower) & (df_borg_normal["NoH"] <= borg_upper)]
df_borg_failures_mean = df_borg_failures_mean[(df_borg_failures_mean["NoH"] >= borg_lower) & (df_borg_failures_mean["NoH"] <= borg_upper)]

# %%

default_carbon_surf = df_surf_normal[df_surf_normal["NoH"] == 277]["total_carbon"].min()
reduced_carbon_surf = df_surf_normal[df_surf_normal["NoH"] == 200]["total_carbon"].min()

default_carbon_marconi = df_marconi_normal[df_marconi_normal["NoH"] == 972]["total_carbon"].min()
reduced_carbon_marconi = df_marconi_normal[df_marconi_normal["NoH"] == 800]["total_carbon"].min()

default_carbon_borg = df_borg_normal[df_borg_normal["NoH"] == 1534]["total_carbon"].min()
reduced_carbon_borg = df_borg_normal[df_borg_normal["NoH"] == 900]["total_carbon"].min()

# %%

df_borg_normal_1700 = df_borg_normal[df_borg_normal["NoH"] == 1700]
df_borg_normal_1900 = df_borg_normal[df_borg_normal["NoH"] == 1900]

SLA_violations_1800 = (df_borg_normal_1700["SLA_violations"].min() + df_borg_normal_1900["SLA_violations"].min()) / 2
total_carbon_1800 = (df_borg_normal_1700["total_carbon"].min() + df_borg_normal_1900["total_carbon"].min()) / 2
carbon_emission_1800 = (df_borg_normal_1700["carbon_emission"].min() + df_borg_normal_1900["carbon_emission"].min()) / 2
embodied_carbon_host_1800 = (df_borg_normal_1700["embodied_carbon_host"].min() + df_borg_normal_1900["embodied_carbon_host"].min()) / 2
energy_usage_1800 = (df_borg_normal_1700["energy_usage"].min() + df_borg_normal_1900["energy_usage"].min()) / 2
embodied_carbon_battery_1800 = (df_borg_normal_1700["embodied_carbon_battery"].min() + df_borg_normal_1900["embodied_carbon_battery"].min()) / 2

new_row = {
    "NoH": 1800,
    "SLA_violations": SLA_violations_1800,
    "total_carbon": total_carbon_1800,
    "carbon_emission": carbon_emission_1800,
    "embodied_carbon_host": embodied_carbon_host_1800,
    "energy_usage": energy_usage_1800,
    "embodied_carbon_battery": embodied_carbon_battery_1800
}

df_borg_normal = pd.concat([df_borg_normal, pd.DataFrame([new_row])], ignore_index=True)


# %%

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(18, 4), sharex="col", gridspec_kw = {'wspace':0.15, 'hspace':0.1})

fontsize = 15

def plotResults(ax, label, results, default, NoH_90 = None, NoH_99 = None, show_legend = False, hide_ticks = True):

    ax.plot(results["NoH"], results["carbon_emission"] / 1_000_000, label="Operational Carbon", linestyle="--")
    ax.plot(results["NoH"], results["embodied_carbon_host"] / 1_000_000, label="Embodied Carbon", linestyle="dotted")
    ax.plot(results["NoH"], results["total_carbon"] / 1_000_000, label="Total Carbon", color="forestgreen")
    ax.set_ylim([-2,None])

    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    ax.tick_params(axis='both', which='minor', labelsize=fontsize - 2)

    # Create a second y-axis for SLA violationss
    axb = ax.twinx()
    axb.plot(results["NoH"], results["SLA_violations"], label="SLA Violations", color="firebrick")
    axb.set_ylim([-3, 103])
    axb.tick_params(axis='y', colors='firebrick')
    axb.spines['right'].set_color('firebrick')
    
    axb.tick_params(axis='both', which='major', labelsize=fontsize, colors='firebrick')
    
    if hide_ticks:
        axb.set_yticks([])

    bbox_props = dict(boxstyle="square,pad=0.4", edgecolor="black", facecolor="gainsboro")
    ax.text(0.05, 0.1, label, transform=ax.transAxes, fontsize=fontsize, verticalalignment='bottom', bbox=bbox_props)

    lines_1, labels_1 = ax.get_legend_handles_labels()
    lines_2, labels_2 = axb.get_legend_handles_labels()

    if show_legend:
        ax.legend(lines_1 + lines_2, labels_1 + labels_2, fontsize=12, loc="lower right", labelspacing=0, borderpad=0.2)

NoH_99_surf_normal = df_surf_normal[df_surf_normal["SLA_violations"] <= 1]["NoH"].min()
NoH_90_surf_normal = df_surf_normal[df_surf_normal["SLA_violations"] <= 10]["NoH"].min()
NoH_99_surf_failures = df_surf_failures_mean[df_surf_failures_mean["SLA_violations"] <= 1]["NoH"].min()
NoH_90_surf_failures = df_surf_failures_mean[df_surf_failures_mean["SLA_violations"] <= 10]["NoH"].min()

plotResults(ax1, "A", df_surf_normal, 277, NoH_90_surf_normal, NoH_99_surf_normal)
plotResults(ax4, "D", df_surf_failures_mean, 277, NoH_90_surf_failures, NoH_99_surf_failures)

NoH_99_marconi_normal = df_marconi_normal[df_marconi_normal["SLA_violations"] <= 1]["NoH"].min()
NoH_90_marconi_normal = df_marconi_normal[df_marconi_normal["SLA_violations"] <= 10]["NoH"].min()
NoH_99_marconi_failures = df_marconi_failures_mean[df_marconi_failures_mean["SLA_violations"] <= 1]["NoH"].min()
NoH_90_marconi_failures = df_marconi_failures_mean[df_marconi_failures_mean["SLA_violations"] <= 10]["NoH"].min()

plotResults(ax2, "B", df_marconi_normal, 972, NoH_90_marconi_normal, NoH_99_marconi_normal)
plotResults(ax5, "E", df_marconi_failures_mean, 972, NoH_90_marconi_failures, NoH_99_marconi_failures)

NoH_99_borg_normal = df_borg_normal[df_borg_normal["SLA_violations"] <= 1]["NoH"].min()
NoH_90_borg_normal = df_borg_normal[df_borg_normal["SLA_violations"] <= 10]["NoH"].min()

NoH_90_borg_failures = df_borg_failures_mean[df_borg_failures_mean["SLA_violations"] <= 10]["NoH"].min()

df_borg_normal_filtered = df_borg_normal[df_borg_normal["NoH"] < 1900]

plotResults(ax3, "C", df_borg_normal_filtered, 1534, NoH_99_borg_normal, NoH_90_borg_normal, show_legend=True, hide_ticks=False)
plotResults(ax6, "F", df_borg_failures_mean, 1534, NoH_90_borg_failures, hide_ticks=False)

########################### Plot 90 and 99

# SURF

NoH_99_surf_normal = df_surf_normal[df_surf_normal["SLA_violations"] <= 1]["NoH"].min()
NoH_90_surf_normal = df_surf_normal[df_surf_normal["SLA_violations"] <= 10]["NoH"].min()

ax1.axvline(NoH_99_surf_normal, color="firebrick", linestyle="--")
ax1.text(NoH_99_surf_normal - 5, ax1.get_ylim()[1] * 0.95, f"1%", color="firebrick", fontsize=fontsize, ha='right', va="top")

ax1.set_xticks([25, 100, 200, 300])

default = 277
ax1.axvline(default, color="dimgray", linestyle="--")
ax1.text(default - 5, ax1.get_ylim()[1] * 0.95, f"Original\n{default}", color="dimgray", fontsize=fontsize, ha='right', va="top")
   
NoH_99_surf_failures = df_surf_failures_mean[df_surf_failures_mean["SLA_violations"] <= 1]["NoH"].min()
NoH_90_surf_failures = df_surf_failures_mean[df_surf_failures_mean["SLA_violations"] <= 10]["NoH"].min()

ax4.axvline(NoH_99_surf_failures, color="firebrick", linestyle="--")
ax4.text(NoH_99_surf_failures - 5, ax4.get_ylim()[1] * 0.95, f"1%", color="firebrick", fontsize=fontsize, ha='right', va="top")

ax4.axvline(default, color="dimgray", linestyle="--")
ax4.text(default - 5, ax4.get_ylim()[1] * 0.95, f"Original\n{default}", color="dimgray", fontsize=fontsize, ha='right', va="top")
  

# MARCONI

NoH_99_marconi_normal = df_marconi_normal[df_marconi_normal["SLA_violations"] <= 1]["NoH"].min()
NoH_90_marconi_normal = df_marconi_normal[df_marconi_normal["SLA_violations"] <= 10]["NoH"].min()

ax2.axvline(NoH_99_marconi_normal, color="firebrick", linestyle="--")
ax2.text(NoH_99_marconi_normal - 5, ax2.get_ylim()[1] * 0.95, f"1%", color="firebrick", fontsize=fontsize, ha='right', va="top")

default = 972
ax2.axvline(default, color="dimgray", linestyle="--")
ax2.text(default + 5, ax2.get_ylim()[1] * 0.95, f"Original\n{default}", color="dimgray", fontsize=fontsize, ha='left', va="top")

NoH_99_marconi_failures = df_marconi_failures_mean[df_marconi_failures_mean["SLA_violations"] <= 1]["NoH"].min()
NoH_90_marconi_failures = df_marconi_failures_mean[df_marconi_failures_mean["SLA_violations"] <= 10]["NoH"].min()

ax5.axvline(NoH_99_marconi_failures, color="firebrick", linestyle="--")
ax5.text(NoH_99_marconi_failures - 5, ax5.get_ylim()[1] * 0.95, f"1%", color="firebrick", fontsize=fontsize, ha='right', va="top")

ax5.axvline(default, color="dimgray", linestyle="--")
ax5.text(default + 5, ax5.get_ylim()[1] * 0.95, f"Original\n{default}", color="dimgray", fontsize=fontsize, ha='left', va="top")

# BORG

NoH_99_borg_normal = df_borg_normal[df_borg_normal["SLA_violations"] <= 1]["NoH"].min()
NoH_90_borg_normal = df_borg_normal[df_borg_normal["SLA_violations"] <= 10]["NoH"].min()

ax3.axvline(NoH_99_borg_normal, color="firebrick", linestyle="--")
ax3.text(NoH_99_borg_normal + 5, ax3.get_ylim()[1] * 0.95, f"1%", color="firebrick", fontsize=fontsize, ha='left', va="top")

default = 1534
ax3.axvline(default, color="dimgray", linestyle="--")
ax3.text(default - 5, ax3.get_ylim()[1] * 0.95, f"Original\n{default}", color="dimgray", fontsize=fontsize, ha='right', va="top")

NoH_99_borg_failures = df_borg_failures_mean[df_borg_failures_mean["SLA_violations"] <= 1]["NoH"].min()
NoH_90_borg_failures = df_borg_failures_mean[df_borg_failures_mean["SLA_violations"] <= 10]["NoH"].min()

ax6.axvline(default, color="dimgray", linestyle="--")
ax6.text(default - 5, ax6.get_ylim()[1] * 0.95, f"Original\n{default}", color="dimgray", fontsize=fontsize, ha='right', va="top")

ax1.set_title("Surf", fontsize=fontsize, fontweight="bold")
ax2.set_title("Marconi", fontsize=fontsize, fontweight="bold")
ax3.set_title("Borg", fontsize=fontsize, fontweight="bold")

ax5.set_xlabel("Number of Hosts", fontsize=fontsize)

fig.text(0.09, 0.5, "Carbon Emission [MgCO2eq]", va='center', rotation='vertical', fontsize=fontsize)
fig.text(0.93, 0.5, "SLA violations [%]", va='center', rotation='vertical', fontsize=fontsize)

plt.tight_layout()

plt.savefig(f"{base_folder}/figures/figure_5.pdf", bbox_inches='tight', pad_inches=0)

# %%
