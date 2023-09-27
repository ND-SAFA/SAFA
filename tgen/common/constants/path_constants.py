import os
from os.path import abspath, dirname

ROOT_PATH_PARAM = "ROOT_PATH"
DATA_PATH_PARAM = "DATA_PATH"
OUTPUT_PATH_PARAM = "OUTPUT_PATH"
CURRENT_PROJECT_PARAM = "CURRENT_PROJECT"
WANDB_DIR_PARAM = "WANDB_DIR"
WANDB_PROJECT_PARAM = "WANDB_PROJECT"
PROJ_PATH = dirname(dirname(dirname(abspath(__file__))))
RES_PATH = os.path.join(PROJ_PATH, "res")
JAVA_KEYWORDS_PATH = os.path.join(RES_PATH, "JavaReservedKeywords.txt")
GENERATION_QUESTIONNAIRE_PROMPTS_PATH = os.path.join(PROJ_PATH, "data", "prompts", "supported_prompts",
                                                     "generation_questionnaire_prompts")
INPUTS_FOR_GENERATION_PATH = os.path.join(PROJ_PATH, "hgen", "inputs_for_generation")
USER_SYM = "~"
