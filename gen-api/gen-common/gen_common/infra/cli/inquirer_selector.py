import sys
from typing import Any, Callable, List, Type

from gen_common.constants.cli_constants import EXIT_COMMAND, BACK_COMMAND, EXIT_MESSAGE, REQUIRED_FIELD_ERROR
from gen_common.infra.t_logging.logger_manager import logger

from gen_common.constants.symbol_constants import F_SLASH, EMPTY_STRING, NEW_LINE


def get_choice(menu_options: List[str], message: str = EMPTY_STRING) -> str:
    """
    Gets the users choice from the menu options
    :param menu_options: Options given to the user
    :param message: The message to display
    :return: The user's choice
    """
    possible_choices = [str(i + 1) for i in range(len(menu_options))]
    menu = NEW_LINE.join([f"{i}) {option}" for i, option in zip(possible_choices, menu_options)])
    print(message)
    print(menu)
    choice = input(f"Select an option ({F_SLASH.join(possible_choices)}): {NEW_LINE}").strip()
    try:
        assert choice in possible_choices
        choice = int(choice)
        selected_options = menu_options[choice - 1]
    except (TypeError, AssertionError):
        print(f"Unknown input {choice}. Please try again {NEW_LINE}")
        selected_options = None
    return selected_options


def inquirer_selection(selections: List[str], message: str = None, allow_back: bool = False):
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
    selections_message = f"--- {message} --->"
    menu_options = selections + other_commands
    selected_choice = get_choice(menu_options, selections_message)

    if selected_choice == EXIT_COMMAND:
        logger.info(EXIT_MESSAGE)
        sys.exit()
    if allow_back and selected_choice == BACK_COMMAND:
        return None
    return selected_choice


def inquirer_value(message: str, class_type: Type, type_constructor: Callable = None,
                   default_value: Any = None, allow_back: bool = False,
                   is_required: bool = True):
    """
    Prompts user with message for a value.
    :param message: The message to prompt user with.
    :param class_type: The type of value to expect back.
    :param type_constructor: Responsible for converting the input to the correct type.
    :param default_value: The default value to use if optional.
    :param allow_back: Allow the user to type back command.
    :param is_required: If True, then the user is required to supply a value (unless a default is provided) else may be blank
    :return: The value after parsing user response.
    """
    annotation_name = class_type.__name__ if hasattr(class_type, "__name__") else repr(class_type)
    message += f" - {annotation_name}"
    if default_value is not None:
        message += f" ({default_value})"
    elif is_required:
        message += "*"
    else:
        message += " (Optional)"
    message = message + ": "

    user_value = input(message)
    if allow_back and user_value.lower() == BACK_COMMAND:
        return None
    if user_value.strip() == EMPTY_STRING:
        if default_value is None and is_required:
            raise Exception(REQUIRED_FIELD_ERROR)
        user_value = default_value
    if user_value is not None and not isinstance(user_value, class_type):
        user_value = class_type(user_value) if not type_constructor else type_constructor(user_value)
    return user_value
