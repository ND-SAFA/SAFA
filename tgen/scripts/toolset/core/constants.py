import os

FUNC_PARAM = "func"
DESC_PARAM = "desc"
IGNORE_PARAMS = ["self"]
TOOL_RUNNER_NAME = "Tool Runner"
EXIT_COMMAND = "Exit"
BACK_COMMAND = "Back"
DEFAULT_CONFIG_PATH = "~/.aws/config"
DEFAULT_DATA_BUCKET = "safa-training-data"
DEFAULT_MODEL_BUCKET = "safa-models"
IGNORE_FILES = [".DS_Store"]
DATA_PATH = os.environ.get("DATA_PATH", None)
CLI_METHOD_PARAM = 'climethod'
