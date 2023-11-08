import os
import re
from typing import Any, Dict, List, Tuple, Type

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.file_util import FileUtil
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.scripts.constants import MISSING_DEFINITION_ERROR, RQ_INQUIRER_CONFIRM_MESSAGE, RQ_VARIABLE_REGEX, \
    RQ_VARIABLE_START, \
    SUPPORTED_TYPES_RQ
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
        self.__value = None
        self.__default_value = None

    def get_value(self) -> Any:
        """
        :return: Returns the value of the variable.
        """
        value = self.__default_value if self.__value is None else self.__value
        if isinstance(value, str):
            value = os.path.expanduser(value)
        return value

    def inquirer_value(self) -> None:
        """
        Prompts user to enter valid value for variable.
        :return: None
        """
        message = f"{self.name}"
        self.__value = inquirer_value(message, self.type_class, default_value=self.__default_value)

    def parse_value(self, variable_value: Any) -> Any:
        """
        Parses the variable value using definition for typing.
        :param variable_value: The variable value.
        :return: Value of variable.
        """
        typed_value = self.type_class(variable_value)
        self.__value = typed_value
        return typed_value

    def set_default_value(self, default_value: Any) -> None:
        """
        Sets the default value for variable.
        :param default_value: Default value to set.
        :return: None
        """
        typed_default_value = self.type_class(default_value)
        self.__default_value = typed_default_value

    def has_valid_value(self, throw_error: bool = False) -> bool:
        """
        :param throw_error: Whether to throw error if value is not valid.
        :return: Returns whether variable contains value of specified type.
        """
        value = self.get_value()
        result = True
        if value is None:
            if throw_error:
                raise Exception(f"{self.name} has value of None.")
            result = False
        if not isinstance(value, self.type_class):
            if throw_error:
                raise Exception(f"{self.name} contains value of type {type(value)} but expected {self.type_class}.")
            result = False
        return result

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
        return f"{self.name}={self.get_value()}"


class RQDefinition:
    def __init__(self, rq_path: str):
        """
        Defines proxy API for RQ at path.
        :param rq_path: Path to RQ to create proxy for.
        """
        if not os.path.isfile(rq_path):
            raise ValueError(MISSING_DEFINITION_ERROR.format(rq_path))
        self.rq_path = rq_path
        self.script_name = self.get_script_name(rq_path)
        self.rq_json = JsonUtil.read_json_file(rq_path)
        self.variables = self.extract_variables(self.rq_json)

    def build_rq(self, error_on_fail: bool = True) -> Dict:
        """
        Builds the RQ JSON with all variables filled in.
        :param error_on_fail: Whether to throw an error if a variable does not have a valid value.
        :return: RQ Json.
        """
        self.has_all_variable(throw_error=error_on_fail)
        variable_replacements = self.__get_variable_replacements()
        built_rq = FileUtil.expand_paths(self.rq_json, variable_replacements)
        return built_rq

    def set_default_values(self, default_values: Dict = None, use_os_values: bool = False) -> None:
        """
        Sets the default values for variable in map.
        :param default_values: Map of variable names to their default values.
        :return: None
        """
        if default_values is None and not use_os_values:
            raise Exception("Expected default_values to be passed or os values to be turned on.")
        if default_values is None:
            default_values = {}
        if use_os_values:
            for env_key, env_value in os.environ.items():
                default_values[env_key] = os.path.expanduser(env_value)

        for variable in self.variables:
            if variable.name not in default_values:
                continue
            default_value = default_values[variable.name]
            variable.set_default_value(default_value)

    def inquirer_variables(self) -> None:
        """
        Prompts user to fill in any missing variables in RQ definition.
        :param default_values: Dictionary of default values to allow user to select from.
        :return: None
        """
        for variable in self.variables:
            variable.inquirer_value()
        if not self.confirm():
            self.inquirer_variables()

    def confirm(self, title: str = RQ_INQUIRER_CONFIRM_MESSAGE) -> bool:
        """
        Confirms values of the rq with the user.
        :param title: The title of the message.
        :return: Whether the user confirmed the values.
        """
        variable_messages = []
        for variable in self.variables:
            variable_messages.append(repr(variable))
        variable_values_message = NEW_LINE.join(variable_messages)
        return confirm(f"\n{title}\n{variable_values_message}")

    def has_all_variable(self, throw_error: bool = True):
        """
        Checks is all variables have valid values.
        :param throw_error: Whether to throw error
        :return:
        """
        for variable in self.variables:
            variable.has_valid_value(throw_error=True)
        return True

    def __get_variable_replacements(self) -> Dict:
        """
        :return: Returns the map of variable names to their values.
        """
        return {f"[{v.definition}]": v.get_value() for v in self.variables}

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

        if ReflectionUtil.is_primitive(rq_json):
            return [rq_json]
        
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
