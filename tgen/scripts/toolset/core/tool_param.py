import inspect
from typing import Any

from tgen.scripts.toolset.core.selector import inquirer_value


class ToolParam:

    def __init__(self, name: str, param: inspect.Parameter, func_doc: str):
        """
        Parameter for a tool function.
        :param name: The name of the parameter in the function.
        :param param: The parameter object.
        :param func_doc: The doc string for the function.
        """
        self.name = name
        self.param = param
        self.description = ToolParam.get_param_description(func_doc, name)
        self.default = ToolParam.get_default(param)
        self.annotation = param.annotation

    def inquirer(self) -> Any:
        """
        Prompts user to give value for param.
        :return: The value of the param.
        """
        param_message = self._get_inquirer_message()
        param_value = inquirer_value(param_message, self.annotation, self.default)
        return param_value

    def _get_inquirer_message(self) -> str:
        """
        :return: The message used to inquire about the param value.
        """
        message = f"{self.name} - {self.annotation.__name__} - {self.description}"
        if self.default is not None:
            message += f"({self.default})"
        return message

    @staticmethod
    def get_default(param: inspect.Parameter):
        """
        Extracts the default value for the parameter.
        :param param: The parameter to extract value from.
        :return: The default value.
        """
        param_default = None
        if param.default is not inspect.Parameter.empty:
            param_default = param.default
        return param_default

    @staticmethod
    def get_param_description(method_doc: str, param_name: str):
        """
        Returns the description of parameter in DocString.
        :param method_doc: The PyDoc as a string.
        :param param_name: The name of the parameter whose description is returned.
        :returns: The description of parameters.
        """
        error_message = f"`{param_name}` is missing a description.."
        assert method_doc is not None, error_message
        lines = method_doc.split('\n')
        for line in lines:
            if f':param {param_name}:' in line:
                return line.split(f':param {param_name}:')[1].strip()
        raise Exception(error_message)
