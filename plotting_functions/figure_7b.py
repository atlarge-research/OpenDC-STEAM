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

charging_speeds = [10, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 3000, 6000]

mins = np.array([-0.42740537, -0.38969643, -0.32087598, -0.1904874 , -0.17028299,
       -0.13942928, -0.12867514, -0.12496243, -0.12182402, -0.11984078,
       -0.11848098, -0.11756958, -0.11728248, -0.11591151, -0.1141083 ,
       -0.11225086, -0.11039187, -0.10620929, -0.10468525, -0.10356042,
       -0.10200915, -0.10046831, -0.10046831, -0.10046831])
means = np.array([-0.47186383, -0.43514312,  0.42176922,  2.59249599,  3.92666547,
        4.70529563,  5.1928207 ,  5.49699437,  5.70220214,  5.84675262,
        5.9616365 ,  6.05107197,  6.09575063,  6.13574457,  6.17316206,
        6.20659728,  6.23426105,  6.25899517,  6.2794496 ,  6.29676269,
        6.31091283,  6.3230941 ,  6.3230941 ,  6.3230941 ])
maxs = np.array([-0.1167193 , -0.10206113, -0.01739019,  3.4591862 ,  5.39712497,
        6.9048761 ,  8.416195  ,  8.7993905 ,  8.93638   ,  9.12754125,
        9.34557975,  9.4639155 ,  9.51413425,  9.5954695 ,  9.630045  ,
        9.629702  ,  9.658566  ,  9.69584525,  9.7252515 ,  9.7607915 ,
        9.8008365 ,  9.847309  ,  9.847309  ,  9.847309  ])

# %%

ratio = 3.16 / means.max()

mins = mins * ratio
means = means * ratio
maxs = maxs * ratio

# %%

performance_thresh = 95 

means = np.array(means)
distance = (means.max() - means) / means.max() * 100
performance_line = charging_speeds[np.where(distance < 100-performance_thresh)[0][0]]

# %%

plt.figure(figsize=(6, 2))

bax = brokenaxes(xlims=((0, 1.2), (2.800, 3.200), (5.800, 6.010)), wspace=.1)  

linewidth = 2.5
bax.plot(np.array(charging_speeds)/1000, maxs, label = "3rd quartile", color="goldenrod", linestyle="--", linewidth=linewidth)
bax.plot(np.array(charging_speeds)/1000, means, label= "mean", color="mediumpurple", linestyle="-", linewidth=linewidth)
bax.plot(np.array(charging_speeds)/1000, mins, label="1st quartile", color="maroon", linestyle=":", linewidth=linewidth)

bax.axvline(x=performance_line/1000, color='green', linestyle='--')
bax.axvline(x=3.000, color='gray', linestyle='--')
bax.axvline(x=6.000, color='gray', linestyle='--')

text_hoffset = 0.01
text_voffset = 0.1
fontsize = 13
tick_fontsize = 12

bax.annotate(f'{performance_thresh}%\nPerformance:\n{performance_line/1000}kW/kWh', 
             xy=(performance_line/1000+text_hoffset, text_voffset), fontsize=fontsize,
             textcoords='data', ha='left', va='bottom', color='green')

bax.annotate('Tesla Super\nCharger:\n3kW/kWh', xy=(3.000 - text_hoffset, text_voffset), 
             textcoords='data', ha='right', va='bottom', color='gray', fontsize=fontsize)

bax.annotate('Facebook\nDC charger:\n6kW/kWh', xy=(6.000 - text_hoffset, text_voffset), 
             textcoords='data', ha='right', va='bottom', color='gray', fontsize=fontsize)

bax.legend(bbox_to_anchor=(0.6, 0.99), loc='upper left', fontsize=fontsize, labelspacing=0, borderpad=0.2)

plt.ylim([None, None])

bax.set_xlabel("Charging Speed [kW/kWh]", labelpad=20, fontsize=15)
bax.set_ylabel("Carbon Reduction [%]", labelpad=22, fontsize=fontsize)
bax.set_ylabel("")

bax.axs[0].set_xticks(np.arange(0, 1.2, 0.2))
bax.axs[0].tick_params(axis='x', labelsize=tick_fontsize)
bax.axs[1].set_xticks([3])
bax.axs[1].tick_params(axis='x', labelsize=tick_fontsize)
bax.axs[2].set_xticks([6])
bax.axs[2].tick_params(axis='x', labelsize=tick_fontsize)

bax.axs[0].tick_params(axis='y', labelsize=tick_fontsize)

plt.savefig(f"{base_folder}/figures/figure_7b.pdf", dpi=300, bbox_inches='tight')
