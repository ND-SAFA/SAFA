# About
This repository contains the resources needed to support our research in traceability and includes the following:

## Data
Contains tools for creating datasets from flat files and storing them in custom dataframes. There are additional resources for data cleaning, augmentation and splitting datasets for testing/training. 

## LLM
Contains ways of interacting with various LLMs such as Anthropic and OpenAI models. Additionally, prompt templates are provided alongside parsers for XML and JSON responses.

## Traceability
Contains custom metrics for traceability alongside managers for cross encoder and embedding models for scoring relationships between artifacts.

## Tools
Contains utility methods, custom logger, threading resources, and project constants.

# Setup
To install:
```sh
 pip install git+https://github.com/kat-dearstyne/common-resources.git
```
1. All requirements can be found in requirements.txt
2. Certain environment variables are expected to be set to use private LLMs and other features. <br>
   Note: A full list of environment params can be found in `common_resources/tools/constants/env_var_name_constants.py`
