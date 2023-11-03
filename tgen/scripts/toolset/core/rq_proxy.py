import re
from typing import Dict, List, Type

from tgen.common.util.json_util import JsonUtil
from tgen.scripts.toolset.core.selector import inquirer_value


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
        values = self.get_json_values(self.rq_json)
        values = [v for v in values if isinstance(v, str) and "[" in v]  # extract values containing variables

        variables = []
        for value in values:
            variables.extend(self.extract_variables(value))

        variable2value = {}
        for variable in variables:
            message = f"{variable}"
            default_value = default_values[variable] if variable in default_values else None
            variable_type = self.get_variable_type(variable)
            user_value = inquirer_value(message, variable_type, default_value)
            variable2value[variable] = user_value
        variable2value.update(default_values)
        return variable2value

    @classmethod
    def get_variable_type(cls, variable: str, default_type: Type = str) -> Type:
        """
        Returns the type of variable it should be casted into.
        :param variable: The variable name.
        :param default_type: The default type to cast into if no type is found.
        :return: The expected class of the variable.
        """
        supported_types = [int, float, str]
        supported_type_map = {f"_{t.__name__.upper()}]": t for t in supported_types}
        for k, v in supported_type_map.items():
            if variable.endswith(k):
                return v
        return default_type

    @classmethod
    def extract_variables(cls, input_string: str):
        """
        Finds the variables defined in string.
        :param input_string: The input string to check for variables.
        :return: List of variables in string.
        """
        pattern = r'\[([^\[\]]+)\]'
        matches = re.findall(pattern, input_string)
        return [f'[{match}]' for match in matches]

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
