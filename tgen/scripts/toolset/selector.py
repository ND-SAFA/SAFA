import sys
from typing import Any, List, Type

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.logging.logger_manager import logger
from tgen.scripts.constants import BACK_COMMAND, DEFAULT_ALLOW_BACK, EXIT_COMMAND, EXIT_MESSAGE, \
    REQUIRED_FIELD_ERROR


def inquirer_selection(commands: List[str], message: str = None, allow_back: bool = DEFAULT_ALLOW_BACK):
    """
    Prompts user to select an option.
    :param commands: The options to select from.
    :param message: The message to display when selecting from options.
    :param allow_back: Allow the user to select command to move `back` in menu.
    :return: The selected option.
    """

    other_commands = [EXIT_COMMAND]
    if allow_back:
        other_commands.insert(0, BACK_COMMAND)
    selections_prompt = create_selection_prompt(commands)
    other_commands_prompt = create_selection_prompt(other_commands, len(commands))
    selections_message = f"--- {message} ---\n{selections_prompt}\n\n{other_commands_prompt}\n>"
    user_input = input(selections_message)
    try:
        selected_index = int(user_input)
    except:
        raise Exception("Expected an int.")
    all_commands = commands + other_commands
    selected_choice = all_commands[int(selected_index)]
    if selected_choice == EXIT_COMMAND:
        logger.info(EXIT_MESSAGE)
        sys.exit()
    if allow_back and selected_choice == BACK_COMMAND:
        return None
    return selected_choice


def inquirer_value(message: str, class_type: Type, default_value: Any = None, allow_back: bool = DEFAULT_ALLOW_BACK):
    """
    Prompts user with message for a value.
    :param message: The message to prompt user with.
    :param class_type: The type of value to expect back.
    :param default_value: The default value to use if optional.
    :param allow_back: Allow the user to type back command.
    :return: The value after parsing user response.
    """
    annotation_name = class_type.__name__ if hasattr(class_type, "__name__") else repr(class_type)
    message += f" - {annotation_name}"
    if default_value is not None:
        message += f" ({default_value})"
    message = message + ": "
    user_value = input(message)
    if allow_back and user_value.lower() == BACK_COMMAND:
        return None
    if class_type is list:  # TODO: Support list of ints, bools, and floats.
        return user_value.split(",")
    if user_value.strip() == EMPTY_STRING:
        if default_value is None:
            raise Exception(REQUIRED_FIELD_ERROR)
        user_value = default_value
    return class_type(user_value)


def create_selection_prompt(selections: List[str], start: int = 0):
    """
    Creates a prompt containing all selections.
    :param selections:
    :param start:
    :return:
    """
    options = [f"{i + start}) {s}" for i, s in enumerate(selections)]
    selections_message = NEW_LINE.join(options)
    return selections_message
