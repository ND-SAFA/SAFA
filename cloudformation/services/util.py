from copy import deepcopy
from typing import Dict


def print_params(parameters: Dict, **kwargs) -> None:
    """
    Prints the override values.
    :param parameters: Key-value pairs to pass as parameters.
    :return: None
    """
    printables = deepcopy(parameters)
    printables.update(kwargs)
    for k, v in printables.items():
        print(f"{k}:{v}")
