import os
from os.path import abspath, dirname

from dotenv import load_dotenv

load_dotenv()
# -------------- JOB ARGS --------------
SAVE_OUTPUT_DEFAULT = True
SAVE_DATASET_SPLITS_DEFAULT = True

# -------------- TRACE ARGS --------------
MAX_SEQ_LENGTH_DEFAULT = 256
N_EPOCHS_DEFAULT = 3
EVALUATION_STRATEGY_DEFAULT = SAVE_STRATEGY_DEFAULT = "epoch"  # should be the same to load best model as per transformers docs
SAVE_TOTAL_LIMIT_DEFAULT = 2
LOAD_BEST_MODEL_AT_END_DEFAULT = True
METRIC_FOR_BEST_MODEL_DEFAULT = "f1"  # TODO

# -------------- DATASET --------------
BLOCK_SIZE_DEFAULT = 128
TRAINING_DATA_DIR_DEFAULT = "jobs/pretrain/mlm"
USE_LINKED_TARGETS_ONLY_DEFAULT = False
VALIDATION_PERCENTAGE_DEFAULT = 0.1
RESAMPLE_RATE_DEFAULT = 2
MLM_PROBABILITY_DEFAULT = 0.15
REPLACEMENT_PERCENTAGE_DEFAULT = 0.15

# -------------- PRE-PROCESSING --------------
MIN_LENGTH_DEFAULT = 1

# -------------- METRICS --------------
K_METRIC_DEFAULT = [1, 2, 3]
THRESHOLD_DEFAULT = 0.5

# -------------- MODELS --------------
LOGITS = "logits"
LOSS = "loss"

# -------------- TEST/DEV --------------
IS_TEST = os.getenv("DEPLOYMENT", "development").lower() == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true").capitalize() == "True"
MNT_DIR = os.environ.get('MNT_DIR', "")

# -------------- PATHS --------------
PROJ_PATH = dirname(dirname(dirname(abspath(__file__))))
