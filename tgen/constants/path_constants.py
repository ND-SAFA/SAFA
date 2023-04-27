import os
from os.path import dirname, abspath

ROOT_PATH_PARAM = "ROOT_PATH"
DATA_PATH_PARAM = "DATA_PATH"
OUTPUT_PATH_PARAM = "OUTPUT_PATH"
WANDB_DIR_PARAM = "WANDB_DIR"
WANDB_PROJECT_PARAM = "WANDB_PROJECT"
PROJ_PATH = os.path.join(dirname(dirname(dirname(abspath(__file__)))), 'tgen')
RES_PATH = os.path.join(PROJ_PATH, "res")
JAVA_KEYWORDS_PATH = os.path.join(RES_PATH, "JavaReservedKeywords.txt")