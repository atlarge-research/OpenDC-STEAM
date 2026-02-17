# %%

from subprocess import Popen
import os
import argparse

parser = argparse.ArgumentParser(description='Run experiments for month 0')

parser.add_argument('--job_num', type=int, help='The job number')

args = parser.parse_args()

job_num = args.job_num

procs = []

for script in os.listdir(f"./bash_scripts/{job_num}"):
    procs.append(Popen(f"./bash_scripts/{job_num}/{script}", shell=True))
    
for p in procs:
    p.wait()

print("All processes are done")

# %%
