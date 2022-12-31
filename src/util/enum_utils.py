from enum import Enum
from typing import Type

SEP_SYM = "_"


def get_enum_from_name(enum_class: Type, enum_name: str) -> Enum:
    """
    Gets the enum
    :param enum_class: the enum class
    :param enum_name: the name of the specific enum to retrieve
    :return: the enum
    """
    enum_name = enum_name.upper()
    if SEP_SYM not in enum_name:
        for e in enum_class:
            name_removed_sep = "".join(e.name.split(SEP_SYM))
            if name_removed_sep == enum_name:
                return e
    try:
        return enum_class[enum_name]
    except:
        raise ValueError("%s does not have value: %s" % (enum_class, enum_name))
