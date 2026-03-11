# %%

from pathlib import Path
import pandas as pd 

import json

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.variables import base_folder
sys.path.append(base_folder)

from processing_functions.process_output import process_experiment_output

# %%

experiment_name = "surf"

process_experiment_output(experiment_name)
