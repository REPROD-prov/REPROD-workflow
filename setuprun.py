import os
import argparse
from utils import load_format_config
from utils import dotdict

parser = argparse.ArgumentParser()
parser.add_argument(
    'config_file', help="name of the config file with run parameters")
args = parser.parse_args()

config = load_format_config(args.config_file)

paths = [config.pml_path,
         config.pml_done_path,
         config.xml_path,
         config.density_path,
         config.dotfiles_path,
         config.screenshots_path,
         f"{config.density_path}/before",
         f"{config.density_path}/after"
         ]

paths = [os.path.normpath(path) for path in paths]

for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)

print("setup done")
