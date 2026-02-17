
-----

# STEAM
This repository is the home to the source code of the STEAM framework, a first-of-its-kind simulation tool supports data center designers and operators estimating the impact of sustainability techniques on data center performance and sustainability. 

STEAM is based on [OpenDC](https://opendc.org/), an data center discrete simulator.

STEAM is accepted for The 26th IEEE International Symposium on Cluster, Cloud, and Internet Computing (CCGrid) conference to be held in Sydney in 2026.

## Input files
STEAM requires four input files to function: 

- *Topology* files define the available hardware in the data center. The file also defines the power models used by the simulator to estimate power draw and energy usage. The [generate_topology](topologies/generate_topology.py) file defines a generic function to generate topology files. We use this function to generate all the topologies need for the [surf](topologies/generate_topologies_surf.py), [marconi](topologies/generate_topologies_marconi.py), and [borg](topologies/generate_topologies_borg.py) workloads. [generate_topologies.sh](topologies/generate_topologies.sh) generates all the topologies required to run the experiments used in the paper. 

- *Carbon* traces define the carbon intensity at a location during a specific time period. For the paper, we have used 158 traces between 2021 and 2024, collected from [ElectricityMaps](https://electricitymaps.com). These traces can be found in the carbon_traces folder. **Note**, carbon traces are not required. However, if no carbon trace is provided, no carbon metrics can be simulated.

- *Failure* traces define when failures occur, how long they take, and how many hosts they impact. In this work we use the [FB_Msgr_user_reported](failure_traces/FB_Msgr_user_reported.parquet) trace collected from the [Cloud Uptime Archive paper](https://arxiv.org/abs/2504.09476). **Note**, Failure traces are not required. If no failure trace is provided, no failures will occur.

- *Experiment* files define what should be simulated, and how. The [generate_experiment](experiments/generate_experiment.py) file defines a generic function to generate experiment files. We use this function to generate all experiment files need to run the [surf](experiments/generate_experiments_surf.py), [marconi](experiments/generate_experiments_marconi.py), and [borg](experiments/generate_experiments_borg.py) workloads. [generate_experiments.sh](topologies/generate_experiments.sh) generates all the topologies required to run the experiments used in the paper.    

## How to use

**Important:** before you start, you have to set the base_folder variable in the [variables](utils/variables.py) files. This ensures that all input and output files will be collected from and put in the correct locations.

The experiments executed for the STEAM paper consist of four steps: 

### *1. Generating input files* 
For the STEAM paper, a large number of experiments had to be run. We automate this process using the [generate_topology](topologies/generate_topologies.py) and [generate_topology](experiments/generate_experiment.py) functions to generate input files systematically. The [variables](utils/variables.py) files defines the ranges to use for the experiments. Running [generate_topologies](topologies/generate_topologies.sh) and [generate_experiments](experiments/generate_experiments.sh) using bash will generate all needed topologies and experiment files. 

### *2. Simulating experiments* 
The next step is to run each experiment using STEAM. An experiment can be run using STEAM in the terminal using the following command: 

``` bash
./STEAM/bin/STEAMExperimentrunner.sh --experiment-path "path_to_experiment"
```

Because STEAM is lightweight, it is possible to run multiple simulations in parallel. To orgistrate this, we used the following process: 

Using [generate_bash_scripts](experiments/generate_bash_scripts.py) we generate a folder of bash scripts based on the number of nodes available, and how many simulations we want to run in parallel on each node. The folder contains a folder of scripts for each node to execute. We run [start_slurm.py](start_slurm.py) which queues the number of nodes we need. Next, [run_experiments.py](run_experiments.py) and [run_scripts.job](run_scripts.job) execute the generated bash scripts in parralel.  

**Note:** This method will only work when using slurm. It might also be necessary to add some extra sbatch info required by the syste.

### *3. Processing output*
STEAM produces a large amount of raw data. We process the output data into aggregated metrics. The [processing_functions](processing_functions) folder contains all functions needed to process the output data into aggregated CSV files. Using [TODO], we convert all the results in a folder to aggregated csv files. We have provided the aggregated CSV files used in the paper for the [borg](aggregated/borg_aggregated.csv), [marconi](aggregated/marconi_aggregated.csv), and [surf](aggregated/surf_aggregated.csv) workloads. 

### *4. Visualization*
We use the aggregated results created in step 3 to create all the figures shown in the paper. The [plotting_functions](plotting_functions) folder, contains all the files needed to produce the figures from the paper. Using the [plot_functions.sh](plotting_functions/plot_functions.sh), you can create all figures and save them in the [figures](figures) folder.  

## Acknowledgements
STEAM has been developed in the context of the EU Horizon [Graph Massivizer](https://github.com/graph-massivizer) (g.a. 101093202).