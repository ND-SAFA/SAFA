from typing import List

from gen_common.constants.symbol_constants import COMMA


class CustomReprFunc:

    def __init__(self, f, custom_repr):
        """
        Wraps a function to have a __repr__
        :param f: The function being decorated.
        :param custom_repr: The custom representation method.
        """
        self.f = f
        self.custom_repr = custom_repr

    def __call__(self, *args, **kwargs):
        """
        Delegates call to function back to base function.
        :param args: Positional args.
        :param kwargs: Keywords args.
        :return: The return value of the base function.
        """
        return self.f(*args, **kwargs)

    def __repr__(self):
        """
        :return: Returns the custom repre.
        """
        return self.custom_repr(self.f)


def set_repr(custom_repr):
    """
    The decorator used to wrap functions with a custom repr.
    :param custom_repr: The custom repr function top use.
    :return: The wrapped function.
    """

    def set_repr_decorator(f) -> CustomReprFunc:
        """
        Internal decorator using custom repr to wrap function.
        :param f: The function to wrap.
        :return: The wrapped function.
        """
        return CustomReprFunc(f, custom_repr)

    return set_repr_decorator


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
