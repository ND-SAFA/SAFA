import os

from common_resources.tools.constants.environment_constants import PROJ_PATH
from dotenv import load_dotenv

load_dotenv()

DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true").capitalize() == "True"
IS_INTERACTIVE = False
MODEL_PARAM = "MODEL"
RESPONSES_DIRNAME = "responses"
RES_PATH = os.path.join(PROJ_PATH, "res")
JAVA_KEYWORDS_PATH = os.path.join(RES_PATH, "JavaReservedKeywords.txt")
WANDB_DIR_PARAM = "WANDB_DIR"
WANDB_PROJECT_PARAM = "WANDB_PROJECT"
