The following project encompasses all jobs relating to generating trace links.

# Structure

- models: Responsible for loading models
- predict: Responsible for generating trace predictions
- pretrain: Responsible for pre-training models
- train: Responsible for training models

# Downloading

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