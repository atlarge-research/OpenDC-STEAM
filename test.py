# %%

import pandas as pd

# %%

for i in range(2):
    df = pd.read_parquet(f"/home/dante-niewenhuis/Documents/Papers/STEAM-github/output/test/277/0_1000/normal/raw-output/{i}/seed=0/powerSource.parquet")

    print(df["energy_usage"].sum())
    
# %%

df_normal = pd.read_parquet("/home/dante-niewenhuis/Documents/Papers/STEAM-github/output/test/277/0_1000/normal/raw-output/0/seed=0/powerSource.parquet")
df_shifted = pd.read_parquet("/home/dante-niewenhuis/Documents/Papers/STEAM-github/output/test/277/0_1000/normal/raw-output/1/seed=0/powerSource.parquet")

# %%

print(df_normal["energy_usage"].max())
print(df_shifted["energy_usage"].max())
