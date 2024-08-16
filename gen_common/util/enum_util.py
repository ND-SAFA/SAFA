from collections import OrderedDict
from enum import Enum
from typing import Any, Callable, Dict, Type, Union, Optional

from gen_common.constants import UNDERSCORE, EMPTY_STRING

SEP_SYM = UNDERSCORE


class EnumUtil:

    @staticmethod
    def get_enum_from_name(enum_class: Type, enum_name: str, raise_exception: bool = True) -> Optional[Enum]:
        """
        Gets the enum
        :param enum_class: the enum class
        :param enum_name: the name of the specific enum to retrieve
        :param raise_exception: If True, raises an exception if the enum cannot be found.
        :return: the enum
        """
        enum_name = enum_name.upper()
        if SEP_SYM not in enum_name:
            for e in enum_class:
                name_removed_sep = EMPTY_STRING.join(e.name.split(SEP_SYM))
                if name_removed_sep == enum_name:
                    return e
        try:
            return enum_class[enum_name]
        except Exception:
            if raise_exception:
                raise ValueError("%s does not have value: %s" % (enum_class, enum_name))
            return

    @staticmethod
    def get_enum_from_value(enum_class: Type, enum_val: Any) -> Enum:
        """
        Gets the enum with the corresponding value
        :param enum_class: The enum class to get the enum from
        :param enum_val: The value to get the enum for
        :return: The enum with the corresponding value
        """
        for e in enum_class:
            if e.value == enum_val:
                return e

    @staticmethod
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

    def __init__(self, dict_: Dict[Union[str, Enum], Any] = None, **kwargs):
        """
        Dictionary that accepts enum or enum value as key
        :param dict_: A dictionary containing enum or enum value as key
        """
        dict_ = [(EnumUtil.to_string(key), val) for key, val in dict_.items()] if dict_ is not None else []
        kwargs = {EnumUtil.to_string(key): val for key, val in kwargs.items()}
        super().__init__(dict_, **kwargs)

    def get(self, key: Union[str, Enum], default: Any = None) -> Any:
        """
        Get an item if it exists or return default
        :param key: The key to get
        :param default: default value to return
        :return: The value if it exists else default
        """
        return super().get(EnumUtil.to_string(key), default)

    def __contains__(self, item: Union[str, Enum]) -> bool:
        """
        Returns True if item in dictionary else False
        :param item: Dictionary key as enum or str
        :return: True if item in dictionary else False
        """
        return super().__contains__(EnumUtil.to_string(item))

    def __getitem__(self, item: Union[str, Enum]) -> Any:
        """
        Returns the dictionary item
        :param item: Dictionary key as enum or str
        :return: The dictionary item
        """
        return super().__getitem__(EnumUtil.to_string(item))

    def __setitem__(self, key: Union[str, Enum], value: Any) -> None:
        """
        Sets the given key to the given value
        :param key: Dictionary key as enum or str
        :param value: Value to set the key
        :return: None
        """
        return super().__setitem__(EnumUtil.to_string(key), value)
