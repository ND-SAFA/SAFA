from enum import Enum
from typing import Callable, Type

SEP_SYM = "_"


class FunctionalWrapper:
    """
    Wraps functions within class to allow them to be used as values in enum.
    """

    def __init__(self, f: Callable):
        """
        Constructs wrapper for given function.
        :param f: The function to wrap and use as enum.
        """
        self.f = f

    def __call__(self, *args, **kwargs):
        """
        Calls wrapped function.
        :param args: Argument to function
        :param kwargs: Additional arguments to function.
        :return: Output of function.
        """
        return self.f(*args, **kwargs)


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