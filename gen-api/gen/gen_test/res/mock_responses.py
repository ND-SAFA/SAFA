from copy import deepcopy


class MockResponses:

    def __getattr__(self, item: str):
        """
        Returns a copy of the requested attribute.
        :param item: The name of the attribute.
        :return: The value of the attribute.
        """
        item_value = super().__getattribute__(item)
        return deepcopy(item_value)
