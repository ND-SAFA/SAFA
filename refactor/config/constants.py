import os
from os.path import abspath, dirname

import math

# -------------- JOB ARGS --------------
MAX_SEQ_LENGTH_DEFAULT = 256
RESAMPLE_RATE_DEFAULT = 2
EVAL_DATASET_SIZE_DEFAULT = math.inf
PAD_TO_MAX_LENGTH_DEFAULT = True
LINKED_TARGETS_ONLY_DEFAULT = False
VALIDATION_PERCENTAGE_DEFAULT = 0.1
N_EPOCHS_DEFAULT = 10
SAVE_OUTPUT_DEFAULT = True

# -------------- METRICS --------------
K_METRIC_DEFAULT = 10  # TODO

# -------------- MODELS --------------

LOGITS = "logits"
LOSS = "loss"

# -------------- MODELS --------------
IS_TEST = os.getenv("DEPLOYMENT", "development").lower() == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true") == "true"
MNT_DIR = os.environ.get('MNT_DIR', "")
# -------------- PATHS --------------

PROJ_PATH = dirname(dirname(dirname(abspath(__file__))))
