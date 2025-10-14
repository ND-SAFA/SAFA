from typing import Any, Dict


class UncasedDict(dict):
    # TODO : Test that updates with uncased dictionaries work as expect
    def __init__(self, dict_: Dict[Any, Any] = None):
        """
        Represents a dictionary whose keys are uncased
        :param dict_: the dictionary to represent
        """
        super().__init__()
        if dict_:
            self.__initialize_as_dict(dict_)

    def rename_property(self, prop: str, new_prop: str) -> Dict[str, Any]:
        """
        Renames the given property to a new name
        :param prop: the original property name
        :param new_prop: new property name
        :return: the updated dictionary
        """
        converted_dict = self.copy()
        for key, value in self.items():
            if isinstance(value, UncasedDict):
                value = value.rename_property(prop, new_prop)
            if key == prop:
                key = new_prop
            converted_dict[key] = value
        return converted_dict

    def __initialize_as_dict(self, dict_: Dict[Any, Any]) -> None:
        """
        Moves the input dictionary into its own internal dictionary representation
        :param dict_: input dictionary to set internal attributes
        :return: None
        """
        for key, val in dict_.items():
            self[key] = val

    @staticmethod
    def _process_key(key: str) -> str:
        """
        Ensures the key is always in the correct case, etc.
        :param key: the key to process
        :return: the processed key
        """
        if isinstance(key, str):
            return key.lower()
        return key

    @staticmethod
    def _process_value(value: Any):
        """
        Ensures the value is always in the correct format
        :param value: the value to process
        :return: the processed value
        """
        if isinstance(value, dict) and not isinstance(value, UncasedDict):
            processed_value = UncasedDict()
            for key, val in value.items():
                processed_value[key] = val
            return processed_value
        return value

    def get(self, key, *args, **kwargs) -> Any:
        """
        Gets item in dictionary.
        :param key: The key to get item at.
        :param args: Positional arguments passed to get.
        :param kwargs: Keyword arguments passed to get.
        :return: Item with given key.
        """
        processed_key = self._process_key(key)
        return super().get(processed_key, *args, **kwargs)

    def __getitem__(self, key: str) -> Any:
        """
        Returns value matching the given key in the dictionary
        :param key: the key to the results dictionary
        :return: the value from the results dictionary
        """
        processed_key = self._process_key(key)
        return super().get(processed_key)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Sets the key to be mapped to the given value in the dictionary
        :param key: the key to the results dictionary
        :param value: the value to be mapped to the key in the results dictionary
        :return: None
        """
        super().__setitem__(self._process_key(key), self._process_value(value))

    def __contains__(self, key: str) -> bool:
        """
        Returns True if the key is in the results dictionary
        :param key: the key to the results dictionary
        :return: True if the key is in the results dictionary else False
        """
        return super().__contains__(self._process_key(key))
