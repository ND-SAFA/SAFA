import os
import re
from typing import Any, Dict, List, Optional, Tuple, Type

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, NONE
from tgen.common.logging.logger_manager import logger
from tgen.common.util.file_util import FileUtil
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.common.util.yaml_util import YamlUtil
from tgen.scripts.constants import MISSING_DEFINITION_ERROR, RQ_INQUIRER_CONFIRM_MESSAGE, RQ_VARIABLE_REGEX, \
    RQ_VARIABLE_START, \
    SUPPORTED_TYPES_RQ
from tgen.scripts.toolset.confirm import confirm
from tgen.scripts.toolset.selector import inquirer_value

OPTIONAL_KEY = "_OPTIONAL"


class RQVariable:

    def __init__(self, variable_definition: str):
        """
        Creates RQ variables from string possibly defining type.
        :param variable_definition: The variable definition containing name and optionally the type to cast into.
        """
        self.definition = variable_definition
        is_optional = OPTIONAL_KEY in variable_definition
        self.is_required = is_optional
        if is_optional:
            variable_definition = variable_definition.replace(OPTIONAL_KEY, EMPTY_STRING)
        self.name, self.type_constructor, self.type_class = RQVariable.get_variable_type(variable_definition)
        self.__value = None
        self.__default_value = None

    def has_value(self) -> bool:
        """
        Returns if the variable has a value other than default
        :return: True if the variable has a value other than default
        """
        return self.__value is not None

    def get_value(self) -> Any:
        """
        :return: Returns the value of the variable.
        """
        value = self.__default_value if self.__value is None else self.__value
        if isinstance(value, str):
            value = os.path.expanduser(value)
        return value

    def inquirer_value(self) -> bool:
        """
        Prompts user to enter valid value for variable.
        :return: Whether the user input was successful or not
        """
        message = f"{self.name}"
        try:
            value = inquirer_value(message, self.type_class, default_value=self.__default_value, allow_back=True)
            self.__value = value
        except Exception as e:
            logger.warning(e)
            return False
        assert value is not None
        return True

    def parse_value(self, variable_value: Any) -> Any:
        """
        Parses the variable value using definition for typing.
        :param variable_value: The variable value.
        :return: Value of variable.
        """
        typed_value = self.type_constructor(variable_value)
        self.__value = typed_value
        return typed_value

    def set_default_value(self, default_value: Any) -> None:
        """
        Sets the default value for variable.
        :param default_value: Default value to set.
        :return: None
        """
        typed_default_value = self.type_constructor(default_value) if default_value is not None else default_value
        self.__default_value = typed_default_value

    def set_value(self, value: Any) -> None:
        """
        Sets the value of teh variable
        :param value: The value to set
        :return: None
        """
        self.__value = value

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
    def get_variable_type(cls, variable_definition: str, default_type: Type = str) -> Tuple[str, Type, Type]:
        """
        Extracts variable name and its associated type class.
        :param variable_definition: The variable name.
        :param default_type: The default type to cast into if no type is found.
        :return: Name and type class of variable.
        """

        for type_class, type_class_constructor in SUPPORTED_TYPES_RQ.items():
            type_class_key = f"_{type_class.__name__.upper()}"
            if variable_definition.endswith(type_class_key):
                variable_name = variable_definition.split(type_class_key)[0]
                return variable_name, type_class_constructor, type_class
        return variable_definition, default_type, default_type

    def __repr__(self):
        """
        Represents class with variable name.
        :return: Variable name.
        """
        return f"{self.name}={self.get_value()}"


