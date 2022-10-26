import os
from os.path import abspath, dirname

import math

# -------------- JOB ARGS --------------
SAVE_OUTPUT_DEFAULT = True
ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT = True
MLM_PROBABILITY_DEFAULT = 0.15

# -------------- TRACE ARGS --------------
MAX_SEQ_LENGTH_DEFAULT = 256
RESAMPLE_RATE_DEFAULT = 2
EVAL_DATASET_SIZE_DEFAULT = math.inf
PAD_TO_MAX_LENGTH_DEFAULT = True
LINKED_TARGETS_ONLY_DEFAULT = False
VALIDATION_PERCENTAGE_DEFAULT = 0.1
N_EPOCHS_DEFAULT = 10
EVALUATION_STRATEGY_DEFAULT = SAVE_STRATEGY_DEFAULT = "epoch"  # should be the same to load best model as per transformers docs
SAVE_TOTAL_LIMIT_DEFAULT = 2
LOAD_BEST_MODEL_AT_END_DEFAULT = True
METRIC_FOR_BEST_MODEL_DEFAULT = "f1"  # TODO

# -------------- DATASET --------------
BLOCK_SIZE_DEFAULT = 128
TRAINING_DATA_DIR_DEFAULT = "jobs/pretrain/mlm"
USE_LINKED_TARGETS_ONLY_DEFAULT = False

# -------------- PreProcessing --------------
MIN_LENGTH_DEFAULT = 1

# -------------- METRICS --------------
K_METRIC_DEFAULT = 10  # TODO

# -------------- MODELS --------------
LOGITS = "logits"
LOSS = "loss"

# -------------- TEST/DEV --------------
IS_TEST = os.getenv("DEPLOYMENT", "development").lower() == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true").capitalize() == "True"
MNT_DIR = os.environ.get('MNT_DIR', "")

# -------------- PATHS --------------
PROJ_PATH = dirname(dirname(dirname(abspath(__file__))))
