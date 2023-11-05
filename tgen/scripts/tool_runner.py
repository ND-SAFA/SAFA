import os
import sys
from typing import Callable, Dict, List

from dotenv import load_dotenv

from tgen.scripts.find_missing_docs import print_missing_headers
from tgen.scripts.toolset.core.tool import Tool

load_dotenv()
root_path = os.path.expanduser(os.environ["ROOT_PATH"])
sys.path.append(root_path)

from tgen.scripts.toolset.core.selector import inquirer_selection
from tgen.scripts.toolset.core.tool_set import ToolSet
from tgen.scripts.toolset.tools.rq_tools import RQ_TOOLS
from tgen.scripts.toolset.tools.s3_tools import S3_TOOLS


def tool_runner_loop(tool_set_map: Dict[str, List[Callable]], default_tool_set_name: str = None, default_tool_id: str = None, *args):
    """
    Prompts user to select and run tools.
    :param tool_set_map: Map of tool set names and their functions.
    :param default_tool_set_name: The default tool set to run.
    :param default_tool_id: The default tool to run inside of default tool set.
    :param args: Args to run default tool with.
    :return: None
    """
    exit_loop = False

    while not exit_loop:
        if default_tool_id:
            tools = tool_set_map[default_tool_set_name]
            tool_set = ToolSet(tools)
            tool: Tool = tool_set.tool_map[default_tool_id]
            exit_loop = True
        else:
            default_tool_set_name = inquirer_selection(list(tool_set_map.keys()), "Select tool set")
            tools = tool_set_map[default_tool_set_name]
            tool_set = ToolSet(tools)
            if len(tools) == 1:
                tool = list(tool_set.tool_map.values())[0]
            else:
                tool = tool_set.inquire_tool()
                if tool is None:
                    continue

            args = tool.get_tool_args()
            if args is None:
                continue
        tool.func(*args)
    print(f"\n:-)\n")  # add a blank line after the output


TOOLS = {
    "Data": S3_TOOLS,
    "Run RQ": RQ_TOOLS,
    "Dev-Ops": [print_missing_headers]
}
if __name__ == "__main__":
    tool_runner_loop(TOOLS)
