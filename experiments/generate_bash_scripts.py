# %%

import math
import glob
import shutil

import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

bash_folder = f"{base_folder}/bash_scripts"

if not os.path.exists(bash_folder):
    os.makedirs(bash_folder)

for file in os.listdir(bash_folder):
    shutil.rmtree(f"{bash_folder}/{file}")

def generateBashStript(bash_folder, experiment_list, name, steamrunner = "STEAM"):

    bash_script_content = """#!/bin/bash"""

    for experiment in experiment_list:
        bash_script_content += f"\n\n./{steamrunner}/bin/STEAMExperimentRunner --experiment-path \"{experiment}\""

    # Specify the file path
    file_path = f"{bash_folder}/{name}.sh"

    # Write the bash script content to the file
    with open(file_path, 'w') as file:
        file.write(bash_script_content)

    # Make the bash script executable
    import os
    os.chmod(file_path, 0o755)

    print(f"Bash script created at {file_path}")


experiment_name = "surf"

experiment_folder = f"{base_folder}/experiments/{experiment_name}"
print(f"Creating bash scripts for the {experiment_name} experiment...")

num_of_nodes = 5 # The number of available nodes to run the experiments on
simulations_per_node = 10 # The number of simulations in parallel on a node

experiment_paths = [x.replace(f"{base_folder}/", "") for x in glob.glob(f"{experiment_folder}/**/*.json", recursive=True)]

num_experiments = len(experiment_paths)

print(f"This experiment has {num_experiments} simulations to run.")

experiments_per_node = math.ceil(num_experiments / num_of_nodes)

print(f"Each node will run {experiments_per_node} simulations.")

number_of_rounds = experiments_per_node / simulations_per_node

print(f"This will take {number_of_rounds} rounds of simulations on each node.")

base_num = int(num_experiments / num_of_nodes)
remaining = num_experiments - (base_num * num_of_nodes) 
experiments_per_node_list = [base_num for _ in range(num_of_nodes)]

for i in range(remaining):
    experiments_per_node_list[i] += 1

# %%

for node_idx, experiment_paths_node in enumerate(experiments_per_node_list):

    experiment_paths_node = experiment_paths[node_idx*experiments_per_node:(node_idx+1)*experiments_per_node]

    print(len(experiment_paths_node))

    bash_script_size = int(len(experiment_paths_node) / (simulations_per_node))

    splitted_experiments = []

    for i in range(simulations_per_node):
        splitted_experiments.append(experiment_paths_node[i*bash_script_size:(i+1)*bash_script_size])

    start = (simulations_per_node)*bash_script_size

    for i, index in enumerate(range(start, len(experiment_paths_node))):
        splitted_experiments[i].append(experiment_paths_node[index])

    print([len(x) for x in splitted_experiments])

    if not os.path.exists(f"{bash_folder}/{node_idx}"):
        os.makedirs(f"{bash_folder}/{node_idx}")

    for i, experiments in enumerate(splitted_experiments):
        generateBashStript(bash_folder, experiments, f"{node_idx}/{i}", steamrunner = "STEAM")
