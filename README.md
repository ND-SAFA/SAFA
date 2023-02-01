The following project encompasses all jobs relating to generating trace links.

# Structure

- rqs: Contains JSON definition for research questions
- src: Source code
    - data: The tools for reading and transforming data between input and outputs.
    - experiments: The code that allows experiment definitions to be written.
    - jobs: The infrastructure for running operations within TGEN (e.g. training, prediction).
    - models: The code for reading and using different models.
    - scripts: The scripts for running tgen on the server.
    - testres: The testing resources.
    - train: Responsible for training models
    - util: Series of utilities for files, json, data frames and other external data structures.
    - variables: The different types of variable used in experiments.
- all other files in this scope are deployment related files.

# Installation

1. Install conda, then run:
    - conda create -n tgen
    - conda activate tgen
    - pip3 install -r requirements.txt
    - conda install -c nvidia cudatoolkit
2. Setup .env file:

```commandline
ROOT_PATH=~/tgen/src
DATA_PATH=~/data
OUTPUT_PATH=~/output
DJANGO_SETTINGS_MODULE=server.settings
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256
RQ_PATH=~/tgen/rqs
BUCKET=s3://safa-datasets-open/results
```

3. Use `run.py` to run different research questions!

```commandline
$ (tgen) python3 src/scripts/run.py test_rq.json
```