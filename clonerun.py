import sys
import shutil
import os
import pandas as pd
import argparse
import json
import copy

from utils import load_format_config
from utils import dotdict

parser = argparse.ArgumentParser()
parser.add_argument("source_config", type=str,
                    help="name of config file of source run")
parser.add_argument("target_folder", type=str,
                    help="name of target run folder")
parser.add_argument("-q", "--query", required=False, help="")
args = parser.parse_args()

# load without variable substitution
with open(args.source_config) as f:
    source_config = json.load(f)

target_folder = args.target_folder
query = args.query

if os.path.exists(target_folder):
    sys.exit("a file with this name already exists, please choose another name")

os.mkdir(target_folder)

target_config = source_config
target_variables = target_config["variables"]
df = pd.read_csv(target_config["summary_csv_filename"].format(**target_variables))
target_config["variables"]["run_dir"] = os.path.abspath(target_folder)

with open(os.path.normpath(f"{target_folder}/config.json"), "w+") as f:
    json.dump(target_config, f)

filtered_df = df
if query is None:
    pass
else:
    match query:
        case "failed_pml":
            filtered_df = df.query("failed_pml_extract==1")

mb_SHA256 = filtered_df["SHA256"].tolist()
with open(target_variables["run_dir"] + "\\" + target_config["mb_SHA256_filename"], 'w+') as f:
    f.write('\n'.join(mb_SHA256))
