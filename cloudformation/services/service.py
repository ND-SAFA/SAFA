import os
import sys

from cloudformation.services.file_loader import collect_user_inputs
from cloudformation.services.store import CFArgs

ROOT_PATH = os.path.expanduser("//")
TGEN_PATH = os.path.join(ROOT_PATH, "tgen")
sys.path.append(ROOT_PATH)
sys.path.append(TGEN_PATH)

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from cloudformation.services.stack import create_stack

DEFINITIONS = "definitions"


def ref_constructor(loader, node):
    value = loader.construct_scalar(node)
    return {"Ref": value}


def get_file_path(store: CFArgs) -> str:
    if "file_name" in store:
        file_selected = store["file_name"]
    else:
        prompt = EMPTY_STRING
        definitions = list(filter(lambda f: f[0] != ".", os.listdir(DEFINITIONS)))

        for i, d in enumerate(definitions):
            prompt += f"{NEW_LINE}{i}:{d}"
        file_selected = input(f"{prompt}{NEW_LINE}Select index: ")

    store["file_name"] = file_selected
    file_path = os.path.join(DEFINITIONS, file_selected)
    if not os.path.isfile(file_path):
        raise Exception(f"File does not exists: {file_path}")
    print(f"Definition: {file_path}")
    return file_path


def get_parameter_value(parameter_name):
    return input(f"Enter value for parameter '{parameter_name}': ")


def prompt_for_parameters(parameters):
    user_parameters = {}
    for parameter in parameters:
        parameter_name = parameter['ParameterKey']
        parameter_value = get_parameter_value(parameter_name)
        user_parameters[parameter_name] = parameter_value
    return user_parameters


def prompt_definition(file_path: str):
    definition_params = get_definition_params(file_path)
    user_params = prompt_for_parameters(definition_params)
    return user_params


if __name__ == "__main__":
    file_path = get_file_path()
    params = collect_user_inputs(file_path)
    params = prompt_definition(file_path)
    stack_name = "test"
    create_stack(stack_name, file_path, params)
