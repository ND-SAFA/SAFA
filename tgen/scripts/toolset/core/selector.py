import sys
from typing import List

import inquirer

from tgen.scripts.toolset.core.constants import BACK_COMMAND, EXIT_COMMAND


def selector(options: List[str], message: str = None, allow_back: bool = False):
    """
    Prompts user to select an option.
    :param options: The options to select from.
    :param message: The message to display when selecting from options.
    :param allow_back: Allow the user to select command to move `back` in menu.
    :return: The selected option.
    """
    prompt_id = "prompt_id"
    other_commands = [EXIT_COMMAND]
    if allow_back:
        other_commands.insert(0, BACK_COMMAND)
    prompts = [inquirer.List(prompt_id, message=message, choices=options + other_commands)]
    answers = inquirer.prompt(prompts)
    selected_choice = answers[prompt_id]
    if selected_choice == EXIT_COMMAND:
        print("Bye bye :)")
        sys.exit()
    if allow_back and selected_choice == BACK_COMMAND:
        return None
    return selected_choice
