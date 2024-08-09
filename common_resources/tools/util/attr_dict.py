from typing import Any


class AttrDict(dict):
    """
    Allows attribute access using . notation
    """

    def __getattr__(self, key: Any):
        """
        Overrides the error message if attribute does not exist.
        :param key: The key to extract from dictionary.
        :return: The value of the key.
        """
        if key in self:
            return self[key]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")


