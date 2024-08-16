from typing import List

from gen_common.constants.symbol_constants import COMMA

OPTIONAL_KEY = "_OPTIONAL"


def bool_constructor(s: str):
    """
    The default boolean constructor that uses bool reprbut is able to parse wide range of true responses.
    :param s: The string to construct into a boolean.
    :return: The boolean constructed.
    """
    return s.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


def list_constructor(s: str, delimiter: str = COMMA) -> List[str]:
    """
    Constructs a list from a string by splitting the string on delimiter.
    :param s: The string to convert to list.
    :param delimiter: The delimiter to use to create list.
    :return: The list of strings.
    """
    return s.split(delimiter)


SUPPORTED_TYPES_RQ = {
    int: int,
    float: float,
    str: str,
    bool: bool_constructor,
    list: list_constructor
}
MISSING_DEFINITION_ERROR = "{} does not exists."
RQ_INQUIRER_CONFIRM_MESSAGE = "Are these the correct values?"
RQ_VARIABLE_START = "["
RQ_VARIABLE_REGEX = r'\[([^\[\]]+)\]'
