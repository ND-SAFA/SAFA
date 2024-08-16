import os
from typing import Any, Type, Tuple

from gen_common.infra.cli.inquirer_selector import inquirer_value
from gen_common.constants import OPTIONAL_KEY, SUPPORTED_TYPES_RQ
from gen_common.constants import EMPTY_STRING
from gen_common.infra.t_logging.logger_manager import logger


class RQVariable:

    def __init__(self, variable_definition: str):
        """
        Creates RQ variables from string possibly defining type.
        :param variable_definition: The variable definition containing name and optionally the type to cast into.
        """
        self.definition = variable_definition
        is_optional = OPTIONAL_KEY in variable_definition
        self.is_required = not is_optional
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
            value = inquirer_value(message=message, class_type=self.type_class, type_constructor=self.type_constructor,
                                   default_value=self.__default_value, allow_back=True,
                                   is_required=self.is_required)
            self.__value = value
        except Exception as e:
            logger.warning(e)
            return False
        assert value is not None or not self.is_required
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
            if self.is_required:
                if throw_error:
                    raise Exception(f"{self.name} has value of None.")
                result = False
        elif not isinstance(value, self.type_class):
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
