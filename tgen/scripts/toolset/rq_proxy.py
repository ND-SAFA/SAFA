import json
import re
from typing import Any, Dict, List, Tuple, Type

from tgen.common.util.file_util import FileUtil
from tgen.common.util.json_util import JsonUtil
from tgen.scripts.constants import RQ_VARIABLE_REGEX, RQ_VARIABLE_START, SUPPORTED_TYPES_RQ
from tgen.scripts.toolset.confirm import confirm
from tgen.scripts.toolset.selector import inquirer_value


class RQVariable:

    def __init__(self, variable_definition: str):
        """
        Creates RQ variables from string possibly defining type.
        :param variable_definition: The variable definition containing name and optionally the type to cast into.
        """
        self.definition = variable_definition
        self.name, self.type_class = RQVariable.get_variable_type(variable_definition)
        self.value = None

    def parse_value(self, variable_value: Any) -> Any:
        """
        Parses the variable value using definition for typing.
        :param variable_value: The variable value.
        :return: Value of variable.
        """
        typed_value = self.type_class(variable_value)
        self.value = typed_value
        return typed_value

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
        self.script_name = self.get_script_name(rq_path)
        self.rq_json = JsonUtil.read_json_file(rq_path)
        self.variables = self.extract_variables(self.rq_json)

    def get_unknown_variables(self, default_values: Dict):
        """
        Prompts user to fill in any missing variables in RQ definition.
        :param default_values: Dictionary of default values to allow user to select from.
        :return: Dictionary of variable to values selected.
        """
        variable2value = {}
        unknown_variables = []
        for variable in self.variables:
            variable_name = variable.name
            if variable_name in variable2value:
                continue
            if variable_name in default_values:
                variable2value[variable.definition] = variable.parse_value(default_values[variable_name])
            else:
                unknown_variables.append(variable)
        return variable2value, unknown_variables

    def inquirer_variables(self, default_values: Dict) -> Dict:
        """
        Prompts user to fill in any missing variables in RQ definition.
        :param default_values: Dictionary of default values to allow user to select from.
        :return: Dictionary of variable to values selected.
        """
        variable2value, unknown_variables = self.get_unknown_variables(default_values)

        for variable in self.variables:
            message = f"{variable.name}"
            user_value = inquirer_value(message, variable.type_class, default_value=variable.value)
            variable2value[variable.definition] = user_value
        confirmation_message = json.dumps(variable2value, indent=4)
        if confirm(f"Are these the correct values?\n{confirmation_message}"):
            return variable2value
        else:
            return inquirer_value(default_values)

    @classmethod
    def extract_variables(cls, rq_definition: Dict) -> List[RQVariable]:
        """
        Extracts the variables present in RQ definition.
        :param rq_definition: Definition of research question.
        :return: List of variables
        """
        json_values = cls.get_json_values(rq_definition)
        values = [v for v in json_values if isinstance(v, str) and RQ_VARIABLE_START in v]  # extract values containing variables

        seen_variables = set()
        variables: List[RQVariable] = []
        for value in values:
            for variable in cls.create_variables_from_string(value):
                if variable.name in seen_variables:
                    continue
                variables.append(variable)
                seen_variables.add(variable.name)
        return variables

    @classmethod
    def create_variables_from_string(cls, input_string: str) -> List[RQVariable]:
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

    @staticmethod
    def get_script_name(path: str) -> str:
        """
        :param path: Path used to construct id.
        :return: Returns the directory and file name of path used to identify scripts.
        """
        return FileUtil.get_file_name(path, n_parents=1)
