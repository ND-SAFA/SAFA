from typing import Callable, Dict, List, Optional

from common_resources.tools.cli.inquirer_selector import inquirer_selection

from tgen.scripts.toolset.tool import Tool


class ToolSet:

    def __init__(self, tool_functions: List[Callable]):
        """
        Creates manager for running the functions.
        :param tool_functions: The functions serving as entry points to your tool set.
        """
        self.tool_functions = tool_functions
        self.tool_map = self.create_tool_map(tool_functions)

    def get_tool_id(self, tool_choice: str):
        """
        Returns the tool id of selected choice.
        :param tool_choice: The choice containing tool id and description.
        :return: The tool id.
        """
        tool_choices = list(self.tool_map.keys())
        for t_id, tool in self.tool_map.items():
            if tool_choice in tool.description:
                return t_id
        raise Exception(f"{tool_choice} not recognized, must be one of {tool_choices}")

    def get_tool_descriptions(self) -> List[str]:
        """
        Gets descriptions for tools in tool map.
        :return: List of tool descriptions.
        """
        return [t.description for t in self.tool_map.values()]

    def inquire_tool(self) -> Optional[Tool]:
        """
        Prompts user to select a tool. If back is selected then None is returned.
        :return: The selected tool.
        """
        selected_choice = inquirer_selection(self.get_tool_descriptions(), "Choose a tool to run:", allow_back=True)
        if selected_choice is None:
            return None
        tool_id = self.get_tool_id(selected_choice)
        tool = self.tool_map[tool_id]
        return tool

    @staticmethod
    def create_tool_map(tool_functions: List[Callable]) -> Dict[str, Tool]:
        """
        Creates mapping of tool name to its contents including function and description.
        :param tool_functions: List of tools to run as functions.
        :return: Tool Mapping.
        """
        tool_choices = {}
        tool_map = {}
        for tool_func in tool_functions:
            tool = Tool(tool_func)
            tool_map[tool.id] = tool
        tool_choices["Exit"] = "Leave."
        return tool_map
