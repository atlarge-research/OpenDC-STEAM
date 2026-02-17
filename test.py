# %%

import pandas as pd

# %%

df_marconi = pd.read_csv("aggregated/borg_aggregated.csv")

# %%

df_marconi[df_marconi["failures"] != "no"]