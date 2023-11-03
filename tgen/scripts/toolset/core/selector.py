import sys
from typing import Any, List, Type

import inquirer

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.logging.logger_manager import logger
from tgen.scripts.toolset.core.constants import BACK_COMMAND, EXIT_COMMAND


def inquirer_selection(selections: List[str], message: str = None, allow_back: bool = False):
    """
    Prompts user to select an option.
    :param selections: The options to select from.
    :param message: The message to display when selecting from options.
    :param allow_back: Allow the user to select command to move `back` in menu.
    :return: The selected option.
    """
    prompt_id = "prompt_id"
    other_commands = [EXIT_COMMAND]
    if allow_back:
        other_commands.insert(0, BACK_COMMAND)
    prompts = [inquirer.List(prompt_id, message=message, choices=selections + other_commands)]
    answers = inquirer.prompt(prompts)
    selected_choice = answers[prompt_id]
    if selected_choice == EXIT_COMMAND:
        print("Bye bye :)")
        sys.exit()
    if allow_back and selected_choice == BACK_COMMAND:
        return None
    return selected_choice


def inquirer_value(message: str, class_type: Type, default_value: Any):
    """
    Prompts user with message for a value.
    :param message: The message to prompt user with.
    :param class_type: The type of value to expect back.
    :param default_value: The default value to use if optional.
    :return: The value after parsing user response.
    """
    message += f"- {class_type.__name__} -"
    if default_value is not None:
        message += f"({default_value})"
    user_value = inquirer.text(message=message)
    if user_value.strip() == EMPTY_STRING:
        if default_value is None:
            raise Exception("Required field received empty value.")
        logger.info("Default value used.")
        return default_value
    return class_type(user_value)
