import re
from typing import Dict, List, Tuple, Type

from tgen.common.util.json_util import JsonUtil
from tgen.scripts.constants import RQ_VARIABLE_REGEX, RQ_VARIABLE_START, SUPPORTED_TYPES_RQ
from tgen.scripts.toolset.core.selector import inquirer_value


class RQVariable:

    def __init__(self, variable_definition: str):
        """
        Creates RQ variables from string possibly defining type.
        :param variable_definition: The variable definition containing name and optionally the type to cast into.
        """
        self.definition = variable_definition
        self.name, self.type_class = RQVariable.get_variable_type(variable_definition)

    @classmethod
    def get_variable_type(cls, variable_definition: str, default_type: Type = str) -> Tuple[str, Type]:
        """
        Extracts variable name and its associated type class.
        :param variable_definition: The variable name.
        :param default_type: The default type to cast into if no type is found.
        :return: Name and type class of variable.
        """

        supported_type_map = {f"_{t.__name__.upper()}": t for t in SUPPORTED_TYPES_RQ}
        for type_class_key, type_class in supported_type_map.items():
            if variable_definition.endswith(type_class_key):
                variable_name = variable_definition.split(type_class_key)[0]
                return variable_name, type_class
        return variable_definition, default_type

    def __repr__(self):
        """
        Represents class with variable name.
        :return: Variable name.
        """
        return self.name


class RQProxy:
    def __init__(self, rq_path: str):
        """
        Defines proxy API for RQ at path.
        :param rq_path: Path to RQ to create proxy for.
        """
        self.rq_path = rq_path
        self.rq_json = JsonUtil.read_json_file(rq_path)

    def inquirer_unknown_variables(self, default_values: Dict) -> Dict:
        """
        Prompts user to fill in any missing variables in RQ definition.
        :param default_values: Dictionary of default values to allow user to select from.
        :return: Dictionary of variable to values selected.
        """
        json_values = self.get_json_values(self.rq_json)
        values = [v for v in json_values if isinstance(v, str) and RQ_VARIABLE_START in v]  # extract values containing variables

        variables: List[RQVariable] = []
        for value in values:
            variables.extend(self.extract_variables(value))

        variable2value = {}
        for variable in variables:
            variable_name = variable.name
            if variable_name in variable2value:
                continue
            message = f"{variable_name}"
            default_value = default_values[variable_name] if variable_name in default_values else None
            user_value = inquirer_value(message, variable.type_class, default_value)
            variable2value[variable.definition] = user_value
        variable2value.update(default_values)
        return variable2value

    @classmethod
    def extract_variables(cls, input_string: str) -> List[RQVariable]:
        """
        Finds the variables defined in string.
        :param input_string: The input string to check for variables.
        :return: List of variables in string.
        """
        matches = re.findall(RQ_VARIABLE_REGEX, input_string)
        variables = [RQVariable(match) for match in matches]
        return variables

    @classmethod
    def get_json_values(cls, rq_json: Dict) -> List[str]:
        """
        Returns all values defined in the dictionary.
        :param rq_json: Json of RQ definition.
        :return: List of values.
        """
        values = []
        for child_key, child_value in rq_json.items():
            if isinstance(child_value, list):
                for i in child_value:
                    values.extend(cls.get_json_values(i))
            elif isinstance(child_value, dict):
                values.extend(cls.get_json_values(child_value))
            else:
                values.append(child_value)
        return values
