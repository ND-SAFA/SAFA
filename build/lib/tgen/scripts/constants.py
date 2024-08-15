import os

from tgen.scripts.util import bool_constructor, list_constructor

"""
RQ DEFINITION
"""
RQ_INQUIRER_CONFIRM_MESSAGE = "Are these the correct values?"
"""
Tool Set
"""
FUNC_PARAM = "func"
DESC_PARAM = "desc"
IGNORE_PARAMS = ["self"]
TOOL_RUNNER_NAME = "Tool Runner"
EXIT_COMMAND = "exit"
BACK_COMMAND = "back"
DEFAULT_CONFIG_PATH = "~/.aws/config"
DEFAULT_DATA_BUCKET = "safa-training-data"
DEFAULT_MODEL_BUCKET = "safa-models"
IGNORE_FILES = [".DS_Store"]
DATA_PATH = os.environ.get("DATA_PATH", None)
CLI_METHOD_PARAM = 'climethod'
DEFAULT_ALLOW_BACK = False
SINGLETON_PROMPT_ID = "prompt_id"
EXIT_MESSAGE = "Bye bye :)"
REQUIRED_FIELD_ERROR = "Required field received empty value."
DEFAULT_VALUE_MESSAGE = "Default value used."
MISSING_PARAM_ERROR = "`{}` is missing a description.."
PARAM_DOCSTRING_QUERY = ":param {}:"
TOOL_MISSING_DOCSTRING_ERROR = "Tool {} does not have a doc-string."

SUPPORTED_TYPES_RQ = {
    int: int,
    float: float,
    str: str,
    bool: bool_constructor,
    list: list_constructor
}
RQ_VARIABLE_START = "["
RQ_VARIABLE_REGEX = r'\[([^\[\]]+)\]'
RQ_NAV_MESSAGE = "Select RQ to run"
FOLDER_NAV_MESSAGE = "Select RQ Folder"
PARENT_FOLDER = ".."
RQ_PATH_PARAM = "RQ_PATH"
MISSING_DEFINITION_ERROR = "{} does not exists."
CONFIRM_MESSAGE_DEFAULT = "Confirm?"
CONFIRM_OPTIONS = "(y/n)"
CONFIRM_PARSE_ERROR = "Unable to parse response: {}"
CONFIRM_POS = "y"
CONFIRM_NEG = "n"
