import inspect
from typing import Any

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.scripts.constants import MISSING_PARAM_ERROR, PARAM_DOCSTRING_QUERY
from tgen.scripts.toolset.inquirer_selector import inquirer_value


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

    def inquirer_value(self, **kwargs) -> Any:
        """
        Prompts user to give value for param.
        :param kwargs: Keyword arguments to inquirer value from user.
        :return: The value of the param.
        """
        param_message = f"{self.name} - {self.description}"
        param_value = inquirer_value(param_message, class_type=self.annotation, default_value=self.default, **kwargs)
        return param_value

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
        error_message = MISSING_PARAM_ERROR.format(param_name)
        assert method_doc is not None, error_message
        lines = method_doc.split(NEW_LINE)
        for line in lines:
            param_doc_query = PARAM_DOCSTRING_QUERY.format(param_name)
            if param_doc_query in line:
                return line.split(param_doc_query)[1].strip()
        raise Exception(error_message)
