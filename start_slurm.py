import os

for i in os.listdir("./bash_scripts"):
    os.system(f"sbatch run_scripts.job {i}")
