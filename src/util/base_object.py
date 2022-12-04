from typing import get_type_hints
from experiments.variables.definition_variable import DefinitionVariable


class BaseObject:
    test: str

    def __init__(self, param_dict: DefinitionVariable = None):
        """
        Initializes the object from a dictionary
        :param param_dict: a dictionary of the necessary params to initialize
        :return: the initialize object
        """
        print(get_type_hints(BaseObject.__init__))
        for attr_name, attr_value in param_dict.items():
            if hasattr(self, attr_name):
                if isinstance(attr_value, DefinitionVariable):
                    pass


if __name__ == "__main__":
    BaseObject({"test": 1})
