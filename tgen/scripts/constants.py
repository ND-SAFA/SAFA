import os

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


class CustomReprFunc:

    def __init__(self, f, custom_repr):
        self.f = f
        self.custom_repr = custom_repr

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def __repr__(self):
        return self.custom_repr(self.f)


def set_repr(custom_repr):
    def set_repr_decorator(f):
        return CustomReprFunc(f, custom_repr)

    return set_repr_decorator


@set_repr(lambda f: "bool")
def bool_constructor(s: str):
    return s.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


SUPPORTED_TYPES_RQ = {
    int: int,
    float: float,
    str: str,
    bool: bool_constructor,
    list: list
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
