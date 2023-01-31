from enum import Enum
from typing import Any, List


class SupportedEnum(Enum):
    """
    Contains utility methods for retrieving enum values.
    """

    @classmethod
    def get_value(cls, key_name: str) -> Any:
        """
        Returns the enum value whose key matches given name.
        :param key_name: Case-insensitive key name.
        :return: Enum value.
        """
        key_name = key_name.upper()
        for k in cls._value2member_map_.values():
            if k.name == key_name:
                return k.value
        raise ValueError(f"{key_name} is not one of {cls.get_keys()}")

    @classmethod
    def get_keys(cls) -> List[str]:
        """
        :return: Returns list of keys in enum.
        """
        return [k.name for k in cls._value2member_map_.values()]
