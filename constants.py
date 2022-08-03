import math
import os

# -------------- JOB ARGS --------------
MAX_SEQ_LENGTH_DEFAULT = 256
RESAMPLE_RATE_DEFAULT = 1
EVAL_DATASET_SIZE_DEFAULT = math.inf
PAD_TO_MAX_LENGTH_DEFAULT = True
LINKED_TARGETS_ONLY_DEFAULT = False

# -------------- METRICS --------------
K_METRIC_DEFAULT = 10  # TODO
EVAL_RESULTS_KEY = "metrics"

# -------------- PRETRAIN --------------
PRETRAIN_NUM_TRAINING_SIZE_DEFAULT = 5000
PRETRAIN_BATCH_SIZE_DEFAULT = 4
PRETRAIN_LEARNING_RATE_DEFAULT = 1e-4
PRETRAIN_VOCAB_FILE = ""  # TODO
PRETRAIN_MODEL_PATH = "google/electra-{}-discriminator"
PRETRAIN_MODEL_NAME = "electra_{}"

# -------------- PATHS --------------
PROJ_PATH = os.path.dirname(os.path.abspath(__file__))
PRETRAIN_DATA_PATH = os.path.join(PROJ_PATH, "pretrain", "data")  # TODO - better way to do this?
