import sys
from typing import Any, List, Type

import inquirer

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.logging.logger_manager import logger
from tgen.scripts.constants import BACK_COMMAND, DEFAULT_ALLOW_BACK, DEFAULT_VALUE_MESSAGE, EXIT_COMMAND, EXIT_MESSAGE, \
    REQUIRED_FIELD_ERROR, \
    SINGLETON_PROMPT_ID


def inquirer_selection(selections: List[str], message: str = None, allow_back: bool = DEFAULT_ALLOW_BACK):
    """
    Prompts user to select an option.
    :param selections: The options to select from.
    :param message: The message to display when selecting from options.
    :param allow_back: Allow the user to select command to move `back` in menu.
    :return: The selected option.
    """

    other_commands = [EXIT_COMMAND]
    if allow_back:
        other_commands.insert(0, BACK_COMMAND)
    prompts = [inquirer.List(SINGLETON_PROMPT_ID, message=message, choices=selections + other_commands)]
    answers = inquirer.prompt(prompts)
    selected_choice = answers[SINGLETON_PROMPT_ID]
    if selected_choice == EXIT_COMMAND:
        logger.info(EXIT_MESSAGE)
        sys.exit()
    if allow_back and selected_choice == BACK_COMMAND:
        return None
    return selected_choice


def inquirer_value(message: str, class_type: Type, default_value: Any, allow_back: bool = DEFAULT_ALLOW_BACK):
    """
    Prompts user with message for a value.
    :param message: The message to prompt user with.
    :param class_type: The type of value to expect back.
    :param default_value: The default value to use if optional.
    :return: The value after parsing user response.
    """
    annotation_name = class_type.__name__ if hasattr(class_type, "__name__") else repr(class_type)
    message += f" - {annotation_name} -"
    if default_value is not None:
        message += f" ({default_value})"
    user_value = inquirer.text(message=message)
    if allow_back and user_value.lower() == BACK_COMMAND:
        return None
    if class_type is list:  # TODO: Support list of ints, bools, and floats.
        return user_value.split(",")
    if user_value.strip() == EMPTY_STRING:
        if default_value is None:
            raise Exception(REQUIRED_FIELD_ERROR)
        logger.info(DEFAULT_VALUE_MESSAGE)
        return default_value
    return class_type(user_value)
