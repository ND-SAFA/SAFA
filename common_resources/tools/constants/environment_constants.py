import os
from typing import Any

from dotenv import load_dotenv

from common_resources.tools.constants.env_var_name_constants import ANTHROPIC_API_KEY_PARAM, DATA_PATH_PARAM, \
    DEFAULT_CROSS_ENCODER_MODEL_PARAM, DEFAULT_EMBEDDING_MODEL_PARAM, DEPLOYMENT_PARAM, HF_DATASETS_CACHE_PARAM, OPEN_AI_KEY_PARAM, \
    OPEN_AI_ORG_PARAM
from common_resources.tools.constants.model_constants import DEFAULT_DEPLOYMENT_CROSS_ENCODER_MODEL, \
    DEFAULT_DEPLOYMENT_EMBEDDING_MODEL, DEFAULT_TEST_EMBEDDING_MODEL

load_dotenv()


def get_environment_variable(var_name: str, default: Any = None) -> str:
    """
    By using this method, ensures that load dotenv is called first.
    :param var_name: The name of the variable.
    :param default: The value to default it to if it doesn't exist.
    :return: The variable value or default if not present in .env
    """
    return os.environ.get(var_name, default)


IS_TEST = get_environment_variable(DEPLOYMENT_PARAM, "development").lower() == "test"
OPEN_AI_KEY = get_environment_variable(OPEN_AI_KEY_PARAM)
OPEN_AI_ORG = get_environment_variable(OPEN_AI_ORG_PARAM)
ANTHROPIC_KEY = get_environment_variable(ANTHROPIC_API_KEY_PARAM)
SELECTED_DEFAULT_EMBEDDING_MODEL = DEFAULT_TEST_EMBEDDING_MODEL if IS_TEST else DEFAULT_DEPLOYMENT_EMBEDDING_MODEL
DEFAULT_EMBEDDING_MODEL = get_environment_variable(DEFAULT_EMBEDDING_MODEL_PARAM, SELECTED_DEFAULT_EMBEDDING_MODEL)
DEFAULT_CROSS_ENCODER_MODEL = get_environment_variable(DEFAULT_CROSS_ENCODER_MODEL_PARAM, DEFAULT_DEPLOYMENT_CROSS_ENCODER_MODEL)
HF_DATASETS_CACHE = get_environment_variable(HF_DATASETS_CACHE_PARAM)
DATA_PATH = get_environment_variable(DATA_PATH_PARAM)
