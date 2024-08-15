import inspect
from typing import Any, Callable, List, Optional

from tgen.scripts.constants import IGNORE_PARAMS, TOOL_MISSING_DOCSTRING_ERROR
from tgen.scripts.toolset.tool_param import ToolParam


class Tool:
    def __init__(self, tool_func: Callable):
        """
        Initializes tool for given function.
        :param tool_func: The function to run tool with.
        """
        self.func = tool_func
        self.id = tool_func.__name__
        self.doc = inspect.getdoc(tool_func)
        self.sig = inspect.signature(self.func)
        self.params = self.get_params()
        if self.doc is None:
            raise Exception(TOOL_MISSING_DOCSTRING_ERROR.format(self.id))
        self.description = f"{self.id} - {self.get_tool_description(self.doc)}"

    def get_params(self):
        """
        Gets the parameters for tool
        :return: List of parameters for tool.
        """
        params = []
        for param_name, param in self.sig.parameters.items():
            if param_name in IGNORE_PARAMS:
                continue
            try:
                params.append(ToolParam(param_name, param, self.doc))
            except Exception as e:
                raise Exception(f"{self.id}.{str(e)}")
        return params

    def get_tool_args(self) -> Optional[List[Any]]:
        """
        Prompts the user to enter the args to tool
        :return: Argument to tool func.
        """
        args = []
        for param in self.params:
            user_value = param.inquirer_value(allow_back=True)
            if user_value is None:
                return None
            args.append(user_value)
        return args

    def __hash__(self) -> int:
        """
        :return: Returns hash of tool name.
        """
        return hash(self.id)

    @staticmethod
    def get_tool_description(tool_doc: str):
        """
        Returns the description of the tool.
        :param tool_doc: The doc string for tool.
        :return: The description of the function.
        """
        return tool_doc.splitlines()[0]
