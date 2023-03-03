from enum import Enum
from typing import Callable, Type, Union, Dict, Any, OrderedDict

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


def to_string(item: Union[Enum, str]) -> str:
    """
    Converts enum to string if item is an enum
    :param item: The item as a string or enum
    :return: The item as a string
    """
    if isinstance(item, Enum):
        item = item.value
    return item


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


class EnumDict(OrderedDict):

    def __init__(self, dict_: Dict[Union[str, Enum], Any]):
        """
        Dictionary that accepts enum or enum value as key
        :param dict_: A dictionary containing enum or enum value as key
        """
        dict_ = {to_string(key): val for key, val in dict_.items()}
        super().__init__(dict_)

    def __contains__(self, item: Union[str, Enum]) -> bool:
        """
        Returns True if item in dictionary else False
        :param item: Dictionary key as enum or str
        :return: True if item in dictionary else False
        """
        return super().__contains__(to_string(item))

    def __getitem__(self, item: Union[str, Enum]) -> Any:
        """
        Returns the dictionary item
        :param item: Dictionary key as enum or str
        :return: The dictionary item
        """
        return super().__getitem__(to_string(item))

    def __setitem__(self, key: Union[str, Enum], value: Any) -> None:
        """
        Sets the given key to the given value
        :param key: Dictionary key as enum or str
        :param value: Value to set the key
        :return: None
        """
        return super().__setitem__(to_string(key), value)
