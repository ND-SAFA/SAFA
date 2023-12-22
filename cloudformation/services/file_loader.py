from typing import Dict

import yaml

from cloudformation.services.store import CFArgs


def ref_constructor(loader, node):
    """
    YAML constructor for !Ref tag.
    """
    value = loader.construct_scalar(node)
    return {"Ref": value}


def sub_constructor(loader, node):
    """
    YAML constructor for !Sub tag.
    """
    value = loader.construct_scalar(node)
    return {"Fn::Sub": value}


yaml.SafeLoader.add_constructor("!Ref", ref_constructor)
yaml.SafeLoader.add_constructor("!Sub", sub_constructor)


def get_definition_params(file_path: str) -> Dict:
    """
    Reads the cloudformation parameters of file.

    :param file_path: Path to cloud formation yaml file.
    :return: Dictionary of parameters.
    """
    with open(file_path, 'r') as file:
        template = yaml.safe_load(file)

    parameters = template.get('Parameters', {})
    return parameters


def prompt_for_parameter(param_name, param_info):
    """
    Prompts the user for a parameter value.

    :param param_name: Name of the parameter.
    :param param_info: Information about the parameter from CloudFormation template.
    :return: User-input value for the parameter.
    """
    param_type = param_info["Type"]
    default_value = param_info.get("Default")

    while True:
        prompt_message = f"Enter a value for '{param_name}' ({param_type})"
        if default_value is not None:
            prompt_message += f" [Default: {default_value}]"

        user_input = input(prompt_message + ": ").strip()

        if not user_input and default_value is None:
            print(f"Value for '{param_name}' is required. Please provide a value.")
        else:
            # Use the default value if the user enters no value
            value = cast_to_type(param_type, user_input) if user_input else cast_to_type(param_type, default_value)
            return value


def cast_to_type(param_type: str, user_input: str):
    """
    Casts the user input to the given type.

    :param param_type: Name of the type.
    :param user_input: Input to cast.
    :return: Casted value.
    """
    if param_type == "Number":
        value = int(user_input)  # Assumes the parameter is an integer
    else:
        # Handle other types as needed
        value = str(user_input)
    return value


def collect_user_inputs(file_path: str, store: CFArgs = None, printable_vars: Dict = None, skip_defaults: bool = True) -> Dict:
    """
    Prompts the user for each parameter without a default value.

    :param file_path: Path to cloud formation file.
    :return: Dictionary containing user-input values for each parameter.
    """
    if store is None:
        store = {}
    if printable_vars is None:
        printable_vars = {}

    params = get_definition_params(file_path)
    user_inputs = {}

    for param_name, param_info in params.items():
        p_query = param_name.lower()
        if p_query in printable_vars:
            printable_vars[p_query](store)
        if "Default" in param_info and skip_defaults:
            v = param_info["Default"]
        elif p_query in store:
            v = store[p_query]
        else:
            v = prompt_for_parameter(param_name, param_info)
        user_inputs[param_name] = v

    return user_inputs
