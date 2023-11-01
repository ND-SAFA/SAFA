import sys

from tool_registry import TOOLS

sys.path.append("sys")

import inquirer
from dotenv import load_dotenv

from tool_manager import ToolManager

TOOL_RUNNER_NAME = "Tool Runner"
EXIT_COMMAND = "Exit"


def main_menu(tool_manager: ToolManager):
    return [
        inquirer.List(TOOL_RUNNER_NAME,
                      message="Choose a tool to run:",
                      choices=tool_manager.descriptions + [EXIT_COMMAND],
                      ),
    ]


def select_tool(tool_manager: ToolManager, default_tool_id: str = None, *args):
    while True:
        if default_tool_id:
            tool_id = tool_manager.get_tool_id(default_tool_id)
        else:
            # Prompt user: show the main menu and prompt the user for input
            answers = inquirer.prompt(main_menu(tool_manager))
            selected_choice = answers[TOOL_RUNNER_NAME]
            if selected_choice == EXIT_COMMAND:
                break
            tool_id = tool_manager.get_tool_id(selected_choice)

            # Perform selected command
            tool_param_names, tool_param_descs, tool_param_defaults = tool_manager.get_tool_params(tool_id)
            args = []
            for param_name, param_desc, param_default in zip(tool_param_names, tool_param_descs, tool_param_defaults):
                param_message = f"{param_name} - {param_desc}"
                if param_default is not None:
                    param_message += f"({param_default})"
                arg = inquirer.text(message=param_message)
                arg = param_default if arg == "" else arg
                args.append(arg)
        tool_func = tool_manager.get_tool_function(tool_id)
        tool_func(*args)
        print(f"{tool_id} finished.")  # add a blank line after the output


if __name__ == "__main__":
    load_dotenv()
    select_tool(ToolManager(TOOLS))