class RQDefinition:
    OUTPUT_DIR = "output_dir"

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

    def build_rq(self) -> Dict:
        """
        Builds the RQ JSON with all variables filled in.
        :return: RQ Json.
        """
        variable_replacements = self.__get_variable_replacements()
        built_rq_json = FileUtil.expand_paths(self.rq_json, variable_replacements)
        self.save_rq_variables()
        return built_rq_json

    def set_default_values(self, default_values: Dict = None, use_os_values: bool = False) -> None:
        """
        Sets the default values for variable in map.
        :param default_values: Map of variable names to their default values.
        :param use_os_values: Whether to use OS values as the default values.
        :return: None
        """
        if default_values is None and not use_os_values:
            raise Exception("Expected default_values to be passed or os values to be turned on.")
        if default_values is None:
            default_values = {}
        if use_os_values:
            for env_key, env_value in os.environ.items():
                env_value = None if env_value.lower() == NONE else os.path.expanduser(env_value)
                default_values[env_key] = env_value

        for variable in self.variables:
            if variable.name not in default_values:
                continue
            default_value = default_values[variable.name]
            variable.set_default_value(default_value)

    def fill_variables(self) -> None:
        """
        Ensures all variables have been filled in either by reloading a previous config or by prompting the user
        :return: None
        """
        load_rq_path = self.get_rq_save_path()
        if FileUtil.safely_check_path_exists(load_rq_path):
            should_reload = confirm(f"Do you want to reload variables from the last run of {self.script_name}?")
            if should_reload:
                try:
                    variables_map = self.read_rq_variables()
                    for v in self.variables:
                        if v.name in variables_map:
                            v.set_value(variables_map[v.name].get_value())
                except Exception:
                    logger.exception(f"Unable to reload previous rq config from {load_rq_path}")
        self.inquirer_variables()

    def inquirer_variables(self) -> None:
        """
        Prompts user to fill in any missing variables in RQ definition.
        :return: None
        """
        for variable in self.variables:
            if not variable.has_value():
                success = variable.inquirer_value()
                if not success:
                    self.inquirer_variables()
        if not self.has_all_variable():
            self.inquirer_variables()
        if not self.confirm():
            self.clear_variable_values()
            self.inquirer_variables()

    def read_rq_variables(self) -> Dict[str, RQVariable]:
        """
        Reads the rq variables from a yaml file
        :return: Mapping of variable name to variable if successfully reloaded
        """
        try:
            load_rq_path = self.get_rq_save_path()
            assert load_rq_path
            variables = YamlUtil.read(load_rq_path)
            return variables
        except Exception:
            return {}

    def save_rq_variables(self) -> bool:
        """
        Saves the rq variables to a yaml file
        :return: Whether the rq successfully saved
        """
        try:
            save_rq_path = self.get_rq_save_path()
            assert save_rq_path
            variables_map = {v.name: v for v in self.variables}
            YamlUtil.write(variables_map, save_rq_path)
            return True
        except Exception:
            return False

    def get_rq_save_path(self) -> Optional[str]:
        """
        Returns the path at which the rq config should be saved
        :return: The path at which the rq config should be saved
        """
        if self.OUTPUT_DIR not in self.rq_json:
            return
        output_dir = FileUtil.expand_paths(self.rq_json[self.OUTPUT_DIR])
        save_rq_path = os.path.join(output_dir, "rq_config.yaml")
        return save_rq_path

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

    def has_all_variable(self):
        """
        Checks is all variables have valid values.
        :return: True if all variables are valid else False
        """
        has_all_variables = True
        for variable in self.variables:
            if not variable.has_valid_value(throw_error=False):
                variable.set_value(None)
                has_all_variables = False
        return has_all_variables

    def clear_variable_values(self):
        """
        Resets all variable values to None.
        :return:
        """
        for variable in self.variables:
            variable.set_value(None)

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
        values = [v for v in json_values if cls.is_variable(v)]  # extract values containing variables

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
    def is_variable(cls, json_value: Any) -> bool:
        """
        Determines if the json value is a variable
        :param json_value: The json value
        :return: True if it is a variable, else False
        """
        return isinstance(json_value, str) and RQ_VARIABLE_START in json_value

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
