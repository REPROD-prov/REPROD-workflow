This repo contains the code that was used to generate the provenance data at:
[https://doi.org/10.5281/zenodo.7933806](https://doi.org/10.5281/zenodo.7933806)

Published in the CSET 2023: [https://doi.org/10.1145/3607505.3607510](https://doi.org/10.1145/3607505.3607510)

Broadly, the code can be used to download batches of malware samples from 
[MalwareBazaar](https://bazaar.abuse.ch/), run them in a windows virtual machine and extract procmon logs
provided as  input to [SPADE](https://github.com/ashish-gehani/SPADE). The code depends on two virtual machine
images, the detailed instructions to create those images can be found in `virtual_machine_setup.txt`.

1. Setup the virtual environment inside the reprod directory with:
   1. `python -m venv venv`
   2. `source venv/bin/activate`
   3. `pip install -f requirements.txt`
2. Ensure that VirtualBox binaries are in your path (this is done by default on most package manager installations). 
This can be checked by running `vboxmanage` at the command line.
3. Download and unzip the [7zip](https://www.7-zip.org/) and
[Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) folders in the root directory
of this repo. The "7-Zip" and "ProcessMonitor" folders are already in the repo, ensure that the programs expand
into them.
4. NOT CLEAR HOW TO SETUP VIRTUAL MACHINES
5. The folder `runtemplate` is provided with `config.json` and `malwarebazaar_ransomware_exe_sha256.txt` a
complete list of ransomware hashes from MalwareBazaar (as of time of writing). A list of malware SHA256 hashes from
MalwareBazaar (this list can easily be obtained from [Malware Bazaar](https://bazaar.abuse.ch/export/#csv)). Copy
`runtemplate` to a location of your choice and edit `config.json`.
   1. Edit `run_dir` to the absolute path of the directory you just copied `runtemplate`.
   2. Edit `reprod_dir` to point to your `reprod_workflow` directory.
   3. Edit  `bazaar_api_key` to your malware bazaar API key.
6. Run `setup.py`, with your new `config.json`.
7. Run `run.py` to run the list of malware binaries inside the associated BMcollect logs, file-operations, 
densities, and screenshots for each hash in the previous step.
8. Run `makesummary.py` to generate a summary of the dataset.
9. To setup a new run based on the configuration of an existing run `clonerun.py` supplying the run folder
that will act as teh template and the name of the new run as command line arguments.


# Requirements
Python version: 3.11.0

Windows malware sandbox virtual machine requirements:
Ram : 8gb
Processor : 1 core
Storage: 68gb

SPADE virtual machine requirments:
Ram : 32gb
Processor: 2 cores
Storage : 50gb

Note: To change the settings of any vm, first make the desired changes then delete the current snapshot and take a new snapshot with same name.

# run.py
This script will take as argumnent the name of the folder you want to run and read a new line delimeted list of sha256 hashes available in that folder, download the corresponding binary from MalwareBazaar, run the binary in the windows malware host and log its activity using ProcMon and then extract the logs and densities of desktop files to log.txt and density folder respectively. It will then take the pml log files from the folder logs and will convert them into xml format using ProcMon filter then runs the script `getFileOperations.py`.

# getfileops.py
This script runs in spadeVm and take xml logs from the main folder which is also a shared folder between 
host and spadeVm. The script then runs bash script `file_ops.sh` within the SPADE host which uses SPADE to
calculate the file operations done by the ransomware.

# makesummary.py
This script extracts the maximum density changed from densities, number of new files, and file operations
of a ransomware and add that data to the `summary.csv` file. It takes as argument the name of the folder for which you want to make the csv.

# clonerun.py
This will clone a source run into a new directory, changing `run_dir` in the config appropriately and can
filter the summary file.
at follows the rules for DataFrame of the Pandas library and is a valid query based on "summary.csv", created after running vmAutomation.py for a folder
