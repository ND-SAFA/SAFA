import inspect
from typing import Callable, Dict, List

from tgen.scripts.toolset.core.constants import DESC_PARAM, FUNC_PARAM, IGNORE_PARAMS


class ToolSet:

    def __init__(self, tool_functions: List[Callable]):
        """
        Creates manager for running the functions.
        :param tool_functions: The functions serving as entry points to your tool set.
        """
        self.tool_functions = tool_functions
        self.tool_map, self.tool_choices = self.create_tool_map(tool_functions)
        self.tool_params = self.read_tool_params(self.tool_map)
        self.descriptions = self.create_descriptions(self.tool_map)

    def get_tool_id(self, tool_choice: str):
        """
        Returns the tool id of selected choice.
        :param tool_choice: The choice containing tool id and description.
        :return: The tool id.
        """
        tool_choices = list(self.tool_map.keys())
        for t_id, tool in self.tool_map.items():
            tool_desc = self.create_description(t_id, tool)
            if tool_choice in tool_desc:
                return t_id
        raise Exception(f"{tool_choice} not recognized, must be one of {tool_choices}")

    def get_tool_function(self, tool_id: str):
        return self.tool_map[tool_id][FUNC_PARAM]

    def get_tool_params(self, tool_id: str):
        tool_params = self.tool_params
        tool_param_names = [p[0] for p in tool_params[tool_id]]
        tool_param_descs = [p[1] for p in tool_params[tool_id]]
        tool_param_defaults = [p[2] for p in tool_params[tool_id]]
        return tool_param_names, tool_param_descs, tool_param_defaults

    @staticmethod
    def create_descriptions(tool_map) -> List[str]:
        """
        Returns printable descriptions of tools.
        :param tool_map: Map of tool id to tool contents.
        :return: List of tool descriptions.
        """
        return [ToolSet.create_description(t_id, tool) for t_id, tool in tool_map.items()]

    @staticmethod
    def create_tool_map(tool_functions: List[Callable]) -> Dict:
        """
        Creates mapping of tool name to its contents including function and description.
        :param tool_functions: List of tools to run as functions.
        :return: Tool Mapping.
        """
        tool_choices = {}
        tool_map = {}
        for tool_func in tool_functions:
            if callable(tool_func):
                tool_id = tool_func.__name__
                tool_desc = inspect.getdoc(tool_func)
                tool_desc = "" if tool_desc is None else tool_desc.splitlines()[0]
                tool_choices[tool_id] = tool_desc
                tool_map[tool_id] = {
                    "desc": tool_desc,
                    "func": tool_func
                }
            else:
                class_functions = [getattr(tool_func, f) for f in dir(tool_func) if not f.startswith("_")]
                class_functions = [f for f in class_functions if callable(f)]
                class_functions = [f for f in class_functions if getattr(f, 'climethod', False)]

                class_map, class_choices = ToolSet.create_tool_map(class_functions)
                tool_map.update(class_map)
                tool_choices.update(class_choices)
        tool_choices["Exit"] = "Leave."
        return tool_map, tool_choices

    @staticmethod
    def read_tool_params(tool_map: Dict):
        """
        Reads tool function an extracts the name and description of each parameter.
        :param tool_map: Map of tool id to tool contents including function and description.
        :return: Mapping of tool id to list of parameters and their descriptions.
        """
        tool_params = {}

        for tool_id, tool in tool_map.items():
            tool_func = tool["func"]
            sig = inspect.signature(tool_func)
            pydoc = inspect.getdoc(tool_func)
            if pydoc is None:
                raise Exception(f"{tool_func.__name__} is missing a PyDoc.")
            params = []
            for param_name, param in sig.parameters.items():
                if param_name in IGNORE_PARAMS:
                    continue
                param_default = None
                if param.default is not inspect.Parameter.empty:
                    param_default = param.default
                param_desc = ToolSet.get_param_description(pydoc, param_name)
                params.append((param_name, param_desc, param_default))
            tool_params[tool_id] = params
        return tool_params

    @staticmethod
    def get_param_description(pydoc_str, param_name):
        """
        Returns the description of parameter in DocString.
        :param pydoc_str: The PyDoc as a string.
        :param param_name: The name of the parameter whose description is returned.
        :returns: The description of parameters.
        """
        assert pydoc_str is not None, "PyDoc is missing on a tool function."
        lines = pydoc_str.split('\n')
        for line in lines:
            if f':param {param_name}:' in line:
                return line.split(f':param {param_name}:')[1].strip()
        return None

    @staticmethod
    def create_description(tool_id: str, tool_info: Dict):
        """
        Returns description of the tool.
        :param tool_id: The id of the tool
        :param tool_info: Information dictionary about the tool.
        :return: String representing description.
        """
        return f"{tool_id} - {tool_info[DESC_PARAM]}"
