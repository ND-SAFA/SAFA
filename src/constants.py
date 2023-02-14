import logging
import os
from os.path import abspath, dirname

from dotenv import load_dotenv

load_dotenv()
# -------------- END --------------
ROOT_PATH_PARAM = "ROOT_PATH"
DATA_PATH_PARAM = "DATA_PATH"
OUTPUT_PATH_PARAM = "OUTPUT_PATH"
WANDB_DIR_PARAM = "WANDB_DIR"
WANDB_PROJECT_PARAM = "WANDB_PROJECT"
# -------------- LOGGING --------------
LOG_LEVEL_DEFAULT = logging.INFO
LOG_FILE_DEFAULT = "output.log"
VERBOSE_DEFAULT = False
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s(%(lineno)d) %(message)s'
LOG_TO_CONSOLE_DEFAULT = True

# -------------- EXPERIMENT --------------
MAX_JOBS = 1
RUN_ASYNC = False
EXIT_ON_FAILED_JOB = True
BASE_EXPERIMENT_NAME = "base_experiment"
BEST_MODEL_NAME = "best"
EXPERIMENT_ID_DEFAULT = 0
OUTPUT_FILENAME = "output.json"

# -------------- JOB ARGS --------------
SAVE_OUTPUT_DEFAULT = True
SAVE_DATASET_SPLITS_DEFAULT = False

# -------------- TRACE ARGS --------------
MAX_SEQ_LENGTH_DEFAULT = 512
N_EPOCHS_DEFAULT = 3
EVALUATION_STRATEGY_DEFAULT = SAVE_STRATEGY_DEFAULT = "epoch"  # should be the same to load best model as per transformers docs
LOGGING_STRATEGY_DEFAULT = "steps"
EVAL_STEPS_DEFAULT = SAVE_STEPS_DEFAULT = None
LOGGING_STEPS_DEFAULT = 1
GREATER_IS_BETTER_DEFAULT = False
SAVE_TOTAL_LIMIT_DEFAULT = 1
LOAD_BEST_MODEL_AT_END_DEFAULT = True
METRIC_FOR_BEST_MODEL_DEFAULT = "eval_loss"
OPTIMIZER_DEFAULT = "adam"
SCHEDULER_DEFAULT = "linear"
GRADIENT_ACCUMULATION_DEFAULT = 8
USE_BALANCED_BATCHES_DEFAULT = False
MULTI_GPU_DEFAULT = True
EVAL_ON_EPOCH_DEFAULT = True
SAVE_RANDOM_MODEL_DEFAULT = True

# -------------- VSM --------------
VSM_THRESHOLD_DEFAULT = 0.5

# -------------- DATASET --------------
BLOCK_SIZE_DEFAULT = 50
VALIDATION_PERCENTAGE_DEFAULT = 0.1
RESAMPLE_RATE_DEFAULT = 2
MLM_PROBABILITY_DEFAULT = 0.15
REPLACEMENT_PERCENTAGE_DEFAULT = 0.15
REMOVE_ORPHANS_DEFAULT = False
ALLOWED_MISSING_SOURCES_DEFAULT = 0
ALLOWED_MISSING_TARGETS_DEFAULT = 0
ALLOWED_ORPHANS_DEFAULT = 0
NO_ORPHAN_CHECK_VALUE = -1
# -------------- PRE-PROCESSING --------------
MIN_LENGTH_DEFAULT = 1

# -------------- METRICS --------------
K_METRIC_DEFAULT = [1, 2, 3]
THRESHOLD_DEFAULT = 0.5
UPPER_RECALL_THRESHOLD = .95

# -------------- TEST/DEV --------------
IS_TEST = os.getenv("DEPLOYMENT", "development").lower() == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true").capitalize() == "True"
MNT_DIR = os.environ.get('MNT_DIR', "")

# -------------- PATHS --------------
PROJ_PATH = dirname(dirname(dirname(abspath(__file__))))

# -------------- SCRIPT PATHS --------------
METRICS = ["map", "map@1", "map@2", "map@3", "ap", "f2", "f1", "precision@1", "precision@2", "precision@3"]
DISPLAY_METRICS = ["map", "f2"]
OS_IGNORE = [".DS_Store"]
EXPERIMENTAL_VARS_IGNORE = ["job_args", "model_manager", "train_dataset_creator", "project_reader", "eval_dataset_creator",
                            "trainer_dataset_manager", "trainer_args", "dataset_creator"]

# -------------- ANALYSIS --------------
HIGH_FREQ_THRESHOLD_DEFAULT = 0.1
LOW_FREQ_THRESHOLD_DEFAULT = 0.02
LINK_COMMON_WORDS_THRESHOLD_DEFAULT = 0.01
SAVE_LINK_ANALYSIS_DEFAULT = True

# -------------- Datasets --------------
CACHE_DIR_NAME = "HuggingFace"
