import os
from os.path import dirname

from dotenv import load_dotenv

load_dotenv()
GEN_ROOT_PATH = dirname(dirname(dirname(__file__)))
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true").capitalize() == "True"
MODEL_PARAM = "MODEL"
RESPONSES_DIRNAME = "responses"
WANDB_DIR_PARAM = "WANDB_DIR"
WANDB_PROJECT_PARAM = "WANDB_PROJECT"
